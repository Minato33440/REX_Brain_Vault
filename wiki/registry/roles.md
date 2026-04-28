# Role Registry

REX_AI システムのAIロール登録簿(現在の状態)。

最終更新: 2026-04-28（15代目統括Evaluator）  
管轄: `Wiki-Eval`

> 本ファイルは「現在の登録状態」を記録する。決定の理由・権限定義は [adr/ADR-Role.md](../adr/ADR-Role.md) を参照。

---

## アクティブロール

| 起動コード | ロール名 | 担当領域 | 主担当リポ | 担当NLM | 状態 |
|---|---|---|---|---|---|
| `Wiki-Eval` | 統括Evaluator | **全リポ統括・ADR管轄・Vault運用・構造変更全般（フォルダー命名・物理配置・起動コード仕様・運用文書）** | 全リポ | REX_Wiki_Vault | 稼働中 |
| `Wiki-trade` | Trade_System Planner+ClaudeCode | Trade_System リポ専属 | Trade_System | REX_System_Brain | 稼働中 |
| `Wiki-brain` | Trade_Brain Planner+ClaudeCode | Trade_Brain リポ専属 | Trade_Brain | REX_Trade_Brain | 稼働中 |
| `Wiki-hp` | Setona_HP Planner+ClaudeCode | Setona_HP リポ専属 | Setona_HP | REX_HP_Brain | **構築予定** |
| `Wiki-Personal` | Personal-Planner (Advisor兼任) | ボスの全人的な人格・思想・起源情報の統合 + 雑談・横断知見・REX_AI全体相談役 | REX_Brain_Vault (personal/) | REX_Personal_Brain | 稼働中 |

> **Wiki-Eval 二系統管轄 Note (v3)**: 2026-04-28 ADR-Role v3 で明文化。
> - **① プロジェクト実装ライン**: Planner 想起 → ClaudeCode 実装 → Evaluator 検閲・修正
> - **② Vault ナレッジシステム改善・管理**: 構造変更全般（ディレクトリ・起動コード仕様・ADR・registry・運用文書）
>
> 詳細は [adr/ADR-Role.md](../adr/ADR-Role.md) §0 §14 §15 参照。

> **Wiki-Personal 改名 Note**: 2026-04-28 に旧 `Wiki-casual` から改名。NLM 表示名 `REX_Casual_Brain` → `REX_Personal_Brain`（UUID `daf281ae-...` 不変）。Vault 物理ディレクトリ `wiki/casual/` → `wiki/personal/` への移行は別タスク（Step 4）。詳細は [adr/ADR-Role.md](../adr/ADR-Role.md) §1 §4 / [adr/ADR-NLM.md](../adr/ADR-NLM.md) §2 参照。

---

## Personal と Advisor の役割分担

両者とも `Wiki-Personal` 起動コードで動作:

- **Personal**: ボスの全人的な人格・思想・起源情報の統合（射程: 日常/思想/起源/横断メタファー）
- **Advisor**: REX_AI 全システムにおける相談役

蓄積先は同じく REX_Personal_Brain NLM。Advisor用の独立リポ・NLMは作成しない方針。

詳細は [adr/ADR-Role.md](../adr/ADR-Role.md) §4 参照。

---

## 権限マトリクス概要

詳細権限は [adr/ADR-Role.md](../adr/ADR-Role.md) §5 参照。

| ロール | ADR読込 | ADR書込 | pending書込 | registry書込 | リポ書込 | NLM書込 | **Vault 構造変更** |
|---|---|---|---|---|---|---|---|
| Wiki-Eval | ✅ | ✅ | ✅(全) | ✅ | ✅(全) | ✅(REX_Wiki_Vault のみ) | **✅** |
| Wiki-trade | ✅ | ❌ | ✅(自領域) | ❌ | ✅(Trade_System) | ✅(REX_System_Brain のみ) | ❌ |
| Wiki-brain | ✅ | ❌ | ✅(自領域) | ❌ | ✅(Trade_Brain) | ✅(REX_Trade_Brain のみ) | ❌ |
| Wiki-hp | ✅ | ❌ | ✅(自領域) | ❌ | ✅(Setona_HP) | ✅(REX_HP_Brain のみ・構築後) | ❌ |
| Wiki-Personal | ✅ | ❌ | ✅(personal) | ❌ | ✅(personal/ + pending/personal) | ✅(REX_Personal_Brain のみ) | ❌ |

> **NLM 1:1原則**: 各ロールは担当NLM以外への投入・クエリ禁止(詳細: [adr/ADR-NLM.md](../adr/ADR-NLM.md))
> **Vault 構造変更**: フォルダー命名・物理配置・起動コード仕様・運用文書の枠組み（v3 §0 §14 で明文化）

---

## ロール任命の原則

**起動コードのみがロールを決定する。** プラットフォーム(Claude.ai / Claude Desktop / Claude Code 等)はロール任命に関与しない。

詳細: [adr/ADR-Role.md](../adr/ADR-Role.md) §2

---

## Plannerの実装兼用ルール

`Wiki-trade` / `Wiki-brain` / `Wiki-hp` は Planner + ClaudeCode 兼用:

- **軽微な実装** (Cursorローカル作業): フラグなしで実行可
- **重要な実装** (新Phase着手・凍結ファイル周辺・新規ADR採番を伴う変更): 起動コードフラグ付与で統一性を保つ

---

## Personal-Planner の運用責任

Personal-Planner は人格付与情報の蓄積を担当するが、その運用には特別な責任が伴う:

| 主体 | 責任範囲 |
|---|---|
| **Personal-Planner** | Personal_Brain への投入主担当・サブ層運用・handoff 維持・サブ層内コンテンツ起草 |
| **Wiki-Eval** | 構造整合性監査（**人格内容には介入しない**・思想強制の禁忌を守る）+ personal/ ディレクトリ構造の保守 |
| **ボス** | `wiki/philosophy/minato_core.md` の完全コントロール / Personal_Brain への投入はボス判断ゲート経由で承認 |

詳細は [adr/ADR-Role.md](../adr/ADR-Role.md) §13 参照。

---

## 廃止ロール

| ロール名 | 廃止日 | 経緯 |
|---|---|---|
| (現時点なし) | - | - |

> Wiki-casual は廃止ではなく Wiki-Personal への改名（射程拡大を伴う supersede）であるため本表には含まない。

---

## 構築予定ロール

| 起動コード | ロール名 | 構築開始条件 |
|---|---|---|
| `Wiki-hp` | Setona_HP Planner+ClaudeCode | ボス判断 + REX_HP_Brain NLM作成 + STARTUP_CODES.md 改訂（**v3 §12 訂正により Wiki-Eval 直接実施**） |

詳細フロー: [adr/ADR-Role.md](../adr/ADR-Role.md) §11

---

## 更新ルール

- **更新権限**: `Wiki-Eval` のみ
- **更新タイミング**:
  - ロール新規追加時(ADR-Role 改訂と同時)
  - ロール廃止時(ADR-Role 改訂と同時)
  - 権限変更時(ADR-Role 改訂と同時)
  - ロール改名時（ADR-Role 改訂と同時）
  - **管轄領域変更時（ADR-Role 改訂と同時・v3 が初例: Wiki-Eval 二系統管轄明文化）**
- **更新方法**: GitHub MCP 経由のみ (ADR-Vault 遵守)
