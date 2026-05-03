# GitHub MCP 書込テスト & 解決記録

**書込テスト**: ✅ 成功（2026-05-03）
**実施者**: ClaudeCode (claude-sonnet-4-6)

---

## 解決記録（2026-05-03）

**効いた対処**: Step B — `claude_desktop_config.json` に `env` ブロックを明示追加

**経緯**:
1. Step A（PAT 直接テスト）: `GET /user` → 200 OK / `login: Minato33440` 確認 → PAT は有効
2. PAT 有効なのに書込 401 が継続していた原因 = Claude Desktop が npx 子プロセスに OS 環境変数を継承していなかった
3. `claude_desktop_config.json` の github エントリに `env` ブロックを追加し PAT を直書き → Claude Desktop 完全終了再起動 → running 確認 → 書込成功

**最終構成**:
- `claude_desktop_config.json`: github エントリに `env.GITHUB_PERSONAL_ACCESS_TOKEN` を直書き
- 環境変数: `GITHUB_PERSONAL_ACCESS_TOKEN` + `GITHUB_TOKEN` 両方 User スコープに登録済み（並存は問題なし）
- MCP server: `@modelcontextprotocol/server-github`（npm 版）

---

## 修正ポイントと注意事項（将来の Vault-Planner / Wiki-Eval 向け）

### 根本原因

Windows + Claude Desktop の組み合わせでは、**OS のユーザー環境変数は npx 子プロセスに自動継承されない**。

`env-mcp-incident.md §4-5` で「env ブロックは不要・OS 環境変数から自動継承」と判断されていたが、これは誤り。`claude_desktop_config.json` の `env` ブロック明示が必須。

### 修正箇所

`%APPDATA%\Claude\claude_desktop_config.json` の github エントリ:

```json
"github": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "<PAT値を直書き>"
  }
}
```

**重要**: `${VAR}` や `%VAR%` の変数展開構文は Claude Desktop では機能しない。必ず値を直接文字列として記載する。

### セキュリティ注意

- `claude_desktop_config.json` は `%APPDATA%\Claude\` 配下のローカルファイルで Git 管理対象外
- ただし PC のバックアップ・同期ツール（OneDrive 等）に含まれる可能性があるため、バックアップ除外設定を確認すること
- PAT の期限切れ・再発行時はこのファイルの値も更新し、Claude Desktop を完全終了再起動すること

### 変数名について

| 変数名 | 状態 | 備考 |
|---|---|---|
| `GITHUB_PERSONAL_ACCESS_TOKEN` | ✅ 公式参照名 | `@modelcontextprotocol/server-github` が参照する名前 |
| `GITHUB_TOKEN` | 並存登録済み | `env-mcp-incident.md §6` の誤修正の残滓。害はないが不要 |

### PAT 検証コマンド（トラブル時の Step A）

PowerShell から:
```powershell
$pat = [Environment]::GetEnvironmentVariable("GITHUB_PERSONAL_ACCESS_TOKEN", "User")
Invoke-WebRequest -Uri "https://api.github.com/user" -Headers @{Authorization = "Bearer $pat"; "User-Agent" = "Test"} -UseBasicParsing | Select-Object StatusCode
```
→ `200` が返れば PAT 有効。それ以外なら PAT 再発行を検討。

---

*記録: ClaudeCode (claude-sonnet-4-6) / 2026-05-03*
*本ファイルは書込テスト兼解決記録として保持。削除不要。*
