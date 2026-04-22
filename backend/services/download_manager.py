import asyncio
from typing import Dict, List, Optional, Callable
from datetime import datetime
from sqlalchemy.orm import Session
from ..database import DownloadTaskDB, SessionLocal
from ..models import DownloadTask, DownloadStatus
from .yt_dlp_executor import YtDlpExecutor


class DownloadManager:
    """非同期ダウンロード管理"""
    
    def __init__(self, max_concurrent: int = 3):
        self.max_concurrent = max_concurrent
        self.task_queue: asyncio.Queue = asyncio.Queue()
        self.active_tasks: Dict[int, asyncio.Task] = {}
        self.progress_callbacks: Dict[int, Callable] = {}
        self.executors: Dict[int, YtDlpExecutor] = {}
        self.yt_dlp_path: Optional[str] = None
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.running = False
        self.worker_tasks: List[asyncio.Task] = []
    
    def set_yt_dlp_path(self, path: str):
        """yt-dlp バイナリパスを設定"""
        self.yt_dlp_path = path
    
    async def start(self):
        """ダウンロード管理を開始"""
        self.running = True
        # ワーカーを起動
        for _ in range(self.max_concurrent):
            worker = asyncio.create_task(self._worker())
            self.worker_tasks.append(worker)
    
    async def stop(self):
        """ダウンロード管理を停止"""
        self.running = False
        for worker in self.worker_tasks:
            worker.cancel()
        self.worker_tasks.clear()
        for task in list(self.active_tasks.values()):
            task.cancel()
        self.active_tasks.clear()
        self.executors.clear()
        self.progress_callbacks.clear()
    
    async def add_download(self, task: DownloadTask, progress_callback: Optional[Callable] = None) -> int:
        """ダウンロードをキューに追加"""
        db = SessionLocal()
        
        # DB に保存
        db_task = DownloadTaskDB(
            url=task.url,
            profile_id=task.profile_id,
            parameters=task.parameters,
            output_path=task.output_path,
            status=DownloadStatus.PENDING,
            created_at=datetime.utcnow(),
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        
        task_id = db_task.id
        
        # コールバック登録
        if progress_callback:
            self.progress_callbacks[task_id] = progress_callback
        
        # キューに追加
        await self.task_queue.put((task_id, task))
        
        db.close()
        return task_id
    
    async def _worker(self):
        """ダウンロードワーカー"""
        while self.running:
            try:
                task_id, task = await asyncio.wait_for(self.task_queue.get(), timeout=1.0)
            except asyncio.TimeoutError:
                continue
            
            db = SessionLocal()
            db_task = db.query(DownloadTaskDB).filter(DownloadTaskDB.id == task_id).first()
            if not db_task or db_task.status != DownloadStatus.PENDING:
                db.close()
                continue
            db.close()
            
            async with self.semaphore:
                current = asyncio.current_task()
                if current is not None:
                    self.active_tasks[task_id] = current
                try:
                    await self._execute_download(task_id, task)
                finally:
                    self.active_tasks.pop(task_id, None)
    
    async def _execute_download(self, task_id: int, task: DownloadTask):
        """ダウンロード実行"""
        db = SessionLocal()
        
        try:
            if not self.yt_dlp_path:
                raise RuntimeError("yt-dlp path is not configured")
            
            db_task = db.query(DownloadTaskDB).filter(DownloadTaskDB.id == task_id).first()
            if not db_task:
                raise RuntimeError("Download task not found")
            
            db_task.status = DownloadStatus.DOWNLOADING
            db_task.started_at = datetime.utcnow()
            db.commit()
            
            executor = YtDlpExecutor(self.yt_dlp_path)
            self.executors[task_id] = executor
            
            if task_id in self.progress_callbacks:
                async def progress_callback(progress_info):
                    callback_db = SessionLocal()
                    try:
                        callback_task = callback_db.query(DownloadTaskDB).filter(DownloadTaskDB.id == task_id).first()
                        if callback_task:
                            callback_task.progress_percent = progress_info.get("percent", 0.0)
                            callback_task.speed = progress_info.get("speed")
                            callback_task.eta = progress_info.get("eta")
                            callback_db.commit()
                    finally:
                        callback_db.close()
                    
                    if task_id in self.progress_callbacks:
                        await self.progress_callbacks[task_id](progress_info)
                executor.set_progress_callback(progress_callback)
            
            result = await executor.execute(
                task.url,
                task.parameters,
                task.output_path or "%(title)s.%(ext)s"
            )
            
            db_task = db.query(DownloadTaskDB).filter(DownloadTaskDB.id == task_id).first()
            if db_task:
                if result.get("success"):
                    db_task.status = DownloadStatus.COMPLETED
                    db_task.current_filename = result.get("filename")
                else:
                    db_task.status = DownloadStatus.FAILED
                    db_task.error_message = result.get("error")
                db_task.completed_at = datetime.utcnow()
                db.commit()
        except asyncio.CancelledError:
            db_task = db.query(DownloadTaskDB).filter(DownloadTaskDB.id == task_id).first()
            if db_task:
                db_task.status = DownloadStatus.CANCELLED
                db_task.completed_at = datetime.utcnow()
                db.commit()
            raise
        except Exception as e:
            db_task = db.query(DownloadTaskDB).filter(DownloadTaskDB.id == task_id).first()
            if db_task:
                db_task.status = DownloadStatus.FAILED
                db_task.error_message = str(e)
                db_task.completed_at = datetime.utcnow()
                db.commit()
        finally:
            db.close()
            self.executors.pop(task_id, None)
            self.progress_callbacks.pop(task_id, None)
    
    async def pause_download(self, task_id: int):
        """ダウンロード一時停止"""
        db = SessionLocal()
        db_task = db.query(DownloadTaskDB).filter(DownloadTaskDB.id == task_id).first()
        
        if db_task and db_task.status == DownloadStatus.DOWNLOADING:
            db_task.status = DownloadStatus.PAUSED
            db.commit()
            
            executor = self.executors.get(task_id)
            if executor:
                executor.pause()
        
        db.close()
    
    async def resume_download(self, task_id: int):
        """ダウンロード再開"""
        db = SessionLocal()
        db_task = db.query(DownloadTaskDB).filter(DownloadTaskDB.id == task_id).first()
        
        if db_task and db_task.status == DownloadStatus.PAUSED:
            db_task.status = DownloadStatus.DOWNLOADING
            db.commit()
            
            executor = self.executors.get(task_id)
            if executor:
                executor.resume()
        
        db.close()
    
    async def cancel_download(self, task_id: int):
        """ダウンロードキャンセル"""
        db = SessionLocal()
        db_task = db.query(DownloadTaskDB).filter(DownloadTaskDB.id == task_id).first()
        
        if db_task:
            db_task.status = DownloadStatus.CANCELLED
            db_task.completed_at = datetime.utcnow()
            db.commit()
            
            executor = self.executors.get(task_id)
            if executor:
                executor.cancel()
            
            if task_id in self.active_tasks:
                self.active_tasks[task_id].cancel()
        
        db.close()
    
    async def get_task_status(self, task_id: int) -> Optional[DownloadTask]:
        """タスク状態を取得"""
        db = SessionLocal()
        db_task = db.query(DownloadTaskDB).filter(DownloadTaskDB.id == task_id).first()
        db.close()
        
        if not db_task:
            return None
        
        return DownloadTask(
            id=db_task.id,
            url=db_task.url,
            status=db_task.status,
            progress_percent=db_task.progress_percent,
            speed=db_task.speed,
            eta=db_task.eta,
            current_filename=db_task.current_filename,
            error_message=db_task.error_message,
        )
    
    async def get_queue(self) -> List[DownloadTask]:
        """キュー内のタスク一覧を取得"""
        db = SessionLocal()
        db_tasks = db.query(DownloadTaskDB).filter(
            DownloadTaskDB.status.in_([DownloadStatus.PENDING, DownloadStatus.DOWNLOADING])
        ).all()
        db.close()
        
        return [
            DownloadTask(
                id=t.id,
                url=t.url,
                status=t.status,
                progress_percent=t.progress_percent,
                speed=t.speed,
                eta=t.eta,
                current_filename=t.current_filename,
            )
            for t in db_tasks
        ]
