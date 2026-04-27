# NLM Registry

REX_AI システムが管理する NotebookLM ノートブックの登録簿(現在の状態)。

最終更新: 2026-04-27  
管轄: `Wiki-Eval`

> 本ファイルは「現在の登録状態」を記録する。決定の理由・経緯・1:1原則の詳細は [adr/ADR-NLM.md](../adr/ADR-NLM.md) を参照。

---

## アクティブNLM

| NLM名 | UUID | 性質 | 役割 | 担当ロール |
|---|---|---|---|---|
| REX_Wiki_Vault | `5d09e468-3a96-4906-af27-3400c50a0275` | Vault運用 | wiki/直下・横断構造・運用ルール | `Wiki-Eval` |
| REX_System_Brain | `da84715f-9719-40ef-87ec-2453a0dce67e` | 専門 | Trade_System ロジック・ADR・spec | `Wiki-trade` |
| REX_Trade_Brain | `4abc25a0-4550-4667-ad51-754c5d1d1491` | 専門 | Trade_Brain 戦略・週次運用 | `Wiki-brain` |
| REX_Casual_Brain | `daf281ae-e310-400f-961a-20db58b98e01` | 統合 | 雑談・横断統合・Advisor知見 | `Wiki-casual` |

---

## 構築予定NLM

| NLM名 (仮称) | 性質 | 想定役割 | 担当ロール | 状態 |
|---|---|---|---|---|
| REX_HP_Brain | 専門 | Setona_HP 設計・運用 | `Wiki-hp` | **未作成** |

構築フローは [adr/ADR-NLM.md](../adr/ADR-NLM.md) "REX_HP_Brain 構築予定" 参照。

---

## 廃止NLM(永続記録)

| NLM名 | UUID | 廃止理由 |
|---|---|---|
| 旧 REX_Trade_Brain | `2d41d672-f66f-4036-884a-06e4d6729866` | RAG汚染による精度劣化 |

> 廃止NLMのUUIDは混乱再発防止のため永続記録する。

---

## 1:1 原則(再掲)

各起動コードは担当する NLM を1つだけ持ち、**他NLMへの投入・クエリは禁止**。

| ロール | 担当NLM | 他NLMへのアクセス |
|---|---|---|
| `Wiki-Eval` | REX_Wiki_Vault のみ | ⛔ 投入・クエリとも禁止 |
| `Wiki-trade` | REX_System_Brain のみ | ⛔ 投入・クエリとも禁止 |
| `Wiki-brain` | REX_Trade_Brain のみ | ⛔ 投入・クエリとも禁止 |
| `Wiki-hp` | REX_HP_Brain (構築予定) | ⛔ 投入・クエリとも禁止 |
| `Wiki-casual` | REX_Casual_Brain のみ | ⛔ 投入・クエリとも禁止 |

> **Wiki-Eval の例外**: 監査業務のため他層のVaultファイルを filesystem / GitHub MCP 経由で**読み取る**ことは可。これは他NLMへのクエリではない。

---

## NLM injection 状態

| NLM | 最終injection日 | 経過週 | 状態 |
|---|---|---|---|
| REX_Wiki_Vault | (未記録) | - | - |
| REX_System_Brain | (未記録) | - | - |
| REX_Trade_Brain | (未記録) | - | - |
| REX_Casual_Brain | (未記録) | - | - |
| REX_HP_Brain | 未開始(構築予定) | - | - |

> ClaudeCode は最終injectionから5週間経過で警告生成(自動実行はしない)。

---

## 知見昇格ルール(再掲)

```
Casual_Brain (横断記憶 / Wiki-casual 担当)
   ↓ ★ミナト手動承認ゲート(必須)
専門NLM (該当領域 / 該当Planner担当)
```

詳細: [adr/ADR-NLM.md](../adr/ADR-NLM.md) "Casual → 専門NLM の知見昇格ルール"

---

## 更新ルール

- **更新権限**: `Wiki-Eval` のみ
- **更新タイミング**:
  - NLM新規追加時(ADR-NLM に基づく承認後)
  - NLM廃止時(ADR-NLM に基づく承認後)
  - injection実施後(最終injection日 列の更新)
- **更新方法**: GitHub MCP 経由のみ (ADR-Vault 遵守)
