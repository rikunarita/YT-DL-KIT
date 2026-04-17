from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db, GlobalSettingsDB
from models import GlobalSettings
from services.config_parser import ConfigParser
from datetime import datetime

router = APIRouter()


@router.get("")
async def get_settings(
    db: Session = Depends(get_db)
):
    """グローバル設定取得"""
    try:
        settings = db.query(GlobalSettingsDB).first()
        
        if not settings:
            # デフォルト設定を作成
            settings = GlobalSettingsDB()
            db.add(settings)
            db.commit()
            db.refresh(settings)
        
        return {
            "success": True,
            "settings": {
                "id": settings.id,
                "default_output_directory": settings.default_output_directory,
                "max_concurrent_downloads": settings.max_concurrent_downloads,
                "default_proxy": settings.default_proxy,
                "proxy_username": settings.proxy_username,
                "ffmpeg_path": settings.ffmpeg_path,
                "yt_dlp_path": settings.yt_dlp_path,
                "theme": settings.theme,
                "auto_update_yt_dlp": settings.auto_update_yt_dlp,
                "updated_at": settings.updated_at.isoformat() if settings.updated_at else None,
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("")
async def update_settings(
    settings: GlobalSettings,
    db: Session = Depends(get_db)
):
    """グローバル設定更新"""
    try:
        db_settings = db.query(GlobalSettingsDB).first()
        
        if not db_settings:
            db_settings = GlobalSettingsDB()
        
        db_settings.default_output_directory = settings.default_output_directory
        db_settings.max_concurrent_downloads = settings.max_concurrent_downloads
        db_settings.default_proxy = settings.default_proxy
        db_settings.proxy_username = settings.proxy_username
        db_settings.proxy_password = settings.proxy_password
        db_settings.ffmpeg_path = settings.ffmpeg_path
        db_settings.yt_dlp_path = settings.yt_dlp_path
        db_settings.theme = settings.theme
        db_settings.auto_update_yt_dlp = settings.auto_update_yt_dlp
        db_settings.updated_at = datetime.utcnow()
        
        db.add(db_settings)
        db.commit()
        
        return {
            "success": True,
            "message": "Settings updated"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/yt-dlp/parameters")
async def get_yt_dlp_parameters(
    db: Session = Depends(get_db)
):
    """yt-dlpパラメータメタデータ取得"""
    try:
        from app import app_state
        
        yt_dlp_path = app_state.get("yt_dlp_path")
        if not yt_dlp_path:
            raise HTTPException(status_code=500, detail="yt-dlp not initialized")
        
        parser = ConfigParser(yt_dlp_path)
        json_str = await parser.export_as_json()
        
        # JSON文字列をパースして返す
        import json
        parameters = json.loads(json_str)
        
        return {
            "success": True,
            "parameters": parameters
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/config/export")
async def export_config(
    db: Session = Depends(get_db)
):
    """設定ファイルエクスポート"""
    try:
        import json
        
        settings = db.query(GlobalSettingsDB).first()
        
        config = {
            "default_output_directory": settings.default_output_directory if settings else None,
            "max_concurrent_downloads": settings.max_concurrent_downloads if settings else 3,
            "default_proxy": settings.default_proxy if settings else None,
            "theme": settings.theme if settings else "light",
            "auto_update_yt_dlp": settings.auto_update_yt_dlp if settings else True,
            "exported_at": datetime.utcnow().isoformat(),
        }
        
        return JSONResponse(content=config, media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/config/import")
async def import_config(
    config: dict,
    db: Session = Depends(get_db)
):
    """設定ファイルインポート"""
    try:
        settings = db.query(GlobalSettingsDB).first()
        
        if not settings:
            settings = GlobalSettingsDB()
        
        # 指定されたキーのみ更新
        if "default_output_directory" in config:
            settings.default_output_directory = config["default_output_directory"]
        if "max_concurrent_downloads" in config:
            settings.max_concurrent_downloads = config["max_concurrent_downloads"]
        if "default_proxy" in config:
            settings.default_proxy = config["default_proxy"]
        if "theme" in config:
            settings.theme = config["theme"]
        if "auto_update_yt_dlp" in config:
            settings.auto_update_yt_dlp = config["auto_update_yt_dlp"]
        
        settings.updated_at = datetime.utcnow()
        
        db.add(settings)
        db.commit()
        
        return {
            "success": True,
            "message": "Configuration imported successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
