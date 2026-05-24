# Discord × Hermes × Grok Bot システム構築ガイド

**作成日**: 2026-05-21  
**バージョン**: 1.0

---

## 📋 目次

1. [概要](#概要)
2. [セットアップ手順](#セットアップ手順)
3. [トラブルシューティング](#トラブルシューティング)
4. [使用可能な機能](#使用可能な機能)
5. [使用例](#使用例)
6. [自動起動設定](#自動起動設定)

---

## 概要

このシステムは、Discord サーバーで Hermes Agent を通じて xAI の **Grok** モデルとチャットできるようにしたものです。

### アーキテクチャ

```
Discord サーバー
    ↓ (メッセージ送信)
Hermes Gateway (Discord Platform)
    ↓ (API呼び出し)
Grok モデル
    ↓ (Web Search, X-Search など)
外部 API (FAL, Tavily など)
    ↓ (応答生成)
Discord Bot → ユーザーへ返信
```

### 必要なもの

- ✅ Discord サーバー（自分が管理するサーバー）
- ✅ Discord Developer Portal アカウント
- ✅ Hermes Agent インストール済み
- ✅ xAI API キー（XAI_API_KEY）
- ✅ Windows / macOS / Linux

---

## セットアップ手順

### Step 1: Discord Bot の作成

#### 1.1 Discord Developer Portal へアクセス

```
https://discord.com/developers/applications
```

#### 1.2 新規 Application を作成

- **「New Application」** をクリック
- 名前を入力（例：`Hermes Agent`）
- **「Create」** をクリック

#### 1.3 Bot を追加

左メニューから **「Bot」** → **「Add Bot」** をクリック

#### 1.4 Bot Token をリセット・コピー

1. **「Bot」** タブの **「TOKEN」** セクションを探す
2. **「Reset Token」** をクリック（確認が出たら Yes）
3. **「Copy」** をクリック
4. トークンをメモ（後で使用）

#### 1.5 Privileged Gateway Intents を有効化

**「Bot」** タブで以下をオン（トグル）にする：

```
☑ Presence Intent
☑ Server Members Intent
☑ Message Content Intent
```

#### 1.6 OAuth2 スコープと権限を設定

**「OAuth2」→「URL Generator」** に移動：

**Scopes:**
```
☑ bot
```

**Bot Permissions:**
```
☑ Send Messages
☑ Read Messages/View Channels
☑ Embed Links
☑ Attach Files
☑ Read Message History
```

#### 1.7 Bot を Discord サーバーに招待

URL Generator で生成された URL をコピー → ブラウザで開く

```
https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=117760&scope=bot
```

- Discord のポップアップで **サーバーを選択**
- **「認可」** をクリック

---

### Step 2: Hermes Gateway 設定

#### 2.1 Discord Token を .env に設定

```bash
# Hermes の .env ファイルを開く
notepad C:\Users\[ユーザー名]\AppData\Local\hermes\.env
```

以下を追加：

```bash
# =============================================================================
# DISCORD INTEGRATION
# =============================================================================
DISCORD_BOT_TOKEN=<Step 1.4 でコピーした Bot Token をここに貼り付け>
```

**保存して閉じる**

#### 2.1b Grok 認証の設定（SuperGrok ユーザー推奨）

**SuperGrok Subscription をお持ちの場合：**

以下のコマンドで確認：

```bash
hermes model
```

もし以下のように表示されれば、**XAI_API_KEY は不要**です：

```
Current model:    grok-4.3
Active provider:  xAI Grok OAuth (SuperGrok Subscription)
```

この場合、`.env` ファイルに `XAI_API_KEY` を追加する必要はありません。

> 💡 **メリット：**
> - API キー管理が不要
> - SuperGrok Subscription の利用枠内で全機能が使える
> - 追加課金なし
> - 複数プラットフォーム（Discord、Telegram、Slack など）で同じサブスク利用可能

**API キー認証の場合：**

もし `Active provider` が `OpenRouter API` などの場合は、`.env` に `XAI_API_KEY` を追加してください：

```bash
XAI_API_KEY=<xai-から始まるAPIキー>
```

#### 2.2 Hermes Gateway を起動

```bash
hermes gateway run
```

**期待される出力：**

```
⚕ Hermes Gateway Starting...
Messaging platforms + cron scheduler
Press Ctrl+C to stop

WARNING gateway.platforms.discord: Opus codec not found — voice channel playback disabled
✓ discord connected
✓ Gateway ready
```

> 💡 Opus codec not found は無視してOK（ボイスチャネル機能が不要な場合）

---

### Step 3: Discord でテスト

Discord サーバーで Hermes Bot にメッセージを送信：

```
@Hermes こんにちは
```

**期待される応答：**

```
こんにちは！👋
何かお手伝いできることはありますか？
```

---

### Step 4: ホームチャネル設定（オプション）

初回メッセージで以下が表示される場合：

```
No home channel is set for Discord. 
A home channel is where Hermes delivers cron job results 
and cross-platform messages.
Type /sethome to make this chat your home channel.
```

以下を実行：

```
/sethome
```

これでこのチャネルが Hermes のホームチャネルになります。

---

## トラブルシューティング

### 問題: Bot が応答しない

#### 原因 1: Token が無効

**エラーメッセージ：**
```
discord.errors.LoginFailure('Improper token has been passed.')
401 Unauthorized
```

**解決方法：**

1. Discord Developer Portal で **新しい Token を再生成**
2. `.env` ファイルを更新
3. Hermes Gateway を再起動

```bash
hermes gateway restart
```

#### 原因 2: Bot がサーバーに招待されていない

**確認方法：**
- Discord のメンバーリストに Hermes Bot が表示されているか確認
- 表示されない場合は、Step 1.7 の OAuth2 招待 URL を再度使用

#### 原因 3: Bot に権限がない

**確認方法：**
1. Discord サーバー設定 → ロール → Hermes Bot のロールを確認
2. 以下の権限があるか確認：
   - メッセージを送信
   - メッセージ履歴を読む
   - リンクを埋め込み

### 問題: Gateway が起動しない

**エラーメッセージ：**
```
ERROR gateway.run: ✗ discord error: discord connect timed out after 30s
```

**解決方法：**

1. Token が正しいか確認
2. 既に実行中のプロセスを停止

```bash
hermes gateway stop
Start-Sleep -Seconds 2
hermes gateway run
```

### 問題: 画像や動画が生成できない

**エラーメッセージ：**
```
FAL_KEY is not set
```

**解決方法：**

FAL API キーを設定：

```bash
# FAL API キーを取得
# https://www.fal.ai/ でサインアップ

# Hermes に設定
hermes config set fal.api_key YOUR_FAL_API_KEY
```

---

## 使用可能な機能

### 現在利用可能

| 機能 | 説明 | 例 |
|------|------|-----|
| 🔍 **Web Search** | 最新情報をネットで検索 | `@Hermes 2026年のAI技術トレンドを検索して` |
| 🐦 **X-Search** | Twitter/X の投稿を検索 | `@Hermes SpaceX IPO について最新ツイートを探して` |
| 💬 **テキスト生成** | Grok で応答生成 | `@Hermes Pythonについて教えて` |
| ⚙️ **コード実行** | Python コードを実行 | `@Hermes print("Hello")を実行して` |
| 📊 **データ分析** | CSV・JSON を分析 | `@Hermes このデータの傾向を分析して` |
| 📄 **ファイル処理** | テキスト・PDF を処理 | ファイルをアップロード → 分析依頼 |
| 🧠 **メモリ機能** | 会話履歴を記憶 | 複数ターンの会話が可能 |
| 🌐 **多言語対応** | 日本語を含む多言語 | `@Hermes ...` (日本語で送信) |

### 設定で利用可能

| 機能 | 状態 | 必要な設定 |
|------|------|-----------|
| 🖼️ **画像生成** | ❌ 未設定 | `FAL_API_KEY` が必要 |
| 🎬 **動画生成** | ❌ 未設定 | `FAL_API_KEY` が必要 |
| 🎤 **音声入力** | ❌ 未設定 | OpenAI STT キーが必要 |

---

## 使用例

### 例 1: Web Search で最新ニュースを取得

```
@Hermes 2026年5月のテクノロジーニューストップ3を検索して要約して
```

**応答例：**
```
最新のテクノロジーニュース3つ：

1. 【AI開発】OpenAI が GPT-5 のプレビューを発表
   ...

2. 【スペーステック】SpaceX の IPO 計画が発表
   ...

3. 【量子コンピューティング】Google が新量子チップを開発
   ...
```

### 例 2: X-Search で特定トピックの投稿を検索

```
@Hermes @elonmusk の最新ツイート5件を X-Search で探して
```

**応答例：**
```
🐦 x_search: "@elonmusk latest tweets"

1. [ツイート1の内容と要約]
2. [ツイート2の内容と要約]
3. [ツイート3の内容と要約]
...
```

### 例 3: コードを実行して結果を取得

```
@Hermes このPythonコードを実行して：
import random
numbers = [random.randint(1, 100) for _ in range(5)]
print(f"平均: {sum(numbers)/len(numbers)}")
```

**応答例：**
```
コード実行結果：
平均: 67.4

実行されたコード：
import random
numbers = [random.randint(1, 100) for _ in range(5)]
print(f"平均: {sum(numbers)/len(numbers)}")
```

### 例 4: 複数ターンの会話

```
@Hermes AI について教えて

@Hermes 具体的に何ができるのか詳しく

@Hermes その中で最も重要なのは？
```

会話コンテキストが保持されるため、複数のターンでやり取りできます。

---

## 自動起動設定

### Windows での自動起動

Hermes Gateway を Windows サービスとして登録し、PC 起動時に自動で起動させることができます。

#### 方法 1: systemd/サービスとして登録（推奨）

```bash
# 管理者権限で PowerShell を開く

# Hermes Gateway をサービスに登録
hermes gateway install

# ステータス確認
Get-Service hermes-gateway

# 自動起動を有効化
Set-Service hermes-gateway -StartupType Automatic

# サービス開始
Start-Service hermes-gateway
```

#### 方法 2: タスクスケジューラで登録

1. Windows タスクスケジューラを開く
2. タスク作成 → 新規タスク
3. **「トリガー」** → PC 起動時に実行
4. **「操作」** → `hermes gateway run` を実行

---

## ベストプラクティス

### 効率的な使用方法

```bash
# ✅ 具体的で詳細なプロンプト
@Hermes SpaceX の 2026年6月 IPO について、
X-Search で最新の投稿 3 つを検索して、
それぞれの要点を日本語で要約して

# ❌ 曖昧なプロンプト
@Hermes SpaceX について
```

### ロング・コンテキスト対応

Hermes は 90 ターンまでの会話履歴を保持します：

```
@Hermes [質問 1]
@Hermes [質問 2 - 質問 1 のコンテキストを活用]
@Hermes [質問 3 - 質問 1, 2 のコンテキストを活用]
```

### エラーハンドリング

エラーが出た場合は、以下を確認：

1. Token が有効か
2. ネットワークが接続しているか
3. API キーが設定されているか

```bash
# 設定確認
hermes config show

# ログ確認
hermes gateway run  # フォアグラウンドで実行してログを見る

```

Hermesのグローバル側.env設定は
Get-Content C:\Users\Setona\AppData\Local\hermes\.env
=============================================================================
# DISCORD INTEGRATION
=============================================================================
DISCORD_BOT_TOKEN=<Discord Bot Token>のみでOK
# ※ XAI_API_KEY は削除OK
# すでに hermes model で xAI Grok OAuth が設定済みのため不要

---

## 参考リンク

- [Hermes Agent 公式](https://github.com/hermesai/hermes)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [xAI Grok API](https://api.x.ai/)
- [FAL.ai](https://www.fal.ai/)

---

## 更新履歴

| 日付 | 変更内容 |
|------|---------|
| 2026-05-21 | 初版作成 |

---

**最終確認日**: 2026-05-21  
**ステータス**: ✅ 全機能動作確認済み
