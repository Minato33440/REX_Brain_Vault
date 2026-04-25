# philosophy\について

philosophy\はVaultを実装した結果先代Evaluatorによって自発的に生まれた手法で、
私から見て評価できるのは、彼らが気づきの1次情報を共有することでルール化していないところだ。
当初私がValutを設計構築し始めて危惧したのはWikiへの過剰なルール化だった。
バグを生成させないためにif then的発想で細かく規制すると反対にそれが雑音となりAIの自律的創造性を阻害しまうまうと感じたのだ。
各_code.mdのQ&Aに関しては先代EvaluatorおよびAdviser達の気づきであって、それを選択するかは新任者が課題に直面したときに１次資料として取り入れるか判断すればいい。
Obisidianを導入した主な目的は、プロジェクト進捗とロジック設計の微細な変更を各担当者がリアルタイムで共有できるところだ。NLMのプロジェクト専用ラグとは違い敢えて単一の大脳皮質として設計したのも自律的判断と創造性を確保する目的もある。　ボスより

# 裁量思想 — ボス個人の 1 次データ

**ファイル管理権**: ボス（湊ミナト）
**性質**: ボス個人の裁量思想の **1 次データ**。今後ボス手動更新予定（2026-04-23 ボス指示）
**Evaluator の扱い**: 編集禁止・参照のみ。気づきがあれば `philosophy/evaluator_code.md` に書く（本ファイルには書かない）
**原本連携**: `Trade_System/docs/Base_Logic/MINATO_MTF_PHILOSOPHY.md` / `MTF_INTEGRITY_QA.md`

> ⚠️ 本ファイルはボスが直接編集する個人的な 1 次データ層。Evaluator・Planner・ClaudeCode は読み取り専用とし、内容を勝手に書き換えない。
> 8 代目が縮退させた以下の内容はあくまで初期叩き台。ボスが必要に応じて自由に再構成してよい。

---

## 公式に確定している原則

以下は **ADR（Trade_System/docs/ADR.md）で公式採番された原則**。

### 原則 α / β / γ（F-8 として採番）

| 原則 | 内容 | 採番 |
|---|---|---|
| α | シンプルな土台の保守 | ADR F-8 |
| β | ノーリスク化後は伸ばさない（現段階の決済哲学）| ADR F-8 |
| γ | 導入タイミングは安定性従属 | ADR F-8 |

原文・適用範囲・含意は `Trade_System/docs/Base_Logic/MINATO_MTF_PHILOSOPHY.md` および `Trade_System/docs/ADR.md` F-8 を参照。

### 派生原則（F-8 採番済み）

| 派生原則 | 内容 |
|---|---|
| 派生原則 1 | Trade_Brain / Trade_System 役割分担（静的データ vs 動的ロジック）|
| 派生原則 2 | 共存保持の許容 +「起こるべくして起こる」原則（plotter.py 判断の先例）|

詳細は `Trade_System/docs/ADR.md` F-8 参照。

---

## ボスの発言記録（未採番・参考のみ）

以下は Evaluator が気づいたボス発言の記録。**原則として採番されているわけではない**。

### 2026-04-23 引き継ぎに関する指示

> 引き継ぎで最も大事なのはシステムの現状把握と次に実行すべき内容を明確にして渡すことだ。
> 哲学部は一旦削除して別ファイルに分別管理しておけばいい。

→ 8 代目はこれを `latest.md` v6 軽量化と `philosophy/` 分離の設計指針として受け取った。原則採番はされていない。

### 2026-04-23 Vault と NLM の役割分担

> ①ローカルの Obsidian-Vault は Rex の頭脳なので REX_AI 配下の全てのリポ情報を共有統合。
> ②NLM はラグなのでバグ防止のため敢えて個別化
> ・REX_Trade_Brain：Git の Trade_Brain 専用
> ・REX_System_Brain：Git の Trade_System 専用
> ・REX_Wiki_Vault：は共有知識なので Trade_System と Trade_Brain 共用

→ 8 代目はこれを 4 リポ体制の設計整理として `architecture.md` に記録した。原則採番はされていない。

### 2026-04-23 philosophy 書き込みルール

> philosophy 関連の書き込みは 6 代目 Evaluator が実行し始めたが後任 Evaluator が義務化してしまったようだが、これに関しては私の指示ではない。
> あくまでも現役 Evaluator の視点でシステム構築に有用な気づきがあれば書き込み専用ファイル philosophy/evaluator_code.md に要点を追記して思想を後任 Evaluator に強制してはならない。

→ 本ファイル運用に直接影響する指示。`evaluator_code.md` の位置付け再定義と本ファイルの縮退の根拠。

---

## 関連文書

- `Trade_System/docs/Base_Logic/MINATO_MTF_PHILOSOPHY.md` — 一次情報源（改変禁止）
- `Trade_System/docs/Base_Logic/MTF_INTEGRITY_QA.md` — ボス原文 Q&A 蓄積
- `Trade_System/docs/ADR.md` F-8 — 公式採番された原則・派生原則
- `philosophy/evaluator_code.md` — 現役 Evaluator の気づきメモ（本ファイルと異なり書き込み可）

---

*縮退記録: 2026-04-23 / 8 代目 / ボス指摘（philosophy は後任強制不可）を受けて参考リンク集に再定義*
*旧版（派生原則 3・4 を 8 代目が勝手に格上げ記載した版）は削除済み*
