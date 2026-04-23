# window_scanner.py

**状態**: ✅ #026d 完了・**拡張可能**（カラム追加・出力拡張 OK / スキャンロジック変更は要確認）  
**最終更新**: 2026-04-20（REX_028 Phase 1-2 完了・#026d PF 4.54 静的保持）

---

## 役割

4H→1H→15M→5M の階層スキャンを担う **Trade_System の中心ファイル**。
エントリー検出と CSV 出力を担当する。決済は `src/exit_simulator.py`（方式 B）が
`window_scan_entries.csv` を読み取って独立に実施する（F-2: エントリー文脈はエントリー時に確定）。

凍結ファイル（backtest / entry_logic / exit_logic / swing_detector）は一切変更しない。

---

## 処理フロー（#026d 確定版）

```
scan_4h_events()
  └── 4H LONG 期間を抽出（get_direction_4h, n=3, lookback=20）
       └── get_1h_window_range()
             └── 4H SL ±8本窓内で最近傍 1H SL を検索（N_1H_SWING=3 / D-7）
                  └── 4H 構造優位性フィルター: neck_4h >= neck_1h ?（D-10）
                       ├── No  → SKIP（誤除外 0 件で検証済み）
                       └── Yes → scan_window_entry()
                              └── 窓内 5M → 15M リサンプル
                                   └── check_15m_range_low() → DB / IHS / ASCENDING 判定
                                        └── 統一 neck 原則: neck_15m = sh_before_sl.iloc[-1]（A-5）
                                             └── 5M High >= neck_15m + 7pips
                                                  → 指値エントリー確定（E-7）
```

---

## 確定パラメータ（#026d 版）

| パラメータ | 値 | 確定 ADR |
|---|---|---|
| `DIRECTION_MODE` | `'LONG'` | #012 |
| `ENTRY_OFFSET_PIPS` | `7.0`（🟡 暫定・STEP ⑥ ボラ係数実装時に動的化予定） | D-9 / E-7 |
| `N_1H_SWING` | `3`（旧 `2` から変更） | D-7 |
| neck 計算（全 TF 共通） | `sh_before_sl.iloc[-1]`（統一 neck 原則） | A-5 |
| 4H 構造優位性フィルター | `neck_4h >= neck_1h`（エントリー有効の必要条件） | D-10 |
| `WINDOW_1H_PRE` | 20 本 | #020 |
| `WINDOW_1H_POST` | 10 本 | #023 |
| `PLOT_PRE_H` / `PLOT_POST_H` | 25h / 40h | #024a |
| Swing n 値（全 TF） | 4H=3 / 1H=3 / 15M=3 / 5M=2 | F-6 |

---

## neck 用途定義（地雷 D-6 回避・doc_map と一致）

| neck | 用途 |
|---|---|
| `neck_15m` | エントリートリガー（5M High >= neck_15m + 7pips で指値約定） |
| `neck_1h` | 窓特定アンカー + 4H 構造優位性フィルター基準値 |
| `neck_4h` | 半値決済トリガー（`exit_simulator.py` が CSV から読み取り） |

---

## 出力 CSV

`logs/window_scan_entries.csv`（12 カラム）。
エントリー文脈はエントリー時に確定する（F-2）。`exit_simulator.py` は本 CSV を読み取るだけで
決済を実施する（再計算しない）。

---

## #026 シリーズ実装履歴（現役起点）

| # | 変更内容 | 確定 ADR |
|---|---|---|
| #026a | 統一 neck 原則 `sh_before_sl.iloc[-1]` / sh_4h / neck_1h CSV 追加 | A-5 / E-6 |
| #026b | `manage_exit()` 迂回 → `exit_simulator.py` 方式 B 採用 | D-8 |
| #026c | `WICKTOL_PIPS` → `ENTRY_OFFSET_PIPS` 置換・指値方式確定 | D-9 / E-7 |
| **#026d** | **4H 構造優位性フィルター（neck_4h >= neck_1h）追加** | **D-10** |

---

## #026d バックテスト結果（静的保持中）

```
PF        : 4.54
勝率      : 60.0% (10 件 LONG)
MaxDD     : 35.8 pips
総損益    : +150.6 pips
```

⚠️ 上記は `exit_simulator.py` 側の 🤖 **創作混入 2 件を含む結果**
（D-12 stage2 建値移動 / D-13 stage3 1H 実体確定）。
Phase 4（REX_029 以降）で裁量整合版に訂正予定・新 PF を新しい静的点として記録する計画。

---

## 関連 ADR

- **A-5** / **E-7** — 統一 neck 原則・指値方式
- **D-6** — neck_1h / neck_4h 用途の地雷（doc_map §neck 用途定義で恒常的防止）
- **D-7** — 1H Swing n=3 確定
- **D-8** — `manage_exit()` 迂回・`exit_simulator.py` 方式 B 正式採用
- **D-9** — ENTRY_OFFSET_PIPS=7.0 置換
- **D-10** — 4H 構造優位性フィルター（裁量思想フラクタル構造から必然的に導かれる）
- **E-6** — neck_1h / neck_4h の CSV 追加（方式 B 選択採用）
- **F-1** — トップダウン原則（上位足 → 下位足）
- **F-2** — エントリー文脈はエントリー時確定
- **F-6** — 各 TF SH/SL 目的定義

## 関連文書

- Trade_System/docs/ADR.md
- Trade_System/docs/SYSTEM_OVERVIEW.md §データフロー
- Trade_System/docs/EX_DESIGN_CONFIRMED.md
- Trade_System/docs/src_inventory.md
- [[exit_logic]]（#009 凍結・使用禁止）
- [[entry_logic]]（#018 凍結・`check_15m_range_low()` のみ現役利用）
- [[swing_detector]]（#020 凍結・1H n=3）
