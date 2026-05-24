# Grok OAuth Bridge & vault-mcp — アーキテクチャ & 構築ノート

- 最終更新: 2026-05-23（vault-mcp 統合完了）
- 対象: Claude オーケストレーター ⇄ OAuth-Grok（Hermes ワンショット経由） + Obsidian（vault-mcp 統合）
- 関連: `Rex_Grok_Toolbox.md`（運用マニュアル）
- ステータス: **Phase 4.9 完成（2026-05-23）**
  - Plan C（grok-oauth）: `ask_grok` から OAuth で X 検索が同期で通ることを実機確認済み
  - Phase 4.9（vault-mcp）: Obsidian REST API + hermes_ask_grok 統合、stdio MCP 接続確認済み

---

## 1. 目的

Claude Desktop（オーケストレーター）から、SuperGrok サブスクの OAuth セッションをそのまま使って Grok を **同期的に** 呼び出す。xAI 開発者API（従量課金）を使わず **追加コストなし**。かつ `REX_Brain_Vault`（Rex の聖域）には一切手が届かない構造にする。

---

## 2. 全体アーキテクチャ

```
Claude Desktop (オーケストレーター)
   │
   ├─ MCP ツール呼び出し (ask_grok / grok_work)
   │  ▼
   │  grok_oauth_bridge.py  (カスタム MCP サーバー / stdio)
   │     │  subprocess: hermes -z "<prompt>" -t <toolsets> --accept-hooks
   │     │  env: HERMES_HOME = ...\AppData\Local\hermes
   │     ▼
   │     Hermes Agent (one-shot)   ← provider: xai-oauth (SuperGrok)
   │        ▼
   │     Grok が応答 → stdout → MCP レスポンス → Claude のチャットに同期表示
   │
   └─ MCP ツール呼び出し (obsidian_list_notes / hermes_ask_grok / 他)
      ▼
      vault-mcp (filesystem-mcp/server.py)  (MCP サーバー / stdio)
         │  Obsidian REST API (local)
         │  hermes -z ワンショット統合
         │  env: HERMES_HOME, Obsidian_Local_REST_API
         ▼
         Obsidian Vault ← (直接ローカルアクセス)
         Grok (via hermes_ask_grok ツール)
```

---

## 3. 認証レイヤーの整理（重要・混同注意）

同じ "Grok" でも 2 系統あり、ここを混同すると沼にはまる。

| ライン | 経路 | 認証 | コスト |
|---|---|---|---|
| A. Grok-MCP 直結 | Claude → Grok-MCP → api.x.ai | `XAI_API_KEY`（開発者API） | 従量課金 |
| B. 本ブリッジ | Claude → grok-oauth → `hermes -z` | OAuth（SuperGrok） | サブスク内（追加なし） |

- SuperGrok サブスクと xAI 開発者API は **課金が別建て**。サブスクがあっても API キーは別途クレジット/支払いが要る（古いキーや未課金だと `API key is currently blocked`）。
- 本ブリッジ（B）は OAuth を使うので **サブスク範囲内で完結**する。

---

## 4. 構築のポイント（経緯と設計判断）

### 4.1 行き止まり: メッセージング・ブリッジ
- `hermes mcp serve` が公開するのは **会話（messaging）ツールのみ**（`conversations_list` / `messages_send` 等 10 個）。Grok を直接叩くツールは無い。
- `messages_send` で Discord に投稿しても、記録 role が `assistant`（= Bot 自身の発言）になり、gateway のエージェントは自分の発言に応答しない → **Grok の返信がトリガーされない**。
- 結論: messaging 経由の **双方向ループは不成立**。読み取り（`messages_read` 等）は可能。

### 4.2 教訓: HERMES_HOME 不一致
- `hermes mcp serve` を Claude Desktop が素のコマンドで起動すると、`HERMES_HOME` 未指定時は `~/.hermes` をデフォルト参照 → gateway の `AppData\Local\hermes` と **別ディレクトリ** になり、channels/conversations が空になる。
- 同じ罠がワンショットにも効く: subprocess の hermes が正しい home を見ないと **OAuth 資格情報を見失い、headless でプロンプト待ちハング** する（無言タイムアウトの主犯）。
- 対策: 起動 env / subprocess env に `HERMES_HOME` を明示注入。

### 4.3 採用: hermes -z ワンショット
- `hermes -z "<prompt>"` は **最終応答テキストのみ stdout に出力**（バナー/スピナー/session_id 行なし、approval 自動バイパス）。スクリプト/パイプ用途。
- これを subprocess で呼ぶカスタム MCP ツールにすることで、Discord も role 問題も非同期待ちも回避。**同期・OAuth・追加コストなし** を同時達成。

---

## 5. headless 堅牢化のポイント

ワンショットを MCP から無人起動するため、以下を仕込む（`grok_oauth_bridge.py` 実装済み）:

- `HERMES_HOME` を subprocess env に明示注入（OAuth 解決）
- `--accept-hooks`（シェルフック承認待ちのハング回避）
- `stdin=subprocess.DEVNULL`（対話入力待ちを EOF で即終了）
- `timeout=120`（固まらず即エラー）
- stdout が空なら `returncode` と `stderr` を返す（原因が見える）

---

## 6. ガードレール設計

| 項目 | 値 |
|---|---|
| 許可ルート | `C:\Python\REX_AI` 配下のみ |
| 明示拒否 | `C:\Python\REX_AI\REX_Brain_Vault`（聖域・配下含む） |
| terminal / computer-use | どちらのツールにも **含めない** |
| `ask_grok` toolsets | `x_search,web,vision`（書込なし） |
| `grok_work` toolsets | `file,code_execution,image_gen,x_search,web,vision`（workdir 限定） |

> **2026-05-23 更新（重要）:** `-t` の値を `web,search,vision` → `x_search,web,vision` に修正。
> `search` は `web` と中身（`web_search`）が重複するため削除。`x_search` を**明示追加**したことで X 検索が有効化された（経緯は §9）。

検証結果（2026-05-22）: 聖域拒否 / ルート外拒否（System32）/ 聖域配下拒否 / 許可リポ書込成功 — **全て確認済み**。
注: `grok_work` の実通は `-t` 変更後に再確認予定（次回作業。日次制限の都合で本日は見送り）。

---

## 7. 関連ファイル・設定

### 7.1 Grok-OAuth（質問応答・X検索）

- MCP サーバー実装: `C:\Python\REX_AI\MCP_Servers\Grok-OAuth\grok_oauth_bridge.py`
- 依存管理: `C:\Python\REX_AI\MCP_Servers\Grok-OAuth\pyproject.toml` （mcp >= 1.0.0）
- Hermes home: `C:\Users\Setona\AppData\Local\hermes`

Claude Desktop 設定：

```json
"grok-oauth": {
  "command": "uv",
  "args": [
    "--directory",
    "C:\\Python\\REX_AI\\MCP_Servers\\Grok-OAuth",
    "run",
    "python",
    "grok_oauth_bridge.py"
  ]
}
```

> 注: `hermes` が PATH で見つからない場合は env に `HERMES_BIN`（絶対パス）を追加。

### 7.2 vault-mcp（Obsidian 統合・ローカルアクセス）

- MCP サーバー実装: `C:\Python\REX_AI\MCP_Servers\filesystem-mcp\server.py`
- 依存管理: `C:\Python\REX_AI\MCP_Servers\filesystem-mcp\pyproject.toml`
  - `mcp[cli] >= 1.26.0`, `httpx >= 0.28.1`, `python-dotenv >= 1.0.1`
- 起動モード: **stdio（デフォルト）** ＝ Claude Desktop MCP クライアント接続用
  - オプション: `--http` で Uvicorn HTTP サーバーモード（テスト用）に切替可

提供ツール：
- `obsidian_get_note(path)` — ノート読み込み（Obsidian REST API）
- `obsidian_list_notes(directory)` — Vault 内ファイル一覧
- `obsidian_create_note(path, content)` — ノート作成・上書き
- `obsidian_append_to_note(path, content)` — ノート追記
- `obsidian_delete_note(path)` — ノート削除
- `obsidian_search(query)` — 全文検索
- `hermes_ask_grok(prompt)` — Grok に質問（x_search, web, vision）
- `read_file(path)` / `write_file(path, content)` / `list_directory(path)` など（ファイルシステム）

Claude Desktop 設定：

```json
"vault-mcp": {
  "command": "uv",
  "args": [
    "--directory",
    "C:\\Python\\REX_AI\\MCP_Servers\\filesystem-mcp",
    "run",
    "python",
    "server.py"
  ],
  "env": {
    "HERMES_HOME": "C:\\Users\\Setona\\AppData\\Local\\hermes",
    "Obsidian_Local_REST_API": "f520accd02fd161394252fdf25facbba22de0bc0f44924854e107125c36b174c"
  }
}
```

---

## 8. 既知の制約・注意点

### grok-oauth 関連
- `-z` は approval 自動バイパス。だから **ツールセットを `-t` で絞ることが安全の要**。`terminal` は既定で外す。
- 日次制限（SuperGrok）に達すると応答が止まる / 強制終了することがある。
- ワンショットは起動のたびにエージェント全体をロードするオーバーヘッドあり。低レイテンシ / 再利用が必要なら `hermes proxy`（OpenAI 互換ローカルプロキシ）への昇格を検討。
- スキルのドキュメントに **実在しないツール名を書かない**。公開中の実ツールは `ask_grok` / `grok_work` の 2 つ。
- **`web`（web_search / web_extract）は別プロバイダのキーが必須**（`EXA_API_KEY` / `PARALLEL_API_KEY` / `FIRECRAWL_API_KEY` / `TAVILY_API_KEY` のいずれか）。キー未設定だと `-t` に `web` を入れても Web 検索は動かない。**X 検索（`x_search`）は OAuth で動くので、この Web 検索キーとは無関係**。両者は別系統と理解すること。

### vault-mcp（Obsidian 統合）関連
- Obsidian REST API キー（`Obsidian_Local_REST_API`）は **vault-mcp の env に必須**。未設定だと Obsidian ツールが 401 Unauthorized を返す。
- stdio モードが MCP クライアント接続用デフォルト。HTTP モード（`--http`）は開発・テスト用（Uvicorn サーバー、本来のオーケストレータ経由）。
- `hermes_ask_grok()` は vault-mcp 内部で subprocess で hermes -z を呼ぶため、**HERMES_HOME が正しく設定されていることが必須**。不一致だと OAuth 資格情報が見失われ、タイムアウトする。
- REX_Brain_Vault の読み書きは **ガードレール外（禁止）**。filesystem-mcp の `_check_workdir()` で prevent される。

---

## 9. x_search 有効化の確定知見（2026-05-23・Plan C 完成時）

今日いちばんハマった所。**`x_search` を効かせるには 3 点すべてが必要**で、1 つでも欠けると `ask_grok` は `vision` だけになり、X 検索結果が空（`None` や stdout 空）になる。

### 必須 3 点セット
1. **`hermes tools` → CLI で 🐦 X (Twitter) Search のトグルを ON**（`[✓]`）。
2. **`hermes tools` → `4. Reconfigure an existing tool's provider or API key` → 🐦 X Search → `1. xAI Grok OAuth (SuperGrok Subscription)` を選択**。
   - 選択すると `no configuration needed!` と出る。これは**既存の SuperGrok OAuth セッションをそのまま使う**意味で正常（追加のブラウザ認証は不要だった）。
   - もう一方の選択肢 `2. xAI API key [paid]` は**従量課金ライン A**。OAuth・追加課金なしで行くなら必ず `1` を選ぶ。
3. **bridge の `-t` に `x_search` を明示**（`ask_grok` = `x_search,web,vision`）。

### 名前の罠（沼の本体）
- **`x_search` は toolset 名ではなく tool 名。** Hermes の Toolsets Reference / Built-in Tools Reference の toolset レジストリに `x_search` という toolset は載っていない（xAI モデル内蔵の Responses ツール扱い）。
- それでも **`-t` の文字列としては受理される**（実機確認済み: `hermes -z "..." -t x_search,vision` で X 検索が動いた）。
- 一方 `web_search` は **tool 名であって toolset 名ではない**ため、`-t web_search` と書くと `ignoring unknown --toolsets entries: web_search` で弾かれる。Web 検索を `-t` で有効化したいときは toolset 名の **`web`**（中身 = `web_search` + `web_extract`）を渡す。
- まとめ: `-t` に渡すのは **toolset 名**（`web` / `vision` / `file` 等）。例外的に `x_search` だけは tool 名で直接通る。

### 切り分けの定石（再発時）
- `2+2`（ツール不要）が通る → OAuth で Grok 本体との会話は生きている。
- なのに検索が空 → ほぼ「ツールが候補に乗っていない」。素の `hermes -z "..." -t <toolsets> --accept-hooks` を**ターミナルで直接**叩いて、bridge を介さず切り分ける。素で通れば犯人は bridge プロセス側（下記の再起動）。

### 運用上の最重要ハマりどころ: MCP プロセスの完全終了
- **`grok_oauth_bridge.py` を修正したら、Claude Desktop の「ウィンドウ再起動」だけでは不十分。** MCP サブプロセスが古いコード（旧 `-t`）を掴んだまま残留し、修正が反映されない。
- **対策: タスクマネージャから Claude Desktop を完全終了 → 再起動。** これで MCP サーバーが新しいコードを読み直す。本日この残留で 2 回ハマった。
