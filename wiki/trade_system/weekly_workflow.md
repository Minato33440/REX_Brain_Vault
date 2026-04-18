# weekly_workflow.md — 週末 Git データ更新ワークフロー
# 管理: Evaluator
# 更新: 2026-04-18（Vault移設・入力パス固定化・命名規則明確化）
# 参照元: Trade_System/.CLAUDE.md から参照

---

## 目的

週末のGitデータ更新を、ボスからの最小限の指示で正確に実行するための
一元化されたワークフロー。指示書のテキスト入力を不要にし、
データ取得・ファイル生成・命名の精度を構造的に保証する。

---

## ⚠️ RTK ルール（全工程共通）

```bash
# 全てのgitコマンドに rtk プレフィクスを付ける
rtk git status
rtk git add ...
rtk git commit -m "msg"
rtk git push origin main

# python は rtk 対象外
python main.py --trade --news
```

---

## 1. 入力データ（ボスが事前配置）

週末作業の前に、ボスが以下のファイルを配置する。
ClaudeCodeは作業開始時にこれらの存在を確認すること。

### 1-1. 入力パス一覧

| データ | パス | 頻度 |
|---|---|---|
| 週次市況解説 | `logs/gm/boss's-weeken-Report/2026/wr-YYYY-M-D.txt` | 毎週 |
| トレード履歴 | `logs/gm/boss's-weeken-Report/trade_summary_tmp.txt` | 随時追記 |
| GMポートフォリオ | `logs/png_data/*.png` | 月1回程度・不定期 |

### 1-2. 作業開始前の確認

```
ClaudeCodeは以下を順に確認する:

1. 今週のwr-*.txtが存在するか確認
   → ls logs/gm/boss's-weeken-Report/2026/
   → 最新のwr-YYYY-M-D.txtを特定

2. trade_summary_tmp.txtの内容を確認
   → cat logs/gm/boss's-weeken-Report/trade_summary_tmp.txt
   → 未記録分があれば private_trades.csv に反映

3. ボスに「python main.py --trade --news」の実行を依頼
   → ターミナル出力（8ペア変動率・レジーム）を受領してから次に進む
   → ⚠️ 実測データなしにファイル作成しない（推定値の二度手間防止）
```

---

## 2. 週次フォルダ命名規則

### 2-1. フォルダ名フォーマット

```
YYYY-M-D_wkNN

YYYY = 年
M    = 月（ゼロ埋めしない: 1, 2, ... 12）
D    = 日（ゼロ埋めしない: 1, 2, ... 31）
wkNN = その月の第N週（月リセット方式）
```

### 2-2. 日付の決め方

**日付 = その週の金曜日**（データ抽出期間は前週の月〜金）

```
例: 2026年4月18日（土）に作業する場合
  → 金曜日 = 4月17日
  → 4月の第3週
  → フォルダ名: 2026-4-17_wk03
```

### 2-3. wkNN のカウント方法

**月リセット方式**: 各月の第1週目からwk01で開始する。

```
2026-3-7_wk01     ← 3月第1週
2026-3-14_wk02    ← 3月第2週
...
2026-3-28_wk04    ← 3月第4週
2026-4-3_wk01     ← 4月第1週（リセット）
2026-4-10_wk02    ← 4月第2週
2026-4-17_wk03    ← 4月第3週（今週）
```

### 2-4. date_range（データ抽出期間）

```
date_range = その週の月曜日 → 金曜日
例: 2026-4-17_wk03 の date_range = 2026-04-14 -> 2026-04-18
```

---

## 3. データ取得コマンド

### 3-1. メインコマンド

```bash
python main.py --trade --news
```

⚠️ 旧コマンド `python configs/rex_chat.py --trade --news` は廃止。

### 3-2. --trade から得るもの

| 抽出物 | 元パス | 週次フォルダでの保存先 |
|---|---|---|
| 8ペア30日プロット | `logs/png_data/multi_pairs_plot_8.png` | `charts/Portforio-YYYY-MM-DD.png` |
| 8ペア変動率テキスト | ターミナル出力 | `charts/YYYY-MM-DD 〜 YYYY-MM-DD.txt`（取得期間） |
| レジームスナップショット | `logs/png_data/YYYY_MM_DD_snapshot.yaml` | `charts/YYYY_MM_DD_snapshot.yaml` |

### 3-3. --news から得るもの

| 抽出物 | 保存先 |
|---|---|
| GMキーワードニュース | `charts/Market conditions -YYYY-M-D~.txt` |

ボスの市況テキスト（wr-*.txt）を先頭に配置し、--news出力を続けて一元管理。

### 3-4. トレードデータ

```bash
# 当週トレードのMarkdown生成
python src/track_trades.py summary --start YYYY-MM-DD --end YYYY-MM-DD
# → trade_results.md として保存
```

---

## 4. 出力ファイル一覧

### 4-1. 週次フォルダ構造

```
logs/gm/weekly/2026/YYYY-M-D_wkNN/
├── meta.yaml         ← week, date_range, regime, snapshot, portfolio
├── review.md         ← 結論・材料・Evidence・Implication・Trades of the Week
├── note.md           ← Macro/Regime・takeaways・gates・Portfolio action
├── charts.md         ← charts/内ファイルのリンク一覧
├── trade_results.md  ← track_trades.py summary の出力
└── charts/
    ├── Portforio-YYYY-MM-DD.png       ← ローカル専用（.gitignore）
    ├── YYYY_MM_DD_snapshot.yaml       ← Git追跡
    ├── YYYY-MM-DD 〜 YYYY-MM-DD.txt   ← Git追跡（取得期間）
    ├── Market conditions -YYYY-M-D~.txt ← Git追跡
    └── GM Strategy-YYYY-M-D.txt       ← Git追跡（ClaudeCode作成）
```

### 4-2. charts/ Git追跡ルール

```
追跡対象: *.txt / *.yaml / *.md
ローカル専用: *.png（.gitignore除外済み）
```

---

## 5. 更新対象（週次フォルダ外）

| ファイル | 更新内容 |
|---|---|
| `logs/gm/weekly/2026/_index.md` | 当週エントリ追加（Regime/1行/Key gates/Links） |
| `docs/STATUS.md` | 最新 Weekly Brief セクション追加 |
| `docs/Trade-Main.md` | Weekly Indexに当週追加 / Distilled Linksリンク更新 / Weekly Brief追加 |
| `versions/distilled/2026/distilled-gm-2026-N.md` | 当週distilledエントリ追記 |
| `data/private_trades.csv` | 当週トレード反映 |

### distilled ファイル命名ルール（重要）

```
N = 月番号。同月内は必ず同じファイルに追記する。
例: 4月全週 → distilled-gm-2026-4.md に追記
    5月第1週 → distilled-gm-2026-5.md を新規作成
⚠️ 月内で分割しない（-4, -5 のように週ごとに新規作成しない）
```

---

## 6. 実行チェックリスト

```
□ 1. 入力データ確認
     □ wr-YYYY-M-D.txt の存在確認
     □ trade_summary_tmp.txt の内容確認
     □ ボスに「python main.py --trade --news」実行を依頼

□ 2. データ取得
     □ ターミナル出力 → charts/YYYY-MM-DD 〜 YYYY-MM-DD.txt
     □ multi_pairs_plot_8.png → charts/Portforio-YYYY-MM-DD.png
     □ snapshot.yaml → charts/ にコピー
     □ 市況 + --news出力 → charts/Market conditions -YYYY-M-D~.txt

□ 3. トレードデータ
     □ trade_summary_tmp.txt → private_trades.csv に反映
     □ track_trades.py summary → trade_results.md

□ 4. 週次フォルダ作成
     □ logs/gm/weekly/2026/YYYY-M-D_wkNN/ 作成
     □ charts/ サブフォルダ作成

□ 5. ファイル生成（ClaudeCode）
     □ meta.yaml
     □ review.md（Trades of the Week含む）
     □ note.md
     □ charts.md
     □ GM Strategy-YYYY-M-D.txt

□ 6. 週次フォルダ外の更新
     □ _index.md
     □ STATUS.md
     □ Trade-Main.md
     □ distilled-gm-2026-N.md

□ 7. Git更新
     □ rtk git add logs/gm/weekly/2026/YYYY-M-D_wkNN/ \
               logs/gm/weekly/2026/_index.md \
               docs/STATUS.md docs/Trade-Main.md \
               versions/distilled/2026/ \
               data/private_trades.csv
     □ rtk git commit -m "weekly: YYYY-M-D_wkNN review + trade_results + charts"
     □ rtk git push origin main
```

---

## 7. GM Strategy ファイル構成

ClaudeCodeが8ペア30日データ・レジーム・市況・newsを統合して作成。

```
セクション構成:
① 8ペアサマリ
② 週末市況
③ ファンダメンタルズ
④ テクニカル
⑤ シナリオ
⑥ 押し目戦略
⑦ アクション
⑧ 参照データ
⑨ 総合解説(A-G)
```

---

## 8. review.md「Trades of the Week」セクション

```
- 数値: track_trades.py summary の概要（回数・勝敗・勝率・合計PnL）
- 代表トレード: 1〜3件の要約（symbol, direction, pnl_%, tag, notes）
- 学び: 反省・改善点・来週方針を2〜3行
```

---

## 9. ClaudeCodeへの起動指示（ボス用テンプレート）

```
週末Git更新を実行してくれ。

参照: C:\Python\REX_AI\REX_Brain_Vault\wiki\trade_system\weekly_workflow.md
入力: logs/gm/boss's-weeken-Report/ に市況とトレード履歴を配置済み。
対象週: 2026-4-17_wk03
```

この3行だけでClaudeCodeが全工程を実行できる。
