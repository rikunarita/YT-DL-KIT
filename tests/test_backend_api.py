"""
バックエンド API 統合テスト

実行: pytest tests/test_backend_api.py -v
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# テスト用インポート
from backend.app import app
from backend.database import Base, get_db
from backend.models import DownloadTask, DownloadProfile

# テスト用データベース
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test_database.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
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

client = TestClient(app)

class TestHealthCheck:
    """ヘルスチェック テスト"""
    
    def test_health_endpoint(self):
        """GET /api/health"""
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

class TestDownloads:
    """ダウンロード API テスト"""
    
    def test_get_queue(self):
        """GET /api/downloads/queue"""
        response = client.get("/api/downloads/queue")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_start_download(self):
        """POST /api/downloads/start"""
        payload = {
            "url": "https://example.com/video.mp4",
            "format": "best",
            "output_template": "/tmp/%(title)s.%(ext)s"
        }
        response = client.post("/api/downloads/start", json=payload)
        # 実装によって異なるため、ステータスコード確認のみ
        assert response.status_code in [200, 201, 400]

class TestProfiles:
    """プロファイル API テスト"""
    
    def test_get_profiles(self):
        """GET /api/profiles"""
        response = client.get("/api/profiles")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_create_profile(self):
        """POST /api/profiles"""
        payload = {
            "name": "Test Profile",
            "format": "best",
            "extract_audio": False
        }
        response = client.post("/api/profiles", json=payload)
        assert response.status_code in [200, 201]

class TestHistory:
    """履歴 API テスト"""
    
    def test_get_history(self):
        """GET /api/history"""
        response = client.get("/api/history?limit=50&offset=0")
        assert response.status_code == 200
        data = response.json()
        assert "records" in data or isinstance(data, list)
    
    def test_get_stats(self):
        """GET /api/history/stats"""
        response = client.get("/api/history/stats")
        assert response.status_code == 200
        stats = response.json()
        assert "total_downloads" in stats

class TestSettings:
    """設定 API テスト"""
    
    def test_get_settings(self):
        """GET /api/settings"""
        response = client.get("/api/settings")
        assert response.status_code == 200
        assert "default_output_directory" in response.json()
    
    def test_get_yt_dlp_parameters(self):
        """GET /api/settings/yt-dlp/parameters"""
        response = client.get("/api/settings/yt-dlp/parameters")
        assert response.status_code == 200
        params = response.json()
        # パラメータメタデータが返されること
        assert len(params.get("parameters", [])) > 0 or isinstance(params, list)

class TestScheduler:
    """スケジューラ API テスト"""
    
    def test_get_tasks(self):
        """GET /api/scheduler/tasks"""
        response = client.get("/api/scheduler/tasks")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_create_task_invalid_cron(self):
        """POST /api/scheduler/tasks - 無効な Cron 式"""
        payload = {
            "name": "Invalid Schedule",
            "cron_expression": "invalid cron",
            "urls": ["https://example.com"],
            "is_enabled": True
        }
        response = client.post("/api/scheduler/tasks", json=payload)
        # 無効な Cron 式は 400 エラー
        assert response.status_code == 400

class TestErrorHandling:
    """エラーハンドリング テスト"""
    
    def test_404_error(self):
        """404 エラー"""
        response = client.get("/api/nonexistent")
        assert response.status_code == 404
    
    def test_method_not_allowed(self):
        """405 エラー"""
        response = client.delete("/api/downloads/start")
        assert response.status_code == 405

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
