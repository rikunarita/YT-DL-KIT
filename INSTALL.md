# WeaveDLX - インストール・セットアップガイド

## 前提条件

- **Python**: 3.11 以上
- **Node.js**: 18.x 以上（フロントエンド開発用）
- **Git**: バージョン管理用

## クイックスタート

### 1. リポジトリをクローン

```bash
git clone https://github.com/your-username/WeaveDLX.git
cd WeaveDLX
```

### 2. 自動セットアップ（推奨）

```bash
# スクリプトは自動で Python + Node.js の依存パッケージをインストール
./setup.sh
```

### 3. 手動セットアップ

**バックエンド:**
```bash
cd backend
pip install -r requirements.txt
```

**フロントエンド:**
```bash
cd frontend
npm install
```

## 開発環境での実行

### ターミナル 1: バックエンド起動

```bash
# ⚠️  重要: 親ディレクトリ /home/user/WeaveDLX から実行してください
cd /home/user/WeaveDLX
python -m uvicorn backend.app:app --reload --port 8000
```

出力例:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
✅ WeaveDLX サーバー準備完了
```

**注意:** `cd backend && python -m uvicorn app:app --reload` という実行方法は使用できません。
INFO:     Application startup complete
```

### ターミナル 2: フロントエンド起動

```bash
cd frontend
npm run dev
```

出力例:
```
  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

### ターミナル 3: API ドキュメント確認（オプション）

```bash
# Swagger UI で API 仕様確認
open http://localhost:8000/docs

# または ReDoc
open http://localhost:8000/redoc
```

## ブラウザで開く

```
http://localhost:5173
```

## 設定ファイル

### バックエンド設定

- **Database**: `./weavedlx.db` (SQLite)
- **yt-dlp バイナリ**: `~/.weavedlx/bin/yt-dlp`（自動ダウンロード）
- **API**: http://localhost:8000
- **WebSocket**: ws://localhost:8000/ws/downloads/{task_id}

### フロントエンド設定

- **Vite Dev Server**: http://localhost:5173
- **API Proxy**: `/api` → `http://localhost:8000/api`
- **Build Output**: `dist/`

## テスト実行

### バックエンド統合テスト

```bash
python test_backend.py
```

期待結果: `4/4 passed`

## よくある問題

### 1. yt-dlp バイナリが見つからない

```
Error: yt-dlp binary not found at ~/.weavedlx/bin/yt-dlp
```

**解決方法**:
```bash
mkdir -p ~/.weavedlx/bin
# 手動ダウンロード
# macOS/Linux:
curl -L https://github.com/yt-dlp/yt-dlp/releases/download/latest/yt-dlp -o ~/.weavedlx/bin/yt-dlp
chmod +x ~/.weavedlx/bin/yt-dlp

# Windows: releases ページからダウンロード
```

### 2. ポート 8000 が既に使用中

```
Address already in use: ('127.0.0.1', 8000)
```

**解決方法**:
```bash
# 異なるポートで起動
python -m uvicorn app:app --reload --port 8001

# フロントエンド設定を更新
# frontend/vite.config.ts の proxy を 8001 に変更
```

### 3. npm install エラー

```
npm ERR! code ERESOLVE
npm ERR! ERESOLVE unable to resolve dependency tree
```

**解決方法**:
```bash
npm install --legacy-peer-deps
```

### 4. CORS エラー

```
Access to XMLHttpRequest has been blocked by CORS policy
```

**確認**:
- バックエンド CORS 設定: `backend/app.py` の `allow_origins`
- 開発環境: `http://localhost:5173` が許可リストに含まれているか確認

## パッケージング（スタンドアロン実行ファイル作成）

### Prerequisites

- **PyInstaller**: `pip install pyinstaller`
- **Webpack**: フロントエンド build に必要

### ビルド手順

```bash
# 全スタック build
cd packaging
python build_standalone.py

# 出力ファイル
# - Linux: dist/weavedlx-linux-x86_64
# - macOS: dist/weavedlx-macos-universal
# - Windows: dist/weavedlx-windows-x86_64.exe
```

## リソース

- **yt-dlp ドキュメント**: https://github.com/yt-dlp/yt-dlp
- **FastAPI ドキュメント**: https://fastapi.tiangolo.com/
- **React ドキュメント**: https://react.dev/
- **Redux Toolkit ドキュメント**: https://redux-toolkit.js.org/

## 開発者向け情報

### ディレクトリ構成

```
WeaveDLX/
├── backend/                # FastAPI アプリケーション
│   ├── app.py             # メインエントリーポイント
│   ├── models.py          # Pydantic データモデル
│   ├── database.py        # SQLAlchemy ORM
│   ├── services/          # ビジネスロジック
│   └── api/               # REST エンドポイント
├── frontend/              # React + TypeScript
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/    # UI コンポーネント
│   │   ├── store/         # Redux Toolkit
│   │   └── services/      # API クライアント
│   └── package.json
├── packaging/             # スタンドアロン build
├── test_backend.py        # バックエンド統合テスト
├── setup.sh               # セットアップスクリプト
└── README.md              # プロジェクト概要
```

### データベースマイグレーション

```bash
# 手動で初期化（必要な場合）
python -c "from backend.database import init_db; init_db()"
```

### API エンドポイント一覧

| Method | Endpoint | 説明 |
|--------|----------|------|
| POST | `/api/downloads/start` | ダウンロード開始 |
| GET | `/api/downloads/queue` | キュー一覧 |
| GET | `/api/history` | ダウンロード履歴 |
| GET | `/api/profiles` | プロファイル一覧 |
| POST | `/api/profiles` | プロファイル作成 |
| GET | `/api/settings` | グローバル設定取得 |
| POST | `/api/scheduler/tasks` | スケジュール作成 |

## バージョン情報

- **yt-dlp GUI Version**: 1.0.0
- **Python**: 3.11+
- **Node.js**: 18.x+
- **React**: 18.2+

## サポート

問題が発生した場合は、GitHub Issues で報告してください。

---

**最終更新**: 2026-04-17
