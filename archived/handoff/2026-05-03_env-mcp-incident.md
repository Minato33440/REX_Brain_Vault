# 環境変数 & MCP設定 不具合まとめ
**日付**: 2026-05-03  
**対応者**: Claude Code (Wiki-Rex セッション)  
**トリガー**: GitGuardian アラート — X AI API Key 露出検知

---

## 1. 発端：GitGuardian アラート

`Minato33440/REX_Brain_Vault` リポジトリに `.env` ファイルが commit されており、
以下の機密情報が GitHub 上に公開状態になっていた（push 日: 2026-04-18）。

| 種別 | 状態 |
|---|---|
| X AI API Key | 露出 → 無効化 |
| Polygon API Key | 露出 → 無効化 |
| GitHub PAT（2本） | 露出 → 無効化・再発行 |
| Obsidian アカウント情報（メール/PW） | 露出 → PW変更要 |

---

## 2. 不具合①：`.env` が `.gitignore` に未登録

### 問題
`.gitignore` に `.env` の記載がなく、機密ファイルがそのまま Git 管理対象になっていた。→
これに対しては、Git上の.env履歴全削除→.gitignoreに.env追記→windows環境変数に新規GitHub PAT設置にて対処済み

### 修正内容
[.gitignore](../../.gitignore) に以下を追記:

```
# Secrets (never commit)
.env
.env.local
.env.*
```

---

## 3. 不具合②：Git 履歴に機密情報が残存

### 問題
`.env` を `.gitignore` に追加・削除 commit をしても、過去の commit 履歴にキーが残る。

### 修正手順
```bash
# 1. git トラッキングから除去
git rm --cached .env

# 2. .gitignore 更新を commit
git commit -m "security: remove .env from tracking, add to .gitignore"

# 3. 全履歴から .env を完全除去（要: pip install git-filter-repo）
git filter-repo --path .env --invert-paths --force

# 4. origin を再登録（filter-repo が自動削除するため）
git remote add origin https://github.com/Minato33440/REX_Brain_Vault.git

# 5. 強制 push
git push origin main --force
```

> **注意**: `git filter-repo` 実行後は origin が自動削除される。再追加が必要。  
> iPhone の Git アプリなど他端末 clone は再 clone が必要になる。

---

## 4. 不具合③：`claude_desktop_config.json` の JSON 構文エラー

### 問題
`github` MCP サーバーに `env` ブロックを手動追記した際、閉じ括弧を誤記。

```json
// 誤（36行目）
"env": {
  "GITHUB_TOKEN": "%GITHUB_PAT%"
]   ← ] になっていた（正しくは }）
```

### 原因
- `]`（配列の閉じ）と `}`（オブジェクトの閉じ）の誤入力。

---

## 5. 不具合④：`env` ブロック内で Windows 環境変数参照が使えない

### 問題
```json
"GITHUB_TOKEN": "%GITHUB_PAT%"
```
JSON 内の `%VAR%` 記法は Windows シェル構文であり、
MCP サーバープロセスは shell 経由で起動しないため展開されない（文字列のまま渡る）。

### 正しい対処
`claude_desktop_config.json` の `env` ブロックは**不要**。  
Windows ユーザー環境変数に `GITHUB_TOKEN` を登録すれば、
Claude Desktop 起動時に子プロセス（MCP サーバー）へ自動継承される。

**最終的な正しい `github` MCP 設定**:
```json
"github": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"]
}
```

---

## 6. 不具合⑤：環境変数名の不一致

### 問題
`@modelcontextprotocol/server-github` が参照する変数名は **`GITHUB_TOKEN`** だが、
Windows 環境変数に `GITHUB_PAT` という名前で登録していた。

### 修正
Windows ユーザー環境変数を `GITHUB_PAT` → **`GITHUB_TOKEN`** に変更。

---

## 7. 最終確認

| 確認項目 | 結果 |
|---|---|
| `.env` が Git 履歴から完全除去 | ✅ |
| `.gitignore` に `.env` 追加 | ✅ |
| `GITHUB_TOKEN` を Windows ユーザー環境変数に登録 | ✅ |
| `claude_desktop_config.json` の JSON 構文修正 | ✅ |
| Claude Desktop 再起動 → GitHub MCP `running` | ✅ |
| Claude Desktop で GitHub 接続確認 | ✅ |

---

## 8. 再発防止チェックリスト

- [ ] 新規リポジトリ作成時に `.gitignore` テンプレートで `.env` を必ず含める
- [ ] API キー・PAT は `.env` ではなく Windows ユーザー環境変数で管理
- [ ] `claude_desktop_config.json` 編集後は JSON バリデーターで確認
- [ ] PAT の有効期限（2026-08-01）を calendar に登録して更新漏れ防止
