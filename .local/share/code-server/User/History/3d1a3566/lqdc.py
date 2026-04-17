from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
from database import get_db, DownloadTaskDB
from models import DownloadTask, DownloadStatus

router = APIRouter()


@router.post("/start")
async def start_download(
    task: DownloadTask,
    db: Session = Depends(get_db)
):
    """ダウンロード開始"""
    from app import app_state
    
    if not app_state["download_manager"]:
        raise HTTPException(status_code=500, detail="Download manager not initialized")
    
    try:
        task_id = await app_state["download_manager"].add_download(task)
        return {
            "success": True,
            "task_id": task_id,
            "message": f"Download started: {task.url}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/queue")
async def get_queue(
    db: Session = Depends(get_db)
):
    """ダウンロードキュー取得"""
    from app import app_state
    
    try:
        queue = await app_state["download_manager"].get_queue()
        return {
            "success": True,
            "tasks": [t.dict() for t in queue]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{task_id}/status")
async def get_status(
    task_id: int,
    db: Session = Depends(get_db)
):
    """タスク詳細取得"""
    from app import app_state
    
    try:
        task = await app_state["download_manager"].get_task_status(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return {
            "success": True,
            "task": task.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{task_id}/pause")
async def pause_download(
    task_id: int,
    db: Session = Depends(get_db)
):
    """ダウンロード一時停止"""
    from app import app_state
    
    try:
        await app_state["download_manager"].pause_download(task_id)
        return {
            "success": True,
            "message": f"Task {task_id} paused"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{task_id}/resume")
async def resume_download(
    task_id: int,
    db: Session = Depends(get_db)
):
    """ダウンロード再開"""
    from app import app_state
    
    try:
        await app_state["download_manager"].resume_download(task_id)
        return {
            "success": True,
            "message": f"Task {task_id} resumed"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{task_id}")
async def cancel_download(
    task_id: int,
    db: Session = Depends(get_db)
):
    """ダウンロードキャンセル"""
    from app import app_state
    
    try:
        await app_state["download_manager"].cancel_download(task_id)
        return {
            "success": True,
            "message": f"Task {task_id} cancelled"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
