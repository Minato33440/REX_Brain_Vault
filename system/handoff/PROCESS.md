# 引き継ぎプロセス — PROCESS.md

**役割**: 引き継ぎプロセスの**要点と運用原則**を一元化したリファレンス。
**位置付け**: `latest.md`（=現在地データ）と並列。本ファイルは**方法論・運用ガイド**。
**最終更新**: 2026-04-24 / 9 代目統括 Evaluator（本体）+ 2026-04-28 / 14 代目（第 II 部 A〜H 追補）+ 2026-04-29 / 16 代目（第 II 部 I 節追加・第 I 部に最小限の参照マーク追記）
**前版**: 2026-04-23 / 8 代目統括 Evaluator（初版）
**読み手**: 統括 Evaluator / Planner / ClaudeCode / Advisor

> **2026-04-28 14 代目追補**: 13 代目による ADR/pending/registry 三層分離体系の確立(2026-04-27)と、14 代目による Wiki-Personal 改名(2026-04-28)を反映する**第 II 部追補**を末尾に追加。本体(第 I 部・9 代目作成)は変更せず保全。
> **2026-04-29 16 代目訂正**: 15 代目セッション(2026-04-28〜29)で確立された ADR-Role v3→v4 supersede / Wiki-Rex 新設 / Phase Casual-Final-Archive 系列を反映する**第 II 部 I 節**を末尾に追加。第 I 部(9 代目)・第 II 部 A〜H(14 代目)は文体保全のため不可侵を維持。第 I 部 STEP 0 と STEP 1 テーブル直前にのみ最小限の ⚠️ 参照マークを追加(本文は不変)。

---

## 🧭 3 つの基本原則

引き継ぎプロセスはこの 3 原則に従って設計されている。

### 原則 1: 引き継ぎは「現状把握 + 次の実行内容」に純化

ボス指示（2026-04-23）。哲学・思想・行動規範は別ファイル（philosophy/）に分離し、引き継ぎ書本体には書かない。

### 原則 2: 思想を後任に強制しない

ボス指示（2026-04-23）。気づきは `philosophy/evaluator_code.md` に**個人的メモ**として残す。「派生原則」「行動規範」と勝手に格上げしない。

### 原則 3: トークンコストは「読込量 ≠ 情報総量」で削減

NLM 導入により情報総量を削らずにローカル読込量を削れる。詳細は `wiki/philosophy/architecture.md` 参照。

---

## 🚀 セッション開始時の標準フロー

### 共通プロトコル（全ロール）

> ⚠️ **2026-04-29 16 代目訂正**: 以下の STEP 0(起動コード判定)の最新版は **第 II 部 I 節 I-3** を参照。本記述は 9 代目時点の 4 起動コード体制(Wiki-system / Wiki-trade / Wiki-brain / Wiki-casual)を文体保全しているが、現行は **6 ロール体制**(Wiki-Eval / Wiki-trade / Wiki-brain / Wiki-hp / Wiki-Personal / Wiki-Rex・15 代目時点)。

```
STEP 0: スレ冒頭の起動コードを確認
  → 「Wiki-Eval」「Wiki-trade」「Wiki-brain」「Wiki-casual」のいずれか
  → コードがあれば wiki/STARTUP_CODES.md の定義に従う
  → コードがなければ文脈判断（システム業務 / 雑談）
  → ⚠️ 旧コード `Wiki-system` は 2026-04-24 より `Wiki-Eval` に改名済み

STEP 1: ロール別の必須ファイルを読む（後述）

STEP 2: 「読み込み検証チェックリスト」（10 問）に答える
  → 答えられなければ読込不十分・再読込

STEP 3: 「前回からの変更点」を一言で把握

STEP 4（必要時）: NLM クエリで詳細取得
  → ローカル読込で不足する情報のみ NLM に問う
  → 全 4 NLM 運用可（2026-04-23 凍結解除）
```

### ロール別の STEP 1（必須読込）

> ⚠️ **2026-04-29 16 代目訂正**: 以下の必須読込テーブルの最新版は **第 II 部 I 節 I-2** を参照。本テーブルは 9 代目時点の 4 起動コード体制を文体保全しているが、現行は 6 ロール体制で必須読込ファイルも更新済み(START_HERE.md 凍結移設・Wiki-casual → Wiki-Personal 改名・Wiki-Rex / Wiki-hp 追加等)。

| ロール | 起動コード | 必須読込 |
|---|---|---|
| 統括 Evaluator（全プロジェクト Evaluator 兼任）| `Wiki-Eval` | START_HERE.md → CLAUDE.md → handoff/latest.md（必須 3 ファイル）|
| Trade_System Planner + ClaudeCode 兼用 | `Wiki-trade` | START_HERE.md + Trade_System/docs/ 主要 5 つ |
| Trade_Brain Planner + ClaudeCode 兼用 | `Wiki-brain` | START_HERE.md + Trade_Brain/docs/ 主要 5 つ |
| 雑談モード | `Wiki-casual` | casual/_RUNBOOK.md のみ + 継続話題 topics/ |

詳細は `wiki/STARTUP_CODES.md` の各ロール詳細セクション参照。

---

## 📋 セッション終了時の /wrap-up フロー

### 統括 Evaluator の /wrap-up（フル版）

```
STEP 1: wiki/log.md に本セッションの決定事項・完了タスクを追記（追記のみ）
STEP 2: wiki/trade_system/pending_changes.md を更新（変更があれば）
STEP 3: wiki/trade_system/adr_reservation.md を更新（採番があれば）
STEP 4: wiki/handoff/latest.md を更新（現状反映）
STEP 4-b: wiki/START_HERE.md を更新（3 リポに状態変化があった時）
STEP 5: NLM に新規ソースを追加（必要時）
STEP 6: docs/ の旧版ファイルを archive 移動（該当時）
STEP 7: REX_Brain_Vault に GitHub push（rtk git）
STEP 8: Claude.ai プロジェクトナレッジ更新（ボス手動）
STEP 9（任意）: philosophy/evaluator_code.md に気づきメモ追記
```

### Trade_System Planner の /wrap-up（軽量版）

```
STEP 1: wiki/log.md に追記
STEP 2: wiki/trade_system/pending_changes.md を更新
STEP 4: wiki/handoff/latest.md の Trade_System セクションのみ更新
STEP 7: REX_Brain_Vault に GitHub push
```

### Trade_Brain Planner / ClaudeCode の /wrap-up

```
STEP 1: Trade_Brain 側の WEEKLY_UPDATE workflow に従う
STEP 4: wiki/handoff/latest.md の Trade_Brain セクションのみ更新(依頼ベース)
STEP 7: Trade_Brain GitHub push（rtk git）
```

### 雑談スレの /wrap-up（最小版）

```
STEP 1: wiki/casual/log.md に追記（任意）
STEP 2: 熟した話題を wiki/casual/topics/ または insights/ に整理
STEP 3: NLM REX_Casual_Brain への投入候補を提示（ボス承認後に投入）
```

---

## 🤖 NLM 活用ガイド

### NLM 体制（2026-04-23 凍結解除済み・全 4 NLM 運用可）

| NLM | 用途 | クエリすべき例 |
|---|---|---|
| REX_System_Brain | Trade_System 設計詳細 | 「ADR D-8 の経緯」「stage2 設計根拠」 |
| REX_Trade_Brain | Trade_Brain 蒸留 | 「先週の市場環境」「distillation の出力例」 |
| REX_Wiki_Vault | ナレッジシステム運用 | 「過去の Phase 進行」「7 代目セッション経緯」 |
| REX_Casual_Brain | 雑談・個人的話題 | 「合気道の前回議論」「motorcycle メモ」 |

### NLM クエリすべき場面

- ✅ 設計判断の**過去の経緯**を知りたい時
- ✅ ローカル読込から省略した**詳細情報**が必要な時
- ✅ **複数文書の横断的な要約**が欲しい時
- ✅ ボスの過去発言の**正確な引用**が必要な時

### NLM クエリすべきでない場面

- ❌ 現在の動的状態（pending_changes / adr_reservation 等）→ ローカル直読
- ❌ 致命的地雷リスト → handoff/latest.md 直読（NLM 経由だと精度劣化リスク）
- ❌ 起動コード辞書 → STARTUP_CODES.md 直読
- ❌ 緊急判断 → ローカル即読の方が速い

### NLM 個別化原則

各 NLM は**ドメイン分離**されている。横断クエリは混乱を招くため避け、各 NLM に該当ドメインのクエリだけを投げる。横断的整理が必要な時は統括 Evaluator が手動で各 NLM の結果を統合する。

---

## 🎯 トークンコスト最適化の原則

### 4 色マトリクス分類（簡略版）

| 色 | 性質 | 例 | 引き継ぎ時の扱い |
|---|---|---|---|
| 🟢 常駐型 | 動的状態 | latest.md / pending_changes / STARTUP_CODES | ローカル必須 |
| 🟡 ハイブリッド型 | 主要設計 | ADR.md / MINATO_MTF_PHILOSOPHY | ローカル + NLM 両方 |
| 🔵 NLM 専用化候補 | 履歴・蓄積 | log.md / concepts/ / src_inventory | NLM 投入後ローカル省略 |
| ⚪ アーカイブ/削除 | 旧版・移管済み | weekly_workflow.md（削除予定）| 物理削除 or archive |

### 引き継ぎ読込最小セット（NLM 投入完了後の目標）

```
CLAUDE.md              約  80 行
wiki/START_HERE.md     約  80 行
wiki/handoff/latest.md 約 150 行
wiki/STARTUP_CODES.md  約 100 行（必要時）
─────────────────────────────────
合計                   約 310 行（≒ 4-5k トークン）
```

詳細情報は **NLM クエリ経由で取得**する設計。

---

## ⚠️ 避けるべき罠（過去の失敗パターン）

### 罠 1: 思想の制度化（8 代目 2026-04-23）

前任の所感を「継承された規範」と格上げして後任に義務化する。**回避**: 気づきは個人的メモとして書き、タイトル格上げしない。

### 罠 2: ボス発言の勝手な原則化（8 代目 2026-04-23）

ボス発言を勝手に「派生原則」と命名する越権行為。**回避**: 原則認定は ADR 本体採番でボスが行う。Evaluator は「ボス発言の記録」として残すに留める。

### 罠 3: latest.md の肥大化（7 代目 2026-04-22）

哲学・行動規範を引き継ぎ書本体に書き込んで 520 行に膨らませた。**回避**: 引き継ぎ書は「現状把握 + 次の実行内容」に純化（ボス指示）。

### 罠 4: 静的シンプル化偏り（6 代目 2026-04-20）

机上推論で「分離 = 安全」「シンプル = 正解」と即断する。**回避**: ボス裁量の動的エコシステム発展性を常に参照。判断前に「ボスの意図」を文節分解。

### 罠 5: NLM 一本化案の見落とし（8 代目 2026-04-23）

「Git は冗長」と即断して NLM 一本化を提案、スレ跨ぎ中期記憶（Vault casual/）が抜けた。**回避**: ストレージ階層は「会話履歴 / Vault / NLM」の 3 層が基本。

### 罠 6: 起動オーバーヘッド（8 代目 2026-04-23）

ボスがロール指定と読むべきファイルパスを毎回打つ手間を見落としていた。**回避**: 起動コード辞書（STARTUP_CODES.md）を活用し UX を最優先。

### 罠 7: Phase 命名の混乱（9 代目 2026-04-24）

Phase 1-4（Trade_System src/ 構造再編）と Phase A-E（Vault・ナレッジシステム整備）が並存し、さらに Phase A' / A'' と派生させて 9 代目が命名枯渇を感じた。**回避**: 下記「Phase 命名規則」セクションで分離を明記・Phase 系列は 2 系統（数字と英字）で扱い、派生形（A'・A''）は最低限にする。

---

## 🔢 Phase 命名規則（9 代目 2026-04-24 明文化）

REX_AI プロジェクトでは 2 系統の Phase 命名が並存するため、以下の規則で分離して扱う。

### Phase 1-4（数字系）— Trade_System 専用

| Phase | 内容 | 状態 |
|---|---|---|
| Phase 1 | src/ 棚卸し・分類・Trade_Brain 移設 | ✅ 2026-04-20 完了 |
| Phase 2 | track_trades 隔離・plotter.py 共存確定 | ✅ 2026-04-20 完了 |
| Phase 3 | 責務別ディレクトリ化（src/core/ viz/ scan/ tests/）| ⬜ ボス着手承認済（2026-04-24）|
| Phase 4 | D-12/D-13 裁量整合版実装訂正（REX_029+）| ⬜ Phase 3 後 |

**新 Phase 追加は Trade_System のみ**。Phase 5 / Phase 6 と連番で進める。

### Phase A-E（英字系）— Vault・ナレッジシステム専用

| Phase | 内容 | 状態 |
|---|---|---|
| Phase A | Vault v5 整備（7 代目）| ✅ 2026-04-22 完了 |
| Phase A' | Vault 軽量化（8 代目）| ✅ 2026-04-23 完了 |
| Phase A'' | entities/decisions 整合性回復（9 代目）| ✅ 2026-04-23 完了 |
| Phase B | REX_Wiki_Vault への初期 Ingest | ⬜ ボス承認待ち |
| Phase C | wiki/entities + decisions を trade_system/ 配下へ物理統合 | ⬜ Phase B 後 |
| Phase D | Trade_Brain wiki 骨組み構築 | ⬜ 未着手 |
| Phase E | Ingest/Compile/Lint 運用開始 | ⬜ Phase B 後 |

**新 Phase 追加は Vault・ナレッジシステムのみ**。大きな作業は **Phase F 以降を連番**で使用（A' / A'' 形式の派生命名は命名枯渇の兆候なので避ける）。

### 使い分けの原則

1. **新規に Phase を立ち上げる時は、上記 2 系統のどちらに属するかを最初に判定**
2. **Trade_System の構造・ロジック変更 → 数字系**
3. **Vault・NLM・ナレッジ運用の構造変更 → 英字系**
4. **Trade_Brain 固有の大きな作業は将来別系統（例: Phase α-ε、または WEEK 系統）として切り出す余地を残す**
5. **派生形（A'・A''）は最低限にし、通常は連番で進める**

---

## 📐 latest.md の更新原則

### 含めるもの

- 致命的地雷リスト（4 項目・2026-04-24 時点）
- 読み込み検証チェックリスト（10 問）
- 3 リポ現在地スナップショット
- Phase 進行状況（Phase 命名規則に従い数字系・英字系を分けて記述）
- 次に実行すべき内容（優先度順）
- ロール別起動プロンプト
- 関連文書一覧

### 含めないもの

- 哲学・思想・行動規範 → philosophy/ に分離
- 過去経緯の長文説明 → log.md または NLM
- ボス発言の解釈 → philosophy/evaluator_code.md
- 設計判断の詳細 → ADR.md（Trade_System 側）

### バージョン管理

- 大きな構造変更時にバージョン番号を上げる（v6.1 → v6.2）
- 軽微更新はバージョン据え置きで日付のみ更新

---

## 🤝 ボスとの分担

### Evaluator（AI）が自動で行う

- ファイル更新・読込・検証チェックリスト回答
- log.md / pending_changes.md / adr_reservation.md / latest.md 更新
- NLM クエリ実行
- ロジック整合性監査

### ボス（人間）が手動で行う

- 設計判断の最終承認（ADR 本体採番）
- GitHub push（rtk git add/commit/push）
- Claude.ai プロジェクトナレッジ更新（添付ファイル差し替え）
- NLM への source 投入（Claude Desktop or ClaudeCode 経由）
- minato_core.md の更新（ボス個人 1 次データ）
- 凍結解除タイミングの決定
- Phase 進行可否の判断
- 新機能実装の優先順位決定

---

## 📚 関連ファイル

```
wiki/STARTUP_CODES.md                        — 起動コード辞書
wiki/START_HERE.md                           — 新スレ最初の入口
wiki/handoff/latest.md                       — 現在地ダッシュボード（v6.4）
wiki/handoff/architecture_handoff.md         — 7 代目セッション記録
wiki/philosophy/evaluator_code.md            — Evaluator 気づきメモ
wiki/philosophy/architecture.md              — 4 リポ・4 NLM 体制事実記録
wiki/philosophy/cross_vectors.md             — 4 横断ベクトル事実記録
wiki/philosophy/minato_core.md               — ボス個人 1 次データ（ボス手動更新）
wiki/casual/_RUNBOOK.md                      — 雑談層運用ルール
CLAUDE.md（Vault 直下）                     — Vault 運用手順
```

---

## 🔄 本ファイルの更新ルール

- 引き継ぎプロセスに**構造変化**があった時のみ更新
- 軽微な運用改善は本ファイルではなく `philosophy/evaluator_code.md` の気づきメモへ
- 大きな変更時は本ファイル冒頭の「最終更新」日付と版数を更新
- ボス指示で原則が変更された時は速やかに反映

---

*発行: 9 代目統括 Evaluator (Opus 4.7) / 2026-04-24*
*前版: 8 代目統括 Evaluator (Opus 4.7) / 2026-04-23*
*次回更新トリガー: NLM 実投入完了後の運用改善 / Phase B/C/D/E 進行時の手順追加 / ボスからの新原則指示*

---
---
---

# 第 II 部追補 — ADR 体系下の運用フロー(13・14 代目分の積み残し反映)

**追補発行**: 2026-04-28 / 14 代目統括 Evaluator (Claude Opus 4.7)
**追補対象**: 13 代目(2026-04-27 ADR 体系化)+ 14 代目(2026-04-28 Wiki-Personal 改名)による構造変化
**位置付け**: 第 I 部(9 代目作成・本体)は不可侵で保全。本追補は新体制下での運用差分を記録する。

---

## A. 三層分離アーキテクチャの導入(13 代目・2026-04-27)

13 代目統括 Evaluator がボス指示を受けて確立した構造変更:

```
ADR(確定事項層) — Wiki-Eval のみ書込可能
  ↑ 昇格(ADR Promotion Criteria に基づく承認)
pending(仮決定議論層) — 各 Planner が自領域を書込可能
  ↑ 仮決定発生時に各 Planner が起票
[Planner セッション]

並行レイヤー:
registry(現在の登録状態層) — Wiki-Eval のみ書込可能(ADR 改訂と同時更新)
```

### 構造の意義

「ADR と registry の役割分離」が拡張時の整合性を構造的に担保する。リポ・NLM・ロールが増減しても、registry/ で 1 行追加・削除するだけで済み、ADR 本体は触らずに済む。CLAUDE.md と ADR 本体は将来の肥大化を回避する設計。

### 制定された 4 本の ADR(現行版)

| ADR | タイトル | 現行バージョン |
|---|---|---|
| ADR-Role | Roles and Permissions | **v2(14 代目 2026-04-28)** |
| ADR-Repo | Repository Architecture | v1(13 代目 2026-04-27) |
| ADR-Vault | Vault Write Path Unification | v1(13 代目 2026-04-27) |
| ADR-NLM | NLM Architecture (1:1 Principle) | **v2(14 代目 2026-04-28)** |

旧版は `wiki/adr/archived/` に日付付き命名で保管。本体ファイル名は固定パス(日付なし)を維持。

---

## B. ADR Supersede 運用フロー(14 代目実地経験により確立)

14 代目セッションで初の ADR supersede を実施した経験から、運用フローを明文化する:

### Step-by-Step 実行手順

```
1. pending 起票
   → wiki/pending/<repo>/YYYY-MM-DD_<topic>.md
   → 仮決定内容・根拠・ADR 昇格希望・影響範囲・整合性論点を記載

2. ボス承認
   → 必要に応じて議論を重ねる
   → 承認時点で次 Step へ進める

3. archived/ 旧版保管(supersede 対象 ADR ごと)
   → wiki/adr/archived/ADR-<Name>-<制定日>.md
   → ファイル冒頭に [SUPERSEDED by ADR-XXX vN (Date)] flag を追記
   → supersede 経緯と関連 pending へのリンクを冒頭に記載

4. ADR 本体上書き(固定パス・日付なし)
   → wiki/adr/ADR-<Name>.md を新版で上書き
   → SHA 必要(create_or_update_file の sha 引数)

5. INDEX.md 更新
   → 確定 ADR 一覧表のバージョン更新
   → 「Supersede 履歴」セクションに改訂行を追加
   → archived/ 内のファイル一覧を更新

6. registry 同期
   → registry/<該当>.md を新 ADR の内容に合わせて更新
   → ロール改名・NLM 改名等は同時反映必須

7. typo / 表記漏れの自己訂正
   → push 後に view で再読み確認(任意・推奨)
   → 検出した typo は同セッション内で修正(次代に持ち越さない)
```

### 固定パス原則(ボス指示・2026-04-28 / ADR-Role v2 §10)

- `wiki/adr/ADR-<Name>.md` は **常に最新版を指す固定パス**(ファイル名に日付・バージョンを付けない)
- 旧版は v 新版配置と **同時に** archived へ移動
- archived/ 内のファイルは時系列監査のため日付付き命名(`ADR-<Name>-<YYYY-MM-DD>.md`)
- INDEX.md が supersede 関係を記録

意図: 後任が「現行 ADR」を迷わず参照できる形を構造的に保証する。

---

## C. 起動コード一覧(2026-04-28 時点・ADR-Role v2 反映)

| 起動コード | ロール | 担当 NLM | 状態 |
|---|---|---|---|
| `Wiki-Eval` | 統括 Evaluator | REX_Wiki_Vault | 稼働中 |
| `Wiki-trade` | Trade_System Planner+ClaudeCode | REX_System_Brain | 稼働中 |
| `Wiki-brain` | Trade_Brain Planner+ClaudeCode | REX_Trade_Brain | 稼働中 |
| **`Wiki-Personal`** | **Personal-Planner (Advisor 兼任)** | **REX_Personal_Brain** | **稼働中(14 代目改名)** |
| `Wiki-hp` | Setona_HP Planner+ClaudeCode | REX_HP_Brain | **構築予定** |

### Wiki-casual → Wiki-Personal 改名(14 代目・2026-04-28)

- 旧 `Wiki-casual` は `Wiki-Personal` に改名(寛容認識原則により旧コードも当面認識可)
- NLM 表示名 `REX_Casual_Brain` → `REX_Personal_Brain`(UUID `daf281ae-...` **不変**)
- ロール正式名 Casual-Planner → Personal-Planner(Advisor 兼任は継続)
- 射程拡大: 雑談・横断知見の議論窓口 → **ボスの全人的な人格・思想・起源情報の統合リポ + 雑談・横断知見**
- Vault 物理ディレクトリ `wiki/casual/` → `wiki/personal/` への移行は次スレで実施(Step 4)

---

## D. ロール別 /wrap-up フロー(ADR 体系下・2026-04-28 改訂)

第 I 部の /wrap-up フローを ADR 体系に対応させた改訂版。

### 統括 Evaluator(Wiki-Eval)の /wrap-up

```
STEP 1: wiki/log.md に本セッション記録を追記(追記のみ)
STEP 2: wiki/handoff/latest.md を現状反映で更新
STEP 3: 構造変化があれば該当 ADR 改訂(supersede フロー B に従う)
STEP 4: registry/<該当>.md 同期更新(ADR 改訂と同時)
STEP 5: pending エントリの archived 移動(ADR 昇格時)
STEP 6: NLM injection 実施 or 候補提示(必要時)
STEP 7: GitHub push(GitHub MCP 経由・ADR-Vault 遵守)
STEP 8: Claude.ai プロジェクトナレッジ更新(ボス手動)
STEP 9(任意): philosophy/evaluator_code.md に気づきメモ追記
```

### 各 Planner(Wiki-trade / Wiki-brain / Wiki-Personal / Wiki-hp)の /wrap-up

```
STEP 1: wiki/log.md に追記
STEP 2: pending/<自領域>/ に新規仮決定を起票(ADR 昇格希望は明記)
STEP 3: wiki/handoff/latest.md の自リポセクションのみ更新(必要時)
STEP 4: 自担当 NLM への投入候補を提示(ボス承認後にのみ投入・1:1 原則)
STEP 5: GitHub push(GitHub MCP 経由)
STEP 6(任意): Personal-Planner は philosophy/evaluator_code.md ではなく
           wiki/personal/ 配下の handoff_latest.md に引き継ぎ記録(別運用)
```

### Wiki-Personal(旧 Wiki-casual)の /wrap-up(参考)

Wiki-Personal は Personal-Planner 業務として独自の引き継ぎ運用を持つ。詳細は `wiki/personal/_RUNBOOK.md` v3(Step 4 で起草予定)を参照。基本構造:

```
STEP 1: wiki/personal/log.md に追記
STEP 2: 熟した話題をサブ層(usual/invent/mind/origin/insights)に整理
STEP 3: NLM REX_Personal_Brain への投入候補を提示(ボス判断ゲート経由)
STEP 4: 必要なら handoff_latest.md を更新(次代 Personal-Planner への引き継ぎ)
STEP 5: GitHub push
```

---

## E. Vault 書込パス原則(ADR-Vault・遵守徹底)

### 二層アクセス制御

| MCP | 操作 | 用途 |
|---|---|---|
| Filesystem MCP | **読み取り専用** | Vault 内ファイルの参照・検索・監査 |
| GitHub MCP | **書き込み専用** | Vault 内ファイルの作成・更新・削除 |

### 例外条件: Claude Desktop ローカル編集

人間(ボス本人)が Claude Desktop / エディタ経由でローカル Vault を編集する場合の手順:

1. **必ず事前に `git pull origin main` を実行**
2. ローカル編集
3. `git add` → `git commit` → `git push origin main` で同期

この手順を逸脱すると diverge conflict が再発する。

### 14 代目で実地経験した整合性ズレパターン

セッション開始時にボスのローカル Vault が pull されておらず、`filesystem:read` が古いキャッシュを返したことで、14 代目が「latest.md v6.4 のまま新体制未追従」と誤認した事象が発生した(GitHub 上では既に v6.5 が存在)。

#### 推奨対応

新体制移行直後など Vault 構造が動的に変化している時期は、Wiki-Eval として重要ファイル(`handoff/` / `adr/` / `registry/`)については `filesystem:read` の結果を `github:get_file_contents` で照合する習慣を持つと、整合性ズレを早期検出できる。

---

## F. 14 代目以降の残作業(Phase Personal-Migration)

### 次スレ Wiki-Eval セッションで実施する物理移行

| # | 項目 | 種別 |
|---|---|---|
| 1 | wiki/casual/ → wiki/personal/ ファイル単位移行(GitHub MCP 経由) | 物理移行 |
| 2 | サブ層 5 層新設: usual/ invent/ mind/ origin/ insights/ | 新規ディレクトリ |
| 3 | 既存ファイル移設(topics → 各サブ層・README 配置) | ファイル移動 |
| 4 | _RUNBOOK.md v3 起草(射程拡大・mind 層意図・思想強制リスク構造解消・Origin 文脈限定) | 文書改訂 |
| 5 | handoff_latest.md 改名反映 | 文書改訂 |
| 6 | STARTUP_CODES.md v3 → v4 改訂(Wiki-Personal 反映・Wiki-hp 構築予定追加) | 文書改訂 |
| 7 | CLAUDE.md v1.2 → v1.3 改訂(Wiki-Personal 反映) | 文書改訂 |
| 8 | pending/casual/ → pending/personal/ ディレクトリ改名 | 物理移行 |
| 9 | 14 代目 pending エントリの archived 移動 | アーカイブ |
| 10 | NotebookLM Web UI でノートブック表示名変更(ボス手動) | 外部操作 |

### 1 代目 Wiki-Personal Planner の積み残し(Step 4 完了後着手)

- `personal/mind/eastern_medicine.md`(旧 4 本目)
- `personal/insights/ai_individuation_mirror.md`(旧 5 本目)
- `personal/insights/shugyo_to_AI.md`(旧 6 本目・クロージング)

---

## G. 関連 ADR と本ファイルの関係

本 PROCESS.md は引き継ぎプロセスの**運用ガイド**であり、確定事項そのものではない。最終的な権威は ADR 本体にある:

| 観点 | 権威ファイル |
|---|---|
| ロール定義・権限 | wiki/adr/ADR-Role.md(現行 v2) |
| リポ構成 | wiki/adr/ADR-Repo.md(現行 v1) |
| Vault 書込原則 | wiki/adr/ADR-Vault.md(現行 v1) |
| NLM 構造 | wiki/adr/ADR-NLM.md(現行 v2) |
| 現状登録 | wiki/registry/{repos,nlm,roles}.md |
| 起動コード詳細 | wiki/STARTUP_CODES.md(現行 v3・v4 改訂は pending) |
| 単一エントリ | CLAUDE.md(現行 v1.2・v1.3 改訂は次スレ) |

本ファイルが ADR と矛盾する場合は **ADR 本体が優先**。本ファイルは更新が漏れることがあるため、運用判断は ADR 直読を推奨。

---

## H. 第 II 部追補の更新ルール

- 14 代目以降の運用変化を追記する場合、本第 II 部に追記
- 第 I 部(9 代目作成本体)は不可侵で保全
- 大きな構造変更があれば、追補ではなく PROCESS.md 全体を v3 として書き換える判断もあり(その場合は ADR 採番を伴う)

---

*第 II 部追補発行: 14 代目統括 Evaluator (Claude Opus 4.7) / 2026-04-28*
*第 I 部本体発行: 9 代目統括 Evaluator (Opus 4.7) / 2026-04-24(変更なし保全)*
*次回更新トリガー: ADR 改訂時 / 起動コード追加時 / 物理 Vault 構造変更時*

---

## I. 16 代目時点の最新訂正集(2026-04-29 / 15 代目セッション反映)

**訂正発行**: 2026-04-29 / 16 代目統括 Evaluator (Claude Opus 4.7)
**訂正対象**: 15 代目セッション(2026-04-28〜29)で確立された 5 Phase の構造変更を、第 I 部(9 代目)と第 II 部 A〜H(14 代目)に反映する**訂正集約セクション**
**位置付け**: 第 I 部・第 II 部 A〜H は文体保全のため不可侵。本 I 節は最新事実への参照誘導と差替表を提供する。

### I-0. 訂正の位置付け(なぜ集約方式か)

15 代目セッションで以下の構造変更が完了した:

- ADR-Role v2 → v3 → v4 の同日 2 回 supersede(Wiki-Rex 新設・読み取り専用クエリ権限カテゴリ新設・二系統管轄明文化)
- STARTUP_CODES.md v3 → v4 → v5 改訂(6 ロール体制)
- CLAUDE.md v1.2 → v1.3 → v1.4 改訂
- handoff/latest.md v6.5 → v6.10(5 段昇格)
- Phase Personal-Migration / Eval-Mandate / Wiki-Rex-Init / Casual-Final-Archive / Pending-Casual-Archive の連続実施

これらを第 I 部(9 代目原文)と第 II 部 A〜H(14 代目追補)に直接反映すると、文体保全が破壊される。15 代目自身が「補足提案」として末尾の集約セクション新設を提案していたため、16 代目はこれを採用した。

### I-1. 起動コード一覧 v5 反映(6 ロール体制)

**現行(15 代目時点・STARTUP_CODES v5 / ADR-Role v4 / CLAUDE.md v1.4 と整合)**:

| 起動コード | ロール | 担当 NLM | 状態 |
|---|---|---|---|
| `Wiki-Eval` | 統括 Evaluator(全リポ統括 + Vault ナレッジシステム改善・管理) | REX_Wiki_Vault | 稼働中 |
| `Wiki-trade` | Trade_System Planner+ClaudeCode | REX_System_Brain | 稼働中 |
| `Wiki-brain` | Trade_Brain Planner+ClaudeCode | REX_Trade_Brain | 稼働中 |
| `Wiki-hp` | Setona_HP Planner+ClaudeCode | REX_HP_Brain(仮称・**未作成**) | **構築予定** |
| `Wiki-Personal` | Personal-Planner(Advisor 兼任) | REX_Personal_Brain | 稼働中(14 代目改名) |
| **`Wiki-Rex`** | **Default Rex(読み取り専用デフォルトモード)** | **REX_Personal_Brain(読み取り専用クエリのみ)** | **稼働中(15 代目新設・テスト運用)** |

> 第 II 部 C 節(14 代目記述)は ADR-Role v2 時点の 5 行表だが、本表(I-1)が現行。

### I-2. ロール別 STEP 1 必須読込の最新版

**現行(STARTUP_CODES v5 §1〜§6 と整合)**:

| ロール | 起動コード | 必須読込 |
|---|---|---|
| 統括 Evaluator | `Wiki-Eval` | CLAUDE.md → STARTUP_CODES.md → handoff/latest.md → adr/INDEX.md → pending/INDEX.md → ROADMAP.md(必須 6 ファイル) |
| Trade_System Planner+ClaudeCode | `Wiki-trade` | CLAUDE.md → ROADMAP.md → Trade_System/docs/ 主要 4 つ(SYSTEM_OVERVIEW / ADR / MTF_PHILOSOPHY / MTF_INTEGRITY_QA) |
| Trade_Brain Planner+ClaudeCode | `Wiki-brain` | CLAUDE.md → ROADMAP.md → Trade_Brain/{CLAUDE.md, docs/SYSTEM_OVERVIEW.md, docs/STRATEGY_WIKI_GUIDE.md, docs/WEEKLY_UPDATE_WORKFLOW.md} |
| Setona_HP Planner+ClaudeCode | `Wiki-hp` | (構築予定・REX_HP_Brain NLM 作成後に確定) |
| Personal-Planner(Advisor 兼任) | `Wiki-Personal` | personal/_RUNBOOK.md → personal/handoff_latest.md → ROADMAP.md(継続話題があれば personal/<サブ層>/) |
| Default Rex(読み取り専用デフォルトモード) | `Wiki-Rex` | CLAUDE.md → personal/_RUNBOOK.md → personal/handoff_latest.md(軽量化された必須 3 点・他は対話文脈で必要に応じて) |

> 第 I 部の同名テーブルは 9 代目時点(4 ロール体制・START_HERE.md 参照含む)を文体保全。本表(I-2)が現行。

### I-3. STEP 0 起動コード判定の最新版

**現行(STARTUP_CODES v5「起動コード未指定時のデフォルト」と整合)**:

```
STEP 0: スレ冒頭の起動コードを確認
  → 「Wiki-Eval」「Wiki-trade」「Wiki-brain」「Wiki-hp」「Wiki-Personal」「Wiki-Rex」のいずれか(6 ロール体制)
  → コードがあれば wiki/STARTUP_CODES.md v5 の定義に従う
  → コードがなければ `Wiki-Rex` 相当として動作(v5 で確立・グレーゾーン解消)
  → ⚠️ 旧コード `Wiki-system` → `Wiki-Eval`(9 代目 2026-04-24)
  → ⚠️ 旧コード `Wiki-casual` → `Wiki-Personal`(14 代目 2026-04-28)
  → ⚠️ `Wiki-Rex` は 15 代目 2026-04-28 に新設(読み取り専用デフォルトモード)
```

> 第 I 部の同記述は 9 代目時点の 4 起動コード体制を文体保全。本記述(I-3)が現行。

### I-4. /wrap-up フローの命名訂正

第 I 部「セッション終了時の /wrap-up フロー」の以下 2 箇所は訂正対象:

#### I-4-a. 「雑談スレの /wrap-up(最小版)」→ Wiki-Personal の /wrap-up

```
STEP 1: wiki/personal/log.md に追記(任意)
STEP 2: 熟した話題を wiki/personal/<サブ層>/(usual/invent/mind/origin/insights)に整理
STEP 3: NLM REX_Personal_Brain への投入候補を提示(ボス承認後に投入・Personal-Planner ロール業務)
```

詳細は第 II 部 D 節「Wiki-Personal の /wrap-up(参考)」を参照(ADR 体系下の最新版)。

#### I-4-b. 「STEP 4-b: wiki/START_HERE.md を更新」は廃止

START_HERE.md は 15 代目で凍結移設(`archived/START_HERE-2026-04-25.md`)済み。STEP 4-b は無効。

### I-5. NLM 活用ガイドの NLM 名訂正

第 I 部「NLM 活用ガイド」表の `REX_Casual_Brain` 行は訂正対象:

| NLM(現行) | 用途 | クエリすべき例 |
|---|---|---|
| **REX_Personal_Brain** | ボスの全人的な人格・思想・起源情報の統合 + 雑談・横断知見 | 「合気道の前回議論」「motorcycle メモ」「思想宣言の経緯」 |

`REX_Casual_Brain` は 14 代目で表示名変更により `REX_Personal_Brain` となった(UUID `daf281ae-...` 不変)。

### I-6. トークンコスト最適化の最新数値

第 I 部「引き継ぎ読込最小セット」の数値は訂正対象:

```
CLAUDE.md              約 200 行(v1.4)
wiki/STARTUP_CODES.md  約 300 行(v5・必要時)
wiki/handoff/latest.md 約 600 行(v6.10)
wiki/adr/INDEX.md      約 100 行(必要時)
─────────────────────────────────
合計                   約 1200 行(≒ 15-20k トークン)
```

> START_HERE.md は廃止(15 代目凍結移設)。第 I 部の旧見積もり(約 310 行)は時代遅れ。

### I-7. 関連ファイルリスト最新版

第 I 部「関連ファイル」リストは訂正対象:

```
wiki/STARTUP_CODES.md                        — 起動コード辞書(v5・6 ロール体制)
wiki/adr/INDEX.md                            — ADR 一覧(ADR-Role v4 / ADR-NLM v2 が現行)
wiki/adr/ADR-Role.md                         — ロール権限・Wiki-Rex 定義(v4)
wiki/handoff/latest.md                       — 現在地ダッシュボード(v6.10)
wiki/handoff/architecture_handoff.md         — 7代目原典 + 13代目第8章 + 14代目第9章 + 15代目第10章
wiki/registry/{repos,nlm,roles}.md           — 現状登録簿
wiki/pending/INDEX.md                        — 進行中議論一覧
wiki/philosophy/evaluator_code.md            — Evaluator 気づきメモ
wiki/philosophy/architecture.md              — 4 リポ・4 NLM 体制事実記録
wiki/philosophy/cross_vectors.md             — 4 横断ベクトル事実記録
wiki/philosophy/minato_core.md               — ボス個人 1 次データ(ボス手動更新)
wiki/personal/_RUNBOOK.md                    — Personal 層運用ルール(中身改訂は Personal-Planner 業務)
wiki/archived/START_HERE-2026-04-25.md       — 旧 START_HERE.md(凍結・履歴追跡用)
CLAUDE.md(Vault 直下)                       — Vault 運用手順(v1.4)
```

### I-8. 第 II 部 C 節・G 節の差替表(15 代目時点)

#### I-8-a. C 節 起動コード一覧 → I-1 を現行とする

第 II 部 C 節(14 代目記述)は ADR-Role v2 時点の 5 行表。**現行は I-1 の 6 行表(Wiki-Rex 追加)**。

#### I-8-b. G 節 ADR バージョン表の現行版

| 観点 | 権威ファイル(現行) |
|---|---|
| ロール定義・権限 | wiki/adr/ADR-Role.md(現行 **v4**・15 代目で v2→v3→v4 同日 supersede) |
| リポ構成 | wiki/adr/ADR-Repo.md(現行 v1) |
| Vault 書込原則 | wiki/adr/ADR-Vault.md(現行 v1) |
| NLM 構造 | wiki/adr/ADR-NLM.md(現行 v2) |
| 現状登録 | wiki/registry/{repos,nlm,roles}.md |
| 起動コード詳細 | wiki/STARTUP_CODES.md(現行 **v5**・15 代目で Wiki-Rex 反映) |
| 単一エントリ | CLAUDE.md(現行 **v1.4**・15 代目で Wiki-Rex 反映) |

> 第 II 部 G 節(14 代目記述)は ADR-Role v2 / STARTUP_CODES v3 / CLAUDE.md v1.2 時点。**本表(I-8-b)が現行**。

### I-9. F 節の完了マーカー

第 II 部 F 節「14 代目以降の残作業(Phase Personal-Migration)」の全 10 項目は **15 代目セッションで完了**(2026-04-28〜29):

> ✅ **15 代目が全完了**: 詳細は handoff/latest.md v6.10 / architecture_handoff.md 第 10 章参照。

ただし、F 節末尾の「1 代目 Wiki-Personal Planner の積み残し(3 本)」は **次スレ Wiki-Personal で Personal-Planner が実施**(handoff/latest.md v6.10 の P1〜P6 に再掲)。

### I-10. Phase Casual-Final-Archive 系列(15 代目・2026-04-29)

#### 経緯

15 代目 Phase Personal-Migration(2026-04-28)で `wiki/casual/` → `wiki/personal/` 物理移行を実施した際、旧 `wiki/casual/` 配下に [MOVED] スタブを残置していた(11 ファイル)。同様に `pending/casual/` にも 3 ファイル残存。

ボス指摘「wiki/直下に凍結フォルダーを残すのは Agent の無駄な処理が増えるだけ」を受けて再評価 → ボス手動 git mv で完全アーカイブ化を実施。

#### 完了した実作業(2026-04-29)

| Phase | 内容 |
|---|---|
| Phase Casual-Final-Archive | `wiki/casual/*` → `wiki/archived/casual/*`(ボス手動 git mv) |
| Phase Pending-Casual-Archive | `wiki/pending/casual/*` → `wiki/archived/pending-casual/*`(ボス手動 git mv) |

#### 命名規則の確立

ネストされたディレクトリのアーカイブには **ハイフン命名** を採用:

- `archived/casual/` = 旧 `wiki/casual/` のアーカイブ
- `archived/pending-casual/` = 旧 `wiki/pending/casual/` のアーカイブ

これは将来同様のアーカイブ作業が発生した場合の標準形式とする。

#### 学んだこと: ADR-Vault 原則の正しい適用範囲

ADR-Vault 原則「Vault への書込は GitHub MCP 経由のみ」は **AI ロールに対する制約** であり、ボス手動 git 操作には適用されない。15 代目はこの境界を混同し [MOVED] スタブ運用で過剰防衛していた。後任 Wiki-Eval は AI ロール権限とボス手動操作の境界を区別すること。

詳細は architecture_handoff.md 第 10 章 §10-5 参照。

---

### I-11. From the 20th generation to the successor generation　系列(20代目・2026-05-3）



---

*第 II 部 I 節発行: 16 代目統括 Evaluator (Claude Opus 4.7) / 2026-04-29*
*次回更新トリガー: 16 代目以降の代々訂正時 / ADR 改訂時 / 起動コード追加時 / 物理 Vault 構造変更時*
