# swing_detector.py

**状態**: ✅ 凍結（#020 以降）・ただし D-7 で 1H n=3 に確定反映  
**最終更新**: 2026-04-20（REX_028 Phase 1-2 完了・D-7 反映）

---

## 役割

全時間軸のSwing High/Low検出と方向判定を担う基盤ファイル。
全ファイルから参照されるため変更は最小限にとどめる。

---

## 主要関数

| 関数 | 内容 | 追加番号 |
|---|---|---|
| `detect_swing_highs/lows()` | SH/SL検出の基本実装 | 基盤 |
| `get_nearest_swing_high/low()` | 直近SH/SL取得 | 基盤 |
| `get_nearest_swing_high_1h()` | 1H SH取得（neck_4h用） | #016 |
| `get_nearest_swing_low_15m()` | 15M SL取得（support_1h暫定） | #016 |
| `get_nearest_swing_low_1h()` | 1H SL取得（support_1h正式版） | #020 |
| `get_all_swing_lows_1h()` | 1H 全SL取得（最安値検索用） | #020 |
| `get_direction_4h()` | 4H方向判定 | 基盤 |
| `get_direction_from_raw_4h()` | 4H生データから方向判定 | 基盤 |
| `_build_direction_5m()` | パフォーマンス最適化版 | 基盤 |

---

## 確定パラメータ

| 用途 | TF | n | lookback |
|---|---|---|---|
| 4H方向判定（backtest） | 4H | 3 | 20 |
| 4H方向判定（structure_plotter） | 4H | 5 | 100 |
| 4H SH/SL取得（base_scanner） | 4H | 3 | 100 |
| 1H neck_4h取得 | 1H | 3 | 20 |
| 1H SL窓内検索（window_scanner） | 1H | 3 | ±8本窓 |
| 15M レンジロジック | 15M | 3 | 50 |
| 5M DB確定 | 5M | 2 | 20 |

NONE比率: 42.1%（目標50%以下クリア済み）

---

## 関連 ADR

- **D-7** — 1H Swing n=2 → n=3 確定（#026a-verify / TV チャート整合性合格）
- **F-6** — 各 TF SH/SL 目的定義（Swing 確定値: 4H n=3 / 1H n=3 / 15M n=3 / 5M n=2）

## 関連文書

- Trade_System/docs/ADR.md
- Trade_System/docs/SYSTEM_OVERVIEW.md
- Trade_System/docs/EX_DESIGN_CONFIRMED.md
