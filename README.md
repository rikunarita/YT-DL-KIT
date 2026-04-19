#  WeaveDLX - Modern Download Manager

[日本語](#-日本語) | [English](#-english) | [中文](#-中文)

---

## 🇯🇵 日本語

モダンな web UI で yt-dlp の全機能を制御できるデスクトップアプリケーション。

### 機能

- ✅ yt-dlp の 150+ パラメータをフルサポート
- ✅ 複数並列ダウンロード管理（スケジューラ対応）
- ✅ ダウンロード履歴・統計情報
- ✅ プロファイル管理
- ✅ Cron ベーススケジューリング
- ✅ リアルタイムプログレス表示

### 技術スタック

**Backend**:
- Python 3.9+ with FastAPI
- SQLAlchemy ORM + SQLite
- croniter スケジューラ
- 動的 yt-dlp バイナリダウンロード

**Frontend**:
- React 18 + TypeScript
- Redux Toolkit（状態管理）
- Tailwind CSS + Shadcn/UI
- Vite（ビルドツール）

### セットアップ

#### 初回セットアップ（推奨）

プロジェクトルートから以下のコマンドを実行してください：

```bash
python setup.py
```

**実行結果の例：**
```
╔════════════════════════════════════════════════════════════╗
║           WeaveDLX - Project Setup                         ║
╚════════════════════════════════════════════════════════════╝

✅ Backend setup complete
✅ Frontend setup complete

Next steps:
1. Start the backend: cd backend && python -m uvicorn app:app --reload --port 8000
2. Start the frontend: cd frontend && npm run dev
3. Open http://localhost:5173 in your browser
```

#### バックエンド開発サーバー起動

**方法 1：プロジェクトルートから起動（推奨）**

```bash
python -m uvicorn backend.app:app --reload --port 8000
```

**方法 2：バックエンドディレクトリから起動**

```bash
cd backend
python -m uvicorn app:app --reload --port 8000
```

**起動確認：**

ターミナルに以下のメッセージが表示されたら成功です：
```
🚀 yt-dlp GUI サーバー起動中...
✅ データベース初期化完了
✅ yt-dlp バイナリ: /home/user/.yt-dlp-gui/bin/yt-dlp
✅ yt-dlp GUI サーバー準備完了
INFO:     Uvicorn running on http://127.0.0.1:8000
```

ブラウザで http://localhost:8000/api/health にアクセスして、以下のレスポンスが返ってくることを確認してください：
```json
{"status":"healthy","yt_dlp_path":"/home/user/.yt-dlp-gui/bin/yt-dlp"}
```

#### フロントエンド開発サーバー起動

**別のターミナルウィンドウで以下を実行してください：**

```bash
cd frontend
npm install
npm run dev
```

**起動確認：**

ターミナルに以下のように表示されたら成功です：
```
  VITE v5.4.21  ready in 212 ms
  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

ブラウザで http://localhost:5173 を開く（デフォルトポート、使用中の場合は自動的に次のポート 5174, 5175... が割り当てられます）

### ビルド

#### プロダクション フロントエンド アセットのビルド

**方法 1：setup.py を使用（推奨）**

```bash
python setup.py --build-frontend
```

**方法 2：手動でビルド**

```bash
cd frontend
npm run build
```

ビルド結果は `frontend/dist` ディレクトリに出力されます。

#### スタンドアロン実行ファイル生成（Windows/macOS/Linux）

PyInstaller を使用してスタンドアロン実行ファイルを生成します：

```bash
cd packaging
python build_standalone.py
```

**プラットフォーム指定：**
```bash
python build_standalone.py --platform windows   # Windows のみ
python build_standalone.py --platform macos     # macOS のみ
python build_standalone.py --platform linux     # Linux のみ
python build_standalone.py --platform all       # すべてのプラットフォーム
```

生成されたファイルは `packaging/dist` ディレクトリに出力されます。

### API ドキュメント

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### ファイル構成

```
yt-dlp-gui/
├── backend/
│   ├── __init__.py
│   ├── app.py                 # FastAPI メインアプリケーション
│   ├── models.py              # Pydantic データモデル
│   ├── database.py            # SQLAlchemy ORM定義
│   ├── requirements.txt        # Python 依存パッケージ
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
│   │   ├── App.tsx            # メインアプリケーション
│   │   ├── main.tsx
│   │   ├── i18n.tsx           # 多言語対応
│   │   ├── components/        # UI コンポーネント
│   │   ├── store/             # Redux Toolkit ストア
│   │   ├── services/          # API クライアント
│   │   ├── hooks/             # カスタムフック
│   │   └── styles/            # CSS スタイル
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
├── packaging/
│   ├── build_standalone.py
│   └── yt_dlp_gui.spec
├── setup.py                    # プロジェクト初期化スクリプト
└── README.md
```

### トラブルシューティング

#### ❌ バックエンド起動エラー: "Address already in use"

**原因：** ポート 8000 が既に使用されている

**解決方法：**
```bash
# ポート 8001 を使用して起動
python -m uvicorn backend.app:app --reload --port 8001

# または、既存プロセスを終了
pkill -f "python -m uvicorn"
```

#### ❌ yt-dlp バイナリが見つからない

**原因：** yt-dlp バイナリの自動ダウンロードに失敗した

**解決方法：**
```bash
# 手動で確認
~/.yt-dlp-gui/bin/yt-dlp --version

# キャッシュをリセット
rm -rf ~/.yt-dlp-gui/
python setup.py
```

#### ❌ WebSocket 接続エラー

**原因：** バックエンドが起動していないか、ファイアウォール設定

**解決方法：**
1. バックエンドが実行中か確認: http://localhost:8000/api/health
2. ファイアウォール設定を確認（ポート 8000 を許可）

#### ❌ フロントエンドビルドエラー

**原因：** Node.js 依存パッケージのキャッシュが破損

**解決方法：**
```bash
cd frontend
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
npm run build
```

### ライセンス

MIT

---

## 🇬🇧 English

A modern web UI to control all yt-dlp features in a desktop application.

### Features

- ✅ Full support for 150+ yt-dlp parameters
- ✅ Multi-threaded download management with scheduler support
- ✅ Download history and statistics
- ✅ Profile management
- ✅ Cron-based scheduling
- ✅ Real-time progress display

### Tech Stack

**Backend**:
- Python 3.9+ with FastAPI
- SQLAlchemy ORM + SQLite
- croniter scheduler
- Dynamic yt-dlp binary download

**Frontend**:
- React 18 + TypeScript
- Redux Toolkit for state management
- Tailwind CSS + Shadcn/UI
- Vite build tool

### Setup

#### Initial Setup (Recommended)

Run the following command from the project root:

```bash
python setup.py
```

**Expected output:**
```
╔════════════════════════════════════════════════════════════╗
║           WeaveDLX - Project Setup                         ║
╚════════════════════════════════════════════════════════════╝

✅ Backend setup complete
✅ Frontend setup complete

Next steps:
1. Start the backend: cd backend && python -m uvicorn app:app --reload --port 8000
2. Start the frontend: cd frontend && npm run dev
3. Open http://localhost:5173 in your browser
```

#### Starting Backend Development Server

**Method 1: From project root (Recommended)**

```bash
python -m uvicorn backend.app:app --reload --port 8000
```

**Method 2: From backend directory**

```bash
cd backend
python -m uvicorn app:app --reload --port 8000
```

**Verification:**

You should see these messages in the terminal:
```
🚀 yt-dlp GUI サーバー起動中...
✅ データベース初期化完了
✅ yt-dlp バイナリ: /home/user/.yt-dlp-gui/bin/yt-dlp
✅ yt-dlp GUI サーバー準備完了
INFO:     Uvicorn running on http://127.0.0.1:8000
```

Visit http://localhost:8000/api/health in your browser. You should receive:
```json
{"status":"healthy","yt_dlp_path":"/home/user/.yt-dlp-gui/bin/yt-dlp"}
```

#### Starting Frontend Development Server

**Run in a separate terminal window:**

```bash
cd frontend
npm install
npm run dev
```

**Verification:**

You should see:
```
  VITE v5.4.21  ready in 212 ms
  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

Open http://localhost:5173 in your browser (if port 5173 is in use, Vite will automatically use 5174, 5175, etc.)

### Build

#### Building Production Frontend Assets

**Method 1: Using setup.py (Recommended)**

```bash
python setup.py --build-frontend
```

**Method 2: Manual build**

```bash
cd frontend
npm run build
```

Build output is saved to `frontend/dist` directory.

#### Generating Standalone Executables (Windows/macOS/Linux)

Use PyInstaller to generate standalone executables:

```bash
cd packaging
python build_standalone.py
```

**Platform-specific builds:**
```bash
python build_standalone.py --platform windows   # Windows only
python build_standalone.py --platform macos     # macOS only
python build_standalone.py --platform linux     # Linux only
python build_standalone.py --platform all       # All platforms
```

Output files are generated in `packaging/dist` directory.

### API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Project Structure

```
yt-dlp-gui/
├── backend/
│   ├── __init__.py
│   ├── app.py                 # FastAPI main application
│   ├── models.py              # Pydantic data models
│   ├── database.py            # SQLAlchemy ORM definitions
│   ├── requirements.txt        # Python dependencies
│   ├── services/              # Business logic layer
│   │   ├── yt_dlp_executor.py
│   │   ├── download_manager.py
│   │   ├── scheduler.py
│   │   └── config_parser.py
│   └── api/                   # REST API endpoints
│       ├── downloads.py
│       ├── profiles.py
│       ├── history.py
│       ├── settings.py
│       └── scheduler.py
├── frontend/
│   ├── src/
│   │   ├── App.tsx            # Main application
│   │   ├── main.tsx
│   │   ├── i18n.tsx           # Multi-language support
│   │   ├── components/        # UI components
│   │   ├── store/             # Redux Toolkit store
│   │   ├── services/          # API client
│   │   ├── hooks/             # Custom hooks
│   │   └── styles/            # CSS styles
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
├── packaging/
│   ├── build_standalone.py
│   └── yt_dlp_gui.spec
├── setup.py                    # Project initialization script
└── README.md
```

### Troubleshooting

#### ❌ Backend Error: "Address already in use"

**Cause:** Port 8000 is already in use

**Solution:**
```bash
# Use a different port
python -m uvicorn backend.app:app --reload --port 8001

# Or terminate existing processes
pkill -f "python -m uvicorn"
```

#### ❌ yt-dlp Binary Not Found

**Cause:** Automatic yt-dlp binary download failed

**Solution:**
```bash
# Check manually
~/.yt-dlp-gui/bin/yt-dlp --version

# Reset cache
rm -rf ~/.yt-dlp-gui/
python setup.py
```

#### ❌ WebSocket Connection Error

**Cause:** Backend not running or firewall issue

**Solution:**
1. Verify backend is running: http://localhost:8000/api/health
2. Check firewall settings (allow port 8000)

#### ❌ Frontend Build Error

**Cause:** Corrupted Node.js dependency cache

**Solution:**
```bash
cd frontend
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
npm run build
```

### License

MIT

---

## 🇨🇳 中文

一个现代化的网页 UI，可以在桌面应用中控制 yt-dlp 的所有功能。

### 功能

- ✅ 完全支持 150+ 个 yt-dlp 参数
- ✅ 多线程下载管理（支持调度器）
- ✅ 下载历史记录和统计信息
- ✅ 配置文件管理
- ✅ 基于 Cron 的定时调度
- ✅ 实时进度显示

### 技术栈

**后端**:
- Python 3.9+ with FastAPI
- SQLAlchemy ORM + SQLite
- croniter 定时器
- 动态 yt-dlp 二进制文件下载

**前端**:
- React 18 + TypeScript
- Redux Toolkit 状态管理
- Tailwind CSS + Shadcn/UI
- Vite 构建工具

### 设置

#### 初始化设置（推荐）

从项目根目录运行以下命令：

```bash
python setup.py
```

**预期输出：**
```
╔════════════════════════════════════════════════════════════╗
║           WeaveDLX - Project Setup                         ║
╚════════════════════════════════════════════════════════════╝

✅ Backend setup complete
✅ Frontend setup complete

Next steps:
1. Start the backend: cd backend && python -m uvicorn app:app --reload --port 8000
2. Start the frontend: cd frontend && npm run dev
3. Open http://localhost:5173 in your browser
```

#### 启动后端开发服务器

**方法 1：从项目根目录启动（推荐）**

```bash
python -m uvicorn backend.app:app --reload --port 8000
```

**方法 2：从后端目录启动**

```bash
cd backend
python -m uvicorn app:app --reload --port 8000
```

**验证：**

终端应显示以下消息：
```
🚀 yt-dlp GUI サーバー起動中...
✅ データベース初期化完了
✅ yt-dlp バイナリ: /home/user/.yt-dlp-gui/bin/yt-dlp
✅ yt-dlp GUI サーバー準備完了
INFO:     Uvicorn running on http://127.0.0.1:8000
```

在浏览器中访问 http://localhost:8000/api/health，应获得响应：
```json
{"status":"healthy","yt_dlp_path":"/home/user/.yt-dlp-gui/bin/yt-dlp"}
```

#### 启动前端开发服务器

**在另一个终端窗口运行：**

```bash
cd frontend
npm install
npm run dev
```

**验证：**

终端应显示：
```
  VITE v5.4.21  ready in 212 ms
  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

在浏览器中打开 http://localhost:5173（如果端口 5173 已被占用，Vite 会自动使用 5174、5175 等）

### 构建

#### 构建生产环境前端资源

**方法 1：使用 setup.py（推荐）**

```bash
python setup.py --build-frontend
```

**方法 2：手动构建**

```bash
cd frontend
npm run build
```

构建输出保存到 `frontend/dist` 目录。

#### 生成独立可执行文件（Windows/macOS/Linux）

使用 PyInstaller 生成独立可执行文件：

```bash
cd packaging
python build_standalone.py
```

**特定于平台的构建：**
```bash
python build_standalone.py --platform windows   # 仅 Windows
python build_standalone.py --platform macos     # 仅 macOS
python build_standalone.py --platform linux     # 仅 Linux
python build_standalone.py --platform all       # 所有平台
```

输出文件生成在 `packaging/dist` 目录。

### API 文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 项目结构

```
yt-dlp-gui/
├── backend/
│   ├── __init__.py
│   ├── app.py                 # FastAPI 主应用程序
│   ├── models.py              # Pydantic 数据模型
│   ├── database.py            # SQLAlchemy ORM 定义
│   ├── requirements.txt        # Python 依赖项
│   ├── services/              # 业务逻辑层
│   │   ├── yt_dlp_executor.py
│   │   ├── download_manager.py
│   │   ├── scheduler.py
│   │   └── config_parser.py
│   └── api/                   # REST API 端点
│       ├── downloads.py
│       ├── profiles.py
│       ├── history.py
│       ├── settings.py
│       └── scheduler.py
├── frontend/
│   ├── src/
│   │   ├── App.tsx            # 主应用程序
│   │   ├── main.tsx
│   │   ├── i18n.tsx           # 多语言支持
│   │   ├── components/        # UI 组件
│   │   ├── store/             # Redux Toolkit 存储
│   │   ├── services/          # API 客户端
│   │   ├── hooks/             # 自定义钩子
│   │   └── styles/            # CSS 样式
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
├── packaging/
│   ├── build_standalone.py
│   └── yt_dlp_gui.spec
├── setup.py                    # 项目初始化脚本
└── README.md
```

### 故障排除

#### ❌ 后端错误："Address already in use"

**原因：** 端口 8000 已被占用

**解决方案：**
```bash
# 使用不同的端口
python -m uvicorn backend.app:app --reload --port 8001

# 或终止现有进程
pkill -f "python -m uvicorn"
```

#### ❌ yt-dlp 二进制文件未找到

**原因：** 自动下载 yt-dlp 二进制文件失败

**解决方案：**
```bash
# 手动检查
~/.yt-dlp-gui/bin/yt-dlp --version

# 重置缓存
rm -rf ~/.yt-dlp-gui/
python setup.py
```

#### ❌ WebSocket 连接错误

**原因：** 后端未运行或防火墙问题

**解决方案：**
1. 验证后端是否运行: http://localhost:8000/api/health
2. 检查防火墙设置（允许端口 8000）

#### ❌ 前端构建错误

**原因：** Node.js 依赖项缓存损坏

**解决方案：**
```bash
cd frontend
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
npm run build
```

### 许可证

MIT

### 开发路线图

- [ ] 从元数据自动生成参数 UI
- [ ] WebSocket 进度流
- [ ] 跨平台打包（Windows/macOS/Linux）
- [ ] 单元/集成测试
- [ ] 后处理插件系统

