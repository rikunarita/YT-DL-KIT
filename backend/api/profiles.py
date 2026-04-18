from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db, DownloadProfileDB
from ..models import DownloadProfile

router = APIRouter()


@router.get("")
async def get_profiles(
    db: Session = Depends(get_db)
):
    """プロファイル一覧取得"""
    try:
        profiles = db.query(DownloadProfileDB).all()
        return {
            "success": True,
            "profiles": [
                {
                    "id": p.id,
                    "name": p.name,
                    "description": p.description,
                    "parameters": p.parameters,
                    "created_at": p.created_at,
                    "updated_at": p.updated_at,
                }
                for p in profiles
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("")
async def create_profile(
    profile: DownloadProfile,
    db: Session = Depends(get_db)
):
    """新規プロファイル作成"""
    try:
        # 同名プロファイルが存在するかチェック
        existing = db.query(DownloadProfileDB).filter(
            DownloadProfileDB.name == profile.name
        ).first()
        
        if existing:
            raise HTTPException(status_code=400, detail=f"Profile '{profile.name}' already exists")
        
        # 新規作成
        db_profile = DownloadProfileDB(
            name=profile.name,
            description=profile.description,
            parameters=profile.parameters,
        )
        
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        
        return {
            "success": True,
            "profile_id": db_profile.id,
            "message": f"Profile '{profile.name}' created"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{profile_id}")
async def update_profile(
    profile_id: int,
    profile: DownloadProfile,
    db: Session = Depends(get_db)
):
    """プロファイル更新"""
    try:
        db_profile = db.query(DownloadProfileDB).filter(
            DownloadProfileDB.id == profile_id
        ).first()
        
        if not db_profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        # 別のプロファイルが同じ名前を使っていないかチェック
        existing = db.query(DownloadProfileDB).filter(
            DownloadProfileDB.name == profile.name,
            DownloadProfileDB.id != profile_id
        ).first()
        
        if existing:
            raise HTTPException(status_code=400, detail=f"Profile name '{profile.name}' is already used")
        
        # 更新
        db_profile.name = profile.name
        db_profile.description = profile.description
        db_profile.parameters = profile.parameters
        
        db.commit()
        db.refresh(db_profile)
        
        return {
            "success": True,
            "message": f"Profile updated"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{profile_id}")
async def delete_profile(
    profile_id: int,
    db: Session = Depends(get_db)
):
    """プロファイル削除"""
    try:
        db_profile = db.query(DownloadProfileDB).filter(
            DownloadProfileDB.id == profile_id
        ).first()
        
        if not db_profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        db.delete(db_profile)
        db.commit()
        
        return {
            "success": True,
            "message": f"Profile deleted"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{profile_id}/duplicate")
async def duplicate_profile(
    profile_id: int,
    new_name: str,
    db: Session = Depends(get_db)
):
    """プロファイル複製"""
    try:
        source_profile = db.query(DownloadProfileDB).filter(
            DownloadProfileDB.id == profile_id
        ).first()
        
        if not source_profile:
            raise HTTPException(status_code=404, detail="Source profile not found")
        
        # 同名チェック
        existing = db.query(DownloadProfileDB).filter(
            DownloadProfileDB.name == new_name
        ).first()
        
        if existing:
            raise HTTPException(status_code=400, detail=f"Profile '{new_name}' already exists")
        
        # コピー作成
        new_profile = DownloadProfileDB(
            name=new_name,
            description=f"Copy of {source_profile.name}",
            parameters=source_profile.parameters,
        )
        
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)
        
        return {
            "success": True,
            "profile_id": new_profile.id,
            "message": f"Profile duplicated as '{new_name}'"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
