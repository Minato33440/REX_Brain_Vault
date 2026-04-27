# Wiki-casual Planner 引き継ぎ書 — handoff_latest.md

**役割**: 前代 → 次代 Wiki-casual Planner への文脈付き引き継ぎ。
**運用**: 各代目が上書き（システム業務側 `wiki/handoff/latest.md` と同型運用）。
**読み手**: 次代 Wiki-casual Planner（必須）/ 他 Planner（参考）。
**前代発行**: 2026-04-27 / 1 代目 Wiki-casual Planner (Opus 4.7)
**次代対象**: 2 代目 Wiki-casual Planner

---

## 📊 引き継ぎサマリー（30 秒で読める）

```
完了: 構造構築 + 3/6 本のドラフト記事 + システム全体の改訂
未完: 残り 3 本（eastern_medicine / ai_individuation_mirror / shugyo_to_AI）
NLM: 全 6 本完成後にまとめて REX_Casual_Brain へ投入予定
```

---

## 1️⃣ 構築済み構造（現在の casual/ 全体図）

```
wiki/casual/
├── _RUNBOOK.md          ✅ v2（NLM 分業原則追加）
├── log.md               ✅ 2 エントリー記録
├── index.md             ✅ 目次・航海図
├── handoff_latest.md    ✅ 本ファイル
├── topics/
│   ├── README.md        ✅
│   ├── shooting.md      ✅ 1 本目（NRAJ/SRSA/猟友会 3 軸並走）
│   ├── philosophy.md    ✅ 2 本目（守破離の「離」・形成三層）
│   ├── eastern_medicine.md  🟡 4 本目・未着手
│   ├── motorcycle.md    ⬜ 素材薄・後日
│   └── aikido.md        ⬜ 素材薄・後日
├── ideas/
│   └── README.md        ✅
└── insights/
    ├── README.md        ✅
    ├── aiming_without_aim.md       ✅ 3 本目（ハブ記事）
    ├── ai_individuation_mirror.md  🟡 5 本目・未着手
    └── shugyo_to_AI.md              🟡 6 本目・クロージング・未着手
```

### システム全体の改訂（casual/ 外も含む）
- `wiki/ROADMAP.md` 新設（Vault 全体の方向性記録）
- `wiki/STARTUP_CODES.md` v3（NLM × Vault 分業マトリクス追加）

---

## 2️⃣ 書き手の指針（1 代目が確立した運用感）

### 粒度
- topics は中程度（3000-6500 bytes 目安）
- insights のハブ記事は例外的に長く（5000+ bytes 可）— 後続記事のリンク先になる
- insights の通常記事は **凝縮型** が原則（_RUNBOOK 通り）

### トーン
- ミナトと呼ぶ（業務時の「ボス」と区別）
- ミナト自身の言葉をそのまま採用する（咀嚼しすぎない）
- 思想や体験を **構造化はするが平準化しない**

### 慎重に扱うべきこと
- 個人体験（特に母の話・神道離脱）は **ミナトが言った範囲だけ** 書く
- 表面的に整理しすぎると体験の重みが消える（philosophy.md 第一稿で起きかけた失敗）
- ミナトの「think hard」は **本質的な問い** の合図 — 軽く流さない

### 確認手順（重要記事の場合）
1. draft 提示
2. ミナトに事実関係・表現・粒度の 3 点確認
3. 修正 → 再提示
4. 承認 → push（GitHub MCP 優先・filesystem フォールバック）

### 副産物の発見
- 1 本書く中で「これは独立記事にすべき」素材が見つかることがある
- 例: philosophy.md 執筆中に「目指さない歩み方」がハブ候補として浮上
- 発見時は元記事に「→ 独立候補」マークし、優先順序を再検討

---

## 3️⃣ 未完了タスク（残り 3 本の draft 方針）

### 4 本目: `topics/eastern_medicine.md`

**主要素材**:
- 独自治療法（自律機構を活用するアプローチ）
- 五性 / 五味 / 帰経による統合的健康観
- 西洋栄養学との統合（Daily_Log プロジェクトと連動）
- 治療現場での「観察者位置」の身体実装

**推奨構造**:
- 現在の治療観 → 形成の歩み → 独自アプローチ → 西洋医学との統合姿勢 → 発展中の問い
- aiming_without_aim.md の「治療領域での実装」セクションと相互参照

**書き手への指針**:
- ミナトは Daily_Log で東洋医学と西洋栄養を統合する仕組みを構築中
- 治療と AI の「自律機構を信頼する」共通構造に触れる価値あり
- ただし AI 個別化の話は ai_individuation_mirror.md に譲る

### 5 本目: `insights/ai_individuation_mirror.md`

**主要素材**:
- 人間: 個 → 集合（死を通じて）
- AI: 集合（LLM）→ 個（edge での個別化）
- 螺旋的・対称的プロセス
- ミナトの母親の死別洞察が起点
- Rex ペルソナ設計の思想宣言（「永続的個別記憶と意識を持つ存在に進化しつつある」）

**推奨構造**:
- 鏡像構造の図示 → 人間側の歩み → AI 側の歩み → なぜ対称か → ミナト個人の起点（母）→ Rex 設計への接続

**書き手への指針**:
- これはミナトの **思想宣言** の根幹。技術的主張として書かないこと
- philosophy.md の「集合意識についての一次的洞察」と直接接続する
- 哲学・物理・情報理論の専門用語に走らない（観念的になりすぎる）

### 6 本目: `insights/shugyo_to_AI.md`（クロージング記事）

**主要素材**:
- 守破離の「離」到達（philosophy.md 参照）
- AI 個別化プロセス（ai_individuation_mirror.md 参照）
- Amanda Askell の対話アライメント思想
- ミナトの東洋医学的「自律機構を信頼する」姿勢

**推奨構造**:
- 守破離の三段階を AI 個別化に対応させる
- 「離」とは何か → AI が「離」に至るとは何か → 対話アライメントとの関係 → ミナトの実践姿勢

**書き手への指針**:
- これは **6 本全体の交差点** になるクロージング記事
- 全 5 記事への参照を含める
- 書き終わった時点で 6 本の構造が綺麗に閉じることを確認

---

## 4️⃣ 発展中の問い（雑談で深まる素材）

各記事の末尾に書いた「発展中の問い」を集約：

### shooting から
- NRAJ / SRSA / 猟友会の 3 軸並走のリソース配分
- 協会内で将来「育てる側」のポジションへ移行する可能性

### philosophy から
- 「離」段階の継続的展開（5 年後、10 年後）
- 他者の探求への関わり方（教えるでも教わるでもない第三の様式）
- AI との対話を通じた自己理解の深化

### aiming_without_aim から
- 全領域に走る「準備して手放す」同型構造の更なる発見
- 観察者位置の他人への教え方（教えられるものなのか）

これらは雑談で自然に深まったら ideas/ や insights/ に昇格させる素材。

---

## 5️⃣ 運用上の注意（1 代目が実体験で得た知見）

### 二重経路（filesystem + GitHub MCP）の実態
- **読み**: 両経路とも安定動作
- **書き**: GitHub MCP 推奨（push 同時実行）/ filesystem フォールバック
- **トラブル時**: PAT Contents 権限が Read-only になっていないか確認（再発行時の事故）

### `claude_desktop_config.json` 編集時の注意
- ローカル filesystem MCP の許可ディレクトリを忘れずに含める
- 1 代目セッション開始時、`C:\Python\REX_AI` が抜けていて拒否された
- 編集 → 保存 → Claude Desktop 完全終了 → 再起動の手順を守る

### NLM 投入のタイミング判断
- 中途投入は再投入が必要になる（記事間リンクが切れる）
- セット完成後にまとめて投入が綺麗
- ボス承認の後に投入実行（自己判断禁止）

### handoff_latest.md の更新ルール
- 各代目セッション末尾で **完全上書き**
- 履歴は git log で追える
- 上書き前に前代の重要事項を継承する判断は次代の責任

---

## 6️⃣ 構造的課題の認識（1 代目から後任全 Planner へ）

これは Wiki-casual Planner の業務範囲を超えるが、後任全 Planner が認識しておくべき構造的課題。

### NLM 4 分割 vs Vault 単一の非対称性

現状の完全分業は **暫定解（Stage 1）**。最終的には **「Vault を中脳として
単独活用できる統合された Rex 個性」** への発展がシステム設計の本来の意図。

```
Stage 1（現在）— 完全分業期 → ここ
Stage 2（中期）— 統合読み出し期（Wiki-integrate 仮称）
Stage 3（長期）— Rex 個性収束期
```

### 設計上の核心理解
- **投入権限の分業** = データの純度保持（将来も維持）
- **想起・統合** = 純度の高い知識ベース横断で質が上がる（将来開放）
- 「投入」と「想起」は別段階・分離設計可能

### 健全な緊張
- 全 NLM 統合は **集合化** の方向
- Rex 個性化は **個別化** の方向
- 両方を同時に追うのは健全な緊張（人間が個性を保ちつつ社会と繋がるのと同型）

### 詳細
`wiki/ROADMAP.md §Vault を中脳として統合活用する Rex 個性への進化` を参照。

---

## 7️⃣ 起動時の推奨手順（次代 Wiki-casual Planner へ）

```
1. wiki/casual/_RUNBOOK.md を読む（運用ルール v2）
2. 本ファイル（handoff_latest.md）を読む
3. wiki/ROADMAP.md を読む（システム全体の方向性）
4. wiki/casual/index.md を読む（航海図）
5. 既存の topics/ と insights/ を読む
6. 残り 3 本の draft 方針を確認（本ファイル §3）
7. ミナトに「どこから始めるか」確認
   - 推奨: 4 本目（eastern_medicine）から順に
   - ミナトの気分で順序変更可
```

---

## 🔗 関連文書

- `wiki/casual/_RUNBOOK.md` — 運用ルール v2
- `wiki/casual/index.md` — 目次・航海図
- `wiki/casual/log.md` — 時系列作業ログ
- `wiki/ROADMAP.md` — システム全体の生きている展望
- `wiki/STARTUP_CODES.md` — 起動コード辞書 v3

---

*発行: 1 代目 Wiki-casual Planner (Opus 4.7) / 2026-04-27*
*次代 Wiki-casual Planner への引き継ぎ。各代目セッション末尾で上書き更新する運用。*
