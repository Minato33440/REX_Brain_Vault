---
type: design_doc
status: draft            # canon昇格はボス承認まで
version: v1
supersedes: "[[2026-07-04_backfill_workflow_v0]]"
created: 2026-07-05
author: Rex (Broker帽子 / Claude)
scope: Trade_Brain backfill — outcome/照合層（codex一段目フィードバック反映）
related:
  - "[[2026-07-04_backfill_workflow_v0]]"
  - "[[2026-06-27_belly_elevated]]"
  - "[[yen_carry_unwind]]"
  - "[[same_news_bear_bull_timeframe_split]]"
tags: [trade_brain, backfill, misread_log, outcome, workflow]
---

# Backfill Workflow v1 — outcome/照合層
codex 逆引き一段目(2026-7-3_wk01_reverse_lookup_dryrun)の実測を反映

## v0 からの変更点（要旨）

1. **Stage 1 は完了扱い**。regimeベクトル再生成は不要——index_feed_raw(24週・regime系譜＋theme束)で既に収穫済み。
2. **Stage 2 を theme固有の outcome署名に具体化**。v0 の汎用レベル照合(貫通/回収/方向)は base層として残し、
   その上に driver-theme ごとの固有チェックを重ねる。← codex §4-3 の実測要求。
3. **Stage 3 を両利き化**。分類ドラフトは codex、判定確定は claude(Broker)。役割分担どおり canon寄り判定は Broker所有。
4. **出力先を両利きレーン規約に整合**(scratch/<engine>/ ・ coordination/<engine>/ ・ Vault misreads/ 昇格)。
5. **specimen先行**を明記。6-5 / 6-19 / 6-26(逆引きで実際に使われた3週)を手で先に通し、証明後に系統化。

## 設計原則（v0 から継承・不変）

- 罠ラベルは後知恵の物置にしない。trap判定は機械検出可能な証拠(sweep&reclaim・イベント近接・レンジ異常)がある時のみ。
- 原本ノートは不変更・追記専用。後知恵で当時の判断を上書きしない。
- 結果とプロセスを分離。読み誤り×結果的中(D_lucky)が最危険。
- 開ループ終端。全周回はボス裁定か Vault着地で終わる。

> codex一段目の核心的裏付け: outcome未照合のまま逆引きすると「6-5/6-19/6-26 からかなり
> もっともらしい物語が作れてしまう」(codex自己監査5点)。照合層はこの物語生成力を抑える装置。
> ノードを増やす前に照合を入れる、が実測の指す順序。

## Stage 1: regime/theme feed（完了・参照のみ）

- 出所: `scratch/claude/index_feed_raw.md`(24週・regime系譜5・theme束→3 node-kind へ再編済み)
- 本v1では再生成しない。outcome層はこの feed の週リストを入口に使う。

## Stage 2: outcome 事実層（base + theme固有署名）

各週の「時点Tの読み」に対し翌1〜4週の実価格・実挙動を機械照合。原本不変・追記専用。

### 2-A. base層（v0 継承・全週共通）

```yaml
outcome_facts:
  levels_stated: [...]           # prediction_seed / distilled から
  level_events:
    - level: <値>
      pierced: <bool>            # ヒゲ貫通
      pierce_depth_atr: <float>
      reclaimed_bars: <int>      # N本以内回収 → sweep疑い
      event_proximity: <event>   # 経済カレンダーjoin
  next_1w_direction: ...
  next_4w_direction: ...
  trap_candidate: <bool>         # pierce+reclaim +(イベント近接 or レンジ異常)
```

### 2-B. theme固有署名（codex §4-3 反映・該当themeが立つ週のみ）

各 driver-theme は固有の outcome署名を持つ。base層に加えて該当週で検証:

| theme | outcome署名（機械照合対象） | 判定が効く node |
|---|---|---|
| jpy_policy_complex / 介入面 | USDJPY高値圏から実際に円買いflashが発生したか（発生/不発）・発生なら深度と回収 | [[jpy_policy_complex]] |
| yen_carry_unwind | USDJPY円高と US100/BTC/半導体下落の**同時性**が実際に出たか（相関の同時発生 y/n） | [[yen_carry_unwind]] 判定条件2の裏取り |
| same_news_bear_bull | 短期側の売りが実際に何日続き、中期側の買いがどの時間窓で復活したか（時間窓別） | [[same_news_bear_bull_timeframe_split]] |
| vix_gate(将来node) | <18 / >18 ゲートが実際の株式exposure調整に効いたか | system/vix_add_risk_gate(未整備) |

```yaml
theme_outcome:
  yen_carry_unwind:
    cross_asset_simultaneous: <bool>   # 円高とUS100/BTC/半導体が同時に下落したか
    fired_or_latent: fired | latent    # 発火 or 地雷待機のまま
  intervention:
    flash_occurred: <bool>
    flash_depth: <値> / null
  same_news_split:
    short_side_days: <int>             # 短期売りの継続日数
    mid_side_recovery_window: <期間> / pending
```

**trap → pattern 接続**: intervention面の flash_occurred＋base層の trap_candidate が揃う週は、
codex提案の `patterns/thin_liquidity_flash_trap`(米休場/薄商い/介入flash/節目sweep)の一次インスタンス候補。

## Stage 3: 判定層（両利き・codexドラフト → claude確定）

該当週の note/distilled + outcome_facts + theme_outcome **のみ**をスコープに分類:

| ラベル | 意味 | 条件 |
|---|---|---|
| A_regime_misread | 環境認識自体が違った | — |
| B_timing | 読みは合っていたが時間軸ズレ | — |
| C_swept | 読みは妥当だが流動性狩りに刺された | trap_candidate=true 必須 |
| D_lucky | 読み誤り×結果的中(最危険) | 「的中理由が読み通りか」判定含む |

- C は A/B と排他でない(複合可)。
- 併記必須: 「当時見えていなかった差分」一行。
- **両利き分担**: codex が分類ドラフトを `scratch/codex/` に生成 → claude(Broker)が確定し
  `coordination/claude/` に記録。判定の最終所有は Broker(canon寄りのため)。

## Stage 4: ボス裁定 → Vault 昇格

- Stage 3確定分はレビューキューへ。ボス承認分のみ `bridges/trade_brain/misreads/` へ misread記録として昇格。
- 当該週 distilled へ wikilink。開ループ終端（生産側）。消費側スコープは [[../../../bridges/trade_brain/index/README]] 参照。

## 実行配分（両利きレーン整合）

| Stage | 実行主体 | 出力先 |
|---|---|---|
| 1 | 完了(参照のみ) | scratch/claude/index_feed_raw.md |
| 2 | Python(決定論) or codex | scratch/<engine>/ |
| 3 | codexドラフト → claude確定 | scratch/codex/ → coordination/claude/ |
| 4 | ボス手動裁定 | bridges/trade_brain/misreads/(Vault) |

## specimen先行スコープ

まず **6-5 / 6-19 / 6-26** の3週(逆引きで実使用)を手で通す。うち1週を最初の specimen として
Stage 2-3 を通し、outcome/misread記録の型を確定 → 証明後に残り2週、その後 Python化を判断。
※ 全24週の一括Python化は型確定後。

## 既知の依存（未解決）

- **regime軸の曖昧さ**: codex §1-2/§5 が指摘。指示書の `RiskOff` と機械regime `Equities Down` の関係が未定義。
  regime起点の outcome照合を綺麗に回すには、`regime/Equities_Down` と `regime/RiskOff` の関係を先に定義する必要。
  本v1の theme固有署名は regime非依存なので当面は進められるが、regimeノード整備時に要決着。

## 位置づけ

Vault起動型運用の一部。近傍検索は「現在状態 → 近傍期間 → 差分付きレポート」を基本形とし、
アナロジー提示と反証提示をワンセットにする。照合層はこの反証側に実データの裏付けを与える。最終裁量は常にボス。
