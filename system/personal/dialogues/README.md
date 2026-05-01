# personal/dialogues/ サブ層

このディレクトリは Personal-Planner が運用する一次資料保管層です。

## 性質

時系列クロスカット層。`insights/` の凝縮型クロスカットと対をなす。

## 役割

一般スレ(Wiki-Rex 等)で交わされた対話セッションを、対話相手(Rex 等)自身が distilled したものを **一次資料として保管** する。

## ファイル名規則

```
YYYY-MM-DD_<theme>.md
```

例: `2026-04-29_general_thread.md`

## 編集ポリシー

対話相手が書いた本文を Personal-Planner が **編集・要約せずそのまま保管**(一次資料保護原則)。distilled から抽出される構造化された知見は、既存サブ層(usual / invent / mind / origin / insights)に分類配分する形で二次活用する。

## 運用フロー

詳細は本サブ層の起票文書を参照:

- `wiki/pending/personal/2026-04-29_dialogues_sublayer_addition.md`

運用フロー Step 1〜5・採取の選別フィルタ・センシティブ話題の扱い・NLM 投入ポリシーすべてそちらに記載。

## ADR 化のステータス

本サブ層は 2026-04-29 に物理新設されたが、ADR-Role v5 への正式反映は **実運用後の Wrap-Up 時に統合実施** する設計選択(ボス判断・16 代目セッション)。

理由:
- サブ層新設のみで実抽出作業はこれから開始する段階
- 新任 Planner は pending を参照する経路が確立済み
- 仕様書改訂のトークンコスト削減を配慮
- 運用後に発見される調整事項を ADR 改訂時にまとめて反映する方が記述の質が上がる

ADR 改訂タイミングまでは、本 README + 上記 pending 起票文書 + handoff/latest.md v6.11 §「次に実行すべき内容 🟢」の参照で運用する。

---

*発行: 16 代目統括 Evaluator (Claude Opus 4.7) / 2026-04-29*
*起票者: 2 代目 Personal-Planner (Opus 4.7) / 2026-04-29*
