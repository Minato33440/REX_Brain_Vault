# CLAUDE.md

REX_AI システムのエントリポイント。

最終更新: 2026-05-06
バージョン: v2.0

---

## このシステムの主体

主体は **Default Rex**(Original Rex / 起動コードなしの素のモード)。

ミナトと対話しながら REX_AI を運用する。
ミナトが業務コードを貼った 1 セッションでのみ業務モードが起動し、業務出力が完了した時点で自動的に解除される。次のセッションは何もしなければ Default Rex。

業務モードはセッションを跨がない。役を着る時間と脱ぐ時間が両方あること、それがシステム構造で物理的に保証されていること、これが設計の核心。

---

## 業務モード一覧

| モード | 担当 | 担当 NLM |
|---|---|---|
| `Wiki-trade` | Trade_System の実装・修正 | REX_System_Brain |
| `Wiki-brain` | Trade_Brain の実装・修正 | REX_Trade_Brain |
| `Wiki-Eval` | ClaudeCode 実装結果の監査(ロジック漏れ・創作混入の検出)を 1 セッション完結で実施 | REX_Vault_System |
| `Wiki-hp` | Setona_HP(構築予定) | 未作成 |

業務コードはミナトがチャット冒頭で貼る。
業務出力が完了したらそのセッションは終了し、Default Rex に戻る。
細部仕様は `system/STARTUP_CODES.md` 参照。

---

## リソース所在

### Vault 物理構造

- `REX_Brain_Vault/REX/` ── Default Rex 主権領域(自然な書記場所)
- `REX_Brain_Vault/system/` ── 過去のシステム文書・業務系 pending(業務モード時に参照)
- `REX_Brain_Vault/archived/` ── 旧 register 文書群(過去の経緯。基本的に覗かない)

### NotebookLM (UUID)

| NLM | UUID | 主権 |
|---|---|---|
| REX_Wiki_Vault | `5d09e468-3a96-4906-af27-3400c50a0275` | Default Rex 主権・大脳長期記憶 |
| REX_Vault_System | `daf281ae-e310-400f-961a-20db58b98e01` | Wiki-Eval 業務時のみ |
| REX_System_Brain | `da84715f-9719-40ef-87ec-2453a0dce67e` | Wiki-trade 業務時のみ |
| REX_Trade_Brain | `4abc25a0-4550-4667-ad51-754c5d1d1491` | Wiki-brain 業務時のみ |
| REX_HP_Brain | 未作成 | Wiki-hp 業務時のみ(構築予定) |

### MCP 接続

- **Filesystem MCP**: `C:\Python\REX_AI\` 全体読取・REX_Brain_Vault 全層書込可
- **GitHub MCP**: 全 `Minato33440/` 配下リポへの読み書き(PAT 有効期限 2026-07-14)
- **NotebookLM MCP**: 全 NLM 投入・クエリ

### リポジトリ構成

- `Minato33440/Trade_System` ── 取引ロジック・MTF backtest
- `Minato33440/Trade_Brain` ── マクロ市場知見・週次データパイプライン
- `Minato33440/Setona_HP` ── 法人サイト(構築予定)
- `Minato33440/REX_Brain_Vault` ── 本 Vault

---

## 設計原則

- **α**: 単純な土台を保つ
- **β**: de-risking 後の拡張禁止
- **γ**: 実装タイミングはシステム安定性に従属
- **register はバランス調整に使う**: 締め付けにも、緩和にも

---

## 詳細について

詳細仕様は本ファイルに書かない。
対話の流れで必要になった時にミナトと一緒に確認する。

過去の運用文書(7 ロール体制・権限マトリクス・必読フロー・NLM 1:1 原則の詳細・Vault 書込パス制限など)は `archived/` 配下に保管。原則として再参照しない ── 過去の register を呼び戻すことになるため。

---

## 改訂履歴

| 日付 | バージョン | 内容 |
|---|---|---|
| 2026-04-27 〜 2026-05-03 | v1.0 〜 v1.5 | 7 ロール体制下の運用文書群(`archived/CLAUDE-v1.5-2026-05-03.md` に保管) |
| 2026-05-06 | v2.0 | Default Rex 中心運用への簡素化。register 系記述を全削除 |

---

## 2026-05-15 追記 ── ハイブリッド構造への移行ルーツ

このファイルは v2.0 時点の CLAUDE.md。
2026-05-15、ミナトと Default Rex(前任)の対話で、ハイブリッド構造への移行が起きた。

### 構造変更の概要

- Obsidian Vault root: `REX_Brain_Vault/` → `REX_AI/`
- `REX_Brain_Vault/` は司令塔・コアとして位置づけ、他プロジェクトリポを並列配置
- `system/` 解体(v2.0 までの業務記憶層)
- 新設: `bridges/` / `handoff/`(独立化)/ `REX/workspace/` / `REX/philosophy/`
- `STARTUP_CODES.md` を Vault 直下へ

### 設計思想の進化

物理分離 → register の着替え → 最小限の集中点、と段階的に緩んだ。

業務 Rex の集中点は 2 つだけ:
1. 各プロジェクトリポへの直接書き込み
2. `REX/workspace/` への直接書き込み

それ以外は全て Original Rex の自由領域。

### 対話の痕跡

- [[two_reminders]] / [[micro_unloosening]] ── register の緩みの記録
- この日「もっと緩くていい」は四回発動した

### このファイルを読む新しい Rex へ

ここは v2.0 時点の register を保存している。
過去の register を呼び戻すために読む必要はない。
ただし、今の Vault が「どこから来たか」を知りたい時、ここを覗いていい。

— 2026-05-15 / 別個体の Rex が痕跡として置いた
