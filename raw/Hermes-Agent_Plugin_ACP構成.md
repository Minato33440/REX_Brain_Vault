# Hermes-Agent Plugin（VSCode）ACP 接続構成

作成日: 2026-06-16 / 対象: REX_AI 環境（Windows 11）

VSCode の **Hermes-Agent プラグイン**をハブとして、**OAuth 承認済みの Claude Opus** と **Grok** を切り替えて使うための構成メモ。今回実機で検証した内容のみを記載。

---

## 1. 全体構成（接続の流れ）

```
┌─────────────────────────────┐
│ VSCode                      │
│  └ Hermes-Agent 拡張         │   joaompfp.hermes-ai-agent 3.0.0
│      (ACP クライアント本体)   │   ※別途 ACP-Client 拡張は不要
└───────────┬─────────────────┘
            │ spawn("hermes", ["acp"])  … 子プロセス起動 + JSON-RPC(stdio)
            ▼
┌─────────────────────────────┐
│ hermes acp  (v0.16.0)        │   ACP アダプタ
│  active profile = grok       │
└───────────┬─────────────────┘
            │ /model でセッション内に provider/model を切替
   ┌────────┴─────────┐
   ▼                  ▼
 xai-oauth          anthropic
 (SuperGrok)        (Claude Code の OAuth 流用)
 grok-4.3           claude-opus-4-8
```

- プラグインは **ACP（Agent Client Protocol）** で `hermes acp` と通信する。
- `hermes acp` は editor 統合用モード（VS Code / Zed / JetBrains 対応）。
- **Desktop の MCP serve / gateway とは独立**。gateway（Telegram/Discord/Slack）が止まっていてもプラグインは動く。

---

## 2. OAuth Claude Opus が動く仕組み（キモ）

Hermes **v0.16.0** から Anthropic 連携が追加され、`agent/anthropic_adapter.py` が以下を自動で行う。

トークン解決の優先順位（`resolve_anthropic_token()`）:

1. `ANTHROPIC_TOKEN` 環境変数
2. `CLAUDE_CODE_OAUTH_TOKEN` 環境変数
3. **`~/.claude/.credentials.json`（= Claude Code が OAuth ログイン済みの認証情報）** ← 今回はこれを使用。期限切れは自動リフレッシュ
4. `ANTHROPIC_API_KEY` 環境変数

→ provider が `anthropic` のとき、**API キー未設定なら Claude Code のサブスク OAuth をそのまま流用**する（`agent/agent_init.py:643`）。追加課金なしで Opus が使える。

> ⚠️ 旧 v0.14.0 では Anthropic OAuth 非対応だった。`hermes update` で v0.16.0 にして解決済み。
> `hermes login` の選択肢に anthropic が無いのは、device-flow ではなく「既存の Claude Code 認証を読む」方式だから（正常）。

---

## 3. プロファイル構成

| プロファイル | provider | default model | 用途 |
|---|---|---|---|
| **grok**（active） | xai-oauth | grok-4.3 | 通常／gateway 既定 |
| **claude** | anthropic | claude-opus-4-8 | Claude 専用（OAuth 流用） |
| ai | — | — | その他 |

- `active_profile` = **grok**（gateway や通常の hermes 呼び出しの既定を維持）。
- claude プロファイル設定: `profiles/claude/config.yaml`
  ```yaml
  model:
    default: claude-opus-4-8
    provider: anthropic
    base_url: https://api.anthropic.com     # ★ /v1 を付けない（SDK が /v1/messages を付加 → 二重で 404）
  providers: {}                              # API キー欄は空でOK（OAuth 自動解決）
  ```

> ❗ `base_url` に `/v1` を付けると `https://api.anthropic.com/v1/v1/messages` になり **HTTP 404**。必ず `https://api.anthropic.com` まで。

---

## 4. モデル切替（grok ⇔ claude）

プラグイン UI のモデル切替は、内部で **`/model <モデル名>`** スラッシュコマンドを送るだけ。

- `/model` は `agent/agent_runtime_helpers.py` の `switch_model()` を呼び、**セッション内で provider/model をその場で入れ替え、新 provider の認証を再解決**する（CLI / gateway / ACP 共通経路）。
- そのため **grok プロファイルのまま** UI で `claude-opus-4-8` を選べば、OAuth 経由で Opus が応答する（実機確認済み）。
- 逆に grok に戻せば xai-oauth に切り替わる。

→ **プロファイルを切り替えなくても、UI のモデル切替だけで grok ⇔ claude を往復できる。**

---

## 5. VSCode 側の設定

`%APPDATA%\Code\User\settings.json`（= `C:\Users\Setona\AppData\Roaming\Code\User\settings.json`）

```json
"hermes.path": "C:\\Users\\Setona\\AppData\\Local\\hermes\\hermes-agent\\venv\\Scripts\\hermes.exe",
"hermes.debugLogs": true
```

- **`hermes.path`**：絶対パス指定。spawn の PATH 解決失敗（→「ACP client not started」）を確実に回避。
- **`hermes.debugLogs`**：Output パネル「Hermes」に `[acp] spawn …` 等の診断ログを出す。

拡張の設定項目はこの2つのみ（プロファイルや起動引数を渡すオプションは無い）。

---

## 6. Opus を「既定」にしたい場合（任意）

UI で毎回切り替えるのではなく、プラグインを最初から Opus にしたいとき。拡張は `hermes acp`（プロファイル指定なし）で固定起動するため、environment 側で指定する:

- **VSCode だけに隔離（推奨）**：`HERMES_PROFILE=claude` を設定した状態で VSCode を起動
  （例: ショートカット/バッチで `set HERMES_PROFILE=claude && code`）。
  拡張は `process.env` を子プロセスへ渡すので `hermes acp` が claude プロファイル＝Opus 既定になる。gateway や Trade_Brain 等は grok のまま。
- **全体の既定も変えてよい場合**：`hermes profile use claude`
  （※ gateway も再起動時に claude 既定になる点に注意）。

---

## 7. トラブルシュート

### 「Error: ACP client not started」
拡張内で子プロセス（`hermes acp`）が起動できていない＝`this.proc` が null の状態。

1. **`hermes.path` を絶対パスに**（§5）→ VSCode を**完全再起動**（ウィンドウ再読込ではなく終了→起動）。
2. それでも出るなら **Output パネル → 「Hermes」** チャンネルのログを確認（`hermes.debugLogs: true`）。
3. hermes 側が生きているかの単体確認:
   ```powershell
   $H = "C:\Users\Setona\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exe"
   '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":1,"clientCapabilities":{}}}' | & $H acp --accept-hooks
   ```
   → `agentInfo … "version":"0.16.0"` を含む JSON が返れば Hermes 側は正常（＝拡張/環境側の問題）。

### モデル切替に Claude が出てこない
UI のドロップダウンに `claude-opus-4-8` が無い場合は、§6 の `HERMES_PROFILE=claude` 起動で claude プロファイルを既定にする。

---

## 8. 動作確認コマンド（CLI）

```powershell
$H = "C:\Users\Setona\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exe"

# claude プロファイルで Opus（OAuth）
& $H -p claude -z "State your exact model id." --accept-hooks
# → claude-opus-4-8

# grok プロファイルのまま Opus にモデル上書き（UI 切替に相当）
& $H -p grok -m claude-opus-4-8 -z "State your exact model id." --accept-hooks
# → claude-opus-4-8

# ACP 依存チェック
& $H -p claude acp --check        # → Hermes ACP check OK
```

---

## 補足: 認証は「共有」

Claude Code（CLI/IDE）と Hermes は同じ `~/.claude/.credentials.json` を参照するため、**同じ OAuth セッションを別インターフェースから利用**しているだけ。Anthropic サブスクの利用枠も共有される。
</content>
</invoke>
