# REX_AI システム全体アーキテクチャー — 事実記録

**位置付け**: 4 リポ体制の**事実記録**。構造記述のみ・強制力なし。
**本ファイルの性質**: 参考資料。Evaluator / Planner / ClaudeCode がシステム全体像を把握したい時に開く。
**一次情報源**: ボス原文（2026-04-22 / 2026-04-23）

---

## 4 リポ体制（全体図）

```
┌────────────────────────────────────────────────────────────────┐
│ Git リポ層（3 リポ・全て現状維持・新規作成なし）              │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Trade_System     ← 動的ロジック側（実装・BackTest）          │
│                    凍結ファイル + #026d PF 4.54 静的保持       │
│                                                                │
│  Trade_Brain      ← 静的データ側（logs / distilled）          │
│                    WEEKLY_UPDATE 運用・週次蓄積                │
│                                                                │
│  Rex_Brain_Vault  ← Rex の頭脳・統合層                        │
│                    REX_AI 配下の全リポ情報を共有統合           │
│                    将来の進化先: 市場環境データ精密図書館      │
│                                                                │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│ NotebookLM 層（3 Notebook・個別化原則・現在凍結中）           │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  REX_System_Brain  : da84715f-9719-40ef-87ec-2453a0dce67e      │
│                      Trade_System 専用（凍結中・投入ゼロ）    │
│                                                                │
│  REX_Trade_Brain   : 4abc25a0-4550-4667-ad51-754c5d1d1491      │
│                      Trade_Brain 専用（凍結中・投入ゼロ）     │
│                                                                │
│  REX_Wiki_Vault 🆕 : 未作成                                    │
│                      両プロジェクト共用（自己増殖ナレッジ）    │
│                                                                │
└────────────────────────────────────────────────────────────────┘

⚠️ 切り離し済（参照禁止）:
   旧 REX_Trade_Brain: 2d41d672-f66f-4036-884a-06e4d6729866
   切り離し日: 2026-04-18 / 理由: RAG 汚染排除
```

---

## Vault と NLM の役割分担

ボス原文（2026-04-23）:

> ①ローカルの Obsidian-Vault は Rex の頭脳なので REX_AI 配下の全てのリポ情報を共有統合。
> ②NLM はラグなのでバグ防止のため敢えて個別化
> ・REX_Trade_Brain：Git の Trade_Brain 専用
> ・REX_System_Brain：Git の Trade_System 専用
> ・REX_Wiki_Vault：は共有知識なので Trade_System と Trade_Brain 共用

### 構造的対応

| 層 | 性質 | 役割 |
|---|---|---|
| Obsidian Vault（Rex_Brain_Vault）| 全統合 | 関連付け・編集・統合的理解 |
| NotebookLM（3 Notebook）| 個別化 | ドメイン分離・混同防止・クエリ精度保持 |

---

## 各 NLM の投入想定

| NLM | 投入対象（想定）| 現状 |
|---|---|---|
| REX_System_Brain | Trade_System 設計文書（ADR / EX_DESIGN / MINATO_MTF_PHILOSOPHY / MTF_INTEGRITY_QA / SYSTEM_OVERVIEW 等）| 凍結中・投入ゼロ |
| REX_Trade_Brain | Trade_Brain 蒸留（distilled / brain_pack / 市場環境データ）| 凍結中・投入ゼロ |
| REX_Wiki_Vault | ナレッジシステム運用情報（latest.md / log.md / philosophy/ 等）| 未作成 |

---

## NLM 凍結ポリシー（2026-04-22 ボス確認）

### 現状

両 NLM とも ID 取得のみ・投入ゼロ・凍結中

### 凍結理由

- #026d 以前の ADM や引継ファイルは MTF ロジック誤認や創作コードの記載が多い → RAG 汚染リスク
- #027 以降はシステム分割作業・ナレッジシステム構築が主 → クリーンな出発点
- 凍結解除はボス指示待ち

### 運用上の含意

- NLM クエリは現段階では意味ある回答を返さない
- 引き継ぎ・設計判断は Vault `wiki/` + リポ `docs/` を 1 次情報源とする
- NLM 前提の作業計画は立てない

---

## ファイルシステム配置（2026-04-23 時点）

```
C:\Python\REX_AI\
├── Trade_System\          ← Git リポ: Minato33440/Trade_System
│   └── docs\
│       └── Base_Logic\    ← 裁量思想一次情報源
│
├── Trade_Brain\           ← Git リポ: Minato33440/Trade_Brain
│   ├── logs\              ← 週次運用・追記のみ
│   ├── distilled\         ← 月次蒸留
│   └── docs\
│
└── REX_Brain_Vault\       ← Git リポ: Minato33440/REX_Brain_Vault
    ├── CLAUDE.md          ← Vault 運用指示
    ├── raw\               ← 元資料（イミュータブル）
    └── wiki\
        ├── START_HERE.md  ← 新スレ入口
        ├── index.md       ← 全ページ目次
        ├── log.md         ← 時系列ログ
        ├── philosophy\    ← 参考資料・Evaluator の気づきメモ
        ├── handoff\
        │   ├── latest.md             ← 現在地ダッシュボード
        │   └── architecture_handoff.md ← 7 代目セッション記録
        ├── trade_system\  ← Trade_System 専用層
        ├── trade_brain\   ← ⬜ 未構築
        ├── cross\         ← 骨組のみ
        ├── entities\      ← 旧配置
        └── decisions\     ← 旧配置
```

---

## 三階層 CLAUDE.md の棲み分け

```
~/.claude/CLAUDE.md            — RTK 設定（全リポ共通・自動読込）
Trade_System/.CLAUDE.md        — Trade_System 固有ルール（自動読込）
REX_Brain_Vault/CLAUDE.md      — Vault 運用手順（明示的読込）
```

---

## 関連文書

- `CLAUDE.md`（Vault 直下）— Vault 運用手順
- `handoff/latest.md` — 現在地ダッシュボード
- `philosophy/cross_vectors.md` — 4 横断ベクトル事実記録
- `philosophy/evaluator_code.md` — 各代 Evaluator の気づきメモ

---

*記録: 8 代目統括 Evaluator / 2026-04-23*
*縮退: 強制口調除去・事実記述のみに再整理*
