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
