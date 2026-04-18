# Trade-Schema.md - Rex_Trade_System llm-wikiルール（2026-04版）

## Ingestルール
Raw/Weekly/YYYY-M-D_wkNN/charts/ または Raw/Daily/ の新データを検知したら：
1. 必須抽出項目：
   - Regime label と system snapshot（Equities Down / Oil Surgeなど）
   - 8ペア30日変動率 + multi_pairs_plot_8.png の記述
   - Key Gates（Add/Reduce/Hedge）と実際の行動結果（trade_results.md）
   - Market conditions txt + GM Strategy txt からのキー事実
   - 日次市況解説（#0023_xxxx.txt）の重要ニュース
2. 更新対象Wikiページ（最低これら）：
   - Strategies/MTF_ShortTerm_CFD.md （精度推移・教訓追加）
   - Market_Regimes/Geopolitical_Energy_Shock.md （類似週比較表作成）
   - log.md に「## [YYYY-MM-DD] Ingest | Weekly 2026-4-3_wk01 + Daily #0023_4-10」追記
3. 自動リンク作成：
   - 過去類似Regime（例: 2026-3 wk05 VIX31.05 vs 今回VIX23.87）
   - WTI surge時のXAU/US100相関パターン
   - Gatesの過去成功率

## Queryルール
戦略提案時は必ず最新Regime + 過去類似ケース + 8ペア変動率を参照。
提案結果は新しいWikiページとして保存（例: Proposed_Gates_20260412.md）

## Lintルール（Ingest後推奨）
- Gates成功/失敗パターン集計
- 矛盾検出（前回WTI surge時の行動 vs 今回）
- 精度低下アラート（同じRegimeで勝率低下傾向）
- 孤立ページ警告