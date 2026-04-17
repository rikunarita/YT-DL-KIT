from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import get_db, DownloadHistoryDB

router = APIRouter()


@router.get("")
async def get_history(
    limit: int = Query(50, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    status: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """ダウンロード履歴取得"""
    try:
        query = db.query(DownloadHistoryDB)
        
        # ステータスフィルタ
        if status:
            query = query.filter(DownloadHistoryDB.status == status)
        
        # 日付範囲フィルタ
        if date_from:
            date_from_dt = datetime.fromisoformat(date_from)
            query = query.filter(DownloadHistoryDB.completed_at >= date_from_dt)
        
        if date_to:
            date_to_dt = datetime.fromisoformat(date_to) + timedelta(days=1)
            query = query.filter(DownloadHistoryDB.completed_at < date_to_dt)
        
        # ソート (新しい順)
        query = query.order_by(DownloadHistoryDB.completed_at.desc())
        
        # ページネーション
        total = query.count()
        records = query.offset(offset).limit(limit).all()
        
        return {
            "success": True,
            "total": total,
            "offset": offset,
            "limit": limit,
            "records": [
                {
                    "id": r.id,
                    "task_id": r.task_id,
                    "url": r.url,
                    "output_filename": r.output_filename,
                    "file_size": r.file_size,
                    "status": r.status,
                    "duration_seconds": r.duration_seconds,
                    "error_message": r.error_message,
                    "completed_at": r.completed_at.isoformat(),
                    "profile_name": r.profile_name,
                }
                for r in records
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_stats(
    db: Session = Depends(get_db)
):
    """統計情報取得"""
    try:
        total = db.query(DownloadHistoryDB).count()
        successful = db.query(DownloadHistoryDB).filter(
            DownloadHistoryDB.status == "completed"
        ).count()
        failed = db.query(DownloadHistoryDB).filter(
            DownloadHistoryDB.status == "failed"
        ).count()
        
        # 総容量計算
        total_size = 0
        for record in db.query(DownloadHistoryDB).all():
            if record.file_size:
                total_size += record.file_size
        
        return {
            "success": True,
            "total_downloads": total,
            "successful": successful,
            "failed": failed,
            "total_size_bytes": total_size,
            "total_size_gb": round(total_size / (1024**3), 2),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{history_id}")
async def delete_history(
    history_id: int,
    db: Session = Depends(get_db)
):
    """履歴削除"""
    try:
        record = db.query(DownloadHistoryDB).filter(
            DownloadHistoryDB.id == history_id
        ).first()
        
        if not record:
            raise HTTPException(status_code=404, detail="History record not found")
        
        db.delete(record)
        db.commit()
        
        return {
            "success": True,
            "message": "History record deleted"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/export")
async def export_history(
    db: Session = Depends(get_db)
):
    """履歴をCSVエクスポート"""
    try:
        import csv
        import io
        
        records = db.query(DownloadHistoryDB).order_by(
            DownloadHistoryDB.completed_at.desc()
        ).all()
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # ヘッダー
        writer.writerow([
            "ID", "URL", "Output Filename", "File Size (MB)", 
            "Status", "Duration (s)", "Error Message", "Completed At", "Profile Name"
        ])
        
        # データ
        for r in records:
            writer.writerow([
                r.id,
                r.url,
                r.output_filename or "",
                round(r.file_size / (1024*1024), 2) if r.file_size else 0,
                r.status,
                r.duration_seconds or "",
                r.error_message or "",
                r.completed_at.isoformat(),
                r.profile_name or "",
            ])
        
        return {
            "success": True,
            "csv_data": output.getvalue(),
            "message": f"{len(records)} records exported"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
