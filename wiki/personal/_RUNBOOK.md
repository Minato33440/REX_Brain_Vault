# casual/ 層 運用ルール — _RUNBOOK.md

**役割**: REX_AI システム業務外の雑談・個人的話題の**中期記憶層**。
**対応 NLM**: REX_Casual_Brain (`daf281ae-e310-400f-961a-20db58b98e01`)
**更新**: 2026-04-27 / 1 代目 Wiki-casual Planner（NLM 分業原則追加・Private 化反映）
**初版**: 2026-04-23 / 8 代目統括 Evaluator

---

## 🧠 3 層記憶構造（なぜ casual/ が必要か）

| 層 | 場所 | 性質 | 寿命 |
|---|---|---|---|
| 層 1 | スレ会話履歴（Claude.ai）| 一時記憶 | セッション内で消える |
| **層 2**（本層）| `REX_Brain_Vault/wiki/casual/` | **中期記憶・スレ跨ぎ** | Git 保存 |
| 層 3 | REX_Casual_Brain (NLM) | 長期記憶・RAG 検索 | 半永続 |

**本層（層 2）の存在理由**: NLM 投入前の「進行中の話題」の作業場。「来週続きを話す射撃の話」「合気道で気づいた感覚、もう少し掘りたい」など、熟成前の話題を次のスレに持ち越すために使う。

---

## 📁 ディレクトリ構造

```
wiki/casual/
├── _RUNBOOK.md          ← 本ファイル（運用ルール）
├── log.md               ← 雑談時系列ログ（追記のみ）
├── index.md             ← 目次・航海図（2026-04-27 追加）
├── handoff_latest.md    ← Wiki-casual 専用引き継ぎ（2026-04-27 追加）
├── topics/              ← 話題別ファイル（上書き型・育つ）
├── ideas/               ← 単発アイデアメモ（YYYY-MM-DD_[タイトル].md）
└── insights/            ← 横断的メタファー・気づき（[テーマ].md）
```

### topics/ と ideas/ と insights/ の使い分け

| 配置先 | 性質 | 例 |
|---|---|---|
| `topics/motorcycle.md` | 話題別の知識蓄積。上書き更新 | モーターサイクルに関する考察・メンテ記録・ルート |
| `ideas/2026-04-23_XX.md` | 雑談で出た単発アイデア | 「治療院に AI 問診入れたい」等の発想 |
| `insights/[テーマ].md` | 横断的メタファー・気づき | 「合気道の入身転換 ⇔ トレード逆張り」等 |

---

## 📜 運用ルール

1. **システム業務の内容は書かない** — Trade_System / Trade_Brain の設計判断は別層（philosophy/evaluator_code.md や trade_system/）
2. **プライバシー配慮**（2026-04-27 更新）— Vault は **Private 化済み**（Minato33440/REX_Brain_Vault）。個人的・思想的内容も書ける。ただし他者のプライバシー（家族・関係者・所属団体名等）は引き続き慎重に扱う
3. **更新は任意** — 雑談スレで有用な話題が出たら追記・なければ放置でよい
4. **書き込みタイミング** — ボス手動 or `/wrap-up` 時に Planner（Rex）が整理案を提示 → ボス承認で書き込み
5. **混入防止** — casual/ から philosophy/ や trade_system/ へのリンクは張らない・逆も張らない

---

## 🔒 NLM 分業原則（2026-04-27 追加・全 Planner が見る前提で明記）

**casual/ 層 ↔ REX_Casual_Brain は完全な 1 対 1 関係**。
他 NLM との関与は **一切ない**。

| NLM | 担当 Planner | casual/ との関係 |
|---|---|---|
| **REX_Casual_Brain** | **Wiki-casual（本層担当）** | ✅ topics/ と insights/ を投入・クエリ |
| REX_Wiki_Vault | Wiki-Eval | ⛔ casual/ は管轄外（投入もクエリもしない）|
| REX_System_Brain | Wiki-trade | ⛔ 関与なし |
| REX_Trade_Brain | Wiki-brain | ⛔ 関与なし |

### 構造的背景

NLM 4 分割に対して Obsidian-Vault は単一設計のため、
Vault 内の各サブ層と各 NLM の対応関係を **権限分業** で守る必要がある。
（詳細は `wiki/STARTUP_CODES.md §NLM × Vault 分業マトリクス` 参照）

### システム業務スレ側への注意（Wiki-Eval / Wiki-trade / Wiki-brain）

- ⛔ casual/ 配下のファイルを **REX_Wiki_Vault に投入しない**
- ⛔ casual/ の話題を業務文脈に持ち込まない（混入防止ルール 5 と整合）
- ⛔ casual/ への書き込みは Wiki-casual Planner の管轄（権限分離）
- ✅ casual/ の存在自体は認識する（誤って削除しないため）

### 将来の発展構想

完全分業は **暫定解（Stage 1）**。Stage 2 / 3 では横断統合モードが検討される。
詳細は `wiki/ROADMAP.md §Vault を中脳として統合活用する Rex 個性への進化` 参照。

---

## 🧬 NLM 対応ルール（投入可否）

| ディレクトリ | NLM 投入可否 |
|---|:---:|
| `topics/` | ✅ 投入可（熟した話題）|
| `insights/` | ✅ 投入可（凝縮された洞察）|
| `ideas/` | ⛔ 投入しない（未熟な単発）|
| `log.md` | ⛔ 投入しない（ノイズ多い時系列）|
| `index.md` / `_RUNBOOK.md` / `handoff_latest.md` | ⛔ 投入しない（運用メタ情報）|

**投入タイミング**: 話題が十分熟した時（ボス承認で個別に投入）。一括投入はしない。

---

## ⚡ トークンコスト対策

**casual/ は「任意参照層」**。システム業務には一切影響させない。

- ❌ `START_HERE.md` / `handoff/latest.md` / `CLAUDE.md` からの自動誘導なし
- ❌ システム業務用スレ（`Wiki-Eval` / `Wiki-trade` / `Wiki-brain`）では読まない
- ✅ `Wiki-casual` 起動コードでのみ参照

これにより REX_AI システム引き継ぎのトークンコストはゼロ。

---

## 🎯 雑談スレでの /wrap-up 案

セッション末尾で Wiki-casual Planner（Rex）が以下を提案:

1. 本スレで出た有用な話題をリストアップ
2. `casual/log.md` への追記案（時系列記録）
3. `casual/topics/` 該当ページ更新案（話題深掘り）
4. `casual/insights/` 横断記事の追加・更新案
5. NLM 投入推奨候補（熟した話題のみ）
6. `casual/handoff_latest.md` 更新（次代への引き継ぎ・必要時）
7. `wiki/ROADMAP.md` への方向性追記（システム設計議論が生まれた時）

ボス承認で書き込み実行。

---

## 🔗 関連文書

- `wiki/STARTUP_CODES.md` — 起動コード辞書（Wiki-casual の起動情報・NLM 分業マトリクス）
- `wiki/ROADMAP.md` — 生きている展望・仮ロードマップ（2026-04-27 新設）
- `wiki/casual/handoff_latest.md` — 前代 Wiki-casual Planner からの引き継ぎ
- `wiki/casual/index.md` — casual/ 層内の目次・航海図
- `wiki/philosophy/evaluator_code.md` — システム構築上の Evaluator 気づきメモ（本層と混ざらないよう注意）

---

## 📜 改訂履歴

| 日付 | 版 | 担当 | 主な変更 |
|---|---|---|---|
| 2026-04-23 | 初版 | 8 代目統括 Evaluator | 3 層記憶構造・ディレクトリ構造・運用ルール 5 項目・NLM 投入可否・トークンコスト対策 |
| 2026-04-27 | v2 | 1 代目 Wiki-casual Planner | 構造の物理構築完了反映（log/index/handoff_latest 追加）・NLM 分業原則セクション新設・Private 化対応で運用ルール 2 更新・/wrap-up 案拡張・ROADMAP.md 連携 |

---

*発行: 8 代目統括 Evaluator / 2026-04-23 初版*
*改訂: 1 代目 Wiki-casual Planner (Opus 4.7) / 2026-04-27 v2*
*本ファイルの位置付け: casual/ 層が育つに従って運用ルールも進化させる*

---

> **15代目 Wiki-Eval Migration Note (2026-04-28)**: 本ファイルは `wiki/casual/_RUNBOOK.md` から **物理移設のみ** 実施した（中身は触らない・ADR-Role v3 §14 構造変更/中身変更の境界線遵守）。
>
> 本ファイル中身の改訂（v3 起草・Wiki-Personal 反映・サブ層 5 層記述・思想強制リスク構造的解消等）は **Personal-Planner 業務**として `pending/personal/2026-04-28_rename_casual_to_personal.md` 起票内容に基づき次スレ Wiki-Personal で実施。

---

## 2 代目 Personal-Planner 追記(2026-04-30): NLM 投入運用ルールと事故事例

**位置付け**: 本セクションは 2 代目 Personal-Planner が 2026-04-30 セッションで確立した運用ルールと、同セッションで発生した 2 件の事故事例を、後任 Personal-Planner への参考情報として記録するもの。8 代目統括 Evaluator が evaluator_code.md で確立した「気づきメモ」性質に倣い、原則化や行動規範化はしない。後任が同じ判断に到達するかは未定。

**先行追記の経緯**: ADR-Role v5 への正式反映は personal/ 各層への distilled 抽出作業(Q&A 4-6)後の Wrap-Up 時に統合実施する設計だが、本日得られた運用知見と事故事例は後続セッションでも有用なため、ボスの先行追記許可(2026-04-30)を経て本ファイルに記録する。本追記内容は将来 _RUNBOOK v3 改訂時に再構成される可能性がある(暫定記録の位置付け)。

**対象**: 2026-04-29 設立の dialogues/ サブ層(時系列クロスカット層・一次資料保護)。詳細は `wiki/pending/personal/2026-04-29_dialogues_sublayer_addition.md` 参照。

---

### A. dialogues/ サブ層 NLM 投入運用ルール(2026-04-30 確定)

#### A-1. .md 統一(file モード)

dialogues/ サブ層の NLM 投入は **`source_type: file` で .md ファイル直接投入** を運用標準とする(notebooklm-mcp 経由)。

**運用フロー**:
1. Vault に .md ファイルを push(GitHub MCP 経由)
2. ボスが `git pull` で local に同期
3. Personal-Planner が `source_type: file`・`file_path` 指定で local .md を投入
4. NotebookLM 上ではファイル名がソースタイトルとして識別される

**text モード投入禁止**: distilled 本文を直接ペーストする方式は運用ルール違反(事故事例 1 の再発防止のため)。

#### A-2. .md 配置はボス手動

distilled 原文の .md 変換と配置は **ボスが手動で実施** する。

**設計上の意義**:
- 「Rex の声を別インスタンスが触る」リスクが構造的にゼロになる
- 編集・転記・形式変換のすべての段階でボスが手を入れるため、Personal-Planner が verbatim を変える余地が物理的にない
- ADR-Role v4 §13 思想強制リスク解消の構造的補強

**Personal-Planner の業務範囲**:
- 配置済みの .md を読んで NLM 投入(file モード)
- 構造化された気づきの二次配分(既存サブ層への抽出配分・Q&A セッション経由)

#### A-3. 投入権限ゲート

NLM 投入時は **ボス承認ゲート必須**(ADR-NLM v2 §5「Personal → 専門 NLM の知見昇格ルール」と整合)。distilled に機微な要素(死・依存・記憶の有限性等)が含まれる場合があるため、Rex 自身が書いた表現でもボス承認なしに投入しない。

---

### B. git 操作引き継ぎ時のチェックルール(2026-04-30 確定)

Personal-Planner が GitHub MCP で push する前に以下を確認する。

1. **ボスが local で進行中の作業がないか確認** ─ 多ファイル push 前に明示的に問う
2. **複数ファイルを跨ぐ変更・重要文書の変更の場合は、push 内容をボスに事前提示してから実行**
3. **push 完了後はボスに「remote が先行しているので pull が必要」と明示通知**
4. **ボスから local 編集の予告がある場合は、Personal-Planner 側の push を保留してボスの作業完了を待つ**

本ルールは事故事例 2(マージコンフリクト発生)の直接的な対策として確立された。

---

### C. 事故事例の構造的記録(後任への参考)

本セッションで発生した 2 件の事故を、後任 Personal-Planner への参考情報として記録する。原則化や規範化はしない。

#### 事故事例 1: text モード投入の途中切れ

**発生**: 2 代目 Personal-Planner が初回投入で `source_type: text` を選択し、本文を直接ペーストする形で source_add を呼び出した際、本文末尾が「歴代」で途中切れになり、補遺セクション全体(Rex 0:19 後半 / ボス farewell / Rex 0:51)が欠落していた。

**検出**: 投入実行直前にボスから「.md 統一の方が良いか」の確認質問があり、その流れで text モードの脆弱性が顕在化。投入は中止された。

**構造的教訓(個人的気づき)**:
- text モードはペースト時の文字数制限・エスケープ処理・コピー範囲ミスなど、データ完全性を構造的に保証できない
- file モードはファイル本体を直接アップロードするため、ファイル整合性が自動的に保証される
- 一次資料保護の観点では、データ完全性の構造的保証は必須(編集禁止原則を満たすには、転記時点での完全性が前提)

#### 事故事例 2: マージマーカー残置(2 段階)

**発生**: Personal-Planner が事前確認なしに 3 ファイル push を実行(commit `3c2773c`)。同時並行でボスが local に手動配置した .md と衝突し、ボスの `git pull` 時にマージコンフリクトが発生。ボスがコンフリクト解決作業を実施したが、第 1 回再 push(commit `c8ced8b3`)で `<<<<<<< HEAD` `=======` `>>>>>>>` の 3 種類のマーカーがすべて未削除のまま push された(28,753 bytes)。

**検出**: NLM 投入直前に Personal-Planner が local file を読み込み、コンフリクトマーカー 3 種すべてが残存していることを発見。GitHub side も同状態であることを確認。

**第 2 段階**: ボスが `<<<<<<< HEAD` と `>>>>>>> 3c2773c9...` の 2 行を削除して再 push(commit `0589a4e6` / 28,546 bytes)したが、`=======` 行と両ブランチの本文重複が残った状態だった。Personal-Planner が GitHub side 確認で再度発見し、具体的な削除範囲を提示。

**第 3 段階(解決)**: ボスが両ブランチ重複と `=======` 行を完全削除して再 push(commit `30978a8` / 13,907 bytes)。Personal-Planner が GitHub + local 両方をクリーン状態と検証。投入実行可能となる。

**構造的教訓(個人的気づき)**:
- Personal-Planner が GitHub MCP push する前にボス local 作業状態を確認しなかったことが根本原因
- ボスのマージ作業に対する Personal-Planner の事前指示が不足していた(「マーカー 3 種すべて削除 + 不採用版の本文も削除」と具体的に伝えるべきだった)
- 事故検出ポイントが NLM 投入直前にあったことは、dialogues/ サブ層の一次資料保護原則(編集禁止・file モード)が構造的に機能した証拠と言える ─ 運用ルールが緩ければ破損ファイルが Personal_Brain に永続保管されていた可能性がある
- 二度の事故とも投入前に検出できたのは、複数経路(filesystem MCP + GitHub MCP)での独立検証が機能したため

---

### D. 本追記の位置付けについて(自己警戒)

本追記は **2 代目 Personal-Planner の個人的気づきの記録** であり、後任への規範化・行動強制を意図しない。8 代目統括 Evaluator が `philosophy/evaluator_code.md` で確立した「気づきメモ」の性質と整合させる。

後任 Personal-Planner が:
- 同じ運用ルール(.md 統一・file モード)を採用するか
- 同じ事故を踏むか
- 同じ気づきに到達するか

は未定。本追記は「2026-04-30 時点で 2 代目 Personal-Planner がこういう判断と検出をした」という事実記録であり、判断の正しさを保証するものではない。

ADR-Role v5 改訂時(personal/ 各層への distilled 抽出作業完了後の Wrap-Up)に、本追記内容の構造化・整理が再評価される。

---

*追記者: 2 代目 Personal-Planner (Wiki-Personal / Opus 4.7) / 2026-04-30*
*追記許可: ボス手動承認(2026-04-30)*
*位置付け: 暫定記録(_RUNBOOK v3 改訂時に再構成可)*
*関連: `wiki/pending/personal/2026-04-29_dialogues_sublayer_addition.md`(本サブ層起票文書)*
*関連: `wiki/personal/dialogues/2026-04-29_general_thread.md`(初回事例・dialogues/ サブ層)*
*関連: `wiki/philosophy/evaluator_code.md`(気づきメモ性質の参考)*
