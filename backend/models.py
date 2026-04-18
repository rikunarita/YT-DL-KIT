from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class DownloadStatus(str, Enum):
    """ダウンロードステータス"""
    PENDING = "pending"
    DOWNLOADING = "downloading"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class YtDlpParameter(BaseModel):
    """yt-dlpパラメータメタデータ"""
    name: str
    category: str
    description: str
    type: str  # "bool", "string", "int", "choice"
    default_value: Optional[Any] = None
    required: bool = False
    incompatible_with: List[str] = Field(default_factory=list)
    depends_on: List[str] = Field(default_factory=list)
    ui_control: Optional[str] = None
    choices: Optional[List[str]] = None


class DownloadProfile(BaseModel):
    """ダウンロードプロファイル"""
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    parameters: Dict[str, Any]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DownloadTask(BaseModel):
    """ダウンロードタスク"""
    id: Optional[int] = None
    url: str
    profile_id: Optional[int] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)
    output_path: Optional[str] = None
    status: DownloadStatus = DownloadStatus.PENDING
    progress_percent: float = 0.0
    speed: Optional[str] = None
    eta: Optional[str] = None
    current_filename: Optional[str] = None
    error_message: Optional[str] = None
    created_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DownloadHistory(BaseModel):
    """ダウンロード履歴"""
    id: Optional[int] = None
    task_id: Optional[int] = None
    url: str
    output_filename: Optional[str] = None
    file_size: Optional[int] = None
    status: DownloadStatus
    duration_seconds: Optional[int] = None
    error_message: Optional[str] = None
    completed_at: datetime
    profile_name: Optional[str] = None

    class Config:
        from_attributes = True


class ScheduledDownload(BaseModel):
    """スケジュール済みダウンロード"""
    id: Optional[int] = None
    name: str
    cron_expression: str
    urls: List[str]
    profile_id: int
    is_enabled: bool = True
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class GlobalSettings(BaseModel):
    """グローバル設定"""
    id: Optional[int] = None
    default_output_directory: str = "~/Downloads"
    max_concurrent_downloads: int = 3
    default_proxy: Optional[str] = None
    proxy_username: Optional[str] = None
    proxy_password: Optional[str] = None
    ffmpeg_path: Optional[str] = None
    yt_dlp_path: Optional[str] = None
    theme: str = "light"
    auto_update_yt_dlp: bool = True
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProgressUpdate(BaseModel):
    """プログレス更新メッセージ"""
    task_id: int
    type: str  # "progress", "error", "complete"
    data: Dict[str, Any]
