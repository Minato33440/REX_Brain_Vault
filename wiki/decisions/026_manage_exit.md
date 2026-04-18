# #026 manage_exit() 統合

**優先度**: 🔴 最優先  
**対象ファイル**: window_scanner.py  
**状態**: 未着手（#025完了後に実施）

---

## 実装内容

window_scanner.py に決済シミュレーションを統合する。

```
① エントリー記録から manage_exit() を呼び出す決済ループ
② 損益（P&L）・PF・勝率・MaxDD の計算
③ 結果CSV出力（エントリー+決済+損益）
```

---

## 完了条件

旧版 backtest.py との比較レポートを出力する。

| 指標 | 旧版（#018） | 新版（#026目標） |
|---|---|---|
| 総トレード数 | 20件 | 15件（窓ベース） |
| 勝率 | 55.0% | 計算待ち |
| PF | 5.32 | 計算待ち |
| MaxDD | 14.9 pips | 計算待ち |

---

## 設計方針

- [[exit_logic]] の `manage_exit()` をそのまま流用
- window_scanner.py のみ修正（他ファイル変更なし）
- 思考フラグ: `think harder`

---

## 進め方（Planner + Evaluator + ClaudeCode）

```
Planner（Rex）  → 実装仕様を設計・指示書作成
Evaluator（Rex）→ 結果レポートの監査・修正案
ClaudeCode     → 実装・Git管理
```

> ⚠️ 自律システム（REX_Brain_System）の本番組み込みは
> #026完了・結果評価後に判断する。
