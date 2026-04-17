import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Boolean, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import DownloadStatus

# SQLiteデータベース
DATABASE_URL = "sqlite:///./yt_dlp_gui.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class DownloadProfileDB(Base):
    """ダウンロードプロファイル DB モデル"""
    __tablename__ = "download_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    parameters = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DownloadTaskDB(Base):
    """ダウンロードタスク DB モデル"""
    __tablename__ = "download_tasks"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    profile_id = Column(Integer, nullable=True)
    parameters = Column(JSON)
    output_path = Column(String, nullable=True)
    status = Column(String, default=DownloadStatus.PENDING)
    progress_percent = Column(Float, default=0.0)
    speed = Column(String, nullable=True)
    eta = Column(String, nullable=True)
    current_filename = Column(String, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)


class DownloadHistoryDB(Base):
    """ダウンロード履歴 DB モデル"""
    __tablename__ = "download_history"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, nullable=True)
    url = Column(String)
    output_filename = Column(String, nullable=True)
    file_size = Column(Integer, nullable=True)
    status = Column(String)
    duration_seconds = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)
    completed_at = Column(DateTime, default=datetime.utcnow)
    profile_name = Column(String, nullable=True)


class ScheduledDownloadDB(Base):
    """スケジュール済みダウンロード DB モデル"""
    __tablename__ = "scheduled_downloads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    cron_expression = Column(String)
    urls = Column(JSON)
    profile_id = Column(Integer)
    is_enabled = Column(Boolean, default=True)
    last_run = Column(DateTime, nullable=True)
    next_run = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class GlobalSettingsDB(Base):
    """グローバル設定 DB モデル"""
    __tablename__ = "global_settings"

    id = Column(Integer, primary_key=True, index=True)
    default_output_directory = Column(String, default=os.path.expanduser("~/Downloads"))
    max_concurrent_downloads = Column(Integer, default=3)
    default_proxy = Column(String, nullable=True)
    proxy_username = Column(String, nullable=True)
    proxy_password = Column(String, nullable=True)
    ffmpeg_path = Column(String, nullable=True)
    yt_dlp_path = Column(String, nullable=True)
    theme = Column(String, default="light")
    auto_update_yt_dlp = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


def init_db():
    """データベーステーブル初期化"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """データベースセッション取得"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
