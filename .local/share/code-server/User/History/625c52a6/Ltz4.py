#!/usr/bin/env python3
"""
バックエンド統合テスト - エラーなく起動できるか確認
"""

import sys
import asyncio
from pathlib import Path

# プロジェクトパスを追加
sys.path.insert(0, str(Path(__file__).parent))

async def test_imports():
    """モジュール import テスト"""
    try:
        print("✓ Import: backend.app")
        from backend.app import app
        
        print("✓ Import: backend.models")
        from backend.models import DownloadTask, DownloadStatus
        
        print("✓ Import: backend.database")
        from backend.database import init_db, SessionLocal
        
        print("✓ Import: backend.services.download_manager")
        from backend.services.download_manager import DownloadManager
        
        print("✓ Import: backend.services.scheduler")
        from backend.services.scheduler import Scheduler
        
        print("✓ Import: backend.services.config_parser")
        from backend.services.config_parser import ConfigParser
        
        print("✓ Import: backend.api.downloads")
        from backend.api.downloads import router as downloads_router
        
        print("✓ Import: backend.api.profiles")
        from backend.api.profiles import router as profiles_router
        
        print("✓ Import: backend.api.history")
        from backend.api.history import router as history_router
        
        print("✓ Import: backend.api.settings")
        from backend.api.settings import router as settings_router
        
        print("✓ Import: backend.api.scheduler")
        from backend.api.scheduler import router as scheduler_router
        
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_database():
    """データベース初期化テスト"""
    try:
        print("\n--- Database Tests ---")
        from backend.database import init_db, engine, Base
        
        # テーブル作成
        print("✓ Creating database tables...")
        Base.metadata.create_all(bind=engine)
        
        # セッション確認
        from backend.database import SessionLocal
        db = SessionLocal()
        db.close()
        print("✓ Database session works")
        
        return True
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_config_parser():
    """ConfigParser テスト"""
    try:
        print("\n--- ConfigParser Tests ---")
        from backend.services.config_parser import ConfigParser
        
        parser = ConfigParser()
        metadata = parser.generate_metadata()
        
        print(f"✓ Generated metadata for {len(metadata)} parameters")
        
        # サンプルパラメータを表示
        sample_params = list(metadata.items())[:3]
        for param_name, param_info in sample_params:
            print(f"  - {param_name}: {param_info.get('description', 'N/A')[:50]}...")
        
        # 依存関係適用テスト
        params = {
            'extract-audio': True,
            'format': 'best'
        }
        result = parser.apply_dependencies(params)
        print(f"✓ Dependencies applied: {result}")
        
        return True
    except Exception as e:
        print(f"✗ ConfigParser test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_api_routes():
    """API ルートテスト"""
    try:
        print("\n--- API Routes Tests ---")
        from backend.app import app
        
        routes = [route.path for route in app.routes]
        print(f"✓ Registered {len(routes)} routes:")
        
        # 主要ルートを確認
        required_routes = [
            '/api/downloads',
            '/api/profiles',
            '/api/history',
            '/api/settings',
            '/api/scheduler',
            '/api/health',
        ]
        
        for route in required_routes:
            if any(route in r for r in routes):
                print(f"  ✓ {route}")
            else:
                print(f"  ✗ {route} NOT FOUND")
                return False
        
        return True
    except Exception as e:
        print(f"✗ API routes test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("=" * 60)
    print("yt-dlp GUI バックエンド統合テスト")
    print("=" * 60)
    
    results = []
    
    print("\n--- Import Tests ---")
    results.append(("Imports", await test_imports()))
    
    results.append(("Database", await test_database()))
    results.append(("ConfigParser", await test_config_parser()))
    results.append(("API Routes", await test_api_routes()))
    
    print("\n" + "=" * 60)
    print("テスト結果:")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} passed")
    
    if passed == total:
        print("\n✨ すべてのテストが成功しました！")
        return 0
    else:
        print(f"\n❌ {total - passed} 個のテストが失敗しました")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
