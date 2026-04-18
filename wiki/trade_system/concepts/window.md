---
type: concept
status: active
last_updated: 2026-04-18
---

# window — 1H押し目ウィンドウ

## 定義

4H SLに対応する1H SLを中心とした時間窓。
この窓内で15M/5Mパターンを検出しエントリー判定を行う。

```
|←── 前20本 ──→|SL|←── 後10本 ──→|
                 ↑
              1H SL足
```

## 構造

```
LAYER 1（4H）: 上昇ダウの各SLが押し目候補
    ↓
LAYER 2（1H窓）: 4H SL ±8本窓内で最近傍の1H SLを検出
    → 1H SL足: 前20本 + SL足 + 後10本 = 計31本（≈31時間）
    ↓
LAYER 3（窓内15M/5M）: DB / IHS / ASCENDINGパターン検出
    → neck_15m上抜けでエントリー
```

## パラメータ

| パラメータ | 値 | 確定時期 |
|---|---|---|
| WINDOW_1H_PRE | 20 | #021 |
| WINDOW_1H_POST | 10 | #023 |
| WINDOW_SEARCH | ±8本 | #020 |
| N_1H_SWING | 3 | #026a-v2 |

## 1H SL検出の検証結果（#020）

```
対象: 89件（4H LONG期間）
1H SL検出率: 100.0%
距離: 0.0 pips（同一データ源リサンプルのため数学的必然）
```

## 関連ページ

- [[neck]] — 窓内でのneck検出
- [[4h_superiority]] — 窓を通過したエントリーのフィルター
