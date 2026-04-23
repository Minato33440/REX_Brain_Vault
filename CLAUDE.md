# CLAUDE.md — REX_Brain_Vault 運用指示書
# 更新: 2026-04-23（8 代目 Phase A' 拡張完了・NLM 4 本体制・起動コード辞書・casual/ 層新設）
# 前版: 2026-04-18（独立リポ化・Second_Brain_Lab参照を REX_Brain_Vault に統一）

このファイルは Claude（および ClaudeCode）が REX_Brain_Vault を操作する際の
ルールと構造を定義する。毎セッション開始時に必ず読み込むこと。

---

## Vault の目的

スレをまたいでも「なぜこの設計にしたか」「今どこまで進んでいるか」を
ゼロから説明し直さずに済む自己増殖型ナレッジベース。
REX_AI 全プロジェクトの中枢として、プロジェクト横断のナレッジ管理を担う。

---

## ⚠️ このシステムの理解が前提

Trade_System のようにロジック変更が頻繁なプロジェクトでは、
「現在のロジックを読む」だけでなく「なぜそうなったか（変更推移）」の
理解が必要。その変更推移はこの REX_Brain_Vault に蓄積されている。

新スレッドの Evaluator / Planner は以下の 2 層を理解すること:
```
Layer 1: Trade_System のロジック理解
  → Trade_System/docs/ADR.md, EX_DESIGN_CONFIRMED.md, .CLAUDE.md

Layer 2: REX_Brain_Vault のシステム理解（本ファイル）
  → Vault 構造、NLM の使い方、doc_map、ADR 採番ルール
  → 「どこに何があるか」「なぜその構造か」
```

---

## 3 階層 CLAUDE.md の棲み分け

```
~/.claude/CLAUDE.md            — RTK 設定（全リポ共通・ClaudeCode 起動時自動読込）
Trade_System/.CLAUDE.md        — 不変ルール・パラメータ・凍結ファイル（Trade_System 内で自動読込）
REX_Brain_Vault/CLAUDE.md      — 本ファイル。Vault 運用手順（filesystem MCP 経由で明示的読込）

原則: 「誰が・いつ読むか」で分ける
  グローバル = 全セッション自動
  プロジェクト = Trade_System 内で自動
  Vault = 明示的読込（設計者・Evaluator・Planner が必要時に参照）
```

---

## ディレクトリ構造

```
REX_Brain_Vault/                          ← GitHub: Minato33440/REX_Brain_Vault
├── CLAUDE.md                             ← 本ファイル（運用ルール）
├── README.md                             ← リポジトリ概要
├── .gitignore                            ← .obsidian / .venv 等を除外
├── raw/                                  ← 元資料（イミュータブル・読むだけ）
│   └── system_build/                     ← 構築過程の記録
└── wiki/
    ├── START_HERE.md                     ← 🆕 新スレ入口（100 行以内）
    ├── STARTUP_CODES.md                  ← 🆕 起動コード辞書（Wiki-system/trade/brain/casual）
    ├── index.md                          ← 全ページ目次（v3）
    ├── log.md                            ← 時系列作業ログ（追記専用）
    │
    ├── philosophy/                       ← 🆕 参考資料・Evaluator の気づきメモ
    │   ├── evaluator_code.md             ← 唯一の書き込み先（任意・強制なし）
    │   ├── minato_core.md                ← 一次情報源参考リンク集
    │   ├── cross_vectors.md              ← 7 代目整理の 4 横断ベクトル事実記録
    │   └── architecture.md               ← 4 リポ / 4 NLM 体制事実記録
    │
    ├── casual/                           ← 🆕 雑談・個人的話題中期記憶層（Wiki-casual 専用）
    │   ├── _RUNBOOK.md
    │   ├── topics/
    │   ├── ideas/
    │   └── insights/
    │
    ├── entities/                         ← 旧配置（Phase C で trade_system/ へ統合予定）
    ├── decisions/                        ← 旧配置（Phase C で trade_system/ へ統合予定）
    │
    ├── trade_system/                     ← Trade_System 専用層
    │   ├── _RUNBOOK.md
    │   ├── doc_map.md                    ← 設計文書バージョン管理・NLM source_id
    │   ├── adr_reservation.md            ← ADR 採番予約台帳
    │   ├── pending_changes.md            ← 決定済み未確定変更
    │   └── concepts/                     ← neck / window / 4h_superiority
    │
    ├── trade_brain/                      ← ⬜ 未構築（Phase D 着手対象）
    │
    ├── cross/                            ← プロジェクト横断ナレッジ
    │   └── index.md                      ← 骨組みのみ
    │
    └── handoff/
        ├── latest.md                     ← v6.2 現在地ダッシュボード
        └── architecture_handoff.md       ← 7 代目セッション記録（保全）
```

---

## セッション開始時のルール

```
STEP 0: wiki/START_HERE.md を読む（最優先）
  → 100 行以内で 3 リポ現在地 + 地雷 5 つ + 起動コードを把握
  → スレ冒頭に「Wiki-system」「Wiki-trade」「Wiki-brain」「Wiki-casual」などの
    起動コードがあった場合は wiki/STARTUP_CODES.md の定義に従い適切なモードで起動

STEP 1: wiki/handoff/latest.md を読む（統括 Evaluator / システム業務時）
  → ⚠️ 冒頭の「致命的地雷リスト（5 項目）」を必ず確認する
  → 特に ADR D-6（neck_1h/neck_4h 混同）は繰り返し発生している
  → 「読み込み検証チェックリスト」の全 10 問に回答してから作業開始

STEP 2: wiki/log.md の末尾 5 件を確認する

STEP 3: Trade_System が話題なら以下も確認する:
  → wiki/trade_system/doc_map.md（どの doc が最新か）
  → wiki/trade_system/pending_changes.md（決定済み未確定変更）
  → wiki/trade_system/adr_reservation.md（ADR 採番状況）

STEP 4: Trade_System/docs/ を確認
  → 日付なしファイルのみが有効（ADR.md, EX_DESIGN_CONFIRMED.md 等）
  → 日付付きファイルが残っていたらボスに報告（旧版→archive 移動漏れ）

STEP 5: 「前回からの変更点」を一言で把握してから作業開始

STEP 6（任意）: NLM 認証チェック
  → システム系 3 NLM（System/Trade/Wiki）は 2026-04-23 運用開始
  → REX_Casual_Brain は雑談スレでのみクエリ
  → 認証切れ時: ボスに「nlm login をお願いします」と伝える
  → フォールバック: wiki/trade_system/pending_nlm_sync.md に記録
```

### 雑談スレ時（`Wiki-casual` 起動）

- STEP 0 の後、wiki/casual/_RUNBOOK.md のみ読む
- STEP 1〜5 はスキップ（システム業務用なので）
- 継続話題があれば casual/topics/ 該当ページを読む
- NLM: REX_Casual_Brain のみ参照（システム系 NLM は参照しない）

---

## セッション終了時のルール（/wrap-up）

```
STEP 1: wiki/log.md に今日の決定事項・完了タスクを追記
STEP 2: wiki/trade_system/pending_changes.md を更新
STEP 3: wiki/trade_system/adr_reservation.md を更新（新規採番があれば）
STEP 4: wiki/handoff/latest.md を更新（次スレ用引き継ぎ）
  → ⚠️ 冒頭に「致命的地雷リスト（5 項目）」を必ず含める
  → 分析ベースの最新版番号を明記
  → 「読み込み検証チェックリスト（10 問）」のQ&Aを最新ロジックに更新

STEP 4-b: wiki/START_HERE.md を更新（3 リポに状態変化があった時）

STEP 5: NLM に新規ソースを追加（認証切れなら pending_nlm_sync.md）
STEP 6: docs/ の旧版ファイルを logs/docs_archive/ に移動

STEP 7: REX_Brain_Vault に GitHub push（⚠️ 必須確認）
  → push 対象（必須）:
    ✅ wiki/handoff/latest.md（本体ファイル — NOTE だけでは不十分）
    ✅ wiki/START_HERE.md
    ✅ wiki/log.md
    ✅ その他更新ファイル
  → ⚠️ latest.md 本体が push されていないと、
    Claude.ai の次セッションで Vault を直接読めないため引き継ぎが破綻する
  → リポジトリ: Minato33440/REX_Brain_Vault

STEP 8: Claude.ai プロジェクト更新（⚠️ ボス手動 — チェックリスト）
  □ プロジェクトナレッジから旧版ファイルを削除
  □ latest.md をプロジェクトナレッジに添付（最新版に差し替え）
  □ START_HERE.md をプロジェクトナレッジに添付
  □ STARTUP_CODES.md をプロジェクトナレッジに添付（Wiki-xxx コマンドが全スレで機能する）
  □ Vault CLAUDE.md をプロジェクトナレッジに添付
  □ docs/ の最新版（ADR.md / EX_DESIGN_CONFIRMED.md）を添付

STEP 9（任意）: philosophy/evaluator_code.md に気づきメモ追記
  → 強制ではない。システム構築上の気づきがあった時のみ
  → 「後任はこうすべき」と書かない（思想強制禁止）
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

## 設計文書管理ポリシー（Trade_System）

### 基本原則：不変 × 新規作成 × archive 移動

```
❌ 既存の設計文書を編集する
✅ 設計が変わったら新しい .md を作成する（日付なしファイル名）
✅ 旧版は logs/docs_archive/ に移動する（docs/ に残さない）
✅ 決定した時点で pending_changes.md に記録する
✅ 新ファイルを NotebookLM に追加してからスレッドを開始
```

### NotebookLM への追加手順

```
1. source_add(file_path="C:\...\docs\[新ファイル].md", source_type="file")
2. doc_map.md の「NLM 投入済みソース」テーブルに source_id を記録
3. pending_changes.md を更新
4. wiki/log.md に Ingest 記録を追記
5. REX_Brain_Vault に push（latest.md 本体含む）
```

---

## Lint 運用

```
タスク完了時 + 週次に実施:
Lint-1: ADR 採番整合チェック（NLM query + adr_reservation 照合）
Lint-2: pending_changes 整合チェック
Lint-3: doc_map × NLM ソース整合チェック
Lint-4: docs/ に日付付きファイルが残っていないかチェック（archive 移動漏れ検出）
Lint-5: Claude.ai プロジェクトナレッジに旧版が残っていないか確認（STEP 8 漏れ検出）
```

---

## 書き込みルール

- `raw/` は絶対に編集しない（読み取り専用）
- `wiki/log.md` は追記のみ（過去ログは削除しない）
- `wiki/handoff/latest.md` は毎セッション上書き更新
- `wiki/START_HERE.md` は 3 リポに状態変化があった時上書き
- `wiki/trade_system/pending_changes.md` は設計判断のたびに更新
- `wiki/trade_system/adr_reservation.md` は採番のたびに更新
- `wiki/philosophy/evaluator_code.md` は任意追記（後任への強制禁止）
- `wiki/philosophy/` の他 3 ファイル（minato_core / cross_vectors / architecture）は事実記録のみ
- `wiki/casual/*` は雑談スレ（Wiki-casual）でのみ更新・システム業務スレでは触らない

---

## プロジェクト基本情報

| 項目 | 値 |
|---|---|
| REX_Brain_Vault | C:\Python\REX_AI\REX_Brain_Vault\ |
| Vault GitHub | **Minato33440/REX_Brain_Vault** |
| Trade_System | C:\Python\REX_AI\Trade_System\ |
| Trade_System GitHub | **Minato33440/Trade_System** |
| Trade_Brain | C:\Python\REX_AI\Trade_Brain\ |
| Trade_Brain GitHub | **Minato33440/Trade_Brain** |
| 対象通貨 | USDJPY（5M足・4H方向判定） |
| HP | setona.co.jp（さくら・WordPress） |
| HP GitHub | Minato33440/Setona_HP |
| Second_Brain_Lab | **凍結**（Minato33440/Second_Brain_Lab） |
| NotebookLM ① | REX_System_Brain（ID: da84715f-9719-40ef-87ec-2453a0dce67e）|
| NotebookLM ② | REX_Trade_Brain（ID: 4abc25a0-4550-4667-ad51-754c5d1d1491）|
| NotebookLM ③ | REX_Wiki_Vault（ID: 5d09e468-3a96-4906-af27-3400c50a0275）🆕 2026-04-23 設立 |
| NotebookLM ④ | REX_Casual_Brain（ID: daf281ae-e310-400f-961a-20db58b98e01）🆕 2026-04-23 設立 |
| 旧 NotebookLM | 旧 REX_Trade_Brain（ID: 2d41d672-f66f-4036-884a-06e4d6729866）⚠️ 切り離し済・参照禁止 |
