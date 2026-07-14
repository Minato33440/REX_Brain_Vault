---
type: index_readme
status: active
created: 2026-07-04
updated: 2026-07-12
author: Rex (Broker帽子)
---

# bridges/trade_brain/index — 逆引きインデックス層

## 役割

Trade_Brain distilled（canon）への**逆引き検索層**。Vault側 control-plane、Broker書込、canon由来のみ。
distilled へ wikilink で戻すだけで、**生データは複製しない**（ミラーでない）。
実Trade時に Rex が「現在の状態 → 近傍期間 → 差分付きレポート」で戦略材料を引くための入口。
`misreads/` もこの入口の一部（下記参照）——setup一致だけでなく outcome 側の重み付けを持たせるための必須参照。

## 粒度の決定（Target B → 3 node-kind）

index_feed_raw（24週）で判明: **raw-tag は signal 141種でほぼ全単発** → tag単独では連想ノードにならない。
初回はregime系譜/theme束9個の2軸へ束ねたが、その9個は**3種類の別物が混在**していた。
逆引きの因果精度のため、index を **3つの node-kind** で構成する（+ 横断の pattern）:

- **regime**（市場全体の状態）: RiskOn / Neutral / GoldBid / RiskOff / RiskOff+EnergyShock 〔第一軸〕
- **theme**（個別の駆動力）: geopolitical_oil / rates_curve / ai_semi / jpy_policy_complex / yen_carry_unwind / quantum_crypto_risk 〔第二軸〕
- **instrument**（銘柄の技術水準・挙動）: us100_levels / gold挙動 / btc trend … 〔第三軸〕
- **system**（Rex自身の機構）: vix_add_risk_gate（Add-risk-gate開閉履歴）
- **pattern**（上記を横断する再利用可能な構造）: same_news_bear_bull_timeframe_split 〔第一号〕

**銘柄バケツを避ける**: gold/btc/us100 を"テーマ"扱いすると低情報になる（毎週その銘柄は動くが駆動はバラバラ）。
駆動は theme へ、技術水準は instrument へ分離する。gold-as-theme が GoldBid-regime と重複するのは、この分離で解消。

## ディレクトリ

```
index/
├── README.md
├── regime/       ← (将来) regime系譜ノード
├── themes/       ← 駆動テーマ（jpy_policy_complex, yen_carry_unwind を配置）
├── instruments/  ← (将来) 銘柄の技術・挙動ノード
├── system/       ← (将来) Rex機構（vix_add_risk_gate 等）
└── patterns/     ← 横断パターン（same_news_bear_bull_timeframe_split）
```

misreads/ は index 外だが同格の canon 由来層（backfill workflow の着地先・誤読/罠の教訓）。逆引き入口としては index と一体で読む——setup一致でなく outcome 重み付けのための必須参照。advisor scope からの除外ではない（2026-07-12 訂正：当初案の抜けだった）。

## ノード schema

frontmatter（type / status / created / source）→ 定義 → 判定条件 → 初出インスタンス
→ 運用含意 → 変遷 → 関連ページ（distilled へ wikilink）。
判定条件は機械寄りにできる部分を明示し、**物置化を防ぐ**（例に漏れる正面衝突は別扱いへ回す）。

## 構築ステータス（確信度で刻む）

- **済（高確信）**: 3 node-kind 枠 / `jpy_policy_complex` 統合 / `yen_carry_unwind`（第二号）/ `same_news_bear_bull_timeframe_split`（第一号・pattern）
- **保留（走らせながら出す）**: gold/btc の駆動分解、`quantum_crypto_risk`、us100等の instrument ノード、regime/system 各ノード。週が積んで逆引きの不都合が出た所から起こす。
- theme境界は設計選択。継承でなくBossと引き直す（分類の物置化防止）。

## 昇格規律（一方向）

```
scratch/claude/ の生抽出（executor）
    ↓ Broker蒸留
    ↓ Boss承認
index/ へ昇格（canon由来のみ・生データは置かない）
```

coordination/（append-only handoff・repo側）が executor→Broker の記録経路。
index/ は承認済みの蒸留物だけを受け取る。
