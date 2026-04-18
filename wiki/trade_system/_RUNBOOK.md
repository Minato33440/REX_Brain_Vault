# _RUNBOOK.md — Trade_System Wiki 運用ガイド
# Planner / Evaluator / ClaudeCode 向け

---

## このWikiの目的

Trade_Systemの設計知識を構造化し、新セッションで即座に辿れるようにする。
NLMが「検索エンジン」なら、Wikiは「整理された本棚」。

---

## ページ種別

| ディレクトリ | 内容 | 誰が書くか |
|---|---|---|
| concepts/ | 設計概念（neck, window, ダウ等） | ClaudeCode提案 → Evaluator承認 |
| entities/ | ファイル・関数の仕様 | ClaudeCode自動 |
| patterns/ | 戦略パターン（DB, IHS, ASCENDING） | ClaudeCode提案 → Evaluator承認 |
| bug_patterns/ | ADR A〜Dの個別ページ | ClaudeCode提案 → Evaluator承認 |
| decisions/ | ADR Eの個別ページ | Evaluator作成 |
| sources/ | 設計文書の要約 | ClaudeCode自動 |

---

## フロントマター（全ページ共通・必須3フィールド）

```yaml
---
type: concept | entity | pattern | bug_pattern | decision | source
status: active | archived | frozen
last_updated: 2026-04-18
---
```

種別固有のフィールドは任意。段階的に充実させる。

---

## 迷ったときの参照先

```
概念・用途の定義    → concepts/
過去の判断の理由    → decisions/
同じバグを踏まないか → bug_patterns/
ファイルの依存関係   → entities/
大量ソース検索      → NLM（@notebooklm-mcp）
パラメータ確定値    → Trade_System/.CLAUDE.md
```

---

## Source-of-Truth 原則

Wikiは docs/ の「整理された解釈層」。新しい事実を発明してはならない。

```
Source of Truth:
  コード実装     → src/*.py
  設計文書       → docs/EX_DESIGN_CONFIRMED.md
  意思決定       → docs/ADR.md
  パラメータ     → .CLAUDE.md

Wikiの役割:
  上記から派生した構造化知識。Sourceが更新されたらWikiが追従する。
```
