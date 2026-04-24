# 引き継ぎプロセス — PROCESS.md

**役割**: 引き継ぎプロセスの**要点と運用原則**を一元化したリファレンス。
**位置付け**: `latest.md`（=現在地データ）と並列。本ファイルは**方法論・運用ガイド**。
**最終更新**: 2026-04-24 / 9 代目統括 Evaluator（役割再定義・起動コード改名・Phase 命名規則追加・旧 NLM 参照除去）
**前版**: 2026-04-23 / 8 代目統括 Evaluator（初版）
**読み手**: 統括 Evaluator / Planner / ClaudeCode / Advisor

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
