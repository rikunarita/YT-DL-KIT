import os
import json
from fastapi import FastAPI, WebSocket, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import asyncio
from sqlalchemy.orm import Session
from .database import init_db, get_db, GlobalSettingsDB, SessionLocal

# グローバル状態
app_state = {
    "download_manager": None,
    "scheduler": None,
    "yt_dlp_path": None,
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """アプリケーション起動・シャットダウン処理"""
    # 起動処理
    print("🚀 yt-dlp GUI サーバー起動中...")
    
    # データベース初期化
    init_db()
    print("✅ データベース初期化完了")
    
    # グローバル設定を取得
    db = SessionLocal()
    settings = db.query(GlobalSettingsDB).first()
    if not settings:
        # デフォルト設定を作成
        default_settings = GlobalSettingsDB()
        db.add(default_settings)
        db.commit()
        db.refresh(default_settings)
        print("✅ デフォルト設定を作成")
    db.close()
    
    # yt-dlp パスをチェック
    await ensure_yt_dlp()
    
    # Download Manager と Scheduler を後で初期化
    from services.download_manager import DownloadManager
    from services.scheduler import Scheduler
    
    app_state["download_manager"] = DownloadManager()
    app_state["scheduler"] = Scheduler(app_state["download_manager"])
    
    print("✅ yt-dlp GUI サーバー準備完了")
    
    yield
    
    # シャットダウン処理
    print("🛑 yt-dlp GUI サーバーシャットダウン中...")
    if app_state["scheduler"]:
        app_state["scheduler"].stop()
    print("✅ シャットダウン完了")


# FastAPI アプリケーション初期化
app = FastAPI(
    title="yt-dlp GUI Backend",
    description="yt-dlpパラメータ制御用のバックエンドAPI",
    version="1.0.0",
    lifespan=lifespan
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Vite デフォルトポート
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def ensure_yt_dlp():
    """yt-dlpバイナリがなければダウンロード"""
    import platform
    import subprocess
    
    system = platform.system()
    
    # キャッシュディレクトリ
    cache_dir = os.path.expanduser("~/.yt-dlp-gui/bin")
    os.makedirs(cache_dir, exist_ok=True)
    
    if system == "Windows":
        yt_dlp_bin = os.path.join(cache_dir, "yt-dlp.exe")
    else:
        yt_dlp_bin = os.path.join(cache_dir, "yt-dlp")
    
    # すでに存在するかチェック
    if os.path.exists(yt_dlp_bin):
        app_state["yt_dlp_path"] = yt_dlp_bin
        print(f"✅ yt-dlp バイナリ: {yt_dlp_bin}")
        return
    
    # ダウンロード
    print(f"⬇️  yt-dlp を {cache_dir} にダウンロード中...")
    try:
        if system == "Windows":
            url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
        elif system == "Darwin":
            url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp_macos"
        else:  # Linux
            url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp_linux"
        
        import urllib.request
        urllib.request.urlretrieve(url, yt_dlp_bin)
        
        # 実行権限を付与 (Unix系)
        if system != "Windows":
            os.chmod(yt_dlp_bin, 0o755)
        
        app_state["yt_dlp_path"] = yt_dlp_bin
        print(f"✅ yt-dlp ダウンロード完了: {yt_dlp_bin}")
    except Exception as e:
        print(f"❌ yt-dlp ダウンロード失敗: {e}")
        raise


# ルートエンドポイント
@app.get("/api/health")
async def health_check():
    """ヘルスチェック"""
    return {
        "status": "healthy",
        "yt_dlp_path": app_state.get("yt_dlp_path"),
    }


@app.get("/api/version")
async def get_version():
    """バージョン情報"""
    return {
        "app_version": "1.0.0",
        "backend_version": "1.0.0",
    }


# WebSocketエンドポイント
@app.websocket("/ws/downloads/{task_id}")
async def websocket_download_progress(websocket: WebSocket, task_id: int):
    """ダウンロード進捗WebSocketエンドポイント"""
    await websocket.accept()
    try:
        # Download Manager からのメッセージを受信・中継
        while True:
            # ここでキューからメッセージを取得
            await asyncio.sleep(0.1)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()


# 後で API ルーターをインクルード
from .api import downloads, profiles, history, settings, scheduler

app.include_router(downloads.router, prefix="/api/downloads", tags=["downloads"])
app.include_router(profiles.router, prefix="/api/profiles", tags=["profiles"])
app.include_router(history.router, prefix="/api/history", tags=["history"])
app.include_router(settings.router, prefix="/api/settings", tags=["settings"])
app.include_router(scheduler.router, prefix="/api/scheduler", tags=["scheduler"])


# 静的ファイル配信 (React フロントエンド)
frontend_build_path = os.path.join(os.path.dirname(__file__), "../frontend/dist")
if os.path.exists(frontend_build_path):
    app.mount("/", StaticFiles(directory=frontend_build_path, html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
