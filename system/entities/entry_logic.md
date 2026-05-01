# entry_logic.py

**状態**: ✅ #018 完了・**変更凍結**  
**最終更新**: 2026-04-20（REX_028 Phase 1-2 完了・現役利用範囲を反映）

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

## エントリー条件（旧版 backtest.py 用）

```
優位性★★★: fib_pct <= 0.55
            かつ 1H neck から ±20pips以内
            かつ sl_last >= support_1h
```

> ⚠️ **現役 #026d 経路**: `window_scanner.py` は本ファイルから `check_15m_range_low()` のみ呼び出し、
> neck 計算は **統一 neck 原則** `sh_before_sl.iloc[-1]` を独自に実施（A-5 / E-7 / F-6）。
> エントリー判定は **指値方式**（`neck_15m + ENTRY_OFFSET_PIPS=7.0`）で行われ、
> 本ファイルの `evaluate_entry()` は現役ロジックでは使用されない（E-7）。

---

## 関連 ADR

- **A-5** — neck 選択の後期バイアス → 統一 neck 原則への転換
- **D-9** — WICKTOL_PIPS → ENTRY_OFFSET_PIPS 置換
- **E-7** — 指値方式への転換（#026c 確定）
- **F-3** — 関数の責務を単一に（`check_15m_range_low()` → パターンラベル取得のみ）
- **F-4** — 凍結ファイル変更ポリシー
- **F-6** — 各 TF SH/SL 目的定義

## 関連文書

- Trade_System/docs/ADR.md
- Trade_System/docs/SYSTEM_OVERVIEW.md
- Trade_System/docs/EX_DESIGN_CONFIRMED.md
