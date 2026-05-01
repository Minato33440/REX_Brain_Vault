# pending_changes.md — 決定済み未確定設計変更トラッカー
# 管理: 統括 Evaluator（REX_Brain_System 設計責任者）
# 更新: 2026-04-23（9 代目セッション末・8 代目以降の停止分を一気に最新化）
# 前版: 2026-04-18（Wiki 構築 Phase 1 開始 + 独立リポ化完了時点）

---

## 本ファイルの役割

「決定はされたが未確定（実施途中・実施待ち・予約中）」の設計変更を一元管理する。
完了済みは「完了済み履歴」セクションへ移動・古い完了履歴は archive に追い出す。

---

## 🔴 進行中・未確定（現時点で動いているもの）

| 決定日 | トピック | 状態 | 担当 / ADR |
|---|---|---|---|
| 2026-04-23 | NLM 凍結解除済・**ソース投入はボス承認待ち** | ⏳ ボス承認待ち | 統括 Evaluator |
| 2026-04-22 | Phase 3（src/ 責務別ディレクトリ化） | ⏳ ボス判断待ち | Trade_System Planner / Evaluator |
| — | Phase 4（D-12 / D-13 裁量整合版実装訂正・REX_029 以降） | ⏳ Phase 3 完了後 | Trade_System Planner / Evaluator |
| 2026-04-23 | Phase B（REX_Wiki_Vault への初期 Ingest） | ⏳ ボス承認待ち | 統括 Evaluator |
| 2026-04-23 | Phase C（wiki/entities/ + wiki/decisions/ を `trade_system/` 配下へ物理統合） | ⏳ Phase B 完了後・ボス確定「選択肢 B」 | 統括 Evaluator |
| — | Phase D（wiki/trade_brain/ 骨組み構築） | ⏳ 未着手 | 統括 Evaluator |

---

## ⏳ 予約保持（REX_027 再開待ち）

| 番号 | 内容 | 担当 | 再開トリガー |
|---|---|---|---|
| ADR D-11 | Trade_Brain 分離 + NLM RAG 全面再構築 | Advisor / Evaluator | REX_027 Task A 着手指示 |
| ADR F-7 | Vault 構造標準化 + RAG 管理方針 | Advisor / Evaluator | REX_027 Task A 着手指示 |
| MINATO_MTF_PHILOSOPHY 第 0 章追記 | 原則 α/β/γ 正式反映 | Evaluator | ボス承認時 |
| Layer 1/3/5 残 QA | MTF_INTEGRITY_QA.md への追記 | Evaluator | 原則γ（システム安定後） |

---

## ✅ 完了済み履歴（直近・8 代目以降）

| 完了日 | トピック | ADR / 関連文書 |
|---|---|---|
| 2026-04-23 | **wiki/entities + decisions の #026d 以降への整合性回復**（9 代目）| 本セッション ・ entities 4 ファイル + decisions リネーム + 全面書き換え |
| 2026-04-23 | `wiki/decisions/025_fixed_neck.md` 削除（ボス手動 + push） | A-5（#026a で統一 neck 原則に転換済み） |
| 2026-04-23 | NLM 凍結解除宣言（システム系 3 NLM）| 8 代目 Phase A' 拡張 |
| 2026-04-23 | `wiki/handoff/PROCESS.md` 新設（引き継ぎプロセス要点一元化）| 8 代目セッション末 |
| 2026-04-23 | `wiki/philosophy/minato_core.md` をボス手動更新ファイルに性質変更 | 8 代目 |
| 2026-04-23 | `wiki/STARTUP_CODES.md` 新設（Wiki-system / trade / brain / casual）| 8 代目 Phase A' 拡張 |
| 2026-04-23 | REX_Wiki_Vault NLM 設立（5d09e468-...） | 8 代目 |
| 2026-04-23 | REX_Casual_Brain NLM 設立（daf281ae-...）+ wiki/casual/ 層新設 | 8 代目 |
| 2026-04-23 | `wiki/handoff/latest.md` v6 → v6.2（軽量化・NLM 4 本体制反映）| 8 代目 |
| 2026-04-23 | `wiki/philosophy/` 4 ファイル分離（軽量化対応）| 8 代目 Phase A' |
| 2026-04-23 | `wiki/START_HERE.md` 新設（100 行以内入口）| 8 代目 |
| 2026-04-22 | `wiki/index.md` v2 / `wiki/trade_system/doc_map.md` v2 全面改訂 | 7 代目 Phase A |
| 2026-04-22 | `wiki/handoff/latest.md` v5（統括 Evaluator 化対応）| 7 代目 |
| 2026-04-20 | REX_028 Phase 1 完了（src/ 棚卸し・分類・Trade_Brain 移設）| ADR E-8 |
| 2026-04-20 | REX_028 Phase 2 完了（track_trades 隔離・plotter.py 共存方針確定）| ADR F-8 派生原則 |
| 2026-04-20 | ADR D-12 / D-13 / E-8 / F-8 採番完了 | ADR.md |

---

## ✅ 完了済み履歴（#026 シリーズ・参考）

| 完了日 | トピック | ADR |
|---|---|---|
| 2026-04-17 | #026d 完了（4H 構造優位性フィルター追加） | D-10 |
| 2026-04-17 | 全設計文書最新化 | — |
| 2026-04-15 | 指値方式（neck + 7pips） | D-9 / E-7 |
| 2026-04-15 | exit_simulator 方式 B 正式採用 | D-8 |
| 2026-04-15 | 1H Swing n=2 → n=3 | D-7 |
| 2026-04-15 | 統一 neck 原則 | A-5 |

---

## 📋 本ファイルの運用ルール

- 設計判断のたびに即更新（停止期間を作らない・8 代目までの 5 日停止は再発防止）
- 完了から 1 ヶ月経過した履歴は別ファイル `pending_changes_archive_YYYY-MM.md` に切り出し可
- 進行中・予約保持・完了の 3 ステータスを明確に分離
- ADR 採番された項目は ADR 番号を必ず併記（追跡性）
- Phase 名（Phase 1-4 / Phase A-E）は他文書（latest.md / doc_map.md）と統一語彙

---

*管理: 統括 Evaluator / 9 代目更新: 2026-04-23*
