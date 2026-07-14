---
type: theme
status: active
created: 2026-07-04
kind: driver-theme
source: "[[distilled-gm-2026-1]] .. [[distilled-gm-2026-7]]"
tags: [trade_brain, index, theme, jpy, boj, intervention, carry]
---

# jpy_policy_complex — 円政策複合

## 定義

USDJPYを動かす**因果的に連結した3つの面**を一つの駆動テーマとして束ねる。独立テーマでない:

1. **MOF介入** — 財務省の価格トリガー介入・USDJPY水準防衛（短期flash）
2. **BOJ利上げ経路** — スケジュール会合・金利差（中期方向）
3. **円キャリー巻き戻し** — クロス資産への伝達帯 → **専用ノード [[yen_carry_unwind]]**（第二号）

逆引き原則: **介入を引くならBOJ経路とcarry-unwindも必ず一緒に引く**。同一駆動の3面だから。

## 統合の理由（Sonnet 9theme からの修正）

初回抽出は yen_intervention(11週) と boj_hike(13週) を**別テーマ**にしたが、両者は8週重複し、
`yen_carry_unwind` が両者を全資産に繋ぐ伝達帯として散在（boj_hike/btc/risk に分裂）。
分割したままだと「介入」逆引きが因果連結したBOJ週・carry週を取りこぼす。→ 複合として統合。

## 3面の週リスト（distilled収穫）

**MOF介入面 (11週)**: 1-24_wk03 / 2-6_wk01 / 3-13_wk03 / 4-17_wk03 / 4-24_wk04 / 5-1_wk01 / 5-8_wk02 / 5-29_wk05 / 6-5_wk01 / 6-19_wk03 / 6-26_wk04
主要tag: `intervention_bottom_154_00`(5-1) / `usdjpy_160_kingpin`(6-5) / `intervention_watch_2024_apr_replay`(6-19) / `coordinated_intervention_asymmetry_155` `usdjpy_imf_ammo`(6-26)

**BOJ利上げ経路面 (13週)**: 3-13 / 3-20 / 3-27 / 4-10 / 4-17 / 4-24 / 5-1 / 5-8 / 5-15 / 5-22 / 5-29 / 6-5 / 6-19
主要弧: BOJ 4-28 no-hike → 6-16 rate hike（`BOJ_6_16_main_event`→`BOJ_6_16_rate_hike`→`double_central_bank_6_16_17_passed`）

**円キャリー巻き戻し面**: → [[yen_carry_unwind]]

統合union: 約16-18週（JPYが主語の局面）。

## 運用含意（Rex戦略立案時）

- USDJPY戦略時は**3面を同時に読む三層**: 介入警戒（短期flash）× BOJ経路（中期方向）× carry-unwind（クロス資産リスクオフ）。
- 本流は円安トレンド → 基本は戻り高値売り。介入・BOJ利上げ・carry-unwindは**円高方向のflash/転換リスク**として重なる。
- 薄商い・オーバーナイトで介入flash が増幅（trap_watch と接続）。

## サブノード化予定（分解は後）

`mof_intervention` / `boj_rate_path` はデータが積み、逆引きの不都合が出た段で個別ノードへ分解。
現状は本複合ノード内の面として保持。`yen_carry_unwind` のみ高価値のため先行ノード化（第二号）。

## 変遷

| 時期 | 状態 |
|---|---|
| 2026-07-04 | Sonnet 9theme の yen_intervention＋boj_hike を統合、carry_unwind を伝達帯として分離ノード化。3-kind枠の driver-theme 第一陣。 |

## 関連ページ

- [[yen_carry_unwind]] — 伝達帯（第二号・専用ノード）
- [[README]] — 3 node-kind 設計根拠
- regime `RiskOff` — carry-unwind発火時の帰着regime
- distilled: [[distilled-gm-2026-5]] / [[distilled-gm-2026-6]] / [[distilled-gm-2026-7]]（6-16利上げ前後が密度域）
