---
title: Claude Code コマンド一覧リファレンス
created: 2026-06-14
tags: [reference, claude-code, cli, slash-commands]
---

# Claude Code コマンド一覧リファレンス

Claude Code（Anthropic 公式 CLI）で使えるコマンドの早見表。
セッション内で打つ **スラッシュコマンド**、ターミナルで打つ **CLI コマンド/フラグ**、
**キーボードショートカット** の 3 種に分けて整理。

最終更新: 2026-06-14

---

## 1. スラッシュコマンド（セッション内で `/` で実行）

対話中に入力する組み込みコマンド。よく使うものから順に。

### よく使う

| コマンド | 説明 |
|---|---|
| `/help` | 使い方・コマンド一覧のヘルプ表示 |
| `/clear` | 会話履歴を全消去（コンテキストをリセット） |
| `/compact [指示]` | 会話を要約して圧縮。`[指示]` で残す論点を指定可 |
| `/context` | 現在のコンテキスト使用量を可視化 |
| `/model` | 使用する AI モデルを選択・変更 |
| `/config` | 設定画面を開く（テーマ・モデル等） |
| `/resume` | 過去の会話を選んで再開 |
| `/review` | コードレビューを依頼 |
| `/init` | プロジェクトを解析し `CLAUDE.md` を生成 |

### コンテキスト・履歴管理

| コマンド | 説明 |
|---|---|
| `/rewind` | 会話／コード変更を巻き戻す |
| `/export` | 会話をエクスポート（ファイル・クリップボード） |
| `/cost` | トークン使用量・コスト統計を表示 |
| `/usage` | プランの使用上限・残量を表示 |
| `/add-dir` | 作業ディレクトリを追加 |

### 設定・管理

| コマンド | 説明 |
|---|---|
| `/memory` | `CLAUDE.md` メモリファイルを編集 |
| `/permissions` | ツール許可（allow/deny）ルールを管理 |
| `/hooks` | フック設定を管理（自動実行の登録） |
| `/agents` | カスタムサブエージェントを管理 |
| `/mcp` | MCP サーバ接続を管理 |
| `/output-style` | 出力スタイルを設定 |
| `/statusline` | ステータスライン（下部表示）を設定 |
| `/fast` | Fast モード切替（Opus を高速出力。下位モデルには落ちない） |
| `/vim` | Vim モードに入る |

### システム・アカウント

| コマンド | 説明 |
|---|---|
| `/status` | システム状態を表示 |
| `/doctor` | インストールの健全性チェック |
| `/ide` | IDE 連携を管理 |
| `/login` | Anthropic アカウント切替・ログイン |
| `/logout` | サインアウト |
| `/privacy-settings` | プライバシー設定を表示 |
| `/release-notes` | リリースノートを表示 |
| `/bug` / `/feedback` | バグ報告・フィードバック送信 |
| `/install-github-app` | GitHub Actions 連携をセットアップ |
| `/pr-comments` | GitHub PR のコメントを取得 |
| `/terminal-setup` | 改行キーバインドをインストール |
| `/exit` | REPL を終了 |

> 補足: `/code-review`, `/security-review`, `/loop`, `/schedule` などはスキル／拡張コマンド。
> このリポジトリ独自では `/code-review ultra`（クラウド多エージェントレビュー）も利用可。

---

## 2. CLI コマンド（ターミナルで `claude ...`）

| コマンド | 説明 |
|---|---|
| `claude` | 対話セッションを開始 |
| `claude "質問"` | 初期プロンプト付きで対話開始 |
| `claude -p "質問"` | **print モード**（非対話・1 回応答して終了。スクリプト向き） |
| `claude -c` / `claude --continue` | 直近の会話を継続 |
| `claude -r` / `claude --resume` | 会話を選んで再開 |
| `claude commit` | コミットメッセージを生成してコミット |
| `claude update` | 最新版へ更新 |
| `claude mcp` | MCP サーバを設定・管理 |
| `claude config` | 設定の表示・変更 |
| `claude doctor` | インストール診断 |

### 主なフラグ

| フラグ | 説明 |
|---|---|
| `--model <name>` | モデル指定（例: `claude-opus-4-8`） |
| `-p, --print` | 非対話の print モード |
| `--output-format <fmt>` | 出力形式（`text` / `json` / `stream-json`） |
| `--input-format <fmt>` | 入力形式 |
| `--add-dir <path>` | 追加の作業ディレクトリ |
| `--allowedTools <list>` | 許可ツールを指定 |
| `--disallowedTools <list>` | 禁止ツールを指定 |
| `--permission-mode <mode>` | 許可モード（`plan` / `acceptEdits` 等） |
| `--dangerously-skip-permissions` | 許可確認をスキップ（自己責任） |
| `--max-turns <n>` | 自動ターン数の上限 |
| `--verbose` | 詳細ログ出力 |
| `--session-id <id>` | セッション ID 指定 |

---

## 3. キーボードショートカット（対話中）

| キー | 動作 |
|---|---|
| `Esc` | 生成・処理を中断 |
| `Esc` ×2 | 直前のメッセージ／ターンへ戻る（履歴編集） |
| `Ctrl+C` | 入力クリア／終了 |
| `Ctrl+D` | セッション終了 |
| `Ctrl+L` | 画面クリア |
| `Ctrl+R` | 履歴の逆方向検索 |
| `Shift+Tab` | 許可モード切替（plan ⇄ 通常 ⇄ acceptEdits） |
| `↑` / `↓` | 入力履歴をたどる |
| `#` 始まり | その行をメモリ（CLAUDE.md）に追記する候補に |
| `!` 始まり | bash モード（コマンドを直接実行） |
| `@` | ファイル参照の補完 |
| `/` | スラッシュコマンドの補完 |

> 改行は環境により `Shift+Enter` または `Option+Enter`。
> 効かない場合は `/terminal-setup` でキーバインドを入れる。

---

## モデル ID 早見（2026 時点）

| モデル | ID |
|---|---|
| Fable 5 | `claude-fable-5` |
| Opus 4.8 | `claude-opus-4-8` |
| Sonnet 4.6 | `claude-sonnet-4-6` |
| Haiku 4.5 | `claude-haiku-4-5-20251001` |

---

## 関連メモ

- このリポ独自の RTK（トークン節約コマンド）は別途 `CLAUDE.md` 参照（`rtk git ...` 等）
- MCP コマンドの詳細は [[MCP_Commands_Reference]] を参照
- Hermes / Grok CLI 連携はグローバル `CLAUDE.md` 参照
