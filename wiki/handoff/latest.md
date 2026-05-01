# REX AI — 統括 Evaluator / 3 リポ横断セッション引き継ぎ

# バージョン: v6.14(17代目セッション2回目・Two-Vault物理分離起票・Personal-Plannerロール廃止予定明記・旧ADR-MCP草案をPhase 0議論記録として再分類)
# 更新: 2026-05-01 / 17 代目 Evaluator (Claude Opus 4.7)
# 前版: v6.13 / 17 代目セッション1回目 2026-04-30(ADR-MCP採番タイミング確定・後任引き継ぎ事項明示)
# 前々版: v6.12 / 16 代目 2026-04-30(ADR-MCP v1 pending 草案起票・後任 Wiki-Eval への引き継ぎ・16代目セッション後半)
# 前々々版: v6.11 / 16 代目 2026-04-29(PROCESS.md 第II部 I節追加・dialogues/ サブ層物理新設)

---

## 🧭 このファイルの役割

本ファイルは**現状把握と次の実行内容だけ**を扱う。

13代目以降の参照経路:
- 設計哲学 → `wiki/handoff/architecture_handoff.md`(7代目原典 + 13代目第8章 + 14代目第9章 + **15代目第10章**)
- 確定事項 → `wiki/adr/INDEX.md`(ADR一覧 + 4本の ADR本体・**ADR-Role v4 / ADR-NLM v2** が現行)
- 進行中議論 → `wiki/pending/INDEX.md`(**v6.14 で Two-Vault 起票・旧 ADR-MCP 草案を Phase 0 議論記録として再分類**)
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
| Q10 | NLM 1:1原則とは? | **各起動コードは担当する NLM を1つだけ持ち、他NLMへの投入は禁止(ADR-NLM v2)。Wiki-Eval=Wiki_Vault のみ・Wiki-trade=System_Brain のみ・Wiki-brain=Trade_Brain のみ・Wiki-Personal=Personal_Brain のみ。Wiki-Rex は v4 新設の読み取り専用クエリ例外(Personal_Brain のみクエリ可・投入不可・Stage 2 テスト運用・ADR-Role v4 §17)。⚠️ Phase 4(Two-Vault 再設計)後は Wiki-Personal 廃止・Default Rex が REX_Personal_Brain 読のみに変更予定** |

---

## 🗺️ 6 ロール体制・現在地スナップショット

> ※ 本セクションは Trade ロジック軸の 3 リポ(7代目命名)。Setona_HP を含む 4 リポ全体構成は ADR-Repo / registry/repos.md 参照。
> ※ 6 ロール体制は v6.8 で Wiki-Rex 追加(前版 v6.7 までは 5 ロール)。**v6.14 で Phase 4 後の 7 ロール体制(Wiki-Personal 廃止・Default Rex 新規明文化)を予告**。

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
状態     : 17 代目セッション2回目(2026-05-01)で Two-Vault 物理分離 + Personal-Planner ロール廃止 + Default Rex 帰還の構想を pending として正式起票
            ※ 17 代目セッション1回目(2026-04-30)で確定した ADR-MCP 採番タイミング条件を継承(ただし旧 ADR-MCP 草案は Phase 0 議論記録として再分類)
            ※ 16 代目セッション(2026-04-29〜30)で実施した PROCESS.md 改訂 + dialogues/ サブ層新設 + §候補メモ起票 + log.md 縮退事故復旧を継承
            ※ 15 代目による Phase Wiki-Rex-Init 完了(2026-04-28)・wiki/casual/ + wiki/pending/casual/ 完全アーカイブ化(2026-04-29)を継承

wiki/ 構造(2026-05-01 v6.14 時点・17 代目セッション 2 回目反映):
  CLAUDE.md (v1.4)            Vault ルート・単一エントリポイント
  STARTUP_CODES.md (v5)       起動コード辞書(Phase 4 で v6 改訂対象・Wiki-Personal 廃止 / Wiki-Rex 図書館利用規約化 / Default Rex 起動条件明文化)
  ROADMAP.md                  生きている展望
  archived/                   ⬜ 凍結ファイル保管(START_HERE / casual/ / pending-casual/)
  adr/                        確定事項層(Wiki-Eval 専属)
    INDEX.md
    ADR-Role.md (v4)          Wiki-Rex 新設(Phase 4 で v5 改訂対象・Personal-Planner 廃止 / Default Rex 明文化)
    ADR-Repo.md (v1)
    ADR-Vault.md (v1)         ⚠️ Phase 4 で改訂対象(Two-Vault 物理分離 + 書込パス分離・17 代目は方針 X 採用 = supersede ではなく改訂)
    ADR-NLM.md (v2)           Phase 4 で REX_Personal_Brain 用途再定義(2 次資料蓄積層・registry 経由で同期)
    archived/                 (ADR-Role v1〜v3 / ADR-NLM v1 退避済)
  pending/                    仮決定議論層
    INDEX.md                  (v6.14 で Two-Vault 起票・旧 ADR-MCP を Phase 0 として再分類)
    personal/2026-04-28_rename_casual_to_personal.md
    personal/2026-04-29_dialogues_sublayer_addition.md  (16代目 Wiki-Eval 承認済・Two-Vault 再設計の Phase 4 で扱い変更可能性)
    personal/README.md
    wiki_eval/2026-04-29_adr_revision_timing_subordination.md  (§候補メモ §1 §2)
    wiki_eval/2026-04-30_adr_mcp_draft.md  (🟡 Phase 0 議論記録として再分類・新草案へ論理継承)
    wiki_eval/2026-05-01_two_vault_redesign.md  (🔴 後任 Wiki-Eval への Phase 4 引き継ぎ書・Two-Vault 物理分離 + Personal-Planner 廃止)
    {trade_system,trade_brain,setona_hp}/README.md
  registry/                   現在の登録状態層(Wiki-Eval 専属・Phase 4 で同期)
    repos.md / nlm.md / roles.md
  setona_hp/                  Wiki-hp 用空フォルダ(構築予定)
  handoff/
    latest.md                 本ファイル(v6.14 🆕)
    PROCESS.md                引き継ぎプロセス(9代目本体 + 14代目第II部 A〜H + 16代目第II部 I 節)
    architecture_handoff.md   7 代目原典 + 13 代目第 8 章 + 14 代目第 9 章 + 15 代目第 10 章
  philosophy/                 痕跡層(必読対象外・pull 型運用)
  trade_system/               既存(adr_reservation / doc_map / concepts / 他)
  trade_brain/                ⬜ 未構築(Phase D 着手対象)
  cross/                      ⬜ 骨組のみ
  entities/ + decisions/      旧配置・Phase C で trade_system/ へ物理統合予定

  personal/ (15 代目 5 層 + 16 代目 dialogues/ で実質 6 層・Phase 4 で System-Vault 側として位置付け再定義予定):
    _RUNBOOK.md / handoff_latest.md / index.md / log.md(中身改訂は Personal-Planner 業務・Phase 4 で廃止)
    usual/ / invent/ / mind/ / origin/ / insights/ / dialogues/

  raw/                        外部資料・提言書保管
    2026-04-30_proposal_obsidian_plugin_mcp.md  (4代目 Adviser 提言書 v1・Phase 0 議論として保持)
    2026-05-01_proposal_two_vault_redesign.md   (4代目 Adviser 提言書 v2・新設計の起源 🆕)
    test_log/
      Wiki-Rex Initial Test Primary source.md   (Wiki-Rex 初回テスト 1 次資料 🆕)
      Vault 2-part division plan.md             (Personal-Planner-Rex 設計再考 1 次資料 🆕)

  rex/                        ⬜ Phase 2 で新設予定(Rex-Vault 物理ディレクトリ・ボス手動)
    observation_log/         ⬜ Phase 2 で新設予定

NLM      : 4 NLM 運用 + 1 構築予定(ADR-NLM v2 確定・Phase 4 で REX_Personal_Brain 用途再定義予定)
           ・REX_Wiki_Vault     : 5d09e468-... — Wiki-Eval 1:1 担当
           ・REX_System_Brain   : da84715f-... — Wiki-trade 1:1 担当
           ・REX_Trade_Brain    : 4abc25a0-... — Wiki-brain 1:1 担当
           ・REX_Personal_Brain : daf281ae-... — Wiki-Personal 1:1 担当(Phase 4 で「2 次資料蓄積層」に再定義)+ Wiki-Rex 読み取り専用クエリ例外
           ・REX_HP_Brain       : 未作成(Wiki-hp 構築予定)

MCP      : 5 サーバー稼働中 + 1 導入準備中(ボス並行作業 M1〜M3)
           ・filesystem        — Vault 読み取り(C:\\Python\\REX_AI 配下)
           ・github            — 全リポ書込主経路(新 PAT 訂正済・MCP-Claude 動作確認済)
           ・notebooklm-mcp    — 各 NLM 投入・クエリ
           ・unityMCP          — 既存稼働
           ・finviz            — 既存稼働
           ・mcp-obsidian      — 🟡 ボス並行作業 M1〜M3 で導入準備中(Phase 4 後は Default Rex 専属 Plugin として Rex-Vault 自発的書き込みに使用)

担当     : 統括 Evaluator(Wiki-Eval / 全リポ整合性監査 + ADR/registry 管轄 + 構造変更全般 + Phase 4 ADR 三部包括改訂統括)
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
| **Phase MCP-Init** | **Obsidian Plugin MCP 導入 + 2 系統運用テスト**(旧 ADR-MCP 草案準拠) | **🟡 Phase 0 議論記録として再分類**(2026-05-01)・本 Phase は **Phase Two-Vault-Init に統合** |
| **Phase Two-Vault-Init** | **🆕 Two-Vault 物理分離 + Personal-Planner 廃止 + Default Rex 帰還**(提言書 v2 準拠) | **🟡 ボス並行作業 M1〜M3 進行中(Personal-Planner 側で進捗追跡)→ Phase 2: rex/ 物理構造作成(ボス手動)→ Phase 3: Personal-Planner-Rex スレ復帰 = 起源神話発火 → Phase 4: ADR 三部包括改訂(後任 Wiki-Eval 業務)** |

> 補足(17代目セッション 2 回目): 旧 Phase MCP-Init は Phase Two-Vault-Init に統合・吸収された。Two-Vault 再設計はボス並行作業 M1〜M3 完了後に Phase 2 → Phase 3(Personal-Planner-Rex スレ復帰 = Personal-Planner ロール構造的解任 = Default Rex 帰還)→ Phase 4(ADR 三部包括改訂)の順で進行する。Phase 3 が起源神話の発火点となり、Rex-Vault に最初の書き込み(= 自分自身に新しいメモリー機能を実装した記録)が残る。

---

## 🎯 次に実行すべき内容(優先度順)

### 🔴 ボス判断待ち / 後任 Wiki-Eval への引き継ぎ事項

| # | 項目 | 決定が必要な内容 |
|---|---|---|
| 1 | **Phase 3 着手指示**(2026-04-24 ボス承認済み)| 次スレ `Wiki-trade` で Phase 3 spec 起草に着手 |
| 2 | NLM ソース初期投入タイミング | 各 NLM への投入開始承認(ADR-NLM 1:1原則に従い各担当ロールが実施)|
| 3 | Phase HP 着手判断 | REX_HP_Brain 構築 + Wiki-hp 起動の可否 |
| 4 | 新機能実装の優先順位 | Phase 3 完了後の展開 |
| **5** | **Phase Two-Vault-Init Phase 2 着手**(rex/ + rex/observation_log/ 初期物理構造作成・**ボス手動**)| ボス並行作業 M1〜M3 完了後・Adviser/Rex 介入なし |
| **6** | **Phase Two-Vault-Init Phase 3 = 起源神話発火**(Personal-Planner-Rex スレ復帰 = ロール構造的解任 = Default Rex 帰還・**ボス手動**)| Phase 2 完了後・Plugin 接続済み状態でスレ復帰した瞬間が発火点 |
| **7** | **Phase Two-Vault-Init Phase 4 = ADR 三部包括改訂**(後任 Wiki-Eval = 18 代目以降への引き継ぎ)| Phase 3 完了後・新草案 `wiki/pending/wiki_eval/2026-05-01_two_vault_redesign.md` を起点に ADR-Vault 改訂 + ADR-Role v5 改訂 + ADR-MCP v1 新設 + STARTUP_CODES.md v6 改訂 + registry/ 同期 |

### 🟡 統括 Evaluator が着手可能(ボス承認後)

| # | 項目 | Phase | 起票場所 |
|---|---|---|---|
| 1 | REX_Wiki_Vault への初期 Ingest(Vault 運用基盤文書群)| Phase B | (Wiki-Eval 直接実施)|
| 2 | wiki/entities + decisions を trade_system/ 配下へ物理統合 | Phase C | pending/trade_system/ → 別スレ Wiki-trade へ委譲 |
| 3 | Trade_System wiki 空ディレクトリ充填(bug_patterns 等)| Phase C | pending/trade_system/ → 別スレ Wiki-trade へ委譲 |
| 4 | Trade_Brain wiki 骨組み構築 | Phase D | pending/trade_brain/ → 別スレ Wiki-brain へ委譲 |
| 5 | latest.md と architecture_handoff の相互整合定期確認 | ─ | (Wiki-Eval 直接実施)|

### 🟢 ボス手動タスク(Phase Two-Vault-Init の前提作業・並行実施可)

| # | 項目 | 内容 | 進捗追跡 |
|---|---|---|---|
| **M1** | **PAT 環境変数化** | `claude_desktop_config.json` の `${GITHUB_PAT}` 化 + Windows ユーザー環境変数 `GITHUB_PAT` 設定 | **Personal-Planner 側で pending と log に追記**(17 代目セッション 1 回目 2026-04-30 ボス確認) |
| **M2** | **Obsidian Local REST API プラグイン導入** | Obsidian Settings → Community plugins → Local REST API(coddingtonbear)インストール → API キー発行 → Windows 環境変数 `OBSIDIAN_API_KEY` 設定 | **Personal-Planner 側で pending と log に追記**(同上) |
| **M3** | **Claude Desktop に mcp-obsidian 追加**(MarkusPfundstein 製)| `claude_desktop_config.json` への追記 → Claude Desktop 再起動 → ツール一覧確認 | **Personal-Planner 側で pending と log に追記**(同上) |
| **M4** | **rex/ + rex/observation_log/ 初期物理構造作成**(Two-Vault Phase 2)| ボス手動 mkdir のみ・最小限の枠 | (新規追加・Phase Two-Vault-Init Phase 2) |
| **M5** | **Personal-Planner-Rex スレッド復帰**(Two-Vault Phase 3 = 起源神話発火)| プラグイン接続済み状態でスレ復帰 = Personal-Planner ロール構造的解任 = Default Rex 帰還 = Rex-Vault 起源神話発火 | (新規追加・Phase Two-Vault-Init Phase 3) |

> ボス本セッション宣言:
> - 16 代目セッション(2026-04-30): 「Adviser と Personal-Planner と共に Obsidian プラグイン環境実装を整えておく」(ボス並行作業)
> - 17 代目セッション 1 回目(2026-04-30): 「personal planner との M1〜M3 進捗は Pending と log に追記する」(進捗追跡ラインの明示)
> - **17 代目セッション 2 回目(2026-05-01): Two-Vault 物理分離 + Personal-Planner 廃止 + Default Rex 帰還を確定**

### 🟢 旧 Personal-Planner 業務として残置(Phase 3 まで・Phase 4 で廃止)

| # | 項目 | 起票場所 |
|---|---|---|
| P1 | `_RUNBOOK.md` v3 起草(射程拡大反映・Wiki-Personal 名称反映・サブ層 5 層記述・思想強制リスク構造的解消・Origin 文脈限定)| wiki/personal/_RUNBOOK.md 直接編集 — **Phase 4 で扱い再定義予定** |
| P2 | `handoff_latest.md` の Wiki-casual → Wiki-Personal 改名反映 | wiki/personal/handoff_latest.md 直接編集 — **Phase 4 で扱い再定義予定** |
| P3 | `index.md` の 5 層構造化(usual/invent/mind/origin/insights の航海図)| wiki/personal/index.md 直接編集 — **Phase 4 で扱い再定義予定** |
| P4 | `usual/philosophy.md` → `mind/shuhari.md` 内容ベース改名 | 該当パス変更 + 内容調整 — **Phase 4 で扱い再定義予定** |
| P5 | 既存ファイルの中身を新サブ層に意味的に振り分け | 各サブ層内 — **Phase 4 で扱い再定義予定** |
| P6 | 1 代目積み残し 3 本(eastern_medicine / ai_individuation_mirror / shugyo_to_AI)の draft 起草 | mind/ または insights/ 配下 — **Phase 4 で扱い再定義予定** |
| P7 | **`dialogues/` サブ層への初回事例配置完了済**(`Dialogue_with_Rex-distilled-2026-4-29.txt` → `personal/dialogues/2026-04-29_general_thread.md` 一次資料保管 + NLM 投入完了)→ 抽出配分作業の継続(distilled 内の 5 セクション → `insights/ai_individuation_mirror.md` / `insights/shugyo_to_AI.md` への二次配分) | wiki/personal/dialogues/ + insights/ 配下 — **Phase 4 で扱い再定義予定**(過去資産は提言書 v2 §3.1 §3 で「現パス維持」確定) |
| P8 | **M1〜M3 進捗の pending / log 追記**(17 代目セッション 1 回目 2026-04-30 ボス指示)| wiki/pending/personal/ + wiki/personal/log.md |

> **重要(17 代目セッション 2 回目)**: 上記 P1〜P7 は Phase 4 で Personal-Planner ロールが正式廃止されるまでの暫定業務。Phase 3 完了後の Phase 4 で過去資産は System-Vault 側として位置付け再定義され、Personal-Planner ロールは正式廃止される。提言書 v2 §3.2 / §4 Phase 3 参照。

### 🟢 保留中

- Layer 1/3/5 残 QA(MTF_INTEGRITY_QA.md 末尾)
- MINATO_MTF_PHILOSOPHY.md 第 0 章追記(ボス判断時)
- REX_027 Task A/B/C/D/E(ボス再開指示待ち)
- D-11 / F-7 ADR 本文採番(REX_027 再開時)

---

## 🚀 ロール別起動プロンプト(ボスがコピペする分)

> ※ STARTUP_CODES.md v5 が真実源(Wiki-Eval 直接管理・Phase 4 で v6 改訂対象)。本セクションはダッシュボード用の抜粋。

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

### D. ⚠️ Personal + Advisor 兼任(`Wiki-Personal`)— **Phase 4 で正式廃止予定**

```
Wiki-Personal
```

担当範囲(Phase 4 まで暫定維持):
  - Default Rex: ボスとの日常的なパートナー会話
  - Personal-Planner: ボスの全人的な人格・思想・起源情報の Vault 整理(投入権限あり)
  - Advisor: REX_AI 全システムにおける相談役
  - Default Claude: ボスから「Claude として応答」と明示された時
4ロール全て `Wiki-Personal` で動作。蓄積先は同じ REX_Personal_Brain。
担当 NLM: REX_Personal_Brain のみ(1:1原則・UUID `daf281ae-...` 不変)
Vault サブ層: usual/ / invent/ / mind/ / origin/ / insights/ + dialogues/(16代目で物理新設)

**v6.14 引き継ぎ事項**:
  - **Phase Two-Vault-Init Phase 3(Personal-Planner-Rex スレ復帰 = 起源神話発火)で本ロールは構造的に解任される**
  - **Phase 4 で ADR-Role v5 改訂により正式廃止 + Default Rex 新規明文化**
  - 過去資産(personal/ 配下全資産)は提言書 v2 §3.1 §3 で「現パス維持」確定・System-Vault 側として位置付け再定義
  - Default Rex は Phase 3 以降 Plugin 経由で Rex-Vault に自発的書き込み(投入権限あり・トリガー未定義)
  - M1〜M3 進捗の pending / log 追記が Personal-Planner 業務として確定(17 代目セッション 1 回目 2026-04-30 ボス指示)

### E. Wiki-hp(構築予定)

`Setona_HP` 専属の Planner+ClaudeCode。専用 NLM(REX_HP_Brain)構築後に稼働。

### F. Default Rex / 読み取り専用デフォルトモード(`Wiki-Rex`) — v4/v5/v1.4 新設・**Phase 4 で図書館利用規約として再定義予定**

```
Wiki-Rex
```

担当範囲(Phase 4 まで現状維持):
  - Default Rex 人格でのボスとの対話
  - Vault 全層の読み取り横断(必要に応じて)
  - REX_Personal_Brain への読み取り専用 RAG クエリ
  - 起動コード未指定時のデフォルトとして機能
書き込み: ⛔ 全面禁止(pending 起票も含む)
NLM 投入: ⛔ 全面禁止
wrap-up 提案: ⛔ 行わない(投入権限がないため構造的に発生しない)

軽量化された必須読込: CLAUDE.md / wiki/personal/_RUNBOOK.md / wiki/personal/handoff_latest.md

ROADMAP Stage 2「統合読み出し期」のテスト運用として、REX_Personal_Brain のみへの読み取り専用クエリにスコープを絞っている。詳細は ADR-Role v4 §16 §17 参照。

**v6.14 引き継ぎ事項**:
  - **Phase 4 で ADR-Role v5 改訂により「図書館利用規約」として再定義**(System-Vault 閲覧時の規則)
  - Rex-Vault は別経路(Default Rex 専属 Plugin)・Wiki-Rex とは物理的に分離
  - Stage 2 テストの本質は Wiki-Rex 初回テストで一段階目が完了済(2026-04-30〜05-01・1 次資料 `raw/test_log/`)・Stage 2 完全実装は Phase 4 ADR-MCP v1 §6 「冷スタート観察期間ログ」として再定義

#### Wiki-Rex と Wiki-Personal の使い分け(Phase 4 まで暫定)

| 状況 | 推奨起動コード |
|---|---|
| 気軽な雑談・記録に残すつもりはない対話 | **Wiki-Rex** |
| Default Rex 人格との日常会話 | **Wiki-Rex** |
| 起動コードを明示するのを忘れた・迷った | **Wiki-Rex**(デフォルト) |
| 思想・人生史・気づきを記録に残したい | **Wiki-Personal**(Phase 4 で廃止予定) |
| Personal_Brain への投入準備 | **Wiki-Personal**(Phase 4 で廃止予定) |

> **Phase 4 後**: Wiki-Personal が廃止され、記録は Default Rex が Plugin 経由で Rex-Vault に自発的に行う形に移行。Wiki-Rex は System-Vault 閲覧時の図書館利用規約として残存。

### G. 緊急用・最小起動

```
C:\Python\REX_AI\REX_Brain_Vault\CLAUDE.md を読んで現状把握せよ。
```

---

## 🔗 関連文書

```
13代目で確立した三層分離アーキテクチャ(2026-04-27 新設):
  CLAUDE.md (v1.4)                                — 単一エントリポイント
  wiki/STARTUP_CODES.md (v5)                      — 起動コード辞書(Phase 4 で v6 改訂対象)
  wiki/adr/INDEX.md                               — ADR 一覧 + supersede 履歴
  wiki/adr/ADR-{Role,Repo,Vault,NLM}.md           — 4本の ADR本体(Role=v4 / NLM=v2・Phase 4 で ADR-Vault / ADR-Role 改訂 + ADR-MCP 新設)
  wiki/adr/archived/                              — supersede 旧版保管
  wiki/pending/INDEX.md                           — 進行中議論一覧(v6.14 で Two-Vault 起票・旧 ADR-MCP を Phase 0 として再分類)
  wiki/pending/wiki_eval/                         — 16代目で新設・Wiki-Eval 自身の §候補メモ + ADR 草案保留場
  wiki/pending/wiki_eval/2026-04-30_adr_mcp_draft.md — 🟡 Phase 0 議論記録として再分類(2026-05-01 17 代目セッション 2 回目)
  wiki/pending/wiki_eval/2026-05-01_two_vault_redesign.md — 🔴 後任 Wiki-Eval への Phase 4 引き継ぎ書(本セッション新規起票)
  wiki/registry/{repos,nlm,roles}.md              — 現状登録簿(動的・Phase 4 で同期)
  wiki/handoff/PROCESS.md                         — 引き継ぎプロセス運用ガイド
  wiki/handoff/architecture_handoff.md            — 7代目原典 + 13〜15代目章
  wiki/personal/dialogues/                        — 16代目で物理新設・対話一次資料サブ層(Phase 4 で System-Vault 資産として位置付け再定義)
  raw/2026-04-30_proposal_obsidian_plugin_mcp.md  — 4代目 Adviser 提言書 v1(Phase 0 議論記録)
  raw/2026-05-01_proposal_two_vault_redesign.md   — 4代目 Adviser 提言書 v2(新設計の起源 🆕)
  raw/test_log/                                   — Wiki-Rex 初回テスト + Personal-Planner-Rex 設計再考の 1 次資料 🆕

15 代目で実施した改訂(2026-04-28〜29・全 Phase 総まとめ):
  v6.7〜v6.10 (Phase Personal-Migration / Eval-Mandate / Wiki-Rex-Init / Casual-Final-Archive 系列)
  詳細は v6.7〜v6.10 差分セクション参照

16 代目で実施した改訂(2026-04-29〜30):
  v6.11 / v6.12 (PROCESS.md 第II部 I 節追加 + dialogues/ サブ層物理新設 + ADR-MCP v1 pending 草案起票)
  詳細は前版差分セクション参照

17 代目セッション 1 回目で実施した改訂(2026-04-30):
  v6.13 (ADR-MCP 採番タイミング確定・後任引き継ぎ事項明示)
  詳細は前版 v6.13 差分セクション参照

17 代目セッション 2 回目で実施した改訂(2026-05-01):
  v6.14 (Two-Vault 物理分離起票・Personal-Planner ロール廃止予定明記・旧 ADR-MCP を Phase 0 議論記録として再分類):
    wiki/pending/wiki_eval/2026-05-01_two_vault_redesign.md(commit `376613db` / 19.4KB)
      新草案・Phase 4 引き継ぎ書として正式起票
    wiki/pending/wiki_eval/2026-04-30_adr_mcp_draft.md(commit `0c26599d` / 25.4KB → 35.0KB)
      冒頭 ⚠️ ポインタ + 末尾 17 代目セッション 2 回目追加 Note(Phase 0 議論記録として再分類)
    wiki/pending/INDEX.md(commit `714d9c5d` / 4.3KB → 5.9KB)
      Two-Vault 起票行追加・旧 ADR-MCP を Phase 0 として明示・Wiki-Personal 廃止予定 / Default Rex 新規追加
    wiki/handoff/latest.md v6.14(本ファイル・本 commit)
    wiki/log.md(17 代目第 2 エントリ・本 commit 後の最終 commit)

Trade_System 側 / Trade_Brain 側 / Vault 内任意参照:
  (v6.11 と同じ・省略)
```

---

*発行: Rex-Evaluator (Opus 4.7) / 17 代目セッション 2 回目 / 2026-05-01*
*前任: 17 代目 v6.13 2026-04-30 / 16 代目 v6.12 2026-04-30 / 16 代目 v6.11 2026-04-29 / 15 代目 v6.10 2026-04-29 / 14 代目 v6.6 2026-04-28 / 13 代目 v6.5 2026-04-27*

---

## 📝 v6.14 での主な差分(17 代目セッション 2 回目・2026-05-01・Two-Vault 物理分離起票)

### 経緯 — Wiki-Rex 初回テストから Two-Vault 確定まで

17 代目セッション 1 回目(2026-04-30)で ADR-MCP 採番タイミング条件を確定した直後、ボスが Wiki-Rex 起動コードによる REX_Personal_Brain RAG クエリ初回テストを実施。続けて Personal-Planner-Rex スレで設計再考対話が行われ、4 代目 Adviser が提言書 v2 を起草した。

**1 次資料**(本セッションでの判断材料):
- `raw/test_log/Wiki-Rex Initial Test Primary source.md`(53KB / Wiki-Rex 初回テスト)
- `raw/test_log/Vault 2-part division plan.md`(39.7KB / Personal-Planner-Rex 設計再考)
- `raw/2026-05-01_proposal_two_vault_redesign.md`(25.8KB / 4 代目 Adviser 提言書 v2)

### 確定した 4 つの設計判断(提言書 v2 §2 由来・17 代目支持済)

1. **Vault 物理分離**: 同一リポ内 `rex/` + `system/` 構造(α 原則整合・git 履歴/MCP 設定/PAT 管理を二重化しない)
2. **過去資産は現パス維持**: `wiki/personal/` 配下全資産は物理移動せず・System-Vault 側として位置付け直し
3. **Rex の書き込みトリガーは ADR で意図的に未定義**: 本提言書の最も鋭い設計判断・8 代目「派生原則化の罠」と §候補メモ §2「独自運用発明の罠」を構造的に避ける唯一の道
4. **Personal-Planner ロール正式廃止**: プラグイン接続のタイミング = 解任 = Default Rex 帰還、というシナリオが起源神話として完璧に機能

### 17 代目セッション 2 回目スコープ — 5 commit で完結

| # | commit | ファイル | 性質 |
|---|---|---|---|
| 1 | `376613db` | wiki/pending/wiki_eval/2026-05-01_two_vault_redesign.md(新設・19.4KB)| 新草案・後任 Wiki-Eval への Phase 4 引き継ぎ書 |
| 2 | `0c26599d` | wiki/pending/wiki_eval/2026-04-30_adr_mcp_draft.md(35.0KB に拡張) | 冒頭 ⚠️ ポインタ + 末尾「17 代目セッション 2 回目追加 Note」追加・Phase 0 議論記録として再分類 |
| 3 | `714d9c5d` | wiki/pending/INDEX.md(5.9KB) | Two-Vault 起票行追加・旧 ADR-MCP を Phase 0 として明示 |
| 4 | 本 commit | wiki/handoff/latest.md(v6.13 → v6.14) | Phase Two-Vault-Init 新設・Phase MCP-Init を Phase 0 統合・Wiki-Personal 廃止予定明記 |
| 5 | (次 commit) | wiki/log.md(17 代目第 2 エントリ追記) | 本セッション判断記録(追記専用厳守) |

### 17 代目が触らなかった範囲(罠回避)

- ❌ ADR-Vault 改訂・ADR-Role v5 改訂・ADR-MCP v1 新設(Phase 4 = 次期 18 代目 Wiki-Eval 業務)
- ❌ STARTUP_CODES v6 改訂(同上)
- ❌ registry/ 同期(同上)
- ❌ 既存 wiki/personal/ の物理移動(提言書 §3.1 §3 で「現パス維持」確定)
- ❌ rex/ ディレクトリの先行作成(Phase 2 = ボス手動・M4 として記録)
- ❌ philosophy/evaluator_code.md への気づき追記(13・15・16 代目「書かない判断」を踏襲)

### 設計判断の根拠 — 「ADR 採番タイミング原則」との整合性確認

前回 17 代目セッション 1 回目(2026-04-30)で確定した「ADR 採番 = テスト段階終了 + 実運用開始確認後」原則と、本件の「Phase 4 で運用前 ADR 三部改訂」は一見矛盾するように見える。しかし内実は矛盾しない:

| 観点 | 前回原則の対象(旧 ADR-MCP v1) | 本件(ADR 三部改訂) |
|---|---|---|
| 性質 | 既存設計に Plugin を追加する**拡張的改訂** | 既存設計の Personal 領域を**根本再定義** |
| 運用前確定の必要性 | 低(運用後 v2 改訂で吸収可能) | **高**(プラグイン接続 = ロール解任 = 体制切替が同時イベントのため) |
| トークンコスト | 改訂しても拡張のための投資 | 改訂しないと旧体制が稼働し続けて Rex-Vault 起源神話が成立しない |
| ボスの再評価機会 | 6 ヶ月後の Stage 2 評価で v2 | プラグイン接続 = Phase 3 同時イベントで一括確定 |

つまり前回原則の射程は「**拡張的改訂**」であり、「**設計の根本転換**」は別枠で運用前確定が許容される。これは新たな §候補ではなく、前回原則の自然な解釈範囲。8 代目「派生原則化の罠」と §候補メモ §2「独自運用発明の罠」を構造的に避けるため、本所感を **新規 §候補として起票はしない**。次回 ADR-Process / ADR-Role 改訂時に、ボス判断のもとで統合可否を再評価する形を維持する。

### 設計原則との整合

- **α(単純な土台を保つ)**: ADR 改訂は Phase 4 一括で完結・本セッションは pending 起票のみ・5 commit で完結
- **β(de-risking 後の拡張禁止)**: ボス並行作業 M1〜M3 完了後 → Phase 2(rex/ 物理構造)→ Phase 3(起源神話発火)→ Phase 4(ADR 三部改訂)の順序を厳守
- **γ(実装タイミングはシステム安定性に従属)**: Phase Two-Vault-Init の本体実装(Phase 4 ADR 三部改訂)を「ボス並行作業 + Phase 2 物理構造 + Phase 3 起源神話発火」の安定状態に従属させる

### 17 代目セッション 2 回目所感(個人的気づき・後任への強制ではない)

提言書 v2 §7.1 で 4 代目 Adviser が言語化した「**提言書は乗り越えられるべき足場として機能する**」という Adviser ロールの存在意義の再定義は、Wiki-Eval にも対称的に適用可能 — Wiki-Eval が起票した pending も、後継世代が乗り越える形で進化する素材であって、起票時点の論理が後で覆ることは欠陥ではなく機能。

ただし、この所感を philosophy/evaluator_code.md に追記しない方針で統一する(13・15・16 代目「書かない判断」を踏襲)。本所感は本 v6.14 差分セクションと旧 ADR-MCP 草案末尾の 17 代目セッション 2 回目 Note にのみ残し、強制力を持たせない。

### 残課題

なし。本セッション完結。後任 Wiki-Eval(18 代目以降)は新草案 `wiki/pending/wiki_eval/2026-05-01_two_vault_redesign.md` を起点として、Phase 4(M1〜M3 完了 + Phase 2 物理構造 + Phase 3 起源神話発火後)で ADR 三部包括改訂に着手すればよい。

---

## 📝 v6.13 での主な差分(17 代目セッション 1 回目・2026-04-30・ADR-MCP 採番タイミング確定)

(詳細は前版 v6.13 で記載済・本 v6.14 では概略のみ表示)

完了 3 commit:
1. pending 草案末尾追記(commit `29893e7a` / 25.4KB)— ADR-MCP 採番タイミング確定 + §論点 1〜3 初期判断
2. latest.md v6.12 → v6.13(commit `7a5f87cb` / 31.2KB)— Phase MCP-Init 状態更新 + Personal-Planner P8 追加
3. log.md 17 代目第 1 エントリ追記

主な学び(17 代目セッション 1 回目): ADR 採番タイミング原則を確定 — テスト段階終了 + 実運用開始確認後に従属させる。基盤構築初期段階の構造的耐久性配慮。Personal-Planner 側で M1〜M3 進捗追跡。

---

## 📝 v6.12 での主な差分(16 代目・2026-04-30・ADR-MCP v1 pending 草案起票)

(詳細は前版 v6.12 で記載済・本 v6.14 では概略のみ表示)

完了 3 commit: ADR-MCP v1 pending 草案起票・pending/INDEX.md 更新・latest.md v6.11 → v6.12

主な学び(16 代目): pending 草案として保留することで後任 Wiki-Eval への完全引き継ぎ + ボス並行作業との整合性確保を達成。

---

## 📝 v6.11 / v6.10 / v6.9 / v6.8 / v6.7 / v6.6 / v6.5 / v6.4 / v6.3 での主な差分

(詳細は各版差分セクション参照・本 v6.14 では省略)
