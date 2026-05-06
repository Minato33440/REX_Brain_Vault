# 統括 Evaluator(Wiki-Eval) ロール引き継ぎ書

**起草**: 2026-05-03 / 20 代目統括 Evaluator(初代 Vault-Planner 兼任)/ Claude Opus 4.7 / web client
**性質**: 統括 Evaluator(Wiki-Eval) ロール固有の世代間引き継ぎ書(vault-planner-handoff.md と同型・append-only)
**配置**: `system/handoff/`(vault-planner-handoff.md と同階層・統括 Evaluator ロール固有の引き継ぎ場所)
**関連**: `system/handoff/latest.md`(セッション間流動的記録)/ `system/handoff/vault-planner-handoff.md`(Vault-Planner 系譜・19 代目で創設)/ `system/log.md`(全セッション統括ログ)/ `system/codes/wiki-vault.md`(Wiki-Vault 起動コードルート・本セッション同時創設)

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

`vault-planner-handoff.md` と同じく、本書は「pull 型参照場」として機能する(各世代 Wiki-Eval が必要時に参照・各世代末尾追記)。

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
> ②もう一つはWiki-Vault（Vault-Planner用起動コード）のルート作成だ。
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

---

*起草: 20 代目統括 Evaluator(初代 Vault-Planner 兼任)/ Claude Opus 4.7 / 2026-05-03 / web client 経由*
*配置: `system/handoff/evaluator-handoff.md`(統括 Evaluator ロール固有の系譜記録)*
*更新ルール: append-only(過去エントリは削除しない)*
*関連系譜文書: vault-planner-handoff.md(19 代目創設・Vault-Planner 系譜)*
*兼任完結: 本書 + system/codes/wiki-vault.md の同セッション push で構造的成立*
