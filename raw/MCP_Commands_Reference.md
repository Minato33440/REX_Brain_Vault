# MCP コマンド・ツール一覧（ユーザー用リファレンス）

## 📌 MCP（Model Context Protocol）とは

Claude が外部サービス・ツール・データベースにアクセスするための仲介層。複数の MCP を同時に登録することで、Claude Desktop から様々なサービスを統合的に利用可能。

**MCP の役割：**
```
Claude Desktop (ユーザーの質問)
    ↓
MCP サーバー（仲介役）
    ↓
外部サービス（Grok API、GitHub、NotebookLM など）
    ↓
Claude がまとめて返す
```

Claude は自動判断で最適な MCP を選択。必要に応じて `@mcp_name` で明示指定も可能。

---

## 📁 Filesystem MCP
**ファイル・ディレクトリ操作**

> **仕組み:** Claude が指定ディレクトリ内のファイルに直接アクセス。ローカルファイルを読み書き・管理

- `read_text_file` - **ファイル内容読み込み**（テキスト・マークダウン・コードを読込。head/tail で部分読みも可）
- `read_multiple_files` - **複数ファイル一括読み込み**（複数のパスを同時に読む）
- `write_file` - **ファイル作成・上書き**（新規作成または既存ファイルを全上書き）
- `edit_file` - **行単位の部分編集**（oldText→newText の置換。git 形式 diff を返す。dryRun でプレビュー可）
- `list_directory` - **ディレクトリ一覧**（フォルダ内のファイル・フォルダ一覧表示）
- `directory_tree` - **ツリー表示**（ディレクトリ構造を再帰的に JSON で取得）
- `create_directory` - **ディレクトリ作成**（新しいフォルダを作成）
- `move_file` - **ファイル移動・リネーム**（別フォルダへ移動または名前変更）
- `search_files` - **ファイル検索**（パターンでファイル・ディレクトリを再帰検索）
- `get_file_info` - **ファイル情報取得**（サイズ・作成/更新日時・権限・種別などのメタデータ）
- `list_allowed_directories` - **許可ディレクトリ一覧**（アクセス可能なルートを確認）

> **注:** この MCP は**永続削除（delete）ツールを持たない**。ファイル削除が必要なときはユーザーが手動で行う。

**対象パス:** `C:\Users\Setona\Desktop`, `C:\Users\Setona\Downloads`, `C:\Python\REX_AI`

---

## 💬 Hermes MCP
**メッセージング・会話管理（Telegram、Discord、Slack など全プラットフォーム対応）**

> **仕組み:** Hermes エージェント（ローカル実行）が複数プラットフォームの会話データを一元管理。Claude が Hermes API を経由してメッセージを送受信・監視

### 会話・メッセージ操作
- `conversations_list` - **全プラットフォームの会話一覧取得**（Telegram、Discord、Slack など）
- `conversation_get` - **特定の会話情報取得**（スレッド・チャネル情報を取得）
- `messages_read` - **メッセージ履歴読み込み**（過去メッセージをClaudeに提供）
- `messages_send` - **メッセージ送信**（Telegram/Discord/Slack などに直接投稿）
- `attachments_fetch` - **添付ファイル取得**（メッセージ内のファイルを取得）

### イベント・ポーリング
- `events_poll` - ライブイベント確認（ノンブロッキング）
- `events_wait` - イベント待機（ブロッキング）

### チャネル・権限管理
- `channels_list` - 利用可能なチャネル一覧
- `permissions_list_open` - 保留中の権限リスト
- `permissions_respond` - 権限リクエストに応答

> **注意:** `hermes mcp serve` が公開するのは上記の**会話（メッセージング）ツールのみ**。
> Grok を直接叩くツールは含まれない。また `HERMES_HOME` を gateway と揃えないと
> 会話・チャネルが空になる（config の env で明示すること）。

---

## 🚀 Grok-MCP（xAI Grok / 開発者API）
**AI エージェント機能（Web/X 検索、コード実行、画像生成など）**

> **仕組み:** Claude が Grok API にアクセスして Grok モデルを利用。ユーザーは Claude Desktop 経由で Grok の機能を使える（Claude が仲介）

### チャット
- `chat` - **Grok AI モデルでチャット**（Claude が仲介して Grok API を呼び出し）
- `chat_with_vision` - **画像分析付きチャット**（Grok のビジョン機能を利用）
- `chat_with_files` - **ドキュメント対話**（Grok がアップロードしたファイルを分析）

### 検索
- `web_search` - Web 検索（複数ソース、ドメインフィルタ対応）
- `x_search` - X (Twitter) 検索（ハンドル・日付フィルタ対応）

### コード実行
- `code_executor` - Python コード実行（サンドボックス）
- `grok_agent` - 統合エージェント（ファイル・画像・検索・コード混在）

### 画像・動画生成
- `generate_image` - 画像生成・編集（Grok Imagine）
- `generate_video` - 動画生成・編集
- `extend_video` - 動画拡張

### ファイル操作
- `upload_file` - ファイルアップロード
- `list_files` - アップロード済みファイル一覧
- `get_file` - ファイルメタデータ取得
- `get_file_content` - ファイル内容ダウンロード
- `delete_file` - ファイル削除

### その他
- `list_models` - 利用可能な Grok モデル一覧
- `list_chat_sessions` - ローカルチャット履歴一覧
- `get_chat_history` - セッション履歴取得
- `clear_chat_history` - 履歴削除

**認証:** xAI 開発者API（`XAI_API_KEY`）。**従量課金**（SuperGrok サブスクとは課金が別建て）。
キーが古い / 未課金だと `API key is currently blocked` になる。

---

## 🔮 Grok-OAuth MCP（Hermes ワンショット経由）
**Claude → OAuth-Grok ブリッジ（追加課金なし）**

> **仕組み:** Claude がカスタム MCP サーバー `grok_oauth_bridge.py` を呼び、内部で
> `hermes -z`（ワンショット）を実行。Grok は SuperGrok の **OAuth セッション**で応答するため、
> 開発者API キーを使わず**サブスク範囲内・追加課金なし**で動く。Discord も非同期待ちも経由しない。

### ツール
- `ask_grok` - **Grok に質問・壁打ち・Web/X 検索・画像理解をさせる**
  - toolsets = `x_search,web,vision`。**ファイル書込なし**（安全寄り）
  - 例: `ask_grok("最近の金先物のセンチメントを X で調べて要約して")`
- `grok_work` - **指定リポ内でファイル整理・コード作業・画像生成をさせる**
  - toolsets = `file,code_execution,image_gen,x_search,web,vision`
  - 引数 `workdir` は **`C:\Python\REX_AI` 配下のみ許可**
  - **`REX_Brain_Vault`（聖域）への書込は拒否**。許可ルート外（System32 等）も拒否
  - 例: `grok_work("このフォルダの .md を一覧化して index.md を作って", "C:\\Python\\REX_AI\\Daily_Log")`

### ガードレール
- `terminal` / `computer-use` はどちらのツールにも**含めない**（無確認シェル実行を既定で遮断）
- `-z` は approval 自動バイパスのため、安全は `-t`（toolsets 限定）と workdir 制限で担保
- headless 堅牢化: `HERMES_HOME` 注入 / `--accept-hooks` / `stdin=DEVNULL` / `timeout=120`

### ⚠️ x_search 有効化の 3 点セット（2026-05-23 確定）
X 検索を動かすには以下 3 つが必要。欠けると `vision` だけになり検索結果が空になる。
1. `hermes tools` → CLI で 🐦 X (Twitter) Search を ON
2. `hermes tools` → `4. Reconfigure...` → 🐦 X Search → **`1. xAI Grok OAuth (SuperGrok)`** を選択（`no configuration needed!` = 既存 OAuth 流用で正常）
3. bridge の `-t` に `x_search` を明示（上記 toolsets 参照）

**注意:** `x_search` は tool 名だが `-t` に直接渡せる。一方 `web_search` は tool 名なので `-t` に書くと弾かれる→Web 検索は toolset 名 `web` を使う。また `web` は別プロバイダキー（EXA/PARALLEL/FIRECRAWL/TAVILY）が未設定だと動かない（X 検索とは別系統）。

**bridge 修正後の再起動:** ウィンドウ再起動だけでは MCP サブプロセスが旧コードを掴んだまま残る。**タスクマネージャから完全終了 → 再起動**すること。

**認証:** SuperGrok サブスクの **OAuth**（追加課金なし）。
**詳細:** `Hermes_Agent\docs\Grok_OAuth_Bridge_Architecture.md`（設計） /
`Rex_Grok_Toolbox.md`（運用）

> **Grok-MCP との使い分け:** OAuth・追加課金なしで済むなら **Grok-OAuth**。
> 同期・低レイテンシで開発者API の機能が要るなら **Grok-MCP**（要・有効キー＋課金）。

---

## 🐙 GitHub MCP
**GitHub リポジトリ・Issue・PR 操作**

> **仕組み:** Claude が GitHub API にアクセス。ユーザーはClaude Desktop からリポジトリ操作・Issue管理が可能

- `search_repositories` - **リポジトリ検索**（キーワードで GitHub リポを検索）
- `search_issues` - **Issue 検索**（複数リポから Issue/PR を検索）
- `list_issues` - **リポジトリの Issue 一覧**（特定リポの Issue をフィルタ付きでリスト）
- `create_issue` - **Issue 作成**（新しい Issue を GitHub に投稿）
- `create_pull_request` - **PR 作成**（ブランチから PR を作成）
- `update_issue` - **Issue 更新**（タイトル・説明・ラベルなどを更新）
- `add_issue_comment` - **Issue へコメント追加**（Issue に返信コメント）
- `get_file_contents` - **ファイル内容取得**（リポ内のファイルを読み込み）
- `create_or_update_file` - **ファイル作成・更新**（リポ内のファイルを逐次編集・作成。日本語コンテンツは push_files より安定）
- `push_files` - **複数ファイル一括 push**（1コミットで複数ファイル。日本語含むと不安定なことがある→create_or_update_file 逐次推奨）

**認証:** GitHub PAT（Personal Access Token）

---

## 📚 NotebookLM MCP
**NotebookLM クエリ・知識ベース操作**

> **仕組み:** Claude が NotebookLM にアクセス。REX_Personal_Brain 等のノートブックに対してクエリ・ソース追加・Webリサーチを実行

### クエリ（既存ソースに質問）
- `notebook_query` - **ノートブックへクエリ**（既存ソースに質問を投げて回答取得。要 `notebook_id`）
- `notebook_query_start` / `notebook_query_status` - **非同期クエリ**（ソース50+の大型ノートブック用。startで query_id 取得→status でポーリング）
- `cross_notebook_query` - **複数ノートブック横断クエリ**（名前/タグ/全件で選択し集約回答）

### ソース管理
- `source_add` - **ソース追加**（`source_type` = url/text/drive/file。旧 `upload_document` の役割。ローカルファイルは file 必須）
- `source_get_content` - **ソース生テキスト取得**（AI処理なしの原文。エクスポートに高速）
- `source_describe` - **ソース要約**（キーワード付きの AI 要約）
- `source_list_drive` / `source_sync_drive` - **Driveソースの一覧・鮮度同期**
- `source_rename` - **ソース名変更**

### リサーチ（新規ソースを探す）
- `research_start` / `research_status` / `research_import` - **Web/Drive を検索して新規ソースを発見→取り込み**（start→statusポーリング→import のワークフロー）

### その他
- `tag` - **タグ管理**（add/remove/list/select。タグマッチで関連ノートブックを選択）
- `batch` - **バッチ操作**（複数ノートブックへの query/add_source/create/studio 等）

> **注:** 上記は代表的なもの。notebook_create / notebook_list / notebook_get / studio_* / export_artifact 等多数のツールがある。
> NLMへのアップロードは `source_type: file` 必須（テキストモード禁止）、アップロード前にローカルで git pull が必要（運用規約）。

**対象例:** REX_Personal_Brain (ID: `daf281ae-e310-400f-961a-20db58b98e01`) / REX_Wiki_Vault (ID: `5d09e468-3a96-4906-af27-3400c50a0275`)

---

## 💡 よくある使用例

### Hermes + Grok の連携
```
"Slack の最新メッセージを読み込んで、Web 検索で関連情報を集めて、要約を画像化して Slack に送信"

↓ 実行フロー

@hermes messages_read (Slack メッセージ取得)
  ↓
@grok web_search (記事検索)
@grok code_executor (要約スクリプト実行)
→ @grok generate_image (画像化)
  ↓
@hermes messages_send (Slack へ送信)
```

### Grok-OAuth 単独（OAuth・追加課金なし）
```
"X で最新の金先物センチメントを調べて要約して"

↓ 実行フロー

@grok-oauth ask_grok (OAuth-Grok が X 検索 + 分析、同期で返す)
```

### Grok-OAuth でリポ作業（聖域は保護）
```
"Daily_Log の .md を一覧化して index を作って"

↓ 実行フロー

@grok-oauth grok_work (workdir=Daily_Log。Vault 指定は自動拒否)
```

### Grok 単独
```
"Python で Fibonacci 数列を計算するコードを書いて実行"

↓ 実行フロー

@grok code_executor (自動的に実行)
```

### GitHub + Grok
```
"GitHub の issue を検索して、内容を分析してコード例を生成"

↓ 実行フロー

@github search_issues (issue 検索)
  ↓
@grok grok_agent (分析・コード生成)
```

### NotebookLM + Grok
```
"REX_Wiki_Vault から AI 関連情報を取得して、最新情報を Web 検索で補完"

↓ 実行フロー

@notebooklm-mcp notebook_query (知識ベースクエリ)
  ↓
@grok web_search (最新情報検索)
```

---

## 🎯 使用時のコツ

### 1. **自動判断を活用**
```
指定なし：「Slack に送信して」
→ Claude が @hermes messages_send を自動選択
```

### 2. **明示的に指定する場合**
```
明示指定：「@grok で Python コード書いて」
→ Grok のみを明確に指定
```

### 3. **複合操作はリクエスト内で指示**
```
「X で最新の Grok ニュース検索して、要約を Slack に送信」
→ Claude が自動的に @grok x_search → @hermes messages_send を実行
```

### 4. **Grok は 2 経路あるので使い分け**
```
追加課金を避けたい / OAuth で十分 → @grok-oauth ask_grok
開発者API の機能・低レイテンシが要る → @grok（要・有効キー＋課金）
```

---

## 🔄 MCP 設定ファイル

- **Claude Desktop:** `C:\Users\Setona\AppData\Roaming\Claude\claude_desktop_config.json`
- **グローバル設定:** `C:\Users\Setona\.claude\CLAUDE.md`
- **Grok-MCP:** `C:\Python\REX_AI\MCP_Servers\Grok-MCP`
- **Grok-OAuth:** `C:\Python\REX_AI\MCP_Servers\Grok-OAuth`（`grok_oauth_bridge.py`）
- **Hermes:** `C:\Users\Setona\AppData\Local\hermes`
- **MCP サーバー置き場の規約:** `C:\Python\REX_AI\MCP_Servers\README.md`

---

## 📝 更新履歴

- **2026-05-23** - **Plan C 完成**。`ask_grok` から OAuth で X 検索が同期で通ることを実機確認。Grok-OAuth の toolsets を `x_search,web,vision`（grok_work は +file/code_execution/image_gen）に修正。x_search 有効化 3 点セットと MCP 完全終了再起動の注記を追加
- **2026-05-22** - Grok-OAuth MCP（Hermes ワンショット経由・OAuth）を追記。Hermes/Grok-MCP の注記補足
- **2026-05-21** - Grok-MCP、Hermes-MCP を claude_desktop_config.json に統合
- **2026-05-21** - MCP コマンドリスト作成
