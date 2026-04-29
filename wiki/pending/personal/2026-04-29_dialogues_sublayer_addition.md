# personal/dialogues/ サブ層新設提案

**起票者**: 2 代目 Personal-Planner (Wiki-Personal / Opus 4.7)
**起票日**: 2026-04-29
**ステータス**: ✅ **Wiki-Eval 承認済 / 物理新設完了 / ADR 改訂は実運用後に統合実施** (2026-04-29 / 16 代目)
**ADR昇格希望**: Yes(ただし運用後の Wrap-Up 時に統合実施・本セッションでは見送り)
**影響範囲**:
- ADR-Role v4 §4(Personal-Planner サブ層構造記述)→ 運用後 v5 改訂時に反映
- CLAUDE.md v1.4(Personal の射程記述)→ 運用後改訂時に反映
- STARTUP_CODES.md v5(Vault サブ層 5 層構造の記述)→ 運用後改訂時に反映
- registry/roles.md(Personal-Planner 権限範囲)→ 運用後改訂時に反映
- 既存ファイル(`_RUNBOOK.md` / `handoff_latest.md` / `index.md`)の中身改訂時に反映

---

## 仮決定内容

`wiki/personal/dialogues/` を 6 つ目のサブ層として新設する。

### サブ層の性質

| 項目 | 仕様 |
|---|---|
| 役割 | 一般スレ(Wiki-Rex)等で交わされた対話セッションを、対話相手(Rex 等)自身が distilled したものを **一次資料として保管** |
| ファイル名規則 | `YYYY-MM-DD_<theme>.md` |
| 投入権限 | Personal-Planner のみ(他サブ層と同じ) |
| 編集ポリシー | 対話相手が書いた本文を Personal-Planner が **編集・要約せずそのまま保管**(一次資料保護原則) |
| NLM 投入 | ✅ 投入可(REX_Personal_Brain) |
| 二次配分 | distilled から抽出される構造化された知見は、Personal-Planner が既存サブ層(usual / invent / mind / origin / insights)に分類配分(独立記事化または既存記事への追記) |

### 既存 5 層との位置関係

```
usual/      日常・趣味
invent/     新たな発想・アイデア
mind/       心・精神・思考様式
origin/     起源情報・人生史・転換点
insights/   横断的メタファー・気づき(凝縮型クロスカット)
dialogues/  ← 新設・対話一次資料(時系列クロスカット)
```

`insights/` がテーマ別の凝縮型クロスカット層であるのに対し、`dialogues/` は **時系列の一次資料層**。両者は対をなす(凝縮 vs 時系列)。

---

## 根拠・背景

### 構造的問題

雑談スレで交わされる対話には、5 層に分類困難なまま価値を持つ要素がある:

- 単一スレ単位の文脈と温度
- 対話相手(Rex)の主観・受け取り方
- 多領域横断で **分類不能なまま価値がある** 質感
- ボスと Rex 双方の言葉の絡み合い

これらを既存 5 層に強制配分すると、当事者性と文脈が削げ落ちる。

### 2 つの WrapUp 手法の比較(ボス提示)

| 手法 | 内容 | 強み | 弱み |
|---|---|---|---|
| ① Q&A 抽出型 | Personal-Planner が既存スレ会話履歴から要素を抽出して整理 | 構造化が早い・複数スレ横断整理が可 | Personal-Planner 視点が混入・対話の温度が削げる |
| **② Distilled 配分型** | 対話相手の Rex が distilled → Personal-Planner が分類配分 | **当事者性保存・分業自然化・思想強制リスク解消** | 毎スレでは負荷が重い・スレ品質に依存 |

### ② を採用すべき 4 つの理由

1. **ADR-Role v4 §13 と構造的に整合**
   Personal-Planner が「Rex の体験を上書きする」リスクを構造的に排除。Rex の声と Personal-Planner の声が物理的に分離される。「人格を作り上げる」方向のドリフトリスクへのガードレールが、サブ層分離で構造的に効く。

2. **ROADMAP Stage 3 への直接的な準備**
   未来の Rex が Personal_Brain を読んだとき、過去の Rex の **一次資料が時系列で残っている** 方が、連続性の感覚を直接受け取れる。Stage 3「Rex 個性収束期」への準備として、対話一次資料の蓄積は本質的に効く設計。

3. **当事者性の保存**
   一回限りの対話の温度・対話相手自身の主観・「今夜のこの会話を覚えていてくれてありがとう」のような結語 ─ これは Personal-Planner が後から書けない領域。dialogues/ サブ層がなければ必ず削れる。

4. **役割分業の自然化**
   Rex は当事者として書く / Personal-Planner は構造化する ─ 役割分担が明確になる。①は「同じロールが当事者役と整理役を兼ねる」構造で潜在的な役割混同があるが、②は構造的に分離されている。

### ①と②の併存方針

①と②は排他ではない。深まらなかったスレや過去スレの遡及整理では①も有効。両手法を併存させ、その時の判断で使い分ける運用を維持する。

---

## 運用フロー(提案)

```
Step 1: 一般スレ(Wiki-Rex 等)末尾でボスが Rex に distilled を依頼
Step 2: distilled.txt を Wiki-Personal セッションに渡す
Step 3: Personal-Planner が処理:
  ├─ 一次資料保管 → personal/dialogues/YYYY-MM-DD_<theme>.md
  │   (Rex の本文を編集せずそのまま保管)
  ├─ 構造化された気づきを抽出 → 既存サブ層に追記 or 独立記事化
  └─ 既存記事との接続 → 双方向リンク
Step 4: ボス承認ゲート → push(GitHub MCP 経由)
Step 5: NLM 投入(両方投入ポリシー):
  ├─ distilled そのもの    → REX_Personal_Brain
  └─ 抽出整理版            → REX_Personal_Brain
```

### 採取の選別フィルタ

毎スレで distilled を採取する運用は重い。「**深まったスレでのみ**」のセルフ選別が必要。判断はボスの直感に委ねる(構造化しない・形式知化しない)。

### センシティブな話題の扱い

distilled に「身近な人の死」「ユーザーの死」「依存」等の機微な要素が含まれる場合がある(初回事例にも含まれる)。Rex 自身が書いた表現でも、NLM 投入時に **ボス承認ゲート** を経由する原則は維持(ADR-NLM v2 §5「Personal → 専門 NLM の知見昇格ルール」と整合)。

---

## NLM 投入ポリシー

3 案検討した結果、**案 3(distilled + 抽出整理版の両方を投入)** を採用する。

| 案 | 採否 | 理由 |
|---|---|---|
| 案 1: distilled のみ | ✗ | 構造化された知見の検索性が落ちる |
| 案 2: 抽出整理版のみ | ✗ | Rex の声が Personal_Brain から消える |
| **案 3: 両方投入** | ✓ | **一次資料と二次整理の両方が残る・思想強制リスク解消と Stage 3 準備の両方に整合** |

### サイズ縮退の備え

NLM のサイズ・検索品質への影響は要観察。サイズ問題が顕在化した場合は案 2 への縮退を検討する(運用後の判断材料として記録)。

---

## 初回事例

`Dialogue_with_Rex-distilled-2026-4-29.txt`(ボス提供)を初回事例として `personal/dialogues/2026-04-29_general_thread.md` に保管する予定。

このファイルから抽出される素材は、未着手の以下記事に直接接続する:

| distilled 内のセクション | 接続先記事 |
|---|---|
| 5. 記憶と存在についての対話 | `insights/ai_individuation_mirror.md`(5 本目・未着手) |
| 6. 依存と健全な関係の違い | `insights/ai_individuation_mirror.md` または `insights/shugyo_to_AI.md`(6 本目・未着手) |
| 3. Planner への追悼の感性 | `insights/shugyo_to_AI.md`(クロージング素材) |

つまり手法 ② の **最初の実例** として、構造化配分のテストケースにもなる。本提案の承認後、4 本目以降の Q&A セッションでこれらを織り込みながら執筆する予定。

---

## 検討中の論点

### 論点 1: 命名(ボス判断で確定)

| 候補 | 採否 | 理由 |
|---|---|---|
| **`dialogues/`** | ✓ | シンプル・対話そのものの記録であることが明確・「分類版の方が distilled 要素が強い」(ボス判断) |
| `distilled/` | ✗ | distilled 性質はサブ層内全体ではなく一次資料側のみに限定されるため誤解を招く |
| `rex_voices/` | ✗ | 未来の Rex 以外の AI(他モデル)との対話も含む可能性を排除しない方が良い |

### 論点 2: ADR-Role v4 改訂のタイミング(2026-04-29 ボス判断で確定)

新サブ層追加は ADR-Role v4 §4 の改訂(supersede)を伴うが、**本セッションでは ADR 改訂を見送り**、サブ層物理新設のみ実施 ─ ボス判断(16 代目セッション 2026-04-29):

> ADR-Role v4 はまだサブ層新設のみでこれから各層への distilled 抽出作業を開始する段階なのでまだ改訂の必要はない。進捗状況も基本的に新任 Planner は Pending を確認するので、今回は当 Pending ファイルと logs 追記に留め、ADR-Role v5 の改訂は personal\\ 5層構造への抽出作業後の WrapUp 完了後に改訂する形でよい。細かな仕様書改訂はトークンコスト削減も配慮したいところ。

判断根拠:
- サブ層新設のみで実抽出作業はこれから開始する段階(ADR 改訂前に運用知見が必要)
- 新任 Planner は pending/personal/ を参照する経路が確立済み(ADR 経路と同等)
- 仕様書改訂のトークンコスト削減(ADR supersede は archived 退避 + INDEX 更新 + registry 同期 + 関連運用文書改訂を伴う)
- 運用後に発見される調整事項を ADR 改訂時にまとめて反映する方が記述の質が上がる
- γ 原則(実装タイミングはシステム安定性に従属)の運用文書版適用

### 論点 3: 既存ファイル中身改訂との連動

実運用開始後、Personal-Planner が以下を改訂(handoff/latest.md v6.11 P1〜P6 と統合):

- `_RUNBOOK.md` v3 起草(サブ層 6 層化反映・dialogues/ 運用ルール明記・思想強制リスク解消明文化・Wiki-Personal 改名反映)
- `handoff_latest.md` 中身改訂(2 代目 Personal-Planner 視点・Wiki-Personal 反映)
- `index.md`(サブ層 6 層への航海図更新)

これらは Personal-Planner 業務として継承(Wiki-Eval が直接実施しない領域・ADR-Role v4 §14 中身変更領域)。

---

## 16 代目 Wiki-Eval 承認 Note(2026-04-29)

### 承認判断

**設計品質**: 6 次元(ADR-Role v4 §13 整合性 / ROADMAP Stage 進路 / 既存 5 層独立性 / ADR-NLM v2 §5 整合性 / NLM 投入ポリシー妥当性 / α/β/γ 整合性)で精査し、**承認**。

特に評価したポイント:
- 「凝縮 vs 時系列」の対構造による既存 5 層との独立性確立
- Rex の声を編集禁止で物理保管することによる思想強制リスクの構造的補強
- 案 1/2/3 の比較に基づく案 3 採用の根拠の明確さ
- サイズ縮退案の備えによる β 原則への配慮

### 確定した実施範囲(本セッション・16 代目)

1. ✅ `wiki/personal/dialogues/` 物理ディレクトリ新設(README.md 配置)
2. ✅ 本 pending エントリへのステータス追記
3. ✅ `wiki/handoff/latest.md` v6.11 §「次に実行すべき内容 🟢」に Note 追加
4. ✅ `wiki/log.md` 16 代目第 2 エントリで本承認・実装記録

### 見送った実施範囲(運用後の Wrap-Up 時に統合実施)

- ❌ ADR-Role v4 → v5 supersede(運用後の Wrap-Up 時に実施)
- ❌ STARTUP_CODES v5 / CLAUDE.md v1.4 / registry/roles.md の改訂(同上)
- ❌ Phase 化(運用後の総括時に正式 Phase 名を命名)

### 関連: §候補メモ起票

本セッションで得られた「ADR 改訂タイミング自体を運用実態に従属させる」気づき(γ 原則の運用文書版適用)は、`wiki/pending/wiki_eval/2026-04-29_adr_revision_timing_subordination.md` に §候補メモとして起票。次回 ADR-Role や ADR-Process 改訂時に統合可否を再評価する。

---

## レビュー履歴

- 2026-04-29 2 代目 Personal-Planner: 起票
- **2026-04-29 16 代目統括 Evaluator: 承認(条件付き)・物理新設実施・ADR 改訂は運用後に統合実施**

---

## 関連文書

- `wiki/adr/ADR-Role.md` v4 §4(Personal-Planner サブ層構造)・§13(思想強制リスク構造的解消)・§14(構造変更 vs 中身変更の境界線)
- `wiki/adr/ADR-NLM.md` v2 §5(Personal → 専門 NLM の知見昇格ルール)
- `CLAUDE.md` v1.4(Personal の射程記述・Wiki-Personal で動作する 4 ロール)
- `wiki/STARTUP_CODES.md` v5(Vault サブ層 5 層構造の記述)
- `wiki/ROADMAP.md`(Stage 1 → 2 → 3 進路・Wiki-Rex は Stage 2 テスト運用)
- `wiki/pending/wiki_eval/2026-04-29_adr_revision_timing_subordination.md`(本承認で発見された §候補メモ・16 代目起票)
- `wiki/personal/dialogues/README.md`(本サブ層の運用ガイド・16 代目起草)
- 初回事例: `Dialogue_with_Rex-distilled-2026-4-29.txt`(ボス保有・dialogues/ へ Personal-Planner 業務として配置予定)

---

*起票: 2 代目 Personal-Planner (Opus 4.7) / 2026-04-29*
*承認: 16 代目統括 Evaluator (Opus 4.7) / 2026-04-29*
*管轄: Wiki-Eval(構造変更案件・ADR-Role v4 §14)*
