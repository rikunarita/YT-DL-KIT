"""
バックエンド API 統合テスト

実行: pytest tests/test_backend_api.py -v
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# テスト用インポート
from backend.app import app
from backend.database import Base, get_db
from backend.models import DownloadTask, DownloadProfile

# テスト用データベース
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client

class TestHealthCheck:
    """ヘルスチェック テスト"""
    
    def test_health_endpoint(self, client):
        """GET /api/health"""
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

class TestDownloads:
    """ダウンロード API テスト"""
    
    def test_get_queue(self, client):
        """GET /api/downloads/queue"""
        response = client.get("/api/downloads/queue")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert isinstance(data.get("tasks"), list)
    
    def test_start_download(self, client):
        """POST /api/downloads/start"""
        payload = {
            "url": "https://example.com/video.mp4",
            "parameters": {
                "format": "best"
            },
            "output_path": "/tmp/%(title)s.%(ext)s"
        }
        response = client.post("/api/downloads/start", json=payload)
        assert response.status_code in [200, 201, 400, 422]

class TestProfiles:
    """プロファイル API テスト"""
    
    def test_get_profiles(self, client):
        """GET /api/profiles"""
        response = client.get("/api/profiles")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert isinstance(data.get("profiles"), list)
    
    def test_create_profile(self, client):
        """POST /api/profiles"""
        payload = {
            "name": "Test Profile",
            "description": "API test profile",
            "parameters": {
                "format": "best",
                "extract_audio": False
            }
        }
        response = client.post("/api/profiles", json=payload)
        assert response.status_code in [200, 201]
        data = response.json()
        assert data["success"] is True

class TestHistory:
    """履歴 API テスト"""
    
    def test_get_history(self, client):
        """GET /api/history"""
        response = client.get("/api/history?limit=50&offset=0")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert isinstance(data.get("records"), list)
    
    def test_get_stats(self, client):
        """GET /api/history/stats"""
        response = client.get("/api/history/stats")
        assert response.status_code == 200
        stats = response.json()
        assert "total_downloads" in stats

class TestSettings:
    """設定 API テスト"""
    
    def test_get_settings(self, client):
        """GET /api/settings"""
        response = client.get("/api/settings")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "default_output_directory" in data.get("settings", {})
    
    def test_get_yt_dlp_parameters(self, client):
        """GET /api/settings/yt-dlp/parameters"""
        response = client.get("/api/settings/yt-dlp/parameters")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert isinstance(data.get("parameters"), (list, dict))

class TestScheduler:
    """スケジューラ API テスト"""
    
    def test_get_tasks(self, client):
        """GET /api/scheduler/tasks"""
        response = client.get("/api/scheduler/tasks")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert isinstance(data.get("tasks"), list)
    
    def test_create_task_invalid_cron(self, client):
        """POST /api/scheduler/tasks - 無効な Cron 式"""
        payload = {
            "name": "Invalid Schedule",
            "cron_expression": "invalid cron",
            "urls": ["https://example.com"],
            "profile_id": 1,
            "is_enabled": True
        }
        response = client.post("/api/scheduler/tasks", json=payload)
        # 無効な Cron 式は 400 エラー
        assert response.status_code == 400

class TestErrorHandling:
    """エラーハンドリング テスト"""
    
    def test_404_error(self, client):
        """404 エラー"""
        response = client.get("/api/nonexistent")
        assert response.status_code == 404
    
    def test_method_not_allowed(self, client):
        """405 エラー"""
        response = client.delete("/api/profiles")
        assert response.status_code == 405

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
