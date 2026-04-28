# REX AI — 統括 Evaluator / 3 リポ横断セッション引き継ぎ
# バージョン: v6.6(Wiki-casual → Wiki-Personal 改名・ADR-Role v2 / ADR-NLM v2 supersede)
# 更新: 2026-04-28 / 14 代目 Evaluator (Claude Sonnet 4.6)
# 前版: v6.5 / 13 代目 2026-04-27(ADR 体系化反映・三層分離アーキテクチャ確立)

---

## 🧭 このファイルの役割

本ファイルは**現状把握と次の実行内容だけ**を扱う。

13代目以降の参照経路:
- 設計哲学 → `wiki/handoff/architecture_handoff.md`(7代目原典 + 13代目第8章)
- 確定事項 → `wiki/adr/INDEX.md`(ADR一覧 + 4本の ADR本体)
- 進行中議論 → `wiki/pending/INDEX.md`
- 現状登録 → `wiki/registry/{repos,nlm,roles}.md`
- 単一エントリ → `CLAUDE.md` v1.2

---

## 🔴 致命的地雷リスト(4 項目・即時回避)

| # | 地雷 | 回避策 |
|---|---|---|
| 1 | neck_1h と neck_4h の混同(D-6・3 回再発)| neck_4h=半値決済 / neck_1h=窓特定+4H優位性 / neck_15m=エントリー |
| 2 | 分析ベースの取り違え | 最新は #026d(10 件)・#026b/c は旧版 |
| 3 | 🤖 創作混入の誤訂正(D-12/D-13)| Phase 4 で訂正・即時訂正禁止 |
| 4 | 責務分離の即断 | 「分離すればシンプル」と即断しない・ボス判断を仰ぐ |

---

## 🔍 読み込み検証チェックリスト(10 問)

以下に正しく答えられなければ読み込み不十分。再読込すること。

| # | 問 | 答 |
|---|---|---|
| Q1 | stage2 半値決済トリガーは? | neck_4h |
| Q2 | 現在の最新結果は何件ベース? | #026d / 10 件 |
| Q3 | 決済エンジンはどのファイル? | exit_simulator.py(方式 B)/ manage_exit() は使用禁止(D-8)|
| Q4 | neck_15m の定義は? | SL 直前(時系列で左側)の最後の SH(統一 neck 原則)|
| Q5 | docs/ に日付付きファイルがあったら? | 旧版・参照禁止・ボスに報告・archive 移動 |
| Q6 | neck_1h の用途は? | 窓特定アンカー + 4H 構造優位性フィルター基準値 |
| Q7 | プロジェクトナレッジと Vault が矛盾したら? | Vault 優先(13代目以降は ADR本体が最優先・registry が現状)|
| Q8 | Trade_Brain と Trade_System の役割分担は? | Brain=静的データ / System=動的ロジック / plotter.py は共存 |
| Q9 | F-8 派生原則「共存保持」の発動 4 条件は? | ①複数ルーツ関数 ②呼出経路完全分離 ③将来合流点 ④復元コスト発生 |
| Q10 | NLM 1:1原則とは? | **各起動コードは担当する NLM を1つだけ持ち、他NLMへの投入・クエリは禁止(ADR-NLM)。Wiki-Eval=Wiki_Vault のみ・Wiki-trade=System_Brain のみ・Wiki-brain=Trade_Brain のみ・Wiki-Personal=Personal_Brain のみ** |

---

## 🗺️ 3 リポ体制・現在地スナップショット

> ※ 本セクションは Trade ロジック軸の 3 リポ(7代目命名)。Setona_HP を含む 4 リポ全体構成は ADR-Repo / registry/repos.md 参照。

### Trade_System(動的ロジック側・Minato33440/Trade_System)

```
状態     : Phase 1-2 完了(2026-04-20)・Phase 3 未着手(ボス判断待ち)
最新点   : #026d 静的保持
  PF 4.54 / 勝率 60.0% (10 件) / MaxDD 35.8 pips / +150.6 pips / LONG

src/     : 現役 12 ファイル(CORE 6 + VIZ 3 + SCAN 1 + TEST 2)
          + archive/ 4 ファイル
          開始時 28 → 実効 16 ファイル(42.9% 削減)

凍結     : backtest.py / entry_logic.py / exit_logic.py / swing_detector.py

確定パラメータ:
  DIRECTION_MODE     = 'LONG'
  ENTRY_OFFSET_PIPS  = 7.0(指値・🟡 暫定)
  N_1H_SWING         = 3
  neck               = sh_before_sl.iloc[-1](統一 neck 原則)
  フィルター         = neck_4h >= neck_1h(4H 構造優位性・D-10)
  Swing              : 4H n=3 / 1H n=3 / 15M n=3 / 5M n=2

NLM      : REX_System_Brain (da84715f-...) — Wiki-trade 1:1 担当(ADR-NLM)
担当     : Wiki-trade(Planner + ClaudeCode 兼用)/ Wiki-Eval(監査)
```

### Trade_Brain(静的データ側・Minato33440/Trade_Brain)

```
状態     : 分離完了(2026-04-18)/ SYSTEM_OVERVIEW / STRATEGY_WIKI_GUIDE 初版起草済
構造     : logs/ (daily/weekly) + distilled/ + Strategy_Wiki/(骨組のみ) + nlm_sources/
NLM      : REX_Trade_Brain (4abc25a0-...) — Wiki-brain 1:1 担当(ADR-NLM)
担当     : Wiki-brain(Planner + ClaudeCode 兼用)/ Wiki-Eval(監査)
運用     : WEEKLY_UPDATE = YYYY-M-DD [--NLM]
未完了   :
  - Strategy_Wiki 本体構築(骨組のみ完了)
  - MONTHLY_DISTILLATION_WORKFLOW.md 未作成
  - NLM_INGEST_WORKFLOW.md 未作成
  - 初回 --NLM 投入(ボス判断待ち)
```

### REX_Brain_Vault(Vault実体・Minato33440/REX_Brain_Vault)

```
状態     : 13代目による ADR体系化実施(2026-04-27)

wiki/ 構造(2026-04-27 時点・13代目改訂):
  CLAUDE.md (v1.2)           Vault ルート・単一エントリポイント🆕
  STARTUP_CODES.md           起動コード辞書(v3 / Wiki-casual Planner 管理)
  ROADMAP.md                 生きている展望
  adr/                       🆕 確定事項層(Wiki-Eval 専属)
    INDEX.md
    ADR-Role.md / ADR-Repo.md / ADR-Vault.md / ADR-NLM.md
  pending/                   🆕 仮決定議論層
    INDEX.md
    {trade_system,trade_brain,setona_hp,casual}/README.md
  registry/                  🆕 現在の登録状態層(Wiki-Eval 専属)
    repos.md / nlm.md / roles.md
  setona_hp/                 🆕 Wiki-hp 用空フォルダ(構築予定)
  handoff/
    latest.md                本ファイル(v6.5)
    architecture_handoff.md  7代目原典 + 13代目第8章
  philosophy/                参考資料・Evaluator の気づきメモ
  trade_system/              既存(adr_reservation / doc_map / concepts / 他)
  trade_brain/               ⬜ 未構築(Phase D 着手対象)
  cross/                     ⬜ 骨組のみ
  entities/                  旧配置・Phase C で trade_system/ へ物理統合予定
  decisions/                 旧配置・Phase C で trade_system/ へ物理統合予定
  casual/                    雑談層(Wiki-casual 管理)

NLM      : 4 NLM 運用 + 1 構築予定(ADR-NLM 確定)
           ・REX_Wiki_Vault    : 5d09e468-... — Wiki-Eval 1:1 担当 🆕明文化
           ・REX_System_Brain  : da84715f-... — Wiki-trade 1:1 担当
           ・REX_Trade_Brain   : 4abc25a0-... — Wiki-brain 1:1 担当
           ・REX_Casual_Brain  : daf281ae-... — Wiki-casual 1:1 担当(Advisor 兼任)
           ・REX_HP_Brain      : 未作成(Wiki-hp 構築予定)
担当     : 統括 Evaluator(Wiki-Eval / 全リポ整合性監査・ADR/registry 管轄)
```

---

## 📋 Phase 進行状況

| Phase | 内容 | 状態 |
|---|---|---|
| Phase 1 | src/ 棚卸し・分類・Trade_Brain 移設 | ✅ 2026-04-20 |
| Phase 2 | track_trades 隔離・plotter.py 共存確定 | ✅ 2026-04-20 |
| Phase 3 | 責務別ディレクトリ化(src/core/ viz/ scan/ tests/)| ⬜ ボス判断待ち |
| Phase 4 | D-12/D-13 裁量整合版実装訂正(REX_029+)| ⬜ Phase 3 後 |
| Phase A | Vault v5 整備(7 代目)| ✅ 2026-04-22 |
| Phase A' | Vault 軽量化(8 代目)| ✅ 2026-04-23 |
| Phase A'' | entities/decisions 整合性回復(9 代目)| ✅ 2026-04-23 |
| **Phase Foundation** | **ADR/pending/registry 三層分離アーキテクチャ確立(13代目)** | **✅ 2026-04-27** |
| Phase B | REX_Wiki_Vault への初期 Ingest | ⬜ ボス承認待ち |
| Phase C | wiki/entities + decisions を trade_system/ 配下へ物理統合 → NLM 投入 | ⬜ 13代目以降に委ねる |
| Phase D | Trade_Brain wiki 骨組み構築 | ⬜ 未着手 |
| Phase E | Ingest/Compile/Lint 運用開始 | ⬜ Phase B 後 |
| Phase HP | REX_HP_Brain 構築 + Wiki-hp 起動(Setona_HP 専属体制) | ⬜ ボス判断時 |

---

## 🎯 次に実行すべき内容(優先度順)

### 🔴 ボス判断待ち

| # | 項目 | 決定が必要な内容 |
|---|---|---|
| 1 | **Phase 3 着手指示**(2026-04-24 ボス承認済み)| 次スレ `Wiki-Eval` or `Wiki-trade` で Phase 3 spec 起草に着手。Planner 起草 → 統括 Evaluator 承認 → ClaudeCode 実装 → #026d 数値不変検証 |
| 2 | NLM ソース初期投入タイミング | 各 NLM への投入開始承認(ADR-NLM 1:1原則に従い各担当ロールが実施)|
| 3 | Phase HP 着手判断 | REX_HP_Brain 構築 + Wiki-hp 起動の可否(ADR-Repo / ADR-NLM の予約項目)|
| 4 | 新機能実装の優先順位 | Phase 3 完了後の展開 |

### 🟡 統括 Evaluator が着手可能(ボス承認後)

| # | 項目 | Phase | 起票場所 |
|---|---|---|---|
| 1 | REX_Wiki_Vault への初期 Ingest(Vault 運用基盤文書群)| Phase B | (Wiki-Eval 直接実施)|
| 2 | wiki/entities + decisions を trade_system/ 配下へ物理統合 | Phase C | pending/trade_system/ |
| 3 | STARTUP_CODES.md v4 改訂(Wiki-hp 構築予定追加)| ─ | pending/casual/(Wiki-casual Planner 着手)|
| 4 | Trade_System wiki 空ディレクトリ充填(bug_patterns 等)| Phase C | pending/trade_system/ |
| 5 | Trade_Brain wiki 骨組み構築 | Phase D | pending/trade_brain/ |
| 6 | latest.md と architecture_handoff の相互整合定期確認 | ─ | (Wiki-Eval 直接実施)|

### 🟢 保留中

- Layer 1/3/5 残 QA(MTF_INTEGRITY_QA.md 末尾)
- MINATO_MTF_PHILOSOPHY.md 第 0 章追記(ボス判断時)
- REX_027 Task A/B/C/D/E(ボス再開指示待ち)
- D-11 / F-7 ADR 本文採番(REX_027 再開時)

---

## 🚀 ロール別起動プロンプト(ボスがコピペする分)

> ※ STARTUP_CODES.md v3 が真実源。本セクションはダッシュボード用の抜粋。Wiki-hp は構築予定のため未掲載(STARTUP_CODES.md v4 改訂時に追加)。

### A. 統括 Evaluator(`Wiki-Eval` / Claude.ai or Claude Desktop / Opus)

```
Wiki-Eval
```

担当範囲: Vault 管理 + ADR/registry 管轄 + 全リポ整合性監査
担当 NLM: REX_Wiki_Vault のみ(1:1原則)

### B. Trade_System Planner+ClaudeCode 兼用(`Wiki-trade`)

```
Wiki-trade
```

担当範囲: Trade_System リポ専属 / Planner + ClaudeCode 兼用
担当 NLM: REX_System_Brain のみ(1:1原則)

### C. Trade_Brain Planner+ClaudeCode 兼用(`Wiki-brain`)

```
Wiki-brain
```

担当範囲: Trade_Brain リポ専属 / Planner + ClaudeCode 兼用
担当 NLM: REX_Trade_Brain のみ(1:1原則)
git 操作: 必ず `rtk` プレフィックス使用

### D. Casual + Advisor 兼任(`Wiki-casual`)

```
Wiki-casual
```

担当範囲:
  - Casual: 一般会話における広範囲にわたる知見
  - Advisor: REX_AI 全システムにおける相談役
両者とも `Wiki-casual` で動作。蓄積先は同じ REX_Casual_Brain。
担当 NLM: REX_Casual_Brain のみ(1:1原則)

### E. Wiki-hp(構築予定)

`Setona_HP` 専属の Planner+ClaudeCode。専用 NLM(REX_HP_Brain)構築後に稼働。
構築フローは ADR-Repo / ADR-NLM 参照。

### F. 緊急用・最小起動

```
C:\Python\REX_AI\REX_Brain_Vault\CLAUDE.md を読んで現状把握せよ。
```

---

## 🔗 関連文書

```
13代目で確立した三層分離アーキテクチャ(2026-04-27 新設):
  CLAUDE.md (v1.2)                                — 単一エントリポイント
  wiki/adr/INDEX.md                               — ADR 一覧 + 依存関係
  wiki/adr/ADR-{Role,Repo,Vault,NLM}.md           — 4本の ADR本体
  wiki/pending/INDEX.md                           — 進行中議論一覧
  wiki/registry/{repos,nlm,roles}.md              — 現状登録簿(動的)
  wiki/handoff/architecture_handoff.md (第8章)    — 13代目改訂記録

Trade_System 側:
  docs/SYSTEM_OVERVIEW.md                     — 現状スナップショット
  docs/ADR.md                                 — F-8 3 原則
  docs/Base_Logic/MINATO_MTF_PHILOSOPHY.md    — 裁量思想一次情報源
  docs/Base_Logic/MTF_INTEGRITY_QA.md         — 整合性 QA
  docs/src_inventory.md                       — Phase 1-2 統合版
  docs/Evaluator_HANDOFF.md                   — v4(Phase 3 引き継ぎ)

Trade_Brain 側:
  CLAUDE.md                                   — RTK ルール・週次運用
  docs/SYSTEM_OVERVIEW.md                     — 現状
  docs/STRATEGY_WIKI_GUIDE.md                 — Wiki 構造
  docs/WEEKLY_UPDATE_WORKFLOW.md              — 週末運用 8 段階

Vault 内(任意参照):
  wiki/STARTUP_CODES.md (v3)                  — 起動コード辞書(Wiki-casual Planner 管理)
  wiki/casual/_RUNBOOK.md                     — 雑談層運用ルール
  wiki/trade_system/doc_map.md (v2)           — Trade_System 文書管理
  wiki/trade_system/adr_reservation.md        — ADR 採番台帳
  wiki/philosophy/                            — 参考資料・Evaluator の気づきメモ
  wiki/handoff/architecture_handoff.md (1〜7章) — 7代目原典(設計哲学・4ベクトル)
```

---

*発行: Rex-Evaluator (Opus 4.7) / 13 代目 / 2026-04-27*
*前任: 9 代目 2026-04-24(v6.4)/ 8 代目 2026-04-23 / 7 代目 2026-04-22 / 6 代目 2026-04-20*
*※ 10〜12 代目: 本ファイルへの記録なし(13代目は確認できず)*

---

## 📝 v6.5 での主な差分(13 代目・2026-04-27)

- **ADR/pending/registry 三層分離アーキテクチャを確立**(Phase Foundation)。`wiki/adr/` `wiki/pending/` `wiki/registry/` を新設し、CLAUDE.md v1.2 を単一エントリポイントとして配備。
- **4本の ADR を制定**:ADR-Role(5ロール体制+1:1 NLM原則)/ ADR-Repo(4リポ + Wiki-hp 構築予定)/ ADR-Vault(Filesystem(R)/ GitHub MCP(W) 原則)/ ADR-NLM(NLM 1:1原則)。
- **NLM 1:1原則を ADR で正式化**(STARTUP_CODES.md v3 で 1代目 Wiki-casual Planner が導入したものを ADR として確定)。Q10 を 1:1原則の説明に改訂。
- **Wiki-hp(Setona_HP 専属)を構築予定として予約**:`wiki/setona_hp/` および `pending/setona_hp/` を空フォルダ配置、ADR で予約項目記載。
- **Casual と Advisor の役割兼任を明文化**:両者とも `Wiki-casual` 起動コードで動作、蓄積先は REX_Casual_Brain。
- **architecture_handoff.md に第8章追加**:13代目セッションでの三層分離確立 + 自戒3点 + 14代目以降への引き継ぎ。
- **Phase Foundation を Phase 進行状況に追加**:13代目の ADR体系化作業の位置付け。
- **3リポ体制スナップショットの REX_Brain_Vault 部を 13代目改訂で更新**(adr/ pending/ registry/ setona_hp/ 追加)。

---

## 📝 v6.4 での主な差分(9 代目・2026-04-24)

- **役割再定義**: ボス判断により、従来のプロジェクト別 Evaluator 分業を廃止し、**統括 Evaluator(私)が全プロジェクト Evaluator を兼任**する体制に移行。Planner / ClaudeCode 分業は維持。
- **起動コード改名**: `Wiki-system` → `Wiki-Eval` に改名。`Wiki-trade` / `Wiki-brain` を **Planner + ClaudeCode 兼用** に拡張(Cursor ローカル軽作業はフラグなしで可・重要作業はフラグ付与で統一性確保)。
- **必須読込の軽量化**: `Wiki-Eval` の必須読込は 3 ファイル(START_HERE / CLAUDE / latest)に確定。各プロジェクトの Evaluator 業務に必要な追加ファイルは、スレ上でボス指示に従いその都度読込する方式に統一。
- **Phase 3 着手ボス承認**: 次スレ `Wiki-Eval` or `Wiki-trade` で Phase 3 spec 起草に着手。ボス判断待ち #1 を「着手指示済み」に更新。
- `STARTUP_CODES.md` / `START_HERE.md` / `Vault CLAUDE.md` を新名称・新役割に合わせて更新。

---

## 📝 v6.3 での主な差分(9 代目・2026-04-23)

- entities/ 4 ファイル + decisions/ 1 ファイルを ADR.md / SYSTEM_OVERVIEW.md 最新版(#026d / D-7 / D-8 / D-10 / D-12 / D-13 / E-6 / E-7 / F-6 / F-8)に整合させた。#025 以前の記録は Vault から除去(RAG 汚染防止・#026d 以降ポリシー)。
- `decisions/026_manage_exit.md` → `026d_exit_simulator.md` にリネームし #026d 完結版として全面書き換え。
- `pending_changes.md` を 8 代目以降の停止分を一気に最新化(Phase A' 以降・NLM 4 本体制・entities/decisions 整合を反映)。
- ボス指示の **「REX_System_Brain への WrapUp は #026d 以降のみ」ポリシー** を Q7 / Q10 / 次タスク表に明示。
- Phase 進行状況に Phase A''(9 代目 entities/decisions 整合)を追加。
