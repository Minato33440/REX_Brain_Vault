# NLM Registry

REX_AI システムが管理する NotebookLM ノートブックの登録簿(現在の状態)。

最終更新: 2026-04-29（v6.9 / Phase Casual-Final-Archive: Wiki-Rex 読み取り専用クエリ例外を 1:1 原則表に反映・Origin 注記を v3/v4 参照に更新）
管轄: `Wiki-Eval`

> 本ファイルは「現在の登録状態」を記録する。決定の理由・経緯・1:1原則の詳細は [adr/ADR-NLM.md](../adr/ADR-NLM.md) を参照。

---

## アクティブNLM

| NLM名 | UUID | 性質 | 役割 | 担当ロール |
|---|---|---|---|---|
| REX_Wiki_Vault | `5d09e468-3a96-4906-af27-3400c50a0275` | Vault運用 | wiki/直下・横断構造・運用ルール | `Wiki-Eval` |
| REX_System_Brain | `da84715f-9719-40ef-87ec-2453a0dce67e` | 専門 | Trade_System ロジック・ADR・spec | `Wiki-trade` |
| REX_Trade_Brain | `4abc25a0-4550-4667-ad51-754c5d1d1491` | 専門 | Trade_Brain 戦略・週次運用 | `Wiki-brain` |
| **REX_Personal_Brain** | `daf281ae-e310-400f-961a-20db58b98e01` | 統合 | **ボスの全人的な人格・思想・起源情報の統合 + 雑談・横断統合・Advisor知見** | `Wiki-Personal`（投入＋クエリ）/ **`Wiki-Rex`（読み取り専用クエリ・v4 新設）** |

> **REX_Personal_Brain 改名 Note**: 2026-04-28 に旧 `REX_Casual_Brain` から表示名変更。**UUID は不変**（`daf281ae-e310-400f-961a-20db58b98e01`）。NotebookLM Web UI でノートブック表示名を変更するボス手動操作のみ（Step 5）。`notebooklm-mcp-cli` 設定の更新は不要（UUID 参照で動作）。詳細は [adr/ADR-NLM.md](../adr/ADR-NLM.md) v2 参照。

> **Wiki-Rex 読み取り専用クエリ例外 Note (v4 新設)**: 2026-04-28 ADR-Role v4 で新設された「読み取り専用クエリ権限カテゴリ」により、Wiki-Rex は REX_Personal_Brain への RAG クエリが可能（投入は不可）。ROADMAP Stage 2「統合読み出し期」のテスト運用。詳細は [adr/ADR-Role.md](../adr/ADR-Role.md) §16 §17 参照。

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

> **REX_Casual_Brain は廃止記録に含めない**: REX_Casual_Brain → REX_Personal_Brain は **改名であり廃止ではない**。同一 UUID（`daf281ae-...`）のノートブックの表示名変更のみ。データ・履歴・投入内容はすべて継承される。詳細は [adr/ADR-NLM.md](../adr/ADR-NLM.md) v2 §7 参照。

---

## 1:1 原則(再掲・v4 で読み取り専用クエリ例外を反映)

各起動コードは担当する NLM を1つだけ持ち、**他NLMへの投入は禁止**。

| ロール | 担当NLM（投入＋クエリ） | 読み取り専用クエリ例外 |
|---|---|---|
| `Wiki-Eval` | REX_Wiki_Vault のみ | （他層 Vault ファイルの filesystem 読み取りは可・NLM クエリではない） |
| `Wiki-trade` | REX_System_Brain のみ | なし |
| `Wiki-brain` | REX_Trade_Brain のみ | なし |
| `Wiki-hp` | REX_HP_Brain (構築予定) | なし |
| `Wiki-Personal` | REX_Personal_Brain のみ | なし |
| **`Wiki-Rex`** | **なし（投入権限なし）** | **REX_Personal_Brain への読み取り専用クエリのみ可（v4 新設・[ADR-Role v4 §17](../adr/ADR-Role.md) 参照）** |

> **Wiki-Eval の例外（ファイル読み取り）**: 監査業務のため他層のVaultファイルを filesystem / GitHub MCP 経由で**読み取る**ことは可。これは他NLMへのクエリではない。
>
> **Wiki-Rex の例外（NLM 読み取り専用クエリ）**: ROADMAP Stage 2「統合読み出し期」のテスト運用として、REX_Personal_Brain への RAG クエリが可能。投入は不可。「投入権限分業を維持しつつ、想起統合を別レイヤーで段階的に設計する」設計指針の最初の実装。

---

## NLM injection 状態

| NLM | 最終injection日 | 経過週 | 状態 |
|---|---|---|---|
| REX_Wiki_Vault | (未記録) | - | - |
| REX_System_Brain | (未記録) | - | - |
| REX_Trade_Brain | (未記録) | - | - |
| **REX_Personal_Brain** | (未記録) | - | - |
| REX_HP_Brain | 未開始(構築予定) | - | - |

> ClaudeCode は最終injectionから5週間経過で警告生成(自動実行はしない)。

---

## 知見昇格ルール(再掲)

```
Personal_Brain (横断記憶 + 人格付与情報 / Wiki-Personal 担当)
   ↓ ★ミナト手動承認ゲート(必須)
専門NLM (該当領域 / 該当Planner担当)
```

詳細: [adr/ADR-NLM.md](../adr/ADR-NLM.md) "Personal → 専門NLM の知見昇格ルール"

---

## 思想強制リスクの構造的解消（v3/v4 注記・v6.9 で参照更新）

ボスの Origin 情報は **Wiki-Personal / Wiki-Rex 起動時のメンタルマネージメント・価値観文脈においてのみ** Rex が参照する。Trade 判断・実装業務での参照は禁止（NLM 1:1 原則と起動コード物理分離により構造的に保証）。

**v4 補強**: Wiki-Rex も Origin 情報を参照する可能性がある（Personal_Brain 読み取り専用クエリ）。Wiki-Personal と同等の文脈限定原則の下で運用される（Trade 判断ロールでは Wiki-Rex も使用しない・ボスの裁量で起動コードを切り替える）。

詳細: [adr/ADR-Role.md](../adr/ADR-Role.md) v4 §13 / [adr/ADR-NLM.md](../adr/ADR-NLM.md) v2 §5

---

## 更新ルール

- **更新権限**: `Wiki-Eval` のみ
- **更新タイミング**:
  - NLM新規追加時(ADR-NLM に基づく承認後)
  - NLM廃止時(ADR-NLM に基づく承認後)
  - NLM 表示名変更時（ADR-NLM 改訂と同時・本 v2 が初例）
  - **読み取り専用クエリ権限カテゴリ追加時（ADR-Role 改訂と同時・v4 が初例: Wiki-Rex 新設）**
  - injection実施後(最終injection日 列の更新)
- **更新方法**: GitHub MCP 経由のみ (ADR-Vault 遵守)
