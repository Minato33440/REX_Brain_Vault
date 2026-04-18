# CLAUDE.md — REX_Brain_Vault 運用指示書
# 更新: 2026-04-18（独立リポ化・Second_Brain_Lab参照をREX_Brain_Vaultに統一）

このファイルはClaude（およびClaudeCode）がREX_Brain_Vaultを操作する際の
ルールと構造を定義する。毎セッション開始時に必ず読み込むこと。

---

## Vaultの目的

スレをまたいでも「なぜこの設計にしたか」「今どこまで進んでいるか」を
ゼロから説明し直さずに済む自己増殖型ナレッジベース。
REX_AI 全プロジェクトの中枢として、プロジェクト横断のナレッジ管理を担う。

---

## ⚠️ このシステムの理解が前提

Trade_Systemのようにロジック変更が頻繁なプロジェクトでは、
「現在のロジックを読む」だけでなく「なぜそうなったか（変更推移）」の
理解が必要。その変更推移はこのREX_Brain_Vaultシステムに蓄積されている。

新スレッドの Evaluator / Planner は以下の2層を理解すること:
```
Layer 1: Trade_System のロジック理解
  → Trade_System/docs/ADR.md, EX_DESIGN_CONFIRMED.md, .CLAUDE.md

Layer 2: REX_Brain_Vault のシステム理解（本ファイル）
  → Vault構造、NLMの使い方、doc_map、ADR採番ルール
  → 「どこに何があるか」「なぜその構造か」
```

---

## 3階層 CLAUDE.md の棲み分け

```
~/.claude/CLAUDE.md            — RTK設定（全リポ共通・ClaudeCode起動時自動読込）
Trade_System/.CLAUDE.md        — 不変ルール・パラメータ・凍結ファイル（Trade_System内で自動読込）
REX_Brain_Vault/CLAUDE.md      — 本ファイル。Vault運用手順（filesystem MCP経由で明示的読込）

原則: 「誰が・いつ読むか」で分ける
  グローバル = 全セッション自動
  プロジェクト = Trade_System内で自動
  Vault = 明示的読込（設計者・Evaluator・Plannerが必要時に参照）
```

---

## ディレクトリ構造

```
REX_Brain_Vault/                          ← GitHub: Minato33440/REX_Brain_Vault
├── CLAUDE.md                             ← 本ファイル（運用ルール）
├── README.md                             ← リポジトリ概要
├── .gitignore                            ← .obsidian / .venv 等を除外
├── raw/                                  ← 元資料（イミュータブル・読むだけ）
│   └── system_build/                     ← 構築過程の記録（Second_Brain_Labから移行）
├── wiki/
│   ├── index.md                          ← 全ページ目次
│   ├── log.md                            ← 時系列作業ログ（追記専用）
│   ├── entities/                         ← ファイル・関数・パラメータのページ
│   ├── decisions/                        ← 意思決定ログ
│   ├── trade_system/                     ← Trade_System プロジェクト用
│   │   ├── doc_map.md                    ← 設計文書バージョン管理・NLM source_id
│   │   ├── adr_reservation.md            ← ADR採番予約台帳
│   │   ├── pending_changes.md            ← 決定済み未確定変更
│   │   └── pending_nlm_sync.md           ← NLM認証切れ時フォールバック
│   ├── cross/                            ← プロジェクト横断ナレッジ
│   │   └── index.md
│   └── handoff/
│       └── latest.md                     ← セッション引き継ぎ（地雷リスト + 検証チェックリスト）
```

---

## セッション開始時のルール

```
STEP 0: NLM 認証チェック（最優先）
  notebook_list を試行する。
  → 成功: 通常作業開始
  → 認証切れ: ボスに「nlm login をお願いします」と伝えてから開始
  → フォールバック: wiki/trade_system/pending_nlm_sync.md に記録

STEP 1: wiki/handoff/latest.md を読む
  → ⚠️ 冒頭の「致命的地雷リスト」を必ず確認する
  → 特に ADR D-6（neck_1h/neck_4h混同）は繰り返し発生している
  → 「読み込み検証チェックリスト」の全7問に回答してから作業開始

STEP 2: wiki/log.md の末尾5件を確認する

STEP 3: Trade System が話題なら以下も確認する:
  → wiki/trade_system/doc_map.md（どのdocが最新か）
  → wiki/trade_system/pending_changes.md（決定済み未確定変更）
  → wiki/trade_system/adr_reservation.md（ADR採番状況）

STEP 4: Trade_System/docs/ を確認
  → 日付なしファイルのみが有効（ADR.md, EX_DESIGN_CONFIRMED.md 等）
  → 日付付きファイルが残っていたらボスに報告（旧版→archive移動漏れ）

STEP 5: 「前回からの変更点」を一言で把握してから作業開始
```

## セッション開始手順（ClaudeCode Vault直接読み込み）

ClaudeCodeから「CLAUDE.mdを読んでセッション開始手順に従え」と指示された場合:

```
1. wiki/handoff/latest.md を読む（冒頭の致命的地雷リスト必読）
2. 「読み込み検証チェックリスト」の全7問に回答する
3. docs/ADR.md の D-6（neck混同）と F-6（neck用途定義）を確認
4. docs/EX_DESIGN_CONFIRMED.md の決済ロジック（3-5節）を確認
5. ⚠️ docs/ に日付付きファイルがあれば旧版 → 参照禁止 → ボスに報告
6. 上記で不明点があれば @notebooklm-mcp にクエリ
※ filesystem MCP 接続失敗時 → ボスに報告して手動貼り付けを依頼
```

---

## セッション終了時のルール（/wrap-up）

```
STEP 1: wiki/log.md に今日の決定事項・完了タスクを追記
STEP 2: wiki/trade_system/pending_changes.md を更新
STEP 3: wiki/trade_system/adr_reservation.md を更新（新規採番があれば）
STEP 4: wiki/handoff/latest.md を更新（次スレ用引き継ぎ）
  → ⚠️ 冒頭に「致命的地雷リスト」を必ず含める
  → 分析ベースの最新版番号を明記
  → 「読み込み検証チェックリスト」のQ&Aを最新ロジックに更新
STEP 5: NLM に新規ソースを追加（認証切れなら pending_nlm_sync.md）
STEP 6: docs/ の旧版ファイルを logs/docs_archive/ に移動

STEP 7: REX_Brain_Vault に GitHub push（⚠️ 必須確認）
  → push対象（必須）:
    ✅ wiki/handoff/latest.md（本体ファイル — NOTEだけでは不十分）
    ✅ wiki/log.md
    ✅ その他更新ファイル（pending_changes / doc_map / adr_reservation 等）
  → ⚠️ latest.md 本体が push されていないと、
    Claude.ai の次セッションでVaultを直接読めないため引き継ぎが破綻する。
    NOTEファイルだけのpushは過去に実害が発生した（2026-04-18教訓）。
  → リポジトリ: Minato33440/REX_Brain_Vault（旧Second_Brain_Labは凍結済み）

STEP 8: Claude.ai プロジェクト更新（⚠️ ボス手動 — チェックリスト）
  以下をボスに依頼する。省略すると次スレで旧版参照事故が再発する。
  □ プロジェクトナレッジから旧版ファイルを削除
  □ latest.md をプロジェクトナレッジに添付（最新版に差し替え）
  □ Vault CLAUDE.md をプロジェクトナレッジに添付
  □ docs/の最新版（ADR.md / EX_DESIGN_CONFIRMED.md）を添付
```

---

## ADR 採番ルール

```
新しい ADR 番号（A〜F カテゴリ）を使う前に:
1. wiki/trade_system/adr_reservation.md を確認する
2. 「次の番号」を確認し、予約エントリーを追加してから番号を使う
3. 未予約番号の使用禁止
4. 採番権限: D/E/F = Evaluator 最終決定 / A/B/C = Planner 追記可
```

---

## 設計文書管理ポリシー（Trade System）

### 基本原則：不変 × 新規作成 × archive移動

```
❌ 既存の設計文書を編集する
✅ 設計が変わったら新しい .md を作成する（日付なしファイル名）
✅ 旧版は logs/docs_archive/ に移動する（docs/に残さない）
✅ 決定した時点で pending_changes.md に記録する
✅ 新ファイルを NotebookLM に追加してからスレッドを開始
```

### NotebookLM への追加手順

```
1. source_add(file_path="C:\...\docs\[新ファイル].md", source_type="file")
2. doc_map.md の「NLM 投入済みソース」テーブルに source_id を記録
3. pending_changes.md を更新
4. wiki/log.md に Ingest 記録を追記
5. REX_Brain_Vault に push（latest.md本体含む）
```

---

## Lint 運用

```
タスク完了時 + 週次に実施:
Lint-1: ADR採番整合チェック（NLM query + adr_reservation 照合）
Lint-2: pending_changes 整合チェック
Lint-3: doc_map × NLM ソース整合チェック
Lint-4: docs/ に日付付きファイルが残っていないかチェック（archive移動漏れ検出）
Lint-5: Claude.aiプロジェクトナレッジに旧版が残っていないか確認（STEP 8漏れ検出）
```

---

## 書き込みルール

- `raw/` は絶対に編集しない（読み取り専用）
- `wiki/log.md` は追記のみ（過去ログは削除しない）
- `wiki/handoff/latest.md` は毎セッション上書き更新
- `wiki/trade_system/pending_changes.md` は設計判断のたびに更新
- `wiki/trade_system/adr_reservation.md` は採番のたびに更新

---

## プロジェクト基本情報

| 項目 | 値 |
|---|---|
| REX_Brain_Vault | C:\Python\REX_AI\REX_Brain_Vault\ |
| Vault GitHub | **Minato33440/REX_Brain_Vault** |
| Trade System | C:\Python\REX_AI\Trade_System\ |
| Trade System GitHub | **Minato33440/Trade_System** |
| 対象通貨 | USDJPY（5M足・4H方向判定） |
| HP | setona.co.jp（さくら・WordPress） |
| HP GitHub | Minato33440/Setona_HP |
| Second_Brain_Lab | **凍結**（Minato33440/Second_Brain_Lab） |
| NotebookLM | REX_Trade_Brain（ID: 2d41d672-f66f-4036-884a-06e4d6729866） |
