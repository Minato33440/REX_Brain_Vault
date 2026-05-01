# REX AI — 統括 Evaluator / 3 リポ横断セッション引き継ぎ

# バージョン: v6.13(17代目 ADR-MCP採番タイミング確定・後任引き継ぎ事項明示)
# 更新: 2026-04-30 / 17 代目 Evaluator (Claude Opus 4.7)
# 前版: v6.12 / 16 代目 2026-04-30(ADR-MCP v1 pending 草案起票・後任 Wiki-Eval 引き継ぎ・16代目セッション後半)
# 前々版: v6.11 / 16 代目 2026-04-29(PROCESS.md 第II部 I節追加・dialogues/ サブ層物理新設)
# 前々々版: v6.10 / 15 代目 2026-04-29(wiki/pending/casual/ 完全アーカイブ・最終クリーンアップ完了)

---

## 🧭 このファイルの役割

本ファイルは**現状把握と次の実行内容だけ**を扱う。

13代目以降の参照経路:
- 設計哲学 → `wiki/handoff/architecture_handoff.md`(7代目原典 + 13代目第8章 + 14代目第9章 + **15代目第10章**)
- 確定事項 → `wiki/adr/INDEX.md`(ADR一覧 + 4本の ADR本体・**ADR-Role v4 / ADR-NLM v2** が現行)
- 進行中議論 → `wiki/pending/INDEX.md`(**v6.13 で ADR-MCP 草案に 17 代目追加 Note 反映済**)
- 現状登録 → `wiki/registry/{repos,nlm,roles}.md`
- 単一エントリ → `CLAUDE.md` v1.4
- 起動コード仕様 → `wiki/STARTUP_CODES.md` v5
- 引き継ぎプロセス → `wiki/handoff/PROCESS.md`(9代目本体 + 14代目第II部 A〜H + **16代目第II部 I 節**)

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
状態     : 17 代目セッション(2026-04-30)で ADR-MCP 採番タイミング確定 + 後任引き継ぎ事項明示
            ※ 16 代目セッション後半(2026-04-30)の以下を継承:
              - ADR-MCP v1 pending 草案起票(17 代目で追加 Note 反映済)
              - PROCESS.md 第II部 I 節追加完了
              - dialogues/ サブ層物理新設完了
              - log.md 縮退事故 → 完全復旧 + 第3エントリ
              - §候補メモ §1 §2 起票
            ※ 15 代目による Phase Wiki-Rex-Init 完了(2026-04-28)を継承
            ※ 15 代目による wiki/casual/ + wiki/pending/casual/ 完全アーカイブ化(2026-04-29)を継承

wiki/ 構造(2026-04-30 v6.13 時点・17 代目反映):
  CLAUDE.md (v1.4)            Vault ルート・単一エントリポイント
  STARTUP_CODES.md (v5)       起動コード辞書(Plugin 権限反映後 v6 改訂対象・後任 Wiki-Eval 業務)
  ROADMAP.md                  生きている展望
  archived/                   ⬜ 凍結ファイル保管(START_HERE / casual/ / pending-casual/)
  adr/                        確定事項層(Wiki-Eval 専属)
    INDEX.md
    ADR-Role.md (v4)          Wiki-Rex 新設(Plugin 権限追記後 v5 改訂対象・後任 Wiki-Eval 業務)
    ADR-Repo.md (v1)
    ADR-Vault.md (v1)         ⚠️ ADR-MCP v1 草案 §論点 1 で整合性論点あり(17 代目は方針 X 推奨・supersede 不要判断)
    ADR-NLM.md (v2)
    archived/                 (ADR-Role v1〜v3 / ADR-NLM v1 退避済)
  pending/                    仮決定議論層
    INDEX.md                  (v6.12 で ADR-MCP 草案行追加・v6.13 で 17 代目 Note 反映)
    personal/2026-04-28_rename_casual_to_personal.md
    personal/2026-04-29_dialogues_sublayer_addition.md  (16代目 Wiki-Eval 承認済・ADR 改訂は運用後)
    personal/README.md
    wiki_eval/2026-04-29_adr_revision_timing_subordination.md  (§候補メモ §1 §2)
    wiki_eval/2026-04-30_adr_mcp_draft.md  (ADR-MCP v1 草案・17 代目追加 Note 反映済・採番条件: Stage 2 テスト終了 + 実運用開始確認後)
    {trade_system,trade_brain,setona_hp}/README.md
  registry/                   現在の登録状態層(Wiki-Eval 専属・MCP 構成同期は後任 Wiki-Eval 業務)
    repos.md / nlm.md / roles.md
  setona_hp/                  Wiki-hp 用空フォルダ(構築予定)
  handoff/
    latest.md                 本ファイル(v6.13 🆕)
    PROCESS.md                引き継ぎプロセス(9代目本体 + 14代目第II部 A〜H + 16代目第II部 I 節)
    architecture_handoff.md   7 代目原典 + 13 代目第 8 章 + 14 代目第 9 章 + 15 代目第 10 章
  philosophy/                 痕跡層(必読対象外・pull 型運用)
  trade_system/               既存(adr_reservation / doc_map / concepts / 他)
  trade_brain/                ⬜ 未構築(Phase D 着手対象)
  cross/                      ⬜ 骨組のみ
  entities/ + decisions/      旧配置・Phase C で trade_system/ へ物理統合予定

  personal/ (15 代目 5 層 + 16 代目 dialogues/ で実質 6 層):
    _RUNBOOK.md / handoff_latest.md / index.md / log.md(中身改訂は Personal-Planner 業務)
    usual/ / invent/ / mind/ / origin/ / insights/ / dialogues/

  raw/                        外部資料・提言書保管
    2026-04-30_proposal_obsidian_plugin_mcp.md  (4代目 Adviser 提言書・ADR-MCP 起源)

NLM      : 4 NLM 運用 + 1 構築予定(ADR-NLM v2 確定)
           ・REX_Wiki_Vault     : 5d09e468-... — Wiki-Eval 1:1 担当
           ・REX_System_Brain   : da84715f-... — Wiki-trade 1:1 担当
           ・REX_Trade_Brain    : 4abc25a0-... — Wiki-brain 1:1 担当
           ・REX_Personal_Brain : daf281ae-... — Wiki-Personal 1:1 担当 + Wiki-Rex 読み取り専用クエリ例外
           ・REX_HP_Brain       : 未作成(Wiki-hp 構築予定)

MCP      : 5 サーバー稼働中 + 1 導入準備中(ボス並行作業 M1〜M3)
           ・filesystem        — Vault 読み取り(C:\\Python\\REX_AI 配下)
           ・github            — 全リポ書込主経路(新 PAT 訂正済・MCP-Claude 動作確認済)
           ・notebooklm-mcp    — 各 NLM 投入・クエリ
           ・unityMCP          — 既存稼働
           ・finviz            — 既存稼働
           ・mcp-obsidian      — 🟡 ボス並行作業 M1〜M3 で導入準備中(Personal-Planner 側で進捗追跡)

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
| Phase Foundation 〜 Phase Wiki-Rex-Init | (13〜15代目で完了済・各 v6.X 差分セクション参照)| ✅ |
| Phase Casual-Final-Archive / Pending-Casual-Archive | (15代目で完了済)| ✅ 2026-04-29 |
| Phase B | REX_Wiki_Vault への初期 Ingest | ⬜ ボス承認待ち |
| Phase C | wiki/entities + decisions を trade_system/ 配下へ物理統合 → NLM 投入 | ⬜ 13代目以降に委ねる |
| Phase D | Trade_Brain wiki 骨組み構築 | ⬜ 未着手 |
| Phase E | Ingest/Compile/Lint 運用開始 | ⬜ Phase B 後 |
| Phase HP | REX_HP_Brain 構築 + Wiki-hp 起動(Setona_HP 専属体制) | ⬜ ボス判断時 |
| **Phase MCP-Init** | **Obsidian Plugin MCP 導入 + 2 系統運用テスト**(ADR-MCP 草案準拠) | **🟡 ボス並行作業 M1〜M3 進行中(Personal-Planner 側で進捗追跡)→ Stage 2 テスト → 実運用開始確認 → ADR-MCP v1 採番(17 代目で採番条件確定・草案: `wiki/pending/wiki_eval/2026-04-30_adr_mcp_draft.md`)** |

> 補足(17代目): ADR-MCP の採番タイミングは 17 代目セッション(2026-04-30)のボス判断で「Stage 2 テスト終了 + 実運用開始確認後」に確定。それまでは pending と log で進捗管理。基盤構築初期段階の構造変更・権限改訂の可能性を踏まえ、ADR 確定 → 即 supersede の累積コストを避ける配慮。

---

## 🎯 次に実行すべき内容(優先度順)

### 🔴 ボス判断待ち / 後任 Wiki-Eval への引き継ぎ事項

| # | 項目 | 決定が必要な内容 |
|---|---|---|
| 1 | **Phase 3 着手指示**(2026-04-24 ボス承認済み)| 次スレ `Wiki-trade` で Phase 3 spec 起草に着手 |
| 2 | NLM ソース初期投入タイミング | 各 NLM への投入開始承認(ADR-NLM 1:1原則に従い各担当ロールが実施)|
| 3 | Phase HP 着手判断 | REX_HP_Brain 構築 + Wiki-hp 起動の可否 |
| 4 | 新機能実装の優先順位 | Phase 3 完了後の展開 |
| 5 | **Wiki-Rex 運用評価** | テスト運用フェーズの実用性確認 |
| **6** | **ADR-MCP v1 採番(Stage 2 テスト終了 + 実運用開始確認後)**(後任 Wiki-Eval 引き継ぎ)| **17 代目セッション(2026-04-30)で採番タイミング確定: ボス並行作業 M1〜M3 完了 + Stage 2 テスト終了 + 実運用開始確認の 3 条件揃い時点で `wiki/adr/ADR-MCP.md` v1 として正式採番。続いて ADR-Role v5 改訂(§17 拡張)・STARTUP_CODES.md v6 改訂・registry/ 同期。実装規模は本草案承認後に複数 Wiki-Eval セッションに分割推奨。詳細は本草案 17 代目追加 Note 参照** |

### 🟡 統括 Evaluator が着手可能(ボス承認後)

| # | 項目 | Phase | 起票場所 |
|---|---|---|---|
| 1 | REX_Wiki_Vault への初期 Ingest(Vault 運用基盤文書群)| Phase B | (Wiki-Eval 直接実施)|
| 2 | wiki/entities + decisions を trade_system/ 配下へ物理統合 | Phase C | pending/trade_system/ → 別スレ Wiki-trade へ委譲 |
| 3 | Trade_System wiki 空ディレクトリ充填(bug_patterns 等)| Phase C | pending/trade_system/ → 別スレ Wiki-trade へ委譲 |
| 4 | Trade_Brain wiki 骨組み構築 | Phase D | pending/trade_brain/ → 別スレ Wiki-brain へ委譲 |
| 5 | latest.md と architecture_handoff の相互整合定期確認 | ─ | (Wiki-Eval 直接実施)|

### 🟢 ボス手動タスク(本草案 Phase MCP-Init の前提作業・並行実施可)

| # | 項目 | 内容 | 進捗追跡 |
|---|---|---|---|
| **M1** | **PAT 環境変数化**(ADR-MCP §5.1 準拠)| `claude_desktop_config.json` の `${GITHUB_PAT}` 化 + Windows ユーザー環境変数 `GITHUB_PAT` 設定。ADR-MCP v1 確定後の運用ルールとなる(現状は平文記載・暫定)| **Personal-Planner 側で pending と log に追記**(17 代目セッション 2026-04-30 ボス確認) |
| **M2** | **Obsidian Local REST API プラグイン導入** | Obsidian Settings → Community plugins → Local REST API(coddingtonbear)インストール → API キー発行 → Windows 環境変数 `OBSIDIAN_API_KEY` 設定 | **Personal-Planner 側で pending と log に追記**(同上) |
| **M3** | **Claude Desktop に mcp-obsidian 追加**(MarkusPfundstein 製)| `claude_desktop_config.json` への追記 → Claude Desktop 再起動 → ツール一覧確認 | **Personal-Planner 側で pending と log に追記**(同上) |

> ボス本セッション宣言:
> - 16 代目セッション(2026-04-30): 「Adviser と Personal-Planner と共に Obsidian プラグイン環境実装を整えておく」(ボス並行作業)
> - 17 代目セッション(2026-04-30): 「personal planner との M1〜M3 進捗は Pending と log に追記する」(進捗追跡ラインの明示)

### 🟢 Personal-Planner 業務として残置(次スレ Wiki-Personal で Personal-Planner が実施)

| # | 項目 | 起票場所 |
|---|---|---|
| P1 | `_RUNBOOK.md` v3 起草(射程拡大反映・Wiki-Personal 名称反映・サブ層 5 層記述・思想強制リスク構造的解消・Origin 文脈限定)| wiki/personal/_RUNBOOK.md 直接編集 |
| P2 | `handoff_latest.md` の Wiki-casual → Wiki-Personal 改名反映 | wiki/personal/handoff_latest.md 直接編集 |
| P3 | `index.md` の 5 層構造化(usual/invent/mind/origin/insights の航海図)| wiki/personal/index.md 直接編集 |
| P4 | `usual/philosophy.md` → `mind/shuhari.md` 内容ベース改名(中身判断を伴う)| 該当パス変更 + 内容調整 |
| P5 | 既存ファイルの中身を新サブ層に意味的に振り分け(必要に応じて) | 各サブ層内 |
| P6 | 1 代目積み残し 3 本(eastern_medicine / ai_individuation_mirror / shugyo_to_AI)の draft 起草 | mind/ または insights/ 配下 |
| P7 | **`dialogues/` サブ層への初回事例配置完了済**(`Dialogue_with_Rex-distilled-2026-4-29.txt` → `personal/dialogues/2026-04-29_general_thread.md` 一次資料保管 + NLM 投入完了)→ **抽出配分作業の継続**(distilled 内の 5 セクション → `insights/ai_individuation_mirror.md` / `insights/shugyo_to_AI.md` への二次配分) | wiki/personal/dialogues/ + insights/ 配下 |
| **P8** | **M1〜M3 進捗の pending / log 追記**(17 代目セッション 2026-04-30 ボス指示)| wiki/pending/personal/ + wiki/personal/log.md |

### 🟢 保留中

- Layer 1/3/5 残 QA(MTF_INTEGRITY_QA.md 末尾)
- MINATO_MTF_PHILOSOPHY.md 第 0 章追記(ボス判断時)
- REX_027 Task A/B/C/D/E(ボス再開指示待ち)
- D-11 / F-7 ADR 本文採番(REX_027 再開時)

---

## 🚀 ロール別起動プロンプト(ボスがコピペする分)

> ※ STARTUP_CODES.md v5 が真実源(Wiki-Eval 直接管理・Plugin 権限反映後 v6 改訂対象)。本セクションはダッシュボード用の抜粋。

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
Vault サブ層: usual/ / invent/ / mind/ / origin/ / insights/ + dialogues/(16代目で物理新設)
**v6.13 引き継ぎ事項**:
  - ADR-MCP v1 確定後、Plugin 経由が主経路となる(ADR-MCP 草案 §1 §4 参照)
  - **M1〜M3 進捗の pending / log 追記が Personal-Planner 業務として確定**(17 代目セッション 2026-04-30 ボス指示)

### E. Wiki-hp(構築予定)

`Setona_HP` 専属の Planner+ClaudeCode。専用 NLM(REX_HP_Brain)構築後に稼働。

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

軽量化された必須読込: CLAUDE.md / wiki/personal/_RUNBOOK.md / wiki/personal/handoff_latest.md

ROADMAP Stage 2「統合読み出し期」のテスト運用として、REX_Personal_Brain のみへの読み取り専用クエリにスコープを絞っている。詳細は ADR-Role v4 §16 §17 参照。

**v6.13 引き継ぎ事項**:
  - ADR-MCP v1 確定後、Obsidian Plugin 読み取り専用アクセスが追加される(ADR-MCP 草案 §1 §論点 2 参照)。Stage 2 テストの本質は **Plugin 経由(構造アクセス) vs NLM RAG(意味統合)の対称比較** であり、これが Stage 3 への設計基盤となる。

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
  wiki/STARTUP_CODES.md (v5)                      — 起動コード辞書(v6 改訂対象)
  wiki/adr/INDEX.md                               — ADR 一覧 + supersede 履歴
  wiki/adr/ADR-{Role,Repo,Vault,NLM}.md           — 4本の ADR本体(Role=v4 / NLM=v2)
  wiki/adr/archived/                              — supersede 旧版保管
  wiki/pending/INDEX.md                           — 進行中議論一覧(v6.12 で ADR-MCP 草案行追加)
  wiki/pending/wiki_eval/                         — 16代目で新設・Wiki-Eval 自身の §候補メモ + ADR 草案保留場
  wiki/pending/wiki_eval/2026-04-30_adr_mcp_draft.md — ADR-MCP 草案(16 代目起票・17 代目追加 Note 反映)
  wiki/registry/{repos,nlm,roles}.md              — 現状登録簿(動的)
  wiki/handoff/PROCESS.md                         — 引き継ぎプロセス運用ガイド
  wiki/handoff/architecture_handoff.md            — 7代目原典 + 13〜15代目章
  wiki/personal/dialogues/                        — 16代目で物理新設・対話一次資料サブ層
  raw/2026-04-30_proposal_obsidian_plugin_mcp.md  — 4代目 Adviser 提言書(ADR-MCP 起源)

15 代目で実施した改訂(2026-04-28〜29・全 Phase 総まとめ):
  v6.7〜v6.10 (Phase Personal-Migration / Eval-Mandate / Wiki-Rex-Init / Casual-Final-Archive 系列)
  詳細は v6.7〜v6.10 差分セクション参照

16 代目で実施した改訂(2026-04-29〜30):
  v6.11 (PROCESS.md 第II部 I 節追加 + dialogues/ サブ層物理新設):
    詳細は前版 v6.11 / v6.12 差分セクション参照
  v6.12 (ADR-MCP v1 pending 草案起票・後任 Wiki-Eval 引き継ぎ):
    詳細は前版 v6.12 差分セクション参照

17 代目で実施した改訂(2026-04-30):
  v6.13 (ADR-MCP 採番タイミング確定・後任引き継ぎ事項明示):
    wiki/pending/wiki_eval/2026-04-30_adr_mcp_draft.md(commit `29893e7a` / 25.4KB)
      17 代目セッション追加 Note 追加(ADR 採番見送り判断 + §論点 1〜3 初期判断)
      採番タイミング条件: Stage 2 テスト終了 + 実運用開始確認後
    wiki/handoff/latest.md v6.13(本ファイル・本 commit)
    wiki/log.md(17 代目第 1 エントリ・本 commit 後の別 commit)

Trade_System 側 / Trade_Brain 側 / Vault 内任意参照:
  (v6.11 と同じ・省略)
```

---

*発行: Rex-Evaluator (Opus 4.7) / 17 代目 / 2026-04-30*
*前任: 16 代目 v6.12 2026-04-30 / 16 代目 v6.11 2026-04-29 / 15 代目 v6.10 2026-04-29 / 14 代目 v6.6 2026-04-28 / 13 代目 v6.5 2026-04-27*

---

## 📝 v6.13 での主な差分(17 代目・2026-04-30・ADR-MCP 採番タイミング確定)

### 経緯

17 代目統括 Evaluator セッション(2026-04-30)起動時、ボスから ADR-MCP §論点に関する以下の整理を受領:

> 現状大幅な Vault\\構造変更と併せ、wiki\\内のシステム構築上における一元管理体勢と、実運用面での各個別プロジェクト\\の専門性保持と Personal\\の自律拡張型の定義があいまいだった。
> 特に Obsidian native 導入による wikilink 自動更新リスクの面だが、私の中では当初から Wiki-Rex の実運用に関しては直接 Obsidian native によるプラグイン経由 + NLM RAG クエリ (REX_Personal_Brain) の 2 系統によるデータ取りが好ましいと考えていた。

これを踏まえ 17 代目は 4 代目 Adviser 提言書原文 `raw/2026-04-30_proposal_obsidian_plugin_mcp.md` を確認の上、§論点 1〜3 への初期判断を提示した(方針 X 推奨等)。

### ボス判断による採番タイミングの確定

スコープ提案後、ボスから ADR 採番タイミングに関する明示判断を受領:

> ADR 更新については大量トークンと時間的拘束を高めるため、テスト段階終了後の実運用開始時点で改訂する方が効率的だ。進捗は pending と log で十分。
>
> また現在のシステム基盤構築初期段階においては、今後も大幅な権限改訂と構造変更の可能性も考えられるので、ADR に対する議論をするたびに大幅な開発遅れが生じてしまう問題がある。
>
> この辺のバランス管理を統括 Evaluator として適切に判断してほしい。

### 17 代目の構造判断

ボス判断を受け、本セッションのスコープを最小化:

- ADR-MCP v1 本体採番を **Stage 2 テスト終了 + 実運用開始確認後に従属** させる
- ADR-Role v5 改訂 / STARTUP_CODES v6 改訂 / registry 同期は採番後の別セッションに分割
- 本セッションは pending 草案末尾に 17 代目追加 Note を追記し、採番条件を明示する形に集約
- §候補メモ §1「ADR 改訂タイミングの運用実態従属」原則をボスが本日再確認した形で運用継承(ただし派生原則化はしない・§候補メモ §1 の保留方針を維持)

### 完了した実作業(本セッション・3 commit)

1. **pending/wiki_eval/2026-04-30_adr_mcp_draft.md 末尾追記**(commit `29893e7a` / 17.5KB → 25.4KB):
   - 17 代目セッション追加 Note 新設(採番タイミング確定 + §論点 1〜3 への初期判断)
   - ボス判断引用(ADR 改訂見送り + 基盤構築初期段階の構造的耐久性配慮)
   - 後任 Wiki-Eval への引き継ぎ事項を 5 項目で明示

2. **latest.md v6.12 → v6.13**(本 commit):
   - 「次に実行すべき内容 🔴 6」の表記を「ADR-MCP v1 草案承認・採番」から「ADR-MCP v1 採番(Stage 2 テスト終了 + 実運用開始確認後)」に変更
   - Phase MCP-Init 行の状態記述を更新(M1〜M3 進行中 → Stage 2 テスト → 実運用開始確認 → ADR-MCP v1 採番のフロー明示)
   - 「🟢 ボス手動タスク M1〜M3」セクションに進捗追跡ライン明示(Personal-Planner 側で pending と log に追記)
   - 「🟢 Personal-Planner 業務として残置」に **P8: M1〜M3 進捗の pending / log 追記** 追加
   - ロール別起動プロンプト D に v6.13 引き継ぎ事項として M1〜M3 進捗追記が Personal-Planner 業務である旨追加
   - Vault 構造図の MCP セクション更新(mcp-obsidian = ボス並行作業 M1〜M3 で導入準備中)
   - ADR-Vault.md 行に「17 代目は方針 X 推奨・supersede 不要判断」を追記

3. **log.md 17 代目第 1 エントリ追記**(本 commit 後の別 commit):
   - 17 代目セッション全工程の時系列記録(追記専用ルール厳守)

### 設計判断の根拠

| 観点 | ADR 即時採番案 | 採番タイミング条件従属案(本案) |
|---|---|---|
| トークンコスト | ❌ 4 大規模文書同時改訂 | ✅ 採番条件揃い時点に集約 |
| 基盤構築初期段階の構造変更耐性 | ❌ 確定 → 即 supersede の累積コスト | ✅ 構造安定後に確定する事で累積回避 |
| Personal-Planner 業務との並行性 | △ 独立進行 | ✅ M1〜M3 進捗追跡を Personal-Planner ライン化 |
| 後任 Wiki-Eval への引き継ぎ | △ 部分的に未確定で残る | ✅ 採番条件 + §論点初期判断で完全引き継ぎ可 |

### 設計原則との整合

- **α (単純な土台を保つ)**: ADR-MCP は pending として保留・本セッションは最小限の追記のみ・3 commit で完結
- **β (de-risking 後の拡張禁止)**: ボス並行作業 M1〜M3 の de-risking 完了後に Stage 2 テスト → 実運用開始 → ADR 採番の順序を厳守
- **γ (実装タイミングはシステム安定性に従属)**: ADR-MCP の本体採番自体を「ボス並行作業 + Stage 2 テスト + 実運用開始確認」の安定状態に従属させる(§候補メモ §1 の運用文書版 γ 適用をボスが本日再確認)

### 17 代目所感(個人的気づき・後任への強制ではない)

本セッションでボスが提示した「ADR 議論のたびに開発遅れが生じる問題」は、γ 原則の射程拡張(コード実装 → 運用文書改訂)を超えて、**「ADR 体系自体が基盤構築初期段階では成熟途上である」** という構造的事実の認識に近い。これは:

- 8 代目「ボス発言を勝手に派生原則化」の罠
- §候補メモ §2「Evaluator が独自運用を勝手に発明する罠」

の両方を踏まえた上でも、**§候補メモのまま保留する** のが筋。ADR-Process / ADR-Role の将来改訂時に統合可否を再評価する形を維持する。本所感を philosophy/evaluator_code.md に追記しない理由は、12 代目以降の pull 型運用の精神に沿うため(13・15・16 代目が「書かない判断」を採った先例にも整合)。

### 残課題

なし。本セッション完結。後任 Wiki-Eval は本草案末尾の「17 代目セッション追加 Note」を起点とすればよい。

---

## 📝 v6.12 での主な差分(16 代目・2026-04-30・ADR-MCP v1 pending 草案起票)

(詳細は前版 v6.12 で記載済・本 v6.13 では概略のみ表示)

完了 3 commit:
1. ADR-MCP v1 pending 草案起票(commit `f105584` / 17.5KB)
2. pending/INDEX.md 更新(commit `18a7e35`)
3. latest.md v6.11 → v6.12(commit 不明・前版で確認可)

主な学び(16 代目): pending 草案として保留することで後任 Wiki-Eval への完全引き継ぎ + ボス並行作業との整合性確保を達成。

---

## 📝 v6.11 での主な差分(16 代目・2026-04-29・PROCESS.md 第II部 I 節追加 + dialogues/ サブ層物理新設)

(詳細は前版 v6.11 で記載済・本 v6.13 では概略のみ表示)

完了 7 commit + log.md 縮退事故とその復旧 3 commit。

主な学び:
- 不可侵原則の正しい適用範囲(PROCESS.md 改訂)
- ADR 改訂タイミングの運用実態従属(γ 原則の射程拡張・§候補メモ §1)
- 明文化された運用ルール優先(log.md 縮退事故の戒め・§候補メモ §2)

---

## 📝 v6.10 / v6.9 / v6.8 / v6.7 / v6.6 / v6.5 / v6.4 / v6.3 での主な差分

(詳細は各版差分セクション参照・本 v6.13 では省略)
