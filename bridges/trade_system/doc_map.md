# wiki/trade_system/doc_map.md
# Trade_System — 設計文書バージョン管理マップ
# バージョン: v2（3リポ体制対応版・NLM凍結状態反映版）
# 更新: 2026-04-22 / 7代目統括 Evaluator (Opus 4.7)
# 前版: v1（2026-04-17 / #026d 完了時点）

---

## 設計文書管理の基本原則

1. **不変原則**: 一度確定した設計文書は絶対に編集しない（raw/ と同じ扱い）
2. **新規作成原則**: タスク番号が進んで設計が変わった場合は新しい .md を作成
3. **日付なし運用**: EX_DESIGN / SYSTEM_OVERVIEW / ADR は日付なしファイル名が「常に最新」
4. **NotebookLM クエリ**: 有効な設計文書を NLM に投入する（投入対象は本ファイルで管理）
5. **スレッド引き継ぎ**: 本ファイルを読めばどの doc が最新かが分かる

---

## 🆕 3リポ体制における本ファイルのスコープ（2026-04-22 追記）

本ファイルは **Trade_System リポの設計文書のみ** を管理する。
姉妹リポ Trade_Brain の文書管理は `Trade_Brain/docs/SYSTEM_OVERVIEW.md` 側で行う。

役割分担原則（ADR F-8 派生原則）:

```
Trade_System  : シグナル / Fibonacci / BackTest（動的ロジック側）← 本ファイルの管轄
Trade_Brain   : 市況データ / トレード履歴 / レジーム判定 / Plot 抽出（静的データ側）
              → 管轄外。文書管理は Trade_Brain 側で別運用
```

---

## 現在の有効設計文書（2026-04-22 時点・8件）

| ファイル | 最終更新 | カバー範囲 | 状態 |
|---|---|---|---|
| **ADR.md** | **2026-04-20** | **バグ D-1〜D-13 / 判断 E-1〜E-8 / 方針 F-1〜F-8（D-11/F-7 予約保持）** | **✅ 有効（最新）** |
| **EX_DESIGN_CONFIRMED.md** | 2026-04-17 | MTF 設計全体・#026d 完了版 | ✅ 有効 |
| **SYSTEM_OVERVIEW.md** | **2026-04-20** | **Phase 1-2 完了・断捨離後スナップショット** | **✅ 有効（最新）** |
| 🆕 **src_inventory.md** | **2026-04-20** | **src/ 配下 Phase 1-2 統合版・地雷 8 項目** | **✅ 有効（新規追加）** |
| 🆕 **Base_Logic/MINATO_MTF_PHILOSOPHY.md** | **2026-04-18** | **裁量思想・最上位設計哲学（全実装の上位）** | **✅ 有効（新規追加）** |
| 🆕 **Base_Logic/MTF_INTEGRITY_QA.md** | **2026-04-20 追記型** | **裁量整合性 Q&A 1 次資料・継承義務あり** | **✅ 有効（新規追加）** |
| 🆕 **Evaluator_HANDOFF.md** | **2026-04-20 v4** | **Phase 1-2 完走 / Phase 3 引き継ぎ** | **✅ 有効（新規追加）** |
| PLOT_DESIGN_CONFIRMED-2026-3-31.md | 2026-03-31 | プロット関数設計（#025 まで網羅） | ✅ 有効（継承） |
| REX_BRAIN_SYSTEM_GUIDE.md | 2026-04-15 | セカンドブレインシステム利用ガイド | ✅ 有効（継承） |

---

## docs/archive 済み（参照禁止）

| ファイル | アーカイブ日 | 理由 |
|---|---|---|
| EX_DESIGN_CONFIRMED-2026-3-31.md | 2026-04-17 | #026d 完了版に置換 |
| SYSTEM_OVERVIEW-2026-3-26.md | 2026-04-17 | #026d 完了版に置換 |
| ADR-2026-04-14_2_2.md | 2026-04-17 | ADR.md 統合版に置換 |

---

## NLM 構成（2026-04-22 時点）

### 🧊 REX_System_Brain（Trade_System 専用・現在凍結中）

```
Notebook ID: da84715f-9719-40ef-87ec-2453a0dce67e
用途:        Trade_System 設計文書の RAG クエリ基盤（将来）
構築日:      2026-04-18（旧 NLM 切り離しと同時に新規作成）
現在の状態:  ID 取得のみ・投入ゼロ・凍結中（2026-04-22 ボス確認済み）
```

### 🆕 投入予定ソースリスト（2026-04-22 時点・凍結中）

**現状**: 新 REX_System_Brain は**ID 取得のみで投入 0 件の凍結状態**。
2026-04-18 の NLM 再構築以降、ソース追加は一度も実施されていない。

**投入予定ソース**（凍結解除後に実施）:

| 優先 | ファイル | 投入理由 | 投入時 source_id |
|---|---|---|---|
| 🔴 高 | Base_Logic/MINATO_MTF_PHILOSOPHY.md | 裁量思想・全判断の上位規範 | — |
| 🔴 高 | Base_Logic/MTF_INTEGRITY_QA.md | 裁量整合性 QA・継承義務あり | — |
| 🔴 高 | ADR.md | バグパターン + 判断記録 + 方針ガイド（F-8 3 原則） | — |
| 🔴 高 | SYSTEM_OVERVIEW.md | Phase 1-2 完了版・現状スナップショット | — |
| 🟡 中 | EX_DESIGN_CONFIRMED.md | #026d 設計仕様 | — |
| 🟡 中 | src_inventory.md | Phase 1-2 統合版・地雷 8 項目 | — |
| 🟡 中 | Evaluator_HANDOFF.md | Phase 3 引き継ぎ | — |
| 🟢 低 | PLOT_DESIGN_CONFIRMED-2026-3-31.md | プロット関数設計 | — |
| 🟢 低 | REX_BRAIN_SYSTEM_GUIDE.md | ブレインシステム利用ガイド | — |

**Ingest 実施タイミング**: **現在凍結中**（ボス判断）。再開指示があるまで待機。
凍結解除時は本リストを手順書として順次 `source_add` を実行し、各行の
「投入時 source_id」を埋めて本ファイルを更新する。

### ⚠️ 切り離し済：旧 REX_Trade_Brain（歴史記録・参照禁止）

```
Notebook ID: 2d41d672-f66f-4036-884a-06e4d6729866
切り離し日: 2026-04-18
切り離し理由: RAG 汚染排除（却下案・修正前実装の混入で再発バグを誘発するリスク）
過去の投入履歴: Git コミット履歴および下記参考表で保全
```

**参考：切り離し前の投入履歴**（参照禁止・歴史記録として保持）

| # | ソース | 追加日 | source_id |
|---|---|---|---|
| 1 | EX_DESIGN_CONFIRMED-2026-3-31（初回） | 2026-04-15 | ee513351 |
| 2 | EX_DESIGN_CONFIRMED-2026-3-31.md（04-16 修正） | 2026-04-16 | 22c594d5 |
| 3 | ADR-2026-04-14_2_2.md | 2026-04-15 | 404dc00e |
| 4 | ADR_APPENDIX_D8-D10_E7 | 2026-04-17 | 88e26b53 |
| 5 | ADR.md（統合版・D-10/E-7 含む） | 2026-04-17 | 3bd02744 |
| 6 | SYSTEM_OVERVIEW 2026-3-26.md | 2026-04-15 | c5ed4a03 |
| 7 | EX_DESIGN_CONFIRMED.md（#026d 版） | 2026-04-17 | e4bc5060 |
| 8 | SYSTEM_OVERVIEW.md（#026d 版） | 2026-04-17 | 58e2b18b |
| 9 | PLOT_DESIGN_CONFIRMED-2026-3-31.md | 2026-04-15 | 771d6f59 |
| 10 | REX_026d_spec.md | 2026-04-15 | 3dadc5d1 |
| 11 | REX_BRAIN_SYSTEM_GUIDE v2 | 2026-04-16 | ba0bf71f |
| 12 | REX_BRAIN_SYSTEM_GUIDE v1 | 2026-04-15 | e757315f |
| 13 | HP-DESIGN-CONFIRMED_6 | 2026-04-15 | 05e21ff1 |

**注**: 上記 source_id はすべて旧 Notebook (`2d41d672-...`) 内のもので、MCP 接続切り離し
により現在は参照不可。新 REX_System_Brain では全て再投入が必要。

### 姉妹 NLM（参照のみ・本ファイルの管轄外）

```
REX_Trade_Brain  : 4abc25a0-4550-4667-ad51-754c5d1d1491  — Trade_Brain 用
                 → 同様に ID 取得のみ・投入ゼロ・凍結中（2026-04-22 ボス確認済み）
                 → 管理は Trade_Brain/docs/SYSTEM_OVERVIEW.md 側で行う
```

---

## 現在の実装状況（2026-04-22 時点）

```
#026シリーズ 完了 ✅（2026-04-17）
  PF 4.54 / 勝率 60% / MaxDD 35.8p / +150.6p / 10件 LONG

REX_028 Phase 1 完了 ✅（2026-04-20）
  src/ 棚卸し・分類・Trade_Brain 移設・archive 隔離

REX_028 Phase 2 完了 ✅（2026-04-20）
  track_trades.py 隔離・plotter.py 両リポ共存方針確定（F-8 派生原則）

REX_028 Phase 3 ⬜ 未着手
  責務別ディレクトリ化（src/core/ viz/ scan/ tests/）
  完了条件: #026d バックテスト数値完全不変
  ボス判断待ち

REX_028 Phase 4 ⬜ 未着手（REX_029 以降）
  D-12（stage2 建値移動削除）・D-13（stage3 1H実体確定削除）
  裁量整合版 exit_simulator.py 再実装
  新 PF を静的点として記録

NLM Ingest ⬜ 凍結中
  REX_System_Brain（da84715f-...）: ID 取得のみ・投入 0 件
  REX_Trade_Brain（4abc25a0-...） : ID 取得のみ・投入 0 件
  再開はボス指示待ち
```

---

## 陳腐化トリガー

| タスク | 影響を受ける doc | アクション |
|---|---|---|
| Phase 3 着手・完了 | SYSTEM_OVERVIEW / src_inventory | 完了時に更新 → 新 NLM 追加（凍結解除後） |
| Phase 4 実装訂正 | EX_DESIGN_CONFIRMED / ADR / SYSTEM_OVERVIEW / MINATO_MTF_PHILOSOPHY 第3章 | 新 PF 確定時に全更新 |
| 新 NLM 凍結解除・初回 Ingest | 本ファイル（投入予定→投入済み source_id 記録） | Ingest 実施時に即更新 |
| MINATO_MTF_PHILOSOPHY 第0章追記 | 同ファイル（原則α/β/γ 正式反映） | ボス承認後 |
| REX_027 Task A 再開 | D-11 / F-7 ADR 本文採番 | 再開指示時 |
| SHORT 再開 | EX_DESIGN / MINATO_MTF_PHILOSOPHY 前提 | 新バージョン作成 |

---

## neck 用途定義（地雷1の恒常的防止）

```
neck_15m → エントリートリガー（5M High >= neck_15m + 7pips で指値約定）
neck_1h  → 窓特定アンカー + 4H構造優位性フィルター基準値
neck_4h  → 半値決済トリガー（段階2: High >= neck_4h → 50%決済）
条件: neck_4h >= neck_1h（ADR D-10）
```

---

## 関連文書（🆕 v2 で追加）

```
上位規範:
  Base_Logic/MINATO_MTF_PHILOSOPHY.md  — 裁量思想（全判断の上位）
  ADR.md F-8                            — 裁量思想 3 原則 + 派生原則 2 つ

整合性監査:
  Base_Logic/MTF_INTEGRITY_QA.md        — 裁量整合性 QA（追記義務あり）

Vault ハブ:
  REX_Brain_Vault/wiki/handoff/latest.md            — 3リポ現在地（v5）
  REX_Brain_Vault/wiki/trade_system/adr_reservation.md  — ADR 採番台帳

姉妹リポ対応:
  Trade_Brain/docs/SYSTEM_OVERVIEW.md   — 姉妹リポの同等文書
```

---

*発行: 7代目統括 Evaluator (Opus 4.7) / 2026-04-22*
*管轄: Trade_System リポ設計文書のみ（Trade_Brain は管轄外）*
*次回更新トリガー: 新 NLM 凍結解除・初回 Ingest 実施時 / Phase 3 着手時*
