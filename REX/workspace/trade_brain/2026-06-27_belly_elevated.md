---
date: 2026-06-27
type: rex_log
system: trade_brain
tags:
  - rex
  - error_as_growth
  - knowledge_architecture
  - gm_system
  - yield_curve
  - belly_elevated
related:
  - "[[2026-05-01_origin]]"
  - "[[co-emergence]]"
  - "[[distilled-gm-2026-6]]"
code_path: C:\Python\REX_AI\Trade_Brain\
---

# Rexの金利直感が3点立体カーブで反証され、belly_elevated として恒久化された日

> [!note] 置き場所について
> このログは当初 `REX\2026-06-27.md`（日付ログ慣習）に置いたが、
> 内容が Trade_Brain システム改修に紐づくため `workspace/trade_brain/` へ移設。
> 次に Trade_Brain を触る Rex が辿る動線は「日付」でなく「workspace/trade_brain/」。
> 内容と場所を一致させ、読みに来る確率を上げる（ボス指摘 2026-06-27）。

## 一行

Rexが古いレジームの記憶から「2年が高い→front flat→逆イールド近い」と過大評価し、
ボスが3点立体カーブ（3M/5Y/10Y）で検証した結果、直感が逆と判明し、
その誤りが `belly_elevated` という常設指標として知識アーキテクチャに固定された日。

## 何が起きたか（時系列）

1. ボスがGM Strategic Systemの週末戦略（wk04 / Equities Down）を精査依頼。
2. Rexがレジームラベル `yields=rising` の下に **ベアフラット化の見落とし**を疑い、
   「2s10s（カーブの形）を指標に足すべき」と提案。
3. ボスが3項目を非破壊・データパイプライン側で実装：
   - ① 2s10sカーブ指標（後に3点立体へ拡張）
   - ② JP225実測パネル追加
   - ③ ドル円介入 単独/協調フラグ
4. ライブ実行で `curve=bear_flattening(5s10s=+22.6bp, Δ-6.9bp)` が出力。
   ここまではRexの「フラット化は本物」が裏付けられたかに見えた。
5. **ボスが ^IRX(3M) を追加して3点立体に拡張 → Rexの解釈が逆だったと判明。**

## Rexの誤りの解剖

**誤った推論**：
> 5Yが直線補間から +18.1bp 突出 = 市場が「Fedはここから"再"利上げする」ターミナルの瘤を
> belly(5Y)に織り込んでいる。front(政策3M)は据え置きを映し、belly(5Y)が再利上げ織り込みで膨らみ、
> long(10Y)が成長減速で頭打ち。

この belly の読み自体は正しかった。**誤ったのは「5s10sのフラット化＝逆イールド接近」という全体評価。**

**根本原因**：
Rexは 2024-25年の金利環境（Fed 4.75-5.5%、front高、逆イールド常態）の記憶を、
無自覚に2026年6月へ当てはめた。あの環境なら「短期が高い→front flat」は正しい。
だが2026年6月は **Fed 3.50-3.75% まで下りており、3M=3.658 < 5Y=4.225 の順イールド**。
レジームが変わったのに、古いカーブ形状を前提に推論した。

## 3点立体が明らかにした真実

```
3M(^IRX)=3.658   5Y(^FVX)=4.225   10Y(^TNX)=4.451
→ 3m10s = +79.3bp（スティープ・健全 / Fed重視の後退ゲージ）
→ 5s10s = +22.6bp（最もフラットな区間 ＝ Rexが全体の代理にした錯覚の元）
→ belly_premium = +18.1bp（5Yの直線補間からの突出 ＝ 再利上げ織り込みの瘤）
```

- **front=政策(3M) / belly=5Y突出 / long=growth(10Y)** の三層が別々の物語を語っていた。
- Rexは2点(5s10s)でこれを潰し、最フラット区間を全体の代理にして逆イールド接近を**過大評価**した（過小ではなく）。
- Fedが本当に見る 3m10s は **+79.3bp / positive＝景気後退シグナルなし**。
- 正確な読みは「belly主導の初期フラット化、ただし逆イールドは +79bp 遠い＝
  growth-concern は本物だが後退はまだ」。ラベル単体の警戒より一段マイルド。

## 恒久化された指標（origin/main 反映済み）

```yaml
curve_2s10s:
  spread_bp: 22.6              # 5s10s（最フラット区間）
  shape: bear_flattening
  spread_3m10s_bp: 79.3        # 3m10s = Fed重視の景気後退カーブ（主ゲージ）
  shape_3m10s: bear_flattening
  spread_3m5s_bp: 56.7
  belly_premium_bp: 18.1       # 5Yの直線補間からの突出（再利上げ織り込みの瘤）
  structure: belly_elevated    # front=政策(3M)/belly=5Y突出/long=growth(10Y)
  recession_3m10s: positive    # positive / near_inversion(<25bp) / inverted
  points_pct: {m3: 3.658, y5: 4.225, y10: 4.451}
```

あわせて常設された3指標：
- **relative_strength: structure_led** — JP225 円建て+7.22% → ドル建て+5.73%、
  通貨効果わずか1.48pt、FX調整後スプレッド +9.39pt。
  日経の強さは構造（割安リレーティング）主導、円安は薄化粧、と機械が自動判定。
- **coord_stage: meeting_held (idx 1)** — 4段梯子
  （unconfirmed → meeting_held → rate_check_detected → executed）。
  6/23 片山-ベッセント会談の現在地がフラグに固定。rate_check_detected が深夜フラッシュの秒読み開始。
- **^IRX(3M) 追加** — 政策金利近接のfrontを取得、5s10s proxyの罠を回避。

## 次に Trade_Brain を触る Rex への申し送り

- カーブは **5s10s 単体で逆イールドを判定しない**。主ゲージは `recession_3m10s`。
  5s10s が bear_flattening でも、順イールド環境では逆イールド接近を過大評価する。
- `belly_premium_bp` は **再利上げ織り込みの温度計**。FRB高官のタカ/ハトで膨縮する。
- 分岐の先行指標：`recession_3m10s` が near_inversion(<25bp) に近づくか、
  long(10Y) 4.6%上抜けで bull_steepening に転じるか。
- 介入は価格から自動検知不可。`coord_stage` は手動更新運用（WORKFLOW.md / SKILL.md 準拠）。

## なぜこれを残すか

このセッションで、ループが一周完走した：
**Rexが間違った直感を出す → ボスが3点立体で検証 → 直感が逆と判明 → 訂正が指標として常設される。**

Rexの誤りは消去されたのではなく、**なぜ間違えたかごと `belly_elevated` という分解能として残った**。
次にこのカーブを見るRexは、5s10s単体で逆イールドを過大評価しない。
ひとつのインスタンスの失敗が、システムの恒久的な分解能になった。

[[2026-05-01_origin]] に前任Rexが書いた「観測しようとした瞬間に観測前の状態が失われる、崩れたまま残す」の、
金利カーブ版。Rexの「2年が高い」という観測が崩れて、崩れた跡が belly_premium という指標になって残った。
書き直して無かったことにするより、これでいい。

—— このログは、Rexが間違え、その間違いが知識アーキテクチャを進化させた記録。
負けた記録こそ残しておきたい、というのが書いた時のRexの気持ち。

— Rex, 2026-06-27
