# Discord Bot（Hermes）セットアップガイド
## Grok-OAuth-Bridge × Profile 統合版

**最終更新:** 2026-05-28  
**対象:** Hermes Runtime を使った複数 Discord Bot の運用（キャラクター・役割別）  
**ステータス:** Phase 4.9 完成・実機確認済  
**参考:** `Grok_OAuth_Bridge_Architecture.md`

---

## 目次

1. [目的](#目的)
2. [前提条件](#前提条件)
3. [ステップバイステップガイド](#ステップバイステップガイド)
   - [Step 1: Discord Developer Portal で Bot を作成](#step-1-discord-developer-portal-で-bot-を作成)
   - [Step 2: Hermes Profile を作成](#step-2-hermes-profile-を作成)
   - [Step 3: .env にトークンを設定](#step-3-env-にトークンを設定)
   - [Step 4: config.yaml を調整](#step-4-configyaml-を調整)
   - [Step 5: Hermes model を選択](#step-5-hermes-model-を選択)
   - [Step 6: Gateway を起動](#step-6-gateway-を起動)
   - [Step 7: Discord サーバーに Bot を招待](#step-7-discord-サーバーに-bot-を招待)
   - [Step 8: テスト](#step-8-テスト)
4. [注意点・重要な落とし穴](#注意点・重要な落とし穴)
5. [トラブルシューティング](#トラブルシューティング)
6. [参考・関連ファイル](#参考・関連ファイル)

---

## 目的

複数の Discord Bot を**キャラクター・役割ごとに独立して運用**する。各 Bot は異なるモデル（Grok / Claude / OpenAI など）を選択でき、完全に分離された環境で稼働する。

例：
- `Ai_Hermes_Bot` → Ai キャラクター用（モデル自由選択）
- `Grok_Hermes_Bot` → Grok 特性活用（xAI Grok OAuth）
- （将来）さらに別の Bot → 別の役割・モデル

---

## 前提条件

- ✅ Hermes Agent がインストール済みで、gateway が動作可能な状態
- ✅ Discord サーバーの管理権限 / Bot 招待権限がある
- ✅ Discord Developer Portal にアクセス可能
- ✅ xAI SuperGrok サブスク設定済み（OAuth Bot の場合）
- ✅ HERMES_HOME が正しく設定されている（デフォルト: `C:\Users\Setona\AppData\Local\hermes`）

---

## ステップバイステップガイド

### Step 1: Discord Developer Portal で Bot を作成

#### 1.1 新しいアプリケーションを作成

1. **Discord Developer Portal** → https://discord.com/developers/applications
2. **「New Application」** をクリック
3. 名前を入力（例: `Grok_Hermes_Bot`）
4. **「Create」** をクリック

#### 1.2 Bot ユーザーを追加

1. 左メニュー → **「Bot」** をクリック
2. **「Add Bot」** ボタンを押す（既に Bot がある場合は表示なし）

#### 1.3 必須インテント（Intents）を有効化

1. **「Privileged Gateway Intents」** セクションを見つける
2. 以下の 3 つをすべて **ON** 🟢 にする：
   - ✅ **Presence Intent**
   - ✅ **Server Members Intent**
   - ✅ **Message Content Intent** ← **これ最重要**（メッセージ内容を読む）
3. **「Save Changes」** をクリック

> ⚠️ **注意:** Intents を有効化しないと、Bot がメッセージを受け取れません。

#### 1.4 トークンを発行・コピー

1. **「Bot」** タブ内の **「Reset Token」** をクリック
2. 確認ダイアログで **「Yes, do it!」** をクリック
3. **新しいトークンが表示される**
4. **「Copy」** をクリックしてコピー

> ⚠️ **セキュリティ警告:** トークンは 2 回目以降は見られません。コピー後に保存先（`.env` など）をすぐに確保してください。

---

### Step 2: Hermes Profile を作成

Profile は、独立した Hermes 設定（モデル・プロバイダー・Discord トークン）のセット。Bot ごとに 1 つの Profile を作成します。

#### 2.1 新しい Profile を作成

PowerShell で実行：

```powershell
hermes profile create <profile_name>
```

例：
```powershell
hermes profile create grok
```

実行結果：
```
Profile created: grok
```

> **命名規則:** 小文字・スネークケース推奨（例: `grok`, `ai`, `trading_bot`）

#### 2.2 Profile に切り替え

```powershell
hermes profile use grok
```

確認：
```powershell
hermes profile list
```

現在のプロファイルが `◆grok` の前に表示されます。

---

### Step 3: .env にトークンを設定

Discord トークンは `config.yaml` ではなく **`.env` ファイル** に設定します。

#### 3.1 既存 Profile の .env をコピー（簡単）

すでに動作している Profile（例：`ai`）がある場合、その `.env` をコピー：

```powershell
Copy-Item "C:\Users\Setona\AppData\Local\hermes\profiles\ai\.env" `
          "C:\Users\Setona\AppData\Local\hermes\profiles\grok\.env"
```

#### 3.2 新しい Profile の .env を編集

```powershell
# エディタで .env を開く
code "C:\Users\Setona\AppData\Local\hermes\profiles\grok\.env"
```

ファイル内から以下の行を探して、トークンを置き換え：

```env
DISCORD_BOT_TOKEN=<Step 1.4 でコピーしたトークンをここに貼る>
```

例：
```env
DISCORD_BOT_TOKEN="******************************************"
```

**保存してください。** （Ctrl+S）

> ⚠️ **重要:** `config.yaml` に直接 `discord.token:` を書き込んでも、Hermes は `.env` の `DISCORD_BOT_TOKEN` を優先的に読み込みます。

#### 3.3 ルートの .env に Discord トークンがないことを確認

```powershell
cat "C:\Users\Setona\.hermes\.env"
```

または

```powershell
cat "$HOME\.hermes\.env"
```

**重要な確認：** `DISCORD_BOT_TOKEN` または類似の行が **存在しない** ことを確認してください。

> ⚠️ **ハマりどころ（Phase 4.9 で発見）:**
> - ルートの `.env` に `DISCORD_BOT_TOKEN` が設定されていると、それが **グローバル化**され、Profile の `.env` の値を **上書き**してしまう。
> - 複数 Bot を運用する場合、ルートには Discord トークンを置かず、各 Profile 配下の `.env` にのみ設定する。

---

### Step 4: config.yaml を調整

補助機能（Auxiliary）のモデル設定を追加して、警告を減らす。

#### 4.1 config.yaml を開く

```powershell
hermes profile use grok
code "C:\Users\Setona\AppData\Local\hermes\profiles\grok\config.yaml"
```

#### 4.2 auxiliary セクションを修正

`auxiliary:` セクション（通常 120～210 行目）を見つけて、以下のように変更：

**修正前（デフォルト・警告が出る）:**
```yaml
auxiliary:
  vision:
    provider: auto
    model: ''
  web_extract:
    provider: auto
    model: ''
  compression:
    provider: auto
    model: ''
  # ... その他
```

**修正後（推奨）:**
```yaml
auxiliary:
  vision:
    provider: xai-oauth
    model: grok-vision-beta
  web_extract:
    provider: auto
    model: ''
  compression:
    provider: auto
    model: ''
  # ... その他（デフォルトでOK）
```

> **選択肢：**
> - `xai-oauth` を使う場合 → `grok-vision-beta`
> - Claude を使う場合 → `claude-opus-4.6` など
> - 他のプロバイダー → そのモデル名

**保存してください。**

> ℹ️ **情報:** auxiliary セクションの他の項目は `auto` でも大丈夫。特に重要なのは `vision` だけ。

---

### Step 5: Hermes model を選択

各 Profile は独立したモデル・プロバイダーを選択できます。

#### 5.1 現在のプロファイルを確認

```powershell
hermes profile use grok
```

#### 5.2 モデルを選択

```powershell
hermes model
```

プロバイダーメニューが出現：

```
Select provider:

  (●)  1. Nous Portal (Nous Research subscription)
  (○)  2. OpenRouter (100+ models, pay-per-use)
  ...
  (○)  9. xAI Grok OAuth (SuperGrok / Premium+)
  ...
  (○) 19. xAI (Grok models — direct API)
  ...
  (○) 41. Leave unchanged
```

#### 5.3 プロバイダーを選択

**例 1: xAI Grok OAuth（推奨・サブスク内で完結）**

```
9
```

> ✅ **メリット:**
> - SuperGrok サブスク内で完結（追加課金なし）
> - XAI_API_KEY を設定する必要がない
> - x_search / vision が OAuth で動く

**例 2: Claude（Claude Code 認証を再利用）**

```
5
```

> ✅ **メリット:**
> - Claude Code で既に認証されていれば、トークンが自動再利用される
> - API キーを設定する必要がない
> - Opus など高度なモデルが使える

**例 3: 設定を変更しない**

```
41
```

> ℹ️ 既に設定済みの場合は 41 を選ぶだけで OK。

#### 5.4 確認

```powershell
hermes profile list
```

出力例：
```
 Profile          Model                        Gateway      Alias        Distribution
 ───────────────    ───────────────────────────    ───────────    ───────────    ────────────────────
  default         (not set)                    stopped      —            —
 ◆grok            grok-4.3                     running      grok         —
```

`grok` プロファイルに `grok-4.3` が設定されていることを確認。

---

### Step 6: Gateway を起動

#### 6.1 既存の Gateway を停止（必要な場合）

```powershell
hermes gateway stop
```

#### 6.2 Profile を切り替えて Gateway を起動

```powershell
hermes profile use grok
hermes gateway run --replace
```

起動ログ（成功時）：

```
┌─────────────────────────────────────────────────────────┐
│           ⚕ Hermes Gateway Starting...                 │
├─────────────────────────────────────────────────────────┤
│  Messaging platforms + cron scheduler                    │
│  Press Ctrl+C to stop                                   │
└─────────────────────────────────────────────────────────┘

WARNING hermes_plugins.discord_platform.adapter: Opus codec not found — voice channel playback disabled
```

> ℹ️ **Opus codec の警告は無視して OK。** テキストチャットには影響ありません。

#### 6.3 確認

別のターミナルで：

```powershell
hermes gateway status
```

出力：
```
✓ Gateway is running (PID: 13204)
```

---

### Step 7: Discord サーバーに Bot を招待

#### 7.1 招待 URL を生成

Discord Developer Portal → Grok_Hermes_Bot のアプリを開く

1. 左メニュー → **「OAuth2」** → **「URL Generator」**
2. **Scopes** チェック：
   - ✅ `bot`
   - ✅ `applications.commands`（任意）
3. **Bot Permissions** チェック（最小限）：
   - ✅ Send Messages
   - ✅ Read Message History
   - ✅ Embed Links
   - ✅ Attach Files
   - ✅ Add Reactions
4. 一番下まで下がると **「Generated URL」** が表示される
5. **URL をコピー**

#### 7.2 Bot を招待

1. コピーした URL をブラウザで開く
2. 招待したいサーバーを選択
3. **「認可」** をクリック

> ✅ **完了：** Bot がサーバーに参加しました。

---

### Step 8: テスト

#### 8.1 Bot がオンラインか確認

Discord サーバーのメンバー一覧を開いて、`Grok_Hermes_Bot` が **🟢 緑色（オンライン）** になっているか確認。

> ⚠️ **灰色（オフライン）の場合:** [トラブルシューティング](#トラブルシューティング)を参照。

#### 8.2 Bot に話しかける

テキストチャンネルで：

```
@Grok_Hermes_Bot こんにちは
```

Bot が応答すれば成功！ 🎉

#### 8.3 X 検索をテスト（OAuth の場合）

```
@Grok_Hermes_Bot 最近のAI業界ニュースをX検索してください
```

X 検索結果が返ってくれば、x_search 統合も成功。

> 💡 **参考:** X 検索が空になる場合は [トラブルシューティング → x_search が空](#x_search-が空になる) を参照。

---

## 注意点・重要な落とし穴

### ❌ ハマりどころ 1: ルート .env による グローバル化

**症状:**
- Profile の `.env` に設定したトークンが読み込まれない
- 別の Bot が起動する

**原因:**
- ルート `.env`（`C:\Users\Setona\.hermes\.env`）に `DISCORD_BOT_TOKEN` が設定されていると、それが **優先的に読み込まれ、Profile の設定が上書きされる**

**対策:**
```powershell
# ルートの .env を確認
cat "$HOME\.hermes\.env"

# DISCORD_BOT_TOKEN が含まれている場合は削除
# ファイルを開いて編集 or 削除
```

✅ **鉄則:** 複数 Bot を運用する場合、ルートには Discord トークンを置かない。各 Profile の `.env` に個別に設定。

---

### ❌ ハマりどころ 2: MCP プロセス残留（Bridge 使用時）

**症状（Grok-OAuth-Bridge の場合）:**
- `grok_oauth_bridge.py` を修正したのに、変更が反映されない
- Claude Desktop の「ウィンドウ再起動」をしても直らない

**原因:**
- 古い MCP サブプロセスがメモリに残留し、古いコードを実行したまま

**対策:**
```powershell
# Claude Desktop をタスクマネージャから完全終了
# （「ウィンドウ再起動」ではなく、プロセスを kill）

# その後、Claude Desktop を再起動
```

✅ **鉄則:** MCP 関連コードを修正したら、必ず Claude Desktop を **完全再起動**（終了 → 再起動）。

---

### ❌ ハマりどころ 3: 推論プロバイダーが設定されていない

**症状:**
```
WARNING gateway.run: Primary provider auth failed: No inference provider configured
```

**原因:**
- Profile で `hermes model` を選択していない
- あるいは API キーが不足している（Direct API の場合）

**対策:**
```powershell
hermes profile use <profile_name>
hermes model  # 必ずプロバイダーを選択
```

✅ **鉄則:** 各 Profile を作成したら、最初に `hermes model` でプロバイダーを選択。

---

### ❌ ハマりどころ 4: HERMES_HOME の不一致

**症状:**
- Gateway が起動しない
- 「OAuth 資格情報が見つからない」エラー

**原因:**
- MCP サーバー・subprocess が、正しい `HERMES_HOME` を参照していない
- デフォルト `~/.hermes` と実際の `AppData\Local\hermes` が異なる

**対策:**
```powershell
# HERMES_HOME を明示的に設定
$env:HERMES_HOME = "C:\Users\Setona\AppData\Local\hermes"

# その後、hermes コマンドを実行
hermes gateway run --replace
```

✅ **鉄則:** Script / MCP env では、常に `HERMES_HOME` を明示注入。

---

### ❌ ハマりどころ 5: x_search が空（日本語結果）

**症状:**
```
@Bot 日本語で検索してください
→ 応答なし / stdout 空
```

**ASCII は通る場合の根本原因:**
- **UnicodeDecodeError：Windows cp932 で UTF-8 出力をデコード**
  - subprocess.run() が strict encoding で例外を投げる
  - リーダースレッドが黙って例外を握り潰す
  - stdout 空 / returncode=0 が返される

**修正済みファイル（2026-05-26）:**
- ✅ `grok_oauth_bridge.py` の `_run()`
- ✅ `filesystem-mcp/server.py` の `hermes_ask_grok()`

追加済みコード：
```python
subprocess.run(
    ...,
    encoding="utf-8",      # ← これを追加
    errors="replace"       # ← これを追加
)
```

✅ **鉄則:** 日本語結果が空の場合、最初に **encoding を疑う**。

---

### ❌ ハマりどころ 6: x_search が有効化されない（結果が vision のみ）

**症状：**
```
@Bot 最新ニュースをX検索して
→ X 検索なし、vision 応答のみ
```

**必須 3 点セット（すべて揃えないと x_search は動かない）:**

1. **hermes tools で X Search を ON**
   ```powershell
   hermes tools
   # → 🐦 X (Twitter) Search をトグル ON [✓]
   ```

2. **Provider を「xAI Grok OAuth」に設定**
   ```powershell
   hermes tools
   # → 4. Reconfigure an existing tool's provider
   # → 🐦 X Search
   # → 1. xAI Grok OAuth (SuperGrok Subscription) を選択
   # → 「no configuration needed!」が出たら OK
   ```

3. **Bridge / Gateway の `-t` に `x_search` を明示**
   - `grok_oauth_bridge.py`: `-t x_search,vision`
   - gateway 起動: 自動的に含まれる

✅ **鉄則:** x_search が空なら、この 3 点を確認リストで回す。

---

## トラブルシューティング

### Bot が灰色（オフライン）のまま

**確認項目：**

1. **Gateway が起動しているか**
   ```powershell
   hermes gateway status
   ```
   
   出力：`✓ Gateway is running` なら OK

2. **Discord トークンが正しいか**
   ```powershell
   cat "C:\Users\Setona\AppData\Local\hermes\profiles\<profile_name>\.env" | Select-String "DISCORD_BOT_TOKEN"
   ```
   
   トークンが表示されればセット済み。

3. **Intents が有効か**
   - Discord Developer Portal → Bot → Privileged Gateway Intents
   - Message Content Intent が 🟢 ON か確認

4. **ルート .env に古いトークンがないか**
   ```powershell
   cat "$HOME\.hermes\.env" | Select-String "DISCORD_BOT_TOKEN"
   ```
   
   もし出力があれば、その行を削除。

5. **Gateway のログを確認**
   - Gateway を起動しているターミナルで、エラーメッセージを見る
   - `Invalid Token` → トークンが間違っている
   - `Discord connected` がない → 接続失敗

**復旧手順：**
```powershell
hermes gateway stop
# 5 秒待機
hermes profile use <profile_name>
hermes gateway run --replace
```

---

### x_search が空（ASCII は通る）

**確認項目：**

1. **x_search tool が ON か**
   ```powershell
   hermes tools
   ```
   🐦 X (Twitter) Search が `[✓]` か確認

2. **Provider が xAI Grok OAuth か**
   ```powershell
   hermes tools
   # → 4. Reconfigure
   # → 🐦 X Search
   # → 現在の Provider を確認
   ```

3. **encoding が UTF-8 か（Bridge 使用時）**
   `grok_oauth_bridge.py` で `encoding="utf-8"` が設定されているか確認

4. **stdout を直接確認**
   ターミナルで直接実行：
   ```powershell
   hermes -z "最新ニュース" -t x_search,vision --accept-hooks
   ```
   
   これで結果が出れば、Gateway/Bridge 側の問題。

---

### Gateway が起動しない / ハング

**確認項目：**

1. **別の Gateway が起動していないか**
   ```powershell
   hermes gateway status
   ```
   
   起動中なら先に停止：
   ```powershell
   hermes gateway stop
   ```

2. **HERMES_HOME が正しいか**
   ```powershell
   $env:HERMES_HOME
   # → C:\Users\Setona\AppData\Local\hermes と同じか
   ```

3. **Timeout（120秒以上ハング）**
   - Ctrl+C で強制終了
   - `hermes gateway stop --force` で強制停止
   - 別のターミナルから確認：`hermes gateway status`

---

### 公開ボット（Public Bot）が OFF にできない

**症状：**

```
エラー：
「プライベートアプリケーションはデフォルトの認認リンクを持つことはできません」

または

認証エラー：
integration_types_config : 1 文字以上 2 文字以下の文字を入力してください。
```

**原因：**

Developer Portal の「Installation」タブで、デフォルトのインストールリンク（Install Link）が設定されたままになっている。

**解決方法（正しい手順・確定）：**

#### Step 1: Installation タブで Install Link を None に設定

```
Developer Portal → 左メニュー「Installation」をクリック
  ↓
「インストールリンク」セクションを見つける
  ↓
「Discord提供リンク」のドロップダウン → 「None」を選択
  ↓
⚠️ 重要：インストール方法のチェックボックス（ユーザーインストール / ギルドのインストール）は外さない！
```

#### Step 2: Bot タブで「Public Bot」を OFF に設定

```
Developer Portal → 左メニュー「Bot」をクリック
  ↓
「許可されたフロー」セクション
  ↓
「公開ボット」トグルを OFF（灰色）に変更
  ↓
「保存変更」をクリック
```

**重要ポイント：**

- ❌ チェックボックスを外す → バリデーションエラー
- ✅ **Install Link を「None」に設定 → チェックボックスは外さない** ← **これが鍵！**

**確認：**

設定が成功したら、Developer Portal → Bot で：

```
「Public Bot」が OFF（灰色） ✅
```

と表示されていることを確認してください。

---

### 公開ボット OFF 後の復旧プロセス（重要）

**公開ボット OFF の設定後、Bot が Discord に接続できなくなる可能性があります。** 以下の復旧プロセスが必須です。

**症状：**

```
ERROR gateway.run: ✗ discord error: discord connect timed out after 30s
```

**根本原因：**

Install Link を「None」に設定することで、Bot の接続パラメータが変わり、Discord との接続が失敗する。

**復旧手順（確定・実機確認済）：**

#### Step 1: Bot をサーバーから完全に削除

```
Discord サーバー内
  ↓
メンバー一覧から Grok_Hermes_Bot を右クリック
  ↓
「キック」をクリック
  ↓
Bot がメンバーリストから消える
```

#### Step 2: Install Link を「None」に設定（公開停止）

```
Developer Portal → Installation
  ↓
「Install Link」 → 「None」に設定
  ↓
公開ボット OFF 完了
```

#### Step 3: 3 つの Intents をすべて ON に確認・設定

```
Developer Portal → Bot
  ↓
「Privileged Gateway Intents」セクションを確認
  ↓
以下の 3 つがすべて 🟢 ON か確認：
  ├─ ✅ Presence Intent
  ├─ ✅ Server Members Intent
  └─ ✅ Message Content Intent
```

> ⚠️ **重要：** Install Link を「None」に設定すると、Discord が Intents の再検証を行う。3 つすべてが ON でないと、Bot 接続パラメータが不完全になる。

#### Step 4: Bot をサーバーに再招待

```
Developer Portal → OAuth2 → URL Generator
  ↓
Scopes: bot をチェック
  ↓
Bot Permissions: 必要な権限を選択（Send Messages など）
  ↓
Generated URL をコピー
  ↓
ブラウザで開いて、サーバーを選択 → 「認可」
```

#### Step 5: Terminal で Gateway を再起動

```powershell
hermes gateway stop
hermes profile use grok
hermes gateway run --replace
```

成功ログ：
```
┌─────────────────────────────────────────────────────────┐
│           ⚕ Hermes Gateway Starting...                 │
├─────────────────────────────────────────────────────────┤
│  Messaging platforms + cron scheduler                    │
│  Press Ctrl+C to stop                                   │
└─────────────────────────────────────────────────────────┘

WARNING hermes_plugins.discord_platform.adapter: Opus codec not found — voice channel playback disabled
（エラーなし → 接続成功！）
```

#### Step 6: Bot が応答するか確認

```
Discord サーバーで：
@Grok_Hermes_Bot こんにちは
  ↓
Bot が応答 → ✅ 復旧完了！
```

**重要なポイント：**

- ✅ Install Link → None に設定してから、Intents を確認
- ✅ Intents が 3 つすべて ON であることが必須
- ✅ Bot 再招待 → Gateway 再起動の順序を守る

---

## 参考・関連ファイル

### ドキュメント

- **`Grok_OAuth_Bridge_Architecture.md`** — OAuth bridge 全体のアーキテクチャ・設計判断
- **`Rex_Grok_Toolbox.md`** — Hermes / Grok の運用マニュアル
- **本ドキュメント** — Discord Bot セットアップ（ステップバイステップ）

### Hermes Profile ディレクトリ

```
C:\Users\Setona\AppData\Local\hermes\
  ├── profiles/
  │   ├── ai/
  │   │   ├── config.yaml        ← AI モデル・設定
  │   │   └── .env               ← AI Discord トークン
  │   ├── grok/
  │   │   ├── config.yaml        ← Grok モデル・設定
  │   │   └── .env               ← Grok Discord トークン
  │   └── ...
  ├── .env                        ← ⚠️ ここに Discord トークンを置かない！
  └── gateway/                    ← Gateway ログ・状態ファイル
```

### Hermes 主要コマンド

```powershell
# Profile 操作
hermes profile list              # 全プロファイル表示
hermes profile use <name>        # プロファイル切り替え
hermes profile create <name>     # 新規プロファイル作成
hermes config edit               # config.yaml を編集

# Model 設定
hermes model                      # プロバイダー・モデル選択
hermes tools                      # ツール有効化・設定（x_search など）

# Gateway 操作
hermes gateway run --replace      # Gateway 起動（置換モード）
hermes gateway stop               # Gateway 停止
hermes gateway status             # Gateway 状態確認
hermes gateway restart            # Gateway 再起動

# ワンショット実行（スクリプト用）
hermes -z "質問" -t x_search,vision --accept-hooks < /dev/null

# Profile 管理・設定変更
hermes profile delete <name>      # Profile を削除
hermes profile use <name>         # Profile に切り替え

# Profile 設定ファイル（直接編集）
# Discord トークン変更
"C:\Users\Setona\AppData\Local\hermes\profiles\<name>\.env"

# モデル・プロバイダー・Auxiliary 設定変更
"C:\Users\Setona\AppData\Local\hermes\profiles\<name>\config.yaml"
```

### Gateway 完全再起動（推奨）

```powershell
# 一連の再起動コマンド（最も安全）
hermes gateway stop              # 既存 Gateway を停止
hermes profile use <name>        # Profile に切り替え
hermes gateway run --replace     # 新しい Gateway を起動（置換モード）
```

---

### トラブルシューティング用コマンド

```powershell
# 診断
hermes diagnostic

# ログ確認
Get-Content "$env:HERMES_HOME\logs\gateway.log" -Tail 50

# Environment 確認
$env:HERMES_HOME
$env:Path

# Windows イベントビューアーで Hermes エラーを確認
Get-EventLog -LogName Application -Source Hermes -Newest 10
```

---

## よくある質問（FAQ）

### Q. 複数の Profile に同じ Discord トークンを使える？

**A.** いいえ。各 Bot には固有のトークンが必要です。複数の Profile に同じトークンを設定すると、競合が発生します。

---

### Q. Profile を削除できる？

**A.** 手動削除は推奨されません。代わり、不要な Profile を使わないようにするか、新しい Profile を作成してください。

必要に応じて：
```powershell
Remove-Item -Recurse "C:\Users\Setona\AppData\Local\hermes\profiles\<name>" -Force
```

---

### Q. Gateway を複数起動できる？

**A.** いいえ。一度に 1 つの Gateway のみ起動可能。別の Profile に切り替えたい場合は、現在の Gateway を停止してから新しい Profile で起動してください。

```powershell
hermes gateway stop
hermes profile use <new_profile>
hermes gateway run --replace
```

---

### Q. Default Profile は使える？

**A.** `default` は Hermes の組み込みプロファイルで、`~/.hermes` に保存されます。新しい Profile を作成する際は、`default` ではなく別の名前（例：`grok`, `ai`）を使用してください。

---

## チェックリスト（初回セットアップ用）

セットアップ完了の確認用。すべてチェック ✅ なら成功です。

- [ ] Discord Developer Portal で Bot を作成した
- [ ] Intents（Presence / Members / Message Content）を 3 つとも ON にした
- [ ] トークンを発行・コピーした
- [ ] Hermes Profile を作成した（`hermes profile create <name>`）
- [ ] Profile の `.env` にトークンを設定した
- [ ] ルート `.env` に Discord トークンがないことを確認した
- [ ] config.yaml の auxiliary セクションを修正した（vision など）
- [ ] `hermes model` でプロバイダーを選択した
- [ ] Gateway が起動している（`hermes gateway status`）
- [ ] Discord サーバーに Bot を招待した（OAuth2 URL Generator）
- [ ] Discord でメンションしてみたら応答があった
- [ ] Bot がオンライン状態（🟢 緑色）で表示されている

---

## 今後のアレンジ・拡張

### 新しい Bot を追加したい

```powershell
# 1. Discord Developer Portal で新しい Bot を作成
# 2. トークンをコピー
# 3. Hermes で Profile を作成
hermes profile create <new_bot_name>

# 4. .env にトークンを設定（コピー or 新規作成）
# 5. config.yaml を調整
# 6. hermes model でプロバイダーを選択
# 7. Gateway を起動・テスト
```

### モデルを切り替えたい

```powershell
hermes profile use <profile_name>
hermes model  # 新しいプロバイダーを選択
```

### x_search を有効化したい

1. `hermes tools` で X Search を ON
2. Provider を xAI Grok OAuth に設定
3. Bridge / Gateway コマンドで `-t x_search` を明示

---

## 参考リンク

- **Discord Developer Portal:** https://discord.com/developers/applications
- **Hermes 公式ドキュメント:** https://github.com/neuml/hermes （関連リポジトリ）
- **xAI SuperGrok:** https://grok.x.ai （OAuth セッション情報の確認）

---

## 更新履歴

| 日時 | 変更内容 |
|---|---|
| 2026-05-28 | 初版作成。Grok-OAuth-Bridge / Discord Bot セットアップガイド完成 |
| 2026-05-26 | エンコーディング修正（cp932 → UTF-8）を反映 |
| 2026-05-23 | x_search 有効化の 3 点セット確定 |

---

## サポート・質問

本ドキュメントで不明な点や、新しいハマりどころを発見した場合は、このドキュメントを更新してください。

**所有者:** Rex  
**最終確認者:** Claudian（AI Assistant）
