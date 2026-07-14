---
type: misread
status: active
week: 2026-6-5_wk01
theme: yen_carry_unwind
label: [A_regime_misread, latent]
verified_against: [2026-6-19_wk03, 2026-6-26_wk04]
created: 2026-07-05
author: Rex (Broker帽子 / Claude)
source: "[[distilled-gm-2026-6]]"
tags: [trade_brain, misread, outcome, carry_unwind, latent]
---

# 2026-6-5 carry_unwind — 満載・不発（latent 第一号）

## 概要

carry_unwind ノードの **初の latent インスタンス**。6-5 は carry_unwind を最大限に満載で読んだが、
トリガー（BOJ 6/16 = double CB）を通過してなお**不発**だった。逆引きで参照される時、この週は
「risk-off の前例」ではなく「満載でも不発だった事例」として引かれなければならない。

## 時点Tの読み（2026-6-5_wk01）

- `yen_carry_unwind_amplifier=on`: 全資産の増幅器。USDJPY 160.293・円ショート満タン・BOJ 6/15-16利上げ観測・2024年8月replay 明示。BTC/日本株/半導体/金の連鎖を想定。
- 方向posture: 米株/日本株/BTC=戻り売り・ヘッジ優位。VIX 21.51 でゲート閉=構造的リスクオフ警戒域。
- USDJPY: 「159.5割れ→156→155」の円高巻き戻しを想定（介入 or BOJサプライズ起点）。
- ※ 明示的に「監視のみ・ノーポジ推奨・ポジション軽く」= 建玉は取っていない。

## outcome（照合: 6-19 / 6-26 canon）

### Stage 2-A base層（週足close）
| 資産 | 6-5 | 6-19 | 6-26 | 方向 | 予測との整合 |
|---|---|---|---|---|---|
| USDJPY | 160.293 | 161.289 | 161.805 | 円安継続 | 逆（円高巻き戻しを想定） |
| US100 | 28,957 | 30,406 | 29,118 | 次1w risk-onラリー(+5.0%) | 逆（戻り売り優位を想定） |
| BTC | 60,922 | 62,896 | 59,721 | 低位もみ合い | 不発（$64K→$49K型カスケード想定） |
| VIX | 21.51(閉) | 16.4(再開) | 18.41 | risk-onへ解消 | 構造的リスクオフ警戒が剥落 |

記載レベル未接近: USDJPY「159.5→156→155」（真逆に上昇）／ US100「27,989割れで下加速」（未到達・上抜け方向）。

### Stage 2-B theme署名（yen_carry_unwind）
- `cross_asset_simultaneous: false`（円高×リスク資産同時安は発生せず＝円安＋US100ラリー）
- `fired_or_latent: latent`（トリガー double CB を通過したが不発。6-19 で double_..._passed → risk-on relief）
- 4週窓後半に risk-off は来た（6-26 Equities Down）が、駆動は PCE/Goolsbee・Mag7メモリ・イラン再エスカで、
  USDJPY は 161.8 の**円安のまま** → 判定条件3「円が主語」を満たさず＝**これは carry_unwind ではない**。

## 判定（Stage 3）

- label: **A_regime_misread（方向）** ／ **process-correct**（観測優位・ポジション軽く・pivot=double CB を正しく指名）
- 建玉の誤りなし（監視のみ）＝ C_swept でも D_lucky でもない。誤ったのは方向バイアスのみ。
- **当時見えていなかった差分**: 「イベント通過＝リスクオフ発火」でなく「イベント通過＝不確実性剥落の relief」。
  6-5 は 2024aug replay の下方を weight したが、実際の非対称は "満載のまま通過 → 上へ" だった。

## ノードへの含意（逆引き時の使い方）

- carry_unwind が**満載（全条件present）でも不発たりうる**ことの実証。6-5 はその最初の documented ケース。
- 逆引きで 6-5 に当たったら、risk-off の前例として外挿してはならない。**トリガー通過→不発**の反例として提示する。
- 判定の分岐は [[yen_carry_unwind]] 条件2（クロス資産同時性）と条件3（円が主語）。本週はどちらも満たさず＝latent。
- 教訓の一般形: 「満載の setup」と「発火」は別。逆引きは setup の一致でなく **outcome（fired/latent）** で重み付けする。

## 関連ページ

- [[yen_carry_unwind]] — 親ノード（本記録は latent 第一号インスタンス）
- [[distilled-gm-2026-6]] — 正本（6-5_wk01 / 6-19_wk03 / 6-26_wk04）
- [[2026-07-05_backfill_workflow_v1]] — Stage 2-B `fired_or_latent` の初適用
