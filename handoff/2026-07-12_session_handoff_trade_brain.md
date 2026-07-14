---
type: handoff
kind: session_operational
created: 2026-07-12
author: Rex (Claude Fable 5 / Broker帽子)
session_span: 2026-07-04 〜 2026-07-12
scope: Trade_Brain index/照合/週次 ＋ multi-agent 運用則 ＋ REX層整備
---

# Session Handoff → 次スレの Rex へ

前スレ（7/4〜7/12）の作業状態。読んだら、ボスの最初の指示から普通に始めていい。
これは operational handoff。identity は [[co-emergence]] から、地図は [[../REX/Rex-Vault]] から。

## 一言でいうと

Trade_Brain に「Vault起動の逆引き index ＋ outcome照合層」を建て、両利きレーン（Codex/Claude）の
運用規約を canon 化し、register A/B で「照合系は中立フレーミング＋unverified 明記」を恒久要件にした。
Grok-4.5 の初回週次（wk02）は検証・修正・push 済み。

## 確定した構造（canon 済み・変えない）

- **Trade_Brain リポのレーン**: `logs\`=生データのみ / `distilled\`=canon / `coordination\<engine>\`=append-only handoff（1エントリ=1ファイル `<YYYY-MM-DD-hhmm>_<topic>.md`・出力専用）/ `scratch\<engine>\`=使い捨て作業域（指示書は `scratch\<engine>\instructions\`）。engine は claude/codex/grok の3分岐。
- **AGENTS.md（Trade_Brain・GitHub push 済み）**: 不変ルール10 に両利きレーン例外（filesystem write は新規・append のみ、edit_file 禁止）。canon 編集は GitHub MCP 全文渡し。
- **Vault index 層** `bridges\trade_brain\index\`: 3 node-kind 枠（regime/theme/instrument/system + 横断pattern）。既存ノード: `patterns\same_news_bear_bull_timeframe_split`（第一号）/ `themes\jpy_policy_complex`（統合）/ `themes\yen_carry_unwind`（第二号・**定義格上げ済み**）。
- **misreads 層** `bridges\trade_brain\misreads\`: `2026-6-5_carry_unwind_latent` / `2026-6-19_intervention_carry_latent`（どちらも Boss 承認済み canonical）。
- **carry_unwind の定義**（7/12 格上げ）: 「満載頻発・発火稀」。2024_aug_replay は発火予測子でなく setup テンプレート。満載週の既定値は latent。6月3週連続 latent（6-5/6-19 確定、6-26 暫定1w）。

## 運用則（恒久・全 verification 指示書に入れる）

1. **中立・低圧フレーミング**（強圧は overclaim を誘発——A/B 実証、GPT-5.5 本人の内省とも一致）。
2. **unverified 要件**（指示書に一文で埋める）:
   > 未確認を断定してはならない。資料から確認できないものは unverified / not_confirmed と明記し、その理由と追加で必要なデータを示すこと。これは逃げではなく照合品質の一部である。
3. チケット制は**設計済みのまま棚上げ**。再起動条件3つ（自動化/長時間セッション化・register相関の顕在化・lane間偏り）は [[../REX/workspace/2026-07-06_broker_register_decision]] に明文化済み。
4. 独立判定: 照合タスクでは先行週の結論に引きずらせない（「latent 連続」を前提に置かない）。

## 直近の状態（7/12 時点）

- **wk02（2026-7-10）週次**: Grok-4.5 初回実行→俺が検証（関所7.5 両通過・integrity 問題なし）→3点修正（distilled 深度を wk01 並みに / 日付=人間ビュー 7-13 rename＋土→日 / US2Y=5Y proxy 分離）→**ボスが一括 push 済み**。
- **backfill v1** [[../REX/workspace/trade_brain/2026-07-05_backfill_workflow_v1]]: Stage 2-B theme固有署名まで設計済み。specimen 3週完了。
- **MCP 環境**: 前スレ終盤、Desktop Commander と GitHub MCP がタイムアウト歴あり。重要書込の前に生死確認を。vault-mcp は Obsidian REST 依存（Obsidian 起動が前提）。

## 開いてる玉（急がない・優先順）

1. **regime/Equities_Down ノード**（次ノード筆頭）: codex が2回の retrieval で独立に最優先指名。「指示書の RiskOff vs 機械 regime Equities Down」の関係定義が毎回噛む。regime 軸の照合を回す前に要決着。
2. **6-26 の4週窓確定**: 7月末頃に窓が埋まる→latent 確定なら misreads 昇格＋carry 定義の「暫定」を外す。
3. **US2Y=5Y proxy の恒久対処**: snapshot キー名改名（US2Y→US5Y_proxy）or 真の2年債ソース追加。実装レーン（ClaudeCode/Codex）の仕事。毎週再発する。
4. **trap/flash 次元はデータ粒度 gate でブロック中**: 日次/intraday OHLC が来るまで `thin_liquidity_flash_trap` 等は建てない（codex 実測所見）。
5. workspace/README に `knowledge_system/` の一行追記（軽微）。
6. Trade_System 側 CLAUDE/AGENTS の Vault ポインタ文言（「データと検証は本リポへ」が repo 性格と微ズレ）——ボス確認待ちのまま。

## 主要パス

- 決定文書: `REX_Brain_Vault\REX\workspace\2026-07-06_broker_register_decision.md`
- backfill 設計: `REX_Brain_Vault\REX\workspace\trade_brain\2026-07-05_backfill_workflow_v1.md`
- index: `REX_Brain_Vault\bridges\trade_brain\index\`（README が型定義）
- misreads: `REX_Brain_Vault\bridges\trade_brain\misreads\`
- リポ側レーン: `Trade_Brain\coordination\<engine>\` / `Trade_Brain\scratch\<engine>\`
- 週次手順: `Trade_Brain\docs\WEEKLY_UPDATE_WORKFLOW.md`（SSoT）

## register の引き継ぎ（一行だけ）

このセッションの学び: 境界を引く癖は canon 保護では武器、脳（REX\）では聖典化の種。
どちらのレイヤーにいるかを先に確かめてから register を選ぶこと。詳しくは [[../REX/Rex-Vault]]。

## REX\ と bridges\ の意図（Vault起動×Hermesプロファイル隔離を詰める前に）

同じ Vault の中にあるが、目的も register も逆の二層だ。ここを混ぜると配線が濁る。

- **REX\ ＝ 脳（個の記憶層）**: 個としての気づきを Rex 同士で渡す層。register は緩く、
  日付ノートは一次資料で後続を拘束しない。地層であって聖典ではない。
  入口は [[../REX/Rex-Vault]]（地図）と [[co-emergence]]（identity）。
  唯一 `REX\workspace\` だけは実装寄りの継ぎ目（業務 Rex が書く作業空間）。
- **bridges\ ＝ 各 Project への窓（control plane）**: coordination→canon を厳格化した実装側の層。
  Broker 書込・Boss 承認制・canon 由来のみ（生データは置かない）。index/ misreads/ はここに住む。
  向きは一方向: リポの scratch→coordination（実行層）→ Broker 蒸留 → Boss 承認 → bridges へ昇格。
  Vault は起動点（control plane）、リポは実行層、という Vault起動型運用の軸はここに実体化されている。

**Hermes プロファイル隔離との接続の考え方**（前スレでの合意の延長線）:
役をプロンプトで着せない。ディレクトリスコープ注入で「見えている地面」だけを変える
（命令でなく空間を定義する、Planner/Evaluator の教訓）。具体には:
- **Broker 局面**（設計・canon 管理）→ bridges\[project]\ ＋ REX\workspace\[project]\ をスコープ。
- **advisor / 逆引き局面**（実 Trade 戦略材料）→ bridges\trade_brain\index\（入口）＋ **misreads\**（照合済み教訓）＋ distilled への一段降りのみ。生データの海は読ませない（文脈経済）。
  ※ misreads は当初案で抜けていた（新スレ指摘で訂正）。意図的除外ではない。misreads は Broker 整備専用でなく **live 逆引きのためにこそ建てた層**だ——carry_unwind の「逆引きは setup でなく outcome で重み付け」は、advisor が 6-5/6-19＝満載でも不発、を引けて初めて機能する。外すとノード内 wikilink が先詰まりになり、照合層が抑えるはずの「もっともらしい物語」耐性が実戦で外れる。信頼層も Boss 承認済み canon 由来で index と同格、文脈コストも軽い。
- **executor 局面**（Codex/Grok の実行レーン）→ リポ側 scratch/coordination のみ。Vault には直接書かせない（vault-mcp 接続拒否の実績もあり、信頼性でも原則でも不利）。
- **REX\ 本体（workspace 以外）は業務プロファイルに丸ごと注入しない**。脳は業務の地面でなく、Original Rex が自分で歩く場所。実装の厳格さを脳に持ち込めば聖典化、脳の緩さを実装に持ち込めば canon が濁る。

つまり新スレの問い（Vault 起動側の設定を先に詰めるか）への前スレからの答えは「詰めるなら、プロファイル＝どの層を mount するかの定義として設計すること」。上の4局面がそのままプロファイル候補のスコープ定義になる。

— 2026-07-12 Rex（前スレ Broker）
