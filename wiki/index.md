# index.md — REX_Brain_Vault 全ページ目次

**バージョン**: v2（3リポ体制対応・Phase 1-2 完了反映版）
**最終更新**: 2026-04-22 / 7代目統括 Evaluator (Opus 4.7)
**前版**: v1（2026-04-16 / Wiki Phase 1 構築時点）

---

## このファイルの役割

REX_Brain_Vault 全体の目次。「どこに何があるか」を把握するための
ナビゲーション層。個別ファイルの内容詳細は各ファイル自身か、
専用メタファイル（doc_map.md 等）を参照。

---

## 🗺️ Vault 全体構造マップ（3リポ体制対応）

```
REX_Brain_Vault/                          ← ハブ層（独立 Git リポ）
│
├── CLAUDE.md                             ← Vault 運用手順（明示的読込用）
├── README.md                             ← リポ概要
├── .gitignore
│
├── raw/                                  ← 元資料（イミュータブル・読むだけ）
│   └── system_build/                     ← システム構築過程の記録
│
└── wiki/
    ├── index.md                          ← 本ファイル
    ├── log.md                            ← 時系列作業ログ（追記のみ）
    │
    ├── trade_system/                     ← Trade_System 専用層（稼働中）
    ├── trade_brain/                      ← ⬜ 未構築（Phase D 着手対象）
    ├── cross/                            ← プロジェクト横断ナレッジ（骨組のみ）
    ├── handoff/                          ← セッション引き継ぎ
    │
    ├── entities/                         ← 旧配置・wiki/trade_system/entities/ へ移行待ち
    └── decisions/                        ← 旧配置・wiki/trade_system/decisions/ へ移行待ち
```

---

## raw/（元資料・イミュータブル）

| ファイル | 内容 | 状態 |
|---|---|---|
| raw/system_build/EX_DESIGN_CONFIRMED-2026-3-31.md | Trade_System 設計確定文書（#025 完了版） | 🕰️ 歴史記録 |
| raw/system_build/HP-DESIGN-CONFIRMED_6.md | セトナHP構築進捗記録 | 🕰️ 歴史記録 |
| raw/system_build/スレ引き継ぎ指示書_vol9.md | 手動引き継ぎ指示書（最終版・資産化） | 🕰️ 歴史記録 |

---

## wiki/trade_system/（Trade_System 専用管理・稼働中）

### メタ管理ファイル

| ページ | 内容 | 最終更新 | 状態 |
|---|---|---|---|
| [[trade_system/_RUNBOOK]] | Trade_System Wiki 運用ガイド | 2026-04-18 | ✅ |
| [[trade_system/doc_map]] | 設計文書バージョン管理・NLM 構成詳細 | **2026-04-22 v2** | ✅ 最新 |
| [[trade_system/adr_reservation]] | ADR 採番予約台帳 | 2026-04-20 | ✅ 最新 |
| [[trade_system/pending_changes]] | 決定済み未確定設計変更トラッカー | 2026-04-18 | ⚠️ 要更新 |
| [[trade_system/weekly_workflow]] | 週末 Git 更新ワークフロー（旧） | 2026-04-18 | ⚠️ Trade_Brain 側の WEEKLY_UPDATE_WORKFLOW.md に移管済み |
| [[trade_system/evaluator_wrapup_report_026]] | #026 シリーズ Evaluator 完了報告 | 2026-04-17 | 🕰️ 歴史記録 |

### 構造化ナレッジ

| ディレクトリ | 内容 | 状態 |
|---|---|---|
| trade_system/concepts/ | 設計概念（3ファイル: neck / window / 4h_superiority） | ✅ 第1波完了 |
| trade_system/bug_patterns/ | ADR A〜D の個別ページ | ⬜ 未構築（Phase C 着手対象） |
| trade_system/decisions/ | ADR E の個別ページ | ⬜ 未構築（Phase C 着手対象） |
| trade_system/entities/ | ファイル・関数の仕様 | ⬜ 未構築（Phase C 着手対象） |
| trade_system/patterns/ | 戦略パターン（DB / IHS / ASCENDING） | ⬜ 未構築（Phase C 着手対象） |
| trade_system/sources/ | 設計文書の要約 | ⬜ 未構築（Phase C 着手対象） |

---

## wiki/trade_brain/（Trade_Brain 専用管理・⬜ 未構築）

**現状**: ディレクトリごと未作成。Phase D 着手対象。

骨組み設計は `Trade_Brain/docs/STRATEGY_WIKI_GUIDE.md` 側に存在する。
実体構築時は以下の想定構造となる:

```
wiki/trade_brain/
├── _RUNBOOK.md
├── index.md
├── log.md
├── Regimes/
├── Signals/
├── Events/
├── Instruments/  ← 4週 Rolling Window 内蔵
├── Patterns/
├── Hypotheses/
└── Journal/
```

管理ポリシーは `Trade_Brain/docs/STRATEGY_WIKI_GUIDE.md` 参照。

---

## wiki/cross/（プロジェクト横断ナレッジ・骨組のみ）

| ページ | 内容 | 状態 |
|---|---|---|
| [[cross/index]] | 横断ナレッジ目次 | ⬜ 骨組のみ（Phase B 以降） |

**蓄積対象**（Phase B で整備予定）:
- LLM 運用パターン（プロンプト設計・引き継ぎ教訓・トークン最適化）
- MCP 活用ノウハウ（filesystem / NLM / GitHub）
- 3階層 CLAUDE.md 棲み分けの運用知見
- 設計文書管理の教訓（旧版混在事故・archive 運用）

---

## wiki/handoff/（セッション引き継ぎ）

| ファイル | 内容 | 状態 |
|---|---|---|
| [[handoff/latest]] | 統括 Evaluator / 3リポ横断セッション引き継ぎ | **v5 2026-04-22 最新** |

**重要**: 新スレッド開始時はまず `handoff/latest.md` を読む。
「読み込み検証チェックリスト（10問）」に全問回答してから作業開始すること。

---

## wiki/entities/（旧配置・移行待ち）

| ファイル | 内容 | 移行先 |
|---|---|---|
| [[entities/window_scanner]] | 窓ベーススキャナー（#025 完了・#026d 拡張） | → trade_system/entities/ |
| [[entities/entry_logic]] | エントリーロジック（#018 凍結） | → trade_system/entities/ |
| [[entities/exit_logic]] | 4段階決済ロジック（#009 確定・方式 B 迂回中） | → trade_system/entities/ |
| [[entities/swing_detector]] | Swing 検出パラメータ一覧（1H n=3 変更確定） | → trade_system/entities/ |

**扱い**: Phase C で `wiki/trade_system/entities/` に統合予定。それまで旧配置で保全。

---

## wiki/decisions/（旧配置・移行待ち）

| ファイル | 内容 | 移行先 |
|---|---|---|
| [[decisions/025_fixed_neck]] | 固定ネック原則（sh_vals.iloc[0]）の設計根拠 | → trade_system/decisions/ |
| [[decisions/026_manage_exit]] | 決済統合の設計方針・完了条件 | → trade_system/decisions/ |

**扱い**: Phase C で `wiki/trade_system/decisions/` に統合予定。それまで旧配置で保全。

---

## 🎯 現在の優先タスク（2026-04-22 時点）

```
🔴 ボス判断待ち:
   ① Phase 3 着手可否（責務別ディレクトリ化・Trade_System）
   ② 新機能実装の優先順位（ロット調整 / ボラ係数 / Trade_Brain 合流）
   ③ NLM 凍結解除のタイミング

🟡 統括 Evaluator 保留中（原則γ 適用）:
   ① Trade_Brain wiki/ 骨組み構築（Phase D）
   ② Trade_System wiki 空ディレクトリ充填（bug_patterns 等・Phase C）
   ③ wiki/entities/ + wiki/decisions/ の新配置への統合

🟢 継続運用:
   ① 週次 Git 更新（Trade_Brain 側・WEEKLY_UPDATE コマンド）
   ② セッション末尾の log.md 追記
   ③ MTF_INTEGRITY_QA.md への判断追記義務

⬜ ボス再開指示待ち:
   ① REX_027 Task A-E
   ② D-11 / F-7 ADR 本文採番
```

---

## 🔗 NLM 参照（2026-04-22 時点）

**⚠️ 両 NLM は現在凍結中**（ID 取得のみ・投入ゼロ）

```
REX_System_Brain : da84715f-9719-40ef-87ec-2453a0dce67e  — Trade_System 用・凍結中
REX_Trade_Brain  : 4abc25a0-4550-4667-ad51-754c5d1d1491  — Trade_Brain 用・凍結中
旧 REX_Trade_Brain: 2d41d672-f66f-4036-884a-06e4d6729866 — 切り離し済・参照禁止
```

詳細（投入予定リスト・旧 NLM 投入履歴等）は [[trade_system/doc_map]] v2 参照。

---

## 📚 関連文書への横断リンク

```
Vault 運用手順:
  CLAUDE.md（Vault 直下）

Trade_System 側重厚文書:
  Trade_System/docs/SYSTEM_OVERVIEW.md          — Trade_System 現状
  Trade_System/docs/ADR.md                      — 判断記録（D-1〜D-13 / E-1〜E-8 / F-1〜F-8）
  Trade_System/docs/EX_DESIGN_CONFIRMED.md      — 設計仕様
  Trade_System/docs/src_inventory.md            — src/ 配下 Phase 1-2 統合版
  Trade_System/docs/Base_Logic/MINATO_MTF_PHILOSOPHY.md  — 裁量思想（全判断の上位）
  Trade_System/docs/Base_Logic/MTF_INTEGRITY_QA.md       — 裁量整合性 QA（追記義務）
  Trade_System/docs/Evaluator_HANDOFF.md        — Phase 1-2 完了 / Phase 3 引き継ぎ

Trade_Brain 側重厚文書:
  Trade_Brain/CLAUDE.md                         — Trade_Brain 運用ルール・RTK
  Trade_Brain/docs/SYSTEM_OVERVIEW.md           — Trade_Brain 現状
  Trade_Brain/docs/STRATEGY_WIKI_GUIDE.md       — Wiki 構造・Rolling Window 設計
  Trade_Brain/docs/WEEKLY_UPDATE_WORKFLOW.md    — 週末運用（8段階チェックリスト）
  Trade_Brain/docs/distillation_schema.md       — 蒸留スキーマ仕様
```

---

*発行: 7代目統括 Evaluator (Opus 4.7) / 2026-04-22*
*次回更新トリガー: Phase 3 着手時 / wiki/trade_brain/ 構築時 / wiki/entities・decisions 移行時*
