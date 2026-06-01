# Claude Code モデル設定メモ

最終整理: 2026-06-01

---

## 1. 結論（普段の運用）

| やりたいこと | 方法 | 適用範囲 |
|---|---|---|
| 一時的にモデル切替 | チャット欄に `/model opus` | そのセッション |
| 恒久デフォルト化 | `settings.json` の `"model"` | 永続 |
| 起動時にメニュー選択 | `/config` → Model | 永続 |

- **現状の設定**: `~/.claude/settings.json` に `"model": "opus"`（最新 Opus 追従＝今は 4.8）。
- `opus` はファミリーエイリアス。将来 Opus 4.9 等が出たら自動でそちらになる。バージョン固定したい時だけ `"claude-opus-4-8"` と書く。

> **重要な仕様**: `/model opus` は「セッション切替」だけでなく **`~/.claude/settings.json` への永続化も同時に行う**。
> → `/model opus` を一度打てば、それだけで恒久デフォルトが Opus になる（既存の env / permissions / hooks / theme はマージ保持される）。

---

## 2. VS Code 拡張ではエイリアス・起動フラグが効かない

`claude-solo --model claude-opus-4-8` のようなターミナル流のコマンドは **VS Code 拡張では通用しない**。

理由:
- エイリアス（`claude-teams` / `claude-solo`）は PowerShell プロファイル（`$PROFILE`）や `.bashrc` に定義されている。
- それが効くのは **手でターミナルを開いて対話的に打つ時だけ**。
- VS Code 拡張はシェルを噛まず、拡張プロセスから `claude` バイナリを直接 spawn する → エイリアス定義を読む機会がそもそも無い。
- 同じ理由で `--model` などの起動フラグも拡張の起動経路では渡せない。

→ **VS Code 拡張でのモデル指定は `/model`・`/config`・`settings.json` の3択。**

---

## 3. ターミナル CLI での起動（エイリアス運用）

PowerShell プロファイル（`C:\Users\Setona\Documents\PowerShell\Microsoft.PowerShell_profile.ps1`）に定義済み。`@args` で引数をそのまま渡す構造なので、`--model` を併記するだけでよい（ファイル変更不要）。

```powershell
claude-teams                          # Agent Teams ON ・ デフォルト(Sonnet 4.6)で起動
claude-solo                           # Agent Teams OFF ・ デフォルト(Sonnet 4.6)で起動
claude-teams --model claude-opus-4-8  # Teams で Opus 4.8
claude-solo  --model claude-opus-4-8  # Solo で Opus 4.8
claude --model claude-opus-4-8 --remote-control          # Solo でリモート
claude-teams --model claude-opus-4-8 --remote-control     # Teams でリモート
```

- `--model` を省略すれば従来どおりデフォルト（Sonnet 4.6）で起動。

---

## 4. 優先順位（高 → 低）

| 順位 | 方法 | 構文 |
|---|---|---|
| 1（最高・上書き可） | セッション内 `/model` | チャット欄に `/model opus` |
| 2 | CLI フラグ | `claude --model claude-opus-4-8` |
| 3 | 環境変数 | `ANTHROPIC_MODEL=claude-opus-4-8` |
| 4 | プロジェクトローカル設定 | `.claude/settings.local.json` |
| 5 | プロジェクト共有設定 | `.claude/settings.json` |
| 6 | ユーザー設定 | `~/.claude/settings.json` |

---

## 5. settings.json のスコープ

**Claude Code 専用の設定ファイル**（VS Code の settings.json とは別物）。リポジトリ内に置けば Desktop・CLI・VS Code 拡張すべてのクライアントで共通して読まれる。

| スコープ | パス | 効果 |
|---|---|---|
| グローバル | `~/.claude/settings.json`（=`C:\Users\Setona\.claude\settings.json`） | 全プロジェクト共通 |
| プロジェクト共有 | `<repo>/.claude/settings.json` | そのプロジェクト専用（グローバルより優先） |
| プロジェクトローカル | `<repo>/.claude/settings.local.json` | 個人用・gitignore 推奨 |

恒久変更の記入例（`~/.claude/settings.json`）:
```json
{
  "model": "opus"
}
```

---

## 6. モデルID一覧

| モデル | ID | エイリアス |
|---|---|---|
| Opus 4.8 | `claude-opus-4-8` | `opus` |
| Sonnet 4.6 | `claude-sonnet-4-6` | `sonnet` |
| Haiku 4.5 | `claude-haiku-4-5-20251001` | `haiku` |

---
---

# 付録: その他の運用メモ

> ※ ここから下はモデル設定とは別トピック。元ファイルから保全。

## A. インストール / アップデート

```cmd
:: Windows CMD: インストール
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```
- インストール先: `C:\Users\Setona\.local\bin\claude.exe`
- バージョン確認: `claude --version`

## B. REMOTE_CONTROL の起動

```powershell
claude --remote-control
```
起動すると表示される:
```
/remote-control is active. Code in CLI or at
https://claude.ai/code/session_XXXXXXXXXXXXXXXX
```
ブランチ状態確認: `git branch -a | Select-String "claude"`

## C. メモリシステム（MEMORY.md）

- 保存場所: `C:\Users\Setona\.claude\projects\<ローカルパス由来の名前>\memory\MEMORY.md`
- 会話開始時に**自動ロード**される（要点記憶媒体）。
- 紐づくのは **GitHub リポジトリではなくローカルパス**。

| 条件 | 自動ロード |
|---|---|
| 同じパスで新しいチャット | ✅ |
| GitHub で新リポジトリ作成（ローカルパス同じ） | ✅ |
| 別パスに移動・リネーム | ❌（memory フォルダを新パス配下へコピー要） |

## D. RTK（Rust Token Killer）

すべてのターミナルコマンドは `rtk` プレフィックスを付ける。

```bash
# ✅ 正しい
rtk git status
rtk git add logs/gm/weekly/...
rtk git commit -m "msg"
rtk git push origin main
python main.py --trade --news   # python は rtk 対象外（パススルー）
```

## E. 思考フラグの使い分け

| フラグ | 用途 |
|---|---|
| `think hard` / `Extra` | 複雑なシステム開発 |
| `/effort max` | より複雑な開発・デバッグの多く |
| `ultrathink` | アーキテクチャ全体に影響する変更 |
| `/effort ultracode` | 大規模並列コードベース（xhigh 推論 + 自動ワークフローオーケストレーション） |
