# Role Registry

REX_AI システムのAIロール登録簿(現在の状態)。

最終更新: 2026-04-27  
管轄: `Wiki-Eval`

> 本ファイルは「現在の登録状態」を記録する。決定の理由・権限定義は [adr/ADR-Role.md](../adr/ADR-Role.md) を参照。

---

## アクティブロール

| 起動コード | ロール名 | 担当領域 | 主担当リポ | 担当NLM | 状態 |
|---|---|---|---|---|---|
| `Wiki-Eval` | 統括Evaluator | 全リポ統括・ADR管轄・Vault運用 | 全リポ | REX_Wiki_Vault | 稼働中 |
| `Wiki-trade` | Trade_System Planner+ClaudeCode | Trade_System リポ専属 | Trade_System | REX_System_Brain | 稼働中 |
| `Wiki-brain` | Trade_Brain Planner+ClaudeCode | Trade_Brain リポ専属 | Trade_Brain | REX_Trade_Brain | 稼働中 |
| `Wiki-hp` | Setona_HP Planner+ClaudeCode | Setona_HP リポ専属 | Setona_HP | REX_HP_Brain | **構築予定** |
| `Wiki-casual` | Casual-Planner (Advisor兼任) | 雑談・横断知見・REX_AI全体相談役 | REX_Brain_Vault (casual/) | REX_Casual_Brain | 稼働中 |

---

## Casual と Advisor の役割分担

両者とも `Wiki-casual` 起動コードで動作:

- **Casual**: 一般会話における広範囲にわたる知見
- **Advisor**: REX_AI 全システムにおける相談役

蓄積先は同じく REX_Casual_Brain NLM。Advisor用の独立リポ・NLMは作成しない方針。

---

## 権限マトリクス概要

詳細権限は [adr/ADR-Role.md](../adr/ADR-Role.md) "権限マトリクス" 参照。

| ロール | ADR読込 | ADR書込 | pending書込 | registry書込 | リポ書込 | NLM書込 |
|---|---|---|---|---|---|---|
| Wiki-Eval | ✅ | ✅ | ✅(全) | ✅ | ✅(全) | ✅(REX_Wiki_Vault のみ) |
| Wiki-trade | ✅ | ❌ | ✅(自領域) | ❌ | ✅(Trade_System) | ✅(REX_System_Brain のみ) |
| Wiki-brain | ✅ | ❌ | ✅(自領域) | ❌ | ✅(Trade_Brain) | ✅(REX_Trade_Brain のみ) |
| Wiki-hp | ✅ | ❌ | ✅(自領域) | ❌ | ✅(Setona_HP) | ✅(REX_HP_Brain のみ・構築後) |
| Wiki-casual | ✅ | ❌ | ✅(casual) | ❌ | ✅(casual/ + pending/casual) | ✅(REX_Casual_Brain のみ) |

> **NLM 1:1原則**: 各ロールは担当NLM以外への投入・クエリ禁止(詳細: [adr/ADR-NLM.md](../adr/ADR-NLM.md))

---

## ロール任命の原則

**起動コードのみがロールを決定する。** プラットフォーム(Claude.ai / Claude Desktop / Claude Code 等)はロール任命に関与しない。

詳細: [adr/ADR-Role.md](../adr/ADR-Role.md) "プラットフォーム非依存原則"

---

## Plannerの実装兼用ルール

`Wiki-trade` / `Wiki-brain` / `Wiki-hp` は Planner + ClaudeCode 兼用:

- **軽微な実装** (Cursorローカル作業): フラグなしで実行可
- **重要な実装** (新Phase着手・凍結ファイル周辺・新規ADR採番を伴う変更): 起動コードフラグ付与で統一性を保つ

---

## 廃止ロール

| ロール名 | 廃止日 | 経緯 |
|---|---|---|
| (現時点なし) | - | - |

---

## 構築予定ロール

| 起動コード | ロール名 | 構築開始条件 |
|---|---|---|
| `Wiki-hp` | Setona_HP Planner+ClaudeCode | ボス判断 + REX_HP_Brain NLM作成 + STARTUP_CODES.md 改訂 |

詳細フロー: [adr/ADR-Role.md](../adr/ADR-Role.md) "Wiki-hp 構築予定の取り扱い"

---

## 更新ルール

- **更新権限**: `Wiki-Eval` のみ
- **更新タイミング**:
  - ロール新規追加時(ADR-Role 改訂と同時)
  - ロール廃止時(ADR-Role 改訂と同時)
  - 権限変更時(ADR-Role 改訂と同時)
- **更新方法**: GitHub MCP 経由のみ (ADR-Vault 遵守)
