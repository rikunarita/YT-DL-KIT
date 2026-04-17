from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from database import get_db
from models import ScheduledDownload

router = APIRouter()


@router.get("/tasks")
async def get_schedules(
    db: Session = Depends(get_db)
):
    """スケジュール一覧取得"""
    try:
        from app import app_state
        
        if not app_state["scheduler"]:
            raise HTTPException(status_code=500, detail="Scheduler not initialized")
        
        schedules = await app_state["scheduler"].get_schedules()
        
        return {
            "success": True,
            "tasks": [s.dict() for s in schedules]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tasks")
async def create_schedule(
    schedule: ScheduledDownload,
    db: Session = Depends(get_db)
):
    """新規スケジュール作成"""
    try:
        from app import app_state
        
        if not app_state["scheduler"]:
            raise HTTPException(status_code=500, detail="Scheduler not initialized")
        
        schedule_id = await app_state["scheduler"].create_schedule(schedule)
        
        return {
            "success": True,
            "schedule_id": schedule_id,
            "message": f"Schedule '{schedule.name}' created"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/tasks/{schedule_id}")
async def update_schedule(
    schedule_id: int,
    schedule: ScheduledDownload,
    db: Session = Depends(get_db)
):
    """スケジュール更新"""
    try:
        from app import app_state
        
        if not app_state["scheduler"]:
            raise HTTPException(status_code=500, detail="Scheduler not initialized")
        
        success = await app_state["scheduler"].update_schedule(schedule_id, schedule)
        
        if not success:
            raise HTTPException(status_code=404, detail="Schedule not found")
        
        return {
            "success": True,
            "message": f"Schedule updated"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/tasks/{schedule_id}")
async def delete_schedule(
    schedule_id: int,
    db: Session = Depends(get_db)
):
    """スケジュール削除"""
    try:
        from app import app_state
        
        if not app_state["scheduler"]:
            raise HTTPException(status_code=500, detail="Scheduler not initialized")
        
        success = await app_state["scheduler"].delete_schedule(schedule_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Schedule not found")
        
        return {
            "success": True,
            "message": f"Schedule deleted"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
