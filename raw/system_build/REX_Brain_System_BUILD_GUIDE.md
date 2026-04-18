# REX_Brain_System 構築手順書

**作成日**: 2026-04-15  
**作成者**: REX（システムエンジニア）  
**対象環境**: Claude Desktop × Windows  
**目的**: スレ引き継ぎコスト・ロジック漏れ・コンテキスト消費過多の根本解決

> ⚠️ このファイルは人間側がチェックする資料。ローカル管理上の注意点を随時追記する。

---

## 概要

本システムは3つのMCPを組み合わせた自己増殖型ナレッジ環境。

```
REX_Brain_System
├── NotebookLM MCP   → クラウドRAG・引き継ぎプロンプト自動生成
├── filesystem MCP   → ローカルVault読み書き（Obsidian代替）
└── GitHub MCP       → このチャットから直接プッシュ
```

**解決した課題:**

| 課題 | 解決策 |
|---|---|
| スレ引き継ぎの手動作業（vol9まで蓄積） | NotebookLMが引き継ぎプロンプトを自動生成 |
| ロジック漏れ（設計意図の消失） | RAGで設計確定MDを永続保持・検索可能に |
| 新スレ冒頭のコンテキスト消費 | Vault の index.md + handoff/latest.md で即座に文脈復元 |
| GitプッシュにPowerShell必須 | GitHub MCPでチャットから直接プッシュ |

---

## PHASE 1 — NotebookLM MCP セットアップ

### 1-1. uv インストール

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
# ターミナル再起動後に確認
uv --version
```

### 1-2. notebooklm-mcp-cli インストール

```powershell
# fakeredis バージョン固定が必須（2.26.0以降でFakeConnection削除）
uv tool install notebooklm-mcp-cli --force --with "fakeredis==2.20.0"
```

> ⚠️ `uv tool upgrade notebooklm-mcp-cli` は **使わない**。fakeredis 固定が解除される。  
> ⚠️ アップデート時は必ず `--force --with "fakeredis==2.20.0"` を付ける。

### 1-3. Google認証

```powershell
nlm config set auth.browser chrome
nlm login
# ヘッドレスブラウザが起動 → Googleアカウントでログイン
```
これは安全（認証のみ）
nlm login
これは危険（fakeredis固定が解除される可能性）
uv tool upgrade notebooklm-mcp-cliアップデートしたい場合は必ず：
powershelluv tool install notebooklm-mcp-cli --force --with "fakeredis==2.20.0"

認証情報はローカルのみに保存される（外部送信なし）。

### 1-4. claude_desktop_config.json に登録

ファイルパス: `C:\Users\{ユーザー名}\AppData\Roaming\Claude\claude_desktop_config.json`

```json
"notebooklm-mcp": {
  "command": "C:\\Users\\{ユーザー名}\\.local\\bin\\uvx.exe",
  "args": [
    "--from",
    "notebooklm-mcp-cli",
    "notebooklm-mcp"
  ]
}
```

> ⚠️ `command` は **フルパス必須**。`uvx` のみでは Claude Desktop の PATH 解決に失敗する。

### 1-5. トラブルシューティング

| 症状 | 原因 | 解決策 |
|---|---|---|
| ハンマーアイコンが出ない | MCPサーバーが起動していない | `command` をフルパスに変更 |
| Server disconnected | fakeredis バージョン不整合 | `fakeredis==2.20.0` に固定 |
| アンチウィルスが反応 | 誤検知 | 対象ソフトをアンインストール → PC再起動 |
| Authentication expired | Cookie期限切れ（2〜4週間） | `nlm login` で再認証 |
| 設定変更後MCPが反映されない | キャッシュ残存 | **PCごと再起動**が確実 |

### 1-6. 動作確認（RAGクエリ3本）

NotebookLMでノートブックを作成し、設計確定MDをソースとして投入後に以下のクエリで精度確認：

```
① 「現在の最優先タスクは何か？」
   → 複数プロジェクト横断で正確に整理できるか

② 「#025の固定ネック原則とは何か？設計意図を説明して」
   → 具体的な数値・コードレベルの設計意図を保持できるか

③ 「新しいClaudeCodeセッションの引き継ぎプロンプトを生成して」
   → 実装可能レベルの引き継ぎ文を自動生成できるか
```

**クエリ③が最重要**。これが自動化できれば手動引き継ぎ作業がゼロになる。

---

## PHASE 2 — filesystem MCP 拡張（Vault アクセス）

### 2-1. アクセスディレクトリの追加

`claude_desktop_config.json` の filesystem エントリを修正：

```json
"filesystem": {
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-filesystem",
    "C:\\Users\\{ユーザー名}\\Desktop",
    "C:\\Users\\{ユーザー名}\\Downloads",
    "C:\\Python\\REX_AI"   ← 追加
  ]
}
```

> ⚠️ 設定変更後は **PCごと再起動** が確実（Claude Desktop再起動だけでは反映されない場合あり）。

> ⚠️ Obsidian専用MCPパッケージ（`mcp-obsidian`）は **存在しない**。
> Vault は markdown ファイル群なので filesystem MCP で完全に代替可能。

### 2-2. REX_Brain_Vault 構造

```
C:\Python\REX_AI\REX_Brain_Vault\
├── CLAUDE.md              ← LLMへの運用指示書（セッション開始時に必読）
├── raw/                   ← 元資料（イミュータブル・LLMは読むだけ）
│   ├── EX_DESIGN_CONFIRMED-*.md
│   ├── HP-DESIGN-CONFIRMED_*.md
│   └── スレ引き継ぎ指示書_vol*.md   ← 過去の手動作業も資産化
└── wiki/                  ← LLMが書き・育てる自己増殖層
    ├── index.md           ← 全ページ目次（必ずここから参照）
    ├── log.md             ← 時系列作業ログ（追記専用）
    ├── entities/          ← ファイル・関数・パラメータのページ
    ├── decisions/         ← 意思決定ログ（なぜこの設計か）
    └── handoff/
        └── latest.md      ← 次スレ用引き継ぎプロンプト（毎回上書き）
```

### 2-3. Vault 運用の3原則

1. `raw/` は **絶対に編集しない**（読み取り専用）
2. `wiki/log.md` は **追記のみ**（過去ログは削除しない）
3. `wiki/handoff/latest.md` は **毎セッション上書き更新**

### 2-4. セッション開始・終了のルール

**開始時:**
```
1. wiki/index.md を読む
2. wiki/log.md の末尾5件で前回作業を確認
3. wiki/handoff/latest.md を ClaudeCode に貼り付けて実装開始
```

**終了時（/wrap-up）:**
```
1. 今日の決定事項を wiki/log.md に追記
2. wiki/handoff/latest.md を更新（次スレ用）
3. NotebookLM の REX_Trade_Brain に note として記録
4. GitHub MCP で直接プッシュ
```

### 2-5. Vault を Obsidian で開く

```
Obsidian → 左下「Vault切り替え」アイコン
→ Open folder as vault
→ C:\Python\REX_AI\REX_Brain_Vault を選択
```

既存の Obsidian 個人 Vault（グローバル Notes）とは**分離**して管理する。

---

## PHASE 3 — GitHub MCP セットアップ

### 3-1. claude_desktop_config.json に追記

```json
"github": {
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-github"
  ],
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "（PATを記入）"
  }
}
```

### 3-2. Fine-grained PAT の発行

```
GitHub → Settings → Developer settings
→ Personal access tokens → Fine-grained tokens
→ Generate new token

Token name: Claude-MCP
Expiration: 90日（推奨）
  理由: セキュリティと管理負荷のバランス
  ※ GitHub から7日前にメール通知あり

Repository access: Only select repositories
  ✅ 対象リポジトリを選択

Repository permissions:
  ✅ Contents   → Read and write
  ✅ Metadata   → Read-only（自動付与）
```

### 3-3. セキュリティ注意事項

> ⚠️ **PATは絶対にチャットに貼らない・スクリーンショットも送らない**  
> チャット履歴にトークンが残ると漏洩リスクになる。  
> 誤って共有した場合は即座に GitHub で **Revoke → 再発行** すること。

### 3-4. トラブルシューティング

| 症状 | 原因 | 解決策 |
|---|---|---|
| Tool execution failed | リポジトリが未選択 | PAT設定でリポジトリを選択 |
| Tool execution failed | Contents権限が未設定 | Add permissions → Contents: Read and write |
| Tool execution failed | PATが無効化済み | 新しいPATを発行してconfigを書き換え |
| チャットにトークン漏洩 | 誤ってスクリーンショット共有 | 即座にRevoke → 再発行 |

---

## 完成後の構成（確定版）

```json
{
  "mcpServers": {
    "filesystem": { "paths": ["Desktop", "Downloads", "C:\\Python\\REX_AI"] },
    "notebooklm-mcp": { "command": "フルパス指定・fakeredis==2.20.0固定" },
    "github": { "PAT": "Fine-grained / 90日 / Contents:RW" }
  }
}
```

---

## ワークフロー全体像（完成後）

```
新スレ開始
  ↓
Vault の CLAUDE.md + index.md + log.md を読む（3ファイル・30秒）
  ↓
handoff/latest.md を ClaudeCode に貼り付け → 即実装開始
  ↓
実装・バックテスト（ClaudeCode）
  ↓
「引き継ぎプロンプトを生成して」
→ NotebookLM RAG が自動生成
  ↓
/wrap-up
→ wiki/log.md に追記
→ handoff/latest.md を更新
→ NotebookLM に note 保存
→ GitHub MCP で直接プッシュ
```

---

## ローカル管理チェックリスト

### 定期メンテナンス

| 頻度 | 作業 | 手順 |
|---|---|---|
| 2〜4週間ごと | NotebookLM 再認証 | `nlm login`（PCは再起動不要）|
| 90日ごと | GitHub PAT 更新 | GitHub でトークン再発行 → config 書き換え → Claude Desktop 再起動 |
| 指示書#完了時 | NotebookLM ソース更新 | 古いソースを削除 → 新しいMDを再投入 |
| 指示書#完了時 | Vault raw/ を更新 | 最新のEX_DESIGNをraw/に配置 |

### 作業開始前の鉄則

```powershell
# ローカルで編集する前に必ず実行
git pull origin main
```

**理由**: ローカル（PowerShell）とクラウド（GitHub MCP）の両方からプッシュが発生するため、
pull なしで編集すると diverge（分岐）が起きる。

### NotebookLM アップデート通知が出たとき

```
🔔 Update available: 0.5.x → 0.5.y
```

**`uv tool upgrade` は使わない。** 代わりに：

```powershell
uv tool install notebooklm-mcp-cli --force --with "fakeredis==2.20.0"
```

`nlm login` はパッケージを更新しない（認証のみ・通知が出るだけで安全）。

### PAT 有効期限管理

```
Claude-MCP トークン
  発行日: 2026-04-15
  有効期限: 2026-07-14（90日）
  通知: 期限7日前にGitHubからメール
  更新時: 新PAT発行 → config書き換え → Claude Desktop再起動
```

### config ファイルの編集手順

```powershell
# メモ帳で直接開く
notepad "$env:APPDATA\Claude\claude_desktop_config.json"

# 編集後は Claude Desktop を再起動
# 設定が反映されない場合は PCごと再起動
```

---

## 注意点まとめ

| カテゴリ | 注意点 |
|---|---|
| **NotebookLM** | fakeredis==2.20.0 固定（アップグレード不可） |
| **NotebookLM** | uvx はフルパス指定（`C:\Users\{名前}\.local\bin\uvx.exe`） |
| **NotebookLM** | Cookie有効期限2〜4週間 → `nlm login` で再認証（PCは不要）|
| **NotebookLM** | `nlm login` はパッケージ更新なし・認証のみ・通知は無視でOK |
| **NotebookLM** | 非公式API依存 → 突然停止リスクあり（コア作業に依存させない） |
| **filesystem** | Obsidian専用MCPは存在しない → filesystem MCPで代替 |
| **filesystem** | 設定変更後はPCごと再起動が確実 |
| **filesystem** | Vault の `raw/` は絶対に編集しない |
| **GitHub** | Fine-grained PATを推奨（Classic tokenより安全） |
| **GitHub** | PATはチャットに絶対に貼らない・スクリーンショットも送らない |
| **GitHub** | PAT有効期限90日 → 7日前にGitHubからメール通知あり |
| **GitHub** | ローカル作業前は必ず `git pull origin main` |
| **Vault** | 既存のObsidian個人VaultとREX_Brain_Vaultは分離して管理 |
| **Vault** | wiki/log.md は追記のみ・削除禁止 |

---

## 関連ファイル

| ファイル | 場所 | 内容 |
|---|---|---|
| `CLAUDE.md` | REX_Brain_Vault/ | Vault運用指示書 |
| `wiki/index.md` | REX_Brain_Vault/wiki/ | 全ページ目次 |
| `wiki/handoff/latest.md` | REX_Brain_Vault/wiki/handoff/ | 最新引き継ぎプロンプト |
| `eval_report.md` | tests/#001_NotebookLM/ | NotebookLM MCP評価レポート |
| `MCP-DESIGN-CONFIRMED.md` | docs/ | MCP試験運用進捗記録 |

---

*記録: REX（システムエンジニア）*  
*最終更新: 2026-04-15*
