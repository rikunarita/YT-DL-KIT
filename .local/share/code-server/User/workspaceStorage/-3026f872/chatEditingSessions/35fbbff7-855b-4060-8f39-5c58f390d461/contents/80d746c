# yt-dlp GUI - Modern Download Manager

モダンな web UI で yt-dlp の全機能を制御できるデスクトップアプリケーション。

## 機能

- ✅ yt-dlp の 150+ パラメータをフルサポート
- ✅ 複数並列ダウンロード管理（スケジューラ対応）
- ✅ ダウンロード履歴・統計情報
- ✅ プロファイル管理
- ✅ Cron ベーススケジューリング
- ✅ リアルタイムプログレス表示

## 技術スタック

**Backend**:
- Python 3.11+ with FastAPI
- SQLAlchemy ORM + SQLite
- croniter スケジューラ
- 動的 yt-dlp バイナリダウンロード

**Frontend**:
- React 18 + TypeScript
- Redux Toolkit（状態管理）
- Tailwind CSS + Shadcn/UI
- Vite（ビルドツール）

## セットアップ

### バックエンド

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app:app --reload --port 8000
```

### フロントエンド

```bash
cd frontend
npm install
npm run dev
```

ブラウザで http://localhost:5173 を開く

## ビルド（スタンドアロン実行可能ファイル）

```bash
# 全セットアップ
python setup.py build

# 単体実行ファイル生成
cd packaging
python build_standalone.py
```

## API ドキュメント

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## ファイル構成

```
yt-dlp-gui/
├── backend/
│   ├── app.py                 # FastAPI メインアプリケーション
│   ├── models.py              # Pydantic データモデル
│   ├── database.py            # SQLAlchemy ORM定義
│   ├── services/              # ビジネスロジック層
│   │   ├── yt_dlp_executor.py
│   │   ├── download_manager.py
│   │   ├── scheduler.py
│   │   └── config_parser.py
│   └── api/                   # REST エンドポイント
│       ├── downloads.py
│       ├── profiles.py
│       ├── history.py
│       ├── settings.py
│       └── scheduler.py
├── frontend/
│   ├── src/
│   │   ├── App.tsx           # メインアプリケーション
│   │   ├── components/        # UI コンポーネント
│   │   ├── store/            # Redux Toolkit ストア
│   │   ├── services/         # API クライアント
│   │   └── hooks/            # カスタムフック
│   └── package.json
└── README.md
```

## トラブルシューティング

### yt-dlp バイナリが見つからない
- ~/.yt-dlp-gui/bin に自動ダウンロードされます
- 手動: `~/.yt-dlp-gui/bin/yt-dlp --version`

### WebSocket 接続エラー
- バックエンドが実行中か確認: `http://localhost:8000/api/health`
- ファイアウォール設定を確認

### フロントエンドビルドエラー
```bash
cd frontend
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

## ライセンス

MIT

## 開発ロードマップ

- [ ] Parameter UI auto-generation from metadata
- [ ] WebSocket progress streaming
- [ ] Cross-platform packaging (Windows/macOS/Linux)
- [ ] Unit / Integration tests
- [ ] Plugin system for post-processing
