# 🚀 WeaveDLX - クイックスタート

## インストール

### 自動セットアップ
```bash
cd /home/user/WeaveDLX
./setup.sh
```

### 手動セットアップ
```bash
# バックエンド依存パッケージ
cd /home/user/WeaveDLX/backend
pip install -r requirements.txt

# フロントエンド依存パッケージ (Node.js 必要)
cd /home/user/WeaveDLX/frontend
npm install
```

---

## 実行方法

### ✅ 必須：親ディレクトリから実行

**重要:** バックエンドは必ず `/home/user/WeaveDLX` ディレクトリから実行してください。

### ターミナル 1: バックエンド起動

```bash
# ❌ 間違い
cd /home/user/WeaveDLX/backend
python -m uvicorn app:app --reload

# ✅ 正しい
cd /home/user/WeaveDLX
python -m uvicorn backend.app:app --reload --port 8000
```

出力例：
```
INFO:     Uvicorn running on http://127.0.0.1:8000
✅ WeaveDLX サーバー準備完了
```

### ターミナル 2: フロントエンド起動

```bash
cd /home/user/WeaveDLX/frontend
npm run dev
```

出力例：
```
➜  Local:   http://localhost:5173/
```

### ブラウザで開く

```
http://localhost:5173
```

---

## トラブルシューティング

### エラー: `ImportError: attempted relative import with no known parent package`

**原因:** `backend` ディレクトリから uvicorn を実行している

**解決:**
```bash
# ❌ 間違い
cd backend && python -m uvicorn app:app --reload

# ✅ 正しい
cd .. && python -m uvicorn backend.app:app --reload
```

### エラー: `ERROR: Could not open requirements file`

**原因:** `requirements.txt` のあるディレクトリにいない

**解決:**
```bash
# ❌ 間違い
cd frontend && pip install -r requirements.txt

# ✅ 正しい
cd backend && pip install -r requirements.txt
```

### エラー: `npm: command not found`

**原因:** Node.js がインストールされていない

**解決:**
```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo bash -
sudo apt-get install nodejs

# macOS
brew install node

# その後、フロントエンド再セットアップ
cd frontend
npm install
npm run dev
```

---

## ポート設定

デフォルトポート：
- バックエンド: `8000`
- フロントエンド: `5173`

ポートを変更する場合：

```bash
# バックエンド（別ポート）
python -m uvicorn backend.app:app --port 8001

# フロントエンド（別ポート）
cd frontend && npm run dev -- --port 3000
```

フロントエンドの API proxy も調整が必要な場合があります：
- `frontend/vite.config.ts` の `/api` proxy を確認・修正

---

## ビルド（スタンドアロン実行可能ファイル）

```bash
cd packaging
python build_standalone.py --platform all
```

出力：
- `dist/weavedlx-windows-x86_64.exe`
- `dist/weavedlx-macos-universal`
- `dist/weavedlx-linux-x86_64`

---

## テスト実行

### バックエンド統合テスト
```bash
cd /home/user/WeaveDLX
python test_backend.py
```

期待結果: `4/4 PASS`

### API ドキュメント（実行中のサーバー）

バックエンド起動後：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## よくある質問

**Q: ポート 8000 が既に使用中です**
```bash
# 別のプロセスを確認
lsof -i :8000

# または別ポートで起動
python -m uvicorn backend.app:app --port 8001
```

**Q: WebSocket が接続できません**
- バックエンドが起動しているか確認
- ファイアウォール設定を確認
- ブラウザのコンソール（F12）でエラーを確認

**Q: CORS エラーが表示される**
- バックエンド CORS 設定を確認: `backend/app.py`
- フロントエンド API proxy を確認: `frontend/vite.config.ts`

---

## ディレクトリ構造

```
WeaveDLX/
├── backend/           # FastAPI バックエンド
│   ├── app.py
│   ├── requirements.txt
│   ├── models.py
│   ├── database.py
│   ├── services/
│   └── api/
├── frontend/          # React フロントエンド
│   ├── src/
│   ├── package.json
│   ├── vite.config.ts
│   └── index.html
├── tests/             # テストファイル
├── packaging/         # ビルド設定
├── test_backend.py    # 統合テスト
└── setup.sh           # セットアップスクリプト
```

---

**最終更新**: 2026-04-17
