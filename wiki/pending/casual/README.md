# pending/casual/

`Wiki-casual` (Casual-Planner / Advisor兼任) の仮決定記録ディレクトリ。

## 用途

雑談・横断知見・REX_AI全体への所感や提案をここに記録する。

### Casual と Advisor の役割分担

両者とも `Wiki-casual` 起動コードで動作:

- **Casual**: 一般会話における広範囲にわたる知見
- **Advisor**: REX_AI 全システムにおける相談役

### 記録対象例

- ADR-Role / ADR-Repo / ADR-Vault / ADR-NLM への改訂提案
- CLAUDE.md / STARTUP_CODES.md への改訂提案
- 横断的な気づき・メタファー・哲学的考察
- 専門NLMへの昇格候補(ミナト承認ゲート前の起票)

## ファイル命名

```
YYYY-MM-DD_<topic>.md
```

特殊用途:
- `CLAUDE_md_revision_<date>.md` — CLAUDE.md 改訂提案
- `STARTUP_CODES_revision_<date>.md` — STARTUP_CODES.md 改訂提案
- `nlm_promotion_<topic>_<date>.md` — Casual_Brain → 専門NLM 昇格提案

## 記録権限

- 書込: `Wiki-casual` / `Wiki-Eval`(レビューコメント追記)
- 読込: `Wiki-Eval` / `Wiki-casual`

## レビュー

`Wiki-Eval` が週次またはセッション開始時にレビューし、ADR昇格判定を行う。

## NLM 昇格ゲート

専門NLMへの知見昇格は **ミナト手動承認ゲート必須**(ADR-NLM "Casual → 専門NLM の知見昇格ルール" 参照)。
