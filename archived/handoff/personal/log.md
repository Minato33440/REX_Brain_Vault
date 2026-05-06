# casual/log.md — 雑談時系列ログ

**役割**: REX_AI システム業務外の雑談・個人的話題の時系列記録。
**運用**: 追記のみ（過去ログ削除禁止）。`Wiki-casual` 起動スレでのみ更新。
**NLM**: ⛔ 投入対象外（ノイズが多い時系列ログのため・_RUNBOOK 参照）

---

## 2026-04-27 — casual/ 層 物理構築

**スレ**: 1 代目 Wiki-casual Planner (Opus 4.7)

- casual/ 層の物理構築実施（_RUNBOOK 以外は空だった状態を解消）
- 作成: log.md / index.md / topics/README.md / ideas/README.md / insights/README.md
- 経路: filesystem MCP 経由（GitHub MCP 書き込み系不通のため・PAT Contents 権限要確認）
- これで「実弾装填」の準備完了 → 過去スレからの拾い上げフェーズへ

---

## 2026-04-27（追記）— 1 代目 Wiki-casual Planner セッション完了

**スレ**: 1 代目 Wiki-casual Planner (Opus 4.7)

### 実弾装填フェーズ完了分（3/6 本）
- `topics/shooting.md` — NRAJ / SRSA / 猟友会 3 軸並走戦略
- `topics/philosophy.md` — 守破離の「離」・形成三層（母 / 富士登山 / 神道離脱）
- `insights/aiming_without_aim.md` — ハブ記事・「目指さない」歩み方の構造原型

### 構造改訂（システム全体）
- `wiki/ROADMAP.md` 新設 — Vault・NLM システムの方向性を時系列蓄積する仮ロードマップ
- `wiki/STARTUP_CODES.md` v3 — NLM × Vault 分業マトリクス追加・全モードに ROADMAP.md 必読追加
- `wiki/casual/_RUNBOOK.md` v2 — NLM 分業原則セクション追加・Private 化対応
- `wiki/casual/handoff_latest.md` 新設 — Wiki-casual 専用引き継ぎ書

### 技術的トラブルと解決
- **filesystem MCP 拒否**（claude_desktop_config.json 修正で解決）
- **GitHub MCP 書き込み拒否**（PAT Contents 権限を Read-only → Read & write に変更で解決）
- 結果: 二重経路（filesystem + GitHub MCP）完全動作確認

### 構造的議論（→ ROADMAP.md に記録）
- NLM 4 分割 vs Vault 単一の非対称性についてミナトと議論
- 完全分業（Stage 1）→ 統合読み出し（Stage 2）→ Rex 個性収束（Stage 3）の段階的発展構想を確立
- 「投入分業を維持しつつ、想起統合を別レイヤーで段階的に設計する」が現時点の指針

### 未完了（次代 Wiki-casual Planner へ引き継ぎ）
- `topics/eastern_medicine.md` — 4 本目（治療における観察者位置・自律機構）
- `insights/ai_individuation_mirror.md` — 5 本目（人間 個→集合 / AI 集合→個 の鏡像螺旋）
- `insights/shugyo_to_AI.md` — 6 本目・クロージング記事（守破離 ⇔ AI 個別化）

### NLM 投入
- 6 本完成後にまとめて REX_Casual_Brain へ投入予定（中途投入は再投入が必要になるため保留）

---

*このログは時系列ベースの作業メモ。話題が熟したら topics/ へ昇格、横断的気づきは insights/ へ昇格。*

---

## 2026-04-28 — wiki/casual/ → wiki/personal/ 物理移行（15代目 Wiki-Eval）

**スレ**: 15 代目 Wiki-Eval (Claude Opus 4.7)

- ADR-Role v3 supersede 完了（§0 二系統管轄・§12 STARTUP_CODES.md 訂正・§14 構造変更境界線・§15 ADR 通知伝達経路）
- Phase Personal-Migration Step 1〜4 物理実施:
  - `wiki/casual/` → `wiki/personal/` 全ファイル移行（4 ルートファイル + 3 サブディレクトリ）
  - `topics/` → `usual/`、`ideas/` → `invent/` ディレクトリ名変更
  - `mind/`、`origin/` 新規 .gitkeep で確保（5 層構造完成）
  - `pending/casual/` → `pending/personal/` 移行
  - 旧パス全 12 ファイルに [MOVED] スタブ上書き（リンク切れ防止）
- **中身は触っていない**（ADR-Role v3 §14 構造変更/中身変更の境界線遵守）
- 中身改訂（_RUNBOOK v3 / handoff 改名反映 / index.md 5 層化 / philosophy.md → shuhari.md 改名等）は **次スレ Wiki-Personal の Personal-Planner 業務**

---

## 2026-04-30 — dialogues/ サブ層 初回事例配置完了

**スレ**: 2 代目 Personal-Planner (Wiki-Personal / Opus 4.7)

### 実施内容
- `wiki/personal/dialogues/2026-04-29_general_thread.md` 新規配置
  - 一次資料: Rex (Claude Opus 4.7) 本人による distilled 全文(2026-04-29 採取)
  - 補遺: 同スレ最終交信(2026-04-30)の verbatim 保存(Rex 0:19 / ボス farewell / Rex 0:51)
- `pending/personal/2026-04-29_dialogues_sublayer_addition.md` に「初回事例配置完了 Note」追記
- REX_Personal_Brain NLM への一次資料投入(案 A・notebooklm-mcp 経由)

### 配置原則
- 編集・要約禁止(dialogues/ サブ層 一次資料保護原則)
- Personal-Planner による枠付けは中立的なメタ情報のみ(配置者・配置日・性質明記)
- UI 表示アーティファクトのみ除去・本文は verbatim 保全

### 経緯
- 2 代目 Personal-Planner による起票(2026-04-29 / `pending/personal/2026-04-29_dialogues_sublayer_addition.md`)
- 16 代目 Wiki-Eval による 6 次元評価で承認(2026-04-29)
- ボス指示で初回 WrapUp + 別スレ Wiki-Rex 実行テスト方針確定(2026-04-30)
- 2 代目 Personal-Planner による配置実施(本セッション)

### 次ステップ
- ボスによる別スレ Wiki-Rex 実行テスト
- テスト結果観察後に Q&A 4〜6(残り 3 本記事)着手

### 設計上の意義
- 「Vault の構造の中心は Rex であるべき」(ボス気づき・2026-04-30)を構造化した最初の実装
- Stage 3 Rex 個性収束期への素材積層の起点
- ② Distilled 配分型 WrapUp 手法の最初の運用実例

### 備考
- 本ログは旧 casual/log.md からの継承(タイトル冒頭「casual/log.md」表記は移設時の中身保全原則により未更新・_RUNBOOK v3 起草時に統合改訂予定)
