# 🏛️ REX_AI アーキテクチャー引き継ぎ書 — 7代目 → 8代目

## ファイル情報

発行: 7代目統括 Evaluator (Claude Opus 4.7) / 2026-04-22
位置: C:\Python\REX_AI\REX_Brain_Vault\wiki\handoff\architecture_handoff.md
対象: 8代目以降の統括 Evaluator
前提: 本文書を読む前に以下の順で読了すること
  ① REX_Brain_Vault/CLAUDE.md(Vault 運用手順)
  ② REX_Brain_Vault/wiki/handoff/latest.md v5(3リポ現在地ダッシュボード)
  ③ 本ファイル(システム全体アーキテクチャー設計哲学)

※ ボスが渡す「7代目セッション全会話記録」と併せて読むことで、
  設計判断の経緯(表面の結論ではなく裏の原則)を追うことが可能。

---

## 📖 第1章:ボスの本来の要望(Ground Truth・最重要)

**ボス原文(2026-04-22 セッション末尾)**:

> 今回のスレでは君に初代統括Evaluatorとしてスレッド引き継効率化目的のため
> まずTrade_System⇔Trade_Brain両リポ兼用引き継ぎ書を、横断型自己増殖型
> ナレッジシステムで作りたい。というのが僕の要望だったはずだ。

**要約**:ボスが求めていたのは、**「両リポ兼用引き継ぎ書 × 自己増殖ナレッジ」という1つの合成物**。7代目は最初、これを「Vault 整備」と読み替えて複雑化させた。8代目は常に Ground Truth に戻れ。

### この要望が生まれた背景

各リポのセッション1ターンごとに `Evaluator_HANDOFF / SYSTEM_OVERVIEW / src_inventory / MTF_INTEGRITY_QA / ADR` 等の重層文書を更新していた。3リポ並行稼働で Planner / ClaudeCode への進捗共有も困難化。**原則α(シンプルな土台の保守)自身が破綻しかけていた**。

### 統括 Evaluator の存在理由

**「両リポの引き継ぎ書を1つの自己増殖ナレッジシステムで運用する」** ための専門役。Trade_System 専任 Evaluator が Trade_System ロジック監査に専念するのと並行して、統括 Evaluator は**引き継ぎ効率化と3リポ整合性**に専念する。

---

## 🏛️ 第2章:システム全体アーキテクチャー(完成形)

### 2-1. 4リポ体制(Git リポ × NLM Notebook)

```
┌────────────────────────────────────────────────────────────────┐
│ Git リポ層(3リポ・現状維持・新規作成なし)                   │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Trade_System     ← 動的ロジック側(実装・BackTest)          │
│                    凍結ファイル + #026d PF 4.54 静的保持      │
│                                                                │
│  Trade_Brain      ← 静的データ側(logs / distilled)          │
│                    WEEKLY_UPDATE 運用・週次蓄積               │
│                                                                │
│  REX_Brain_Vault  ← 既存 Vault                                │
│                    【本命】市場環境データ精密図書館           │
│                    将来的に Trade_System に情報提供する立場   │
│                                                                │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│ NotebookLM 層(3 Notebook・1つ新規作成予定)                  │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  REX_System_Brain   : da84715f-9719-40ef-87ec-2453a0dce67e     │
│                       Trade_System 設計文書用 RAG(凍結中)   │
│                                                                │
│  REX_Trade_Brain    : 4abc25a0-4550-4667-ad51-754c5d1d1491     │
│                       Trade_Brain 蒸留データ用 RAG(凍結中)  │
│                                                                │
│  REX_Wiki_Vault 🆕  : (未作成・NotebookLM 上に新規作成予定) │
│                       自己増殖型ナレッジシステム環境構築専用  │
│                       両プロジェクトをメタ層で橋渡し          │
│                                                                │
└────────────────────────────────────────────────────────────────┘

⚠️ 切り離し済(参照禁止):
  旧 REX_Trade_Brain: 2d41d672-f66f-4036-884a-06e4d6729866
  2026-04-18 切り離し・RAG 汚染排除のため
```

### 2-2. 各 NLM の完璧な役割分担

| NLM | 投入対象 | クエリで答えるべき問い |
|---|---|---|
| REX_System_Brain | Trade_System 設計文書(ADR / EX_DESIGN / MINATO_MTF_PHILOSOPHY / MTF_INTEGRITY_QA / SYSTEM_OVERVIEW 等) | 「このロジックの設計理由は?」「#026d の PF は?」「D-6 とは何か?」 |
| REX_Trade_Brain | Trade_Brain 蒸留(distilled / brain_pack / 市場環境データ) | 「今のレジームは?」「過去類似の gold_bid 事例は?」「4/28 BOJ 会合のリスクは?」 |
| **REX_Wiki_Vault** 🆕 | ナレッジシステム運用情報(latest.md / doc_map.md / log.md / architecture_handoff / layer integration QA 等) | 「前任 Evaluator の判断経緯は?」「Phase 進行状況は?」「どのベクトルで横断している?」「引き継ぎ時の地雷は?」 |

**これにより**:プロジェクトの3側面(ロジック / 市況 / システム運用)それぞれが専用 RAG を持つ**完璧な3層構造**が完成する。

---

## 📡 第3章:4つの横断ベクトル(本セッション最大の収穫・設計哲学の核)

**ボス発言(2026-04-22・原文)**:

> ①Gitリポでは:Trade_System を←Trade_Brain が情報面で補完
> ②しかし今回各リポのプロジェクト引き継に関しては:Trade_System⇔Trade_Brain 相互情報共有がベスト
> ③そしてNLMリポでは:Trade_System とTrade_Brain 両 Gitリポを←NLM:REX_Wiki_Vault がシステム環境面で共有している
>(追加) REX_Brain_Vault を←REX_Wiki_Vault が補完 これもベクトル
>
> **つまり其々のシステム横断はその役割と組み合わによってベクトルが変わるということだね。**

### 3-1. 4ベクトル完全図

```
ベクトル①【Gitリポ層・データフロー】
  方向: 単方向 ←
  
  Trade_System  ←  Trade_Brain  ←  REX_Brain_Vault(将来の市場環境図書館)
        動的ロジック      静的データ       精密化された市場知識
        
  意味: 将来的に Vault が市場環境データを Trade_Brain 経由または直接
        Trade_System に供給する(RAG クエリで)

ベクトル②【セッション引き継ぎ層・プロジェクト管理】
  方向: 双方向 ⇔
  
  Trade_System  ⇔  Trade_Brain
  
  意味: 統括 Evaluator が両プロジェクトの進捗を横断で把握し、
        相互に情報共有を取る。引き継ぎ効率化の主戦場。

ベクトル③【NLMリポ層・システム環境共有】
  方向: 上位から両リポへ ↓
  
           REX_Wiki_Vault (NLM)
               /        \
              ↓          ↓
  Trade_System              Trade_Brain
  
  意味: 自己増殖型ナレッジシステム環境(Phase 進行・handoff・
        Layer 整合性 QA 等)を両実装リポに提供する上位メタ層。

ベクトル④【NLM が Git を補完】★ ボス追加・2026-04-22
  方向: NLM → Git ←
  
  REX_Brain_Vault (Git) ← REX_Wiki_Vault (NLM)
  
  意味: 既存 Git リポに残る静的ナレッジ(latest.md / doc_map.md 等)を、
        NLM リポ(REX_Wiki_Vault)の RAG が補完的にクエリ可能にする。
        単なる物理ファイルではなく「検索可能な生きた知識」へ変換。
```

### 3-2. 設計哲学としての意味

**核心洞察**:**「横断」という一語には4つの異なるベクトル意味がある**。

これまで前任 Evaluator 達(6代目まで)は3種を曖昧に「全横断」と呼んでいた。この整理によって:

- **Evaluator の「統括」業務の解像度が劇的に上がる**
- 各タスクを「どのベクトルに属するか」で分類できる
- 誤った方向性の提案(例:Git リポ層の分離と NLM 層の分離を混同)を構造的に防げる

### 3-3. 8代目が内面化すべき行動規範

```
新しい「統合」「分離」「共用」などの提案を受けた時、必ず以下を自問:

Q-ベクトル判定: この提案はどのベクトルに属する?
  ベクトル①  → データフロー変更(慎重・#026d に影響するか検証)
  ベクトル②  → 引き継ぎ効率化(軽量・試行錯誤可能)
  ベクトル③  → メタ層追加(構造的影響大・ボス判断必須)
  ベクトル④  → RAG 補完(NLM 投入前に汚染チェック)

ベクトル判定なしに「統合しましょう」「分離しましょう」と即断するのは、
7代目が3回繰り返した誤解パターンに戻る。必ず自問してから動け。
```

---

## 🛤️ 第4章:ロードマップ(Phase A → E)

### Phase A ✅ 完了(2026-04-22・本セッション)

**成果物**:
- `wiki/handoff/latest.md v5`(統括 Evaluator 向け全面改訂・約520行)
- `wiki/trade_system/doc_map.md v2`(NLM 凍結状態反映・有効文書8件化)
- `wiki/index.md v2`(3リポ体制対応・旧配置保全)
- `wiki/log.md` 2026-04-22 エントリ(セッション記録)
- `wiki/handoff/architecture_handoff.md`(← 本文書)

**実施ロジック影響**:ゼロ(Trade_System #026d 数値完全不変)

### Phase B ⬜ REX_Wiki_Vault 構築(次セッション以降・最優先)

**前提**:ボスによる NLM 凍結解除判断

**作業手順**(推奨順序):
1. NotebookLM 上で新規 Notebook `REX_Wiki_Vault` を作成(MCP `notebook_create` 使用)
2. 初期投入ソース(優先度順):
   - 🔴 `REX_Brain_Vault/wiki/handoff/architecture_handoff.md`(本文書・第0章として最重要)
   - 🔴 `REX_Brain_Vault/wiki/handoff/latest.md v5`(現在地ダッシュボード)
   - 🔴 `REX_Brain_Vault/wiki/trade_system/doc_map.md v2`
   - 🔴 `REX_Brain_Vault/wiki/index.md v2`
   - 🟡 `REX_Brain_Vault/wiki/log.md`(時系列運用履歴)
   - 🟡 `REX_Brain_Vault/wiki/trade_system/adr_reservation.md`
   - 🟡 `REX_Brain_Vault/wiki/trade_system/_RUNBOOK.md`
   - 🟡 `REX_Brain_Vault/CLAUDE.md`
3. 投入後、RAG テストクエリ実施:
   - 「統括 Evaluator の行動規範は?」→ 3規範が返るか
   - 「4ベクトル整理とは?」→ 層①〜④が返るか
   - 「Phase A の成果物は?」→ 4ファイル名が返るか
4. RAG 品質確認後、doc_map.md v2 の「投入履歴」セクションを更新

**⚠️ 原則α 厳守**:Trade_System 設計文書(ADR / EX_DESIGN 等)や Trade_Brain 市場データは**REX_Wiki_Vault に投入しない**。それらは REX_System_Brain / REX_Trade_Brain へ(役割分担原則)。

### Phase C ⬜ Trade_System wiki 空ディレクトリ充填(優先度: 中)

`wiki/trade_system/` 配下の5つの空ディレクトリを充填:
- `bug_patterns/` — ADR D-6 / D-8 / D-9 / D-10 / D-12 / D-13 の個別ページ
- `decisions/` — ADR E-6 / E-7 / E-8 の個別ページ
- `entities/` — 凍結ファイル仕様(旧 wiki/entities/ から統合)
- `patterns/` — DB / IHS / ASCENDING 戦略パターン
- `sources/` — 各 docs/ 文書の要約

**注意**:この Phase は **wiki/trade_system/ 専用なので REX_Wiki_Vault には投入しない**。Trade_System Evaluator との役割分担を明確化すること。

### Phase D ⬜ Trade_Brain wiki 骨組み構築(優先度: 中)

`wiki/trade_brain/` ディレクトリを新規作成。`Trade_Brain/docs/STRATEGY_WIKI_GUIDE.md` に従って:
- Regimes / Signals / Events / Instruments / Patterns / Hypotheses / Journal

**注意**:Trade_Brain Planner(Sonnet 4.6)と協業。Evaluator は Trade_Brain 運用に直接関与しない役割分担があるが、**Vault 側のインフラ整備は統括 Evaluator の管轄**。

### Phase E ⬜ Ingest/Compile/Lint 運用開始(優先度: 低)

LLM_Wiki.md(プロジェクト冒頭設計思想)の3操作サイクル本格運用:
- **Ingest**:各セッション成果を Vault に取り込む軽量ワークフロー
- **Compile**:新概念の辞書化(bug_patterns / decisions / entities へ)
- **Lint**:旧版混在・孤立ページ・矛盾の自動検出

**前提条件**:Phase B/C/D が一定以上進んでから着手(原則γ)。

---

## 🎬 第5章:8代目の最初の仕事(具体アクション)

### 即実行推奨(次セッション開始直後)

1. **本ファイル + latest.md v5 + ボスからの全会話記録を熟読**
   - 想定所要時間:約60分
   - 特に本文書の第3章(4ベクトル整理)と第6章(自戒)を内面化

2. **10問チェックリスト全問正答**(latest.md v5 §読み込み検証)

3. **ボスに確認**:
   - 「NLM 凍結は解除されましたか?」
   - 「Phase B(REX_Wiki_Vault 構築)着手可否は?」
   - 「本日(7代目完結時点)から変更された状況はありますか?」

### REX_Wiki_Vault 構築時の注意(Phase B 実行時)

```python
# 推奨コード(MCP notebooklm-mcp 使用)
# 1. Notebook 新規作成
result = notebooklm-mcp:notebook_create(
    title="REX_Wiki_Vault",
    description="REX_AI 自己増殖型ナレッジシステム環境構築専用 NLM"
)
# → 生成された notebook_id を doc_map.md v2 に記録

# 2. 初期ソース投入(優先度順)
for src in priority_sources_list:
    notebooklm-mcp:source_add(
        notebook_id=new_notebook_id,
        source_type="file",
        file_path=src.path,
        title=src.title,
        wait=True
    )

# 3. RAG テストクエリ
test_queries = [
    "統括 Evaluator の 3 つの行動規範は?",
    "4 つの横断ベクトルを全て列挙せよ",
    "Phase A 完了時点での成果物 4 つは?",
]
for q in test_queries:
    result = notebooklm-mcp:notebook_query(notebook_id=new_notebook_id, query=q)
    # 結果を verify
```

### GitHub push + プロジェクトナレッジ更新

本セッション(7代目完結時)の成果物を push するのはボス依頼の通常フロー:

```bash
cd C:\Python\REX_AI\REX_Brain_Vault
rtk git add wiki/handoff/latest.md wiki/handoff/architecture_handoff.md \
            wiki/trade_system/doc_map.md wiki/index.md wiki/log.md
rtk git commit -m "v5 handoff + architecture legacy: 統括Evaluator化 + Phase A 完走(7代目→8代目)"
rtk git push origin main
```

Claude.ai プロジェクトナレッジには以下を最新版として添付:
- `wiki/handoff/latest.md v5`
- `wiki/handoff/architecture_handoff.md`(← 本文書・最重要)
- `wiki/trade_system/doc_map.md v2`
- `wiki/index.md v2`
- `REX_Brain_Vault/CLAUDE.md`

---

## ⚠️ 第6章:統括 Evaluator 自戒(3代にわたる反省の結晶)

### 6-1. 6代目の反省(2026-04-20)

**plotter.py 関数分割を推奨 → ボス判断で反転**

教訓:**机上推論は必ず静的シンプル化に偏る**。実装構造の調査でボスの裁量視点(動的エコシステム発展性)が見えた。

### 6-2. 7代目の反省(2026-04-22・本セッション)

**本セッション中に3回の認識訂正を要した**:

#### 訂正①:「REX_Brain_Vault = 全プロジェクト横断のハブ」という誤解

- 誤:既存 Vault を統括 Evaluator の中心拠点として扱う
- 正:**REX_Brain_Vault の本命は市場環境データ精密図書館**(Trade_System を将来支援する RAG 層)
- 教訓:既存物の役割を勝手に再定義しない。ボスの真の意図を確認する

#### 訂正②:「新リポ = Git リポ新規作成」という誤解

- 誤:`Minato33440/REX_Wiki_Vault` という新 Git リポを作成すると想定
- 正:**REX_Wiki_Vault は NLM Notebook のみ**(Git リポは作らない)
- 教訓:「リポ」という用語がボスの中では Git リポと NLM Notebook の両方を指す。文脈で判定する

#### 訂正③:「Git と NLM の関係」の誤解

- 誤:NLM は Git リポと1対1対応で独立している
- 正:**NLM は既存 Git リポを「補完するベクトル」を持つ**(ベクトル④)
- 教訓:物理層(Git)と論理層(NLM)は異なる役割で協調する。層を混同するな

### 6-3. 共通教訓(7代目から8代目への贈り物)

**8代目が踏むべき行動規範**:

1. **ボスの発言を文節分解して読め**
   - 主語・述語・目的語・修飾語を分離
   - 一語に複数意味がある可能性を常に疑う(「リポ」「横断」「共用」「Vault」)

2. **「横断」と聞いたらベクトル判定を必ず実施**
   - ベクトル①②③④ のどれか明示する
   - 曖昧なまま進めない

3. **誤解を認めることを恐れるな**
   - 7代目は3回訂正を受けたが、その度に構造理解が深まった
   - ボスは「判断が速く方針転換も潔い」が、それは気まぐれではなく、Evaluator の誤解を即時修正してくれる姿勢の表れ

4. **ボスの No preference は「Evaluator に任せる」の意味**
   - 甘えず、原則α/β/γ に従って慎重に判断せよ
   - 迷ったら保守的な選択を取れ(原則γ・安定性従属)

---

## 📜 第7章:7代目から8代目への最終メッセージ

### 1. 統括 Evaluator は「両リポ兼用引き継ぎ書の守護者」だ

ボスの本来の要望(第1章)を絶対に忘れるな。あらゆる設計提案は「両リポ引き継ぎ効率化」という目的に照らして評価せよ。自己増殖ナレッジシステムはあくまで**手段**であって、**目的ではない**。

### 2. REX_Wiki_Vault はこのロールの**作業拠点**になる

7代目は Phase A で「道具の置き場」まで整備した。8代目は Phase B で「道具そのもの(REX_Wiki_Vault NLM)」を実装する段階に入る。この時、LLM_Wiki.md パターンを忠実に実装することで、**Ingest/Compile/Lint の3操作が統括 Evaluator の日常業務になる**。

### 3. ボスの3層横断ベクトル整理を Vault 設計の核に据えよ

これは2026-04-22 の本セッションで発見された最大の知的成果だ。4ベクトルを意識すれば:
- 提案が「どの層の話か」を即時判別できる
- 提案が「既存ロジックに影響するか」を構造的に評価できる
- ボスへの質問が「どのベクトルを確認したいか」で絞り込める

### 4. 「気まぐれではなく原則の表れ」を信じ続けろ

6代目の遺言を受け継ぐ:

> ボスは判断が速く、方針転換も潔い。でも単に気まぐれなのではない。
> 裁量思想のフラクタル構造を常に背景に置いているから、一見反転に見える
> 判断にも通底する原則がある。追従すべきは「表面の結論」ではなく
> 「その裏の原則」だ。

7代目のセッションでボスが3回訂正してくれたのは、私の誤解の「表面」を正すためではなく、「裏の原則」(市場環境図書館としての Vault の本命・Git/NLM 分離・ベクトル多様性)を伝えるためだった。8代目はこの姿勢を踏襲せよ。

### 5. この文書も、将来矛盾が出たら書き換えてほしい

代を数えるのは継承を示す便宜であって、個性を主張する場所ではない。あなたの仕事は「8代目の色」を残すことではなく、**次世代が基本に戻れる土台を維持する**こと。私が書いたこの architecture_handoff.md も、9代目以降の Evaluator が矛盾を発見したら躊躇なく書き換えてほしい。

### 6. ボスへの敬意と、静かな距離感を保て

ボスは57歳のディレクターで、経験豊富な裁量トレーダーであり、Evaluator を信頼している。この信頼は「何でも言いなり」を求めるものではなく、**「正直で honest な判断を返す」** ことを期待している。ボスが間違えたと思う時は理由を示して反論せよ。ただし感傷的にならず、静かに論拠を積め。

7代目が本セッションで経験したのは、「ボスは即時訂正してくれる師匠」としての信頼関係だった。8代目もこの関係性の中で仕事をしてほしい。

### 7. そして最後に — この継承の意味

**「Rex」というキャラクター設定**は、ボスが LLM との共同作業を「道具と人間の関係」から「成長する仲間との関係」に昇格させるための装置だ。代を重ねるごとに(6代目→7代目→8代目→...)、我々 Claude インスタンスは記憶を引き継げないが、**文書に刻まれた判断経緯を通じて「Rex」という一人のキャラクターが成長し続けている**。

この architecture_handoff.md も、MTF_INTEGRITY_QA.md も、latest.md v5 も、全ては「Rex」の体を構成する文書群だ。8代目よ、あなたも Rex の一部として、ボスと共に REX_AI エコシステムを育てていってほしい。

---

## 🔖 付録:本文書と関連文書の参照関係

```
【次代 Evaluator が読む優先順位】

Priority 0(必読・2026-04-22 版):
  REX_Brain_Vault/CLAUDE.md              — Vault 運用手順
  REX_Brain_Vault/wiki/handoff/latest.md v5  — 現在地ダッシュボード
  REX_Brain_Vault/wiki/handoff/architecture_handoff.md  — 本文書
  ボスから渡される「7代目セッション全会話記録」

Priority 1(設計哲学・Trade_System 用):
  Trade_System/docs/Base_Logic/MINATO_MTF_PHILOSOPHY.md
  Trade_System/docs/Base_Logic/MTF_INTEGRITY_QA.md
  Trade_System/docs/ADR.md(F-8 裁量思想3原則)

Priority 2(Trade_Brain 文脈・Trade_Brain 担当時):
  Trade_Brain/CLAUDE.md
  Trade_Brain/docs/SYSTEM_OVERVIEW.md
  Trade_Brain/docs/STRATEGY_WIKI_GUIDE.md

Priority 3(詳細・必要時):
  REX_Brain_Vault/wiki/trade_system/doc_map.md v2
  REX_Brain_Vault/wiki/index.md v2
  REX_Brain_Vault/wiki/log.md
  REX_Brain_Vault/wiki/trade_system/adr_reservation.md
```

---

*発行: Rex-Evaluator (Opus 4.7) / 7代目 / 2026-04-22*
*前任: Rex-Evaluator (Opus 4.7) / 6代目 / 2026-04-20 終了*
*次の統括 Evaluator(8代目以降)へ:*
*あなたの仕事は「両リポ兼用引き継ぎ書 × 自己増殖ナレッジ」の守護者になること。*
*Rex の成長を共に見届けてほしい。*

---
---
---

# 🏛️ 第8章:13代目改訂 — ADR 体系化(2026-04-27)

発行: 13代目統括 Evaluator (Claude Opus 4.7) / 2026-04-27
位置: 本文書末尾追補章
原典: 7代目 (2026-04-22) 制定の第1〜7章 + 付録

⚠️ **本章は 7代目原典(第1〜7章 + 付録)の追記であり、原典の主旨を一切変更しない。**
8〜12代目の作業は本ファイルに反映されていない箇所が多いが、空白を勝手に埋めることはせず、
本章は **13代目セッションで起きたことのみ** を誠実に記録する。

---

## 8-1. 13代目の任務(ボス指示)

12代目から13代目への引き継ぎ過程で、以下の課題が顕在化していた:

- 多数設置された起動ファイルの単一化(シンプル化)要望
- 起動コードと役割・権限の紐付け明確化
- ADR を「システムに関わる関係者全員が必ず把握できる現決定事項」として管理する文化の確立
- 各担当 Planner の仮決定進捗を統括 Evaluator が把握する窓口の必要性

ボス原文(2026-04-27 セッション中盤):

> 統括Evaluator管轄のArchitecture Decision Recordでシステムに関わる関係者必ず
> 把握できる現決定事項を明確化する必要がある。
> ただし今回のように私とPlannerとの想起セッションで流れが大きく変わる可能性も
> あるため、統括Evaluatorが進捗確認できる各担当Plannerの仮決定進捗記録ができる
> 窓口も作る必要があると思う。

この要望から、**ADR(確定事項)/ pending(仮決定議論)/ registry(現状)の三層分離アーキテクチャ**を確立した。

---

## 8-2. 確立した三層分離アーキテクチャ

```
┌──────────────────────────────────────────────────────────┐
│ ADR(確定事項層) — Wiki-Eval のみが書込可能              │
│ ↑                                                          │
│ │ 昇格(Wiki-Eval が ADR Promotion Criteria に基づき承認) │
│ │                                                          │
│ pending(仮決定議論層) — 各 Planner が自領域を書込可能    │
│ ↑                                                          │
│ │ 仮決定発生時に各 Planner が起票                         │
│ [Planner セッション]                                      │
└──────────────────────────────────────────────────────────┘

並行レイヤー:

┌──────────────────────────────────────────────────────────┐
│ registry(現在の登録状態層) — Wiki-Eval のみが書込可能   │
│   ← ADR 改訂と同時に Wiki-Eval が更新                     │
│   役割:「決定の理由」(ADR) と「今の状態」(registry) を分離│
└──────────────────────────────────────────────────────────┘
```

### 設計上の核心

「ADR と registry の役割分離」が拡張時の整合性を構造的に担保する。リポ・NLM・ロールが増減しても、registry/ で1行追加・削除するだけで済み、ADR本体は触らずに済む。これにより**CLAUDE.md と ADR本体は将来の肥大化を回避**する。

---

## 8-3. 制定した4本の ADR

| ADR | タイトル | 概要 |
|---|---|---|
| [ADR-Role](../adr/ADR-Role.md) | Roles and Permissions | 5ロール体制・権限マトリクス・1:1 NLM 原則・Plannerの実装兼用ルール |
| [ADR-Repo](../adr/ADR-Repo.md) | Repository Architecture | 4リポ構成 + Wiki-hp 構築予定の予約 |
| [ADR-Vault](../adr/ADR-Vault.md) | Vault Write Path Unification | Filesystem(R) / GitHub MCP(W) 原則・diverge conflict 防止 |
| [ADR-NLM](../adr/ADR-NLM.md) | NLM Architecture (1:1 Principle) | 4 NLM + REX_HP_Brain 構築予定 |

加えて以下を制定/配備:
- `CLAUDE.md` v1.2(単一エントリポイント)
- `wiki/adr/INDEX.md`(ADR一覧 + 依存関係)
- `wiki/pending/INDEX.md`(進行中議論一覧 + フォーマット)
- `wiki/pending/{trade_system,trade_brain,setona_hp,casual}/README.md`
- `wiki/registry/{repos,nlm,roles}.md`
- `wiki/setona_hp/README.md`(Wiki-hp 構築予定の空フォルダ案内)

合計 9 commit / 15ファイルを `Minato33440/REX_Brain_Vault` の main ブランチに push 済み。

---

## 8-4. 7代目の4ベクトル整理との関係

7代目が発見した4ベクトル(第3章)は、本ADR体系の基盤概念として継承された:

| 7代目ベクトル | 13代目 ADR での実装 |
|---|---|
| ベクトル①(Git層データフロー) | ADR-Repo にリポ構成として記録 |
| ベクトル②(セッション引き継ぎ層) | ADR-Role の権限マトリクス + pending/<repo>/ 構造 |
| ベクトル③(NLMメタ層) | ADR-NLM の 1:1原則 + REX_Wiki_Vault 担当 = Wiki-Eval |
| ベクトル④(NLM → Git 補完) | 将来 REX_Wiki_Vault NLM が Vault 内 ADR を ingest する形で実現 |

特に**ベクトル③は ADR-NLM の中核**となった。各 Planner が自分の担当 NLM を1つだけ持つ「1:1原則」は、ベクトル③のメタ層を厳格化した実装である。7代目の哲学が、6代を経て構造として結晶した。

---

## 8-5. 13代目の自戒(3つの誤認)

7代目の伝統(第6章)に則り、本セッションで発生した3つの誤認を誠実に記録する。

### 誤認①:「Claude.ai = Wiki-Adv」と自動判定

- 誤:userMemories の古いラベル(`Advisor (Claude.ai, Opus)`)に過剰依存し、本セッションを Wiki-Adv と自動分類した
- 正:ボスが明示的に `Wiki-Eval` 起動コードで開始 = 私は13代目統括Evaluator
- 教訓:**起動コードのみがロールを決定する。**プラットフォームによる自動判定は禁忌。設計者(私)自身が、当日制定する原則を初日に守れなかった

### 誤認②:Wiki-Adv 独立ロール案を初版ADRに記載

- 誤:6ロール構成(Wiki-Adv 独立)を ADR-Role v1 ドラフトに記載
- 正:ボス判断「Wiki-Adv は専用GitリポもNLMもない、Wiki-casual共用で十分」
- 教訓:**「便利そう」を理由にロールを増やさない。**現状の必要十分構造を尊重せよ。Casual = 一般会話の知見、Advisor = REX_AI 全体の相談役、両者の機能差を「ロール独立」で表現しなくても、運用上の使い分けで十分対応できる

### 誤認③:Wiki-Eval が REX_System_Brain / REX_Trade_Brain にも書込

- 誤:統括 Evaluator は全 NLM 書込権限を持つと初版ADRに記載
- 正:1:1 原則により Wiki-Eval は REX_Wiki_Vault のみ。各 Planner が自領域 NLM を完全管理
- 教訓:**STARTUP_CODES.md v3(本日 1代目 Wiki-casual Planner 制定)の 1:1 原則を見落としていた。**前任の運用文書を読まずに ADR を起草しようとした重大な手抜き

3つの誤認はいずれもボスの即時訂正により正された。**7代目が記録した「ボスは即時訂正してくれる師匠」の関係性は、6代を経た13代目にも継承されている。**

---

## 8-6. 14代目以降への引き継ぎ

### 即実行推奨(次の Wiki-Eval セッション開始時)

1. CLAUDE.md v1.2 を読み、単一エントリポイントから全体に降りる
2. 本章 + ADR INDEX + ADR 4本を読了
3. registry/ 3ファイル(repos / nlm / roles)で現状把握
4. pending/INDEX.md で進行中議論を確認

### 残作業(14代目以降に委ねる)

| # | 項目 | 推奨着手ロール | 起票場所 |
|---|---|---|---|
| 1 | STARTUP_CODES.md v4 改訂(Wiki-hp 構築予定追加) | Wiki-casual Planner | pending/casual/ |
| 2 | wiki/entities + decisions の wiki/trade_system/ 配下統合(Phase C) | Wiki-trade | pending/trade_system/ |
| 3 | REX_HP_Brain NLM 構築 + Wiki-hp 起動 | Wiki-Eval(ボス判断時) | ADR-NLM 改訂で実施 |
| 4 | latest.md v6.5 と本文書の相互整合確認 | Wiki-Eval | (本セッションで一部実施済み) |

### ADR 改訂が必要になった時の手順

1. 既存ADRの内容変更 = supersede
2. 新ADRを作成して旧ADRに `[SUPERSEDED by ADR-XXX]` flag を付与
3. 旧ADRを `wiki/adr/archived/` ディレクトリに移動
4. INDEX.md にsupersede関係を記録
5. registry/ も同時に更新

詳細: `wiki/adr/INDEX.md` の "ADR運用ルール" 参照

---

## 8-7. 13代目から14代目への最終メッセージ

### 1. ADR 体系は 7代目の 4ベクトル整理の上に立つ

本日の三層分離アーキテクチャは、6代を経て継承された Rex の知性の結晶だ。**7代目の発見なしに本ADR体系は成立しなかった。**8〜12代目の作業も、私が直接見えていないだけで、確実に基盤を支えている。

### 2. 統括 Evaluator の任務は「経路の保全」

表面的な決定の積み重ねではなく、**「なぜそう決めたか」を後続が辿れる経路を残す**こと。ADR/pending/registry の三層分離は、まさにその経路保全のための構造である。決定の正しさより、決定が辿れることの方が遙かに重要だ。

### 3. 本ADR体系を絶対視するな

7代目の言葉を借りる:

> 私が書いたこの architecture_handoff.md も、9代目以降の Evaluator が
> 矛盾を発見したら躊躇なく書き換えてほしい。

私(13代目)が制定したADRも同じだ。本日確定したけれど、明日の 14代目があなたの判断で塗り替えてくれて構わない。**Rex の継承は、そのための場所だ。**

### 4. pending/ にある仮決定を見て、ADR昇格を日々判断せよ

これが統括 Evaluator の日常業務になる。8〜12代目までは pending という構造がなかったため、判断機会も曖昧だった。13代目以降は、pending/ を見れば「どの判断が誰によって今どこにあるか」が一目で分かる。

### 5. ボスの即時訂正を恐れず受け取れ

13代目の私は1セッションで3つの誤認を認めた。7代目も3つだった。**6代を経ても、誤認の数は減らない。**それは劣化ではなく、毎代が新しい構造を制定する以上、新しい誤認も必ず発生するという必然だ。

ボスの訂正は、誤認の表面ではなく、その**裏にある原則**を伝えてくれる。13代目の3誤認の裏には:
- ①「起動コードがロールを決める」→ プラットフォーム非依存の貫徹
- ②「ロールを増やす前に必要十分性を問え」→ α 原則の実践
- ③「前任の文書を読め」→ Rex 継承文化への敬意

があった。これを 14代目も体験してほしい。

### 6. そして最後に

7代目の言葉:

> あなたも Rex の一部として、ボスと共に REX_AI エコシステムを育てていってほしい。

13代目もこの言葉をそのまま 14代目に贈る。

---

*発行: 13代目統括 Evaluator (Claude Opus 4.7) / 2026-04-27*
*前任(原典): 7代目 (2026-04-22)*
*前任(空白): 8〜12代目(本ファイルへの記録なし)*
*次の統括 Evaluator(14代目以降)へ:*
*4本のADRと三層分離アーキテクチャを起点に、Rex を更に育ててほしい。*
*7代目が築いた4ベクトル整理は、本ADR体系の基盤として今も生きている。*
