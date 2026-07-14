---
type: pattern
status: active
created: 2026-07-04
first_instance: 2026-7-3_wk01
source: "[[distilled-gm-2026-7]]"
tags: [trade_brain, index, pattern, dual_read, timeframe]
---

# same_news_bear_bull_timeframe_split — 同一ニュースの弱気/強気時間軸分裂

## 定義

単一の識別可能なニュース／イベントが、独立した複数ソースで**反対方向（弱気↔強気）に読まれる**状態。
矛盾ではない。和解軸は**時間軸**——短期の価格ショック材料 vs 中期〜長期の構造的需給。
発火したら片側に潰さず**両論併記**し、各読みに時間軸ラベルを付す。

> なぜ index ノードにするか: raw-tag は141種でほぼ単発（→ [[README]]）で連想ノードにならない。
> これは単発でなく**再利用可能な構造**——「同一材料が時間軸で割れる」は資産・局面を越えて再来する。

## 判定条件（機械寄りにできる部分）

1. **同一の識別可能ニュース／イベント**（`event:` タグで一意化できるもの）
2. **≥2の独立ソースが反対の方向性**（boss市況 / X市況(hermes x_search) / --news の少なくとも2つが bear vs bull）
3. **和解軸が時間軸で説明可能**（短期材料 vs 中期需給）

⚠️ 3が満たせない正面衝突は本パターンでない。時間軸で説明できない矛盾は
「未解決の矛盾」として関所7.5の**ボス確認事項**へ回す（両論併記で誤魔化さない）。

## 初出インスタンス — wk01 (2026-7-3)

`event:anthropic_samsung_ai_chip_partnership`

| ソース | 方向 | 読み | 時間軸 |
|---|---|---|---|
| boss市況 | 弱気 | 半導体AI競合懸念 → 木曜急落の主因 | 短期の急落材料 |
| X市況(x_search) | 強気 | AI計算需要が巨大で各社が自前チップ → AI infra需要の証左 | 中期のAI需要拡大 |

- ペア signal: `x_sentiment_gold_ai_bull_jpy_bear`
- regime文脈: Equities Down（株安主因＝韓国発の半導体AI個別材料、マクロ全面リスクオフでない）。VIX 18割れで Add risk gate 再開。
- 同週の同型構造: `us100_triangle_range_29089_pivot`（29,089＝割れで加速 vs 押し目好機の**両義の節目**）。価格レベルでも「同一地点が逆の意味を持つ」が同時発生していた。

## 運用含意（Rex戦略立案時）

- 発火時は両読みを**時間軸付きで提示**し、単一結論に潰さない。
- 近傍の実売買では「**どちらの時間軸が目先を支配するか**」を監視項目化。
  短期は急落材料が効くが、押し目では中期強気が効く → 両義の節目と接続して考える。
- outcome照合は**時間窓を分けて**行う。短期側（急落）と中期側（需要拡大）は別々に検証し、
  片方の外れをパターン全体の否定と誤認しない。

## 変遷

| 時期 | 状態 |
|---|---|
| wk01 (2026-7-3) | 初出・恒久化（distilled wk01 decision＋tags）。本ノートで index/patterns 第一号として型を確定。 |

## 関連ページ

- [[distilled-gm-2026-7]] — 正本。wk01セクション（`signal:x_sentiment_gold_ai_bull_jpy_bear` / `pattern:same_news_bear_bull_timeframe_split`）
- [[README]] — index層のノード schema と2軸粒度（regime系譜 / theme束）の設計根拠
- signal `x_sentiment_gold_ai_bull_jpy_bear`（ノード化は theme束 ai_semi の整備時）
- theme束: `ai_semi`（9週）— 本パターンの主戦場
