---
title: Trade_Rogic 索引
type: moc_index
created: 2026-05-16
tags:
  - moc
  - trade_memo
---

# 🗺️ Trade_Rogic 索引

過去に気づいたロジック関連メモの自動集約ハブ。規約は [[_schema|プロパティ規約]]。
**Rex戦略データ正本は distilled。本フォルダは Minato の方法論メモ（検証前段・人間用）。**

> [!info] 動作条件
> Dataview 有効時に各表は自動更新（このVaultは有効化済み）。新規メモが規約準拠なら自動で行が増える。

## 全メモ一覧（status順）

```dataview
TABLE category AS "カテゴリ", status AS "状態", confidence AS "確度", created AS "追加日"
FROM "REX_Brain_Vault/MINATO/Trade_Rogic"
WHERE type = "trade_memo"
SORT status ASC, created DESC
```

## 未検証（draft）— 検証待ち

```dataview
TABLE category AS "カテゴリ", confidence AS "確度", created AS "追加日"
FROM "REX_Brain_Vault/MINATO/Trade_Rogic"
WHERE type = "trade_memo" AND status = "draft"
SORT created ASC
```

## 中核ルール（core）— Playbook蒸留候補

```dataview
TABLE category AS "カテゴリ", confidence AS "確度"
FROM "REX_Brain_Vault/MINATO/Trade_Rogic"
WHERE type = "trade_memo" AND status = "core"
SORT category ASC
```

## カテゴリ別件数

```dataview
TABLE length(rows) AS "件数"
FROM "REX_Brain_Vault/MINATO/Trade_Rogic"
WHERE type = "trade_memo"
GROUP BY category
SORT length(rows) DESC
```

---
*索引 v1 / 2026-05-16 / ClaudeCode。新概念MOC化・正本蒸留は次フェーズ（スターター対象外）。*
