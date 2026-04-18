# window_scanner.py

**状態**: ✅ #025完了  
**変更凍結**: ❌（#026で決済統合が必要）  
**最終更新**: 2026-03-31

---

## 役割

4H→1H→15M→5M の階層スキャンを担う中心ファイル。
`backtest.py` とは独立して動作し、既存ファイルを一切変更しない設計。

---

## 処理フロー

```
scan_4h_events()
  └── 4H LONG期間を抽出（89件）
       └── get_1h_window_range()
             └── 4H SL ±8本窓内で最近傍1H SLを検索
                  └── scan_window_entry()
                        └── 窓内15M/5Mをスキャン
                              └── check_15m_range_low() → DB/IHS/ASCENDING判定
                                   └── neck = sh_vals.iloc[0]（固定ネック）
                                        └── 5M close > neck + 5.0pips → エントリー記録
```

---

## 主要関数

| 関数 | 内容 |
|---|---|
| `scan_4h_events()` | 4H LONG期間をスキャン |
| `get_1h_window_range()` | 4H SL近傍の1H SL窓を確定 |
| `scan_window_entry()` | 窓内15M/5Mスキャン・エントリー判定 |

---

## 確定パラメータ

| パラメータ | 値 | 確定番号 |
|---|---|---|
| WINDOW_1H_PRE | 20本 | #020 |
| WINDOW_1H_POST | 10本 | #023 |
| WICKTOL_PIPS | 5.0 | #013 |
| neck計算 | sh_vals.iloc[0] | #025 |
| PLOT_PRE_H | 25h | #024a |
| PLOT_POST_H | 40h | #024a |

---

## 実装履歴

| # | 変更内容 | 結果 |
|---|---|---|
| #021 | 新規作成（窓左端スキャン） | 13件→全件誤検出 |
| #022 | 1H SL以降限定スキャン | 2件（IHS×2） |
| #023 | WINDOW_1H_POST 5→10延長 | 5件 |
| #024a | neck=1H SL以降初回SH・プロット範囲拡大 | 4件 |
| #025 | 固定ネック原則（iloc[0]） | **15件（DB:3/IHS:3/ASCENDING:9）** |

---

## 出力

- `logs/window_scan_entries.csv`（15件）
- `logs/window_scan_plots/*.png`（15枚）

---

## 次のアクション

**#026**: `manage_exit()` を統合して決済シミュレーションを実装する。

→ [[exit_logic]] の `manage_exit()` を呼び出す決済ループを追加
