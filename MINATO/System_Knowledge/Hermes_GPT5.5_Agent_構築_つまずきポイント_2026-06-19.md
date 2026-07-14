# Hermes gpt（OAuth-GPT5.5）Agent 構築 ── つまずきポイントまとめ

> 日付: 2026-06-19
> 対象: `HERMES_HOME = C:\Users\Setona\AppData\Local\hermes` の `gpt` プロファイル
> ゴール: grok（OAuth-Grok）に準じた構成で **OAuth-GPT5.5** プロファイルを作り、
> **Discord Agent** と **Hermes-Desktop Agent** を立てる
> 関連: [[Local orchestration lecture v8]]（本書はその付録C／§8-3 を補完する実戦ログ）

---

## 0. 結論サマリ（先に要点）

| # | つまずき | 真因（どの層か） | 直し方 |
|---|---|---|---|
| 1 | `hermes login` が消えた | CLI仕様変更 | `hermes auth`（cred管理）／`hermes model`（provider選択）／`hermes setup` に分割された |
| 2 | **`auth status`=logged in なのに実行が「No Codex credentials stored」** | ⑦Runtime（認証の格納先違い） | `auth add`は**pool**に書く。chatは**singleton**を読む → `hermes -p gpt model` で singleton を埋める |
| 3 | 資格情報の場所を見失う | 環境（HERMES_HOME＋囮のバックアップ） | `auth list` で確認。`Desktop\profiles` は**バックアップ**で無関係 |
| 4 | Gateway が勝手に落ちる（exit 15） | プロセス親子関係 | セッション付随で起動すると死ぬ。**自分のターミナルで `--replace` 常駐** |
| 5 | gpt-5.5 で context 警告が出る | ⑧LLM（Codex固有の上限） | 仕様。272K上限ゆえ auto-compaction を85%へ自動引き上げ（無効化可） |

最重要は **#2**。今回の8割の時間はここの切り分けに費やした。

---

## 1. 前提となった発見（OAuth-GPT5.5 の正体）

「OAuth-GPT5.5」= Hermes の **`openai-codex` provider**（ChatGPTサブスクの OAuth、Codexバックエンド）。
grok の `xai-oauth`、claude の `anthropic` と**同じ「OAuth相続」の棚**に並ぶ3本目の柱。

```yaml
# profiles/gpt/config.yaml（最終形）
model:
  provider: openai-codex
  base_url: https://chatgpt.com/backend-api/codex   # ← hermes model が自動設定
  default: gpt-5.5
providers: {}
```

- `hermes login --provider {nous,openai-codex,xai-oauth}` のうち **openai-codex** が GPT 系の OAuth 経路。
- モデルID は **`gpt-5.5`**（bare id。`hermes_cli/codex_models.py` の `DEFAULT_CODEX_MODELS` 先頭）。
- `api_mode` は **config に書かない**（codex ランタイムが実行時に自動解決。grok の xai-oauth と同じ作法）。
- `gpt` プロファイルは構築時点で**独自の Discord Bot トークン**を既に保持していた（grok とは別アプリ）。

---

## 2. 【最重要】credential_pool と singleton の違い

### 症状
```
$ hermes auth status openai-codex
openai-codex: logged in            # ← 通る

$ hermes -p gpt -z "..."
agent failed: No Codex credentials stored. Run `hermes auth` to authenticate.   # ← 落ちる
```
**「認証は通っているのに実行が落ちる」** という、講座 §4-6（OAuthセッション ≠ provider binding）の今回版。

### 真因（コードで確認した格納先の違い）

| | 書き込みコマンド | 格納先 | chat ランタイムが読むか |
|---|---|---|---|
| プール | `hermes auth add openai-codex --type oauth` | `credential_pool.openai-codex`（複数cred・ローテーション用） | ❌ |
| **シングルトン** | `hermes -p gpt model` →（内部で `_login_openai_codex`）→ `_save_codex_tokens()` | `providers.openai-codex.tokens` | ✅ **これだけ** |

- `auth status` / `auth list` は **pool** を見て「logged in」と表示する。
- 実際の推論は `resolve_codex_runtime_credentials()` が **singleton** を読む。
- pool には oauth(device_code) エントリの `access_token` 文字列が無いため、pool フォールバック（`_pool_codex_access_token()`）も空を返す → 「No Codex credentials stored」。

> **理解メモ（2026-06-20）:** `credential_pool` は「認証情報の候補リスト／鍵束」で、`hermes auth list/status` が見る場所。`singleton` は `openai-codex` Runtime が実行時に読む「本命の1個の鍵」で、`providers.openai-codex.tokens` に入る。どちらも Hermes 側のローカル auth store に保存されるが、その token が紐づくアカウント・プラン・使用枠・有効性は OpenAI 側が管理する。たとえるなら、`providers.openai-codex.tokens` はローカルに持っている**運転免許証番号**で、警察側（OpenAI）が「その免許で乗れる車種・違反履歴・有効期限・使用制限」を照会して判断する、という関係。

### 直し方（singleton を埋める正規ルート）
`hermes login` 廃止後、singleton を書く実体（`_login_openai_codex`）は **`hermes model` のプロバイダ選択フロー**から呼ばれる。

```powershell
$env:HERMES_HOME = "C:\Users\Setona\AppData\Local\hermes"
$env:Path += ";$env:HERMES_HOME\hermes-agent\venv\Scripts"

hermes auth remove openai-codex 1     # 紛らわしい pool-only cred を消す（status の誤判定元）
hermes -p gpt model                    # → OpenAI ▸ Codex → ログイン → gpt-5.5 選択
```
`hermes model` の中で:
1. **OpenAI ▸ (Codex CLI or direct OpenAI API)** を選択
2. **OpenAI Codex** を選択
3. 「Found existing Codex CLI credentials at `~/.codex/auth.json` … Import? [y/N]」→ **`y`**
   （`~/.codex` が古い／期限切れなら `n` でデバイスコード認証＝ブラウザ新規ログイン）
4. モデルに **gpt-5.5** を選択

> singleton は **共有ストア（`HERMES_HOME/auth.json`）** に入る → grok の xai-oauth と同じく**全プロファイル共有**（講座 §8-3「設定の単一土台」）。`-p gpt` を付けても config の書き込み先が gpt に向くだけで、codex 資格情報は共有される。

---

## 3. 資格情報の場所を見失った件（囮に注意）

- 最初は「`auth add` を HERMES_HOME 未設定のセッションで打ったから別の home に書かれた」と**疑った**が、これは**誤り**だった。`HERMES_HOME` を固定して `hermes auth list` を見ると、cred は正しく LOCALAPPDATA 側に入っていた（真因は #2 の pool/singleton）。
- 調査中に `C:\Users\Setona\Desktop\profiles\`（ai/claude/codex/grok）が 6/18 以降更新されていて紛らわしかったが、これは**ただのバックアップ**。現行 home（`%LOCALAPPDATA%\hermes`）とは無関係。
- `~/.codex/auth.json` は **Codex CLI 自身のログイン**（auth_mode=chatgpt）。Hermes の singleton/pool とは別物だが、`hermes model` の import 元として再利用される。

> 教訓: 「authが効かない」時は推測で home を疑う前に、**`HERMES_HOME` を明示して `hermes auth list`** で“どのストアに何があるか”を一次情報で確認する。

---

## 4. Gateway の永続性（exit 15 の正体）

- 検証のため一時的にバックグラウンドで `hermes -p gpt gateway run` を起動 → セッション側の都合で **SIGTERM（exit code 15）で終了**した。
- `gateway run` はフォアグラウンド常駐プロセス。**起動した親プロセス（ターミナル／セッション）が死ぬと一緒に落ちる**。
- 永続運用は**ボス自身のターミナル**で起動する。`--replace` で既存インスタンスを安全に置換できる:

```powershell
hermes profile use gpt
hermes gateway run --replace
# もしくは
hermes -p gpt gateway run --replace --accept-hooks
```

- 稼働確認は `hermes profile list`（gateway列が running／◆=active）と、per-agent ログ:
  `profiles\gpt\logs\gateway.log` の `Connected as Codes_Hermes_bot#7452` / `✓ discord connected`。
- 状態ファイル: `profiles\gpt\gateway.lock` / `gateway_state.json`（pid・discord接続状態を保持）。

---

## 5. Discord Agent（実機確定）

- gpt Gateway は **`Codes_Hermes_bot#7452`** として接続。grok の **`Grok_Hermes_Bot#7485`** とは**独立Botで並走**（講座 §8-6 のマルチGateway実証）。
- 接続できた＝Discord Developer Portal の **MESSAGE CONTENT INTENT / PRESENCE INTENT** は既にON、Botもサーバー招待済み（付録C-3 の地雷は今回クリア済み）。
- `.env` の `GATEWAY_ALLOW_ALL_USERS=true` でallowlist無し運用（信頼境界は緩め。講座 Module 5 の通り、危険ツールを絞るなら Profile側で要対応）。

| Profile | Model | Provider | Discord Bot | 枠（quota） |
|---|---|---|---|---|
| grok | grok-4.3 | xai-oauth | Grok_Hermes_Bot#7485 | SuperGrok |
| **gpt** | **gpt-5.5** | **openai-codex** | **Codes_Hermes_bot#7452** | ChatGPT サブスク |
| claude | claude-opus-4-8 | anthropic | （未起動） | Claude Code |

→ provider も枠も別なので、**異種provider並走で枠を食い合わない**（講座 §10-2）。

---

## 6. Hermes-Desktop Agent

```powershell
hermes desktop
```
- §8-5 の通り、Desktop は共有 `HERMES_HOME` の profiles を**自動相続**。起動後 UI で **`gpt` を選ぶだけ**で gpt-5.5 エージェントになる（共有 codex singleton 再利用 → 追加認証不要）。
- 実機で **Discord / Desktop 双方から gpt-5.5 への通信成功を確認**。
- 口頭でまとめると
Hermes という職場に、gpt という職員証を持った GPT5.5 担当 Agent が追加された。 その Agent は Discord では Codes_Hermes_bot#7452 として常駐し、Hermes Desktop からも呼べる。 頭脳はローカルPCではなく ChatGPT / Codex 側の gpt-5.5。 Hermes はその頭脳へ OAuth で接続し、Agent Runtime として会話・ツール・Gateway を回している状態

---

## 7. gpt-5.5 固有の挙動（記録）

Bot 初回応答時に表示:
```
ℹ Codex gpt-5.5 caps context at 272K, so auto-compaction was raised to 85% (from 50%)
  to use more of the window before summarizing.
  Opt back out: hermes config set compression.codex_gpt55_autoraise false
```
- Codex OAuth 経由の gpt-5.5 は context 上限が **272K**（OpenAI API直の 1.05M とは別）。
- そのため `compression.codex_gpt55_autoraise: true`（既定）が、要約前に窓を使い切るよう **auto-compaction 閾値を 0.50→0.85 に自動引き上げ**る。
- 戻すなら: `hermes config set compression.codex_gpt55_autoraise false`

---

## 8. 任意の小改善（未対応・メモ）

- `profiles/gpt/config.yaml` の `stt.provider: xai` は xai専用。gpt で音声を使うなら `local` 推奨。
- `x_search` は xAI/Grok 機能なので gpt プロファイルでは使えない（モデルが選んでも失敗する）。

---

## 9. 付録: 症状 → まず疑う場所（今回版・講座 付録B 拡張）

| 症状 | まず疑う | チェック |
|---|---|---|
| `auth status` 通るのに実行が「No Codex credentials stored」 | pool vs singleton | `hermes -p <p> model` で singleton を埋めたか |
| `hermes login` が「removed」 | CLI仕様 | `hermes auth` / `hermes model` / `hermes setup` を使う |
| authが効かない／場所不明 | HERMES_HOME＋囮 | `HERMES_HOME` 明示で `hermes auth list`。Desktop\profiles はバックアップ |
| Gateway が勝手に落ちる | プロセス親子 | 自分のターミナルで `gateway run --replace` 常駐 |
| context 警告 | LLM固有上限 | Codex gpt-5.5 は272K。`codex_gpt55_autoraise` の挙動 |
| Bot がメッセージを読まない | 信頼境界/Intent | Developer Portal の MESSAGE CONTENT / PRESENCE INTENT |
| `HTTP 429: usage limit has been reached` | ⑧LLM（プランのCodex枠） | `errors.log` の JSON `resets_at` を見る。プラン枠枯渇は upgrade か別provider |

---

## 10. 【追記】HTTP 429 usage_limit_reached ── プランのCodex枠枯渇（2026-06-20）

構築翌日、gpt Bot が送信エラーに。Discordアイコンは点灯（接続OK）なのに応答が毎回**75文字固定** ＝ エラー文がそのまま送信されていた。

### 切り分け
- `hermes -p gpt -z "ping"` でもCLI直で同じ429 → Discord層は無実（§4-4「右半分」の故障）。
- `profiles/gpt/logs/errors.log` の本文に決定的証拠:
```json
{ "type": "usage_limit_reached", "plan_type": "go",
  "resets_at": 1784422312, "resets_in_seconds": 2503315 }
```
- `plan_type: "go"` ＝ プランは**失効ではなく有効**。`usage_limit_reached` ＝ **Goプランに割り当てられたCodex使用枠を消費しきった**。`resets_in_seconds`≒29日（リセット ≒ 2026-07-18）。

### 真因（構造）
このCodex枠は**アカウント共有**で、同一アカウントの **Codex CLI / VS Code拡張 / Hermes(gpt)** が全部1つのGo枠から引く。Goは Plus/Pro よりCodex枠が小さく、常駐Discord Botを足すと使い切る ── 講座 §8-6「**共有OAuth枠がTeam拡張の上限**」（grokのSuperGrok日次枠と同じ構造）がChatGPT Go側で顕在化した形。

### 誤診メモ（戒め）
- 当初 JWT の `subscription_active_until: 2026-06-17` を見て「**失効**」と誤診。実際はこれは6/16取得の**古いトークンにキャッシュされた日付**で、課金状態とは別。プラン状態は **429本文の `plan_type`** で見るのが正しい。
- フレッシュlog inしても**アカウント枠は戻らない**（auth層でなくLLM/プラン層の問題）。

### 解決
- **ChatGPT Plus にアップグレード → 即接続復旧**（2026-06-20、実機確認 / `hermes -p gpt -z` で `gpt-5.5` 応答）。
- 常駐Botを長期で回すなら、枠の食い合いを避ける構造的解は **`openai-api`（APIキー従量課金）への切替** か **Plus/Pro 以上**。Go＋常駐は枠的に無理がある。

---

*この文書は `REX_Brain_Vault/wiki/` 等に置けば、講座v8と*
*`[[openai-codex]]` `[[credential_pool]]` `[[singleton]]` `[[Agent-Team]]` `[[共有OAuth枠]]` 等で繋げられる。*
