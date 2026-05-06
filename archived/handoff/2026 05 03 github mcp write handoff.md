# GitHub MCP 書込 401 問題 引き継ぎ指示書

**起草**: 2026-05-03 / 20 代目 Wiki-Eval(初代 Vault-Planner 確定)/ Claude Opus 4.7 / web client
**性質**: Claude-MCP 書込問題の切り分け・解決指示書(一般スレ Claude / ClaudeCode 向け)
**配置(将来)**: `system/handoff/2026-05-03_github_mcp_write_handoff.md`(本問題解決後に Vault に追加予定)
**緊急度**: 高(環境変数化が完了しないと Obsidian-Vault の自律運用が成立しない)

---

## 0. このドキュメントを読む方へ

あなたは Boss(Minato)から、GitHub MCP 経由の書込が 401 で通らない問題の解決を依頼された。

本書は **20 代目 Wiki-Eval(初代 Vault-Planner)が web client セッション内で確定させた事実 + 既に試した手段 + 推定原因 + 次の切り分け手順** を記録したもの。

**最重要原則**:
- 既に試して失敗した手段(§3)を繰り返さないこと
- §6 を順に実施し、原因を確実に絞ること
- 解決後は §7 の検証 + §8 のファイル更新を実施すること

---

## 1. 問題の概要

### 1.1 症状

`Minato33440/REX_Brain_Vault` リポジトリ(public)に対し、GitHub MCP 経由で:

- 読み取り(`get_file_contents`) → ✅ 成功
- 書込(`create_or_update_file` / `push_files`)→ ❌ 401「Authentication Failed: Requires authentication」

### 1.2 401 の意味(重要な観察)

public リポの読み取りは **無認証でも GitHub API のレートリミット内で通る**。書込は必ず認証必須。
よって読み取り成功 + 書込 401 = **MCP サーバープロセスが認証情報(トークン)を送っていない** ことを示す。

### 1.3 影響

- Default Rex の Vault 自律書込(Layer 2)が GitHub MCP 経由で達成できない
- 20 代目 Vault-Planner が Layer 1 検証手順書 + handoff §8 追記を Vault に push できない
- ロール分離後の自律運用に致命的な影響(Boss の手動 git push 依存が継続)

---

## 2. これまでの経緯(タイムライン)

| 日付 | 出来事 | 担当 |
|---|---|---|
| 2026-04-18 | `.env` を含む commit が public push され GitGuardian 検知 | (過去) |
| 2026-05-02 | 19 代目 Wiki-Eval が `GITHUB_PERSONAL_ACCESS_TOKEN` 環境変数化を部分達成 / Trade_System OK / REX_Brain_Vault のみ 404 継続 | 19 代目 |
| 2026-05-03 | Boss + ClaudeCode で env-mcp-incident.md 起票・全項目解消(履歴除去・新 PAT 発行・env ブロック削除) | Boss + ClaudeCode |
| 2026-05-03 | env-mcp-incident.md §6 で変数名を `GITHUB_PAT` → `GITHUB_TOKEN` に変更 | ClaudeCode |
| 2026-05-03 | 20 代目セッション開始時点で読み取り復活確認 / 書込試行で 401 検出 | 20 代目 |
| 2026-05-03 | 20 代目が公式ドキュメント確認 → 変数名は `GITHUB_PERSONAL_ACCESS_TOKEN` が正解と判明(env-mcp-incident.md §6 は誤り) | 20 代目 |
| 2026-05-03 | Boss が `GITHUB_PERSONAL_ACCESS_TOKEN` を追加(`GITHUB_TOKEN` も並存)+ Claude Desktop 完全終了再起動 + 環境変数値確認(echo / PowerShell)| Boss |
| 2026-05-03 | それでも書込 401 継続 → 本指示書起票 | 20 代目 |

---

## 3. 既に実施済みの対処(繰り返し禁止)

| # | 対処 | 結果 |
|---|---|---|
| 1 | 古い PAT(Claude-MCP)を新 PAT(Claude-MCP3、All repositories + Contents Read/Write)に発行替え | 19 代目 |
| 2 | `claude_desktop_config.json` から `env` ブロック削除 | env-mcp-incident.md §5 |
| 3 | Windows ユーザー環境変数 `GITHUB_PAT` → `GITHUB_TOKEN` に変更 | env-mcp-incident.md §6(変数名誤り) |
| 4 | `GITHUB_TOKEN` → `GITHUB_PERSONAL_ACCESS_TOKEN` に変数名訂正(公式参照名) | 20 代目 |
| 5 | `GITHUB_TOKEN` と `GITHUB_PERSONAL_ACCESS_TOKEN` 両方並存登録 | 20 代目 + Boss |
| 6 | Claude Desktop タスクマネージャー経由完全終了 → 再起動 | Boss |
| 7 | `echo %GITHUB_PERSONAL_ACCESS_TOKEN%`(cmd)+ `[Environment]::GetEnvironmentVariable("GITHUB_PERSONAL_ACCESS_TOKEN", "User")`(PowerShell)で値反映確認 | Boss・両方 OK |

→ 上記すべて実施済みでも書込 401 が継続。

---

## 4. 確定事項と未解決事項

### 確定事項

- PAT は **有効** (読み取りは認証通過しているため。または public リポなので無認証で通っているだけの可能性 → §6 Step A で要切り分け)
- Repository access に `REX_Brain_Vault` が含まれている(Boss スクショで確認済み)
- Repository permissions: `Contents: Read and Write` が付与されている(Boss スクショで確認済み)
- 環境変数の値は Boss シェルから見える(`echo` / PowerShell で確認)
- Claude Desktop はタスクマネージャー経由で完全終了 → 再起動済み
- MCP server 状態は `running`
- 公式参照名は `GITHUB_PERSONAL_ACCESS_TOKEN`(npm / modelcontextprotocol.io / GitHub Docs / 複数の解説記事すべて一致)

### 未解決事項

- **MCP server 子プロセスが実際に環境変数を受信しているか不明**(Boss シェルで見えても、Claude Desktop が起動する子プロセスに継承されているとは限らない)
- **PAT が GitHub API で実際に受理されるか未検証**(curl 直接テスト未実施)

---

## 5. 推定原因(優先度順)

### 5.1 第 1 候補:Claude Desktop の env 継承動作

`@modelcontextprotocol/server-github` は `npx` 経由で起動される子プロセス。
Claude Desktop が子プロセス起動時に親の環境変数を渡す動作をしているか、`claude_desktop_config.json` に `env` ブロックがないと渡らない仕様か、を確認する必要がある。

env-mcp-incident.md §4-5 では「env ブロックは不要・OS 環境変数から自動継承」と判断されているが、これが Windows + Claude Desktop の組み合わせで実際に成立しているかは未検証。

### 5.2 第 2 候補:PAT 自体の有効性が GitHub API で未検証

curl 直接テストで PAT の生存を確認していない。echo で値が表示されることと、その値が GitHub API で受理されることは別。GitHub Fine-grained PAT は発行直後の反映遅延や、複数 PAT 並存時の干渉がある(19 代目で経験済み)。

### 5.3 第 3 候補:`@modelcontextprotocol/server-github` の deprecation

npm 公式ページに「**Deprecation Notice**: Development for this project has been moved to GitHub in the github/github-mcp-server repo」と記載あり。古い npm パッケージが認証ロジックの変更に追従していない可能性。

---

## 6. 次の切り分け手順(順に実施・上から)

### Step A: PAT 直接テスト(最優先・最も確実)

cmd で以下を実行:

```
curl -H "Authorization: Bearer %GITHUB_PERSONAL_ACCESS_TOKEN%" https://api.github.com/user
```

期待される結果:自分のユーザー情報(`"login": "Minato33440"` 等)が JSON で返る。

#### 結果による分岐

| 結果 | 解釈 | 次のステップ |
|---|---|---|
| 200 OK + ユーザー情報 | PAT 有効 + シェル変数展開 OK | Step B へ(問題は MCP 側の継承) |
| 401 Unauthorized | PAT 無効 / 期限切れ / スコープ不足 | PAT 再発行(All repositories + Contents Read/Write)→ 環境変数更新 → Claude Desktop 完全終了再起動 → 再試行 |
| `Authorization: Bearer %GITHUB_PERSONAL_ACCESS_TOKEN%` がそのまま送られる(空展開) | 環境変数が cmd でも展開されていない | 環境変数登録スコープを再確認(User vs System)・PowerShell から再登録 |
| その他のエラー | ネットワーク / プロキシ / DNS の問題 | 環境固有の調査 |

### Step B(Step A で 200 OK の場合): `claude_desktop_config.json` に env ブロック明示追加

env-mcp-incident.md §5 で削除した env ブロックを **明示的に再追加**(セキュリティ上の懸念は §B-1 で対処):

```json
"github": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "github_pat_実際のPAT値をここに直書き"
  }
}
```

**重要な注意**:
- `${VAR}` や `%VAR%` 構文は **Claude Desktop で展開されない**(env-mcp-incident.md §5 の確認事項)
- よって **PAT 値を直接文字列として書く** 必要がある
- 動作確認後、`claude_desktop_config.json` を **`.gitignore` 追加対象**として保護

#### B-1 セキュリティ衛生(直書き対策)

`claude_desktop_config.json` のローカルパス例:

```
%APPDATA%\Claude\claude_desktop_config.json
```

このファイルは:
- リポジトリ管理対象外(Claude Desktop ローカル設定)
- ユーザーホーム配下にあり、Git にコミットされる経路がない
- ただし、誤って共有 / バックアップに含まれないよう Boss に注意喚起

#### B-2 動作確認

1. `claude_desktop_config.json` 編集後、**JSON バリデーター**で構文確認(env-mcp-incident.md §4 で同様の事故あり)
2. Claude Desktop を **タスクマネージャー経由で完全終了** → 再起動
3. ログ確認(github MCP の「ログを表示」)で `running` 確認
4. 書込テスト実施(§7.1)

#### B-3 結果による分岐

| 結果 | 解釈 |
|---|---|
| 書込成功 | 「Claude Desktop が子プロセスへ OS 環境変数を継承していなかった」が確定。env-mcp-incident.md §4-5 の判断は誤り |
| 401 継続 | 第 3 候補(deprecation)に進む → Step C |

### Step C(Step B で解決しない場合): MCP server を新実装に切替

`@modelcontextprotocol/server-github` は deprecated。GitHub 公式の `github/github-mcp-server` に切替する。

#### C-1 npm キャッシュクリア(まず試す)

```
npx clear-npx-cache
```

→ Claude Desktop 完全終了再起動 → 再試行

これで通れば npx キャッシュが古い版を使っていた可能性。

#### C-2 Docker 版に切替(C-1 で解決しない場合)

`claude_desktop_config.json`:

```json
"github": {
  "command": "docker",
  "args": ["run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "ghcr.io/github/github-mcp-server"],
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "github_pat_実際のPAT値"
  }
}
```

前提:Docker Desktop が稼働していること。
これで通れば npm 版の認証ロジック老朽化が原因。

### Step D(全て試して解決しない場合): MCP server ログ詳細取得

Claude Desktop で github MCP の「ログを表示」から、サーバー起動時のメッセージを確認:

- サーバー起動時に `process.env` のダンプがあるか
- `Authentication Failed` 以外のエラーメッセージ(403、429、5xx)が出ていないか
- リクエスト送信時の HTTP ヘッダーが見えるか

ログを Boss にシェアしてもらい、本指示書の §9 に記録した上で、より詳細な切り分けを実施。

---

## 7. 解決後の検証手順

### 7.1 最小書込テスト

```
github:create_or_update_file
  owner: Minato33440
  repo: REX_Brain_Vault
  path: system/handoff/_write_test.md
  content: write test ok
  message: test: write test from solving session
  branch: main
```

→ 成功確認後、即削除(GitHub Web UI から / `git rm` でローカル削除 → push でも可)

### 7.2 20 代目残課題の Vault 反映

20 代目 Wiki-Eval(本指示書の起票者)が web client セッション内で作成済みの **2 ファイル** を Vault に反映する。両ファイルの完全な内容は Boss が web client セッションのメッセージから取得できる(artifact として保管されている)。

#### a. 新規作成

- パス:`system/handoff/2026-05-03_layer1_verification_protocol.md`
- 内容:Layer 1 動作検証プロトコル(Boss 手動実行型・Obsidian 4 項目検証)
- 用途:env-mcp-incident.md による環境変更後の Layer 1 回帰検証手順

#### b. 更新(append-only)

- パス:`system/handoff/vault-planner-handoff.md`
- 操作:`§8 全体を末尾に追加`(append-only ルール厳守・19 代目までの記述は **一切削除しない**)
- SHA:`get_file_contents` で最新 SHA を取得 → `create_or_update_file` の `sha` パラメータに指定
- 内容:20 代目セッションエントリ(初代 Vault-Planner 正式確定 / Vault-Planner ロール範囲訂正 / Layer 1 完成判定 / 21 代目 Wiki-Eval + 2 代目 Vault-Planner への 2 系統同時引き継ぎ等)

両ファイルとも本指示書の §0 で言及した web client セッションに完全形が残されているので、Boss から該当内容を受領して push する。

### 7.3 env-mcp-incident.md 補正

| セクション | 操作 | 内容 |
|---|---|---|
| §6 | 訂正 | `GITHUB_TOKEN` → `GITHUB_PERSONAL_ACCESS_TOKEN`(公式参照名)に修正 |
| §7 | 追加 | 「GitHub MCP 経由 Vault 書込テスト ✅(2026-05-03 解決)」を追加 |
| §8 | 拡張 | 以下 2 項目を再発防止リストに追加: |

§8 追加項目:
- [ ] 環境変数名は公式ドキュメントで毎回確認(`@modelcontextprotocol/server-github` は `GITHUB_PERSONAL_ACCESS_TOKEN`)
- [ ] env 継承動作は OS + Claude Desktop バージョン依存のため、`claude_desktop_config.json` の env ブロック明示が確実

---

## 8. 解決後に更新すべきファイル一覧

| # | ファイル | 操作 | 内容 |
|---|---|---|---|
| 1 | `system/handoff/2026-05-03_layer1_verification_protocol.md` | 新規作成 | 20 代目作成済み(web client artifact) |
| 2 | `system/handoff/vault-planner-handoff.md` | 更新(append-only) | 20 代目 §8 追記(web client artifact) |
| 3 | `system/handoff/2026-05-03_env-mcp-incident.md` | §6 訂正 + §7 追加 + §8 拡張 | 上記 §7.3 |
| 4 | `system/handoff/2026-05-03_github_mcp_write_handoff.md` | 新規作成 + §9 追記 | 本書を Vault に push し、解決記録(§9)を末尾追記 |

---

## 9. 解決記録(解決後に追記)

*(解決を実施した Claude / 日時 / 効いた対処 / 残った警戒事項 を以下フォーマットで記録)*

```markdown
### 解決記録(YYYY-MM-DD)

**実施者**: (一般スレ Claude / ClaudeCode のいずれか)
**効いた対処**: (Step A / B / C / D のどれか・具体的に)
**経緯**:
- (試した順番と結果)

**最終構成**:
- claude_desktop_config.json: (env ブロック有無 + 構成)
- 環境変数: (登録名 + スコープ)
- MCP server: (npm / Docker / その他)

**残った警戒事項**:
- (将来の Vault-Planner / Wiki-Eval が知るべきこと)
```

---

## 10. 参考リンク

- `@modelcontextprotocol/server-github` (npm): https://www.npmjs.com/package/@modelcontextprotocol/server-github
- 後継: `github/github-mcp-server`: https://github.com/github/github-mcp-server
- modelcontextprotocol.io 公式例: https://modelcontextprotocol.io/examples
- GitHub Docs(MCP 設定): https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp/

---

## 改訂履歴

| 日付 | 版 | 起草者 | 主な変更 |
|---|---|---|---|
| 2026-05-03 | v1 | 20 代目 Wiki-Eval(初代 Vault-Planner 確定)/ Claude Opus 4.7 / web client | 初版起票・GitHub MCP 書込 401 問題の切り分け指示書として |

---

*起草: 20 代目 Wiki-Eval(初代 Vault-Planner 確定)/ Claude Opus 4.7 / web client / 2026-05-03*
*本書は Vault-Planner ロールが Vault 自律運用基盤を確立するための「亭主の道具立て」*
*解決後は §9 を追記し、§8 のファイル更新リストに従って Vault 全体を整合化すること*