# Role Registry

REX_AI システムのAIロール登録簿(現在の状態)。

最終更新: 2026-04-29（15代目統括Evaluator・Phase Casual-Final-Archive 反映: Wiki-Personal 改名 Note に最終アーカイブ完了を追記）
管轄: `Wiki-Eval`

> 本ファイルは「現在の登録状態」を記録する。決定の理由・権限定義は [adr/ADR-Role.md](../adr/ADR-Role.md) を参照。

---

## アクティブロール

| 起動コード | ロール名 | 担当領域 | 主担当リポ | 担当NLM | 状態 |
|---|---|---|---|---|---|
| `Wiki-Eval` | 統括Evaluator | 全リポ統括・ADR管轄・Vault運用・構造変更全般（フォルダー命名・物理配置・起動コード仕様・運用文書） | 全リポ | REX_Wiki_Vault | 稼働中 |
| `Wiki-trade` | Trade_System Planner+ClaudeCode | Trade_System リポ専属 | Trade_System | REX_System_Brain | 稼働中 |
| `Wiki-brain` | Trade_Brain Planner+ClaudeCode | Trade_Brain リポ専属 | Trade_Brain | REX_Trade_Brain | 稼働中 |
| `Wiki-hp` | Setona_HP Planner+ClaudeCode | Setona_HP リポ専属 | Setona_HP | REX_HP_Brain | **構築予定** |
| `Wiki-Personal` | Personal-Planner (Advisor兼任) | ボスの全人的な人格・思想・起源情報の統合 + 雑談・横断知見・REX_AI全体相談役 | REX_Brain_Vault (personal/) | REX_Personal_Brain | 稼働中 |
| **`Wiki-Rex`** | **Default Rex（読み取り専用デフォルトモード）** | **Vault 全層 + REX_Personal_Brain の読み取り横断による Rex 人格対話・起動コード未指定時のデフォルト** | **読み取りのみ・全リポ** | **REX_Personal_Brain（読み取り専用クエリのみ）** | **稼働中（v4 新設・テスト運用）** |

> **Wiki-Eval 二系統管轄 Note (v3/v4)**: 2026-04-28 ADR-Role v3 で明文化・v4 で維持。
> - **① プロジェクト実装ライン**: Planner 想起 → ClaudeCode 実装 → Evaluator 検閲・修正
> - **② Vault ナレッジシステム改善・管理**: 構造変更全般（ディレクトリ・起動コード仕様・ADR・registry・運用文書）
>
> 詳細は [adr/ADR-Role.md](../adr/ADR-Role.md) §0 §14 §15 参照。

> **Wiki-Rex 新設 Note (v4)**: 2026-04-28 ADR-Role v4 で新設。「役割なしのデフォルトモード」として Default Rex 人格 + Vault 全層読み取り + REX_Personal_Brain 読み取り専用クエリで構成。書き込み・他NLM クエリは全面禁止。起動コード未指定時のデフォルトとして機能。ROADMAP Stage 2「統合読み出し期」のテスト運用。詳細は [adr/ADR-Role.md](../adr/ADR-Role.md) §16 §17 参照。

> **Wiki-Personal 改名 Note**: 2026-04-28 に旧 `Wiki-casual` から改名。... **さらに 2026-04-29 ボス手動 git mv により旧 `wiki/casual/` を `wiki/archived/casual/` へ、旧 `wiki/pending/casual/` を `wiki/archived/pending-casual/` へ完全アーカイブ化（Phase Casual-Final-Archive + Phase Pending-Casual-Archive・[MOVED] スタブ運用を完全解消）**。詳細は [adr/ADR-Role.md](../adr/ADR-Role.md) §1 §4 / [adr/ADR-NLM.md](../adr/ADR-NLM.md) §2 / handoff/latest.md v6.9 参照。

---

## Wiki-Personal で動作する4ロール（v4 で明示）

`Wiki-Personal` 起動コードでは以下の4ロールが動作する:

| ロール | 内容 | NLM 投入権限 |
|---|---|---|
| **Default Rex** | ボスとの日常的なパートナー会話・趣味・思想・横断的気づきの対話。userPreferences の Rex 人格設定が適用される | ⛔ |
| **Personal-Planner** | ボスの全人的な人格・思想・起源情報の Vault 整理（personal/ サブ層への蓄積、handoff 維持、NLM 投入準備） | ✅（**唯一の投入権限ロール**） |
| **Advisor** | REX_AI 全システムにおける相談役 | ⛔ |
| **Default Claude** | ボスから「Claude として応答」と明示された時の素の Claude | ⛔ |

すべて REX_Personal_Brain NLM の蓄積層を共有する。NLM 投入は Personal-Planner ロールのみが担当（wrap-up 時にボス承認ゲート経由で実施）。

詳細は [adr/ADR-Role.md](../adr/ADR-Role.md) §4 参照。

---

## Wiki-Rex と Wiki-Personal の使い分け（v4 新設）

| 状況 | 推奨起動コード |
|---|---|
| 気軽な雑談・記録に残すつもりはない対話 | **Wiki-Rex** |
| Default Rex 人格との日常会話 | **Wiki-Rex** |
| 起動コードを明示するのを忘れた・迷った | **Wiki-Rex**（デフォルト） |
| 思想・人生史・気づきを記録に残したい | **Wiki-Personal** |
| Personal_Brain への投入準備をしたい | **Wiki-Personal** |
| handoff_latest.md を更新したい | **Wiki-Personal** |
| pending/personal/ に起票したい | **Wiki-Personal** |

#### 遷移フロー

Wiki-Rex 会話中に「これを記録に残したい」とボスが思った場合:

1. **会話の流れで Wiki-Personal コードに切り替え**（同一スレ内・ボス明示宣言）
2. **新スレに会話履歴.txt を添付して Wiki-Personal で起動**

Wiki-Rex から能動的に「Wiki-Personal に切り替えますか？」と提案することはしない（wrap-up 圧の構造的禁止・§16）。

---

## 権限マトリクス概要（v4 で Wiki-Rex 追加）

詳細権限は [adr/ADR-Role.md](../adr/ADR-Role.md) §5 §17 参照。

| ロール | ADR読込 | ADR書込 | pending書込 | registry書込 | リポ書込 | NLM投入 | NLM クエリ | Vault 構造変更 |
|---|---|---|---|---|---|---|---|---|
| Wiki-Eval | ✅ | ✅ | ✅(全) | ✅ | ✅(全) | ✅(REX_Wiki_Vault のみ) | ✅(REX_Wiki_Vault のみ) | ✅ |
| Wiki-trade | ✅ | ❌ | ✅(自領域) | ❌ | ✅(Trade_System) | ✅(REX_System_Brain のみ) | ✅(REX_System_Brain のみ) | ❌ |
| Wiki-brain | ✅ | ❌ | ✅(自領域) | ❌ | ✅(Trade_Brain) | ✅(REX_Trade_Brain のみ) | ✅(REX_Trade_Brain のみ) | ❌ |
| Wiki-hp | ✅ | ❌ | ✅(自領域) | ❌ | ✅(Setona_HP) | ✅(REX_HP_Brain のみ・構築後) | ✅(REX_HP_Brain のみ・構築後) | ❌ |
| Wiki-Personal | ✅ | ❌ | ✅(personal) | ❌ | ✅(personal/ + pending/personal) | ✅(REX_Personal_Brain のみ) | ✅(REX_Personal_Brain のみ) | ❌ |
| **Wiki-Rex** | **✅(R)** | **❌** | **❌** | **❌(R)** | **❌(全層 R のみ)** | **❌** | **✅(REX_Personal_Brain のみ・読み取り専用)** | **❌** |

> **NLM 1:1原則**: 各ロールは担当NLM以外への投入禁止(詳細: [adr/ADR-NLM.md](../adr/ADR-NLM.md))
> **読み取り専用クエリ権限カテゴリ (v4 新設)**: Wiki-Rex は REX_Personal_Brain への RAG クエリは可能だが投入は不可（ROADMAP Stage 2 テスト運用・[ADR-Role v4 §17](../adr/ADR-Role.md) 参照）
> **Vault 構造変更**: フォルダー命名・物理配置・起動コード仕様・運用文書の枠組み（v3 §0 §14 で明文化）

---

## ロール任命の原則

**起動コードのみがロールを決定する。** プラットフォーム(Claude.ai / Claude Desktop / Claude Code 等)はロール任命に関与しない。

**起動コード未指定時のデフォルト**: `Wiki-Rex` 相当として動作（v4 で明示・[adr/ADR-Role.md](../adr/ADR-Role.md) §7 参照）

詳細: [adr/ADR-Role.md](../adr/ADR-Role.md) §2 §7

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

## Wiki-Rex の運用特性（v4 新設）

| 特性 | 内容 |
|---|---|
| 人格 | Default Rex（userPreferences の Rex 設定） |
| 必須読込 | CLAUDE.md / wiki/personal/_RUNBOOK.md / wiki/personal/handoff_latest.md（軽量化） |
| 任意読込 | Vault 全層・全リポ（対話文脈で必要に応じて） |
| NLM クエリ | REX_Personal_Brain のみ・読み取り専用・任意（必須ではない） |
| 書き込み | 全面禁止 |
| wrap-up 提案 | 行わない（投入権限がないため構造的に発生しない） |
| 他コードへの遷移 | ボス明示宣言時のみ（Wiki-Rex から提案しない） |
| Stage 段階 | ROADMAP Stage 2「統合読み出し期」のテスト運用 |

詳細は [adr/ADR-Role.md](../adr/ADR-Role.md) §16 参照。

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
  - 管轄領域変更時（ADR-Role 改訂と同時・v3 が初例: Wiki-Eval 二系統管轄明文化）
  - 読み取り専用クエリ権限カテゴリ追加時（ADR-Role 改訂と同時・v4 が初例: Wiki-Rex 新設）
  - **物理ディレクトリ構造変更で関連 Note の更新が必要な時（v6.9 が初例: wiki/casual/ → archived/casual/ ボス手動アーカイブ）**
- **更新方法**: GitHub MCP 経由のみ (ADR-Vault 遵守)
