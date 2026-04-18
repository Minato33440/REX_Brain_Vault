# entry_logic.py

**状態**: ✅ #018完了・**変更凍結**  
**最終更新**: 2026-03-31

---

## 役割

エントリー判定の全ロジックを担う。3パターン統合レンジロジックが核心。

---

## 主要関数

| 関数 | 内容 |
|---|---|
| `check_fib_condition()` | Fib押し目条件の判定 |
| `check_15m_range_low()` | DB/IHS/ASCENDING統合レンジ判定（#011確定） |
| `check_5m_double_bottom()` | 5M DBネックライン実体確定 |
| `evaluate_entry()` | 3段階統合 + 1H neck/support + gradeフィルター |

---

## check_15m_range_low() — 3パターン統合

```
パターン1 DB       : SL_last ≒ SL2（同水準）
パターン2 IHS      : SL_last <= SL2（逆三尊右肩）
パターン3 ASCENDING: SL_last > SL2（安値切り上げ）

共通成立条件:
  ① SL_last >= SL_min
  ② SL_last <= SL_min + 2.0*(SL2 - SL_min)（等距離ルール）
  ③ SL_min以降に15M SHが存在（ネック形成確認）
```

---

## 確定パラメータ

| パラメータ | 値 | 確定番号 |
|---|---|---|
| LOOKBACK_15M_RANGE | 50 | #014 |
| WICKTOL_PIPS | 5.0 | #013 |
| NECK_TOLERANCE_PIPS | 20.0 | #017 |
| ALLOWED_GRADES | ['★★★'] | #018 |
| ALLOWED_PATTERNS | ['DB', 'ASCENDING', 'IHS'] | #014 |
| DIRECTION_MODE | 'LONG' | #012 |

---

## エントリー条件（旧版backtest.py用）

```
優位性★★★: fib_pct <= 0.55
            かつ 1H neck から ±20pips以内
            かつ sl_last >= support_1h
```

> window_scanner.py では独自のネック計算（sh_vals.iloc[0]）を使用
