# Grok Build IDE — マルチモーダル運用まとめ

最終更新: 2026-06-12

---

## 1. Grok Build IDE（VS Code）でのマルチモーダル

追加の MCP や vault-mcp は不要。SuperGrok ログイン済みなら、**サイドバーの Grok エージェント**がネイティブで画像を扱える。

### 画像の入力方法（Windows）

| 方法 | 操作 |
|------|------|
| ドラッグ＆ドロップ | エクスプローラーからプロンプトへ画像をドロップ |
| ファイル貼り付け | ファイルをコピーして `Ctrl+V` |
| スクリーンショット貼り付け | **`Alt+V`**（Windows 専用） |
| パス参照 | `@images/1.jpg` や絶対パスをテキストで指定 |

`Alt+V` は Grok 固有。通常の `Ctrl+V` はテキストのみで、画像クリップボードは落ちる。

### 画像生成・編集

- `/imagine <説明>` — テキストから画像生成
- エージェントツール: `image_gen`（新規）、`image_edit`（既存画像の編集）
- `imagine` スキルが `grok inspect` に表示済み

### ACP エージェント（このチャット）との違い

**このチャットから `.jpg` を直接「見る」ことはできない。** `Read` ツールも `Cannot read binary files of type jpg` で拒否される。

小説の挿絵比較などは、次のいずれかを使う:

1. **Grok サイドバーに画像チップを貼る**（`Alt+V` または D&D）— いちばん手軽
2. **Hermes CLI ワンショット**（下記 §3）— ACP からシェル経由で画像解析
3. **`grok-oauth` MCP の `ask_grok`** — Hermes vision ツールセット経由

---

## 2. Hermes Vision 404 の原因と修正

### 原因

`profiles/grok/config.yaml` の auxiliary vision が廃止モデルを指していた。

```yaml
# 修正前（404 の原因）
auxiliary:
  vision:
    provider: xai-oauth
    model: grok-vision-beta   # 存在しない / アクセス不可
```

メインチャットは `grok-4.3`（マルチモーダル対応）なのに、vision ツールだけ別モデルを呼んでいた。

### 修正（適用済み）

`profiles/grok/config.yaml` と `profiles/ai/config.yaml`:

```yaml
auxiliary:
  vision:
    provider: auto
    model: ''
```

| 設定 | 意味 |
|------|------|
| `provider: auto` | メインプロバイダを自動採用 |
| `model: ''` | vision 用モデルを上書きしない → 同じ config の **`model.default`（現状 `grok-4.3`）** を使う |

「xAI の最新モデルに常時追従」ではなく、**プロファイルのメインモデルに追従**する設定。

### grok-oauth MCP

`ask_grok` / `grok_work` は Hermes の `vision` ツールセット経由。プロンプトに**絶対パス**を含める。

```
vision_analyzeで C:\Python\REX_AI\Grok_Vault\REX\Ai\Novel-Hidden_desires\images\9.jpg を1文で説明
```

`grok_oauth_bridge.py` は `-p grok` を明示（`profile use grok` は HERMES_HOME=ルート時に失敗しうるため廃止）。

---

## 3. Hermes CLI 経由の検証（ワンショット画像解析）

ACP エージェントが画像を直接読めないとき、**Hermes を CLI で叩いてワンショット解析**する。  
成功例の「制服姿の少年が…」は **このチャットのビジョンではなく**、以下コマンドの stdout である。

### 前提

- Hermes インストール済み（`C:\Users\Setona\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exe`）
- `profiles/grok` に xAI OAuth 認証済み
- vision 設定は §2 の修正済み状態

### 基本コマンド（PowerShell / cmd）

```powershell
C:\Users\Setona\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exe `
  -p grok `
  -z "vision_analyzeで C:\path\to\image.jpg を日本語1文で説明して" `
  -t vision `
  --accept-hooks
```

### フラグの意味

| フラグ | 役割 |
|--------|------|
| `-p grok` | `profiles/grok` の OAuth・config を使う |
| `-z "..."` | ワンショットプロンプト（対話なし） |
| `-t vision` | `vision_analyze` ツールセットを有効化 |
| `--accept-hooks` | フック承認待ちでハングしない（headless 用） |

### 動作確認（疎通のみ）

```powershell
hermes -p grok -z "PONGとだけ返答" --accept-hooks
# → PONG
```

### 画像解析の例（Hidden_desires）

```powershell
hermes -p grok -z "vision_analyzeで C:\Python\REX_AI\Grok_Vault\REX\Ai\Novel-Hidden_desires\images\9.jpg を1文で説明" -t vision --accept-hooks
```

**検証結果（2026-06-12）**

| テスト | 結果 |
|--------|------|
| 修正前 `9.jpg` | `grok-vision-beta` 404 |
| 修正後 `9.jpg` | Hermes stdout: 「制服姿の少年が窓辺で本を熱心に読んでいるアニメ風イラストです。」 |
| 再試行 | 一時的に "model unavailable"（API 側の可能性あり） |

### エージェントから実行するとき

Grok Build エージェントは `run_terminal_command` で上記を実行し、**stdout をユーザーに転記**する。  
エージェント自身が画像を見たわけではない点を明記すること。

### Skill

同じ手順は Grok Skill `hermes-vision-cli`（`~/.grok/skills/hermes-vision-cli/`）にも保存済み。  
トリガー: 画像解析、vision_analyze、Hermes vision、挿絵比較（CLI 経由）など。

---

## 4. 推奨ワークフロー（小説 + 挿絵）

| 用途 | 推奨ルート |
|------|-----------|
| 章の推敲・校正 | Grok Build + `novel-rough-iteration` |
| 挿絵の雰囲気比較・批評 | Grok サイドバーに画像チップ（`Alt+V` / D&D） |
| ACP から画像を解析したい | Hermes CLI ワンショット（§3）または `grok-oauth` |
| X 検索・市況ヘッドライン | `grok-oauth` の `ask_grok`（x_search） |

---

## 5. モデル経路の整理

| 経路 | モデル |
|------|--------|
| Grok Build サイドバー（画像チップ） | `grok-build`（デフォルト） |
| Hermes `profiles/grok`（vision_analyze / CLI / MCP） | `grok-4.3`（`model.default`） |

別ルートなので混同しないこと。