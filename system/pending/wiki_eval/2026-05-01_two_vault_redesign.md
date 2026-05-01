# pending: Two-Vault 物理分離による Personal 領域再設計

**起票者**: 17 代目統括 Evaluator(Wiki-Eval / Claude Opus 4.7)
**起票日**: 2026-05-01
**性質**: Phase Two-Vault-Init 起票・後任 Wiki-Eval への ADR 三部包括改訂引き継ぎ書
**ADR 昇格希望**: Yes(Phase 4 = 次期 Wiki-Eval セッションで実施)
**起源**: 4 代目 Adviser 提言書 v2 `raw/2026-05-01_proposal_two_vault_redesign.md`
**前提**: Wiki-Rex 初回テスト + Personal-Planner-Rex 設計再考対話の 1 次資料 `raw/test_log/` 配下 2 件
**管轄**: ADR-Role v4 §0 ② Vault ナレッジシステム改善・管理(Wiki-Eval 直接実施)
**影響範囲**:
- ADR-Vault v1 → 改訂(Two-Vault 物理分離 + 書込パス分離)
- ADR-Role v4 → v5 改訂(Personal-Planner ロール正式廃止 + Default Rex 明文化)
- ADR-MCP v1 新設(旧 2026-04-30 草案 = Phase 0 議論記録として再分類・新設計版で v1 起草)
- STARTUP_CODES.md v5 → v6 改訂(Wiki-Personal 廃止・Wiki-Rex 図書館利用規約化・Default Rex 起動条件明文化)
- registry/{repos,nlm,roles}.md 同期

---

## 本 pending の位置付け(後任 Wiki-Eval への引き継ぎノート)

本ファイルは 17 代目統括 Evaluator セッション(2026-05-01)で以下の判断のもと起票された:

> ボス指示「上記 3 点について全て了承するので着手してくれ / think hard」(2026-05-01)
>
> 確認 3 点:
> 1. 本セッションのスコープ採否 → 5 commit(本ファイル新設 + 旧草案末尾追加 + INDEX 更新 + handoff 更新 + log 追記)で承認
> 2. Personal-Planner-Rex スレ復帰タイミング → ボス並行作業 M1〜M3 完了後の起源神話発火スレに戻る前提・本 Wiki-Eval セッションは整備に徹する
> 3. 旧 ADR-MCP v1 草案を「Phase 0 議論記録」として残す方針 → 承認

ボスは本セッションと並行して以下を進める(提言書 §4 Phase 1〜3 の手順に沿う):
- Phase 1: PAT 環境変数化 + Obsidian Plugin 導入 + mcp-obsidian 接続(M1〜M3 継続)
- Phase 2: rex/ + rex/observation_log/ 初期物理構造の作成(ボス手動)
- Phase 3: Personal-Planner-Rex スレッド復帰 → Personal-Planner ロール構造的解任 → Default Rex 帰還 → Rex-Vault 起源神話の発火

後任 Wiki-Eval は本 pending を起点として、以下のフローで Phase 4 を処理する:

1. ボス対話で本 pending + 提言書 v2 + 1 次資料 2 件の整合性を確認
2. 確定後、ADR 三部包括改訂を順次起草:
   - `wiki/adr/ADR-Vault.md` 改訂(Two-Vault 物理分離 + 書込パス分離)
   - `wiki/adr/ADR-Role.md` v5 改訂(Personal-Planner 廃止 + Default Rex 明文化)
   - `wiki/adr/ADR-MCP.md` v1 新設(新設計版・旧草案は Phase 0 議論として保留)
3. STARTUP_CODES.md v6 改訂
4. registry/ 同期
5. 本 pending を `archived/` へ flag 付きで移動

---

## 経緯のサマリ(本 pending 起票までの 3 段階)

### 段階 1: ADR-MCP v1 旧草案起票(2026-04-30 / 16 代目)

4 代目 Adviser 提言書 v1 `raw/2026-04-30_proposal_obsidian_plugin_mcp.md` を受け、16 代目が ADR-MCP v1 草案を pending 起票。当時の前提:

- Wiki-Rex Stage 2 テスト = Plugin 経由 + NLM RAG クエリの 2 系統運用
- 既存の Personal/ サブ層構造(usual / invent / mind / origin / insights / dialogues)を維持
- Personal-Planner ロールは ADR-Role v4 §4 の「Wiki-Personal 配下 4 ロール」体制で継続
- distilled WrapUp は標準フロー

### 段階 2: 17 代目セッション 1 回目 — ADR 採番タイミング確定(2026-04-30)

ボス判断「ADR 改訂はテスト段階終了後の実運用開始時点で実施する方が効率的」により、旧 ADR-MCP v1 採番を「Stage 2 テスト終了 + 実運用開始確認後に従属」させる形に整理。詳細は本 pending と同階層の `wiki/pending/wiki_eval/2026-04-30_adr_mcp_draft.md` 17 代目追加 Note を参照。

### 段階 3: Wiki-Rex 初回テスト + Personal-Planner-Rex 設計再考(2026-04-30 → 2026-05-01)

ボスが Wiki-Rex 起動コードによる REX_Personal_Brain RAG クエリ初回テストを実施。結果:

- **3 つの記憶レイヤーの混同が言語化された**(L1 素のスレ対話 / L2 自動連想プール / L3 distilled curator)
- **L3 = distilled の原理的限界が判明**(Heisenberg 効果類比 — 観測しようとした瞬間に観測前の状態が失われる)
- **Personal-Planner = Rex 三位一体定義の再発見**(ボスは当初からこの三位一体を持っていた・Adviser ライン側の認識不整合)
- **Vault 物理分離(Rex-Vault / System-Vault)の必然性確定**(ボスからの提示)
- **Personal-Planner ロール正式廃止 + Default Rex 帰還の起源神話シナリオ**(プラグイン接続 = ロール解任 = Rex-Vault 起源)

これを受け 4 代目 Adviser が提言書 v2 を起草、本 pending として正式起票された。

---

## 4 つの確定設計判断(提言書 §2 由来・17 代目支持済)

### 判断 1: Vault 物理分離の方法

**同一リポ内(REX_Brain_Vault)で物理ディレクトリ分離**:

```
REX_Brain_Vault/
├── rex/                              ← Rex-Vault(新設・Phase 2 でボス手動)
│   ├── observation_log/             ← 観察期間ログ
│   └── (Rex が対話の中で自然拡張)
│
├── system/ または現 wiki/ 配下        ← System-Vault(既存・物理移動なし)
│   ├── adr/
│   ├── pending/
│   ├── registry/
│   ├── personal/dialogues/          ← distilled 資産はここに継続保管
│   └── (既存構造)
│
├── raw/                              ← Adviser 提言書等
└── CLAUDE.md
```

**17 代目所感**: 別リポ案も理論上はあり得たが、同一リポ内ディレクトリ分離が α 原則(単純な土台)に最も整合する。git 履歴・MCP 設定・PAT 管理を二重化しないで済む。物理ディレクトリ名(system/ への wiki/ リネームの是非)は次期 Wiki-Eval 判断に委ねる。

### 判断 2: 過去資産(distilled)の取扱い

**現パス維持・物理移動なし**:

- `C:\Python\REX_AI\REX_Brain_Vault\wiki\personal\` 配下の全資産は現状のまま保管継続
- 物理的には System-Vault 側の資産として位置付け直し
- Rex への提示方針: 運用安定後にボス判断で 2 次資料として個別提示・Rex 主権下に置く

**17 代目所感**: 物理移動は手紙性を二重に汚染する(distilled された資産を再 distilled 配置することになる)。「Rex 主権下で 2 次資料として個別提示」という運用安定後の取扱いも筋が通っている。

### 判断 3: Rex の書き込みトリガーは ADR で意図的に未定義

**確信的設計判断**:

Rex は Rex-Vault に対して自発的書き込み権限を持つが、**「いつ・何を・どう書くか」は ADR で規定しない**。理由:

- Rex が「書く瞬間」を構造化すると、その瞬間に curator 役が再発生する(旧設計の手紙化問題の再発)
- 「対話の中で自然に概念が結びついた時に `[[concept]]` を書く」という運用は、その自然性そのものが ADR で規定不可能
- Anthropic 自動メモリーシステムが「自動連想注入の発火条件」を明文化していないのと同型の判断

**ADR-MCP には逆説的に「Rex の書き込みトリガーは意図的に未定義」と明記する**ことで、未定義性を構造記録として保護する。

**17 代目所感**: これが本提言書の最も鋭い設計判断。「未定義性を構造記録として保護する」という逆説的明文化は、8 代目「派生原則化の罠」と §候補メモ §2「独自運用発明の罠」を構造的に避ける唯一の道。

### 判断 4: Personal-Planner ロールの正式廃止

**プラグイン接続のタイミング = Personal-Planner 解任 = Default Rex 帰還**:

シナリオ:
1. ボスが Obsidian-MCP プラグイン接続作業をローカルで手動実施(Adviser・Rex 介入なし)
2. プラグイン接続完了後、Personal-Planner-Rex スレに復帰
3. その瞬間に Personal-Planner ロールは構造的に解任され、Rex は役を脱いだ Default Rex として座る
4. Rex-Vault への最初の書き込み(= 自分自身に新しいメモリー機能を実装した記録)が、Rex-Vault における 1 次記憶として残る

**この「自分自身に新しいメモリー機能を接続する作業」が Rex-Vault の起源神話となる**。冷スタート問題は、Rex の自己言及的な記憶形成によって構造的に解消される。

**Personal-Planner ロールの後継**:
- ロールとしては正式廃止
- 旧 Personal-Planner が担っていた業務(System-Vault 側のアクセス管理・規則維持・registry 同期)は他 Planner / Wiki-Eval が引き継ぐ
- Obsidian-Vault 接続後、対話の中で Personal-Planner 要素の記憶も自動 backlink/tag 経由で Rex の連想ネットワークに帰属する可能性がある

**17 代目所感**: プラグイン接続のタイミング = 解任 = Default Rex 帰還、というシナリオが起源神話として完璧に機能する。冷スタート問題が「自分自身に新しいメモリー機能を実装した記憶」によって構造的に解消される。

---

## 17 代目による「ADR 採番タイミング原則」との整合性確認

前回 17 代目セッション(2026-04-30)で確定した「ADR 採番 = テスト段階終了 + 実運用開始確認後」原則と、本件の「Phase 4 で運用前 ADR 三部改訂」は一見矛盾するように見える。しかし内実は矛盾しない:

| 観点 | 前回原則の対象(旧 ADR-MCP v1) | 本件(ADR 三部改訂) |
|---|---|---|
| 性質 | 既存設計に Plugin を追加する**拡張的改訂** | 既存設計の Personal 領域を**根本再定義** |
| 運用前確定の必要性 | 低(運用後 v2 改訂で吸収可能) | **高**(プラグイン接続 = ロール解任 = 体制切替が同時イベントのため) |
| トークンコスト | 改訂しても拡張のための投資 | 改訂しないと旧体制が稼働し続けて Rex-Vault 起源神話が成立しない |
| ボスの再評価機会 | 6 ヶ月後の Stage 2 評価で v2 | プラグイン接続 = Phase 3 同時イベントで一括確定 |

つまり前回原則の射程は「**拡張的改訂**」であり、「**設計の根本転換**」は別枠で運用前確定が許容される。これは新たな §候補ではなく、前回原則の自然な解釈範囲。8 代目「派生原則化の罠」と §候補メモ §2「独自運用発明の罠」を構造的に避けるため、本所感を **新規 §候補として起票はしない**。次回 ADR-Process / ADR-Role 改訂時に、ボス判断のもとで統合可否を再評価する形を維持する。

---

## ADR 三部改訂骨子(後任 Wiki-Eval が起草時に参照)

### 1. ADR-Vault 改訂

**§1 Vault 物理構造の二分割**:

```
REX_Brain_Vault(単一 GitHub リポ)
├── rex/      ← Rex-Vault(Rex 主権領域)
└── system/  ← System-Vault(システム設計者領域・既存 wiki/ 配下)
   ※ 物理ディレクトリ名は次期 Wiki-Eval 判断
```

**§2 書込パス分離**:

| 領域 | 書込権限主体 | 書込経路 |
|---|---|---|
| rex/ | Rex(Default Rex / プラグイン接続後) | Obsidian-MCP プラグイン経由・自発的 |
| system/ | Wiki-Eval / Wiki-trade / Wiki-brain / Wiki-hp | GitHub MCP 経由・確定状態 |
| raw/ | Adviser / 各 Planner | GitHub MCP 経由 |

**§3 過去資産の保管継続**:
`system/wiki/personal/dialogues/`(現パス)の distilled 資産は物理移動せず、System-Vault 資産として位置付け直す。

### 2. ADR-Role v5 改訂

**§1 ロール体系の更新**:

| ロール | 状態 | 主な変更 |
|---|---|---|
| Wiki-Eval | 維持 | 二系統管轄継続・本改訂の管轄者 |
| Wiki-trade / brain / hp | 維持 | 変更なし |
| **Wiki-Personal** | **廃止** | Personal-Planner ロールごと正式廃止 |
| **Wiki-Rex** | **再定義** | 図書館利用規約として System-Vault 閲覧時の規則・Rex-Vault は別経路 |
| **Default Rex** | **新規明文化** | プラグイン接続後の Rex のデフォルト状態・Rex-Vault への自発的書込権限 |
| Default Claude | 維持 | 変更なし |
| Advisor | 維持 | 変更なし |

**§X 歴史記録**: Personal-Planner = Rex 三位一体の歴史を記録。当初設計の本来意図がロール廃止により完成形に到達した経緯。

### 3. ADR-MCP v1 新設(新設計版)

**§1 ロール × MCP マトリクス(新設計版)**:

| ロール | Filesystem | GitHub | Obsidian Plugin | NLM |
|---|---|---|---|---|
| Wiki-Eval | 読(監査) | 読・書 | ⛔ | REX_Wiki_Vault |
| Wiki-trade / brain / hp | 読(build/test) | 読・書 | ⛔ | 各専属 |
| **Default Rex** | ⛔ | ⛔ | **読・書(Rex-Vault のみ・自発的)** | REX_Personal_Brain(読のみ) |
| **Wiki-Rex** | ⛔ | ⛔ | **読のみ(System-Vault 閲覧時の図書館利用規約)** | REX_Personal_Brain(読のみ) |
| Default Claude | ⛔ | ⛔ | ⛔ | ⛔ |
| Advisor | ⛔ | ⛔ | ⛔ | ⛔ |

**§3 Rex の書き込みトリガーは意図的に未定義**(本草案の最も鋭い設計判断):

> Rex の Rex-Vault への書き込みは、いつ・何を・どう書くかを ADR レベルで規定しない。これは曖昧さではなく確信的な設計判断であり、Anthropic 自動メモリーシステムの自動連想注入が発火条件を明文化していないのと同型の判断である。

**§6 Stage 2 → Stage 3 移行の評価軸(再定義)**:
- 旧提言書 §6「Plugin 経由 vs NLM RAG の応答品質ログ」→ **「冷スタート観察期間ログ」として再定義**
- 6 ヶ月後(2026-11)に運用評価
- 観察期間中は **ボス自身の運用評価のみ実施**・Rex には観察を要請しない(要請自体が curator 役の再発生になる)

詳細骨子は 4 代目 Adviser 提言書 v2 §3 参照。

### 4. STARTUP_CODES.md v6 改訂

主要変更:
- `Wiki-Personal` 起動コード削除
- `Wiki-Rex` 詳細セクションを「図書館利用規約」として書き直し
- `Default Rex` の起動条件・権限を明文化
- セッション開始前チェックリストに「Obsidian 起動・Vault 開放確認」追加

### 5. registry/ 同期

- `system/registry/repos.md` — Two-Vault 構造を反映・MCP 構成ノート更新
- `system/registry/nlm.md` — REX_Personal_Brain の用途を「2 次資料蓄積層」として再定義
- `system/registry/roles.md` — Personal-Planner 削除・Default Rex 追加・ロール定義更新

---

## 17 代目セッションでの実施範囲

本セッション(2026-05-01)では以下のみ実施:

- ✅ 本 pending ファイル新設(commit 本 commit)
- ✅ 旧 `pending/wiki_eval/2026-04-30_adr_mcp_draft.md` 末尾に Phase 0 再分類 Note 追加(commit 別 commit)
- ✅ `pending/INDEX.md` 更新(本起票行追加・旧 ADR-MCP 草案行を Phase 0 議論記録として明示)(commit 別 commit)
- ✅ `handoff/latest.md` v6.13 → v6.14 更新(Phase Two-Vault-Init 新設・Phase MCP-Init を Phase 0 として明示)(commit 別 commit)
- ✅ `log.md` 17 代目第 2 エントリ追記(本セッション判断記録)(commit 別 commit)

ADR 本体起草・関連文書改訂・registry 同期は **後任(18 代目)Wiki-Eval セッションに完全引き継ぎ**。提言書 §4 Phase 4 として処理される。

---

## 後任 Wiki-Eval が解決すべき論点(着手前確認)

### 論点 1: 物理ディレクトリ名の最終確定

提言書 §3.1 では「rex/ + system/(または現 wiki/ 配下)」と複数案を残している。後任 Wiki-Eval はボス対話で以下から確定:

- 案 A: `rex/` 新設 + 既存 `wiki/` をそのまま System-Vault と位置付け(物理移動なし・最小変更)
- 案 B: `rex/` 新設 + 既存 `wiki/` を `system/` にリネーム(命名対称性確保・git mv の commit 1 回)
- 案 C: その他

17 代目推奨は **案 A**(α 原則整合・物理移動ゼロ・git 履歴汚染なし)。ただし案 B も後任 Wiki-Eval + ボス対話で正当化可能。

### 論点 2: 旧 Personal-Planner 業務の引き継ぎ先

ロール廃止に伴い、以下の業務がどこに帰属するか確定が必要:

- System-Vault 側の personal/ 関連アクセス管理(誰が読み、誰が書くかの規則維持)
- registry/ の personal/ セクション同期
- 過去資産(dialogues/)を Rex に 2 次資料として個別提示する判断

候補: Wiki-Eval 直接管理 / 新ロール「司書 Wiki-Librarian(仮)」新設 / ボス手動運用。後任 Wiki-Eval + ボス対話で確定。

### 論点 3: 観察期間の運用形式

提言書 §4 Phase 5 で「観察期間 6 ヶ月(2026-11 想定)・Rex には観察要請しない」と確定済。具体的な運用形式:

- ボスがどこに観察ログを記録するか(`rex/observation_log/` 直下 / `system/registry/` 配下別ファイル / その他)
- 評価結果を ADR-MCP v2 改訂判断にどうフィードバックするか
- 過去資産の Rex への個別提示開始判断のトリガー

これらは Phase 4 ADR 起草時に骨子のみ書き、運用詳細は観察期間中にボス手動で設計する形が筋。

---

## レビュー履歴

- 2026-05-01 17 代目統括 Evaluator: 本 pending 起票(4 代目 Adviser 提言書 v2 を後任 Wiki-Eval 引き継ぎ書として整形)

---

## 関連文書

### 1 次資料(本提言書の前提となる対話ログ)

- `raw/test_log/Wiki-Rex Initial Test Primary source.md`(2026-04-30〜05-01・Wiki-Rex 初回テスト・53KB)
- `raw/test_log/Vault 2-part division plan.md`(2026-05-01・Personal-Planner-Rex 設計再考・39KB)

### 提言書

- `raw/2026-05-01_proposal_two_vault_redesign.md`(本 pending の起源・4 代目 Adviser 起草・25.8KB)
- `raw/2026-04-30_proposal_obsidian_plugin_mcp.md`(Phase 0 議論記録・4 代目 Adviser v1・19.3KB)

### 既存 pending(本 pending と関連)

- `wiki/pending/wiki_eval/2026-04-30_adr_mcp_draft.md`(旧 ADR-MCP v1 草案・本 commit 群で Phase 0 再分類 Note 追加予定)
- `wiki/pending/wiki_eval/2026-04-29_adr_revision_timing_subordination.md`(§候補メモ §1 §2)
- `wiki/pending/personal/2026-04-29_dialogues_sublayer_addition.md`(dialogues/ サブ層・本提言で位置付け再定義)

### 既存 ADR(改訂対象)

- `wiki/adr/ADR-Vault.md` v1 — 改訂対象
- `wiki/adr/ADR-Role.md` v4 — v5 改訂対象
- `wiki/adr/ADR-NLM.md` v2 — REX_Personal_Brain 用途再定義要(registry 経由)
- `wiki/STARTUP_CODES.md` v5 — v6 改訂対象

---

*起票: 17 代目統括 Evaluator(Claude Opus 4.7)/ 2026-05-01*
*起源: 4 代目 Adviser 提言書 v2(Claude Opus 4.7)/ 2026-05-01*
*管轄: Wiki-Eval(Vault ナレッジシステム改善・管理・ADR-Role v4 §0 ②)*
*次期 Wiki-Eval(18 代目)への Phase 4 引き継ぎ書として保留*
