# Plan: yt-dlp GUI アプリケーション - モダンで完全なパラメータコントロール

## TL;DR

**React フロントエンド + Python FastAPI バックエンド** で、yt-dlpの全150+パラメータを制御できるモダンなGUIアプリケーションを構築します。

**理由**: Python開発者のみで開発可能、複雑な機能（スケジューリング、履歴管理、WebSocket実装）に対応、PyInstaller + Webpack で Windows/Mac/Linux に統一デプロイ。

**アーキテクチャ**:
- **フロントエンド**: React 18 + TypeScript + Shadcn/UI + Tailwind CSS (モダンデザイン)
- **状態管理**: Redux Toolkit
- **バックエンド**: Python FastAPI + SQLite + asyncio (非同期タスク管理)
- **スケジューラー**: croniter (cron式スケジューリング)
- **yt-dlp**: 動的ダウンロード（起動時に最新版を自動取得・キャッシュ）
- **IPC**: HTTP REST API + WebSocket (リアルタイム進捗表示)
- **デプロイ**: PyInstaller (Python) + Webpack (React) → 統合実行ファイル

---

## 詳細な実装ステップ

### **フェーズ 1: アーキテクチャ設計・初期セットアップ**

1. **ディレクトリ構造の定義**
   - `yt-dlp-gui/`
     - `backend/` - Python FastAPI アプリケーション
       - `app.py` - FastAPI メインアプリケーション
       - `models.py` - Pydantic データモデル（ダウンロード、プロファイル、履歴）
       - `database.py` - SQLAlchemy ORM + SQLite 初期化
       - `services/` - ビジネスロジック層
         - `yt_dlp_executor.py` - yt-dlp subprocess 実行・制御
         - `download_manager.py` - ダウンロード非同期タスク管理
         - `scheduler.py` - スケジューリング実装
         - `config_parser.py` - yt-dlp パラメータ解析・検証
       - `api/` - API エンドポイント
         - `downloads.py` - ダウンロード操作 (start/pause/cancel)
         - `profiles.py` - ダウンロードプロファイル管理
         - `settings.py` - ユーザー設定管理
         - `history.py` - ダウンロード履歴取得
     - `frontend/` - React TypeScript アプリケーション
       - `src/`
         - `components/` - React コンポーネント
           - `Sidebar.tsx` - ナビゲーション
           - `DownloadForm.tsx` - URL 入力 + パラメータ設定フォーム
           - `ProfileSelector.tsx` - プロファイル選択
           - `BasicSettings.tsx` - 基本パラメータ (~35個)
           - `AdvancedSettings.tsx` - 詳細パラメータ (~100個)
           - `RawOptions.tsx` - カスタムCLI オプション入力
           - `DownloadQueue.tsx` - ダウンロード待機中/実行中リスト
           - `ProgressBar.tsx` - リアルタイム進捗表示（WebSocket）
           - `HistoryPanel.tsx` - ダウンロード履歴
           - `SchedulerPanel.tsx` - スケジューリング設定
         - `hooks/` - カスタム React hooks
           - `useDownloads.ts` - ダウンロード状態管理
           - `useWebSocket.ts` - WebSocket 接続・リアルタイム更新
           - `useProfiles.ts` - プロファイル CRUD
         - `services/` - API クライアント
           - `api.ts` - Axios インスタンス + 全 API 呼び出し
           - `download_api.ts` - ダウンロード関連エンドポイント
         - `store/` - Redux Toolkit グローバル状態管理
           - `store.ts` - Redux ストア定義
           - `slices/downloadSlice.ts` - ダウンロード状態
           - `slices/profileSlice.ts` - プロファイル状態
           - `slices/historySlice.ts` - 履歴状態
         - `styles/` - CSS/Tailwind スタイル
         - `pages/` - ページコンポーネント
           - `Home.tsx` - メインダウンロードページ
           - `History.tsx` - 履歴一覧ページ
           - `Settings.tsx` - グローバル設定ページ
           - `Scheduler.tsx` - スケジューラーページ
       - `public/` - 静的アセット
     - `packaging/` - デプロイメント設定
       - `build_standalone.py` - PyInstaller + Webpack ビルドスクリプト
       - `requirements.txt` - Python 依存関係
       - `pyinstaller_spec.spec` - PyInstaller 設定
     - `docs/` - ドキュメント

2. **Python バックエンド初期実装**
   - Python 3.11+ 、FastAPI インストール
   - `app.py` で FastAPI アプリケーション生成
   - SQLAlchemy + SQLite による履歴・プロファイル永続化
   - CORS 設定（localhost:3000 に対応）
   - WebSocket エンドポイント定義 (`/ws/downloads/{task_id}`)

3. **React フロントエンド初期実装**
   - `vite` で初期セットアップ
   - TypeScript 設定
   - Shadcn/UI + Tailwind CSS インストール
   - Redux Toolkit で状態管理セットアップ
   - Axios 設定（FastAPI バックエンドへの通信）

---

### **フェーズ 2: yt-dlp パラメータマッピング・データモデル設計**

4. **yt-dlp パラメータメタデータ生成** *(Parallel with Phase 1)*
   - yt-dlp の `--help` 出力を解析し、JSON メタデータ生成
   - 各パラメータ情報:
     - `name`, `description`, `type` (bool/string/int/choice)
     - `category` (General/Network/Auth/Selection/Download/Filesystem/Format/Subtitle/PostProcessing)
     - `required`, `default_value`, `incompatible_with`, `depends_on`
   - **出力**: `backend/config/yt_dlp_params.json`
   - 例:
     ```json
     {
       "format": {
         "category": "Format Selection",
         "description": "動画形式を選択",
         "type": "string",
         "default": "best",
         "incompatible_with": ["simulate"],
         "ui_control": "autocomplete_with_suggestions"
       },
       "extract-audio": {
         "category": "Post-Processing",
         "type": "bool",
         "depends_on": ["format"],
         "default": false
       }
     }
     ```

5. **Pydantic データモデル定義**
   - `models.py` に以下を実装:
     - `DownloadProfile` - プロファイル (名前、パラメータセット、説明)
     - `DownloadTask` - ダウンロードタスク (ID、URL、プロファイル、パラメータ)
     - `DownloadHistory` - 履歴レコード (タスクID、URL、結果、タイムスタンプ、出力ファイル)
     - `ScheduledDownload` - スケジュール (cron式、URL、プロファイル、有効/無効フラグ)
     - `YtDlpParameter` - パラメータスキーマ (上記のメタデータマッピング)

6. **デフォルトプロファイル作成**
   - `mp3_extraction`: `--extract-audio --audio-format mp3 --audio-quality 192`
   - `best_video`: `-f bestvideo+bestaudio/best`
   - `mobile_optimized`: `-f 'best[height<=480]'`
   - `streaming`: `-f best --no-part`
   - `complete_playlist`: `--yes-playlist --write-all-subtitles`

---

### **フェーズ 3: バックエンド API エンドポイント実装**

7. **REST API エンドポイント実装**
   - **ダウンロード操作**:
     - `POST /api/downloads/start` - ダウンロード開始 (URL + パラメータ)
     - `GET /api/downloads/queue` - 待機中・実行中リスト
     - `GET /api/downloads/{task_id}/status` - タスク詳細
     - `POST /api/downloads/{task_id}/pause` - 一時停止
     - `POST /api/downloads/{task_id}/resume` - 再開
     - `DELETE /api/downloads/{task_id}` - キャンセル
   
   - **プロファイル管理**:
     - `GET /api/profiles` - プロファイル一覧
     - `POST /api/profiles` - 新規作成
     - `PUT /api/profiles/{profile_id}` - 更新
     - `DELETE /api/profiles/{profile_id}` - 削除
     - `POST /api/profiles/{profile_id}/duplicate` - コピー作成
   
   - **履歴・統計**:
     - `GET /api/history?limit=50&offset=0` - ダウンロード履歴
     - `DELETE /api/history/{history_id}` - 履歴削除
     - `GET /api/stats` - 統計情報 (総件数、成功数、失敗数、総容量)
     - `POST /api/history/export` - CSV エクスポート
   
   - **設定管理**:
     - `GET /api/settings` - グローバル設定取得
     - `PUT /api/settings` - 設定変更 (デフォルト出力フォルダ、プロキシ等)
     - `GET /api/yt-dlp/parameters` - 全パラメータメタデータ
   
   - **スケジューラー**:
     - `GET /api/scheduler/tasks` - スケジュール一覧
     - `POST /api/scheduler/tasks` - 新規スケジュール
     - `PUT /api/scheduler/tasks/{schedule_id}` - 更新
     - `DELETE /api/scheduler/tasks/{schedule_id}` - 削除
   
   - **ファイル操作**:
     - `POST /api/config/export` - 設定ファイルエクスポート
     - `POST /api/config/import` - 設定ファイルインポート

8. **WebSocket エンドポイント実装**
   - `WS /ws/downloads/{task_id}` - リアルタイムプログレス配信
   - メッセージスキーマ:
     ```json
     {
       "type": "progress|error|complete",
       "data": {
         "percent": 45.5,
         "speed": "2.5MB/s",
         "eta": "00:02:15",
         "filename": "video.mp4"
       }
     }
     ```

9. **非同期タスク管理** (`download_manager.py`)
   - `asyncio.Queue` でダウンロード待機キュー
   - `asyncio.Task` でバックグラウンド実行
   - 最大並列ダウンロード数制御 (デフォルト: 3)
   - yt-dlp subprocess の stdout/stderr をリアルタイムパース
   - 正規表現で進捗情報抽出: `\[download\]\s*(\d+\.\d+)%`, `ETA\s*(\d{2}:\d{2}:\d{2})`

10. **スケジューラー実装** (`scheduler.py`)
    - APScheduler または croniter ライブラリ利用
    - cron 式サポート: `0 22 * * *` (毎日22:00)
    - スケジュール実行時にダウンロードキューに自動追加
    - 失敗時リトライロジック

---

### **フェーズ 4: フロントエンド UI 実装**

11. **基本パラメータフォーム** (`BasicSettings.tsx`) - **ユーザーが最初に見る画面**
    - 実装対象: ~35個の頻出パラメータ
    - グループ化表示:
      - **基本**: URL、出力フォルダ、フォーマット選択
      - **認証**: ユーザー名、パスワード
      - **字幕**: 字幕ダウンロード (yes/no/English/日本語)
      - **オーディオ**: オーディオ抽出、音声品質
      - **プロキシ**: プロキシ URL、ソケットタイムアウト
      - **詳細オプション**: 通知「詳細設定へ」

12. **詳細パラメータフォーム** (`AdvancedSettings.tsx`)
    - 実装対象: ~80-100個の追加パラメータ
    - タブ式レイアウト:
      - Format Selection
      - Download Options
      - Authentication
      - Network / Proxy
      - Post-Processing
      - Filesystem
      - その他
    - 各フォームコントロール:
      - テキスト入力 (string 型)
      - トグル (bool 型)
      - ドロップダウン (choice 型)
      - スライダー (int 型、範囲制限)
      - マルチセレクト (複数選択)

13. **カスタムCLIオプション** (`RawOptions.tsx`)
    - テキストエリアで任意の yt-dlp コマンドラインオプション入力
    - 構文ハイライト (highlight.js)
    - 入力値の簡易バリデーション
    - 例: `--socket-timeout 30 --skip-unavailable-fragments`

14. **プロファイルセレクター・管理** (`ProfileSelector.tsx`)
    - プロファイル一覧ドロップダウン
    - 新規作成/編集/削除ボタン
    - 現在のパラメータをプロファイルに保存する「名前を付けて保存」機能

15. **ダウンロードキュー表示** (`DownloadQueue.tsx`)
    - テーブル形式で表示:
      - URL、ステータス (待機中/ダウンロード中/完了/エラー)
      - 進捗 (%)、速度、残り時間
      - アクション: 一時停止/再開/キャンセルボタン
    - リアルタイム更新 (WebSocket)

16. **プログレスバー** (`ProgressBar.tsx`)
    - WebSocket でリアルタイム受信
    - 進捗率 (%)、速度 (MB/s)、ETA 表示
    - アニメーション効果

17. **履歴パネル** (`HistoryPanel.tsx`)
    - ダウンロード履歴テーブル:
      - URL、完了日時、出力ファイル名、サイズ、ステータス
    - フィルター: 成功/失敗、日時範囲
    - 履歴削除、CSV エクスポート

18. **スケジューラーパネル** (`SchedulerPanel.tsx`)
    - 新規スケジュール作成フォーム:
      - Cron 式入力 (またはGUIビルダー)
      - 実行するプロファイル選択
      - ダウンロード URL (複数行対応)
    - スケジュール一覧、編集、削除、有効/無効切り替え

19. **グローバル設定ページ** (`Settings.tsx`)
    - デフォルト出力フォルダ
    - 最大並列ダウンロード数
    - デフォルトプロキシ設定
    - FFmpeg/yt-dlp バイナリ パス設定
    - テーマ選択 (Light/Dark)
    - 設定ファイルのインポート/エクスポート

---

### **フェーズ 5: パラメータ検証・依存関係処理**

20. **パラメータ相互依存関係の処理** (`config_parser.py`)
    - yt-dlp メタデータから依存関係定義読み込み
    - UI で選択時に自動調整:
      - 例: `extract-audio` 選択時 → `format` を `bestaudio/best` に自動変更
      - 例: `simulate` 選択時 → `extract-audio` 選択肢を無効化
    - フロントエンド側でも同期バリデーション

21. **パラメータ値のバリデーション**
    - Pydantic `validator` で型チェック、範囲チェック
    - 例: `socket-timeout` は正の整数のみ
    - 例: `format` は yt-dlp 形式文字列 (正規表現チェック)
    - エラー時は フロントエンドに詳細エラーメッセージ返却

---

### **フェーズ 6: パッケージング・デプロイメント**

22. **PyInstaller でバックエンド をEXE化** (`packaging/build_standalone.py`)
    - `requirements.txt` で依存ライブラリ指定:
      - fastapi, uvicorn, sqlalchemy, croniter
    - PyInstaller で `.spec` ファイル生成:
      - yt-dlp は同梱せず、起動時に自動ダウンロード（最新版を常に使用）
      - FFmpeg も起動時に確認、なければダウンロード (オプション)
      - 単一ファイルモード (`--onefile`)
    - 出力: `dist/backend.exe` (Windows), `dist/backend` (Linux/Mac)

23. **Webpack でフロントエンドをバンドル**
    - `npm run build` で本番ビルド
    - React + TypeScript をコンパイル
    - CSS、画像 最適化
    - 出力: `dist/frontend/` (静的HTML/JS/CSS)

24. **統合実行スクリプト** (`build_standalone.py`)
    - 以下の順序で実行:
      1. React ビルド (`npm run build`)
      2. PyInstaller ビルド (`pyinstaller ...`)
      3. React 出力 を PyInstaller リソースディレクトリにコピー
      4. FastAPI に静的ファイル配信設定
    - 最終成果物: `dist/yt-dlp-gui.exe` (Windows), `dist/yt-dlp-gui` (Linux/Mac)

25. **各プラットフォーム向けインストーラー**
    - **Windows**: NSIS インストーラー (`yt-dlp-gui-setup.exe`)
    - **Mac**: DMG イメージ (`yt-dlp-gui.dmg`)
    - **Linux**: AppImage (`yt-dlp-gui-x86_64.AppImage`) または deb パッケージ

26. **自動アップデート機構** (オプション - フェーズ2で検討)
    - electron-updater または py2exe 用アップデートスクリプト
    - GitHub Releases からダウンロード

---

### **フェーズ 7: テスト・QA**

27. **ユニットテスト** 
    - バックエンド: pytest で FastAPI エンドポイント
    - フロントエンド: Jest + React Testing Library で コンポーネント

28. **統合テスト**
    - end-to-end テスト (Playwright/Cypress)
    - ダウンロード機能の実機テスト
    - 複数プラットフォーム (Windows/Mac/Linux)

29. **手動QA**
    - パラメータ組み合わせテスト (150+個の中から サンプル組み合わせ)
    - エラーハンドリング (ネットワークエラー、パラメータ不正値等)
    - UI/UX レビュー (モダンデザインの確認)

---

## 関連ファイル

### バックエンド
- `backend/app.py` — FastAPI メインアプリケーション、ルート定義
- `backend/models.py` — Pydantic データモデル (DownloadTask, Profile, etc.)
- `backend/database.py` — SQLAlchemy ORM、SQLite 初期化
- `backend/services/yt_dlp_executor.py` — yt-dlp subprocess 実行・制御、stdout パース
- `backend/services/download_manager.py` — 非同期タスク管理、キュー処理
- `backend/services/scheduler.py` — croniter 統合、cron スケジュール実行
- `backend/services/config_parser.py` — yt-dlp パラメータメタデータ解析
- `backend/api/downloads.py` — ダウンロード API エンドポイント
- `backend/api/profiles.py` — プロファイル管理 API
- `backend/api/history.py` — 履歴取得 API
- `backend/api/settings.py` — グローバル設定 API
- `backend/api/scheduler.py` — スケジューラー API
- `backend/config/yt_dlp_params.json` — パラメータメタデータ (自動生成)

### フロントエンド
- `frontend/src/components/DownloadForm.tsx` — メインフォーム (URL入力 + パラメータ)
- `frontend/src/components/BasicSettings.tsx` — 基本パラメータ (~35個)
- `frontend/src/components/AdvancedSettings.tsx` — 詳細パラメータ (~100個)
- `frontend/src/components/RawOptions.tsx` — カスタム CLI オプション
- `frontend/src/components/ProfileSelector.tsx` — プロファイル管理UI
- `frontend/src/components/DownloadQueue.tsx` — ダウンロードキュー表示
- `frontend/src/components/ProgressBar.tsx` — リアルタイム進捗表示
- `frontend/src/components/HistoryPanel.tsx` — 履歴一覧
- `frontend/src/components/SchedulerPanel.tsx` — スケジューラーUI
- `frontend/src/hooks/useDownloads.ts` — ダウンロード状態管理
- `frontend/src/hooks/useWebSocket.ts` — WebSocket 接続フック
- `frontend/src/services/api.ts` — FastAPI クライアント

### デプロイメント
- `packaging/build_standalone.py` — 統合ビルドスクリプト
- `packaging/requirements.txt` — Python 依存関係
- `packaging/pyinstaller_spec.spec` — PyInstaller 設定
- `frontend/package.json` — Node.js 依存関係

---

## 検証ステップ

1. **バックエンド検証** (フェーズ3完了後):
   - `pytest backend/` で API エンドポイントテスト
   - Postman で各 API 手動確認
   - yt-dlp subprocess 実行確認 (進捗出力の正しい解析)

2. **フロントエンド検証** (フェーズ4完了後):
   - `npm test` でコンポーネントテスト
   - ブラウザで UI 表示確認 (Material-UI/Tailwind スタイル)
   - API 呼び出しの確認 (Network タブ)

3. **統合検証** (フェーズ5完了後):
   - React + FastAPI ローカル実行で全機能テスト
   - WebSocket でのリアルタイム更新確認
   - パラメータ依存関係の自動調整確認

4. **パッケージング検証** (フェーズ6完了後):
   - PyInstaller EXE 実行確認 (Windows)
   - DMG イメージ確認 (Mac)
   - AppImage 実行確認 (Linux)

---

## 意思決定・スコープ

### **含まれる機能** ✅
- yt-dlp 全 150+ パラメータのUI制御
- 複数ダウンロードプロファイル
- ダウンロード履歴・管理
- リアルタイムプログレス表示
- スケジューリング・自動ダウンロード
- 設定のインポート/エクスポート
- 高度なネットワーク設定 (プロキシ、認証)

### **フェーズ2以降で検討** ⏳
- GUI でのプロキシチェーン設定 UI
- ダウンロード再開 (一度完了したタスクの再実行)
- プラグインシステム

### **スコープ外** ❌
- モバイルアプリ (Web API は対応可能→今後の追加)
- ローカルサーバー以外への配置
- 複数ユーザー認証

---

## 最終技術スタック決定

✅ **確定事項**
1. **UI フレームワーク**: Shadcn/UI + Tailwind CSS
   - モダンで美しいコンポーネント設計
   - 軽量で高速なビルド

2. **状態管理**: Redux Toolkit
   - スケーラビリティ重視
   - DevTools 統合で開発効率向上

3. **yt-dlp 実行戦略**: 動的ダウンロード（起動時に最新版を自動取得）
   - 常に最新機能を利用可能
   - ユーザーが手動アップデート不要
   - ローカルキャッシュで起動速度最適化

4. **スケジューラー**: croniter
   - Python の軽量ライブラリ
   - cron 式で直感的にスケジュール定義
   - APScheduler と比べてシンプル・高速

5. **デプロイ戦略**: Python エージェント任せ
   - PyInstaller での単一実行ファイル化
   - Webpack での React バンドル
   - 統合スクリプトで完全自動化
