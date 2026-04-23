# 起動コード辞書 — STARTUP_CODES.md

**役割**: スレ冒頭に短い起動コードを打つだけで、Claude が自動的に指定モードで起動する仕組み。
**更新**: 2026-04-23 / 8 代目統括 Evaluator

---

## 🚀 起動コード一覧

| 起動コード（主）| 別表記（許容）| モード | 対応 NLM |
|---|---|---|---|
| `Wiki-system` | `ウィキシステム` / `wiki-system` | 統括 Evaluator | 4 NLM 横断 |
| `Wiki-trade` | `ウィキトレード` / `wiki-trade` | Trade_System Planner / Evaluator | REX_System_Brain |
| `Wiki-brain` | `ウィキブレイン` / `wiki-brain` | Trade_Brain Planner / ClaudeCode | REX_Trade_Brain |
| `Wiki-casual` | `Wiki-cusuaru` / `ウィキ雑談` / `wiki-casual` | 雑談モード（システム業務外）| REX_Casual_Brain |

**寛容認識原則**: 大文字小文字・ハイフン有無・ローマ字ゆれ（casual / cusuaru / カジュアル）を許容する。

---

## 🛰️ NotebookLM ID 一覧（2026-04-23 更新）

```
REX_System_Brain  : da84715f-9719-40ef-87ec-2453a0dce67e
REX_Trade_Brain   : 4abc25a0-4550-4667-ad51-754c5d1d1491
REX_Wiki_Vault    : 5d09e468-3a96-4906-af27-3400c50a0275  🆕 2026-04-23 設立
REX_Casual_Brain  : daf281ae-e310-400f-961a-20db58b98e01  🆕 2026-04-23 設立
```

⚠️ 切り離し済（参照禁止）: 旧 REX_Trade_Brain `2d41d672-f66f-4036-884a-06e4d6729866`

---

## 🧭 動作原理

1. ボスがスレ冒頭に起動コードを打つ
2. Claude（プロジェクトナレッジで本辞書を読込済み）がコードを認識
3. 対応するモードの起動プロンプトを自動適用
4. 指定ファイルを読み込んで応答開始

---

## 各起動コード詳細

### 1. `Wiki-system` — 統括 Evaluator モード

**担当範囲**: Trade_System / Trade_Brain / Rex_Brain_Vault の整合性監査
**対応 NLM**: 4 NLM 横断参照想定（現在 3 つは凍結中・REX_Casual_Brain のみ使用可）

**作業開始前に読め**:
```
① C:\Python\REX_AI\REX_Brain_Vault\wiki\START_HERE.md
② C:\Python\REX_AI\REX_Brain_Vault\CLAUDE.md
③ C:\Python\REX_AI\REX_Brain_Vault\wiki\handoff\latest.md
```

読み込み完了後、latest.md の「読み込み検証チェックリスト」全 10 問に回答してから開始。

---

### 2. `Wiki-trade` — Trade_System モード

**担当範囲**: Trade_System プロジェクトの Planner または Evaluator
**対応 NLM**: REX_System_Brain（凍結中・クエリ不可）

**作業開始前に読め**:
```
① C:\Python\REX_AI\REX_Brain_Vault\wiki\START_HERE.md
② C:\Python\REX_AI\Trade_System\docs\SYSTEM_OVERVIEW.md
③ C:\Python\REX_AI\Trade_System\docs\ADR.md
④ C:\Python\REX_AI\Trade_System\docs\Base_Logic\MINATO_MTF_PHILOSOPHY.md
⑤ C:\Python\REX_AI\Trade_System\docs\Base_Logic\MTF_INTEGRITY_QA.md
```

---

### 3. `Wiki-brain` — Trade_Brain モード

**担当範囲**: Trade_Brain プロジェクトの Planner または ClaudeCode
**対応 NLM**: REX_Trade_Brain（凍結中・クエリ不可）
**注意**: 統括 Evaluator は Trade_Brain に関与しない（役割分担）

**作業開始前に読め**:
```
① C:\Python\REX_AI\REX_Brain_Vault\wiki\START_HERE.md
② C:\Python\REX_AI\Trade_Brain\CLAUDE.md（RTK ルール）
③ C:\Python\REX_AI\Trade_Brain\docs\SYSTEM_OVERVIEW.md
④ C:\Python\REX_AI\Trade_Brain\docs\STRATEGY_WIKI_GUIDE.md
⑤ C:\Python\REX_AI\Trade_Brain\docs\WEEKLY_UPDATE_WORKFLOW.md
```

---

### 4. `Wiki-casual` — 雑談モード（システム業務外）

**担当範囲**: 雑談・個人的話題（モーターサイクル / 射撃 / 合気道 / 東洋医学 / 趣味 等）
**対応 NLM**: REX_Casual_Brain (`daf281ae-e310-400f-961a-20db58b98e01`)

**作業開始前に読め**:
```
① C:\Python\REX_AI\REX_Brain_Vault\wiki\casual\_RUNBOOK.md
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
- REX_AI システム関連の話題 → `Wiki-system` 相当で対応
- 雑談・個人的話題 → `Wiki-casual` 相当で対応
- 判断がつかない時は確認する

---

## 🔗 関連文書

- `wiki/START_HERE.md` — 新スレ入口
- `wiki/CLAUDE.md`（Vault 直下）— Vault 運用手順
- `wiki/handoff/latest.md` — 現在地ダッシュボード
- `wiki/casual/_RUNBOOK.md` — 雑談モード運用ルール

---

*発行: 8 代目統括 Evaluator / 2026-04-23*
*追加・変更はボス承認を経て本ファイルを更新すること*
