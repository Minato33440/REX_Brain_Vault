---
title: Trade_Rogic プロパティ規約
type: schema
created: 2026-05-16
tags:
  - schema
  - trade_memo
---

# 🧩 Trade_Rogic プロパティ規約

`MINATO/Trade_Rogic/` に置く「過去に気づいたロジック関連メモ」の共通スキーマ。
**断片を Dataview で横断・検証ループに接続するための土台。** 新規メモは本規約に従う。

> Rex戦略データ正本は Trade_Brain の distilled。本フォルダは **Minato の方法論メモ（人間用・検証前段）**。検証済みルールは将来 `Trade_Playbook.md`（正本）へ蒸留する想定。

## 1. 必須プロパティ（frontmatter）

```yaml
title:      <メモ名>
type:       trade_memo            # 固定（索引対象キー）
created:    YYYY-MM-DD            # 追加した日
category:   MTF分析               # 下記カテゴリ語彙から1つ
status:     draft                 # ライフサイクル（§3）
confidence: mid                   # low / mid / high（実戦での確度）
tags:       [trade, ...]          # 自由タグ（検索補助）
```

任意: `timeframe: [4H, 1H, 15m]` / `instrument: [EURUSD, GBPAUD]` / `source: <元メモ名>`

## 2. category 語彙（表記固定）

`MTF分析` / `環境認識` / `エントリー` / `決済` / `資金管理` / `メンタル` / `相場環境` / `銘柄特性` / `検証手法`

## 3. status ライフサイクル（自己淘汰）

| status | 意味 |
|---|---|
| `draft` | 過去メモ・未検証（取り込んだだけ） |
| `validated` | 実トレードで有効性を確認 |
| `core` | 中核ルール。`Trade_Playbook` 蒸留候補 |
| `deprecated` | 検証で無効/不利と判明。残すが非推奨 |

昇格は実戦・過去検証の根拠を伴って行う（draft→validated→core）。負け相関が出たら deprecated に落とす。

## 4. canonical 概念語彙（wikilink・表記揺れ禁止）

メモ本文に `## 🔗 関連概念（MOC接続）` を設け、該当する概念を canonical 表記で `[[ ]]` 化する。
バックリンク／グラフ／2hop／Dataview集約のため、**同義語は1表記に統一**：

`[[MTF分析]] [[環境認識]] [[ダウカウント]] [[エントリールール]] [[決済ルール]] [[フィボナッチ]] [[トレンドライン]] [[節目分析]] [[時間の優位性]] [[波形分類]] [[レンジブレイク]] [[リスク管理]] [[トレード検証]]`

新概念が出たら canonical 名を決めて本規約に追記してから使う（後付け統一は禁止）。
将来 Trade_Brain の `MOC/` 同様、Dataview自動集計MOCを `Trade_Rogic/MOC/` に作る余地あり（スターターでは未実装）。

## 5. 命名・配置

- ファイル: `<内容を表す日本語名>.md`（先頭 `_` はメタ運用ファイル予約: `_index` / `_schema`）
- 配置: `REX_Brain_Vault/MINATO/Trade_Rogic/` 直下
- 索引: [[_index|Trade_Rogic 索引]] が自動集計

---
*規約 v1 / 2026-05-16 / ClaudeCode。改訂時は本ファイルに追記し日付明記。*
