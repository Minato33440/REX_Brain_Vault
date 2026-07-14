# Hermes profiles/broker 新設と Discord-Bot 個別 Gateway 接続 構築メモ

**作成日**: 2026-07-14  
**対象環境**: REX_AI 環境（Windows 11 / Hermes-Agent v0.16.0）  
**目的**: 既存 `claude` プロファイルと同一の権限・Skill を保ったまま、別 Discord-Bot トークンで独立した Gateway を並行稼働させる（Hermes-Runtime-Hub 運用の一環）

> ⚠️ このファイルは人間側がチェックする構築資料。実機検証した内容のみ記載。トークン等の秘匿値は含めない。

---

## 概要

`profiles/claude/` を丸ごとコピーして `profiles/broker/` を新設し、`.env` の `DISCORD_BOT_TOKEN` のみ別 Bot に差し替えることで、**claude・gpt・broker の 3 Gateway を同時並行稼働**させた。

```
Hermes (HERMES_HOME = C:\Users\Setona\AppData\Local\hermes)
├── profiles/claude   → PID 38484  (claude-opus-4-8 / Discord Bot-A)  ← Desktop MCP bridge 既定
├── profiles/gpt      → PID 20352  (gpt-5.5)
└── profiles/broker   → PID 41392  (claude-sonnet-5 / Discord Bot-B)  ← 今回新設
```

Discord Bot は**外向き WebSocket 接続**なのでローカルポートのバインドが無く、**別 Bot トークンさえ使えばポート衝突なしで何本でも並行起動できる**のが要点。

---

## 1. 構築手順（実施済み）

### 1-1. プロファイル複製
`profiles/claude/` → `profiles/broker/`（手動フォルダコピー）。

### 1-2. プロファイル名は「小文字英数字」必須
- Hermes のプロファイル名規約は **lowercase, alphanumeric**。
- 当初 `Broker`（大文字始まり）で作成したため `hermes profile list` に出なかった（`profile show` は Windows の大小無視で通ってしまい紛らわしい）。
- → ディレクトリ名を **`broker`** にリネームして解決。`profile list` に正しく表示された。

### 1-3. Discord Bot トークン差し替え
- `profiles/broker/.env` の `DISCORD_BOT_TOKEN` を **別 Bot** の値に設定済み（claude 用とは別物であることを指紋比較で確認）。
- 同一トークンだと Discord 側でセッション衝突するため、**プロファイルごとに必ず別 Bot** にすること。

### 1-4. コピー由来の「古い状態ファイル」を除去（重要）
コピー元 claude の**稼働中の状態ファイル**がそのまま入っていたので削除した。これを消さないと「既に起動済み」と誤認したり、他プロファイルの PID を指したまま挙動が壊れる。

削除したファイル（`profiles/broker/` 配下）:
```
gateway.pid           ← claude の PID 38484 を指していた
gateway.lock          ← 同上
gateway_state.json    ← 同上（discord: connected 状態のコピー）
state.db-shm          ← claude 稼働中 DB の SQLite サイドカー
state.db-wal          ← 同上（0 バイトで保留なし → 削除安全）
```
- `state.db` **本体は残す**（権限・Skill・セッション状態を claude から継承する目的）。
- `gateway/discord_command_sync_state.json` は無害（新 Bot 側で再同期される）ため保持。

---

## 2. Gateway 起動方法

### 2-1. プロファイル指定は `--profile`（= `-p`）フラグ
```powershell
hermes --profile broker gateway status
hermes -p broker -z "..."           # 短縮形も可
```
- ⚠️ **`hermes --help` の usage 行に `--profile` は載っていない**が、プリパースで**実際に効く隠しグローバルフラグ**。実機で `--profile broker` が broker の Gateway(37656/41392) を、`--profile claude` が claude(38484) を正しく対象にすることを確認済み。
- ⚠️ **`HERMES_PROFILE` 環境変数は効かない**。プロファイル指定は必ず `--profile` フラグで行う。

### 2-2. `active_profile` ファイルとの関係
- `HERMES_HOME/active_profile`（`hermes profile use <name>` で設定）は、`--profile` を省いたコマンドの既定プロファイルを決めるだけ。
- `--profile` を明示すれば `active_profile` を切り替える必要はない。
- **Gateway は「起動時の active_profile／--profile」にバインドされ、以後プロセスが独立保持される**。だから claude・gpt・broker が同時に running でいられる（active_profile は 1 個でも複数 Gateway が別プロファイルで動く）。

### 2-3. `gateway run` と `gateway start` の違い
| コマンド | 実体 | 用途 |
|---|---|---|
| `hermes -p broker gateway run` | フォアグラウンド常駐 | ターミナル/セッション終了で落ちる。手動・検証向け |
| `hermes -p broker gateway install` | Windows スケジュールタスク登録（初回のみ） | 常駐サービス化 |
| `hermes -p broker gateway start` / `stop` / `restart` | インストール済みサービスの管理 | **Runtime-Hub 常駐運用の本命** |

**常駐運用の推奨手順**:
```powershell
hermes -p broker gateway install   # 初回のみ（ログイン時自動起動登録）
hermes -p broker gateway start
```

---

## 3. 注意点

1. **`.env` のプロファイル固有値の見直し**  
   `DISCORD_HOME_CHANNEL` / `DISCORD_HOME_CHANNEL_THREAD_ID` は **claude のチャンネルのままコピー**されている。broker Bot を別チャンネルで運用するなら要書き換え（`DISCORD_BOT_TOKEN` は差し替え済み）。

2. **`gateway start --all` は使わない**  
   `--all` は「**全プロファイルの stale Gateway を kill してから起動**」。broker 単体操作で付けると claude(38484)・gpt(20352) も巻き込む。

3. **`active_profile` の巻き戻り**  
   フォアグラウンド `gateway run` を supervisor 付きで起動 → ラッパー終了(SIGTERM/exit15)時に子が `--replace` で自動再起動し、その際 `active_profile` が broker に書き換わる事象を観測。Desktop MCP bridge は claude 既定を前提とするため、運用後は `hermes profile use claude` で戻すこと（サービス化すればこの往復は不要）。

4. **モデル既定**  
   broker の `config.yaml` は `default: claude-sonnet-5 / provider: anthropic`（claude は opus-4-8）。Provider は claude(anthropic) のままで問題なし。

---

## 4. 検証結果

```
hermes gateway list
  ✗ default   — not running
  ✗ ai        — not running
  ✓ broker    — PID 41392   (discord: connected)
  ✓ claude    — PID 38484   (current)
  ✓ gpt       — PID 20352
  ✗ grok      — not running
```
- broker `gateway_state.json`: `state: running` / `platforms.discord.state: connected` を確認。
- `hermes -p broker doctor`: 「broker: gateway running, claude-sonnet-5」で健全。Skills 72（claude と同数）。

---

## 付録: `-z` ランタイムテスト失敗の切り分け（本構築とは別問題）

`hermes -p broker -z "モデル確認テスト"` が `no final response was produced` で失敗したが、**broker の設定不良ではない**。

- **同じ `-z` が claude プロファイルでも同一エラー**で失敗（英語 ASCII でも失敗＝日本語デコードは無関係）。
- 握り潰されていた実エラーは **profile 側ログ** `profiles/claude/sessions/request_dump_*.json` に記録されていた:
  ```
  HTTP 400 invalid_request_error
  "You have reached your specified API usage limits.
   You will regain access on 2026-08-01 at 00:00 UTC."
  (model: claude-opus-4-8 / request_id: req_011Cd1dwNvVTPkBrPHBTuWki)
  ```
- **原因**: Hermes の anthropic 認証は **OAuth（`api.anthropic.com` 経由）** で、その**API 側の使用上限に到達**。復帰 2026-08-01 00:00 UTC。
- **影響範囲**: 同一 OAuth 認証を使う **claude・broker 両プロファイルの anthropic 推論（`-z`・ACP・Gateway 返信）が 8/1 まで停止**。gpt/grok は別プロバイダのため影響なし。
- **切り分けの含意**: Hermes（ACP/Gateway/`-z` すべて）は **API 経由**でモデルを叩くため API 使用上限に従う。一方で対話型 **Claude Code は別枠で稼働継続**（同一枠かは Anthropic 内部仕様のため未確定）。
- **対処**: `console.anthropic.com → Usage / Limits` で上限・残量・リセット日を確認。上限引き上げ or 8/1 待ち、当面は gpt/grok プロバイダへ一時ルーティングも可。

---

## 参考リンク（同 Vault 内）
- `raw/Hermes-Agent_Plugin_ACP構成.md` — VSCode Hermes プラグイン ACP 接続構成
- `raw/discord_bot_setup_guide.md` / `raw/Discord_Grok_Bot_Setup.md` — Discord Bot セットアップ
- `raw/Grok_OAuth_Bridge_Architecture.md` — OAuth ブリッジ構成
