---
type: design_doc
status: draft            # ボス承認まではdraft
version: v0
created: 2026-07-04
author: Rex (Claude Fable 5, Claude Desktop session)
scope: Trade_Brain backfill — regime vector / outcome / trap detection
related:
  - "[[2026-06-27_belly_elevated]]"
tags: [trade_brain, backfill, misread_log, workflow]
---

# Backfill Workflow v0
regimeベクトル + outcome + trap検出の一括後付け設計書

## 目的

Trade_Brain週次蓄積(note.md / meta.yaml / review.md)に対し、
1. 各週の市況状態を機械検索可能な **regimeベクトル** として構造化
2. 「次週に向けた読み」が実際にどう動いたかの **outcome(結果検証)層** を後付け
3. 戦略判断ミスと **相場側の罠(意図的な流動性剥奪)** を証拠ベースで分離抽出

し、誤読記録をVaultへ系統的にwrapupする経路を作る。
これにより近傍検索は「類似regimeで過去こう読んだ」に加えて
「類似regimeでの読みは、こういう方向に外れがちだった」まで引けるようになる。

## 設計原則

- **罠ラベルは後知恵の物置にしない。** trap判定は機械検出可能な価格挙動の証拠
  (sweep & reclaim、イベント近接、レンジ異常)がある場合のみ付与。
  外れた週を無条件に「狩られた」と分類できる構造にすると誤読記録が自己弁護アーカイブに堕ちる。
- **原本ノートは不変更・追記専用。** 後知恵が当時の判断を上書きすると
  「その時点で何が見えていなかったか」という最重要データが消える。
- **結果とプロセスを分離。** 読みが誤りで結果が当たった週(D_lucky)こそ最危険の誤読記録。
- **開ループ終端。** 全周回はボスの裁定またはVaultへの着地で終わる。自律継続なし。

## Stage 0: 棚卸し(Python・一回きり)

- 週次ノート群を走査し、対象週リスト・欠損週・価格データ(週足OHLC、可能なら日足)の突き合わせ表を作成
- 各週の記載レベル(例: 160.6)を正規表現+LLM補助で抽出し levels 一覧を作成
  → 後段全Stageがこれを参照する

## Stage 1: regimeベクトル後付け(Python・決定論)

既存週次パイプラインのロジックを過去へ再実行し、各週 meta.yaml に追記:

```yaml
regime_vector:
  regime_label: ...
  curve_3m10s: ...
  intervention_stage: ...
  jp225_usd_adj_rs: ...
  atr_percentile_4h: ...
```

## Stage 2: outcome事実層 + trap候補フラグ(Python・決定論)

各週について翌1〜4週の実価格と記載レベルを機械照合。

```yaml
outcome_facts:          # 追記専用、原本ノートは不変更
  levels_stated: [160.6, ...]
  level_events:
    - level: 160.6
      pierced: true          # 終値ベースでなくヒゲで貫通
      pierce_depth_atr: 0.8  # ATR単位の貫通深度
      reclaimed_bars: 3      # N本以内に回収 → sweep疑い
      event_proximity: NFP   # 経済カレンダーjoin
  next_1w_direction: ...
  next_4w_direction: ...
  trap_candidate: true       # pierce+reclaim +(イベント近接 or レンジ異常)の合成条件
```

週足転換点でのサプライズ流動性剥奪は「貫通→短期回収」パターンとして痕跡が残る。

## Stage 3: 判定層ドラフト(LLMレーン・週ごとワンショット)

claudeレーン(または grok一次 → claude検証のクロスチェック)に、
当該週の note.md + outcome_facts **のみ** をスコープ注入して分類:

| ラベル | 意味 | 条件 |
|---|---|---|
| A_regime_misread | 環境認識自体が違った | — |
| B_timing | 読みは合っていたが時間軸がズレた | — |
| C_swept | 読みは妥当だったが流動性狩りに刺された | trap_candidate=true が必要条件 |
| D_lucky | 読みは誤りだが結果が当たった(要注意枠) | 「当たった理由が読み通りか」判定を含む |

- C は A/B と排他ではない。「誤読の上に狩られた」週は複合ラベル
- 併記必須: **「当時見えていなかった差分」一行**

## Stage 4: ボス裁定キュー → Vault wrapup

- Stage 3出力はドラフト扱いでレビューキュー(maintenance_logとは別ファイル)に積む
- ボスが承認・修正したもののみ、誤読/罠distilledとしてVaultへwrapup
- 当該週ノートへwikiリンクを張る。ここで開ループ終端

## 実行配分

| Stage | 実行主体 |
|---|---|
| 0–2 | ClaudeCode 一括バッチ |
| 3 | hermes -z 週次ループ |
| 4 | ボス手動裁定 |

Stage 0–2 は regimeベクトル後付けと同一バッチに相乗り(実装三段の一段目)。

## 位置づけ

Vault起動型運用(Vault = control plane / リポ = 実行層)への移行の一部。
戦略立案時の近傍検索は「現在状態 → 近傍期間 → 差分付きレポート」を基本フォーマットとし、
アナロジー提示と反証提示をワンセットにする。最終裁量は常にボスに残る。
