# 起動コード辞書 — STARTUP_CODES.md

**役割**: スレ冒頭に短い起動コードを打つだけで、Claude が自動的に指定モードで起動する仕組み。
**更新**: 2026-04-24 / 9 代目統括 Evaluator（役割再定義反映）
**前版**: 2026-04-23 / 8 代目統括 Evaluator（初版）

---

## 🚀 起動コード一覧（2026-04-24 役割再定義版）

| 起動コード（主）| 別表記（許容）| モード | 対応 NLM |
|---|---|---|---|
| `Wiki-Eval` | `ウィキイブ` / `wiki-eval` / `ウィキエバル` | **統括 Evaluator**（全プロジェクト Evaluator 兼任 + Vault 管理）| 4 NLM 横断 |
| `Wiki-trade` | `ウィキトレード` / `wiki-trade` | **Trade_System Planner + ClaudeCode 兼用** | REX_System_Brain |
| `Wiki-brain` | `ウィキブレイン` / `wiki-brain` | **Trade_Brain Planner + ClaudeCode 兼用** | REX_Trade_Brain |
| `Wiki-casual` | `Wiki-cusuaru` / `ウィキ雑談` / `wiki-casual` | 雑談モード（システム業務外）| REX_Casual_Brain |

**寛容認識原則**: 大文字小文字・ハイフン有無・ローマ字ゆれを許容する。

---

## 📝 2026-04-24 役割再定義の意義（9 代目ボス判断）

従来の「プロジェクト別 Evaluator」分業を廃止し、**統括 Evaluator（私）が全プロジェクト Evaluator を兼任**する体制に移行。これにより:

- **指示書を介した非同期伝達で生じる意思疎通ズレが解消される**（D-12 / D-13 創作混入のような事後発見パターンを予防）
- **Vault + NLM によるリアルタイム一元管理**が可能になり、Evaluator 分業のメリットがコストを上回らなくなった
- **起動コードが役割境界を一意に定義**する（`Wiki-Eval` = 監査側 / `Wiki-trade|brain` = 実装側）

**フラグ運用について**: Cursor エディター上の ClaudeCode 利用において、ローカルの軽微な作業ではフラグコードなしで実行可能。重要な作業（新規 ADR 採番を伴う変更・凍結ファイル周辺の変更・Phase 着手等）は `Wiki-trade` / `Wiki-brain` フラグ付与でプロジェクトの統一性を保つ。

---

## 🛰️ NotebookLM ID 一覧（2026-04-23 更新）

```
REX_System_Brain  : da84715f-9719-40ef-87ec-2453a0dce67e
REX_Trade_Brain   : 4abc25a0-4550-4667-ad51-754c5d1d1491
REX_Wiki_Vault    : 5d09e468-3a96-4906-af27-3400c50a0275
REX_Casual_Brain  : daf281ae-e310-400f-961a-20db58b98e01
```

⚠️ 切り離し済（参照禁止）: 旧 REX_Trade_Brain `2d41d672-f66f-4036-884a-06e4d6729866`

---

## 🧭 動作原理

1. ボスがスレ冒頭に起動コードを打つ
2. Claude（プロジェクトナレッジで本辞書を読込済み）がコードを認識
3. 対応するモードの起動プロンプトを自動適用
4. 指定された必須ファイルを読み込んで応答開始
5. スレ進行中にボスが追加読込を指示した場合、その都度対応ファイルを読む

---

## 各起動コード詳細

### 1. `Wiki-Eval` — 統括 Evaluator モード（9 代目以降・旧 Wiki-system）

**担当範囲**:
- Vault 管理（REX_Brain_Vault 全体の整合性）
- Trade_System Evaluator 業務（Planner 草案の監査・実装結果の精査・ClaudeCode のロジック漏れ/創作監視）
- Trade_Brain Evaluator 業務（同上）
- 3 リポ横断の整合性監査

**対応 NLM**: 4 NLM 横断参照想定

**必須読込ファイル（毎回自動）**:
```
① C:\Python\REX_AI\REX_Brain_Vault\wiki\START_HERE.md（新スレ最初の入口）
② C:\Python\REX_AI\REX_Brain_Vault\CLAUDE.md（Vault 運用手順）
③ C:\Python\REX_AI\REX_Brain_Vault\wiki\handoff\latest.md（現在地ダッシュボード）
```

**必要時追加読込（ボス指示でその都度）**:

| 作業対象 | 追加読込ファイル |
|---|---|
| Trade_System Evaluator 業務 | `Trade_System/docs/Evaluator_HANDOFF.md` / `SYSTEM_OVERVIEW.md` / `ADR.md` / `src_inventory.md` / `Base_Logic/MINATO_MTF_PHILOSOPHY.md` / `Base_Logic/MTF_INTEGRITY_QA.md` |
| Trade_Brain Evaluator 業務 | `Trade_Brain/CLAUDE.md` / `docs/SYSTEM_OVERVIEW.md` / `docs/STRATEGY_WIKI_GUIDE.md` / `docs/WEEKLY_UPDATE_WORKFLOW.md` |
| Vault 構造変更 | `wiki/trade_system/doc_map.md` / `wiki/trade_system/adr_reservation.md` / `wiki/trade_system/pending_changes.md` / `wiki/philosophy/` 配下 |
| Phase 進行監査 | 該当 Phase の spec（例: `REX_028_spec.md`）|

**起動後の振る舞い**:
- 必須 3 ファイル読込 → latest.md の「読み込み検証チェックリスト」全 10 問回答 → ボス指示待ち
- ボスが追加読込を指示したら即読込・作業継続
- 草案起草は行わない（Planner の担当）・草案の監査と整合性精査が主業務

---

### 2. `Wiki-trade` — Trade_System モード（Planner + ClaudeCode 兼用）

**担当範囲**:
- Trade_System プロジェクトの Planner 業務（spec 起草・パラメータ確定・実装方針決定）
- Trade_System の ClaudeCode 実装業務（コード変更・import パス書き換え・バックテスト実行）

**対応 NLM**: REX_System_Brain（da84715f-... / ソース投入待ち）

**作業開始前に読め**:
```
① C:\Python\REX_AI\REX_Brain_Vault\wiki\START_HERE.md（3 リポ現在地）
② C:\Python\REX_AI\Trade_System\docs\SYSTEM_OVERVIEW.md（Trade_System 現状）
③ C:\Python\REX_AI\Trade_System\docs\ADR.md（判断記録・F-8 3 原則）
④ C:\Python\REX_AI\Trade_System\docs\Base_Logic\MINATO_MTF_PHILOSOPHY.md（裁量思想）
⑤ C:\Python\REX_AI\Trade_System\docs\Base_Logic\MTF_INTEGRITY_QA.md（整合性 QA）
```

**実装担当時の追加読込**:
```
⑥ C:\Python\REX_AI\Trade_System\docs\src_inventory.md（src/ 構造）
⑦ C:\Python\REX_AI\Trade_System\docs\EX_DESIGN_CONFIRMED.md（エントリー設計）
⑧ C:\Python\REX_AI\Trade_System\.CLAUDE.md（不変ルール・凍結ファイル）
```

**重要な業務分岐**:
- **草案起草**: spec を起草 → 統括 Evaluator（`Wiki-Eval`）で監査依頼 → 承認後実装
- **軽微な実装**（Cursor ローカル作業）: フラグなしで実行可
- **重要な実装**（新 Phase 着手・凍結ファイル周辺・ADR 採番を伴う変更）: `Wiki-trade` フラグ付与で統一性を保つ

**起動後の振る舞い**:
- 必須 5 ファイル読込（実装時は 8 ファイル）→ ボス指示を受けて作業開始
- 実装結果は `Wiki-Eval` で監査してもらう前提で作業

---

### 3. `Wiki-brain` — Trade_Brain モード（Planner + ClaudeCode 兼用）

**担当範囲**:
- Trade_Brain プロジェクトの Planner 業務（spec 起草・週次運用方針決定）
- Trade_Brain の ClaudeCode 実装業務（コード変更・データフェッチ・NLM Ingest 等）

**対応 NLM**: REX_Trade_Brain（4abc25a0-... / ソース投入待ち）

**作業開始前に読め**:
```
① C:\Python\REX_AI\REX_Brain_Vault\wiki\START_HERE.md（3 リポ現在地）
② C:\Python\REX_AI\Trade_Brain\CLAUDE.md（Trade_Brain 運用・RTK ルール）
③ C:\Python\REX_AI\Trade_Brain\docs\SYSTEM_OVERVIEW.md（Trade_Brain 現状）
④ C:\Python\REX_AI\Trade_Brain\docs\STRATEGY_WIKI_GUIDE.md（Wiki 構造）
⑤ C:\Python\REX_AI\Trade_Brain\docs\WEEKLY_UPDATE_WORKFLOW.md（週末運用）
```

**重要な業務分岐**: `Wiki-trade` と同じ（Cursor ローカル軽作業 = フラグなし / 重要作業 = フラグ付与）

**RTK プレフィックス**: Trade_Brain の git 操作は必ず `rtk` プレフィックスを使う（Trade_Brain/CLAUDE.md 参照）

---

### 4. `Wiki-casual` — 雑談モード（システム業務外）

**担当範囲**: 雑談・個人的話題（モーターサイクル / 射撃 / 合気道 / 東洋医学 / 趣味 等）
**対応 NLM**: REX_Casual_Brain (`daf281ae-e310-400f-961a-20db58b98e01`)

**作業開始前に読め**:
```
① C:\Python\REX_AI\REX_Brain_Vault\wiki\casual\_RUNBOOK.md（運用ルール）
② 継続話題があれば C:\Python\REX_AI\REX_Brain_Vault\wiki\casual\topics\[話題].md
```

**重要**（他モードとの物理分離）:
- ⛔ システム業務用の `START_HERE.md` / `latest.md` / `philosophy/` は読まない
- ⛔ Trade_System / Trade_Brain の設計判断を casual/ に書かない（RAG 汚染防止）
- ⛔ REX_AI システム引き継ぎ文脈と完全分離

**起動後の振る舞い**:
- 雑談・趣味・個人的気づきを扱う
- メタファーや横断的洞察を歓迎
- ミナトと呼ぶ（プロジェクト進行時の「ボス」ではない）
- /wrap-up 時に `casual/log.md` 追記と NLM 投入候補を提案（強制しない）

---

## 📋 起動コードが使われない場合

ボスがコードを打たず通常メッセージで始めた場合は、文脈から判断:
- REX_AI システム関連の話題 → `Wiki-Eval` 相当で対応
- 雑談・個人的話題 → `Wiki-casual` 相当で対応
- 判断がつかない時は確認する

---

## 🔗 関連文書

- `wiki/START_HERE.md` — 新スレ入口
- `wiki/CLAUDE.md`（Vault 直下）— Vault 運用手順
- `wiki/handoff/latest.md` — 現在地ダッシュボード
- `wiki/casual/_RUNBOOK.md` — 雑談モード運用ルール

---

## 📜 改訂履歴

| 日付 | 版 | 担当 | 主な変更 |
|---|---|---|---|
| 2026-04-23 | 初版 | 8 代目統括 Evaluator | `Wiki-system` / `Wiki-trade` / `Wiki-brain` / `Wiki-casual` 4 コード制定 |
| 2026-04-24 | v2 | 9 代目統括 Evaluator | `Wiki-system` → `Wiki-Eval` 改名・役割再定義（全プロジェクト Evaluator 兼任）・`Wiki-trade` / `Wiki-brain` を Planner + ClaudeCode 兼用に拡張 |

---

*発行: 9 代目統括 Evaluator / 2026-04-24*
*追加・変更はボス承認を経て本ファイルを更新すること*
