# REX AI — 統括 Evaluator / 3 リポ横断セッション引き継ぎ

# バージョン: v6.7(Phase Personal-Migration 物理移行完了・ADR-Role v3 supersede・運用文書 v4/v1.3 改訂反映)
# 更新: 2026-04-28 / 15 代目 Evaluator (Claude Opus 4.7)
# 前版: v6.6 / 14 代目 2026-04-28(Wiki-Personal 改名 ADR 化 Step 3 完了)
# 前々版: v6.5 / 13 代目 2026-04-27(ADR 体系化反映・三層分離アーキテクチャ確立)
# 注: 10〜12 代目の更新は本ファイルに記録なし(13 代目時点で確認できず)

---

## 🧭 このファイルの役割

本ファイルは**現状把握と次の実行内容だけ**を扱う。

13代目以降の参照経路:
- 設計哲学 → `wiki/handoff/architecture_handoff.md`(7代目原典 + 13代目第8章 + 14代目第9章 + 15代目追記予定)
- 確定事項 → `wiki/adr/INDEX.md`(ADR一覧 + 4本の ADR本体・**ADR-Role v3 / ADR-NLM v2** が現行)
- 進行中議論 → `wiki/pending/INDEX.md`
- 現状登録 → `wiki/registry/{repos,nlm,roles}.md`
- 単一エントリ → `CLAUDE.md` v1.3
- 起動コード仕様 → `wiki/STARTUP_CODES.md` v4

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
| Q10 | NLM 1:1原則とは? | **各起動コードは担当する NLM を1つだけ持ち、他NLMへの投入・クエリは禁止(ADR-NLM v2)。Wiki-Eval=Wiki_Vault のみ・Wiki-trade=System_Brain のみ・Wiki-brain=Trade_Brain のみ・Wiki-Personal=Personal_Brain のみ(旧 Casual_Brain・UUID 不変)** |

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

NLM      : REX_System_Brain (da84715f-...) — Wiki-trade 1:1 担当(ADR-NLM v2)
担当     : Wiki-trade(Planner + ClaudeCode 兼用)/ Wiki-Eval(監査)
```

### Trade_Brain(静的データ側・Minato33440/Trade_Brain)

```
状態     : 分離完了(2026-04-18)/ SYSTEM_OVERVIEW / STRATEGY_WIKI_GUIDE 初版起草済
構造     : logs/ (daily/weekly) + distilled/ + Strategy_Wiki/(骨組のみ) + nlm_sources/
NLM      : REX_Trade_Brain (4abc25a0-...) — Wiki-brain 1:1 担当(ADR-NLM v2)
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
状態     : 15 代目による Phase Personal-Migration 物理移行完了(2026-04-28)
            + ADR-Role v3 supersede(二系統管轄明文化)
            + STARTUP_CODES v4 / CLAUDE.md v1.3 / latest.md v6.7 改訂
            ※ 14 代目による Wiki-Personal 改名 ADR 化(2026-04-28)を継承
            ※ 13 代目による ADR 体系化(2026-04-27)を継承

wiki/ 構造(2026-04-28 v6.7 時点・15 代目反映):
  CLAUDE.md (v1.3 🆕)         Vault ルート・単一エントリポイント
  STARTUP_CODES.md (v4 🆕)    起動コード辞書(Wiki-Eval 直接管理・v3 §12 訂正反映)
  ROADMAP.md                  生きている展望
  archived/                   ⬜ 凍結ファイル保管
    START_HERE-2026-04-25.md  (旧 wiki/START_HERE.md・15 代目で凍結移設)
  adr/                        確定事項層(Wiki-Eval 専属)
    INDEX.md (v3 supersede 履歴反映)
    ADR-Role.md (v3 🆕 二系統管轄・STARTUP_CODES 管轄訂正・構造変更境界・通知伝達経路)
    ADR-Repo.md (v1)
    ADR-Vault.md (v1)
    ADR-NLM.md (v2 REX_Personal_Brain 表示名変更・改名フロー)
    archived/
      ADR-Role-2026-04-27.md (v1 SUPERSEDED by v2)
      ADR-Role-2026-04-28.md (v2 SUPERSEDED by v3 🆕)
      ADR-NLM-2026-04-27.md (v1 SUPERSEDED by v2)
  pending/                    仮決定議論層
    INDEX.md
    personal/2026-04-28_rename_casual_to_personal.md (15 代目で casual/ から物理移行・進捗ステータス追記)
    personal/README.md (15 代目で ADR-Role v3 §14 境界反映)
    {trade_system,trade_brain,setona_hp}/README.md
    casual/2026-04-28_rename_casual_to_personal.md ([MOVED] スタブ)
    casual/README.md ([MOVED] スタブ)
  registry/                   現在の登録状態層(Wiki-Eval 専属)
    repos.md
    nlm.md (REX_Personal_Brain 反映・UUID 不変・ボス手動表示名変更完了)
    roles.md (Wiki-Personal + Wiki-Eval 二系統管轄・構造変更権限明示)
  setona_hp/                  Wiki-hp 用空フォルダ(構築予定)
  handoff/
    latest.md                 本ファイル(v6.7 🆕)
    PROCESS.md                引き継ぎプロセス(v3 14 代目追補)
    architecture_handoff.md   7 代目原典 + 13 代目第 8 章 + 14 代目第 9 章 (+ 15 代目第 10 章は別途追記候補)
  philosophy/                 痕跡層(必読対象外・pull 型運用)
  trade_system/               既存(adr_reservation / doc_map / concepts / 他)
  trade_brain/                ⬜ 未構築(Phase D 着手対象)
  cross/                      ⬜ 骨組のみ
  entities/                   旧配置・Phase C で trade_system/ へ物理統合予定
  decisions/                  旧配置・Phase C で trade_system/ へ物理統合予定

  personal/ 🆕 (15 代目で物理移行完了・サブ層 5 層構造):
    _RUNBOOK.md               中身は v2 のまま(v3 起草は Personal-Planner 業務)
    handoff_latest.md         中身は1代目のまま(改名反映は Personal-Planner 業務)
    index.md                  中身は1代目のまま(5 層化は Personal-Planner 業務)
    log.md                    15 代目移行ログ追記済
    usual/    🆕 (旧 topics/) README + philosophy + shooting
    invent/   🆕 (旧 ideas/)  README
    mind/     🆕 .gitkeep (中身は Personal-Planner が育てる)
    origin/   🆕 .gitkeep (中身は Personal-Planner が育てる)
    insights/ (継続)          README + aiming_without_aim

  casual/ ([MOVED] スタブ群・リンク切れ防止保持・追加更新禁止):
    _RUNBOOK.md / handoff_latest.md / index.md / log.md
    topics/{README,philosophy,shooting}.md
    ideas/README.md
    insights/{README,aiming_without_aim}.md

NLM      : 4 NLM 運用 + 1 構築予定(ADR-NLM v2 確定)
           ・REX_Wiki_Vault     : 5d09e468-... — Wiki-Eval 1:1 担当
           ・REX_System_Brain   : da84715f-... — Wiki-trade 1:1 担当
           ・REX_Trade_Brain    : 4abc25a0-... — Wiki-brain 1:1 担当
           ・REX_Personal_Brain : daf281ae-... — Wiki-Personal 1:1 担当
             (旧 REX_Casual_Brain・UUID 不変・ボス手動表示名変更完了 ✅)
           ・REX_HP_Brain       : 未作成(Wiki-hp 構築予定)
担当     : 統括 Evaluator(Wiki-Eval / 全リポ整合性監査・ADR/registry 管轄・構造変更全般)
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
| Phase Foundation | ADR/pending/registry 三層分離アーキテクチャ確立(13代目)| ✅ 2026-04-27 |
| Phase Personal-Rename | Wiki-casual → Wiki-Personal 改名 ADR 化(14 代目)| ✅ 2026-04-28 |
| **Phase Personal-Migration** | **wiki/casual/ → wiki/personal/ 物理移行 + サブ層 5 層新設(15 代目)** | **✅ 2026-04-28** |
| **Phase Eval-Mandate** | **ADR-Role v3 supersede(Wiki-Eval 二系統管轄明文化)+ STARTUP_CODES v4 / CLAUDE.md v1.3 改訂(15 代目)** | **✅ 2026-04-28** |
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
| 1 | **Phase 3 着手指示**(2026-04-24 ボス承認済み)| 次スレ `Wiki-trade` で Phase 3 spec 起草に着手(別スレ推奨・14 代目 §3 アドバイス準拠)。Planner 起草 → 統括 Evaluator 承認 → ClaudeCode 実装 → #026d 数値不変検証 |
| 2 | NLM ソース初期投入タイミング | 各 NLM への投入開始承認(ADR-NLM 1:1原則に従い各担当ロールが実施)|
| 3 | Phase HP 着手判断 | REX_HP_Brain 構築 + Wiki-hp 起動の可否(ADR-Repo / ADR-NLM の予約項目)|
| 4 | 新機能実装の優先順位 | Phase 3 完了後の展開 |

### 🟡 統括 Evaluator が着手可能(ボス承認後)

| # | 項目 | Phase | 起票場所 |
|---|---|---|---|
| 1 | REX_Wiki_Vault への初期 Ingest(Vault 運用基盤文書群)| Phase B | (Wiki-Eval 直接実施)|
| 2 | wiki/entities + decisions を trade_system/ 配下へ物理統合 | Phase C | pending/trade_system/ → 別スレ Wiki-trade へ委譲 |
| 3 | Trade_System wiki 空ディレクトリ充填(bug_patterns 等)| Phase C | pending/trade_system/ → 別スレ Wiki-trade へ委譲 |
| 4 | Trade_Brain wiki 骨組み構築 | Phase D | pending/trade_brain/ → 別スレ Wiki-brain へ委譲 |
| 5 | latest.md と architecture_handoff の相互整合定期確認 | ─ | (Wiki-Eval 直接実施)|
| 6 | architecture_handoff.md 第 10 章追加(15 代目セッション記録: ADR-Role v3 supersede + Phase Personal-Migration 物理実装 + 14 代目アドバイス受領経緯)| ─ | (Wiki-Eval 直接実施・任意)|

### 🟢 Personal-Planner 業務として残置(次スレ Wiki-Personal で Personal-Planner が実施)

| # | 項目 | 起票場所 |
|---|---|---|
| P1 | `_RUNBOOK.md` v3 起草(射程拡大反映・Wiki-Personal 名称反映・サブ層 5 層記述・思想強制リスク構造的解消・Origin 文脈限定)| wiki/personal/_RUNBOOK.md 直接編集 |
| P2 | `handoff_latest.md` の Wiki-casual → Wiki-Personal 改名反映 | wiki/personal/handoff_latest.md 直接編集 |
| P3 | `index.md` の 5 層構造化(usual/invent/mind/origin/insights の航海図)| wiki/personal/index.md 直接編集 |
| P4 | `usual/philosophy.md` → `mind/shuhari.md` 内容ベース改名(中身判断を伴う)| 該当パス変更 + 内容調整 |
| P5 | 既存ファイルの中身を新サブ層に意味的に振り分け(必要に応じて) | 各サブ層内 |
| P6 | 1 代目積み残し 3 本(eastern_medicine / ai_individuation_mirror / shugyo_to_AI)の draft 起草 | mind/ または insights/ 配下 |

### 🟢 保留中

- Layer 1/3/5 残 QA(MTF_INTEGRITY_QA.md 末尾)
- MINATO_MTF_PHILOSOPHY.md 第 0 章追記(ボス判断時)
- REX_027 Task A/B/C/D/E(ボス再開指示待ち)
- D-11 / F-7 ADR 本文採番(REX_027 再開時)

---

## 🚀 ロール別起動プロンプト(ボスがコピペする分)

> ※ STARTUP_CODES.md v4 が真実源(Wiki-Eval 直接管理)。本セクションはダッシュボード用の抜粋。

### A. 統括 Evaluator(`Wiki-Eval` / Claude.ai or Claude Desktop / Opus)

```
Wiki-Eval
```

担当範囲: Vault 管理 + ADR/registry 管轄 + 全リポ整合性監査 + **Vault 構造変更全般**(ADR-Role v3 §0 二系統管轄)
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

### D. Personal + Advisor 兼任(`Wiki-Personal`)

```
Wiki-Personal
```

(旧 `Wiki-casual` から改名・寛容認識原則により旧コードも認識継続)

担当範囲:
  - Personal: ボスの全人的な人格・思想・起源情報の統合(射程: 日常/思想/起源/横断メタファー)
  - Advisor: REX_AI 全システムにおける相談役
両者とも `Wiki-Personal` で動作。蓄積先は同じ REX_Personal_Brain。
担当 NLM: REX_Personal_Brain のみ(1:1原則・UUID `daf281ae-...` 不変)

Vault 物理移行完了(15 代目・2026-04-28): `wiki/personal/` がアクティブパス。サブ層 5 層構造(usual/invent/mind/origin/insights)が物理確保済み。
中身改訂(_RUNBOOK v3 起草・handoff 改名反映・index 5 層化・philosophy → shuhari 内容ベース改名等)は次スレ Wiki-Personal で Personal-Planner が実施。

### E. Wiki-hp(構築予定)

`Setona_HP` 専属の Planner+ClaudeCode。専用 NLM(REX_HP_Brain)構築後に稼働。
構築フローは ADR-Repo / ADR-NLM 参照。STARTUP_CODES.md v4 で起動コード一覧に追記済(構築予定表記)。

### F. 緊急用・最小起動

```
C:\Python\REX_AI\REX_Brain_Vault\CLAUDE.md を読んで現状把握せよ。
```

---

## 🔗 関連文書

```
13代目で確立した三層分離アーキテクチャ(2026-04-27 新設):
  CLAUDE.md (v1.3 🆕)                             — 単一エントリポイント
  wiki/STARTUP_CODES.md (v4 🆕)                   — 起動コード辞書(Wiki-Eval 直接管理)
  wiki/adr/INDEX.md                               — ADR 一覧 + supersede 履歴
  wiki/adr/ADR-{Role,Repo,Vault,NLM}.md           — 4本の ADR本体(Role=v3 / NLM=v2)
  wiki/adr/archived/                              — supersede 旧版保管
  wiki/pending/INDEX.md                           — 進行中議論一覧
  wiki/registry/{repos,nlm,roles}.md              — 現状登録簿(動的)
  wiki/handoff/PROCESS.md                         — 引き継ぎプロセス運用ガイド
  wiki/handoff/architecture_handoff.md            — 7代目原典 + 13代目第8章 + 14代目第9章
  wiki/archived/START_HERE-2026-04-25.md          — 旧 START_HERE.md(凍結・15 代目で移設)

15 代目で実施した改訂(2026-04-28):
  wiki/archived/START_HERE-2026-04-25.md (旧 START_HERE.md 凍結移設)
  wiki/START_HERE.md (スタブ上書き・リンク切れ防止)
  ADR-Role v3 + archived/ADR-Role-2026-04-28.md (v2 SUPERSEDED)
  registry/roles.md (二系統管轄・構造変更権限明示・v3 整合)
  wiki/personal/ サブ層 5 層物理確保(usual/invent/mind/origin/insights + 4 ルートファイル)
  wiki/casual/ 全 8 ファイル → [MOVED] スタブ上書き(リンク切れ防止)
  wiki/pending/personal/ 物理移行(2 ファイル)・wiki/pending/casual/ → スタブ
  wiki/STARTUP_CODES.md v4(本リリース)
  CLAUDE.md v1.3(本リリース)
  wiki/handoff/latest.md v6.7(本ファイル)

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
  wiki/STARTUP_CODES.md (v4)                  — 起動コード辞書(Wiki-Eval 直接管理)
  wiki/personal/_RUNBOOK.md                   — Personal 層運用ルール(中身 v3 起草は Personal-Planner 業務)
  wiki/trade_system/doc_map.md (v2)           — Trade_System 文書管理
  wiki/trade_system/adr_reservation.md        — ADR 採番台帳
  wiki/philosophy/                            — 痕跡層・気づきメモ(必読外)
  wiki/handoff/architecture_handoff.md (1〜9章) — 7代目原典 + 13代目第8章 + 14代目第9章
```

---

*発行: Rex-Evaluator (Opus 4.7) / 15 代目 / 2026-04-28*
*前任: 14 代目 2026-04-28(v6.6)/ 13 代目 2026-04-27(v6.5)/ 9 代目 2026-04-24(v6.4)/ 8 代目 2026-04-23 / 7 代目 2026-04-22 / 6 代目 2026-04-20*
*※ 10〜12 代目: 本ファイルへの記録なし(13・14代目は確認できず)*

---

## 📝 v6.7 での主な差分(15 代目・2026-04-28)

### 完了した実作業（4 commit）

1. **START_HERE.md 凍結**（commit `42116fd`）
   - `wiki/archived/START_HERE-2026-04-25.md` 新設(凍結ヘッダ + 元本文保管)
   - `wiki/START_HERE.md` を [FROZEN] スタブで上書き(リンク切れ防止・GitHub MCP に物理削除ツールがないため)
   - 14 代目アドバイス §5 選択肢 A(廃止確定)を採用・13 代目 CLAUDE.md v1.2 単一エントリポイント設計を完遂

2. **ADR-Role v3 supersede**（commit `aecf7f1`）
   - 統括 Evaluator の二系統管轄(プロジェクト実装ライン + Vault ナレッジシステム改善・管理)を §0 で明文化
   - §12: STARTUP_CODES.md 管轄を Personal-Planner → Wiki-Eval に訂正(構造 = Vault 横断のため)
   - §14: 構造変更 vs 中身変更の境界線を新設(具体例つき・グレーゾーン処理含む)
   - §15: ADR を通じた通知伝達経路を新設(構造変更は ADR 改訂で各担当者への通知が完結)
   - §13(Personal-Planner 運用責任)番号維持 → ADR-NLM v2 §5 への波及修正回避
   - registry/roles.md を v3 整合に更新(Vault 構造変更権限明示)
   - v2 を `archived/ADR-Role-2026-04-28.md` に退避(SUPERSEDED フラグ付・固定パス原則 §10 遵守)

3. **Phase Personal-Migration Step 1〜4 物理実装**（commit `e07a164`・26 ファイル単一 commit）
   - Step 1: `wiki/casual/` 直下 4 ファイル → `wiki/personal/` へ移行
   - Step 2: `topics/` → `usual/` / `ideas/` → `invent/` ディレクトリリネーム / `insights/` 維持(計 6 ファイル移行)
   - Step 3: `mind/` `origin/` を `.gitkeep` で確保 → 5 層構造完成
   - Step 4: `pending/casual/` → `pending/personal/` 移行(2 ファイル)
   - 旧パス全 12 ファイルに [MOVED] スタブ上書き(リンク切れ防止)
   - **Wiki-Eval はパスのみ変更**(中身は触らず ADR-Role v3 §14 厳守)・中身改訂は Personal-Planner 業務として明示的に残置

4. **STARTUP_CODES v4 / CLAUDE.md v1.3 / latest.md v6.7 改訂**(本 commit)
   - STARTUP_CODES v4: 管轄訂正(Personal-Planner → Wiki-Eval)・Wiki-casual → Wiki-Personal 反映・必須読込から START_HERE.md 削除・Wiki-hp 起動コード一覧に追記・統括 Evaluator 二系統管轄明文化・サブ層 5 層構造記述・Origin 文脈限定反映・`wiki/CLAUDE.md` 表記訂正(実体は `CLAUDE.md` Vault ルート)
   - CLAUDE.md v1.3: Wiki-Personal / REX_Personal_Brain 反映・Personal の射程拡大明文化・統括 Evaluator 二系統管轄(v3 §0)明文化・構造変更 vs 中身変更境界線(v3 §14)明文化・ADR を通じた通知伝達経路(v3 §15)明文化・Origin 文脈限定(v3 §13)反映・必読フロー4点に整理・固定パス原則(v3 §10)言及
   - latest.md v6.7: 本ファイル(進捗反映)

### ボス指示で完了した周辺作業

- **NotebookLM 表示名変更**: ボス手動で REX_Casual_Brain → REX_Personal_Brain に変更完了(UUID `daf281ae-...` 不変・15 代目セッション中に報告受領 ✅)

### 14 代目アドバイス §5/§3 への対応総括

- §5 選択肢 A(START_HERE.md 廃止確定): 採用・実施完了
- §3 分業構造の指摘: 当初は STARTUP_CODES.md v4 を Personal-Planner 業務と解釈したが、ボス指示で**「STARTUP_CODES.md は構造 = Wiki-Eval 管轄」**と訂正を受領 → ADR-Role v3 §12 で恒久訂正・本セッションで Wiki-Eval 直接実施
- 「越権を恐れて自分の正当な責務を狭める」リスクを構造的に解消(ADR-Role v3 §0/§14)

### 残作業（Personal-Planner 業務として明示的に残置）

- _RUNBOOK.md v3 起草・handoff_latest.md 改名反映・index.md 5 層化・philosophy.md → mind/shuhari.md 内容ベース改名・1 代目積み残し 3 本 draft 起草
- これらは次スレ `Wiki-Personal` で Personal-Planner が ADR-Role v3 §14「中身変更」として実施

---

## 📝 v6.6 での主な差分(14 代目・2026-04-28)

- **Wiki-casual → Wiki-Personal 改名 ADR 化を完了**(Phase Personal-Rename)。pending 起票 → ADR-Role v2 / ADR-NLM v2 supersede(v1 は archived へ移動・固定パス原則に従い本体ファイル名は不変)→ registry 同期 → typo 修正の 9 commit を本セッション内で完了。
- **NLM 表示名変更**: `REX_Casual_Brain` → `REX_Personal_Brain`(UUID `daf281ae-...` 不変)。NotebookLM Web UI でのノートブック表示名変更はボス手動(Step 5)→ 15 代目セッションでボス完了報告受領 ✅。
- **新フロー確立**: ADR-NLM v2 §11「NLM 表示名変更フロー」(UUID 不変での意味昇格運用)。
- **思想強制リスクの構造的解消**を ADR-Role v2 §13 と ADR-NLM v2 §5 に明文化。Origin 把握の文脈限定(Wiki-Personal 起動時のメンタル文脈のみ・Trade 判断での参照禁止)を NLM 1:1 原則と起動コード物理分離で構造的に保証。
- **ADR 本体の固定パス原則**を ADR-Role v2 §10 に新設(ボス指示)。`wiki/adr/ADR-{Role,NLM}.md` は常に最新版・archived/ は日付付き命名で保管。
- **architecture_handoff.md に第 9 章追加**: 14 代目セッションでの supersede 実地経験 + 起動時整合性ズレ事象 + 命名議論 + 観点 3 構造的解消の記録。
- **PROCESS.md に追補章追加**(14 代目): 三層分離アーキテクチャ運用フロー・Wiki-Personal 反映・新 /wrap-up フロー記述。
- **philosophy/evaluator_code.md に 14 代目気づきメモ追加**(任意・痕跡層・必読外)。

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
