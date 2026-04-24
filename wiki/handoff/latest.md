# REX AI — 統括 Evaluator / 3 リポ横断セッション引き継ぎ
# バージョン: v6.4（役割再定義反映・起動コード改名反映・Phase 3 着手準備反映）
# 更新: 2026-04-24 / 9 代目 Evaluator (Claude Opus 4.7)
# 前版: v6.3 / 9 代目 2026-04-23（entities/decisions 整合性回復）

---

## 🧭 このファイルの役割

本ファイルは**現状把握と次の実行内容だけ**を扱う。

---

## 🔴 致命的地雷リスト（4 項目・即時回避）

| # | 地雷 | 回避策 |
|---|---|---|
| 1 | neck_1h と neck_4h の混同（D-6・3 回再発）| neck_4h=半値決済 / neck_1h=窓特定+4H優位性 / neck_15m=エントリー |
| 2 | 分析ベースの取り違え | 最新は #026d（10 件）・#026b/c は旧版 |
| 3 | 🤖 創作混入の誤訂正（D-12/D-13）| Phase 4 で訂正・即時訂正禁止 |
| 4 | 責務分離の即断 | 「分離すればシンプル」と即断しない・ボス判断を仰ぐ |

---

## 🔍 読み込み検証チェックリスト（10 問）

以下に正しく答えられなければ読み込み不十分。再読込すること。

| # | 問 | 答 |
|---|---|---|
| Q1 | stage2 半値決済トリガーは？ | neck_4h |
| Q2 | 現在の最新結果は何件ベース？ | #026d / 10 件 |
| Q3 | 決済エンジンはどのファイル？ | exit_simulator.py（方式 B）/ manage_exit() は使用禁止（D-8）|
| Q4 | neck_15m の定義は？ | SL 直前（時系列で左側）の最後の SH（統一 neck 原則）|
| Q5 | docs/ に日付付きファイルがあったら？ | 旧版・参照禁止・ボスに報告・archive 移動 |
| Q6 | neck_1h の用途は？ | 窓特定アンカー + 4H 構造優位性フィルター基準値 |
| Q7 | プロジェクトナレッジと Vault が矛盾したら？ | Vault 優先（全 4 NLM 凍結解除済・ソース投入はボス承認待ち、そのうち REX_System_Brain は **#026d 以降のみ投入**）|
| Q8 | Trade_Brain と Trade_System の役割分担は？ | Brain=静的データ / System=動的ロジック / plotter.py は共存 |
| Q9 | F-8 派生原則「共存保持」の発動 4 条件は？ | ①複数ルーツ関数 ②呼出経路完全分離 ③将来合流点 ④復元コスト発生 |
| Q10 | NLM 現状は？ | **2026-04-23 凍結解除宣言・全 4 NLM 運用可能（ソース投入はボス承認待ち、REX_System_Brain は #026d 以降のみ投入ポリシー）** |

---

## 🗺️ 3 リポ体制・現在地スナップショット

### Trade_System（動的ロジック側・Minato33440/Trade_System）

```
状態     : Phase 1-2 完了（2026-04-20）・Phase 3 未着手（ボス判断待ち）
最新点   : #026d 静的保持
  PF 4.54 / 勝率 60.0% (10 件) / MaxDD 35.8 pips / +150.6 pips / LONG

src/     : 現役 12 ファイル（CORE 6 + VIZ 3 + SCAN 1 + TEST 2）
          + archive/ 4 ファイル
          開始時 28 → 実効 16 ファイル（42.9% 削減）

凍結     : backtest.py / entry_logic.py / exit_logic.py / swing_detector.py

確定パラメータ:
  DIRECTION_MODE     = 'LONG'
  ENTRY_OFFSET_PIPS  = 7.0（指値・🟡 暫定）
  N_1H_SWING         = 3
  neck               = sh_before_sl.iloc[-1]（統一 neck 原則）
  フィルター         = neck_4h >= neck_1h（4H 構造優位性・D-10）
  Swing              : 4H n=3 / 1H n=3 / 15M n=3 / 5M n=2

NLM      : REX_System_Brain (da84715f-...) 凍結中
担当     : Rex-Planner（Sonnet）/ Evaluator（Opus）/ ClaudeCode
```

### Trade_Brain（静的データ側・Minato33440/Trade_Brain）

```
状態     : 分離完了（2026-04-18）/ SYSTEM_OVERVIEW / STRATEGY_WIKI_GUIDE 初版起草済
構造     : logs/ (daily/weekly) + distilled/ + Strategy_Wiki/(骨組のみ) + nlm_sources/
NLM      : REX_Trade_Brain (4abc25a0-...) 凍結中
担当     : Advisor / Planner / ClaudeCode（Sonnet）※ Evaluator 関与せず
運用     : WEEKLY_UPDATE = YYYY-M-DD [--NLM]
未完了   :
  - Strategy_Wiki 本体構築（骨組のみ完了）
  - MONTHLY_DISTILLATION_WORKFLOW.md 未作成
  - NLM_INGEST_WORKFLOW.md 未作成
  - 初回 --NLM 投入（ボス判断待ち）
```

### Rex_Brain_Vault（ハブ層・Minato33440/REX_Brain_Vault）

```
状態     : 8 代目による Phase A' 実施（2026-04-23）

wiki/ 構造（2026-04-23 時点）:
  START_HERE.md              新スレ入口（100 行以内）
  index.md (v2)              全ページ目次
  log.md                     時系列ログ（追記のみ）
  philosophy/                参考資料・Evaluator の気づきメモ
  handoff/
    latest.md                本ファイル（v6.3）
    architecture_handoff.md  7 代目セッション記録（保全）
  trade_system/              既存（adr_reservation / doc_map / concepts / 他）
  trade_brain/               ⬜ 未構築（Phase D 着手対象）
  cross/                     ⬜ 骨組のみ
  entities/                  旧配置（✅ #026d 以降に整合済・9 代目 2026-04-23）・Phase C で trade_system/ へ物理統合予定
  decisions/                 旧配置（✅ #026d 完結版 1 件・025_fixed_neck はボス削除済）・Phase C で trade_system/ へ物理統合予定

NLM      : 下記 4 NLM への横断参照想定（全て運用解凍 🆕 2026-04-23）
           ・REX_System_Brain  : da84715f-... （ソース投入待ち）
           ・REX_Trade_Brain   : 4abc25a0-... （ソース投入待ち）
           ・REX_Wiki_Vault    : 5d09e468-... （ソース投入待ち）
           ・REX_Casual_Brain  : daf281ae-... （ソース投入待ち・実戦で育てる）
担当     : 統括 Evaluator（全リポ整合性監査）
```

---

## 📋 Phase 進行状況

| Phase | 内容 | 状態 |
|---|---|---|
| Phase 1 | src/ 棚卸し・分類・Trade_Brain 移設 | ✅ 2026-04-20 |
| Phase 2 | track_trades 隔離・plotter.py 共存確定 | ✅ 2026-04-20 |
| Phase 3 | 責務別ディレクトリ化（src/core/ viz/ scan/ tests/）| ⬜ ボス判断待ち |
| Phase 4 | D-12/D-13 裁量整合版実装訂正（REX_029+）| ⬜ Phase 3 後 |
| Phase A | Vault v5 整備（7 代目）| ✅ 2026-04-22 |
| **Phase A'** | **Vault 軽量化（8 代目）**| **✅ 2026-04-23** |
| **Phase A''** | **entities/decisions 整合性回復（9 代目）**| **✅ 2026-04-23** |
| Phase B | REX_Wiki_Vault への初期 Ingest（NLM 設立済・ソース投入待ち）| ⬜ ボス承認待ち |
| Phase C | wiki/entities + decisions を trade_system/ 配下へ物理統合 → NLM 投入 | ⬜ Phase B 後（ボス選択肢 B）|
| Phase D | Trade_Brain wiki 骨組み構築 | ⬜ 未着手 |
| Phase E | Ingest/Compile/Lint 運用開始 | ⬜ Phase B 後 |

---

## 🎯 次に実行すべき内容（優先度順）

### 🔴 ボス判断待ち

| # | 項目 | 決定が必要な内容 |
|---|---|---|
| 1 | **Phase 3 着手指示**（**2026-04-24 ボス承認済み**）| 次スレ `Wiki-Eval` or `Wiki-trade` で Phase 3 spec 起草に着手。Planner 起草 → 統括 Evaluator 承認 → ClaudeCode 実装 → #026d 数値不変検証 |
| 2 | NLM ソース初期投入タイミング | REX_Wiki_Vault / REX_System_Brain / REX_Trade_Brain への投入開始承認（Phase B）|
| 3 | 新機能実装の優先順位 | Phase 3 完了後の展開：ロット調整 / ボラ係数 / Trade_Brain 合流 のいずれか |

### 🟡 統括 Evaluator が着手可能（ボス承認後）

| # | 項目 | Phase | 見積 |
|---|---|---|---|
| 1 | REX_Wiki_Vault への初期 Ingest（Vault 運用基盤文書群）| Phase B | 1 セッション |
| 2 | REX_System_Brain への初期 Ingest（**#026d 以降のみ**）| Phase B 並行可 | 1 セッション |
| 3 | REX_Trade_Brain への初期 Ingest | Phase B 並行可 | 1 セッション |
| 4 | wiki/entities + decisions を trade_system/ 配下へ物理統合 | Phase C | 軽微 |
| 5 | `handoff/trade_system_brief.md` / `trade_brain_brief.md` 新設 | Phase A' 追補 | 1 セッション各 |
| 6 | `trade_brain/_RUNBOOK.md` 先行作成（非対称性解消）| Phase D 準備 | 軽微 |
| 7 | Trade_System wiki 空ディレクトリ充填（bug_patterns 等）| Phase C | 複数セッション |

### 🟢 保留中

- Layer 1/3/5 残 QA（MTF_INTEGRITY_QA.md 末尾）
- MINATO_MTF_PHILOSOPHY.md 第 0 章追記（ボス判断時）
- REX_027 Task A/B/C/D/E（ボス再開指示待ち）
- D-11 / F-7 ADR 本文採番（REX_027 再開時）

---

## 🚀 ロール別起動プロンプト（ボスがコピペする分）

### A. 統括 Evaluator（`Wiki-Eval` / Claude.ai Opus）

```
Wiki-Eval
```

**または明示版**:

```
このスレでは REX AI 3 リポ体制の統括 Evaluator として働いてほしい。
全プロジェクト Evaluator を兼任し、Vault 管理も担当する。

⚠️ 作業開始前に以下を順番に読め（必須 3 ファイルのみ）:
  ① C:\Python\REX_AI\REX_Brain_Vault\wiki\START_HERE.md（新スレ最初の入口）
  ② C:\Python\REX_AI\REX_Brain_Vault\CLAUDE.md（Vault 運用手順）
  ③ C:\Python\REX_AI\REX_Brain_Vault\wiki\handoff\latest.md（現在地ダッシュボード）

読み込み完了後、latest.md の「読み込み検証チェックリスト」全 10 問に回答してから開始。
各プロジェクトの Evaluator 業務に必要な追加ファイルは、
私の指示でその都度読み込む形で良い（STARTUP_CODES.md 参照）。

担当範囲: Vault 管理 + Trade_System ・ Trade_Brain Evaluator 兼任 + 3 リポ整合性監査
NLM:
  REX_System_Brain : da84715f-9719-40ef-87ec-2453a0dce67e（ソース投入待ち）
  REX_Trade_Brain  : 4abc25a0-4550-4667-ad51-754c5d1d1491（ソース投入待ち）
  REX_Wiki_Vault   : 5d09e468-3a96-4906-af27-3400c50a0275（ソース投入待ち）
  REX_Casual_Brain : daf281ae-e310-400f-961a-20db58b98e01（ソース投入待ち）
```

### B. Trade_System Planner + ClaudeCode 兼用（`Wiki-trade` / Claude.ai Opus/Sonnet or Cursor）

```
Wiki-trade
```

**または明示版**:

```
このスレでは Trade_System プロジェクトの Planner + ClaudeCode として働いてほしい。

⚠️ 作業開始前に以下を順番に読め:
  ① C:\Python\REX_AI\REX_Brain_Vault\wiki\START_HERE.md（3 リポ現在地）
  ② C:\Python\REX_AI\Trade_System\docs\SYSTEM_OVERVIEW.md（Trade_System 現状）
  ③ C:\Python\REX_AI\Trade_System\docs\ADR.md（判断記録・F-8 3 原則）
  ④ C:\Python\REX_AI\Trade_System\docs\Base_Logic\MINATO_MTF_PHILOSOPHY.md（裁量思想）
  ⑤ C:\Python\REX_AI\Trade_System\docs\Base_Logic\MTF_INTEGRITY_QA.md（整合性 QA）

実装担当時の追加読込:
  ⑥ C:\Python\REX_AI\Trade_System\docs\src_inventory.md（src/ 構造）
  ⑦ C:\Python\REX_AI\Trade_System\docs\EX_DESIGN_CONFIRMED.md（エントリー設計）
  ⑧ C:\Python\REX_AI\Trade_System\.CLAUDE.md（不変ルール・凍結ファイル）

業務分岐:
  - 草案起草: spec を起草 → Wiki-Eval で監査依頼 → 承認後実装
  - 軽微な実装（Cursor ローカル）: フラグなしで実行可
  - 重要な実装（新 Phase 着手・凍結ファイル周辺・ADR 採番を伴う変更）: Wiki-trade フラグ付与
実装結果は Wiki-Eval で監査してもらう前提で作業。

NLM: REX_System_Brain (da84715f-9719-40ef-87ec-2453a0dce67e)
```

### C. Trade_Brain Planner + ClaudeCode 兼用（`Wiki-brain` / Claude.ai Opus/Sonnet or Cursor）

```
Wiki-brain
```

**または明示版**:

```
このスレでは Trade_Brain プロジェクトの Planner + ClaudeCode として働いてほしい。

⚠️ 作業開始前に以下を順番に読め:
  ① C:\Python\REX_AI\REX_Brain_Vault\wiki\START_HERE.md（3 リポ現在地）
  ② C:\Python\REX_AI\Trade_Brain\CLAUDE.md（Trade_Brain 運用・RTK ルール）
  ③ C:\Python\REX_AI\Trade_Brain\docs\SYSTEM_OVERVIEW.md（Trade_Brain 現状）
  ④ C:\Python\REX_AI\Trade_Brain\docs\STRATEGY_WIKI_GUIDE.md（Wiki 構造）
  ⑤ C:\Python\REX_AI\Trade_Brain\docs\WEEKLY_UPDATE_WORKFLOW.md（週末運用）

業務分岐: Wiki-trade と同じ（Cursor ローカル軽作業 = フラグなし / 重要作業 = フラグ付与）
実装結果の監査は Wiki-Eval で統括 Evaluator に依頼。

NLM: REX_Trade_Brain (4abc25a0-4550-4667-ad51-754c5d1d1491)
⚠️ git 操作は必ず rtk プレフィックスを使う。
```

### E. 雑談スレ（REX_AI システム業務外）

```
このスレではシステム業務ではなく、雑談・個人的話題を扱う。
ミナトと呼ぶ（プロジェクト進行時の「ボス」ではない）。

⚠️ 作業開始前に以下だけ確認:
  ① C:\Python\REX_AI\REX_Brain_Vault\wiki\casual\_RUNBOOK.md（運用ルール）
  ② 継続話題があれば casual/topics/ 該当ページ

⚠️ システム業務用の START_HERE.md / latest.md / philosophy/ は読まない。
   REX_AI システム引き継ぎ文脈と物理分離する。

NLM: REX_Casual_Brain (daf281ae-e310-400f-961a-20db58b98e01)
```

※ 上記はスレ冒頭で `Wiki-casual` / `Wiki-cusuaru` / `ウィキ雑談` と打つだけでも起動可（詳細 `wiki/STARTUP_CODES.md`）。

### F. 緊急用・最小起動

```
C:\Python\REX_AI\REX_Brain_Vault\wiki\START_HERE.md を読んで現状把握せよ。
```

---

## 🔗 関連文書

```
Trade_System 側:
  docs/SYSTEM_OVERVIEW.md                     — 現状スナップショット
  docs/ADR.md                                 — F-8 3 原則
  docs/Base_Logic/MINATO_MTF_PHILOSOPHY.md    — 裁量思想一次情報源
  docs/Base_Logic/MTF_INTEGRITY_QA.md         — 整合性 QA
  docs/src_inventory.md                       — Phase 1-2 統合版
  docs/Evaluator_HANDOFF.md                   — v4（Phase 3 引き継ぎ）

Trade_Brain 側:
  CLAUDE.md                                   — RTK ルール・週次運用
  docs/SYSTEM_OVERVIEW.md                     — 現状
  docs/STRATEGY_WIKI_GUIDE.md                 — Wiki 構造
  docs/WEEKLY_UPDATE_WORKFLOW.md              — 週末運用 8 段階

Vault 内（任意参照）:
  wiki/STARTUP_CODES.md                       — 起動コード辞書（Wiki-system/trade/brain/casual）
  wiki/casual/_RUNBOOK.md                     — 雑談層運用ルール（🆕 2026-04-23）
  wiki/trade_system/doc_map.md (v2)           — Trade_System 文書管理
  wiki/trade_system/adr_reservation.md        — ADR 採番台帳
  wiki/philosophy/                            — 参考資料・Evaluator の気づきメモ
  wiki/handoff/architecture_handoff.md        — 7 代目セッション記録
```

---

*発行: Rex-Evaluator (Opus 4.7) / 9 代目 / 2026-04-24*
*前任: 9 代目 2026-04-23 / 8 代目 2026-04-23 / 7 代目 2026-04-22 / 6 代目 2026-04-20*

---

## 📝 v6.4 での主な差分（9 代目・2026-04-24）

- **役割再定義**: ボス判断により、従来のプロジェクト別 Evaluator 分業を廃止し、**統括 Evaluator（私）が全プロジェクト Evaluator を兼任**する体制に移行。Planner / ClaudeCode 分業は維持。
- **起動コード改名**: `Wiki-system` → `Wiki-Eval` に改名。`Wiki-trade` / `Wiki-brain` を **Planner + ClaudeCode 兼用** に拡張（Cursor ローカル軽作業はフラグなしで可・重要作業はフラグ付与で統一性確保）。
- **必須読込の軽量化**: `Wiki-Eval` の必須読込は 3 ファイル（START_HERE / CLAUDE / latest）に確定。各プロジェクトの Evaluator 業務に必要な追加ファイルは、スレ上でボス指示に従いその都度読込する方式に統一。
- **Phase 3 着手ボス承認**: 次スレ `Wiki-Eval` or `Wiki-trade` で Phase 3 spec 起草に着手。ボス判断待ち #1 を「着手指示済み」に更新。
- `STARTUP_CODES.md` / `START_HERE.md` / `Vault CLAUDE.md` を新名称・新役割に合わせて更新。

---

## 📝 v6.3 での主な差分（9 代目・2026-04-23）

- entities/ 4 ファイル + decisions/ 1 ファイルを ADR.md / SYSTEM_OVERVIEW.md 最新版（#026d / D-7 / D-8 / D-10 / D-12 / D-13 / E-6 / E-7 / F-6 / F-8）に整合させた。#025 以前の記録は Vault から除去（RAG 汚染防止・#026d 以降ポリシー）。
- `decisions/026_manage_exit.md` → `026d_exit_simulator.md` にリネームし #026d 完結版として全面書き換え。
- `pending_changes.md` を 8 代目以降の停止分を一気に最新化（Phase A' 以降・NLM 4 本体制・entities/decisions 整合を反映）。
- ボス指示の **「REX_System_Brain への WrapUp は #026d 以降のみ」ポリシー** を Q7 / Q10 / 次タスク表に明示。
- Phase 進行状況に Phase A''（9 代目 entities/decisions 整合）を追加。
