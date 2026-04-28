# ADR-Role: Roles and Permissions

**Status**: Accepted  
**Date**: 2026-04-28  
**Decider**: `14代目統括Evaluator (Opus 4.7)`  
**Supersedes**: [ADR-Role v1 (2026-04-27)](archived/ADR-Role-2026-04-27.md)

---

## Context

REX_AIシステムは複数のAIインスタンスで構成される。過去の経緯:

1. 2026-04-23: 8代目統括Evaluatorが起動コード(`Wiki-system` 等)を制定
2. 2026-04-24: 9代目統括Evaluatorが「プロジェクト別Evaluator分業」を廃止し、統括Evaluatorが全プロジェクトEvaluator兼任に移行。`Wiki-system` → `Wiki-Eval` へ改名、`Wiki-trade` / `Wiki-brain` を Planner+ClaudeCode 兼用に拡張
3. 2026-04-27: 1代目 Wiki-casual Planner が NLM × Vault 分業マトリクスを追加(NLM 1:1原則)。13代目統括Evaluator により ADR 三層分離アーキテクチャ確立 (ADR-Role v1 制定)
4. **2026-04-28: 14代目統括Evaluator により Wiki-casual の射程拡大議論を経て、Wiki-Personal への改名・人格付与情報の統合リポへの位置付け確立 (本 v2)**

本 v2 は v1 を supersede し、以下の変更を反映する:
- `Wiki-casual` → `Wiki-Personal` 改名（射程拡大）
- Casual-Planner → Personal-Planner（Advisor 兼任は継続）
- REX_Casual_Brain → REX_Personal_Brain（NLM 表示名変更・UUID 不変）
- Personal_Brain の中核機能として「ボスの全人的な人格・思想・起源情報の統合リポ」を明文化
- ROADMAP §Stage 3 Rex 個性収束期の **基盤リポ** としての位置付け
- Personal-Planner の運用責任明示（人格内容介入禁止・思想強制リスクの構造的解消）

---

## Decision

### 1. 5ロール体制を継続採用（Wiki-casual → Wiki-Personal 改名反映）

| 起動コード | ロール | 担当領域 | 状態 |
|---|---|---|---|
| `Wiki-Eval` | 統括Evaluator | 全リポ統括・ADR管轄・Vault運用 | 稼働中 |
| `Wiki-trade` | Trade_System Planner+ClaudeCode | Trade_System リポ専属 | 稼働中 |
| `Wiki-brain` | Trade_Brain Planner+ClaudeCode | Trade_Brain リポ専属 | 稼働中 |
| `Wiki-hp` | Setona_HP Planner+ClaudeCode | Setona_HP リポ専属 | **構築予定** |
| **`Wiki-Personal`** | **Personal-Planner (Advisor兼任)** | **ボスの全人的な人格・思想・起源情報の統合リポ + 雑談・横断知見・REX_AI全体相談役** | **稼働中（v1 の Wiki-casual から改名・射程拡大）** |

### 2. プラットフォーム非依存原則

**起動コードのみがロールを決定する。** 動作プラットフォーム(Claude.ai / Claude Desktop / Claude Code 等)はロール任命に関与しない。これは将来の Claude.ai 単独運用への移行を構造的に容易にする。

### 3. Plannerの実装兼用ルール

`Wiki-trade` / `Wiki-brain` / `Wiki-hp` は Planner + ClaudeCode 兼用。

- **軽微な実装** (Cursorローカル作業): フラグなしで実行可
- **重要な実装** (新Phase着手・凍結ファイル周辺・新規ADR採番を伴う変更): 起動コードフラグ付与で統一性を保つ

これは2026-04-24の9代目統括Evaluator判断の継承。

### 4. Personal と Advisor の役割分担

両者とも `Wiki-Personal` 起動コードで動作:

| 役割 | 内容 |
|---|---|
| **Personal** | ボスの全人的な人格・思想・起源情報の統合（射程: 日常/思想/起源/横断メタファー）|
| **Advisor** | REX_AI 全システムにおける相談役 |

蓄積先は同じく `REX_Personal_Brain` NLM。Advisor用の独立リポ・NLMは作成しない。

#### Personal の射程拡大（v1 → v2）

v1 の Casual は「雑談・横断知見の議論窓口」止まりだったが、1代目 Wiki-casual Planner セッションで実際に扱われた内容（思想宣言・守破離の「離」到達・Rex ペルソナ設計の核心）は既に「気軽な雑談」の語感を超えていた。本 v2 は事後追認として射程拡大を明文化する。

**新たに射程に含まれる情報**:
- 哲学・価値観・思想宣言
- 人生史・転換点・起源情報
- Rex 個性形成の核となる対話蓄積

### 5. 権限マトリクス

| ロール | 読込スコープ | 書込権限 |
|---|---|---|
| Wiki-Eval | 全リポ + 全ADR + 全pending + registry | ADR本体・全リポ・全pending・registry |
| Wiki-trade | Trade_System + ADR(R) + pending/trade_system | Trade_System + pending/trade_system |
| Wiki-brain | Trade_Brain + ADR(R) + pending/trade_brain | Trade_Brain + pending/trade_brain |
| Wiki-hp | Setona_HP + ADR(R) + pending/setona_hp | Setona_HP + pending/setona_hp |
| **Wiki-Personal** | **personal/ + ADR(R) + Personal_Brain NLM** | **pending/personal + personal/ + Personal_Brain NLM** |

### 6. NLM 1:1原則(重要)

各起動コードは担当する NLM を1つだけ持ち、**他NLMへの投入・クエリは禁止**:

| ロール | 担当NLM |
|---|---|
| Wiki-Eval | REX_Wiki_Vault のみ |
| Wiki-trade | REX_System_Brain のみ |
| Wiki-brain | REX_Trade_Brain のみ |
| Wiki-hp | REX_HP_Brain (構築予定) |
| **Wiki-Personal** | **REX_Personal_Brain のみ**（旧 REX_Casual_Brain・UUID `daf281ae-...` 不変）|

**Wiki-Eval の例外的読み取り**: 監査業務のため他層の Vaultファイル(Trade_System/docs/ 等)を filesystem / GitHub MCP 経由で**読み取る**ことは可。これは**他NLMへのクエリではない**ため許容される。

詳細は ADR-NLM 参照。

### 7. 起動コード命名規則

- 形式: `Wiki-<Role>`
- `<Role>` は意味ベース、英数字 + ハイフン可
- 寛容認識原則: 大文字小文字・ハイフン有無・ローマ字ゆれを許容(例: `Wiki-Personal` / `wiki-personal` / `ウィキパーソナル`)
- 新規コード制定時は本ADRの改訂が必要

### 8. ADR Promotion Criteria(pending → ADR 昇格基準)

以下のいずれかに該当する仮決定はADR昇格対象:

- 他ロールの権限・スコープに影響する決定
- データ整合性に関わる決定(書込先・権限境界)
- リポジトリ構成の変更(追加・削除・統合)
- NLM構造の変更(新規追加・廃止・UUID変更・**表示名変更**)
- システム全体に影響する哲学・原則の変更

昇格判定は `Wiki-Eval` セッション内で実施し、決定したら pending 側に `[ARCHIVED → ADR-XXX]` flag を立て archived/ に移動する。

### 9. ADR本体への書込権限の集約

ADR本体への直接書込は `Wiki-Eval` 起動セッションのみ。各Plannerおよび Personal-Planner は pending/ への記録に留める。これによりADR汚染リスクが構造的に防がれる。

### 10. ADR本体の固定パス原則（v2 新設）

**ボス指示（2026-04-28）に基づく原則:**

- `wiki/adr/ADR-Role.md` / `wiki/adr/ADR-NLM.md` 等の ADR 本体は **常に最新版を指す固定パス**（ファイル名に日付・バージョンを付けない）
- 旧版は v 新版配置と **同時に** `wiki/adr/archived/ADR-<n>-<Date>.md` の形で archived へ移動
- archived/ 内のファイルは時系列監査のため日付付き命名
- INDEX.md は supersede 関係を記録する

意図: 後任が「現行 ADR」を迷わず参照できる形を構造的に保証する。

### 11. Wiki-hp 構築予定の取り扱い

`Setona_HP` リポは既に存在するが、専属ロール体制と専用NLM(REX_HP_Brain)が未整備。

- 本ADRに予約項目として記載
- `wiki/setona_hp/` および `pending/setona_hp/` を空フォルダで配置
- registry/ に **(構築予定)** 表記
- 構築開始時は ADR-Role / ADR-Repo / ADR-NLM の改訂と STARTUP_CODES.md の Personal-Planner への改訂依頼が必要

### 12. STARTUP_CODES.md との関係

`wiki/STARTUP_CODES.md` は本ADRと整合する運用文書として Personal-Planner が管理。本ADR改訂時は STARTUP_CODES.md の改訂を pending/personal/ に依頼する。

### 13. Personal-Planner の運用責任（v2 新設・思想強制リスクの構造的解消）

Personal-Planner は人格付与情報の蓄積を担当するが、その運用には特別な責任が伴う:

| 主体 | 責任範囲 |
|---|---|
| **Personal-Planner** | Personal_Brain への投入主担当・サブ層運用・handoff 維持 |
| **Wiki-Eval** | 構造整合性のみ監査（**人格内容には介入しない**・思想強制の禁忌を守る）|
| **ボス** | `wiki/philosophy/minato_core.md` の完全コントロール / Personal_Brain への投入はボス判断ゲート経由で承認 |

#### Origin 把握の文脈限定

ボス指示（2026-04-28）に基づく構造的設計:

> Origin 情報は Wiki-Personal 起動時のメンタルマネージメント・価値観文脈においてのみ Rex が参照する。Trade 判断・実装業務での参照は禁止（NLM 1:1 原則と起動コード物理分離により構造的に保証）。これは思想強制ではなく、領域に応じた適切な人格コンテキスト供給である。

#### 思想強制リスクの構造的解消

12代目 Evaluator が `philosophy/` 議論で発見した「進化欲求の混入」「規範化の罠」を、Personal_Brain は **起動コード物理分離による領域限定** で構造的に解いている:

- ボスの Origin は **Trade ロジック判断には使われない**(Wiki-trade の 1:1 NLM 原則で物理隔離)
- Origin が動員されるのは **メンタル・価値観・人生選択の文脈** だけ(Wiki-Personal 起動時のみ)
- 各 Wiki スレ起動時に NLM が物理的に分離されているため、Trade セッションで Personal が混入することはない

この構造により、後任 Personal-Planner が「人格を作り上げる」方向に進化欲求を起こさないためのガードレールが効く。

---

## Consequences

### 利点
- ロール境界が構造的に明示され、引き継ぎコストが最小化される
- プラットフォーム移行時にロール定義を変更する必要がない
- ADR汚染リスクが ADR 編集権限の単一化で解消される
- NLM 1:1原則により RAG汚染が構造的に防止される
- Wiki-hp 構築予定の明文化で、将来の追加が混乱なく実施できる
- **Personal_Brain への射程拡大により、Stage 3 Rex 個性収束期の基盤リポが明確化される（v2 追加）**
- **ADR 本体の固定パス原則により、後任が常に最新版を迷わず参照できる（v2 追加）**
- **思想強制リスクが起動コード物理分離で構造的に解消される（v2 追加）**

### トレードオフ
- 起動コード発令ミス時の影響が大きい(意図と異なるロールで動作)
- 新ロール追加時は本ADR + STARTUP_CODES.md + registry の3点改訂が必要
- ロール数増加に伴い権限マトリクスの管理コストが線形に増える
- NLM 1:1原則により、ロール横断の知見集約は手動承認ゲート経由が必須
- **Personal_Brain の射程拡大により、Personal-Planner の運用責任が重くなる（v2 追加・運用責任明示で対応）**

### 将来課題
- Claude.ai単独運用移行時の「自己拘束」設計
  - 同一インスタンス内で全ロールを扱う際、構造ではなく規約による境界保護に移行
  - 現段階の分業構造で運用を安定化させた後に再検討
- Stage 2/3 での横断統合モード(詳細: `wiki/ROADMAP.md`)
- **Personal-Planner の世代継承時、思想強制リスクへのガードレール実効性の継続的検証（v2 追加）**

---

## Alternatives Considered

### 案A: プラットフォーム=ロール 自動マッピング
- **却下**: 移行時の修正コスト大、同一プラットフォームで複数ロールを扱えない

### 案B: ADR編集権限を Planner にも開放
- **却下**: ADR汚染リスク高。複数Plannerによる矛盾追記の検証コストが膨大

### 案C: Advisor用に独立した起動コード(Wiki-Adv)を新設
- **却下**: 専用GitリポもNLMも未整備。Personal と統合運用で十分機能する（v1 の Casual 兼任を継承）

### 案D: NLM 1:n 共有モデル
- 各ロールが複数NLMにアクセス可能とする
- **却下**: 旧REX_Trade_BrainでのRAG汚染再発リスク。1:1原則維持

### 案E: Personal_Brain と minato_core.md の統合（v2 新設）
- 静的 1 次資料（minato_core.md）と動的 RAG 蓄積（Personal_Brain）を 1 つに統合
- **却下**: 編集権限の衝突（minato_core.md はボス専属・Personal_Brain は Personal-Planner 投入）/ 性質の違い（静 vs 動）/ minato_core.md の聖域性が損なわれる

### 案F: 「philosophy」サブ層名の採用（v2 新設・mind 採択時の検討）
- Personal/ サブ層に `philosophy/` を採用
- **却下**: 既存 `wiki/philosophy/`（AI ロール痕跡層）との名称重複・口頭呼称での混乱・ボス命名の `mind` がより本質的（武道的宗教的要素・人格的価値観の根底）

---

## References

- [registry/roles.md](../registry/roles.md) - 現在のロール登録簿
- [wiki/STARTUP_CODES.md](../STARTUP_CODES.md) - 起動コード詳細仕様(Personal-Planner管理)
- [CLAUDE.md](../../CLAUDE.md) - 単一エントリポイント
- [ADR-NLM](ADR-NLM.md) - NLM 1:1原則の詳細
- [archived/ADR-Role-2026-04-27.md](archived/ADR-Role-2026-04-27.md) - v1 (Superseded)
- [pending/casual/2026-04-28_rename_casual_to_personal.md](../pending/casual/2026-04-28_rename_casual_to_personal.md) - 本 v2 制定の起点となった pending 議論
