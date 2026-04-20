#!/usr/bin/env python3
"""
Setup script for WeaveDLX project.

This script prepares the project for development or packaging:
- Installs backend dependencies
- Installs frontend dependencies  
- Optionally builds frontend assets
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, cwd=None, description=None):
    """Run a shell command and handle errors."""
    if description:
        print(f"\n📦 {description}")
    print(f"  Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, cwd=cwd, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed with exit code {e.returncode}")
        return False
    except FileNotFoundError as e:
        print(f"❌ Command not found: {e}")
        return False


def setup_backend():
    """Setup backend dependencies."""
    backend_dir = Path(__file__).parent / "backend"
    
    print("\n" + "="*60)
    print("BACKEND SETUP")
    print("="*60)
    
    # Check if requirements.txt exists
    req_file = backend_dir / "requirements.txt"
    if not req_file.exists():
        print(f"❌ {req_file} not found")
        return False
    
    # Install dependencies
    if not run_command(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        cwd=backend_dir,
        description="Installing backend dependencies"
    ):
        return False
    
    print("✅ Backend setup complete")
    return True


def setup_frontend():
    """Setup frontend dependencies and optionally build."""
    frontend_dir = Path(__file__).parent / "frontend"
    
    print("\n" + "="*60)
    print("FRONTEND SETUP")
    print("="*60)
    
    # Check if package.json exists
    pkg_file = frontend_dir / "package.json"
    if not pkg_file.exists():
        print(f"❌ {pkg_file} not found")
        return False
    
    # Install dependencies
    if not run_command(
        ["npm", "install"],
        cwd=frontend_dir,
        description="Installing frontend dependencies"
    ):
        print("⚠️  npm install had issues, but continuing...")
    
    print("✅ Frontend setup complete")
    return True


def build_frontend():
    """Build frontend assets for production."""
    frontend_dir = Path(__file__).parent / "frontend"
    
    if not run_command(
        ["npm", "run", "build"],
        cwd=frontend_dir,
        description="Building frontend assets"
    ):
        return False
    
    print("✅ Frontend build complete")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Setup WeaveDLX for development or packaging"
    )
    parser.add_argument(
        "--build-frontend",
        action="store_true",
        help="Build frontend assets for production"
    )
    parser.add_argument(
        "--backend-only",
        action="store_true",
        help="Setup backend only"
    )
    parser.add_argument(
        "--frontend-only",
        action="store_true",
        help="Setup frontend only"
    )
    
    args = parser.parse_args()
    
    print("""
╔════════════════════════════════════════════════════════════╗
║         yt-dlp GUI - Project Setup                         ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    success = True
    
    # Determine what to setup
    setup_be = not args.frontend_only
    setup_fe = not args.backend_only
    
    if setup_be:
        if not setup_backend():
            success = False
            if not args.frontend_only:
                return 1
    
    if setup_fe:
        if not setup_frontend():
            success = False
            if not args.backend_only:
                return 1
    
    # Build frontend if requested
    if args.build_frontend:
        if not build_frontend():
            return 1
    
    print("""
╔════════════════════════════════════════════════════════════╗
║         Setup Complete! 🎉                                 ║
╚════════════════════════════════════════════════════════════╝

Next steps:

1. Start the backend:
   cd backend
   python -m uvicorn app:app --reload --port 8000

2. Start the frontend (in another terminal):
   cd frontend
   npm run dev

3. Open http://localhost:5173 in your browser

For production builds:
   python setup.py --build-frontend
    """)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
