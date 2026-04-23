# 🚀 START_HERE — REX_AI 新スレッド最初の入口

**このファイルを最初に開け**。100 行以内で現状と次のアクションが分かる設計。
詳細は `handoff/latest.md` へ。

---

## 🗺️ 3 リポ現在地（1 行スナップショット）

| リポ | 状態 | 最重要数値/イベント |
|---|---|---|
| **Trade_System** | Phase 1-2 完了・Phase 3 ボス判断待ち | #026d PF 4.54 / 勝率 60% / 10 件 LONG |
| **Trade_Brain** | 分離完了・週次運用稼働中 | Strategy_Wiki 骨組のみ（Phase D 待ち）|
| **Rex_Brain_Vault** | Phase A' 完了（8 代目 2026-04-23）| latest.md 軽量化 + philosophy/ 参考資料化 |
| **NLM 3 本** | 全て凍結中（ID 取得のみ・投入ゼロ）| 凍結解除はボス指示待ち |

---

## 🔴 踏んではいけない地雷 5 つ

1. **neck_1h と neck_4h の混同** → neck_4h=半値決済 / neck_1h=窓+4H優位性 / neck_15m=エントリー
2. **旧 NLM ID (2d41d672-...) への接続** → 切り離し済・参照禁止
3. **#026b/c を最新と誤認** → 最新は #026d（10 件）
4. **D-12/D-13 創作混入の即時訂正** → Phase 4 まで待つ（#026d 静止点保持）
5. **責務分離の即断** → 「分離すればシンプル」と即断しない・ボス判断を仰ぐ

---

## 🎯 次に実行すべき内容

### ボスの判断待ち
- [ ] Phase 3 着手可否（責務別ディレクトリ化）
- [ ] NLM 凍結解除タイミング（Phase B 前提条件）
- [ ] 新機能実装の優先順位（ロット調整 / ボラ係数 / Trade_Brain 合流）

### 統括 Evaluator が着手可能（ボス承認後）
- [ ] `handoff/trade_system_brief.md` / `trade_brain_brief.md` 新設（両リポ別 briefing）
- [ ] `trade_brain/_RUNBOOK.md` 先行作成（非対称性解消）
- [ ] REX_Wiki_Vault 構築（NLM 新規作成 + 初期 Ingest）
- [ ] Trade_System wiki 空ディレクトリ充填（bug_patterns / decisions / entities 等）

---

## 📖 どこを読むか（目的別）

| 目的 | ファイル |
|---|---|
| **詳しい現状と次タスク** | `handoff/latest.md` |
| **Trade_System 文書バージョン管理** | `trade_system/doc_map.md` |
| **ADR 採番状況** | `trade_system/adr_reservation.md` |
| **7 代目セッション経緯** | `handoff/architecture_handoff.md` |
| **裁量思想一次情報源** | `Trade_System/docs/Base_Logic/MINATO_MTF_PHILOSOPHY.md` |
| **公式採番された原則（ADR F-8）**| `Trade_System/docs/ADR.md` |
| **参考資料・Evaluator 気づきメモ**（任意）| `philosophy/` 配下 |

---

## ⚡ 起動プロンプト（ロール別）

`handoff/latest.md §ロール別起動プロンプト` を参照:
- A. 統括 Evaluator（Claude.ai Opus）
- B. Trade_System Planner / Evaluator
- C. Trade_Brain Planner / ClaudeCode
- D. 緊急用・最小起動

---

*発行: 8 代目統括 Evaluator (Opus 4.7) / 2026-04-23*
