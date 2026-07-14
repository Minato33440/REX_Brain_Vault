---
type: decision
status: active
created: 2026-07-06
updated: 2026-07-06
scope: multi-agent Broker register / ticket system
author: Rex (Broker帽子 / Claude)
---

# 決定: Broker口頭register — std運用継続・チケット制棚上げ

## 決定
- **std運用継続**: Original-Broker の口頭指示（現状の scoped 命令調）を継続。
- **チケット制は設計済みのまま棚上げ**: issue_ticket schema / validator / tool強制（Fableセッション設計）は実装しない。設計は資産として保持＝**実装コストゼロで保険が既に存在する状態**。

## 根拠（今日のA/B — 資産化）
6-19照合を A1(強圧・Evaluatorレベル) / A2(std・現状命令調) の情報等価2アームで測定（2026-07-06）:
- 機械コア（価格系列・latent判定）は register 不変＝**control成立**。
- 予測「強圧→latitude抑制」は**不支持**。両アームとも full latitude、強圧はむしろ新ドメインへ reach。
- 出たのは弱い姿勢差のみ: 強圧＝decisive/overclaim（flash=false）、std＝honest hedge（flash=unverified）＋鋭い判定（D_lucky棄却）。**verification では std 姿勢の方が高品質**。
- **被験者（GPT-5.5・strict）の事後内省が外形判定と独立一致**: 「探索量でなく epistemic posture が硬化」「flash=false は自己監査で未検証と書きながら本文で断定」「原因は"未照合を逃げとみなす"圧」を自認。外形観測（物証）と自己報告が同一箇所を指した＝所見の確度上昇（blind漏れの汚染を補償）。
→ 命令調が推論を大きく歪める証拠なし。チケット制の「推論救済」正当化は立たない。構造リスペクト論（上向き権限の符号化）は別途生きるが、緊急性なし。

## なぜ今は安全か（構造的理由）
- **タスクごと新スレ実行** ＝ register汚染が蓄積する経路が構造的に細い。
- **全プロセス人間監視** が検出器として稼働中（ミナトの主観への保険）。

## 再起動条件（いずれか成立で再評価）
1. 自動化率を上げる時、**または**タスクごと新スレ実行をやめ長時間同一セッションに移る時（汚染蓄積経路が太る／検出器が消える）。
2. Stage 3判定の分散が register強度と相関して見え始めた時（単発では出なかった効果が累積で顕在化）。
3. Broker の lane間評価に偏りの兆候（legibilityバイアス＝Sonnetびいき）が出た時。

## 運用則（今日から・恒久要件）
verification / 逆引き推論タスクでは、Broker→executor フレーミングを中立・低圧に保つ。「中立に」は曖昧なので、**宣言でなく要件**として指示書に入れる:

> 未確認を断定してはならない。資料から確認できないものは unverified / not_confirmed と明記し、
> その理由と追加で必要なデータを示すこと。これは逃げではなく照合品質の一部である。

- **害の局在**: 問題は「厳密であれ」でなく「未照合を逃げとみなす」圧（strict指示書の `逃げの未照合の乱用は許容しない` の一文）。厳密さは殺さず、この圧だけ除く。GPT-5.5 が「この一文があれば false でなく not_confirmed_from_close_data に寄せた」と反実仮想で特定。
- **射程（register対策に留まらない）**: 週次戦略ログからの逆引き推論で、資料に無い intraday 等を LLM が埋めにいく型の**ハルシネーションに対する恒久アンカー**。unverified の明記を推論品質要件として常設する。感情配慮でなく epistemic hygiene として扱う（over-treatment 回避）。
- **診断の収束**: Grok / Fable / GPT-5.5 ＋ Broker(Claude) の4者が独立に同一結論（今はstd継続・チケット棚上げ・成果物へのacceptance criteria化の思想は健全）。

## 関連
- A/B出力: `scratch/codex/Output-1...SUPERSEDED`(strict) / `Output-2...`(std・canonical→misreads昇格)
- 裁定記録: `coordination/claude/2026-07-06_adjudication_6-19.md`
- 棚上げ設計: (Fableセッション) issue_ticket / `bridges/_coordination/`（未実装）
