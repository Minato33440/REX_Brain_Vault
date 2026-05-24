# Grok OAuth 設定手順 & Claude 切り替え方法

Hermes Agent で **Grok (xAI)** を使う最新の方法と、**Claude** への切り替え方法をまとめました。
SuperGrok サブスクリプションを持っている場合は、**OAuth方式** が最も推奨です。

## 0. 
- 公式に案内されている方法だと上手くいかないことがあるので、一度ダウンロードしてから実行
- Invoke-WebRequest -Uri "https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.ps1" -OutFile ".\install.ps1"
- Unblock-File .\install.ps1
- powershell.exe -ExecutionPolicy Bypass -File .\install.ps1
- １（クイックセットアップ）
- どのモデルを使うか：8
- 

## 1. Grok OAuth 設定手順 (SuperGrok ユーザー向け)

### 前提条件
- Hermes Agent がインストール済み
- **SuperGrok** サブスクリプションが有効
- ブラウザが使える環境

### 設定ステップ

1. ターミナルで以下のコマンドを実行
   ```bash
   hermes model
   ```

2. プロバイダー一覧から **xAI Grok OAuth (SuperGrok Subscription)** を選択

3. ブラウザが自勗で開き、 **accounts.x.ai** のログイン画面が出ます
   - SuperGrok アカウントでログイン

4. 認証完了後、Hermes に戻ると設定が完了

5. 確認
   ```bash
   hermes
   ```
   Grok モデルが使えるようになります。

### 利点
- **XAI_API_KEY 不要**
- **追加のAPI従量課金無し** (既存のSuperGrokサブスク内で使用)
- X検索やリアルタイム機能も利用可能

### 注意点
- オースス・プレミアム+でも使用可能
- おかしなエラー (403等) が出た場合は、以下のAPIキー方式へ切り替える

## 2. 例外： XAI_API_KEY を使う方法 (従量課金が発生)

```bash
# ~/.hermes/.env に設定
XAI_API_KEY= xai-...
```

`hermes model` で **xAI (Grok)** を選択

## 3. Claude への切り替え方法

### 方法A: Anthropic 直接 (OAuth or API Key)
1. `hermes model` を実行
2. **Anthropic** または **Claude** 関連プロバイダーを選択
3. OAuthログインまたはAPIキーを入力

### 方法B: OpenRouter 経由 (Claude 3.5 Sonnet / Opus 等)
1. OpenRouter APIキーを設定
2. `hermes model` で OpenRouter を選択
3. モデルで `anthropic/claude-3.5-sonnet` または `anthropic/claude-opus-4` を指定

### セッション中の切り替え
- チャット内で `/model` コマンドを使用してモデルを切り替え可能な場合があります

## 4. 実用テクニック

- **Grok 優先** で使い始める場合
  ```bash
  hermes model
  # xAI Grok OAuth (SuperGrok Subscription) を選択
  ```

- **Claude 優先** にしたい場合
  ```bash
  hermes model
  # Anthropic または OpenRouter + claude モデルを選択
  ```

- 両方を使い切り替えたい場合
  - プロバイダーを複数設定しておき、`hermes model` で随時切り替え
  - サブエージェントやスケジュールで使い切り替えることも可能

## 5. トラブルシューティング

| エラー | 対策 |
|----------|--------|
| OAuthログイン後 403 | XAI_API_KEY を設定して xAI プロバイダーへ切り替え |
| Claudeが出ない | OpenRouterを使うまたは Anthropic APIキーを確認 |
| モデル切り替えが出てこない | `hermes model` を再実行してプロバイダーを再設定 |

---

**Tips**: このノートをObsidianで編集しておくと、Hermesが自勗生成したスキルと一緒に管理できます。

最終更新: 2026-05-20