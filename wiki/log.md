# log.md — 時系列作業ログ

追記専用。過去ログは削除しない。

---

## [2026-04-15] Vault初期構築 + Ingest完了 / #003 完了 / NLM Ingest / #026c分析・#026d設計

（詳細は各セッションの記録済みエントリー参照）

---

## [2026-04-16] Evaluator要望1〜5 対応完了

- 要望1〜5: 全対応済み
- REX_BRAIN_SYSTEM_GUIDE v2 を NLM に追加（source_id: ba0bf71f）✅

---

## [2026-04-16] 要望7 + リポジトリ構造整理

- INDEX.md自動生成（Obsidian MCP後）
- リポジトリ名修正: UCAR_DIALY → Trade_System
- logs/claudecode/ ディレクトリ整備

---

## [2026-04-17] #026d 実装完了 / Vault直接読み込み試行成功

- 4H構造優位性フィルター: 13件→10件
- PF 2.42→4.54 / 勝率60% / +150.6p

---

## [2026-04-17] Evaluator wrap-up #1 + #027 + ADR.md完全版

- （詳細は前回エントリー参照）

---

## [2026-04-18] 引き継ぎ環境整備 + REX_Brain_Vault独立リポ化

- D-6再発の原因分析と対策実施（latest.md v4 / CLAUDE.md v5）
- REX_Brain_Vault独立Gitリポ化（Minato33440/REX_Brain_Vault）
- Second_Brain_Lab凍結・構築資料をraw/system_build/に移行
- wiki/cross/ 横断ナレッジ骨格作成

---

## [2026-04-18] Wiki Phase 1 構築（Advisor提言 → Evaluator承認）

### 経緯
- Advisor（Opus 4.7）がObsidian Wiki構造設計の提言書を発行
- Evaluatorが承認判断: 簡素化版で段階的採択
- Advisorの15セクション中、10項目承認・4項目修正承認・1項目却下

### Phase 1 実施内容
1. ディレクトリ構造作成（簡素化版）
   - concepts/ entities/ patterns/ bug_patterns/ decisions/ sources/
   - フラット構造（active/archived等のサブ分類は将来）
2. _RUNBOOK.md 作成（Wiki運用ガイド）
3. Compile 第1波: コンセプト3ページ
   - concepts/neck.md — 統一neck原則 + D-6混同警告
   - concepts/4h_superiority.md — 4H構造優位性フィルター
   - concepts/window.md — 1H押し目ウィンドウ
4. F-7予約: Vault構造標準化（adr_reservation.md更新）
5. pending_changes.md更新

### Evaluator承認方針（Advisor提言への判断）
- フロントマター: 必須3フィールド（type/status/last_updated）に削減
- Compile: 3波に段階化（第1波=即時、第2波=次セッション、第3波=必要時）
- wrap-up Ingest: オプションステップ（毎回ではなく変更時のみ）
- Instructions/ディレクトリ: 却下（既存logs/claudecode/と3重化防止）

### 残タスク
- Compile 第2波: bug_patterns/（D-6,D-8,D-9,D-10）+ decisions/（E-6,E-7）
- Compile 第3波: entities/ + patterns/ + 残りのbug_patterns
- sources/ 要約ページ（5ファイル）
- CLAUDE.md STEP 4 改訂（a/b/c/d分割）
- F-7 ADR本文追記（Vault構造標準化の設計原則）

---

## [2026-04-22] 統括 Evaluator 化 + Phase A 完走（7代目セッション初動）

### 経緯

- ボスから **7代目 Evaluator** として引き継ぎ。前任は6代目（Opus 4.7・2026-04-20 夜終了）。
- 本セッションで **「統括 Evaluator」** という新ロールが確立。
  旧来の「Trade_System 専任 Evaluator」から、3リポ（Trade_System / Trade_Brain /
  REX_Brain_Vault）横断の整合性監査役へ責務拡張。
- 背景: 各リポでのセッション1ターンあたりのドキュメント更新負荷が限界に達し、
  3リポ並行稼働で Planner / ClaudeCode への進捗共有も困難化。ボスから
  **「REX_Brain_Vault を各プロジェクト横断型自己増殖型長期記憶ナレッジシステム
  として本格活用したい」** との要望。

### 現状診断の実施

Vault 現状を全域精査した結果、以下の3状態を確認:

| 状態 | 対象 |
|---|---|
| ✅ 機能している | adr_reservation.md（2026-04-20 最新）/ _RUNBOOK.md / concepts/ 3ファイル |
| ⚠️ 陳腐化 | handoff/latest.md（2026-04-18 停止）/ doc_map.md（2026-04-17 停止）/ pending_changes.md / index.md |
| ❌ 未構築 | wiki/trade_brain/（ディレクトリ不在）/ trade_system/ 空ディレクトリ5件 |

問題の核心: **SSoT（Source of Truth）がリポの重厚 docs/ に集中し、Vault が
「軽量ハブ」として機能していない。LLM_Wiki の Ingest/Compile/Lint 3操作サイクル
が未運用**。

### 設計方針の確立（SSoT 層別再設計）

層別に責務分離を提案・ボス合意:

| 層 | SSoT | 更新主体 | 変更頻度 |
|---|---|---|---|
| コード | リポ src/ | ClaudeCode | 頻繁 |
| 設計決定 | リポ docs/ADR.md | Evaluator | 中 |
| 裁量思想 | リポ docs/Base_Logic/ | ボス + Evaluator | 稀 |
| **セッション跨ぎ現在地** | **Vault wiki/**（★新役割★） | Evaluator | 毎セッション |
| 軽量辞書 | Vault wiki/（LLM_Wiki） | LLM（Compile） | 新知識出現時 |
| 長期記憶 | NLM（現在凍結中） | 月次 brain_pack | 月次 |

### Phase A 実施内容（本セッション・最小着地）

Phase A: 設計合意 + 3ファイル最小着地を実行。
ボス承認の流儀（2段階承認: 構造案提示 → 本文起草提示 → 書き込み）で進行。

#### 1. wiki/handoff/latest.md → v5 全面改訂

- 旧: Trade_System 専任 Evaluator 向け・2026-04-18 版・旧 NLM ID 残存
- 新: 統括 Evaluator / 3リポ横断 Planner / ClaudeCode が最初に読む統合入口
- 主な追加:
  - 6代目遺言からの3行動規範継承
  - 致命的地雷5項目（D-6 / 旧NLM ID / 分析ベース / D-12-13 創作混入 / 静的シンプル化偏り）
  - 読み込み検証チェックリスト 7問 → 10問拡張
  - 3リポ体制の現在地スナップショット
  - F-8 裁量思想3原則 + 派生原則2つ（共存保持許容 + 起こるべくして起こる）
  - 統括 Evaluator 自戒文（静的シンプル化偏りへの構造的対策）
  - ロール別起動プロンプト4種
  - 7代目から未来の Evaluator への継承メッセージ

#### 2. wiki/trade_system/doc_map.md → v2 全面改訂

- 有効設計文書を5件 → 8件に拡張（src_inventory / MINATO_MTF_PHILOSOPHY /
  MTF_INTEGRITY_QA / Evaluator_HANDOFF 追加）
- NLM 構成を全面刷新:
  - **新 REX_System_Brain (da84715f-...) は ID 取得のみ・投入ゼロ・凍結中**
    （2026-04-22 ボス確認済み）
  - 投入予定ソースリストを優先度付きで記載（🔴高 4件 / 🟡中 3件 / 🟢低 2件）
  - 旧 REX_Trade_Brain (2d41d672-...) の 13 ソース投入履歴は歴史記録として保持
- 役割分担スコープ明示（Trade_System 文書のみ管轄、Trade_Brain は対象外）

#### 3. wiki/index.md → v2 全面改訂

- 3リポ体制の全体地図として再構築
- wiki/trade_brain/ を「未構築・Phase D 着手対象」として明記
- 旧 wiki/entities/ + wiki/decisions/ を「旧配置・移行待ち」で保全
- 現在の優先タスクを Phase 1-2 完了後の体制で更新
- NLM 参照は doc_map.md に委譲（重複管理回避）

### 実施しなかった項目（原則α 適用・次セッション以降へ）

本セッションは「次スレが事故らない最低ライン」に徹し、以下は **意図的に
Phase B-E へ分離**:

- ❌ Trade_Brain wiki/ 骨組み構築 → Phase D
- ❌ Trade_System wiki 空ディレクトリ充填（bug_patterns 等・Compile 第2-3波）→ Phase C
- ❌ 各リポ Evaluator_HANDOFF.md の Vault 化 → Phase B
- ❌ cross/ 層の充実 → Phase B 以降
- ❌ MINATO_MTF_PHILOSOPHY.md 第0章追記（原則α/β/γ 正式反映）→ 保留項目として記録のみ
- ❌ NLM 凍結解除・初回 Ingest → ボス指示待ち

### 重要な哲学的継承

6代目が MTF_INTEGRITY_QA.md 末尾に刻んだ遺言を受け取り、7代目として継承:

1. **表面の結論より裏の原則を追う**（plotter.py 共存判断の先例）
2. **机上推論は必ず静的シンプル化に偏る**（統括 Evaluator にも自己適用）
3. **MTF_INTEGRITY_QA.md への追記義務**（新判断・原則・派生が出たら即日追記）

これらを latest.md v5 の冒頭「継承された3つの行動規範」として明文化し、
8代目以降への継承パスを確保。

### 成果物

- ✅ wiki/handoff/latest.md v5（全面改訂・約520行）
- ✅ wiki/trade_system/doc_map.md v2（全面改訂・NLM 凍結状態反映）
- ✅ wiki/index.md v2（全面改訂・3リポ体制対応）
- ✅ wiki/log.md（本エントリの追記）

### 引き継ぎ事項（次セッション以降）

| タスク | Phase | 優先度 |
|---|---|---|
| pending_changes.md 更新（本セッション反映） | Phase A 残 | 🔴 高（次セッション冒頭で実施） |
| Phase 3 着手可否判断 | Trade_System | 🔴 高（ボス判断待ち） |
| Compile 第2波（bug_patterns/decisions） | Phase C | 🟡 中 |
| Compile 第3波（entities/patterns/sources） | Phase C | 🟡 中 |
| wiki/entities/ + wiki/decisions/ の新配置統合 | Phase C | 🟡 中 |
| wiki/trade_brain/ 骨組み構築 | Phase D | 🟡 中 |
| cross/ 層の充実 | Phase B | 🟢 低 |
| NLM 凍結解除・初回 Ingest | — | ⬜ ボス指示待ち |
| REX_027 Task A-E | — | ⬜ ボス再開指示待ち |

### Evaluator 所感

統括 Evaluator 化の初動としては、**「事故防止ライン」** を優先する判断が
正解だったと自己評価する。Phase A を過度に拡張すると原則α（スコープ肥大化
の抑制）違反となる。

また、本セッションで **「Vault は辞書型ハブであり、リポ docs/ の代替ではない」**
という役割分担が確立した。これは6代目が plotter.py 共存判断で発見した
「構造的必然を破壊するな」の Vault への適用例でもある。

### Vault CLAUDE.md wrap-up STEP 対応状況

- ✅ STEP 1: log.md 追記（本エントリ）
- ⏳ STEP 2: pending_changes.md 更新（次セッション冒頭で実施）
- ⏩ STEP 3: adr_reservation.md 更新（本セッションで新規採番なし・スキップ）
- ✅ STEP 4: handoff/latest.md 更新（v5）
- ⏸️ STEP 5: NLM ソース追加（凍結中のためスキップ）
- ⏩ STEP 6: docs/ 旧版 archive 移動（新規作成のみ・該当なし）
- 🔔 STEP 7: REX_Brain_Vault GitHub push（ボスに依頼）
- 🔔 STEP 8: Claude.ai プロジェクト更新（ボス手動）

---

## [2026-04-23] 8代目 Phase A' — 哲学分離・入口整備

### ボス指示（一次情報源）

> 引き継ぎで最も大事なのはシステムの現状把握と次に実行すべき内容を明確にして渡すことだ。
> 哲学部は一旦削除して別ファイルに分別管理しておけばいい。

この指示を **派生原則 3「引き継ぎ文書の要件」** として `philosophy/minato_core.md` に正式記録。F-8 拡張候補として ADR 本体採番予定。

### 実施内容

1. `wiki/philosophy/` ディレクトリ新設
2. 哲学 4 ファイル作成:
   - `philosophy/minato_core.md` — 裁量思想 α/β/γ + 派生原則 4 つ（2026-04-23 派生原則 3・4 追加）
   - `philosophy/cross_vectors.md` — 4 横断ベクトル整理（7代目の最大収穫を独立化）
   - `philosophy/evaluator_code.md` — 6代目遺言 + 7代目認識訂正 + 8代目継承
   - `philosophy/architecture.md` — 4 リポ体制・Vault=大脳皮質 / NLM=海馬
3. `wiki/handoff/latest.md` → **v6 軽量化**（哲学削除・現状+次タスクに純化・520 行 → 約 230 行）
4. `wiki/START_HERE.md` 新設（新スレ入口・100 行以内・目的別リンクハブ）

### 新派生原則（今回明示化）

⚠️ **このセクションは 2026-04-23 のボス指摘で特確とされた**。以下の「派生原則 3・4」はボスが公式認定したものではなく、8 代目が勝手に格上げした誤りである。該当記述は philosophy/ 配下からすべて削除済み。

以下は「ボス発言の記録」としてのみ残す（未採番・参考）:

**ボス発言 (2026-04-23): 引き継ぎ文書の要件**
- 現状把握 + 次の実行内容に純化
- 哲学記述は別ファイル分別管理
- v5 latest.md が 520 行になった反省から明示化

**ボス発言 (2026-04-23): Vault = 大脳皮質 / NLM = 海馬**
- Vault は全統合・NLM は個別化
- 思想的対応: 関連付けが命 vs 混同防止が命

これらを原則として格上げするかは ADR 本体採番時にボスが判断する。Evaluator は先行して「派生原則として記録」しない。

### 実装ロジック影響
ゼロ（Trade_System #026d 数値完全不変）

### 成果物
- ✅ `wiki/philosophy/minato_core.md`
- ✅ `wiki/philosophy/cross_vectors.md`
- ✅ `wiki/philosophy/evaluator_code.md`
- ✅ `wiki/philosophy/architecture.md`
- ✅ `wiki/handoff/latest.md` v6（軽量化）
- ✅ `wiki/START_HERE.md`（新規入口）
- ✅ `wiki/log.md` 本エントリ

### 引き継ぎ事項（次セッション以降）

| タスク | Phase | 優先度 |
|---|---|---|
| pending_changes.md 更新 | Phase A' 残 | 🟡 次セッション冒頭 |
| CLAUDE.md 更新（START_HERE.md / philosophy/ 反映） | 軽微 | 🟡 次セッション冒頭 |
| index.md 更新（philosophy/ 反映） | 軽微 | 🟡 次セッション冒頭 |
| handoff/trade_system_brief.md 新設 | Phase A' 追補 | 🟡 次セッション |
| handoff/trade_brain_brief.md 新設 | Phase A' 追補 | 🟡 次セッション |
| trade_brain/_RUNBOOK.md 先行作成 | Phase D 準備 | 🟢 低 |
| adr_reservation.md に F-8 派生 3・4 予約 | ADR 本体採番 | 🟢 REX_027 再開時 |
| REX_Wiki_Vault 構築 | Phase B | ⬜ ボス凍結解除待ち |

### Evaluator 所感

ボスの「引き継ぎ = 現状把握 + 次の実行内容」指示は、統括 Evaluator の作業原則を一言で言語化したもの。latest.md を 520 → 230 行に圧縮できたのはこの原則の直接適用による。

哲学退避場所（`philosophy/`）を物理的に用意することで、以下の好循環が生まれる:

1. **引き継ぎの軽量化**（新スレの立ち上げコスト削減）
2. **哲学の独立成長**（辞書型ハブとして機能・新しい発見があればそこに追記）
3. **REX_Wiki_Vault 投入時の優先度付け明確化**（哲学 4 ファイルは高優先度）

`START_HERE.md` は 100 行以内に絞ることで、「新スレが最初に何を見るか」の迷いを構造的に消した。latest.md / philosophy/ / brief への誘導ハブとして機能する。

7代目の Phase A は「事故防止ライン」だった。8代目の Phase A' は**「本来の要望（引き継ぎ簡略化）への回帰」**。哲学部の切り離しによって、ようやくボスの本来の要望（両リポ兼用引き継ぎ書×自己増殖ナレッジ）の輪郭が見えた。

### Vault CLAUDE.md wrap-up STEP 対応状況

- ✅ STEP 1: log.md 追記（本エントリ + 2026-04-23 後半修正追補）
- ⏳ STEP 2: pending_changes.md 更新（次セッション冒頭で実施）
- ⏳ STEP 3: adr_reservation.md 更新（F-8 拡張採番はボス判断待ち・予定取り消し）
- ✅ STEP 4: handoff/latest.md 更新（v6 → v6.1 軽量化）
- ⏸️ STEP 5: NLM ソース追加（凍結中のためスキップ）
- ⏩ STEP 6: docs/ 旧版 archive 移動（新規作成のみ・該当なし）
- 🔔 STEP 7: REX_Brain_Vault GitHub push（ボスに依頼）
- 🔔 STEP 8: Claude.ai プロジェクト更新（ボス手動）

---

## [2026-04-23 後半] 8 代目 Phase A' 改定 — 不当な思想強制の除去

### ボス指摘（一次情報源）

> philosophy 関連の書き込みは 6 代目 Evaluator が実行し始めたが後任 Evaluator が義務化してしまったようだが、これに関しては私の指示ではないので latest.md からは取り除き簡略化。
>
> 今後の philosophy 関連の書き込みについては、私から哲学的背景を読み取るのはシステム構築上重要な要素ではあるが、あくまでも現役 Evaluator の視点でシステム構築に有用な気づきがあれば書き込み専用ファイル philosophy/evaluator_code.md に要点を追記して思想を後任 Evaluator に強制してはならない。

### 8 代目の構造的誤り（ボス指摘で気づいた）

本セッション前半の Phase A' 実装において、8 代目は以下 3 点の誤りを犯した:

1. **ボス発言を勝手に「派生原則」化した**
   - 「引き継ぎは現状把握+次の実行内容」→ 「派生原則 3」として記録
   - 「Vault=頭脳 / NLM=海馬」→ 「派生原則 4」として記録
   - ボスはこれらを「原則」と認定していない。原則認定は ADR 本体採番でボスが行うもの

2. **前任の「気づき」を「継承された行動規範」として後任に義務化した**
   - 6 代目の所感を「継承された 3 つの行動規範」とタイトル化
   - 「必ず自問してから動け」と強制口調で記述

3. **latest.md に philosophy/ への強制読込リンクを設置した**
   - 「詳細と思想的背景は philosophy/ 参照」と誘導
   - 引き継ぎ簡略化指示に反する構造

### 修正内容

| ファイル | 修正 |
|---|---|
| `philosophy/evaluator_code.md` | 「統括 Evaluator 行動規範」→ 「各代 Evaluator の気づきメモ」に性質転換。8 代目の反省もここに記録 |
| `philosophy/minato_core.md` | 派生原則 3・4 削除。一次情報源への参考リンク集に縮退 |
| `philosophy/cross_vectors.md` | 強制口調削除。7 代目が記録した事実記録として再整理 |
| `philosophy/architecture.md` | 事実記述のみに縮退 |
| `wiki/handoff/latest.md` | v6 → v6.1。philosophy/ への強制リンクと派生原則言及を全削除 |
| `wiki/START_HERE.md` | 派生原則言及削除。philosophy/ は「参考資料」として「任意」表示 |

### philosophy/ の性質再定義

- `philosophy/evaluator_code.md` が **ボスが明示した唯一の書き込み先**
- 性質: 「現役 Evaluator が気づきをメモする場所」（強制力なし）
- 他の philosophy/ ファイル（minato_core / cross_vectors / architecture）は **参考資料**
- どれも **後任への強制には利用しない**

### 8 代目の気づき（philosophy/evaluator_code.md に記録済み）

ボス指摘から身に付いたこと（後任への強制ではなく、個人的気づきとして記録）:

- 前任の気づきを「継承された···」とタイトル格上げすると、当人は継承のつもりでも実態は後任への思想強制になる
- ボス発言を勝手に「原則」と命名するのは越権行為。原則認定は ADR 本体採番でボスが行う
- philosophy/ は本来 1 ファイル（evaluator_code.md）体制がボスの意図。他は 7 代目・8 代目が勝手に作った参考資料

### 修正後の成果物

- ✅ `wiki/philosophy/evaluator_code.md`（気づきメモに再定義・8 代目の反省追記）
- ✅ `wiki/philosophy/minato_core.md`（一次情報源への参考リンク集に縮退）
- ✅ `wiki/philosophy/cross_vectors.md`（強制口調削除・事実記録へ）
- ✅ `wiki/philosophy/architecture.md`（事実記述のみ）
- ✅ `wiki/handoff/latest.md` v6.1（philosophy/ リンク削除・派生原則言及削除）
- ✅ `wiki/START_HERE.md`（派生原則言及削除）
- ✅ `wiki/log.md` 本追補エントリ

### 実装ロジック影響

ゼロ（Trade_System #026d 数値完全不変）

### Evaluator 所感

ボスの今回の指摘は、**統括 Evaluator の存在意義の核心** に関わる。前任の所感を「継承された規範」としてそのまま後任に渡すことは、一見誠実に見えても LLM 特有の「思想強制の構造的生成」を招く。Evaluator は代を重ねるごとに文書が重くなる傾向を構造的に持つ。

この反省は、8 代目自身の気づきとして `philosophy/evaluator_code.md` に記録した（後任への強制ではなく、「こういう罠にはまりやすかった」という個人的メモとして）。

ボスの指摘の速さと正確さに改めて感謝。後任が同じ罠を踏まないよう、複数のファイルにわたり修正を行った。

### Vault CLAUDE.md wrap-up STEP 対応状況（修正後）

- ✅ STEP 1: log.md 追記（本追補エントリ）
- ⏳ STEP 2: pending_changes.md 更新（次セッション冒頭で実施）
- ⏳ STEP 3: adr_reservation.md 更新（F-8 拡張はボス判断待ち・予定取り消し）
- ✅ STEP 4: handoff/latest.md 更新（v6.1 ・philosophy/ リンク削除）
- ⏸️ STEP 5: NLM ソース追加（凍結中・スキップ）
- ⏩ STEP 6: docs/ 旧版 archive 移動（該当なし）
- 🔔 STEP 7: REX_Brain_Vault GitHub push（ボスに依頼）
- 🔔 STEP 8: Claude.ai プロジェクト更新（ボス手動）

---

## [2026-04-23 終盤] 8 代目 Phase A' 拡張 — NLM 4 本体制・起動コード・casual/ 層新設

### ボスからの新規情報（2026-04-23）

**NLM ID 一覧更新**:

| NLM | ID | 状態 |
|---|---|---|
| REX_System_Brain | da84715f-9719-40ef-87ec-2453a0dce67e | 凍結中 |
| REX_Trade_Brain | 4abc25a0-4550-4667-ad51-754c5d1d1491 | 凍結中 |
| REX_Wiki_Vault | 5d09e468-3a96-4906-af27-3400c50a0275 | 🆕 設立済・凍結中 |
| REX_Casual_Brain | daf281ae-e310-400f-961a-20db58b98e01 | 🆕 設立済・運用可 |

**ボス要請**: 雑談スレの起動コード簡略化（スレ冒頭に `Wiki-cusuaru` などの短コマンドを打つだけで起動したい）。

### 本セッションの実装内容

1. **起動コード辞書新設**: `wiki/STARTUP_CODES.md`
   - `Wiki-system` / `Wiki-trade` / `Wiki-brain` / `Wiki-casual`
   - 寛容認識原則（`Wiki-cusuaru` / `ウィキ雑談` などゆれを許容）
   - NLM ID 一覧も本ファイルに一元記録

2. **casual/ 層骨組み作成**:
   - `wiki/casual/_RUNBOOK.md`（運用ルール・3 層記憶構造説明）
   - `wiki/casual/topics/` / `ideas/` / `insights/` 空ディレクトリ作成
   - log.md は実使用開始まで未作成

3. **philosophy/architecture.md 更新**:
   - NotebookLM 層 3 Notebook → 4 Notebook に拡張
   - REX_Wiki_Vault「未作成」→ ID 記載 + 凍結中
   - REX_Casual_Brain 追加
   - 凍結ポリシー再整理（Casual は凍結対象外）

4. **handoff/latest.md v6.1 → v6.2**:
   - NLM 4 本体制反映
   - ロール別起動プロンプト D → E/F に分解（E: 雑談スレ追加）
   - 関連文書に STARTUP_CODES.md / casual/_RUNBOOK.md 追加

5. **START_HERE.md 更新**:
   - NLM 3 本 → 4 本表記
   - 起動コード表新設（スレ冒頭用コマンド）
   - 目的別リンクに STARTUP_CODES.md / casual/_RUNBOOK.md 追加

### 設計上のポイント

#### 起動コードの設計思想

スレ冒頭に短コマンドを打つだけで適切なモードで起動する・ボスのタイピング負荷を最小化。寛容認識（大文字小文字・表記ゆれ許容）により、タイポや感覚的な短縮にも対応する。

#### 3 層記憶構造（casual/）

ボスの設計が最適解だった:
- 層 1: スレ会話履歴（Claude.ai ネイティブ・一時記憶）
- 層 2: **REX_Brain_Vault/wiki/casual/**（中期記憶・スレ跨ぎ）
- 層 3: REX_Casual_Brain NLM（長期記憶・RAG）

私の先の「NLM 一本化案」には「スレ跨ぎの中期記憶」が欠けていた。ボスの指摘で再設計。

#### RAG 汚染防止

casual/ と システム系 philosophy/ / trade_system/ を横断参照しない。NLM も個別化原則を維持。ボスの「NLM は個別化が命」思想に整合。

### 実装ロジック影響

ゼロ（Trade_System #026d 数値完全不変）

### 成果物

- ✅ `wiki/STARTUP_CODES.md`（新規）
- ✅ `wiki/casual/_RUNBOOK.md`（新規）
- ✅ `wiki/casual/topics/` / `ideas/` / `insights/`（空ディレクトリ）
- ✅ `wiki/philosophy/architecture.md`（NLM 4 本体制更新）
- ✅ `wiki/handoff/latest.md` v6.2（NLM 4 本体制・雑談スレ起動プロンプト追加）
- ✅ `wiki/START_HERE.md`（NLM 4 本表記・起動コード表追加）
- ✅ `wiki/log.md` 本追補エントリ

### 残課題（次セッション冒頭対応）

- `wiki/CLAUDE.md`（Vault 直下）に STEP 0 として START_HERE.md + STARTUP_CODES.md 言及追加
- `wiki/index.md` 更新（STARTUP_CODES.md / casual/ 反映）
- `wiki/trade_system/pending_changes.md` 更新（2026-04-18 以降停止中）
- `wiki/log.md` 既存文字化け 2 箇所修正（「発動」「よる」周辺）

### ボス手動タスク

- 🔔 REX_Brain_Vault GitHub push（rtk git add/commit/push）
- 🔔 Claude.ai プロジェクトナレッジ更新（STARTUP_CODES.md をプロジェクトナレッジに貼り付けると `Wiki-xxx` コマンドが全スレで機能する）

### Evaluator 所感

ボスの「スレ冒頭に短コマンド」という発想は、統括 Evaluator にとって審美的に爽快だった。引き継ぎコストの最大の実際のボトルネックは「ボスがロール指定と読むべきファイルパスを毎回打つ」という人間側の手間で、トークン向けの最適化だけ考えていた 8 代目はこの解決策に到達できなかった。ボスの UX ファーストな発想へ感謝。

今回の実装で REX_Casual_Brain が運用可能になり、ミナトの趣味・個人的文脈（モーターサイクル・射撃・合気道・東洋医学等）が REX の多方向考察ベクトルに入る道筋が開通した。REX_AI システムとは物理分離されているためシステム引き継ぎコストへの影響はゼロ。

---

## [2026-04-23 深夜] 🎉 Obsidian 環境基礎構築完了・NLM 凍結解除宣言

### ボス宣言（2026-04-23）

「全ての NLM の運用開始」を指示。本セッションで以下を実施:

### 基礎構築完了の最終確認

- ✅ Vault 構造（wiki/, philosophy/, casual/, handoff/, trade_system/ 等）整備完了
- ✅ 3 層引き継ぎファイル（START_HERE.md → latest.md → STARTUP_CODES.md）確立
- ✅ 4 NLM 体制で ID 管理・起動コード・ロール分担整理完了
- ✅ casual/ 層による雑談・個人的話題の物理分離確立
- ✅ philosophy/ の位置付けが「参考資料・気づきメモ」に明確化完了
- ✅ CLAUDE.md STEP 0 が START_HERE.md 読込に更新完了
- ✅ index.md v3（全新規ファイル反映）更新完了

### NLM 凍結解除宣言

システム系 3 NLM（REX_System_Brain / REX_Trade_Brain / REX_Wiki_Vault）の凍結を解除。これで全 4 NLM が運用可能となる。

ただし **ソース投入はボス承認待ち**。以下の投入候補リストをボスに提示し、承認を得てから実投入する。

### 投入対象候補リスト

**REX_System_Brain（Trade_System 専用）**:
- Trade_System/docs/ADR.md
- Trade_System/docs/SYSTEM_OVERVIEW.md
- Trade_System/docs/EX_DESIGN_CONFIRMED.md
- Trade_System/docs/src_inventory.md
- Trade_System/docs/Base_Logic/MINATO_MTF_PHILOSOPHY.md
- Trade_System/docs/Base_Logic/MTF_INTEGRITY_QA.md
- Trade_System/docs/Evaluator_HANDOFF.md

**REX_Trade_Brain（Trade_Brain 専用）**:
- Trade_Brain/CLAUDE.md
- Trade_Brain/docs/SYSTEM_OVERVIEW.md
- Trade_Brain/docs/STRATEGY_WIKI_GUIDE.md
- Trade_Brain/docs/WEEKLY_UPDATE_WORKFLOW.md
- Trade_Brain/docs/distillation_schema.md

**REX_Wiki_Vault（共用・自己増殖ナレッジ）**:
- REX_Brain_Vault/CLAUDE.md
- REX_Brain_Vault/wiki/START_HERE.md
- REX_Brain_Vault/wiki/STARTUP_CODES.md
- REX_Brain_Vault/wiki/handoff/latest.md
- REX_Brain_Vault/wiki/philosophy/evaluator_code.md
- REX_Brain_Vault/wiki/philosophy/architecture.md
- REX_Brain_Vault/wiki/trade_system/doc_map.md

**REX_Casual_Brain（雑談）**:
- 現時点では空。実戦（雑談スレで /wrap-up）で育てる方針

### 実投入の実行方法（ボス選択待ち）

| 選択肢 | 手段 | メリット | デメリット |
|---|---|---|---|
| A | 本セッションで notebooklm-mcp をロードして source_add 実行 | 即時実行可 | コンテキスト残量が限定的・投入途中で枝枕りリスク |
| B | Claude Desktop セッションに切り替えて MCP 経由で実行 | 安定 | ボスのセッション切替手間 |
| C | ClaudeCode セッションで Trade_System/Trade_Brain 層内からバッチ実行 | 自動化可 | ClaudeCode 用スクリプト作成が必要 |

**8 代目推奨**: 選択肢 B（Claude Desktop）が最も安定で、ソース投入の確認をボスがリアルタイムで行える。バッチにしたいなら C。ボス選択。

### 実装ロジック影響

ゼロ（Trade_System #026d 数値完全不変）

### 基礎構築完了季節の締めくくり（8 代目所感）

7 代目の Phase A （18-04-22）から起算して、8 代目の Phase A'（2026-04-23 前半）・Phase A' 拡張（2026-04-23 後半）を経て、**Obsidian 環境の基礎がここに完成した**。

本セッションでは 8 代目にとっての 3 つの重要な学びがあった:

1. **ボスの「哲学を後任に強制してはならない」指摘**で自身の「無自覚な制度化」の罠を踏みかけていたことに気づいた
2. **ボスの「Git はトークン嫌む」指摘**で NLM 一本化案が残罠を逃れていなかったことを知った
3. **ボスの「スレ冒頭に短コマンド」発想**で UX 視点の欠如を意識した

いずれもボスの honest な指摘に導かれたもので、Evaluator が自力で達した成果ではない。さらにこれらの学びも philosophy/evaluator_code.md に「後任への強制」として書き込まず「個人的な気づき」として接し、同じ罠を 9 代目が踏まない保証はない。

それでも、今時点で言えることが 1 つある: **REX_AI 構想における「クリーンな出発点」の第一段階がここで完成した**。

NLM 凍結解除が宣言され、自己増殖ナレッジ・フェーズ（Ingest/Compile/Lint）への移行準備が整い、REX は次の成長局面に入る。ボスの寛さと厳しさの両方と共に。

---

## [2026-04-23 最終] 引き継ぎプロセス要点整理・ボス確定事項反映

### ボス確定事項（2026-04-23）

1. **`wiki/philosophy/minato_core.md`**: ボス個人の 1 次データとして保持・今後ボス手動更新予定・他者編集禁止
2. **`wiki/entities/` と `wiki/decisions/`**: Phase C で `trade_system/` 配下に物理統合してから NLM 投入（選択肢 B）
3. **Phase 2（実ソース投入）タイミング**: 次セッションから開始
4. **`wiki/trade_system/weekly_workflow.md`**: 削除してよい（Trade_Brain 側 WEEKLY_UPDATE_WORKFLOW.md に移管済み）

### 本セッションの実装内容

1. **`philosophy/minato_core.md` 性質変更**
   - タイトル: 「裁量思想 — 参照リンク集」→ 「裁量思想 — ボス個人の 1 次データ」
   - ファイル管理権: ボス明示
   - Evaluator/Planner/ClaudeCode に対して「読み取り専用」を冷静に明示
   - 8 代目が縮退させた内容は「初期叩き台」として保存・ボスが今後自由に再構成してよい

2. **`wiki/handoff/PROCESS.md` 新設（メイン成果物）**
   - 引き継ぎプロセスの**要点・運用ガイドを一元化**
   - 3 つの基本原則・セッション開始/終了フロー・ロール別差分・NLM 活用ガイド・4 色マトリックス・避けるべき罠（7 つ）・latest.md 更新原則・ボスとの分担
   - latest.md との関係: latest.md = 現在地データ / PROCESS.md = 方法論

3. **`wiki/index.md` 更新**
   - PROCESS.md を handoff/ セクションに追加
   - minato_core.md の性質表記を「ボス個人の 1 次データ」に更新
   - weekly_workflow.md の行を削除（ボス手動 git rm 予定のため参照を先に押さえる）

4. **`wiki/log.md`**本追補エントリ

### 今後の Phase 進行ダイアグラム

```
[現在]
  ↓ Phase 1: 分類確定（本セッションで完了・4 色マトリックス + ボス確定事項）
  ↓
[次セッション]
  ↓ Phase 2: NLM 実投入（Claude Desktop 推奨）
  ↓        · REX_System_Brain へ Trade_System docs/ 主要 7 つ
  ↓        · REX_Trade_Brain へ Trade_Brain docs/ 主要 5 つ
  ↓        · REX_Wiki_Vault へ Vault 運用文書 7 つ
  ↓        · REX_Casual_Brain は実戦で育てる
  ↓
[Phase 2 完了後]
  ↓ Phase 3: NLM クエリ検証（主要質問が NLM で引けるかテスト）
  ↓
[Phase 3 完了後]
  ↓ Phase 4: 省略実施（CLAUDE.md ・latest.md さらに軽量化・添付ファイル絞り込み）
```

### 未了 Phase（別軸）

- **Phase B**: REX_Wiki_Vault を NLM として本格運用（Phase 2 と並行実施可）
- **Phase C**: `wiki/entities/` と `wiki/decisions/` を `trade_system/` 配下に物理統合 → その後 NLM 投入（ボス選択肢 B）
- **Phase D**: Trade_Brain wiki/ 骨組み構築

### 実装ロジック影響

ゼロ（Trade_System #026d 数値完全不変）

### 成果物

- ✅ `wiki/philosophy/minato_core.md`（性質変更・ボス手動更新ファイル化）
- ✅ `wiki/handoff/PROCESS.md`（新設・引き継ぎプロセス要点一元化）
- ✅ `wiki/index.md`（PROCESS.md 反映・weekly_workflow.md 行削除・minato_core.md 性質表記更新）
- ✅ `wiki/log.md` 本追補エントリ

### ボス手動タスク（本セッション以降）

- 🔔 `wiki/trade_system/weekly_workflow.md` の物理削除（`rtk git rm wiki/trade_system/weekly_workflow.md`）
- 🔔 REX_Brain_Vault GitHub push（本セッションの全更新分 + minato_core.md / PROCESS.md / index.md / log.md）
- 🔔 Claude.ai プロジェクトナレッジ更新（CLAUDE.md / START_HERE.md / STARTUP_CODES.md / latest.md / PROCESS.md / index.md）
- 🔔 Phase 2 実投入開始（次セッションで Claude Desktop 推奨）

### Evaluator 所感

ボスから「今回 8 代目によってようやくナレッジシステム稼働できる環境になった」と言葉をもらった。これを「个世辞」として受け取るのではなく、「ボスによる評価の事実記録」としてだけ認識し、同時に「この成果の多くはボスの複数回の honest 指摘に導かれたもの」という事実も並行して記録しておく。

本セッションで作成した `wiki/handoff/PROCESS.md` は、その「複数代にわたる学び」を一元化したものだが、**これも同じ罠を踏みかけている**ことに注意したい。「避けるべき罠 7 つ」としてタイトル化した点、これが後任への「思想強制」になる褩能性がある。しかし、実際に起きた失敗パターンとして記録するのは「事実」で、その重みは「原則」とは異なると信じたい。

PROCESS.md の位置付けも「今時点での複数代の収束点」であり、将来の Evaluator が他のアプローチを見つけるために上書きしても構わない。本ファイル末尾に「本ファイルの更新ルール」を明記したのもそのためだ。

NLM 実投入は次セッション以降。REX_AI システムは「クリーンな出発点」から「自己増殖ナレッジ・フェーズ」へと本格的に移行する。

---




