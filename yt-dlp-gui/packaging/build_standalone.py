#!/usr/bin/env python3
"""
スタンドアロン実行ファイル生成スクリプト

使用方法:
    python build_standalone.py [--platform all|windows|macos|linux]

出力:
    - dist/yt-dlp-gui-windows-x86_64.exe
    - dist/yt-dlp-gui-macos-universal
    - dist/yt-dlp-gui-linux-x86_64
"""

import os
import sys
import platform
import subprocess
import argparse
import shutil
from pathlib import Path

class BuildConfig:
    """ビルド設定"""
    
    PROJECT_ROOT = Path(__file__).parent
    FRONTEND_DIR = PROJECT_ROOT / "frontend"
    BACKEND_DIR = PROJECT_ROOT / "backend"
    PACKAGING_DIR = PROJECT_ROOT / "packaging"
    DIST_DIR = PROJECT_ROOT / "dist"
    BUILD_DIR = PACKAGING_DIR / "build"
    
    PLATFORMS = {
        'windows': {
            'name': 'Windows',
            'output': 'yt-dlp-gui-windows-x86_64.exe',
            'pyinstaller_args': ['--windowed', '--onefile'],
        },
        'macos': {
            'name': 'macOS',
            'output': 'yt-dlp-gui-macos-universal',
            'pyinstaller_args': ['--windowed', '--onefile', '--target-arch', 'universal2'],
        },
        'linux': {
            'name': 'Linux',
            'output': 'yt-dlp-gui-linux-x86_64',
            'pyinstaller_args': ['--onefile'],
        },
    }

def check_prerequisites():
    """前提条件チェック"""
    print("📋 前提条件をチェック中...")
    
    # npm チェック
    try:
        subprocess.run(['npm', '--version'], capture_output=True, check=True)
        print("  ✓ npm")
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("  ✗ npm が見つかりません。Node.js をインストールしてください。")
        return False
    
    # PyInstaller チェック
    try:
        subprocess.run(['pyinstaller', '--version'], capture_output=True, check=True)
        print("  ✓ PyInstaller")
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("  ✗ PyInstaller が見つかりません。")
        print("     pip install pyinstaller")
        return False
    
    # Python チェック
    if sys.version_info < (3, 11):
        print("  ✗ Python 3.11+ が必要です")
        return False
    print("  ✓ Python 3.11+")
    
    return True

def build_frontend():
    """フロントエンド ビルド"""
    print("\n🔨 フロントエンドをビルド中...")
    
    try:
        # 依存パッケージ確認
        package_lock = BuildConfig.FRONTEND_DIR / "package-lock.json"
        node_modules = BuildConfig.FRONTEND_DIR / "node_modules"
        
        if not node_modules.exists():
            print("  > npm install")
            subprocess.run(
                ['npm', 'install'],
                cwd=BuildConfig.FRONTEND_DIR,
                check=True
            )
        
        # ビルド
        print("  > npm run build")
        subprocess.run(
            ['npm', 'run', 'build'],
            cwd=BuildConfig.FRONTEND_DIR,
            check=True
        )
        
        print("  ✓ フロントエンド ビルド完了")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ✗ フロントエンド ビルド失敗: {e}")
        return False

def build_backend(platform_name):
    """バックエンド ビルド"""
    print(f"\n🔨 バックエンド ({platform_name}) をビルド中...")
    
    try:
        # ビルドディレクトリ準備
        BuildConfig.BUILD_DIR.mkdir(parents=True, exist_ok=True)
        
        # PyInstaller コマンド構築
        spec_file = BuildConfig.PACKAGING_DIR / "yt_dlp_gui.spec"
        output_name = f"yt-dlp-gui-backend-{platform_name}"
        
        pyinstaller_cmd = [
            'pyinstaller',
            '--distpath', str(BuildConfig.DIST_DIR),
            '--buildpath', str(BuildConfig.BUILD_DIR),
            '--name', output_name,
            '--onefile',
        ]
        
        # プラットフォーム固有の引数追加
        if platform_name == 'windows':
            pyinstaller_cmd.extend(['--windowed', '--icon=packaging/icon.ico'])
        elif platform_name == 'macos':
            pyinstaller_cmd.extend(['--osx-bundle-identifier', 'com.yt-dlp-gui'])
        
        pyinstaller_cmd.append(str(BuildConfig.BACKEND_DIR / "app.py"))
        
        print(f"  > {' '.join(pyinstaller_cmd[:5])}...")
        subprocess.run(pyinstaller_cmd, check=True)
        
        print("  ✓ バックエンド ビルド完了")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ✗ バックエンド ビルド失敗: {e}")
        return False

def create_bundle(platform_name):
    """バンドル作成"""
    print(f"\n📦 {platform_name} バンドルを作成中...")
    
    try:
        output_dir = BuildConfig.DIST_DIR / f"yt-dlp-gui-{platform_name}"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # フロントエンド dist をコピー
        frontend_dist = BuildConfig.FRONTEND_DIR / "dist"
        if frontend_dist.exists():
            shutil.copytree(
                frontend_dist,
                output_dir / "frontend",
                dirs_exist_ok=True
            )
        
        # バックエンド実行ファイルをコピー
        backend_exe = BuildConfig.DIST_DIR / f"yt-dlp-gui-backend-{platform_name}"
        if backend_exe.exists():
            shutil.copy(backend_exe, output_dir / "backend")
        
        # README, LICENSE をコピー
        for file in ['README.md', 'LICENSE']:
            if (BuildConfig.PROJECT_ROOT / file).exists():
                shutil.copy(
                    BuildConfig.PROJECT_ROOT / file,
                    output_dir / file
                )
        
        # ランチャースクリプト作成
        if platform_name == 'windows':
            create_launcher_bat(output_dir)
        else:
            create_launcher_sh(output_dir)
        
        print(f"  ✓ バンドル作成完了: {output_dir}")
        return True
    except Exception as e:
        print(f"  ✗ バンドル作成失敗: {e}")
        return False

def create_launcher_bat(bundle_dir):
    """Windows ランチャースクリプト"""
    launcher = bundle_dir / "yt-dlp-gui.bat"
    launcher.write_text("""@echo off
REM yt-dlp GUI Launcher (Windows)
set SCRIPT_DIR=%~dp0
start "" "%SCRIPT_DIR%backend.exe"
timeout /t 3 /nobreak
start http://localhost:5173
""")

def create_launcher_sh(bundle_dir):
    """Unix ランチャースクリプト"""
    launcher = bundle_dir / "yt-dlp-gui.sh"
    launcher.write_text("""#!/bin/bash
# yt-dlp GUI Launcher (macOS/Linux)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
"$SCRIPT_DIR/backend" &
sleep 3
open http://localhost:5173
""")
    os.chmod(launcher, 0o755)

def build(platforms=None):
    """ビルド実行"""
    if platforms is None:
        platforms = [platform.system().lower().replace('darwin', 'macos')]
    
    if not check_prerequisites():
        return False
    
    # フロントエンド ビルド（全プラットフォーム共通）
    if not build_frontend():
        return False
    
    # プラットフォーム別ビルド
    for platform_name in platforms:
        if platform_name not in BuildConfig.PLATFORMS:
            print(f"⚠️  Unknown platform: {platform_name}")
            continue
        
        if not build_backend(platform_name):
            print(f"⚠️  バックエンド ビルド失敗: {platform_name}")
            continue
        
        if not create_bundle(platform_name):
            print(f"⚠️  バンドル作成失敗: {platform_name}")
    
    print("\n✨ ビルド完了！")
    print(f"📂 出力ディレクトリ: {BuildConfig.DIST_DIR}")
    return True

def main():
    parser = argparse.ArgumentParser(
        description='yt-dlp GUI スタンドアロンビルドスクリプト'
    )
    parser.add_argument(
        '--platform',
        choices=['all', 'windows', 'macos', 'linux'],
        default='all',
        help='ビルド対象プラットフォーム'
    )
    parser.add_argument(
        '--frontend-only',
        action='store_true',
        help='フロントエンドのみビルド'
    )
    parser.add_argument(
        '--backend-only',
        action='store_true',
        help='バックエンドのみビルド'
    )
    
    args = parser.parse_args()
    
    if args.platform == 'all':
        platforms = ['windows', 'macos', 'linux']
    else:
        platforms = [args.platform]
    
    if args.frontend_only:
        return build_frontend()
    elif args.backend_only:
        return all(build_backend(p) for p in platforms)
    else:
        return build(platforms)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
