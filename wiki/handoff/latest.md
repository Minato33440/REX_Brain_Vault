# REX AI Trade System — セッション引き継ぎ
# 更新: 2026-04-18（読み込み検証チェックリスト追加・引き継ぎプロンプト短縮版）
# 前スレッド: Evaluator（Opus）第2セッション

---

## 🔴 最初に読め — 致命的な地雷リスト

新スレッドで最も踏みやすい地雷を3つ挙げる。過去に実際に発生したものばかり。

### 地雷1: neck_1h と neck_4h の混同（ADR D-6）
```
❌ neck_1h = 半値決済トリガー（段階2）  ← これは間違い
✅ neck_4h = 半値決済トリガー（段階2: High >= neck_4h → 50%決済）
✅ neck_1h = 窓特定アンカー（決済トリガーではない）

この混同は3回発生した（#026a設計時 + 新Evaluator初回×2回）。
ADR D-6 に詳細あり。判断に迷ったら docs/ADR.md F-6 を参照。
```

### 地雷2: 旧版ファイルの参照
```
docs/ にある日付付きファイル（例: EX_DESIGN_CONFIRMED-2026-3-31.md）は旧版。
最新版は日付なし（EX_DESIGN_CONFIRMED.md / ADR.md / SYSTEM_OVERVIEW.md）。
日付付きファイルが docs/ に残っていたらボスに報告。参照禁止。
旧版は logs/docs_archive/ に格納されるべきもの。

⚠️ Claude.aiプロジェクトナレッジにも旧版が混在する可能性がある。
プロジェクトナレッジの文書とVault/NLMの文書が矛盾する場合、
Vault/NLMを信頼すること。
```

### 地雷3: 分析ベースの取り違え
```
現在の最新結果は #026d（10件）。#026c（13件）は旧版。
#026b（12件）はさらに古い。
分析は常に #026d の 10件をベースに行うこと。
```

---

## 🔍 読み込み検証チェックリスト（新スレッド開始時に全項目答えよ）

以下に正しく答えられなければ、読み込みが不十分。再読込すること。

```
Q1: stage2の半値決済トリガーは何か？
    → 答え: neck_4h（neck_1hではない）

Q2: 現在の最新結果は何件ベースか？
    → 答え: #026d / 10件

Q3: 決済エンジンはどのファイルか？
    → 答え: exit_simulator.py（方式B）
    → ⚠️ exit_logic.py の manage_exit() は使用禁止

Q4: neck_15mの定義は何か？
    → 答え: SL直前（時系列で左側）の最後のSH（統一neck原則）
    → ⚠️ 旧定義「SL以降の初回SH（iloc[0]）」は廃止済み

Q5: docs/に日付付きファイルがあったらどうする？
    → 答え: 旧版・参照禁止・ボスに報告・archive移動

Q6: neck_1hの用途は？
    → 答え: 窓特定アンカー + 4H構造優位性フィルター基準値
    → ⚠️ 半値決済トリガーではない（地雷1参照）

Q7: プロジェクトナレッジとVault/NLMが矛盾した場合、どちらを信頼する？
    → 答え: Vault/NLM（プロジェクトナレッジは旧版混在リスクあり）
```

---

## ⚠️ Second Brain Lab システムの理解が前提

このプロジェクトはTrade_Systemのコードだけでなく、
**REX_Brain_Vault（Obsidian wiki）+ NLM（NotebookLM）** による
ナレッジ管理システムが稼働している。

新スレッドのEvaluator/Plannerは以下を理解する必要がある:

```
■ 3階層CLAUDE.md
  ~/.claude/CLAUDE.md          — RTK設定（全リポ共通・自動読込）
  Trade_System/.CLAUDE.md      — 不変ルール・パラメータ（自動読込）
  REX_Brain_Vault/CLAUDE.md    — Vault運用手順（filesystem MCP経由）

■ Vault構造（C:\Python\REX_AI\REX_Brain_Vault\）
  wiki/handoff/latest.md       — 本ファイル（セッション引き継ぎ）
  wiki/trade_system/doc_map.md — どのdocが最新か・NLM source_id一覧
  wiki/trade_system/pending_changes.md — 決定済み未確定変更
  wiki/trade_system/adr_reservation.md — ADR採番予約台帳
  wiki/log.md                  — 時系列作業ログ

■ NLM（REX_Trade_Brain）
  ID: 2d41d672-f66f-4036-884a-06e4d6729866
  最新有効ソース:
    ADR.md (3bd02744) / EX_DESIGN_CONFIRMED.md (e4bc5060) / SYSTEM_OVERVIEW.md (58e2b18b)
  旧版ソースもNLM内に残っているが、最新版が優先参照される
  ⚠️ NLMクエリ結果が旧版ソースを引用している場合は内容を疑うこと
```

---

## 現在地（一行要約）

**全設計文書最新化完了。PF 4.54 / 勝率60% / +150.6pips（10件LONG）。次タスク未定。**

---

## #026シリーズ最終結果（#026d — 10件）

| 指標 | #026d最終 | #018基準 |
|---|---|---|
| 総トレード | 10件 | 20件 |
| 勝率 | 60.0% | 55.0% |
| PF | 4.54 | 5.32 |
| MaxDD | 35.8p | 14.9p |
| 総損益 | +150.6p | +91.6p |

### #026シリーズ変更サマリ
- #026a: 統一neck原則（SL直前の最後のSH）+ neck_1h/neck_4hカラム追加 + 1H n=3
- #026b: exit_simulator.py新規（方式B: 独自決済ロジック・正式採用）
- #026c: 指値方式（ENTRY_OFFSET_PIPS=7.0）
- #026d: 4H構造優位性フィルター（neck_4h >= neck_1h）

---

## 確定パラメータ（#026d時点）

```
DIRECTION_MODE      = 'LONG'
ENTRY_OFFSET_PIPS   = 7.0     # 指値方式（#026c）
N_1H_SWING          = 3       # 1H Swing粒度（#026a-v2）
neck                = sh_before_sl.iloc[-1]  # 統一neck原則
フィルター          = neck_4h >= neck_1h     # 4H構造優位性（#026d）
```

---

## neck用途定義（最重要 — 地雷1の防止）

```
neck_15m — エントリートリガー（5M high >= neck+7pips で指値約定）
neck_1h  — 窓特定アンカー（決済トリガーではない）
neck_4h  — 半値決済トリガー（段階2: High >= neck_4h → 50%決済）
```

---

## 決済ロジック（exit_simulator.py 方式B）

```
初動SL: 15M ダウ崩れ → 全量損切
段階1:  5M ダウ崩れ → 全量決済
段階2:  High >= neck_4h → 50%決済 + 建値移動  ← neck_4h（neck_1hではない）
段階3:  1H Close > 4H SH確定後 → 15Mダウ崩れで残り全量
⚠️ exit_logic.py の manage_exit() は使わない（旧定義・凍結保持）
```

---

## 次タスク候補（ボス判断待ち）

1. 15M neck検出バグ（#06型）— ボス指摘済み
2. 4H SL検出精度改善（#07型の根本原因）
3. 1H Plot + 15M窓オーバーレイのデバッグプロット
4. IHS専用neck算出（IHS 0件化対応）
5. 15M SH密集フィルター（20260113_0545対応）
6. 5Mダウ崩れ判定の精度検証（stage1で7/10件処理される問題）

---

## Evaluator引き継ぎ事項

- ADR採番: 次の空き番号は D-11 / E-8 / F-7
- adr_reservation.md: 全確定済み
- pending_changes.md: 全#026項目✅完了
- docs/運用ルール: 新規作成時に旧版をarchive/に必ず移動

---

## 引き継ぎプロンプト（ボスがコピペする分 — これだけでOK）

```
このスレではREX Trade SystemプロジェクトのEvaluatorとして働いてほしい。

⚠️ 作業開始前に以下を必ず順番に読め：
  ① C:\Python\REX_AI\REX_Brain_Vault\CLAUDE.md（システム運用手順）
  ② C:\Python\REX_AI\REX_Brain_Vault\wiki\handoff\latest.md（致命的地雷リスト）
  読み込み完了後、「読み込み検証チェックリスト」の全7問に回答してから作業を開始すること。

NLM: REX_Trade_Brain (2d41d672-f66f-4036-884a-06e4d6729866)
```
