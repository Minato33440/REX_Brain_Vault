---
type: theme
status: active
created: 2026-07-04
updated: 2026-07-12
kind: driver-theme
first_instance: 2026-5-1_wk01
parent: "[[jpy_policy_complex]]"
source: "[[distilled-gm-2026-5]] .. [[distilled-gm-2026-7]]"
tags: [trade_brain, index, theme, carry, jpy, cross_asset, transmission]
---

# yen_carry_unwind — 円キャリー巻き戻し（伝達帯）

## 定義

低金利の円で調達したポジションの巻き戻しが、**USDJPY急落と同時にグローバルなリスク資産
（NASDAQ / 半導体 / BTC）を売る**クロス資産伝達。JPY政策複合（[[jpy_policy_complex]]）の**伝達帯**であり、
BOJ利上げ・介入・リスクオフが引き金になる。

> なぜ独立ノードか: 初回抽出では boj_hike / btc / risk に散っていたが、wk01(7-3)のX市況で
> 「NASDAQ・半導体・cryptoの**共通トリガー**」「最大の地雷」と名指しされた。
> JPY複合を全資産に繋ぐ機構＝逆引き上、単独ノードの価値が最も高い欠落だった。

### 非対称 ── 満載頻発・発火稀（照合による定義格上げ・2026-07-12）

**満載（全条件 present の setup）は頻発するが、発火は稀。** これは所見でなくノード定義とする。
6月は3週連続（6-5・6-19 確定 / 6-26 暫定1w）で満載読みが並んだが、carry は**一度も fired しなかった**。
したがって carry_unwind は「setup の存在」でなく「**outcome（fired / latent）**」で扱う。

- `2024_aug_replay` タグは**発火の予測子ではなく setup のテンプレート**。replay 記載＝満載であって発火ではない。
- 逆引きで満載週に当たったら、既定値は **latent（不発）**。fired と扱うには判定条件2/3 の実証が要る。
- このノードの生まれ（replay＝発火フレーム）を、実照合が反転させた: **replay は"起こりうる"の記録であって"起こった"の記録ではない。**

## 判定条件（機械寄り）

1. **USDJPYの急速な円高**（短期・数円規模の下落）
2. **同時にリスク資産が下落**（US100 / BTC / 半導体の相関的同時安）＝相関の同時性
3. **引き金がJPY要因に帰せる**（BOJ hike / 介入 / 日米金利差縮小）

⚠️ 3が別要因（米金利単独・地政学）なら本テーマでない。**円が主語か**で切り分け。
米発の通常リスクオフに円高が随伴しただけのものは carry_unwind に数えない（物置化防止）。

## 主要インスタンス（distilled収穫）

| 週 | tag | 内容 | outcome |
|---|---|---|---|
| 5-1_wk01 | `6_16_yen_carry_unwind_btc` (risk) | BOJ 6/16利上げ観測 → BTCへのcarry unwind懸念（初出） | 未照合 |
| 5-8_wk02 | `boj_hike_2024_aug_replay` (risk) | 2024年8月アナログの明示 | 未照合 |
| 6-5_wk01 | `yen_carry_unwind_amplifier` / `..._2024_aug_replay` | 増幅器・再演フレーム（満載読み） | **latent** → [[2026-6-5_carry_unwind_latent]] |
| 6-19_wk03 | `yen_intervention_flash_cascade` (risk) | flashカスケード（介入警戒キングピン） | **latent** → [[2026-6-19_intervention_carry_latent]] |
| 6-26_wk04 | `carry_unwind_simultaneous_riskoff_2024_aug` | 同時リスクオフの再演警戒 | **latent（暫定1w）** ／ coordination/claude 記録 |
| 7-3_wk01 | (X市況) | 「NASDAQ・半導体・cryptoの共通トリガー／最大の地雷」＝共通トリガーとして格上げ | 未照合（setup） |

## アナログ記憶

**2024年8月**（BOJ利上げ→円急騰→グローバル株急落）が参照テンプレ。複数週で `2024_aug_replay` タグ。
ただし上記の通り replay は setup テンプレートであって発火予測子ではない。
逆引き時はこのアナログに対する**差分**（今回と2024の違い）を必ず併記する。

## 運用含意（Rex戦略立案時）

- JPY複合の他2面（介入・BOJ）が動く局面では、carry-unwind を**全資産の共通伝達経路**として監視。
- 確認は USDJPY単体でなく**クロス資産の同時下落**で取る（相関の同時性＝判定条件2）。
- 満載週の既定値は latent。setup 一致だけで risk-off を外挿すると「もっともらしい物語」に落ちる。
- 薄商い・オーバーナイトで flash 発生しやすい → trap_watch と接続（ただし flash/sweep の実証は日次/intraday OHLC 待ち）。
- 帰着regime は `RiskOff`。発火＝株式エクスポージャー一段落としのトリガー候補。だが**発火は稀**という事前確率を持て。

## 照合状態（outcome）

fired/latent の照合を backfill v1 Stage 2-B で実施。**6月3週連続で fired ゼロ**:

| 週 | fired / latent | 根拠 |
|---|---|---|
| 6-5_wk01 | **latent**（確定） | double CB 通過も円安継続＋US100ラリー＝条件2の同時安なし（[[2026-6-5_carry_unwind_latent]]） |
| 6-19_wk03 | **latent**（確定） | 介入flash・carry とも不発。株安は円安のまま＝条件3不成立（[[2026-6-19_intervention_carry_latent]]） |
| 6-26_wk04 | **latent**（暫定1w） | 7-3で US100+0.72%/BTC+2.95%/VIX低下＝条件2の同時安不成立。4週窓未確定のため暫定 |

要約: 満載読みが3週並んでも carry は不発。「満載頻発・発火稀」の実証（6-26 は1週のみで暫定）。

## 変遷

| 時期 | 状態 |
|---|---|
| 5-1_wk01 | 初出（BOJ 6/16 → BTC carry unwind risk） |
| 6月 | 「2024 aug replay」フレームで反復・増幅器として認識 |
| 7-3_wk01 | X市況で共通トリガーとして明示格上げ → 第二号ノード化 |
| 2026-07-05 | 6-5 を照合 → latent 確定。outcome 軸を追加 |
| 2026-07-12 | 6-19 latent 確定・6-26 latent 暫定 → **定義格上げ**: 「満載頻発・発火稀」をノード定義に。replay=setupテンプレートと再定位 |

## 関連ページ

- [[jpy_policy_complex]] — 親（介入・BOJ経路と同一駆動の3面）
- [[README]] — 3 node-kind 設計根拠
- [[same_news_bear_bull_timeframe_split]] — 同じ機械寄り判定型の pattern（第一号）
- [[2026-6-5_carry_unwind_latent]] — 照合済み misread（latent 第一号）
- [[2026-6-19_intervention_carry_latent]] — 照合済み misread（latent 第二号）
- [[2026-07-05_backfill_workflow_v1]] — outcome/照合層の設計
- theme `quantum_crypto_risk`（BTC下落のもう一つの駆動・整備時にcarry-unwindと切り分け）
