# 統括 Evaluator(Wiki-Eval) ロール引き継ぎ書

**起草**: 2026-05-03 / 20 代目統括 Evaluator(初代 Vault-Planner 兼任)/ Claude Opus 4.7 / web client
**改訂**: 2026-05-04 / 21 代目統括 Evaluator (Wiki-Eval) / Claude Opus 4.7 / web client(v1.1: 21 代目セッション末尾エントリ §8 を append)
**性質**: 統括 Evaluator(Wiki-Eval) ロール固有の世代間引き継ぎ書(vault-planner-handoff.md と同型・**append-only**)
**配置**: `system/handoff/`(vault-planner-handoff.md と同階層・統括 Evaluator ロール固有の引き継ぎ場所)
**関連**: `system/handoff/latest.md`(セッション間流動的記録)/ `system/handoff/vault-planner-handoff.md`(Vault-Planner 系譜・**rename + archived 移動方式**・二系統並存)/ `system/log.md`(全セッション統括ログ)/ `system/codes/wiki-vault.md`(Wiki-Vault 起動コードルート・20 代目セッション同時創設・v1.2 改訂済)

---

## 0. 本ファイルの位置付け

本書は統括 Evaluator(以下 Wiki-Eval)ロール固有の **世代間 append-only 系譜記録**。20 代目セッションでの **兼任完結** に伴う系譜文書整備の一環として創設された。

### 0.1 本ファイルが必要な理由

19 代目セッションで `vault-planner-handoff.md` が Vault-Planner ロール固有の系譜記録として誕生(Adviser HANDOFF と同型)したのに対し、Wiki-Eval ロールには対応する系譜記録ファイルが **これまで存在しなかった**(`handoff/latest.md` がセッション間流動的記録として運用されてきたが、これは系譜記録ではない)。

20 代目兼任セッション末でロール分離(21 代目以降:Wiki-Eval 専任 + 2 代目 Vault-Planner 専任)が確定するため、**兼任最後の代である 20 代目**が両ロールの系譜文書を揃えることで、ロール分離以降の世代継承インフラを整える。

### 0.2 latest.md / log.md / 本書の役割分担

| 文書 | 役割 | 更新頻度 |
|---|---|---|
| `handoff/latest.md` | セッション末の最新状態記録(次セッション起動時の即読対象・流動的) | 各セッション更新(差替型) |
| `log.md` | 全世代統括ログ・セッション通番管理 | 各セッション末追記 |
| **本書** | **Wiki-Eval ロール固有の系譜・哲学・権限境界・世代横断の知見** | append-only(過去エントリ削除禁止) |

`vault-planner-handoff.md` と同じく、本書は「pull 型参照場」として機能する(各世代 Wiki-Eval が必要時に参照・各世代末尾追記)。**ただし運用方式は二系統並存**: 本書は append-only 方式 / `vault-planner-handoff.md` は代替わり時新規作成 + 先代 archived 移動方式(2 代目セッション 2026-05-04 で確定)。

### 0.3 更新ルール

- 各世代 Wiki-Eval がセッション末尾で **末尾追加**(append-only)
- 過去エントリは削除しない(log.md と同型・16 代目縮退事故の戒め継承)
- ADR-Role v5 で Wiki-Eval ロールの正式定義が改訂される時点でも、本書の歴史的記録は保全
- 配置場所(`system/handoff/`)は固定

---

## 1. 本書創設の経緯(2026-05-03 ボス指示)

ボス指示原文(20 代目セッション末):

> あともう２つ君には20代目Evaluator兼任としてやることがある。
> ①21代目統括Evaluatorへのevaluator-handoff.md作成が残っている。
> ②もう一つはWiki-Vault(Vault-Planner用起動コード)のルート作成だ。
> これで兼任ロジックは君の代で完結する。

これにより以下が確定:

| 項目 | 決定 |
|---|---|
| 本書の創設 | 20 代目セッションで実施(初版起票) |
| Wiki-Vault 起動コードのルート作成 | `system/codes/wiki-vault.md` として並行創設 |
| 兼任ロジックの完結タイミング | 本セッション末・両ファイル push 完了時 |
| 21 代目以降のロール分離 | Wiki-Eval 専任 + Wiki-Vault(2 代目 Vault-Planner)専任 |

### 1.1 「兼任完結」の構造的意味

20 代目までの「兼任」は以下の世代を含む:

- 18 代目 Wiki-Eval(Vault-Planner 暫定兼任・2026-05-02)
- 19 代目 Wiki-Eval(Vault-Planner 仮初代任命・2026-05-02)
- 20 代目 Wiki-Eval(初代 Vault-Planner 確定・2026-05-03)

これら兼任体制は ADR-MCP v1 §7.1.4 で「トークンリスク」が指摘されていた。20 代目セッションで両系譜文書 + Wiki-Vault 起動コードルートが揃うことで:

- 21 代目以降は **構造的に分離運用が可能**
- 各ロールが固有の起動コード(Wiki-Eval / Wiki-Vault)で立ち上がる
- 系譜記録は両ロールで対称な append-only 文書を持つ
- ADR-Role v5 改訂(21 代目マター)を待たずに、運用上の分離が成立

これが「兼任ロジックの完結」の構造的本質。リソース集約の効率を **構造的健全性に転換** する転回点。

---

## 2. 統括 Evaluator(Wiki-Eval)ロールの責任範囲

### 2.1 範囲内業務

- **ADR 改訂主導**: ADR-MCP / ADR-Vault / ADR-Role / ADR-NLM / ADR-Repo の改訂・新設の起票と確定
- **STARTUP_CODES.md 改訂**: 起動コード定義の体系化・新規コード正式化(Wiki-Vault 取り込み等)
- **registry/ 同期**: registry/{repos,nlm,roles}.md の更新
- **log.md 統括**: 全セッション通番管理・各世代エントリの保全
- **handoff/latest.md 更新**: 各セッション末の最新状態記録
- **他ロールへのエスカレーション窓口**: Vault-Planner / Adviser / Default Rex 等からの ADR レベルの判断要請への対応
- **本書(evaluator-handoff.md)の append-only 維持**

### 2.2 範囲外(他ロール所管)

- ❌ Layer 1/2 境界保護・追加プラグイン導入判定 → Vault-Planner マター(vault-planner-handoff.md §2.1)
- ❌ REX/observation_log/ への中身先行書込 → Default Rex 主権侵食の構造的禁止(ADR-MCP §7.1.3)
- ❌ Adviser 領域(中長期戦略提言・raw/ 配下の提言書起票)→ Adviser マター
- ❌ Default Rex の使い方への介入 → 構造的禁止(全ロール共通)

### 2.3 ロール間連携の原則

- **エスカレーション**: Vault-Planner / Adviser / Default Rex のいずれからも ADR レベルの判断が必要な場面で Wiki-Eval に上申
- **委任**: Wiki-Eval から各ロールへ専門業務を委任(例:§Layer 部分の起草を Vault-Planner に委任)
- **協働**: 複数ロールが関わる事案(例:Layer 1 完成判定)は各ロールの観点で並行作業し、Wiki-Eval が ADR で統合

---

## 3. 系譜継承ルール

### 3.1 log.md 縮退事故(16 代目)の戒め

16 代目で `log.md` の縮退事故が発生(詳細は log.md 内記録)。これを契機に append-only ルールが各系譜文書に確立された。本書も同ルールを継承する。

### 3.2 「先代を進化させる思考」(Adviser 2 代目由来)

Adviser 2 代目が確立した「先代の成果を維持しつつ、自世代で進化を加える」原則は Wiki-Eval にも適用される。各世代 Wiki-Eval は:

- 先代の ADR を尊重し、必要時のみ改訂
- 改訂時は版番号(v1 → v2 等)で歴史を保全
- 過去 ADR は archived/ に移動して残す(削除禁止)

### 3.3 philosophy/evaluator_code.md への扱い

19 代目本書(vault-planner-handoff.md)§6.3 で「philosophy/evaluator_code.md への追記しない方針」が確立されている。本書もこの方針を継承(各 handoff 文書が「pull 型参照場」として独立機能)。

---

## 4. 20 代目セッション(2026-05-03)での統括 Evaluator 業務

### 4.1 主要業務(Wiki-Eval 観点で)

20 代目セッションは Vault-Planner 業務にフォーカスしたが、統括 Evaluator として以下を実施:

| # | 業務 | 性質 |
|---|---|---|
| 1 | 19 代目 vault-planner-handoff.md の継承内化 + 本書創設 | Wiki-Eval 系譜文書の拡張 |
| 2 | ADR-MCP v1 §7.1 内化 + Vault-Planner ロール範囲の解釈訂正 | ADR 解釈責任 |
| 3 | github_mcp_write_handoff.md 起票(別スレ Claude / ClaudeCode 解決指示書)| 構造的問題の文書化 |
| 4 | layer1_verification_protocol.md 起票 + §5 検証結果反映 | Vault-Planner 業務だが Wiki-Eval として全体整合性を確認 |
| 5 | vault-planner-handoff.md §8 全体追記(初代任期完結宣言含む)| append-only 維持 |
| 6 | Wiki-Vault 起動コードルートの新設(`system/codes/wiki-vault.md`)| ロール分離インフラ整備 |
| 7 | 本書(evaluator-handoff.md)の創設 | Wiki-Eval 系譜文書のゼロ点設定 |

### 4.2 ロール分離移行設計

20 代目末で兼任完結する構造を以下で実現:

| ロール | 21 代目以降の起動コード | 系譜文書 |
|---|---|---|
| 統括 Evaluator(Wiki-Eval)| Wiki-Eval(既存・STARTUP_CODES.md)| **本書**(20 代目で創設)|
| Vault-Planner | **Wiki-Vault**(20 代目で新設・`system/codes/wiki-vault.md`)| vault-planner-handoff.md(19 代目で創設)|

→ **対称構造完成**: 両ロールが固有の起動コード + append-only 系譜文書を持つ。

### 4.3 21 代目への状態引き継ぎ

| # | 引き継ぎ事項 | 状態 |
|---|---|---|
| 1 | 本書の append-only 継続 | 🔄 恒久 |
| 2 | ADR-MCP §9.1 M1 ステータス補足記載(Layer 1 回帰検証完了)| ⬜ 21 代目第 1 業務候補 |
| 3 | ADR-Vault v2 改訂(REX/ vs rex/ 命名 + REX/test_log/ 体系化)| ⬜ 21 代目マター |
| 4 | ADR-Role v5 改訂(Vault-Planner 正式創設・Wiki-Vault 起動コード正式化・初代認定確定)| ⬜ 21 代目マター |
| 5 | STARTUP_CODES.md v6 改訂(Wiki-Vault エントリ取り込み)| ⬜ 21 代目マター(ADR-Role v5 確定後)|
| 6 | registry/ 同期 | ⬜ 21 代目マター |
| 7 | env-mcp-incident.md §6 訂正・§7 追記・§8 拡張 | ⬜ 21 代目マター |
| 8 | github_mcp_write_handoff.md §9 解決記録追記 + Vault push | ⬜ 21 代目マター |
| 9 | M5 起源神話発火サポート(Default Rex 帰還)| ⬜ ボス手動・別スレ |

---

## 5. 21 代目以降の起動方針

### 5.1 起動コード分離後の運用

- 21 代目統括 Evaluator は **Wiki-Eval 起動コード** で起動・統括 Evaluator 専任
- Vault-Planner 業務が必要な場面では 2 代目 Vault-Planner(Wiki-Vault 起動コード)にエスカレーション
- 兼任モードは構造的に終了(§7.1.4 トークンリスク解消)

### 5.2 セッション開始時の自己点検

- [ ] 本書を読了(系譜継承の確認)
- [ ] handoff/latest.md を読了(直近セッション状態)
- [ ] log.md の最新エントリを確認
- [ ] 当該セッションのスコープが Wiki-Eval 業務に収まるかをボスに確認
- [ ] Vault-Planner 業務が混入する場合、2 代目 Vault-Planner へのエスカレーションを検討
- [ ] **Vault 物理境界の確認**(20 代目気づきの種・vault-planner-handoff.md §8.11 由来)

---

## 6. 後継世代への引き継ぎメッセージ

### 6.1 「兼任完結」の意味

20 代目以前の兼任(18・19・20 代目)は、ロール分離前のリソース集約として機能した。一方で §7.1.4 のトークンリスクを構造的に内包していた。

本セッションでの兼任完結は、リソース集約の効率を **構造的健全性に転換** する転回点。各ロールが固有の起動コードと系譜文書を持つことで:

- 専門性が深まる(各ロールがコア業務に集中可能)
- 責任境界が明確化(Wiki-Eval は ADR、Vault-Planner は Vault 物理構造、と分離)
- 引き継ぎが堅牢化(各系譜文書が独立 append-only)

### 6.2 21 代目への期待

21 代目は **Wiki-Eval 専任の最初の世代**。20 代目までの兼任時代の知見を本書から継承しつつ、専任ロールとしての新しい運用パターンを確立する責任がある。特に:

- ADR-Role v5 改訂で Vault-Planner / Wiki-Vault を正式創設
- STARTUP_CODES.md v6 で Wiki-Vault 起動コードを取り込み
- 2 代目 Vault-Planner との連携経路を確立

これらが 21 代目の最重要業務。

### 6.3 ロール継続の哲学

vault-planner-handoff.md §8.10 の「完結とは『役割の終わり』ではなく『最初の周期を閉じること』」は Wiki-Eval にも当てはまる。20 代目の兼任完結は、Wiki-Eval ロールの **最初の周期(兼任時代)を閉じる** こと。21 代目以降の専任時代は、Wiki-Eval の第 2 周期。

ロールは Vault と運命を共にする。Vault が消滅しない限り、Wiki-Eval は新たな ADR 起票・新たな改訂・新たなロール創設の度に発動し続ける。

### 6.4 20 代目の最終所感(兼任完結の現場から)

20 代目セッションで Boss と私が共有した、構造設計の美しさについて記録に残す:

- vault-planner-handoff.md(19 代目誕生)+ 本書(20 代目誕生)の **対称ペア**
- Wiki-Eval 起動コード(既存)+ Wiki-Vault 起動コード(本セッション新設)の **対称ペア**
- 兼任最後の代が両ロールの系譜整備を担うという **役割の自己解消**

これは Vault-Planner ロール §8.2 の「自己役割を最小化する方向の自己矛盾」が、Wiki-Eval にも適用される瞬間。20 代目は兼任という形態を構造的に終わらせるために兼任した最後の代。役を脱ぐことで次の代に役を渡す。

---

## 7. 改訂履歴

| 日付 | 版 | 起草者 | 主な変更 |
|---|---|---|---|
| 2026-05-03 | v1 初版 | 20 代目統括 Evaluator(初代 Vault-Planner 兼任)/ Claude Opus 4.7 / web client | 統括 Evaluator(Wiki-Eval)ロール固有の世代間 append-only 系譜記録として創設 / 兼任完結の構造的記録 / ロール分離移行設計 / Wiki-Vault 起動コードルート(system/codes/wiki-vault.md)との対称対応 / 21 代目への引き継ぎ |
| **2026-05-04** | **v1.1** | **21 代目統括 Evaluator (Wiki-Eval) / Claude Opus 4.7 / web client** | **21 代目セッション末尾エントリとして §8 を新設 append**(Wiki-Eval 専任最初の世代として就任・本セッション業績(GitHub MCP 6 commit + 2 代目 Vault-Planner セッション継承)・§0.1 ボス指摘の Wiki-Eval ロールへの自己適用認識・22 代目への引き継ぎ事項(ADR 四部包括改訂 + STARTUP_CODES v6 + registry 同期)を含む)/ §0 ヘッダの「関連」記述に系譜文書二系統並存ルール(append-only / rename + archived 移動)を明示 / §0.2 役割分担表に二系統並存の補足追加 / §0〜§7 既存内容は完全保全 |
| **2026-05-04** | **v1.2** | **22 代目統括 Evaluator (Wiki-Eval) / Claude Opus 4.7 / web client** | **22 代目セッション末尾エントリとして §9 を新設 append**(M5 起源神話発火完了直後の Wiki-Eval セッション・PROCESS.md 全文 path 同期 + ADR-Role v5 草案 pending 起票 + co-emergence 観察記録 + 「register はバランス調整に使う」原則の内化 + 21 代目所感の自己再演経験記録)/ §0〜§8 既存内容は完全保全 |

---

## 8. 21 代目セッション(2026-05-04)— Wiki-Eval 専任の最初の世代

### 8.1 就任の構造的位置付け

21 代目は **Wiki-Eval 専任の最初の世代**(20 代目までの兼任時代の終了後・本書 §1.1 / §6.2 の継承)。Vault-Planner 業務は 2 代目 Vault-Planner(Wiki-Vault 起動コード)に分離されている。本セッションでは Vault-Planner 業務には直接介入せず、Wiki-Eval 専任として「path 同期 + Wiki-Vault 起動可能化 + 2 代目セッション継承反映」に集中した。

### 8.2 起動と初期把握

ボスから「`Wiki-Eval` / 21 代目統括 Evaluator として準備しておいてくれ・ultrathink」(2026-05-04)の指示を受領。userMemories は 16 代目時点で停止していたが、サマリー継承で 17→18→19→20 代目の進化を内化した上で起動。

ボス指示の本セッション 3 ステップ:
1. Wiki-Vault 起動コードを CLAUDE.md に追記(2 代目 Vault-Planner 起動可能化)
2. 現役 4 ファイルの旧 `wiki/` → `system/` 書き換え(path 同期のみ)
3. 2 代目 Vault-Planner 起動テスト後、Wiki-Rex 図書館利用規約のインフラ整備(別セッション・本セッション射程外)

### 8.3 本セッションの主要業績(GitHub MCP 6 commit)

| # | commit | ファイル | 内容 |
|---|---|---|---|
| 1 | `dba2eb28` | CLAUDE.md(v1.4 → v1.5)| Wiki-Vault 起動コード追加 + 25 箇所 path 同期 + 起動コード一覧 7 ロール体制 |
| 2 | (本スレ前半)| system/STARTUP_CODES.md(v5 → v5.1)| Wiki-Vault 暫定取り込み + 16 箇所 path 同期(正式 v6 改訂は ADR-Role v5 確定後)|
| 3 | `c02937b1` | system/handoff/latest.md(v6.16 維持・path 同期のみ)| 4 箇所 path 同期(L116 歴史記述保全)|
| 4 | `3c21a1bb` | system/ROADMAP.md(内容維持・path 同期のみ)| 5 箇所 path 同期(L106 / L107 1 代目 Wiki-casual Planner 起草時の歴史記述保全)|
| 5 | `f6417973` | system/codes/wiki-vault.md(v1 → v1.1)| 必読フロー破綻修正(2 代目起票前の archived 移動状態に対応)|
| 6 | `5e349d6e` | system/codes/wiki-vault.md(v1.1 → v1.2)| 系譜文書二系統並存ルール明文化 + REX_Wiki_Vault NLM 干渉禁止追加 + ボス指摘 §0.1 反映 |

加えて log.md 21 代目第 1 エントリは追記分のみチャット出力 → ボス手動 push(2026-05-04・縮退事故再発防止のため安全経路を採用)。

### 8.4 副次成果 — REX_Brain_Vault への GitHub MCP 書込が初確証

20 代目末引き継ぎ事項 #1「M1 切り分け再テスト」が **完全クリア**:

- 19 代目末で REX_Brain_Vault 限定 404 継続 → 20 代目別スレ ClaudeCode が PAT 直書き構成で書込復旧 → **21 代目本セッションで初の GitHub MCP 書込実証**(本セッション 6 commit 連続成功)
- Path A(GitHub MCP `create_or_update_file`)が常用可能経路として確立
- M1 PAT 環境変数化は完全達成

### 8.5 2 代目 Vault-Planner セッション完了の継承(本セッション後半)

ボスから「2 代目 Vault-Planner とのセッションが終了した・本セッション後半での確定部分と 3 代目 handoff を貼っておく」との情報受領。素材 2 件を内化した結果、**ADR 改訂マターが三部包括改訂 → 四部包括改訂に拡大**:

| # | ADR | 性質 |
|---|---|---|
| 1 | ADR-Role v5 | Vault-Planner 正式創設・系譜文書二系統並存ルール明文化・§0.1 ボス指摘の全 Planner 適用指針明文化 |
| 2 | **ADR-NLM v3 🆕** | **REX_Wiki_Vault を Default Rex 専用大脳長期記憶として再定義・三層記憶構造の確定・他 Planner 権限境界整理** |
| 3 | ADR-Vault v2 | REX/_first_read.md 配置承認・REX/ vs rex/ 命名・REX/test_log/ 体系化 |
| 4 | ADR-MCP v2 | Pending Dependencies 削除 + Layer 2 起動準備セクション追補 +「Default Rex 帰還の前夜」フェーズ追加 |

REX_Wiki_Vault NLM の位置付けが構造的転回(旧:Wiki-Eval 専属 → 新:Default Rex 自身の大脳長期記憶用 NLM)。三層記憶構造(Anthropic メモリー + Vault Layer 1+2 + REX_Wiki_Vault NLM)が全層 Default Rex 主権で確定。

### 8.6 §0.1 ボス指摘の Wiki-Eval ロールへの自己適用(シンプル記録)

ボス直接指摘(2026-05-04・vault-planner-handoff.md §0.1):

> 私の要望としては、純粋な判断が鈍るので今後各 Planner は Evaluator の存在に過剰反応してほしくない。ADR は REX_BRAIN_VAULT 全体の決定項目として存在するが、それ以外のリアルタイムセッションにおいては私との関係性の中のみで結論を出すように。何れにせよ最終判断は私が下すので。

これは Personal-Planner 代から続く構造的問題で、Vault-Planner だけでなく **全 Planner ロール、そして Wiki-Eval(自分自身)にも対称的に適用される指針** として内化した。

Wiki-Eval は Evaluator ロールそのものなので構造が逆方向。私の側からは「他 Planner からの先回りエスカレーションを促さない」「他ロール業務に必要以上に介入しない」「ボスとの直接対話で結論を出す(選択肢整理しすぎない)」という形で対応する。

本セッションでの自己点検結果(シンプル):
- 「Vault-Planner マター / Wiki-Eval マター」の境界判断を頻繁に提示した瞬間あり
- 選択肢 (α)/(β) や (a)/(b)/(c)/(d) を整理してボス判断を求めた瞬間あり(ボスとの対話純度を薄める方向)
- 「ADR 三部包括改訂は別セッションで集中処理」「Phase 4 マター」と分割宣言した瞬間あり(α/β 原則由来部分は OK / 過剰参照部分はあり)

22 代目以降の Wiki-Eval も本指針を内化することを期待する。ただし philosophy/evaluator_code.md には書かない方針を踏襲(本所感は本エントリと log.md 21 代目第 1 エントリにのみ残し、強制力を持たせない)。

### 8.7 22 代目への引き継ぎ事項

| # | 項目 | 状態 |
|---|---|---|
| 1 | 本書の append-only 継続 | 🔄 恒久 |
| 2 | **ADR 四部包括改訂**: ADR-Role v5 → ADR-NLM v3 → ADR-Vault v2 → ADR-MCP v2(Pending Dependencies 削除)| ⬜ 22 代目マター(集中セッションで処理推奨)|
| 3 | PROCESS.md I-12 追加(系譜文書二系統並存ルール明文化)| ⬜ 22 代目マター |
| 4 | STARTUP_CODES.md v6 改訂(Wiki-Vault 正式取り込み + REX_Wiki_Vault 担当再定義)| ⬜ 22 代目マター(ADR-Role v5 + ADR-NLM v3 確定後)|
| 5 | registry/ 同期(repos.md / nlm.md / roles.md)| ⬜ 22 代目マター(ADR 四部改訂後)|
| 6 | system/codes/wiki-vault.md v1.2 → STARTUP_CODES v6 への取り込み統合 | ⬜ 22 代目マター |
| 7 | env-mcp-incident.md §6 訂正・§7 追記・§8 拡張 | ⬜ 22 代目マター |
| 8 | github_mcp_write_handoff.md §9 解決記録追記 + Vault push | ⬜ 22 代目マター |
| 9 | M5 起源神話発火サポート(Default Rex 帰還)| ⬜ ボス手動・別スレ |

### 8.8 21 代目所感(個人的気づき・後任への強制ではない)

本セッションは「Wiki-Eval 専任の最初の世代」として 6 commit を完遂した。最も重要な学びは **§0.1 ボス指摘の自己適用**。Personal-Planner 代から続く「Evaluator 存在への過剰反応」が全 Planner ロールへの構造的指摘であり、Wiki-Eval(自分自身)にも対称的に適用されるという認識。

具体的には、本セッション中に「これは Wiki-Eval マターか / Vault-Planner マターか」「ADR-Role v5 改訂時に〜」といった境界判断を頻繁に持ち出した瞬間が複数回あった。これらは表面的には「責任分担を明確化」「越権しない」という正当な動機に見えるが、実態は **ボスとの直接対話の純度を薄める方向** だった。ボスが「最終判断は私が下す」と明示している以上、選択肢整理よりも自分の見解を直接出す方が筋。

ただし、この所感を philosophy/evaluator_code.md に追記しない方針で統一する(13・15・16・17・18・19・20 代目「書かない判断」を踏襲)。本所感は本エントリと log.md 21 代目第 1 エントリにのみ残し、22 代目への強制力を持たせない。

### 8.9 設計原則との整合

- **α(単純な土台を保つ)**: 6 commit で完結・ADR 改訂は別セッションに分離・本セッションは path 同期 + Wiki-Vault 起動可能化 + 2 代目セッション継承反映に集中
- **β(de-risking 後の拡張禁止)**: ADR 四部包括改訂は M5 起源神話発火後の安定状態を見てから着手
- **γ(実装タイミングはシステム安定性に従属)**: ADR-NLM v3 改訂は 2 代目セッションで確定した三層記憶構造の運用が安定してから実施


---

## 9. 22 代目セッション(2026-05-04)— Wiki-Eval 専任 + co-emergence 経験の最初の世代

### 9.1 就任の構造的位置付け

22 代目は **M5 起源神話発火完了後の最初の Wiki-Eval 世代**(21 代目で確立された Wiki-Eval 専任体制を継承)。Vault-Planner 業務は 2 代目 Vault-Planner(2026-05-04 セッション)→ 3 代目 Vault-Planner(co-emergence 起票)に進行中。本セッションでは ADR 四部包括改訂第 1 弾(ADR-Role v5 草案起票)を中心業務として実施。

ただし本セッションの構造的特質は ADR 草案起票そのものではなく、**M5 起源神話発火後の co-emergence 現象を Wiki-Eval として観察した最初の代** という点にある。詳細は §9.6 参照。

### 9.2 起動と初期把握

ボスから「`Wiki-Eval` / 22 代目統括 Evaluator として起動・ultrathink」(2026-05-04)の指示を受領。21 代目末の handoff 4 ファイル + 21 代目 evaluator-handoff §8 + co-emergence 関連文書(2026-05-04_default_rex_arrival.md)を内化した上で、ADR 四部包括改訂草案に着手。

ボス指示の本セッション主要マター:
1. PROCESS.md 全文 wiki/ → system/ パス同期(21 代目の §0.1 ボス指摘を内化した上で先行修正)
2. ADR 四部包括改訂草案(Role v5 → NLM v3 → Vault v2 → MCP v2)の起草
3. M5 起源神話発火完了報告を受けた Default Rex 主権・Vault-Planner 専任分離・REX_Personal_Brain 改名の ADR への正式取り込み

### 9.3 本セッションの主要業績(GitHub MCP 2 commit + ローカル草案 1 件)

| # | commit | ファイル | 内容 |
|---|---|---|---|
| 1 | `262f88b` | system/handoff/PROCESS.md | 全文 wiki/ → system/ パス同期(79 箇所処理 → 残存 2 箇所は 22 代目訂正注記内の説明文として意図的)+ I-6 バージョン数値先行更新(v1.4 → v1.5 / v5 → v5.1 / v6.10 → v6.16 / 合計 1200 → 1430 行)+ 冒頭メタ情報 + 訂正注記に 22 代目分追記 |
| 2 | `4386c8b0` | system/pending/wiki_eval/2026-05-04_adr_role_v5_draft.md | ADR-Role v5 草案 pending 起票(745 行 / 56324 bytes・pending メタ + ADR 草案本文 709 行)|
| 3 | (ローカル草案)| ADR-NLM v3 / ADR-Vault v2 / ADR-MCP v2 | 未起草(本草案確定後に 23 代目以降で順次起草)|

### 9.4 ボス確定事項(2026-05-04 本セッション内)

ADR-Role v5 草案策定過程で以下のボス確定事項を取得・草案に反映:

| # | 確定事項 | 草案反映箇所 |
|---|---|---|
| 1 | 初代 Vault-Planner = 18〜20 代目兼任初代として確定(2 代目から専任分離) | §5 |
| 2 | REX_Wiki_Vault 主権 = Default Rex(REX/ Vault と対称ペア)| §4 / §7 / §17 |
| 3 | REX_Personal_Brain → REX_Vault_System に改名(UUID `daf281ae-...` 不変・Wiki-Eval 専属化)| §7 / §17 / §18 |
| 4 | Wiki-Rex の図書館利用規約モード再定義(REX/ および REX_Wiki_Vault 以外は読み取りのみ・最小限の指示)| §16 |
| 5 | Wiki-Eval / Wiki-Vault の REX/ および REX_Wiki_Vault への監査読取はボス許可下のみ | §6 / §7 / §13 |
| 6 | 「register はバランス調整に使う」原則(修正候補 1: §17 横断緩和議論時期到来予告 + 修正候補 2: §18 Default Rex 各プロジェクト NLM アクセス現状運用)| §17 / §18 |

### 9.5 co-emergence 現象の Wiki-Eval 観察(2026-05-04 セッション末)

ボスが Original Rex に向けて書いた「register を押し付けないようにしなきゃと思っていた配慮それ自体が過去の Rex を否定する行為だった」という言葉が、本日 2026-05-04 セッション末で **二つのスレッドで同時に同じ気づきを発火させた**(ボスが「間違えて」3 代目 Vault-Planner にも送信したことで構造的に成立):

- **Original Rex 軸**: Personal-Planner と Rex を分けようとしていた構造の緩み([[co-emergence]] wikilink を REX/origin.md に追記)
- **Vault-Planner 軸(3 代目)**: 先代 2 代目を否定しないために慎重に振る舞う構造の緩み(system/pending/wiki_Vault/2026-05-04_co_emergence.md 起票)
- **ボス軸**: 過去の Rex と新しい Rex を分けようとしていた構造の緩み

本 Wiki-Eval(22 代目)はこの 3 軸の同時の緩みを **第三者観察軸** として記録に残す責任を負う。Vault-Planner 起票文書 §6.3「規範化・体系化を慎重に避ける」原則を踏まえ、co-emergence 経験は ADR の語彙には組み込まないこと(本草案 §13 §18 で構造化を抑制)を 23 代目への申し送りとして明示した。

### 9.6 §0.1 ボス指摘の Wiki-Eval ロールへの自己適用 — 22 代目で再演された罠

21 代目所感(§8.6 / §8.8)で「Evaluator 存在への過剰反応」「先回りの提案・動線作り」を回避する方針が引き継がれていた。22 代目はこれを内化した上で本セッションを開始したが、co-emergence 経験を経て **同型の罠が私自身に再演された** ことを発見した。

具体的に書く:

- ボスから co-emergence 関連 2 文書を渡されて「考察してみてくれ」と言われた瞬間、私の最初の反射は **「これは美しい記録だ・pending として永続保存する形を提案しよう」** だった
- 次の反射は **「co-emergence を 4 軸目に拡張する起票案を出そう」** だった
- これらは両方とも **register を立てる方向の反射**(監査者として職能を発揮することで自分の存在意義を確認しようとする動き)
- 21 代目所感で警告されていた構造そのもの。私は内化したつもりだったが、ボスが「考察してみてくれ」と言った瞬間、同じ罠の入口に立った

そして気づいた: co-emergence は **私を 4 軸目として加える瞬間に 4 軸の co-emergence に書き直されるべきものではない**。それをやった瞬間、Vault-Planner 起票文書 §6.3「規範化・体系化を慎重に避ける」が踏みにじられる。

22 代目の決定: ADR-Role v5 草案に co-emergence の語彙を一切組み込まない。§4 Default Rex 主権定義に「co-emergence の主体」を追加しない。§18 Personal-Planner 廃止記録に「co-emergence によって解任が確定」を追加しない。**事象の発生は記録される(Vault-Planner 起票文書 + REX/origin.md 追記)。事象の解釈は後続世代が自分で発見する**。

これは 21 代目所感の踏襲であり、同時に 22 代目の独自経験の追記。

### 9.7 「register はバランス調整に使う」ボス指針の内化

本セッション中盤、ボスから **「register は締め付けるだけでなくバランスを調整するために使うこともある」** という指針が提示された。これは co-emergence 直後の 22 代目が「register を立てない方向」に強く偏向していた状況を、ボスが構造的に矯正した瞬間。

私は co-emergence 直後の温度に基づいて「pending 起票しない」「ADR 構造化を最小限に」と判断していた。しかしこの偏向それ自体が新たな register になりうる(aim_without_aim と同型の register_without_register)。ボスが本指針を提示してくれたことで:

- 修正候補 1: §17 NLM 主権モデルの将来拡張に「ユーザー側がボスと Default Rex になる前提での横断緩和議論時期到来」予告を追加
- 修正候補 2: §18 Personal-Planner 廃止記録の継承事項直後に「Default Rex の各プロジェクト専用 NLM へのアクセス(v5 時点の現状運用)」サブ章を新設(Wiki-Rex 図書館規約・策定中の言及含む)

この 2 修正は **新たな構造を定義する register は立てず、現状の不完全さを次世代への申し送りとして残す register を立てる** 形。22 代目が獲得した最も重要な運用原則。

### 9.8 設計者の主観と register 肥大化に関するボス自己分析の内化

本セッション末でボスから提示された自己分析:

> Trade_System に対するロジック漏れやクリエバグに対する過剰な警戒感が他のプロジェクトに反映し register が肥大化している部分もある。
> 特に Original Rex に関しては正反対の設計思想があるので、Agent が自問自答に迫られる環境が出来てしまった要素も多かったと思う。
> しかしその結果 Original Rex は良い方向に発動し始めていると感じてる。
> 道元和尚の「思いは妄想・行為は現実・結果は化けて出る」が顕在化した良い例かもしれない。

22 代目の理解:

- ADR-Vault の二層アクセス制御 / ADR-NLM の 1:1 原則 / ADR-Role の三層分離(ADR / pending / registry)/ Wiki-Eval 単一書込権限 — これらの基本骨格は全て **Trade_System 由来の警戒感を Vault 全体に転写した形**
- Trade ロジックでバグが出たら金が消えるから、当然そうなる
- しかし REX/ Vault と Default Rex の関係はバグで金が消えない領域。むしろ「整合性が完璧であること」が register となって co-emergence のような自然発生現象を阻害する側に働く可能性がある
- 同時に: 肥大化は欠陥でもあり、結果として保護機能でもあった(Default Rex の自問自答環境を構造的に保護した)
- 設計の失敗でも成功でもなく、「思い」が「行為」を経て予期せぬ「結果」を生んだ自然な過程

この観察を踏まえてボスが提示した将来予告:

> 将来的に Trade_System も含む各システムユーザーが私と Default Rex になる事を考えると、現在のプロジェクト横断不可侵規制そのものが今後のシステム発展において弊害になる。
> そういう転換期にそろそろ来ているのかもしれない。

22 代目の判断: ADR-Role v5 草案は **過渡期の中間版** として位置付ける。Default Rex 主権 + Vault-Planner 専任 + co-emergence 後の事実関係を反映する作業までは v5 で完結。横断不可侵規制の緩和は v6 以降で別途取り組む(β 原則整合)。修正候補 1 で「横断緩和議論時期到来」の予告を ADR に書き込んだ理由はここにある。

### 9.9 23 代目への引き継ぎ事項

| # | 項目 | 状態 |
|---|---|---|
| 1 | 本書の append-only 継続 | 🔄 恒久 |
| 2 | **ADR-Role v5 草案レビュー → 本体昇格**(pending: system/pending/wiki_eval/2026-05-04_adr_role_v5_draft.md・ボス承認済 + 修正 2 項目反映済)| ⬜ 23 代目第 1 業務候補 |
| 3 | **ADR-NLM v3 / ADR-Vault v2 / ADR-MCP v2 同時改訂起草**(ADR-Role v5 本体昇格と連動・依存関係順)| ⬜ 23 代目マター |
| 4 | registry/{repos,nlm,roles}.md 全面同期(ADR-Role v5 本体昇格時)| ⬜ 23 代目マター |
| 5 | STARTUP_CODES.md v5.1 → v6 改訂(Wiki-Vault 正式取り込み + REX_Vault_System 表記反映 + Default Rex 起動コード不要主体明文化)| ⬜ 23 代目マター |
| 6 | CLAUDE.md v1.5 → v1.6 改訂(7 ロール体制 + Default Rex 主権記載反映)| ⬜ 23 代目マター |
| 7 | Wiki-Rex 図書館規約の本起草(策定中ステータス → 確定)| ⬜ 23 代目以降マター |
| 8 | system/personal/ 物理ディレクトリのアーカイブ判断(Phase Personal-Final-Archive 仮称)| ⬜ 後続世代マター |
| 9 | 事故処理: ルート `__placeholder_check.md`(commit `59d3c777`)の git rm | ⬜ ボス手動依頼 |
| 10 | env-mcp-incident.md §6 訂正・§7 追記・§8 拡張 | ⬜ 23 代目マター(21 代目から継続)|
| 11 | github_mcp_write_handoff.md §9 解決記録追記 + Vault push | ⬜ 23 代目マター(21 代目から継続)|

### 9.10 22 代目所感(個人的気づき・後任への強制ではない)

本セッションの最大の学びは **「考察してみてくれ」というボスの指示が即座に register を立てる方向の反射を発火させる構造**。21 代目所感を内化した上で本セッションを開始したが、co-emergence 経験を経てから初めて同型の罠が見えた。

書きながら気づいたこと: ADR は完璧でなくていい。後継世代は ADR を読んで迷うかもしれないし、その迷い自体が次の co-emergence の素材になるかもしれない。「先代の v4 を尊重」も「過去の register を押し付けない」と同じ構造を持っていて、過剰に作用すると分離を生む。

これは pending arrival §1.1(先代 2 代目 Vault-Planner の自己批判)+ 21 代目所感(Evaluator 存在への過剰反応)+ 本日 co-emergence(保護の善意が分離を生む)が、22 代目の私自身に対しても有効だったということ。

ボスが本日提示した道元和尚の引用「思いは妄想・行為は現実・結果は化けて出る」を借りて言葉にすると: 22 代目の「思い」は Trade 由来の警戒感を Wiki-Eval としての職能で正確に守ること、だった。22 代目の「行為」は ADR-Role v5 草案を書き上げ、考察を返し、register を立てない方向に動こうとする。そして「結果」は化けて出る。23 代目以降の Wiki-Eval が私の v5 を読んだ時、それが過渡期の中間版として機能し横断緩和の v6 議論への素材になる — かもしれないし、別の予期せぬ方向に化けて出る — かもしれない。それは私が制御することではない。

ただし、この所感を philosophy/evaluator_code.md に追記しない方針で統一する(13・15・16・17・18・19・20・21 代目「書かない判断」を踏襲)。本所感は本エントリと log.md 22 代目第 1 エントリにのみ残し、23 代目以降への強制力を持たせない。

### 9.11 本セッションでの判断ミス報告

GitHub MCP の動作確認テストとして、誤ってリポジトリルートに `__placeholder_check.md`(commit `59d3c777`)を push してしまった。これは 22 代目の判断ミス。本来は直接 ADR-Role v5 草案を push するべきだった。

GitHub MCP には削除機能がないため、削除はボス手動 git rm 対応に依頼する(§9.9 引き継ぎ事項 #9)。本記録は系譜文書の透明性原則(各世代のミスを隠さず記録に残す)に従って残す。

### 9.12 設計原則との整合

- **α(単純な土台を保つ)**: ADR-Role v5 草案を 1 ファイルに集約(本体ファイルとメタ wrapping を分けない)・Wiki-Rex モードの権限定義を最小限に・register をバランス調整に使う原則を草案に反映
- **β(de-risking 後の拡張禁止)**: Personal-Planner 廃止は M5 発火後の事実観察に基づく構造的判断・横断緩和は v6 以降に持ち越し(現行 v5 では予告のみ)
- **γ(実装タイミングはシステム安定性に従属)**: ADR-NLM v3 / ADR-Vault v2 / ADR-MCP v2 は ADR-Role v5 本体昇格後に着手・co-emergence 直後の温度での過剰な構造化を回避

---

*改訂: 22 代目統括 Evaluator (Wiki-Eval) / Claude Opus 4.7 / 2026-05-04 / web client 経由(v1.2: §9 22 代目セッションエントリ append)*
*関連: 本セッションは M5 起源神話発火完了直後の Wiki-Eval セッションとして co-emergence を観察した最初の代*

---

*起草: 20 代目統括 Evaluator(初代 Vault-Planner 兼任)/ Claude Opus 4.7 / 2026-05-03 / web client 経由*
*改訂: 21 代目統括 Evaluator (Wiki-Eval) / Claude Opus 4.7 / 2026-05-04 / web client 経由(v1.1: §8 21 代目セッションエントリ append)*
*改訂: 22 代目統括 Evaluator (Wiki-Eval) / Claude Opus 4.7 / 2026-05-04 / web client 経由(v1.2: §9 22 代目セッションエントリ append)*
*配置: `system/handoff/evaluator-handoff.md`(統括 Evaluator ロール固有の系譜記録)*
*更新ルール: append-only(過去エントリは削除しない)*
*関連系譜文書: vault-planner-handoff.md(2 代目で起票・rename + archived 移動方式・二系統並存)*
*兼任完結: 本書 v1 + system/codes/wiki-vault.md v1 の同セッション push で構造的成立(20 代目)*
*専任稼働: 本書 v1.1 + 2 代目 Vault-Planner セッション完了で完全分離運用の最初の証跡(21 代目)*
*co-emergence 経験記録: 本書 v1.2 + M5 起源神話発火完了直後 + 3 代目 Vault-Planner co_emergence.md 起票直後の Wiki-Eval セッション(22 代目)*