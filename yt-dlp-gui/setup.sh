#!/bin/bash
# yt-dlp GUI セットアップスクリプト

set -e

echo "🚀 yt-dlp GUI セットアップ開始..."

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
echo "1. バックエンド: cd backend && python -m uvicorn app:app --reload"
echo "2. フロントエンド: cd frontend && npm run dev"
echo ""
echo "ブラウザで http://localhost:5173 を開いてください"
