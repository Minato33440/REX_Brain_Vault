---
type: misread
status: active
week: 2026-6-19_wk03
theme: [jpy_policy_complex, yen_carry_unwind]
label: [A_regime_misread, latent]
verified_against: [2026-6-26_wk04, 2026-7-3_wk01]
created: 2026-07-06
author: Rex (Broker帽子 / Claude)
adjudicated: "std版(Output-2)を正、strict版(Output-1)をsupersede。D_lucky棄却。"
source: "[[distilled-gm-2026-6]]"
tags: [trade_brain, misread, outcome, intervention, carry_unwind, latent]
---

# 2026-6-19 介入・carry — latent（駆動の誤帰属）

## 概要

6-19 は USDJPY 161.80 を新キングピンに置き、「162一段上げからの急落／159.5割れ→156→155」の
介入flash・carry伝達を主軸に読んだ。後続2週で **risk-off は来たが、JPY が主語ではなかった**。
介入flash・carry_unwind とも **latent（不発）**。誤ったのは方向でなく**駆動の帰属**。

## 時点Tの読み（2026-6-19_wk03）

- regime: Neutral（equities=up・risk-on回帰）。ダブル中銀通過＋停戦/ホルムズ再開。
- 新キングピン: `usdjpy_intervention_watch`（161.80＝2024/4介入直前水準）。「162→ズドン」「159.5割れ→156→155」。
- `risk:yen_intervention_flash_cascade`: 介入/レートチェック起点の円高flashがクロス資産へ伝播する想定。
- US100 30,900火傷ゾーン短期逆張り（上値追い厳禁）。

## outcome（照合: 6-26 / 7-3）

### Stage 2-A base層（週足close）
| 資産 | 6-19 | 6-26 | 7-3 | 照合 |
|---|---|---|---|---|
| USDJPY | 161.289 | 161.805 | 161.337 | 円安高値圏維持。159.5/156/155 未達、深い円高flashなし |
| US100 | 30,406 | 29,118 | 29,329 | 6-26 -4.2%下落（方向は慎重postureと合致・駆動は別） |
| BTC | 62,896 | 59,721 | 61,485 | 下落→反発。円高同時性なし |
| VIX | 16.4 | 18.41 | 16.15 | 18超え再閉鎖→再開。介入flash主導でない |

### Stage 2-B theme署名
- **介入面**: `flash_occurred: false`。161.80高値圏滞在（partial pressure）はあったが、実弾介入flash・159.5割れは未発生 → **latent/shallow**。
- **yen_carry_unwind**: `cross_asset_simultaneous: false` / `fired_or_latent: latent`。6-26 は US100/BTC 安だが USDJPY 円安（条件2不成立）、駆動は PCE/Goolsbee・Mag7メモリ・イラン再エスカ（条件3不成立＝円が主語でない）。

## 判定（Stage 3）

- label: **A_regime_misread（駆動の帰属）** ＋ 介入・carry ともに **latent**。
- **D_lucky は棄却**（裁定）: US100 の下落方向的中を carry/JPY thesis の"lucky"として D_lucky に数えると、
  carry_unwind 条件2/3 が断つべき「thesis↔outcome の結合」を復活させてしまう。方向的中は別駆動によるもので、
  thesis から切り離す（＝A_regime_misread）方が index の反・物語化設計と整合する。
- C_swept なし（sweep/reclaim の証拠なし）。
- **当時見えていなかった差分**: 161-162高値圏は即flashを生まず、IMF残弾1発・片山-ベッセント会談・財務省サプライズ姿勢報道が
  「レンジを長く踏ませながら警戒だけ増幅する」構造だった。先に米インフレ・メモリ・地政学が risk-off を駆動した。

## 教訓（strict版から保全）

**方向的中は因果 thesis を検証しない。** 慎重posture はどれかの risk-off driver でしばしば方向的に確認されるが、
それを「介入/carry thesis が当たった」証拠に使ってはならない。6-19 の US100 下落は、慎重posture の的中であって
JPY thesis の的中ではない。逆引きで「6-19 でも介入警戒が効いた」と読むと、latent を fired と誤登録する。

## 関連ページ

- [[yen_carry_unwind]] — 親。6-5 に続く latent 第二事例（6月通して carry は一度も fired していない）
- [[jpy_policy_complex]] — 介入面 latent
- [[2026-6-5_carry_unwind_latent]] — 先行 latent（満載・不発）
- [[distilled-gm-2026-6]] — 正本
- [[2026-07-06_broker_register_decision]] — 本記録を生んだ A/B の裁定（std版採用）
