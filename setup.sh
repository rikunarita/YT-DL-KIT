#!/bin/bash
# WeaveDLX セットアップスクリプト

set -e

echo "🚀 WeaveDLX セットアップ開始..."

# バックエンドセットアップ
echo "📦 バックエンド依存パッケージをインストール中..."
cd backend
pip install -q -r requirements.txt
cd ..
echo "✅ バックエンド準備完了"

# フロントエンドセットアップ（npm が使用可能な場合）
if command -v npm &> /dev/null; then
    echo "📦 フロントエンド依存パッケージをインストール中..."
    cd frontend
    npm install --quiet
    cd ..
    echo "✅ フロントエンド準備完了"
else
    echo "⚠️  npm が見つかりません。フロントエンドのセットアップをスキップしています。"
    echo "   Node.js をインストール後に、以下を実行してください:"
    echo "   cd frontend && npm install"
fi

echo ""
echo "✨ セットアップ完了！"
echo ""
echo "起動方法:"
echo "1. バックエンド（親ディレクトリから実行）:"
echo "   cd /home/user/WeaveDLX && python -m uvicorn backend.app:app --reload --port 8000"
echo ""
echo "2. フロントエンド:"
echo "   cd frontend && npm run dev"
echo ""
echo "ブラウザで http://localhost:5173 を開いてください"
