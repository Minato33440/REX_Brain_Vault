# index.md — REX_Brain_Vault 全ページ目次

最終更新: 2026-04-16

---

## raw/（元資料・イミュータブル）

| ファイル | 内容 | 最終更新 |
|---|---|---|
| EX_DESIGN_CONFIRMED-2026-3-31.md | Trade System 設計確定文書（#025完了版） | 2026-03-31 |
| HP-DESIGN-CONFIRMED_6.md | セトナHP構築進捗記録 | 2026-04-09 |
| スレ引き継ぎ指示書_vol9.md | 手動引き継ぎ指示書（最終版・資産化） | 2026-04-15 |

---

## wiki/trade_system/（Trade System 専用管理）

| ページ | 内容 | 状態 |
|---|---|---|
| [[doc_map]] | 設計文書バージョン管理マップ・NLM投入状況 | ✅ |
| [[adr_reservation]] | ADR採番予約台帳（要望1・二重採番防止） | ✅ 新規 |
| [[pending_changes]] | 決定済み未確定設計変更トラッカー（要望3） | ✅ 新規 |
| [[pending_nlm_sync]] | NLM認証切れ時の追加待ちソース（要望2） | 🔲 必要時作成 |

---

## wiki/entities/（ファイル・関数・パラメータ）

| ページ | 内容 | 状態 |
|---|---|---|
| [[window_scanner]] | 窓ベーススキャナー（#025完了・#026dでフィルター追加中） | ✅ |
| [[entry_logic]] | エントリーロジック（#018凍結） | ✅ |
| [[exit_logic]] | 4段階決済ロジック（#009確定・方式B迂回中） | ✅ |
| [[swing_detector]] | Swing検出パラメータ一覧（1H n=3変更確定） | ✅ |

---

## wiki/decisions/（意思決定ログ）

| ページ | 内容 | 状態 |
|---|---|---|
| [[025_fixed_neck]] | 固定ネック原則（sh_vals.iloc[0]）の設計根拠 | ✅ |
| [[026_manage_exit]] | 決済統合の設計方針・完了条件 | ✅ |

---

## wiki/handoff/（引き継ぎプロンプト）

| ファイル | 内容 |
|---|---|
| latest.md | 最新スレ用引き継ぎプロンプト（セッション毎に上書き） |

---

## 現在の優先タスク（クイック参照）

```
🔴 Trade System #026d — 4H構造優位性フィルター（neck_4h >= neck_1h）
   担当: Planner + Evaluator + ClaudeCode（別プロジェクト）
   参照: doc_map.md → REX_026d_spec / ADR D-10

🟡 #026d完了後: ADR D-8/D-9/D-10 を本体統合（Evaluator担当）
   参照: adr_reservation.md → pending_changes.md

⏳ セトナHP — GSC登録・MailPoetフォーム設置・DKIM最終確認
```

---

## NotebookLM REX_Trade_Brain 投入済みソース（2026-04-16時点）

| ソース | source_id | 状態 |
|---|---|---|
| EX_DESIGN_CONFIRMED-2026-3-31.md | （初回 Ingest） | ✅ |
| HP-DESIGN-CONFIRMED_6.md | （初回 Ingest） | ✅ |
| ADR-2026-04-14_2_2.md | 404dc00e | ✅ |
| SYSTEM_OVERVIEW 2026-3-26.md | c5ed4a03 | ✅ |
| PLOT_DESIGN_CONFIRMED-2026-3-31.md | 771d6f59 | ✅ |
| REX_BRAIN_SYSTEM_GUIDE v1（2026-04-15） | e757315f | ⚠️ v2に更新 |
| REX_026d_spec.md | 3dadc5d1 | ✅ |
| REX_BRAIN_SYSTEM_GUIDE v2（2026-04-16） | ba0bf71f-24a0-4c23-b1f0-7d0c120c0d74 | ✅ |
