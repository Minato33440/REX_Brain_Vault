# wiki/trade_system/doc_map.md
# Trade System — 設計文書バージョン管理マップ
# 更新: 2026-04-17（ADR.md完全版作成・NLM投入完了）

---

## 設計文書管理の基本原則

1. **不変原則**: 一度確定した設計文書は絶対に編集しない（raw/ と同じ扱い）
2. **新規作成原則**: タスク番号が進んで設計が変わった場合は新しい .md を作成
3. **日付なし運用**: EX_DESIGN / SYSTEM_OVERVIEW / ADR は日付なしファイル名が「常に最新」
4. **NotebookLM クエリ**: 全バージョンを NLM に投入済み
5. **スレッド引き継ぎ**: 本ファイルを読めばどの doc が最新かが分かる

---

## 現在の有効設計文書（2026-04-17時点）

| ファイル | 最終更新 | カバー範囲 | 状態 |
|---|---|---|---|
| EX_DESIGN_CONFIRMED.md | 2026-04-17 | MTF設計全体・#026d完了版 | ✅ 有効（最新） |
| **ADR.md** | **2026-04-17** | **バグD-1〜D-10 / 判断E-1〜E-7 / 方針F-1〜F-6** | **✅ 有効（最新・統合版）** |
| SYSTEM_OVERVIEW.md | 2026-04-17 | ファイル構成・依存関係・凍結区分 | ✅ 有効（最新） |
| PLOT_DESIGN_CONFIRMED-2026-3-31.md | 2026-03-31 | プロット関数設計 | ✅ 有効（#025まで網羅） |
| REX_BRAIN_SYSTEM_GUIDE.md | 2026-04-15 | セカンドブレインシステム利用ガイド | ✅ 有効 |

---

## docs/archive 済み（参照禁止）

| ファイル | アーカイブ日 | 理由 |
|---|---|---|
| EX_DESIGN_CONFIRMED-2026-3-31.md | 2026-04-17 | #026d完了版に置換 |
| SYSTEM_OVERVIEW-2026-3-26.md | 2026-04-17 | #026d完了版に置換 |
| ADR-2026-04-14_2_2.md | 2026-04-17 | ADR.md統合版に置換 |

---

## NotebookLM（REX_Trade_Brain）投入済みソース

| ソース | 追加日 | source_id | 状態 |
|---|---|---|---|
| EX_DESIGN_CONFIRMED-2026-3-31.md（初回） | 04-15 | ee513351 | 旧版 |
| EX_DESIGN_CONFIRMED-2026-3-31.md（04-16修正） | 04-16 | 22c594d5 | 旧版 |
| ADR-2026-04-14_2_2.md | 04-15 | 404dc00e | 旧版（D-7まで） |
| ADR_APPENDIX_D8-D10_E7 | 04-17 | 88e26b53 | 旧版（統合版に包含） |
| **ADR.md（統合版・D-10/E-7含む）** | **04-17** | **3bd02744** | **✅ 有効（最新）** |
| SYSTEM_OVERVIEW 2026-3-26.md | 04-15 | c5ed4a03 | 旧版 |
| **EX_DESIGN_CONFIRMED.md（#026d版）** | **04-17** | **e4bc5060** | **✅ 有効（最新）** |
| **SYSTEM_OVERVIEW.md（#026d版）** | **04-17** | **58e2b18b** | **✅ 有効（最新）** |
| PLOT_DESIGN_CONFIRMED-2026-3-31.md | 04-15 | 771d6f59 | ✅ 有効 |
| REX_026d_spec.md | 04-15 | 3dadc5d1 | 参考用 |
| REX_BRAIN_SYSTEM_GUIDE v2 | 04-16 | ba0bf71f | ✅ 有効 |
| REX_BRAIN_SYSTEM_GUIDE v1 | 04-15 | e757315f | 旧版 |
| HP-DESIGN-CONFIRMED_6 | 04-15 | 05e21ff1 | ✅ HP専用 |

---

## 現在の実装状況（2026-04-17 — 全完了）

```
#026シリーズ 完了 ✅
#027 設計文書整理 完了 ✅（Phase A/B/C/D/E）
ADR.md 完全版 完了 ✅（Evaluator・NLM投入済み）

→ 全設計文書が最新化。次のタスク（#028以降）着手可能。
```

---

## 陳腐化トリガー

| タスク | 影響を受ける doc | アクション |
|---|---|---|
| #028以降の実装完了 | EX_DESIGN / SYSTEM_OVERVIEW / ADR | 最新版を上書き → NLM追加 |
| Phase 2 開始 | EX_DESIGN / PLOT_DESIGN | 新バージョン作成 |
| SHORT 再開 | EX_DESIGN | 新バージョン作成 |

---

## neck用途定義

```
neck_15m → エントリートリガー（5M High >= neck_15m + 7pips で指値約定）
neck_1h  → 窓特定アンカー + 4H構造優位性フィルター基準値
neck_4h  → 半値決済トリガー（段階2: High >= neck_4h → 50%決済）
条件: neck_4h >= neck_1h（ADR D-10）
```
