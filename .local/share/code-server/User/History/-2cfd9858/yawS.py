import asyncio
from datetime import datetime
from typing import Optional, Dict, List
from croniter import croniter
from sqlalchemy.orm import Session
from database import ScheduledDownloadDB, DownloadProfileDB, SessionLocal
from models import DownloadTask, ScheduledDownload
from services.download_manager import DownloadManager


class Scheduler:
    """croniter ベースのスケジューラー"""
    
    def __init__(self, download_manager: DownloadManager):
        self.download_manager = download_manager
        self.running = False
        self.loop_task: Optional[asyncio.Task] = None
    
    async def start(self):
        """スケジューラーを開始"""
        self.running = True
        self.loop_task = asyncio.create_task(self._run_scheduler_loop())
        print("✅ Scheduler started")
    
    async def stop(self):
        """スケジューラーを停止"""
        self.running = False
        if self.loop_task:
            self.loop_task.cancel()
        print("✅ Scheduler stopped")
    
    async def _run_scheduler_loop(self):
        """スケジューラーメインループ"""
        while self.running:
            try:
                db = SessionLocal()
                
                # 有効なスケジュール済みダウンロードを取得
                schedules = db.query(ScheduledDownloadDB).filter(
                    ScheduledDownloadDB.is_enabled == True
                ).all()
                
                for schedule in schedules:
                    await self._check_and_execute(schedule, db)
                
                db.close()
                
                # 60秒ごとに確認
                await asyncio.sleep(60)
            
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"❌ Scheduler error: {e}")
                await asyncio.sleep(60)
    
    async def _check_and_execute(self, schedule: ScheduledDownloadDB, db: Session):
        """スケジュール実行チェック"""
        try:
            cron = croniter(schedule.cron_expression)
            now = datetime.utcnow()
            
            # 最後の実行時刻から次の実行時刻を計算
            if schedule.last_run:
                last_run = schedule.last_run
            else:
                # 初回実行
                last_run = now
            
            # 次の実行時刻
            next_run = cron.get_next(datetime)
            
            # 現在時刻が次の実行時刻を超えているかチェック
            if now >= next_run and (not schedule.last_run or (now - schedule.last_run).total_seconds() > 60):
                # スケジュール実行
                await self._execute_scheduled_downloads(schedule, db)
                
                # 最後の実行時刻を更新
                schedule.last_run = now
                schedule.next_run = cron.get_next(datetime)
                db.commit()
        
        except Exception as e:
            print(f"❌ Schedule execution error: {e}")
    
    async def _execute_scheduled_downloads(self, schedule: ScheduledDownloadDB, db: Session):
        """スケジュール済みダウンロードを実行"""
        try:
            # プロファイルを取得
            profile = db.query(DownloadProfileDB).filter(
                DownloadProfileDB.id == schedule.profile_id
            ).first()
            
            if not profile:
                print(f"⚠️  Profile {schedule.profile_id} not found for schedule {schedule.name}")
                return
            
            # 各 URL に対してダウンロードを追加
            for url in schedule.urls:
                task = DownloadTask(
                    url=url,
                    profile_id=schedule.profile_id,
                    parameters=profile.parameters,
                    output_path="%(title)s.%(ext)s"
                )
                
                task_id = await self.download_manager.add_download(task)
                print(f"✅ Scheduled download added: {schedule.name} - {url} (task_id: {task_id})")
        
        except Exception as e:
            print(f"❌ Error executing scheduled downloads: {e}")
    
    async def create_schedule(self, schedule: ScheduledDownload) -> int:
        """新規スケジュール作成"""
        db = SessionLocal()
        
        # Cron式の妥当性をチェック
        try:
            croniter(schedule.cron_expression)
        except Exception as e:
            db.close()
            raise ValueError(f"Invalid cron expression: {e}")
        
        # DB に保存
        db_schedule = ScheduledDownloadDB(
            name=schedule.name,
            cron_expression=schedule.cron_expression,
            urls=schedule.urls,
            profile_id=schedule.profile_id,
            is_enabled=schedule.is_enabled,
        )
        
        db.add(db_schedule)
        db.commit()
        db.refresh(db_schedule)
        
        schedule_id = db_schedule.id
        db.close()
        
        return schedule_id
    
    async def update_schedule(self, schedule_id: int, schedule: ScheduledDownload) -> bool:
        """スケジュール更新"""
        db = SessionLocal()
        
        db_schedule = db.query(ScheduledDownloadDB).filter(
            ScheduledDownloadDB.id == schedule_id
        ).first()
        
        if not db_schedule:
            db.close()
            return False
        
        # Cron式の妥当性をチェック
        try:
            croniter(schedule.cron_expression)
        except Exception as e:
            db.close()
            raise ValueError(f"Invalid cron expression: {e}")
        
        db_schedule.name = schedule.name
        db_schedule.cron_expression = schedule.cron_expression
        db_schedule.urls = schedule.urls
        db_schedule.profile_id = schedule.profile_id
        db_schedule.is_enabled = schedule.is_enabled
        
        db.commit()
        db.close()
        
        return True
    
    async def delete_schedule(self, schedule_id: int) -> bool:
        """スケジュール削除"""
        db = SessionLocal()
        
        db_schedule = db.query(ScheduledDownloadDB).filter(
            ScheduledDownloadDB.id == schedule_id
        ).first()
        
        if not db_schedule:
            db.close()
            return False
        
        db.delete(db_schedule)
        db.commit()
        db.close()
        
        return True
    
    async def get_schedules(self) -> List[ScheduledDownload]:
        """スケジュール一覧取得"""
        db = SessionLocal()
        
        db_schedules = db.query(ScheduledDownloadDB).all()
        db.close()
        
        return [
            ScheduledDownload(
                id=s.id,
                name=s.name,
                cron_expression=s.cron_expression,
                urls=s.urls,
                profile_id=s.profile_id,
                is_enabled=s.is_enabled,
                last_run=s.last_run,
                next_run=s.next_run,
            )
            for s in db_schedules
        ]
    
    async def get_schedule(self, schedule_id: int) -> Optional[ScheduledDownload]:
        """スケジュール取得"""
        db = SessionLocal()
        
        db_schedule = db.query(ScheduledDownloadDB).filter(
            ScheduledDownloadDB.id == schedule_id
        ).first()
        
        db.close()
        
        if not db_schedule:
            return None
        
        return ScheduledDownload(
            id=db_schedule.id,
            name=db_schedule.name,
            cron_expression=db_schedule.cron_expression,
            urls=db_schedule.urls,
            profile_id=db_schedule.profile_id,
            is_enabled=db_schedule.is_enabled,
            last_run=db_schedule.last_run,
            next_run=db_schedule.next_run,
        )
