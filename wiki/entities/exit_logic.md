# exit_logic.py

**状態**: ✅ #009完了・**変更凍結**  
**最終更新**: 2026-03-31

---

## 役割

4段階決済ロジックを担う。#026でwindow_scanner.pyに統合される予定。

---

## 主要関数

| 関数 | 内容 |
|---|---|
| `check_5m_dow_break()` | 5Mダウ崩れ実体確定の判定 |
| `check_15m_dow_break()` | 15Mダウ崩れ実体確定の判定 |
| `check_4h_neck_1h_confirmed()` | 4H neck + 1H実体確定の判定 |
| `manage_exit()` | 4段階決済統合（**#026で呼び出される**） |

---

## 4段階決済ロジック（確定版）

```
【初動SL: エントリー直後〜5M Swing確定前】
  15Mダウ崩れ実体確定の次足始値で全量損切
  → 広めのSLでノイズを吸収

【段階1: 5M Swing確定後〜1H ネック未到達】
  5Mダウ崩れ実体確定の次の5M始値で全量決済

【段階2: 4H ネックライン到達】
  50%ポジション決済
  残り50%のストップを建値に移動（ノーリスク化）

【段階3: 4H ネック + 1H 実体確定後】
  判定: 1H Close が 4H SHを上抜けた足
       = 5M足12本目（毎時00分起算）= 15M足4本目と同義
  15Mダウ崩れ実体確定の次の15M始値で残り全量決済
```

---

## 確定足・執行足の定義（全ロジック共通）

```
「確定足」= 実体（min/max(open,close)）がラインを越えた足
「執行足」= 確定足の次の足の始値で執行
```

---

## #026での使用方法（予定）

```python
# window_scanner.py に追加する決済ループのイメージ
for entry in entries:
    result = manage_exit(
        df_5m=df_5m,
        entry_time=entry['time'],
        entry_price=entry['price'],
        neck_4h=entry['neck_4h'],
        sl_4h=entry['sl_4h']
    )
    pnl_list.append(result)
```
