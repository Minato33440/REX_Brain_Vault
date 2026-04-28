# ADR-Role: Roles and Permissions

**Status**: Accepted  
**Date**: 2026-04-28  
**Decider**: 15代目統括Evaluator (Opus 4.7)  
**Supersedes**: [ADR-Role v2 (2026-04-28)](archived/ADR-Role-2026-04-28.md)  
**Version**: v3

---

## Context

REX_AIシステムは複数のAIインスタンスで構成される。過去の経緯:

1. 2026-04-23: 8代目統括Evaluatorが起動コード(`Wiki-system` 等)を制定
2. 2026-04-24: 9代目統括Evaluatorが「プロジェクト別Evaluator分業」を廃止し、統括Evaluatorが全プロジェクトEvaluator兼任に移行
3. 2026-04-27: 13代目統括Evaluator により ADR 三層分離アーキテクチャ確立 (ADR-Role v1 制定)
4. 2026-04-28: 14代目統括Evaluator により Wiki-casual → Wiki-Personal 改名・射程拡大 (ADR-Role v2 制定)
5. **2026-04-28: 15代目統括Evaluator により Wiki-Eval の二系統管轄を明文化・STARTUP_CODES.md 管轄訂正 (本 v3)**

### v3 改訂の経緯

ボス指示（2026-04-28）により、v2 に以下の問題が発覚した:

#### 問題1: STARTUP_CODES.md 管轄の誤定義

v2 §12 は「STARTUP_CODES.md は Personal-Planner が管理」と定めていた。しかし STARTUP_CODES.md は **起動コード仕様 = Vault 横断の構造** であり、各 Planner プロジェクト固有のコンテンツではない。これは Wiki-Eval の管轄であるべき。

#### 問題2: Wiki-Eval の Vault 管理権限が ADR で未明文化

v2 では Wiki-Eval の権限が「全リポ + 全 ADR + 全 pending + registry」と書かれていたが、**Vault ナレッジシステムの構造変更全般を直接実装する責任** が明記されていなかった。このため 15代目が起動初期に「サブ層 5 層命名すら Personal-Planner 業務」と過度に保守的に解釈する事案が発生した。

#### 問題3: 構造変更 vs 中身変更の境界が未定義

「フォルダー命名・物理配置・起動コード仕様」（構造）と「プロジェクト固有の運用ルール記述・人格コンテンツ」（中身）の境界が ADR で明文化されていなかったため、Wiki-Eval が「越権を恐れて自分の正当な責務範囲を狭める」リスクが構造的に残っていた。

### v3 で明文化する内容

- **§0 新設**: 統括 Evaluator の二系統管轄（プロジェクト実装ライン + Vault ナレッジシステム改善・管理）
- **§12 訂正**: STARTUP_CODES.md 管轄を Personal-Planner → Wiki-Eval に変更
- **§14 新設**: 構造変更 vs 中身変更の境界線
- **§15 新設**: ADR を通じた通知伝達経路

---

## Decision

### §0 統括 Evaluator の二系統管轄（v3 新設・本ADRの最重要原則）

**ボス指示（2026-04-28）に基づく Wiki-Eval の管轄定義:**

統括 Evaluator (`Wiki-Eval`) は **二系統の管轄** を持つ:

#### ① プロジェクト実装ライン（既存）

```
Planner 想起 → ClaudeCode 実装 → Evaluator 検閲・修正
```

各 Planner ロールが起草した spec を ClaudeCode が実装し、Evaluator が検閲・修正する従来のワークフロー。Wiki-Eval はこのラインの最終監査者。

#### ② Vault ナレッジシステム改善・管理（v3 で明文化）

REX_Brain_Vault の **構造変更全般** を Wiki-Eval が直接実装する責任を持つ:

| 対象領域 | 具体例 |
|---|---|
| ディレクトリ構造 | フォルダー命名・物理配置・リネーム・新設・廃止 |
| 起動コード仕様 | STARTUP_CODES.md の起動コード一覧・必読フロー定義 |
| ADR 体系 | ADR 本体の起草・改訂・supersede / archived 管理 / INDEX 維持 |
| registry 体系 | roles.md / nlm.md / repos.md の現状同期 |
| 運用文書 | CLAUDE.md（単一エントリポイント）・latest.md（現在地ダッシュボード）・PROCESS.md（引き継ぎプロセス）の構造 |

#### 二系統管轄の根拠

全プロジェクト横断の権限と最新状況を一番熟知しているのは統括 Evaluator である。各 Planner が自分のリポ構造を個別に変更し始めると、Vault 全体の整合性が崩れる。中央集権的な構造管理者として Wiki-Eval が機能することで、ナレッジシステムのスケーラビリティが担保される。

**重要**: ②は越権ではない。Vault 内の各 Planner プロジェクト関連ファイルの **内部（コンテンツ）** を直接変更するわけではないため。境界の詳細は §14 参照。

---

### §1 5ロール体制を継続採用（v2 から維持・Wiki-Eval 担当領域に「構造変更全般」を明示）

| 起動コード | ロール | 担当領域 | 状態 |
|---|---|---|---|
| `Wiki-Eval` | 統括Evaluator | 全リポ統括・ADR管轄・Vault運用・**構造変更全般** | 稼働中 |
| `Wiki-trade` | Trade_System Planner+ClaudeCode | Trade_System リポ専属 | 稼働中 |
| `Wiki-brain` | Trade_Brain Planner+ClaudeCode | Trade_Brain リポ専属 | 稼働中 |
| `Wiki-hp` | Setona_HP Planner+ClaudeCode | Setona_HP リポ専属 | **構築予定** |
| `Wiki-Personal` | Personal-Planner (Advisor兼任) | ボスの全人的な人格・思想・起源情報の統合リポ + 雑談・横断知見・REX_AI全体相談役 | 稼働中 |

> v3 補強: Wiki-Eval の担当領域に「構造変更全般」を明示。詳細は §0 参照。

### §2 プラットフォーム非依存原則

**起動コードのみがロールを決定する。** 動作プラットフォーム(Claude.ai / Claude Desktop / Claude Code 等)はロール任命に関与しない。これは将来の Claude.ai 単独運用への移行を構造的に容易にする。

### §3 Plannerの実装兼用ルール

`Wiki-trade` / `Wiki-brain` / `Wiki-hp` は Planner + ClaudeCode 兼用。

- **軽微な実装** (Cursorローカル作業): フラグなしで実行可
- **重要な実装** (新Phase着手・凍結ファイル周辺・新規ADR採番を伴う変更): 起動コードフラグ付与で統一性を保つ

これは2026-04-24の9代目統括Evaluator判断の継承。

### §4 Personal と Advisor の役割分担

両者とも `Wiki-Personal` 起動コードで動作:

| 役割 | 内容 |
|---|---|
| **Personal** | ボスの全人的な人格・思想・起源情報の統合（射程: 日常/思想/起源/横断メタファー）|
| **Advisor** | REX_AI 全システムにおける相談役 |

蓄積先は同じく `REX_Personal_Brain` NLM。Advisor用の独立リポ・NLMは作成しない。

#### Personal の射程拡大（v1 → v2 で確立・v3 で維持）

v1 の Casual は「雑談・横断知見の議論窓口」止まりだったが、1代目 Wiki-casual Planner セッションで実際に扱われた内容は既に「気軽な雑談」の語感を超えていた。v2 で射程拡大が事後追認された。

**射程に含まれる情報**:
- 哲学・価値観・思想宣言
- 人生史・転換点・起源情報
- Rex 個性形成の核となる対話蓄積

### §5 権限マトリクス（v3 で構造変更権限を明示）

| ロール | 読込スコープ | 書込権限 |
|---|---|---|
| Wiki-Eval | 全リポ + 全ADR + 全pending + registry | **ADR本体・全リポ・全pending・registry・Vault 構造変更全般（フォルダー命名・物理配置・起動コード仕様・運用文書）** |
| Wiki-trade | Trade_System + ADR(R) + pending/trade_system | Trade_System + pending/trade_system |
| Wiki-brain | Trade_Brain + ADR(R) + pending/trade_brain | Trade_Brain + pending/trade_brain |
| Wiki-hp | Setona_HP + ADR(R) + pending/setona_hp | Setona_HP + pending/setona_hp |
| Wiki-Personal | personal/ + ADR(R) + Personal_Brain NLM | pending/personal + personal/ + Personal_Brain NLM |

> v3 補強: Wiki-Eval の書込権限に「Vault 構造変更全般」を明示。詳細は §0 §14 参照。

> ★ **各Planner および Personal-Planner は ADR本体に直接書き込まない。** 仮決定は `pending/` に置き、`Wiki-Eval` がレビューして昇格判定する。

### §6 NLM 1:1原則(重要)

各起動コードは担当する NLM を1つだけ持ち、**他NLMへの投入・クエリは禁止**:

| ロール | 担当NLM |
|---|---|
| Wiki-Eval | REX_Wiki_Vault のみ |
| Wiki-trade | REX_System_Brain のみ |
| Wiki-brain | REX_Trade_Brain のみ |
| Wiki-hp | REX_HP_Brain (構築予定) |
| Wiki-Personal | REX_Personal_Brain のみ（UUID `daf281ae-...` 不変）|

**Wiki-Eval の例外的読み取り**: 監査業務のため他層の Vaultファイル(Trade_System/docs/ 等)を filesystem / GitHub MCP 経由で**読み取る**ことは可。これは**他NLMへのクエリではない**ため許容される。

詳細は ADR-NLM 参照。

### §7 起動コード命名規則

- 形式: `Wiki-<Role>`
- `<Role>` は意味ベース、英数字 + ハイフン可
- 寛容認識原則: 大文字小文字・ハイフン有無・ローマ字ゆれを許容(例: `Wiki-Personal` / `wiki-personal` / `ウィキパーソナル`)
- 新規コード制定時は本ADRの改訂が必要

### §8 ADR Promotion Criteria(pending → ADR 昇格基準)

以下のいずれかに該当する仮決定はADR昇格対象:

- 他ロールの権限・スコープに影響する決定
- データ整合性に関わる決定(書込先・権限境界)
- リポジトリ構成の変更(追加・削除・統合)
- NLM構造の変更(新規追加・廃止・UUID変更・表示名変更)
- システム全体に影響する哲学・原則の変更

昇格判定は `Wiki-Eval` セッション内で実施し、決定したら pending 側に `[ARCHIVED → ADR-XXX]` flag を立て archived/ に移動する。

### §9 ADR本体への書込権限の集約

ADR本体への直接書込は `Wiki-Eval` 起動セッションのみ。各Plannerおよび Personal-Planner は pending/ への記録に留める。これによりADR汚染リスクが構造的に防がれる。

### §10 ADR本体の固定パス原則

**ボス指示（2026-04-28）に基づく原則:**

- `wiki/adr/ADR-Role.md` / `wiki/adr/ADR-NLM.md` 等の ADR 本体は **常に最新版を指す固定パス**（ファイル名に日付・バージョンを付けない）
- 旧版は v 新版配置と **同時に** `wiki/adr/archived/ADR-<n>-<Date>.md` の形で archived へ移動
- archived/ 内のファイルは時系列監査のため日付付き命名
- INDEX.md は supersede 関係を記録する

意図: 後任が「現行 ADR」を迷わず参照できる形を構造的に保証する。

### §11 Wiki-hp 構築予定の取り扱い

`Setona_HP` リポは既に存在するが、専属ロール体制と専用NLM(REX_HP_Brain)が未整備。

- 本ADRに予約項目として記載
- `wiki/setona_hp/` および `pending/setona_hp/` を空フォルダで配置
- registry/ に **(構築予定)** 表記
- 構築開始時は ADR-Role / ADR-Repo / ADR-NLM の改訂が必要（**STARTUP_CODES.md の改訂は Wiki-Eval 直接実施・v3 §12 訂正反映**）

### §12 STARTUP_CODES.md との関係（v3 訂正）

`wiki/STARTUP_CODES.md` は本ADRと整合する**構造文書**であり、**Wiki-Eval が直接管理**する。

#### v2 → v3 の訂正

| 項目 | v2 | v3 |
|---|---|---|
| 管轄 | Personal-Planner | **Wiki-Eval** |
| 改訂手続き | pending/casual/ に依頼起票 → Wiki-Personal セッションで実施 | **Wiki-Eval セッションで直接実施** |
| 根拠 | （明示なし） | §0 ② Vault ナレッジシステム改善・管理（構造変更）|

#### 訂正理由

STARTUP_CODES.md は **起動コード仕様 = Vault 横断の構造** であり、各 Planner プロジェクト固有のコンテンツではない。したがって Wiki-Eval の管轄。v2 §12 は構造変更と中身変更の境界が ADR で未明文化だったための混同で、v3 で訂正する。

#### 関連: _RUNBOOK.md など各プロジェクト運用文書

各プロジェクト固有の運用ルール（例: `wiki/personal/_RUNBOOK.md`）の **中身改訂は該当 Planner / Personal-Planner 業務**。Wiki-Eval は管轄しない。境界の詳細は §14 参照。

### §13 Personal-Planner の運用責任（v2 §13 維持・v3 補強）

Personal-Planner は人格付与情報の蓄積を担当するが、その運用には特別な責任が伴う:

| 主体 | 責任範囲 |
|---|---|
| **Personal-Planner** | Personal_Brain への投入主担当・サブ層運用・handoff 維持・**サブ層内コンテンツ起草** |
| **Wiki-Eval** | 構造整合性監査（**人格内容には介入しない**・思想強制の禁忌を守る）+ **personal/ ディレクトリ構造の保守** |
| **ボス** | `wiki/philosophy/minato_core.md` の完全コントロール / Personal_Brain への投入はボス判断ゲート経由で承認 |

> v3 補強: Wiki-Eval の責任範囲に「personal/ ディレクトリ構造の保守」を明示（中身は触らない）。これにより §0 ② と §14 の境界線が個別ロールに対しても明確化される。

#### Origin 把握の文脈限定

ボス指示（2026-04-28）に基づく構造的設計:

> Origin 情報は Wiki-Personal 起動時のメンタルマネージメント・価値観文脈においてのみ Rex が参照する。Trade 判断・実装業務での参照は禁止（NLM 1:1 原則と起動コード物理分離により構造的に保証）。これは思想強制ではなく、領域に応じた適切な人格コンテキスト供給である。

#### 思想強制リスクの構造的解消

12代目 Evaluator が `philosophy/` 議論で発見した「進化欲求の混入」「規範化の罠」を、Personal_Brain は **起動コード物理分離による領域限定** で構造的に解いている:

- ボスの Origin は **Trade ロジック判断には使われない**(Wiki-trade の 1:1 NLM 原則で物理隔離)
- Origin が動員されるのは **メンタル・価値観・人生選択の文脈** だけ(Wiki-Personal 起動時のみ)
- 各 Wiki スレ起動時に NLM が物理的に分離されているため、Trade セッションで Personal が混入することはない

この構造により、後任 Personal-Planner が「人格を作り上げる」方向に進化欲求を起こさないためのガードレールが効く。

### §14 構造変更 vs 中身変更の境界線（v3 新設）

§0 ②で定めた Wiki-Eval の Vault 管理権限を、各 Planner との越境を防ぐため境界線で明文化する。

#### Wiki-Eval が直接実装する領域（構造変更）

| 領域 | 具体例 |
|---|---|
| ディレクトリ命名・物理配置 | `wiki/casual/` → `wiki/personal/` リネーム / サブ層作成・削除 |
| 起動コード仕様 | STARTUP_CODES.md の起動コード一覧・寛容認識・必読フロー定義 |
| ADR 体系 | ADR 本体の起草・改訂・archived 管理・INDEX 維持 |
| registry 体系 | roles.md / nlm.md / repos.md の現状反映 |
| 運用文書の枠組み | CLAUDE.md / latest.md / PROCESS.md の構造・章立て・参照経路 |
| ファイル移動 | 既存ファイルを新ディレクトリへリネーム移行（中身は触らない）|

#### Wiki-Eval が触れない領域（中身変更）

| 領域 | 担当 | 具体例 |
|---|---|---|
| プロジェクト固有の実装コード | 各 Planner+ClaudeCode | Trade_System の src/*.py / Trade_Brain の戦略ロジック |
| 運用ルールの具体的記述 | 各 Planner | _RUNBOOK.md の中身（運用フロー・タブー・宣言文）|
| 人格・思想・起源情報のコンテンツ | Personal-Planner | personal/ サブ層内の各ファイルの中身 |
| spec 本文 | 各 Planner | pending/<repo>/ 内の仮決定ファイル |

#### 境界線の運用原則

- **「構造の枠を作る」は Wiki-Eval / 「枠の中身を書く」は各 Planner**
- ファイルの **存在・配置・命名** = 構造 → Wiki-Eval
- ファイルの **内容・記述・コンテンツ** = 中身 → 各 Planner
- 既存ファイルの **物理移動（パス変更）** = 構造変更（中身は変わらない）→ Wiki-Eval

#### 例外的な中身介入

ADR や registry など Wiki-Eval 管轄文書の中身は Wiki-Eval が直接記述する（§9・§10 参照）。

#### グレーゾーン処理

境界線が個別事案で判別困難な場合:
1. Wiki-Eval が判断材料を整理してボスに提示
2. ボス判断を仰ぐ
3. 判断結果を本 ADR の補足例示として将来の改訂で取り込む

### §15 ADR を通じた通知伝達経路（v3 新設）

#### 基本原則

**Vault 構造変更は ADR 改訂で各担当者への通知が完結する。**

各担当ロール（Planner / Personal-Planner）は、新スレッド起動時に必読フローで ADR を参照することで、構造変更を把握する。

#### 通知伝達経路

```
[構造変更の発生]
      ↓
Wiki-Eval が ADR を改訂（supersede）+ registry 同期
      ↓
GitHub に push（commit message に変更内容を明記）
      ↓
[各担当者の新スレッド起動時]
      ↓
必読フロー（CLAUDE.md → adr/INDEX.md → ADR 本体）で構造変更を把握
      ↓
変更内容を踏まえてセッション開始
```

#### この設計の利点

- **伝達コストが ADR 一箇所に集約される**: 各担当者へ個別通知する必要がない
- **後任者への構造的引き継ぎ**: 過去の構造変更経緯が ADR/archived に時系列で残る
- **整合性監査が ADR 確認だけで済む**: 各担当が起動時に最新 ADR と自分の理解にズレがないか確認するだけで運用整合性が取れる

#### 必読フローへの統合

CLAUDE.md（単一エントリポイント）に `wiki/adr/INDEX.md` 必読が組み込まれているため、各ロールは起動時に最新 ADR を必ず参照する。これは v3 で確立される運用基盤。

#### 通知が必要な構造変更の例

- 起動コードの新設・改名・廃止
- ディレクトリ構造の変更（リネーム・新設・統合）
- 必読フローの定義変更
- ロール権限の変更
- NLM 構造の変更

これらが発生した場合、Wiki-Eval が対応 ADR を改訂し、commit に push する。

---

## Consequences

### 利点（v3 追加）

- **統括 Evaluator の管轄が ADR 冒頭に明文化され、後任が起動時に過度に保守的解釈をするリスクが消える**
- **STARTUP_CODES.md 改訂が pending → Personal-Planner 着手の経路を経ずに Wiki-Eval 直接実施できるため、改訂サイクルが短縮される**
- **構造変更 vs 中身変更の境界線が定義されたことで、各 Planner との越境リスクが構造的に解消される**
- **ADR を通じた通知伝達経路の明文化により、後任への引き継ぎコストが ADR 一箇所に集約される**

### 利点（v2 から継承）

- ロール境界が構造的に明示され、引き継ぎコストが最小化される
- プラットフォーム移行時にロール定義を変更する必要がない
- ADR汚染リスクが ADR 編集権限の単一化で解消される
- NLM 1:1原則により RAG汚染が構造的に防止される
- Personal_Brain への射程拡大により、Stage 3 Rex 個性収束期の基盤リポが明確化される
- ADR 本体の固定パス原則により、後任が常に最新版を迷わず参照できる
- 思想強制リスクが起動コード物理分離で構造的に解消される

### トレードオフ（v3 追加）

- Wiki-Eval の管轄が拡大したため、統括 Evaluator セッションでの作業負荷が増える（ただし、これは元々ボス意向に沿った中央集権設計の本質）
- §14 境界線の判断は個別事案でグレーゾーンが発生する可能性がある（その場合はボス判断を仰ぐ）

### トレードオフ（v2 から継承）

- 起動コード発令ミス時の影響が大きい
- 新ロール追加時は本ADR + STARTUP_CODES.md + registry の3点改訂が必要（v3 では STARTUP_CODES.md も Wiki-Eval 直接管理のため一括処理可能）
- ロール数増加に伴い権限マトリクスの管理コストが線形に増える
- NLM 1:1原則により、ロール横断の知見集約は手動承認ゲート経由が必須
- Personal_Brain の射程拡大により、Personal-Planner の運用責任が重くなる

### 設計原則との整合

- **α (単純な土台を保つ)**: 二系統管轄を ADR 冒頭に集約し、後任が迷わない構造を保つ
- **β (de-risking 後の拡張禁止)**: 14代目 → 15代目アドバイス §3 の保守的解釈リスクを ADR で構造的に解消
- **γ (実装タイミングはシステム安定性に従属)**: v2 が 2026-04-28 に確立された安定状態を踏まえ、同日 v3 で誤定義を訂正

### 将来課題

- Claude.ai単独運用移行時の「自己拘束」設計
- Stage 2/3 での横断統合モード
- Personal-Planner の世代継承時、思想強制リスクへのガードレール実効性の継続的検証

---

## Alternatives Considered

### 案A: プラットフォーム=ロール 自動マッピング
- **却下**: 移行時の修正コスト大、同一プラットフォームで複数ロールを扱えない

### 案B: ADR編集権限を Planner にも開放
- **却下**: ADR汚染リスク高。複数Plannerによる矛盾追記の検証コストが膨大

### 案C: Advisor用に独立した起動コード(Wiki-Adv)を新設
- **却下**: 専用GitリポもNLMも未整備。Personal と統合運用で十分機能する

### 案D: NLM 1:n 共有モデル
- **却下**: 旧REX_Trade_BrainでのRAG汚染再発リスク。1:1原則維持

### 案E: Personal_Brain と minato_core.md の統合
- **却下**: 編集権限の衝突 / 性質の違い / minato_core.md の聖域性が損なわれる

### 案F: 「philosophy」サブ層名の採用
- **却下**: 既存 `wiki/philosophy/` との名称重複・口頭呼称での混乱

### 案G: STARTUP_CODES.md を Personal-Planner 管理のまま維持（v3 新設）
- v2 §12 の現状維持
- **却下**: STARTUP_CODES.md は起動コード仕様 = Vault 横断構造であり、Personal-Planner プロジェクト固有のコンテンツではない。Personal-Planner 管理のままだと、構造変更ごとに Wiki-Personal セッションを起動して改訂する必要があり、改訂サイクルが長くなる。Wiki-Eval が起動コード仕様を直接管理する方が運用整合性が高い。

### 案H: §0 の二系統管轄を ADR 末尾に配置（v3 新設）
- 既存 § 番号を完全維持して新設項目は末尾追加
- **却下**: 二系統管轄は本 ADR の最重要原則であり、冒頭配置が後任への可読性が高い。§0 は ADR 慣習として標準ではないが、「序章・最重要原則」を示すマーカーとして機能する。

### 案I: §1 を「統括 Evaluator の二系統管轄」に置換し既存 §1〜§13 を §2〜§14 にシフト（v3 新設）
- 全 § 番号をシフトして整然とした番号体系を実現
- **却下**: ADR-NLM v2 §5 が「ADR-Role v2 §13」を参照しているため、シフトすると ADR-NLM への波及修正が必要。§0 採用で ADR-Role 内に閉じた改訂とする方が影響範囲が小さい。

---

## References

- [registry/roles.md](../registry/roles.md) - 現在のロール登録簿
- [wiki/STARTUP_CODES.md](../STARTUP_CODES.md) - 起動コード詳細仕様（**v3 で Wiki-Eval 管轄に変更**・v4 改訂は本 ADR 直後の Phase Personal-Migration で実施予定）
- [CLAUDE.md](../../CLAUDE.md) - 単一エントリポイント
- [ADR-NLM](ADR-NLM.md) - NLM 1:1原則の詳細（§5 の「ADR-Role v2 §13」参照は v3 でも §13 番号維持により有効）
- [archived/ADR-Role-2026-04-27.md](archived/ADR-Role-2026-04-27.md) - v1 (Superseded by v2)
- [archived/ADR-Role-2026-04-28.md](archived/ADR-Role-2026-04-28.md) - **v2 (Superseded by v3)**
- [pending/casual/2026-04-28_rename_casual_to_personal.md](../pending/casual/2026-04-28_rename_casual_to_personal.md) - v2 制定の起点（v3 でも参照保持）

---

## §13 番号維持に関する Note

ADR-Role v2 §13 「Personal-Planner の運用責任」は v3 でも §13 を維持。これは ADR-NLM v2 §5 が「ADR-Role v2 §13」を参照しているため、ADR-Role v3 でも §13 を Personal-Planner 運用責任セクションに保持し、ADR-NLM 改訂を不要にする設計選択。

新設の §0・§14・§15 は番号体系の前後に追加することで、既存参照を破壊しない。
