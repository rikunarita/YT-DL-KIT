import asyncio
from typing import Dict, List, Optional, Callable
from datetime import datetime
from sqlalchemy.orm import Session
from database import DownloadTaskDB, SessionLocal, DownloadStatus
from models import DownloadTask
from services.yt_dlp_executor import YtDlpExecutor


class DownloadManager:
    """非同期ダウンロード管理"""
    
    def __init__(self, max_concurrent: int = 3):
        self.max_concurrent = max_concurrent
        self.task_queue: asyncio.Queue = asyncio.Queue()
        self.active_tasks: Dict[int, asyncio.Task] = {}
        self.progress_callbacks: Dict[int, Callable] = {}
        self.yt_dlp_executor: Optional[YtDlpExecutor] = None
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.running = False
    
    def set_yt_dlp_executor(self, executor: YtDlpExecutor):
        """yt-dlp Executor を設定"""
        self.yt_dlp_executor = executor
    
    async def start(self):
        """ダウンロード管理を開始"""
        self.running = True
        # ワーカーを起動
        for i in range(self.max_concurrent):
            asyncio.create_task(self._worker())
    
    async def stop(self):
        """ダウンロード管理を停止"""
        self.running = False
        # アクティブなタスクをすべてキャンセル
        for task_id, task in self.active_tasks.items():
            task.cancel()
    
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
            
            # セマフォで並列数を制限
            async with self.semaphore:
                await self._execute_download(task_id, task)
    
    async def _execute_download(self, task_id: int, task: DownloadTask):
        """ダウンロード実行"""
        db = SessionLocal()
        
        try:
            # ステータスを DOWNLOADING に更新
            db_task = db.query(DownloadTaskDB).filter(DownloadTaskDB.id == task_id).first()
            db_task.status = DownloadStatus.DOWNLOADING
            db_task.started_at = datetime.utcnow()
            db.commit()
            
            # プログレスコールバック設定
            if self.yt_dlp_executor and task_id in self.progress_callbacks:
                async def progress_callback(progress_info):
                    db_task = db.query(DownloadTaskDB).filter(DownloadTaskDB.id == task_id).first()
                    db_task.progress_percent = progress_info.get("percent", 0.0)
                    db_task.speed = progress_info.get("speed")
                    db_task.eta = progress_info.get("eta")
                    db.commit()
                    
                    # ユーザーコールバック
                    if task_id in self.progress_callbacks:
                        await self.progress_callbacks[task_id](progress_info)
                
                self.yt_dlp_executor.set_progress_callback(progress_callback)
            
            # ダウンロード実行
            if self.yt_dlp_executor:
                result = await self.yt_dlp_executor.execute(
                    task.url,
                    task.parameters,
                    task.output_path or "%(title)s.%(ext)s"
                )
                
                # 結果を DB に保存
                db_task = db.query(DownloadTaskDB).filter(DownloadTaskDB.id == task_id).first()
                
                if result["success"]:
                    db_task.status = DownloadStatus.COMPLETED
                    db_task.current_filename = result.get("filename")
                else:
                    db_task.status = DownloadStatus.FAILED
                    db_task.error_message = result.get("error")
                
                db_task.completed_at = datetime.utcnow()
                db.commit()
            
        except asyncio.CancelledError:
            # キャンセルされた場合
            db_task = db.query(DownloadTaskDB).filter(DownloadTaskDB.id == task_id).first()
            db_task.status = DownloadStatus.CANCELLED
            db_task.completed_at = datetime.utcnow()
            db.commit()
        
        except Exception as e:
            # エラー処理
            db_task = db.query(DownloadTaskDB).filter(DownloadTaskDB.id == task_id).first()
            db_task.status = DownloadStatus.FAILED
            db_task.error_message = str(e)
            db_task.completed_at = datetime.utcnow()
            db.commit()
        
        finally:
            db.close()
            # コールバック削除
            if task_id in self.progress_callbacks:
                del self.progress_callbacks[task_id]
    
    async def pause_download(self, task_id: int):
        """ダウンロード一時停止"""
        db = SessionLocal()
        db_task = db.query(DownloadTaskDB).filter(DownloadTaskDB.id == task_id).first()
        
        if db_task and db_task.status == DownloadStatus.DOWNLOADING:
            db_task.status = DownloadStatus.PAUSED
            db.commit()
            
            # Executor に通知
            if self.yt_dlp_executor:
                self.yt_dlp_executor.pause()
        
        db.close()
    
    async def resume_download(self, task_id: int):
        """ダウンロード再開"""
        db = SessionLocal()
        db_task = db.query(DownloadTaskDB).filter(DownloadTaskDB.id == task_id).first()
        
        if db_task and db_task.status == DownloadStatus.PAUSED:
            db_task.status = DownloadStatus.DOWNLOADING
            db.commit()
            
            # Executor に通知
            if self.yt_dlp_executor:
                self.yt_dlp_executor.resume()
        
        db.close()
    
    async def cancel_download(self, task_id: int):
        """ダウンロードキャンセル"""
        db = SessionLocal()
        db_task = db.query(DownloadTaskDB).filter(DownloadTaskDB.id == task_id).first()
        
        if db_task:
            db_task.status = DownloadStatus.CANCELLED
            db_task.completed_at = datetime.utcnow()
            db.commit()
            
            # Executor に通知
            if self.yt_dlp_executor:
                self.yt_dlp_executor.cancel()
        
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
