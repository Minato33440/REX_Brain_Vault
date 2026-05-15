---
type: concept
status: active
last_updated: 2026-04-18
---

# neck — 統一neck原則

## 定義

neck = SL直前（時系列で左側）の最後のSH。全TF共通。

```
価格
 ↑    SH(neck)
 |   /  ＼
 |  /    ＼___SL(底)
 | /
 +──────────────→ 時間
       ← neck はここ（SLの左側）
```

## 各TFのneck定義

| TF | 定義 | 窓限定 | 用途 |
|---|---|---|---|
| neck_15m | 窓内 かつ sl_1h_ts以前 の最後の15M SH | 窓内のみ | エントリートリガー |
| neck_1h | 窓内 かつ sl_1h_ts以前 の最後の1H SH | 窓内のみ | 窓特定アンカー + フィルター基準 |
| neck_4h | sl_4h_ts以前 の最後の4H SH | 全体OK | **半値決済トリガー（stage2）** |

## ⚠️ 致命的な混同（ADR D-6）

```
❌ neck_1h = 半値決済トリガー  ← 3回発生した間違い
✅ neck_4h = 半値決済トリガー
✅ neck_1h = 窓特定アンカー（決済トリガーではない）
```

## 変遷

| 時期 | 定義 | 状態 |
|---|---|---|
| #025 | sh_vals.iloc[0]（SL以降の初回SH） | 廃止 |
| #026a | sh_before_sl.iloc[-1]（SL直前の最後のSH） | ✅ 現行 |

## 関連ページ

- [[4h_superiority]] — neck_4h >= neck_1h フィルター
- [[window]] — 窓内でのneck検出範囲
