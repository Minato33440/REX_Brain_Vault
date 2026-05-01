# pending/personal/

`Wiki-Personal` (Personal-Planner / Advisor 兼任) の仮決定記録ディレクトリ。

旧 `pending/casual/` から 2026-04-28 に物理移行（15代目 Wiki-Eval 実施）。

## 用途

雑談・横断知見・REX_AI 全体への所感や提案、および **ボスの全人的な人格・思想・起源情報の統合** に関する仮決定をここに記録する。

### Personal と Advisor の役割分担

両者とも `Wiki-Personal` 起動コードで動作:

- **Personal**: ボスの全人的な人格・思想・起源情報の統合（射程: 日常/思想/起源/横断メタファー）
- **Advisor**: REX_AI 全システムにおける相談役

### 記録対象例

- ADR-Role / ADR-Repo / ADR-Vault / ADR-NLM への改訂提案
- 横断的な気づき・メタファー・哲学的考察
- 専門 NLM への昇格候補（ボス承認ゲート前の起票）
- _RUNBOOK.md / handoff_latest.md / 各サブ層内コンテンツ起草

### Wiki-Eval 管轄との境界（ADR-Role v3 §14）

以下は **Wiki-Eval が直接実施**（pending/personal/ への起票不要）:
- STARTUP_CODES.md 改訂（起動コード仕様 = Vault 横断構造）
- CLAUDE.md 改訂（単一エントリポイント）
- ADR 体系の改訂
- registry 同期
- ディレクトリ命名・物理配置

以下は **Personal-Planner 業務**（pending/personal/ で議論）:
- _RUNBOOK.md の中身（運用ルール記述）
- サブ層内コンテンツ起草（usual/invent/mind/origin/insights 各ファイル）
- 人格・思想・起源情報の編集

## ファイル命名

```
YYYY-MM-DD_<topic>.md
```

## 記録権限

- 書込: `Wiki-Personal` / `Wiki-Eval`(レビューコメント追記)
- 読込: `Wiki-Eval` / `Wiki-Personal`

## レビュー

`Wiki-Eval` がセッション開始時にレビューし、ADR 昇格判定を行う。

## NLM 昇格ゲート

専門 NLM への知見昇格は **ボス手動承認ゲート必須**（ADR-NLM §5「Personal → 専門 NLM の知見昇格ルール」参照）。

---

> **15代目 Wiki-Eval Migration Note (2026-04-28)**: 旧 `wiki/pending/casual/README.md` を本パスに物理移設し、ADR-Role v3 §14 構造変更/中身変更の境界線を反映する形で内容を更新した。これは Wiki-Eval 管轄文書（pending ディレクトリ運用ルール）であるため、Wiki-Eval 直接編集の対象（ADR-Role v3 §14 例外的中身介入）。
