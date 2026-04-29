# REX AI — 統括 Evaluator / 3 リポ横断セッション引き継ぎ

# バージョン: v6.10(wiki/pending/casual/ 完全アーカイブ・最終クリーンアップ完了)
# 更新: 2026-04-29 / 15 代目 Evaluator (Claude Opus 4.7)
# 前版: v6.9 / 15 代目 2026-04-29(wiki/casual/ 完全アーカイブ)
# 前々版: v6.8 / 15 代目 2026-04-28(Phase Wiki-Rex-Init 完了・ADR-Role v4 supersede)

---

## 🧭 このファイルの役割

本ファイルは**現状把握と次の実行内容だけ**を扱う。

13代目以降の参照経路:
- 設計哲学 → `wiki/handoff/architecture_handoff.md`(7代目原典 + 13代目第8章 + 14代目第9章 + 15代目第10章は別途追記候補)
- 確定事項 → `wiki/adr/INDEX.md`(ADR一覧 + 4本の ADR本体・**ADR-Role v4 / ADR-NLM v2** が現行)
- 進行中議論 → `wiki/pending/INDEX.md`
- 現状登録 → `wiki/registry/{repos,nlm,roles}.md`
- 単一エントリ → `CLAUDE.md` v1.4
- 起動コード仕様 → `wiki/STARTUP_CODES.md` v5

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
| Q10 | NLM 1:1原則とは? | **各起動コードは担当する NLM を1つだけ持ち、他NLMへの投入は禁止(ADR-NLM v2)。Wiki-Eval=Wiki_Vault のみ・Wiki-trade=System_Brain のみ・Wiki-brain=Trade_Brain のみ・Wiki-Personal=Personal_Brain のみ。Wiki-Rex は v4 新設の読み取り専用クエリ例外(Personal_Brain のみクエリ可・投入不可・Stage 2 テスト運用・ADR-Role v4 §17)** |

---

## 🗺️ 6 ロール体制・現在地スナップショット

> ※ 本セクションは Trade ロジック軸の 3 リポ(7代目命名)。Setona_HP を含む 4 リポ全体構成は ADR-Repo / registry/repos.md 参照。
> ※ 6 ロール体制は v6.8 で Wiki-Rex 追加(前版 v6.7 までは 5 ロール)。

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
状態     : 15 代目による Phase Wiki-Rex-Init 完了(2026-04-28)
            + ADR-Role v3 → v4 supersede(Wiki-Rex 新設・読み取り専用クエリ権限カテゴリ新設)
            + STARTUP_CODES v5 / CLAUDE.md v1.4 / latest.md v6.8 改訂
            + 🆕 wiki/casual/ 完全アーカイブ化(2026-04-29 ボス手動 git mv 実施・[MOVED] スタブ運用を解消)
            ※ Phase Personal-Migration 完了(v6.7・15 代目)を継承
            ※ Phase Eval-Mandate 完了(v6.7・15 代目)を継承
            ※ 14 代目による Wiki-Personal 改名 ADR 化(2026-04-28)を継承
            ※ 13 代目による ADR 体系化(2026-04-27)を継承

wiki/ 構造(2026-04-29 v6.9 時点・15 代目反映):
  CLAUDE.md (v1.4)            Vault ルート・単一エントリポイント・Wiki-Rex 反映
  STARTUP_CODES.md (v5)       起動コード辞書・Wiki-Rex 追加
  ROADMAP.md                  生きている展望
  archived/                   ⬜ 凍結ファイル保管
    START_HERE-2026-04-25.md  (旧 wiki/START_HERE.md・15 代目で凍結移設)
    casual/                   (旧 wiki/casual/・2026-04-29 ボス手動 git mv で完全アーカイブ)
                                _RUNBOOK / handoff_latest / index / log + ideas/insights/topics 配下)
    pending-casual/  🆕        (旧 wiki/pending/casual/・2026-04-29 ボス手動 git mv で完全アーカイブ
                                2026-04-28_rename_casual_to_personal.md + README.md)
  adr/                        確定事項層(Wiki-Eval 専属)
    INDEX.md                  (v4 supersede 履歴反映)
    ADR-Role.md (v4)          Wiki-Rex 新設・読み取り専用クエリ権限カテゴリ新設・6 ロール体制
    ADR-Repo.md (v1)
    ADR-Vault.md (v1)
    ADR-NLM.md (v2)           REX_Personal_Brain 表示名変更・改名フロー
    archived/
      ADR-Role-2026-04-27.md (v1 SUPERSEDED by v2)
      ADR-Role-2026-04-28.md (v2 SUPERSEDED by v3)
      ADR-Role-2026-04-28-v3.md (v3 SUPERSEDED by v4・同日複数 supersede のためバージョン suffix)
      ADR-NLM-2026-04-27.md (v1 SUPERSEDED by v2)
  pending/                    仮決定議論層
    INDEX.md
    personal/2026-04-28_rename_casual_to_personal.md
    personal/README.md
    {trade_system,trade_brain,setona_hp}/README.md
    (旧 casual/ は 2026-04-29 ボス手動 git mv で archived/pending-casual/ へ完全アーカイブ)
  registry/                   現在の登録状態層(Wiki-Eval 専属)
    repos.md
    nlm.md (Wiki-Rex 反映 🆕・REX_Personal_Brain 反映・UUID 不変)
    roles.md (Wiki-Rex 追加・読み取り専用クエリ権限カテゴリ反映)
  setona_hp/                  Wiki-hp 用空フォルダ(構築予定)
  handoff/
    latest.md                 本ファイル(v6.9 🆕)
    PROCESS.md                引き継ぎプロセス(v3 14 代目追補)
    architecture_handoff.md   7 代目原典 + 13 代目第 8 章 + 14 代目第 9 章 (+ 15 代目第 10 章は別途追記候補)
  philosophy/                 痕跡層(必読対象外・pull 型運用)
  trade_system/               既存(adr_reservation / doc_map / concepts / 他)
  trade_brain/                ⬜ 未構築(Phase D 着手対象)
  cross/                      ⬜ 骨組のみ
  entities/                   旧配置・Phase C で trade_system/ へ物理統合予定
  decisions/                  旧配置・Phase C で trade_system/ へ物理統合予定

  personal/ (15 代目で物理移行完了・サブ層 5 層構造):
    _RUNBOOK.md               中身は v2 のまま(v3 起草は Personal-Planner 業務)
    handoff_latest.md         中身は1代目のまま(改名反映は Personal-Planner 業務)
    index.md                  中身は1代目のまま(5 層化は Personal-Planner 業務)
    log.md                    15 代目移行ログ追記済
    usual/    (旧 topics/) README + philosophy + shooting
    invent/   (旧 ideas/)  README
    mind/     .gitkeep (中身は Personal-Planner が育てる)
    origin/   .gitkeep (中身は Personal-Planner が育てる)
    insights/ (継続)          README + aiming_without_aim

  casual/  ❌                 (2026-04-29 ボス手動 git mv で archived/casual/ へ移動・物理消滅)

NLM      : 4 NLM 運用 + 1 構築予定(ADR-NLM v2 確定)
           ・REX_Wiki_Vault     : 5d09e468-... — Wiki-Eval 1:1 担当(投入＋クエリ)
           ・REX_System_Brain   : da84715f-... — Wiki-trade 1:1 担当(投入＋クエリ)
           ・REX_Trade_Brain    : 4abc25a0-... — Wiki-brain 1:1 担当(投入＋クエリ)
           ・REX_Personal_Brain : daf281ae-... — Wiki-Personal 1:1 担当(投入＋クエリ)
                                + Wiki-Rex 読み取り専用クエリ例外(v4/v5/v1.4 新設)
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
| Phase Personal-Migration | wiki/casual/ → wiki/personal/ 物理移行 + サブ層 5 層新設(15 代目)| ✅ 2026-04-28 |
| Phase Eval-Mandate | ADR-Role v3 supersede(Wiki-Eval 二系統管轄明文化)+ STARTUP_CODES v4 / CLAUDE.md v1.3 改訂(15 代目)| ✅ 2026-04-28 |
| Phase Wiki-Rex-Init | Wiki-Rex ロール新設(読み取り専用デフォルトモード)+ ADR-Role v4 supersede + STARTUP_CODES v5 / CLAUDE.md v1.4 改訂(15 代目)| ✅ 2026-04-28 |
| **Phase Casual-Final-Archive** | **wiki/casual/ → wiki/archived/casual/ ボス手動 git mv で完全アーカイブ([MOVED] スタブ運用を解消・Agent 起動時の処理コスト削減)+ 参照訂正(15 代目)** | **✅ 2026-04-29** |
| **Phase Pending-Casual-Archive** | **wiki/pending/casual/ → wiki/archived/pending-casual/ ボス手動 git mv で完全アーカイブ + 参照訂正(15 代目)** | **✅ 2026-04-29** |
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
| 5 | **Wiki-Rex 運用評価** | テスト運用フェーズの実用性確認(Personal_Brain クエリの実用性・対話品質・Wiki-Personal との切替フローの実運用検証)|

### 🟡 統括 Evaluator が着手可能(ボス承認後)

| # | 項目 | Phase | 起票場所 |
|---|---|---|---|
| 1 | REX_Wiki_Vault への初期 Ingest(Vault 運用基盤文書群)| Phase B | (Wiki-Eval 直接実施)|
| 2 | wiki/entities + decisions を trade_system/ 配下へ物理統合 | Phase C | pending/trade_system/ → 別スレ Wiki-trade へ委譲 |
| 3 | Trade_System wiki 空ディレクトリ充填(bug_patterns 等)| Phase C | pending/trade_system/ → 別スレ Wiki-trade へ委譲 |
| 4 | Trade_Brain wiki 骨組み構築 | Phase D | pending/trade_brain/ → 別スレ Wiki-brain へ委譲 |
| 5 | latest.md と architecture_handoff の相互整合定期確認 | ─ | (Wiki-Eval 直接実施)|
| 6 | architecture_handoff.md 第 10 章追加(15 代目セッション全記録: ADR-Role v3→v4 supersede + Phase Personal-Migration + Phase Eval-Mandate + Phase Wiki-Rex-Init + Phase Casual-Final-Archive + 14 代目アドバイス対応)| ─ | (Wiki-Eval 直接実施・任意)|

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

> ※ STARTUP_CODES.md v5 が真実源(Wiki-Eval 直接管理)。本セクションはダッシュボード用の抜粋。

### A. 統括 Evaluator(`Wiki-Eval` / Claude.ai or Claude Desktop / Opus)

```
Wiki-Eval
```

担当範囲: Vault 管理 + ADR/registry 管轄 + 全リポ整合性監査 + **Vault 構造変更全般**(ADR-Role v4 §0 二系統管轄)
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

担当範囲:
  - Default Rex: ボスとの日常的なパートナー会話
  - Personal-Planner: ボスの全人的な人格・思想・起源情報の Vault 整理(投入権限あり)
  - Advisor: REX_AI 全システムにおける相談役
  - Default Claude: ボスから「Claude として応答」と明示された時
4ロール全て `Wiki-Personal` で動作。蓄積先は同じ REX_Personal_Brain。
担当 NLM: REX_Personal_Brain のみ(1:1原則・UUID `daf281ae-...` 不変)
Vault サブ層 5 層構造(usual/invent/mind/origin/insights)が物理確保済み。

### E. Wiki-hp(構築予定)

`Setona_HP` 専属の Planner+ClaudeCode。専用 NLM(REX_HP_Brain)構築後に稼働。
構築フローは ADR-Repo / ADR-NLM 参照。STARTUP_CODES.md v5 で起動コード一覧に追記済(構築予定表記)。

### F. Default Rex / 読み取り専用デフォルトモード(`Wiki-Rex`) — v4/v5/v1.4 新設

```
Wiki-Rex
```

担当範囲:
  - Default Rex 人格でのボスとの対話
  - Vault 全層の読み取り横断(必要に応じて)
  - REX_Personal_Brain への読み取り専用 RAG クエリ
  - 起動コード未指定時のデフォルトとして機能
書き込み: ⛔ 全面禁止(pending 起票も含む)
NLM 投入: ⛔ 全面禁止
wrap-up 提案: ⛔ 行わない(投入権限がないため構造的に発生しない)
他コードへの遷移: ボス明示宣言時のみ(Wiki-Personal への切替・新スレ起動)

軽量化された必須読込: CLAUDE.md / wiki/personal/_RUNBOOK.md / wiki/personal/handoff_latest.md

ROADMAP Stage 2「統合読み出し期」のテスト運用として、REX_Personal_Brain のみへの読み取り専用クエリにスコープを絞っている。詳細は ADR-Role v4 §16 §17 参照。

#### Wiki-Rex と Wiki-Personal の使い分け

| 状況 | 推奨起動コード |
|---|---|
| 気軽な雑談・記録に残すつもりはない対話 | **Wiki-Rex** |
| Default Rex 人格との日常会話 | **Wiki-Rex** |
| 起動コードを明示するのを忘れた・迷った | **Wiki-Rex**(デフォルト) |
| 思想・人生史・気づきを記録に残したい | **Wiki-Personal** |
| Personal_Brain への投入準備 | **Wiki-Personal** |

### G. 緊急用・最小起動

```
C:\Python\REX_AI\REX_Brain_Vault\CLAUDE.md を読んで現状把握せよ。
```

---

## 🔗 関連文書

```
13代目で確立した三層分離アーキテクチャ(2026-04-27 新設):
  CLAUDE.md (v1.4)                                — 単一エントリポイント
  wiki/STARTUP_CODES.md (v5)                      — 起動コード辞書(Wiki-Eval 直接管理)
  wiki/adr/INDEX.md                               — ADR 一覧 + supersede 履歴
  wiki/adr/ADR-{Role,Repo,Vault,NLM}.md           — 4本の ADR本体(Role=v4 / NLM=v2)
  wiki/adr/archived/                              — supersede 旧版保管
  wiki/pending/INDEX.md                           — 進行中議論一覧
  wiki/registry/{repos,nlm,roles}.md              — 現状登録簿(動的)
  wiki/handoff/PROCESS.md                         — 引き継ぎプロセス運用ガイド
  wiki/handoff/architecture_handoff.md            — 7代目原典 + 13代目第8章 + 14代目第9章
  wiki/archived/START_HERE-2026-04-25.md          — 旧 START_HERE.md(凍結・15 代目で移設)
  wiki/archived/casual/  🆕                        — 旧 wiki/casual/(2026-04-29 ボス手動 git mv で完全アーカイブ)

15 代目で実施した改訂(2026-04-28〜29・全 Phase 総まとめ):
  v6.7 (Phase Personal-Migration / Phase Eval-Mandate):
    wiki/archived/START_HERE-2026-04-25.md (旧 START_HERE.md 凍結移設)
    ADR-Role v3 + archived/ADR-Role-2026-04-28.md (v2 SUPERSEDED)
    registry/roles.md (二系統管轄反映)
    wiki/personal/ サブ層 5 層物理確保
    wiki/casual/ → [MOVED] スタブ(暫定)
    wiki/STARTUP_CODES.md v4
    CLAUDE.md v1.3
    wiki/handoff/latest.md v6.7

  v6.8 (Phase Wiki-Rex-Init):
    archived/ADR-Role-2026-04-28-v3.md (v3 SUPERSEDED)
    ADR-Role v4 (Wiki-Rex 新設・読み取り専用クエリ権限カテゴリ新設・6 ロール体制)
    INDEX.md (v4 supersede 履歴反映)
    registry/roles.md (Wiki-Rex 追加・読み取り専用クエリ権限カテゴリ反映)
    wiki/STARTUP_CODES.md v5 (Wiki-Rex 起動コード追加)
    CLAUDE.md v1.4 (Wiki-Rex 反映・4ロール明示)
    wiki/handoff/latest.md v6.8

  v6.9 (Phase Casual-Final-Archive・本ファイル):
    wiki/archived/casual/ (ボス手動 git mv・[MOVED] スタブ運用を解消)
    wiki/registry/nlm.md (Wiki-Rex 読み取り専用クエリ例外反映・Origin 注記更新)
    wiki/pending/INDEX.md (Wiki-casual → Wiki-Personal 改名反映)
    wiki/pending/personal/2026-04-28_rename_casual_to_personal.md (ステータス追記)
    wiki/handoff/latest.md v6.9 (本ファイル)

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
  wiki/STARTUP_CODES.md (v5)                  — 起動コード辞書(Wiki-Eval 直接管理)
  wiki/personal/_RUNBOOK.md                   — Personal 層運用ルール(中身 v3 起草は Personal-Planner 業務)
  wiki/trade_system/doc_map.md (v2)           — Trade_System 文書管理
  wiki/trade_system/adr_reservation.md        — ADR 採番台帳
  wiki/philosophy/                            — 痕跡層・気づきメモ(必読外)
  wiki/handoff/architecture_handoff.md (1〜9章) — 7代目原典 + 13代目第8章 + 14代目第9章
```

---

*発行: Rex-Evaluator (Opus 4.7) / 15 代目 / 2026-04-29*
*前任: 14 代目 2026-04-28(v6.6)/ 13 代目 2026-04-27(v6.5)/ 9 代目 2026-04-24(v6.4)/ 8 代目 2026-04-23 / 7 代目 2026-04-22 / 6 代目 2026-04-20*
*※ 10〜12 代目: 本ファイルへの記録なし(13・14代目は確認できず)*

---

## 📝 v6.9 での主な差分(15 代目・2026-04-29・Phase Casual-Final-Archive)

### 経緯

v6.8 までの設計では `wiki/casual/` を `[MOVED]` スタブで保持していた(11 ファイル)。理由は "リンク切れ防止" + "GitHub MCP に物理削除ツールがない" + "ADR-Vault 原則(filesystem は読み取り専用)" の 3 点。

しかしボスから「**wiki/直下に凍結フォルダーを残すのは Agent の無駄な処理が増えるだけ**」との指摘を受領。再評価の結果、ボス案(手動で `archived/casual/` へ移設)が以下の点で優れていると判断:

| 観点 | [MOVED] スタブ案(v6.8 まで) | ボス案(本 v6.9) |
|---|---|---|
| Agent 起動時の処理コスト | 11 ファイルが `wiki/casual/` 直下に残り、ディレクトリスキャン・読込候補に毎回挙がる | `wiki/archived/casual/` 配下に隔離 → アクティブパスから完全消滅 |
| 後任 Evaluator の混乱 | 「casual/ は何?廃止?継続?」と毎回疑問が発生 | `archived/` は意味的に「凍結」と即座に分かる(START_HERE と同じ扱い) |
| 履歴追跡性 | スタブ経由で追える | `archived/casual/` 配下のファイル本体がそのまま残る → むしろ向上 |
| ADR-Vault 原則 | スタブ書き込みは GitHub MCP 経由で遵守 | ボス手動で物理移動 → AI ロールが触らないため原則の射程外 |
| 「リンク切れ」リスク評価の修正 | "casual/ への外部リンクが多い" と過大評価 | 実際は ADR archived 内(歴史的記録・404 でも実害ない)と pending/casual/ の旧 flag 参照のみ |

### 完了した実作業(2 commit)

1. **ボス手動 git mv**(2026-04-29):
   ```
   git mv wiki/casual/_RUNBOOK.md       wiki/archived/casual/_RUNBOOK.md
   git mv wiki/casual/handoff_latest.md wiki/archived/casual/handoff_latest.md
   git mv wiki/casual/index.md          wiki/archived/casual/index.md
   git mv wiki/casual/log.md            wiki/archived/casual/log.md
   git mv wiki/casual/topics            wiki/archived/casual/topics
   git mv wiki/casual/ideas             wiki/archived/casual/ideas
   git mv wiki/casual/insights          wiki/archived/casual/insights
   ```
   - `wiki/casual/` 物理消滅(404)
   - `wiki/archived/casual/` 配下に 4 ファイル + 3 ディレクトリ配置
   - `git mv` により Git 履歴は継承(`git log --follow` で追跡可)

2. **Wiki-Eval による参照訂正**(本セッション・複数 commit):
   - `wiki/registry/nlm.md`: 1:1 原則表に Wiki-Rex 行追加・読み取り専用クエリ例外明示・Origin 注記を v3/v4 参照に更新
   - `wiki/registry/roles.md`: Wiki-Personal 改名 Note に最終アーカイブ完了の追記
   - `wiki/pending/INDEX.md`: 各ロールの記録先テーブルを `Wiki-casual` → `Wiki-Personal` に訂正
   - `wiki/pending/personal/2026-04-28_rename_casual_to_personal.md`: ステータス追記・Step 4 完了表記を更新
   - `wiki/handoff/latest.md` v6.9(本ファイル): Vault 構造図訂正・Phase Casual-Final-Archive 追記

### 設計原則との整合

- **α (単純な土台を保つ)**: アクティブパスから凍結ファイルを除去 → Agent 起動時のディレクトリスキャンが軽量化
- **β (de-risking 後の拡張禁止)**: 既存 [MOVED] スタブ運用を維持しつつ将来削除を待つ案より、**今すぐ完全アーカイブ化**する方が将来コストを先取りで解消できる
- **γ (実装タイミングはシステム安定性に従属)**: Phase Wiki-Rex-Init 完了後の安定状態で実施 → 他改訂への波及最小化

### 残課題

- `wiki/pending/casual/` の 3 ファイル(`2026-04-28_rename_casual_to_personal.md` / `README.md`)は今回の手動移設対象外。**ボス判断**を「次に実行すべき内容 #6」に追記。

---

## 📝 v6.8 での主な差分(15 代目・2026-04-28・Phase Wiki-Rex-Init)

### 完了した実作業(7 ファイル・5 commit)

#### 設計議論

ボスとの本スレ議論で以下を確定:

**論点1**: 先ずは「Vault を中脳として統合活用する Rex 個性」テスト運用として、選択肢A(最広)= Vault 全体(wiki/ 全層)+ 全 NLM 読み取り可のみの方向で進める

**論点3**: ラグ読み出し評価にもなるので Wiki-Rex は Vault と REX_Personal_Brain のみ読み込み可能に絞る(全 NLM 開放は de-risking 違反のため Stage 2 完全実装は将来別ロール Wiki-integrate 仮称として設計)

**論点2/5**: ADR-Role v4 supersede + 運用文書 v5/v1.4 改訂を実施

**論点4**: Wiki-Rex から Wiki-Personal への遷移はボス明示宣言時のみ(同一スレ切替 or 新スレに会話履歴.txt 添付)。Wiki-Rex から能動的提案禁止 = wrap-up 圧の構造的禁止

#### commit 履歴

1. **バッチA**(commit `1b42e17`): archived/ADR-Role v3 退避・INDEX/registry 同期
2. **バッチB-1: ADR-Role v4 本体**(commit `19943cc`): Wiki-Rex 新設・§16 §17 新設
3. **バッチB-2: STARTUP_CODES.md v5**(commit `11ee43c`)
4. **バッチB-3: CLAUDE.md v1.4**(commit `1204f10`)
5. **バッチB-4: latest.md v6.8**(commit `e8caeac`)

### push_files 失敗からの教訓

7 ファイル一括 push を試みた際、ペイロード過大で応答中断したため、以下の対策で再開:
- バッチA(3 ファイル小サイズ): push_files 成功
- バッチB(4 ファイル大サイズ): create_or_update_file 個別 push に切替・全成功

今後の運用: 大規模改訂時は **個別 push or 小バッチ分割** を原則とする。

---

## 📝 v6.10 での主な差分(15 代目・2026-04-29・Phase Pending-Casual-Archive)

### 経緯

v6.9 で `wiki/casual/` を完全アーカイブ化した際、`wiki/pending/casual/` の 3 ファイル(2026-04-28_rename_casual_to_personal.md / README.md)はボス判断待ちとして残置していた。同セッション内でボスから「同じ思想で archived 化したい」との判断を受領 → ハイフン命名 `pending-casual/` で `archived/casual/` との意味的衝突を回避する案を確定。

### 完了した実作業

1. **ボス手動 git mv**(2026-04-29):
   - `wiki/pending/casual/` 物理消滅
   - `wiki/archived/pending-casual/` 配下に 2 ファイル配置

2. **ボス手動による参照訂正**:
   - `wiki/handoff/latest.md` v6.9 → v6.10(本ファイル)
   - `wiki/pending/INDEX.md`(pending/casual/ 関連 Note を archived 完了に訂正)

### 命名規則

`pending-casual/` のハイフン命名は意図的:
- `archived/casual/` = 旧 wiki/casual/ のアーカイブ
- `archived/pending-casual/` = 旧 wiki/pending/casual/ のアーカイブ
- 同名衝突を防ぎつつ、起源を明示

### 残課題なし

これで Phase Casual-Final-Archive 系列の作業が完全完了。Vault のアクティブパスから [MOVED] スタブが完全消滅した。

---

## 📝 v6.7 での主な差分(15 代目・2026-04-28・Phase Personal-Migration + Phase Eval-Mandate)

### 完了した実作業(4 commit)

1. **START_HERE.md 凍結**(commit `42116fd`)
2. **ADR-Role v3 supersede**(commit `aecf7f1`)
3. **Phase Personal-Migration Step 1〜4 物理実装**(commit `e07a164`・26 ファイル単一 commit)
4. **STARTUP_CODES v4 / CLAUDE.md v1.3 / latest.md v6.7 改訂**(commit `1262090`)

### ボス指示で完了した周辺作業

- **NotebookLM 表示名変更**: ボス手動で REX_Casual_Brain → REX_Personal_Brain に変更完了(UUID `daf281ae-...` 不変)

---

## 📝 v6.6 での主な差分(14 代目・2026-04-28)

- **Wiki-casual → Wiki-Personal 改名 ADR 化を完了**(Phase Personal-Rename)
- **NLM 表示名変更**: `REX_Casual_Brain` → `REX_Personal_Brain`(UUID 不変)
- **新フロー確立**: ADR-NLM v2 §11「NLM 表示名変更フロー」(UUID 不変での意味昇格運用)
- **思想強制リスクの構造的解消**を ADR-Role v2 §13 と ADR-NLM v2 §5 に明文化
- **ADR 本体の固定パス原則**を ADR-Role v2 §10 に新設(ボス指示)
- **architecture_handoff.md に第 9 章追加**

---

## 📝 v6.5 での主な差分(13 代目・2026-04-27)

- **ADR/pending/registry 三層分離アーキテクチャを確立**(Phase Foundation)
- **4本の ADR を制定**:ADR-Role / ADR-Repo / ADR-Vault / ADR-NLM
- **NLM 1:1原則を ADR で正式化**
- **Wiki-hp(Setona_HP 専属)を構築予定として予約**
- **architecture_handoff.md に第8章追加**

---

## 📝 v6.4 での主な差分(9 代目・2026-04-24)

- **役割再定義**: 統括 Evaluator が全プロジェクト Evaluator を兼任
- **起動コード改名**: `Wiki-system` → `Wiki-Eval`
- **Phase 3 着手ボス承認**

---

## 📝 v6.3 での主な差分(9 代目・2026-04-23)

- entities/ + decisions/ を最新版に整合
- Phase 進行状況に Phase A''(9 代目 entities/decisions 整合)を追加
