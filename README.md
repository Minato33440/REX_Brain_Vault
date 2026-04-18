# REX_Brain_Vault

REX_AI 全プロジェクトの中枢ナレッジベース。  
Obsidian + NotebookLM + filesystem MCP による自己増殖型知識管理システム。

---

## 目的

スレッドをまたいでも「なぜこの設計にしたか」「今どこまで進んでいるか」を  
ゼロから説明し直さずに済む **持続的な脳**。

LLM が読み書きし、人間が監督する。メンテナンスのコストを LLM が負担し、  
人間はソースの選定・方向性の決定・診断に集中する。

---

## アーキテクチャ

```
REX_Brain_Vault（本リポジトリ）
│
├── raw/                    ← 元資料（イミュータブル・LLMは読むだけ）
│   └── system_build/       ← システム構築過程の記録
│
├── wiki/                   ← LLMが書き・育てる自己増殖層
│   ├── index.md            ← 全ページ目次
│   ├── log.md              ← 時系列作業ログ（追記専用）
│   │
│   ├── trade_system/       ← Trade_System プロジェクト用
│   │   ├── doc_map.md      ← 設計文書バージョン管理
│   │   ├── adr_reservation.md  ← ADR採番予約台帳
│   │   └── pending_changes.md  ← 決定済み未確定変更
│   │
│   ├── setona_hp/          ← Setona_HP プロジェクト用（将来）
│   ├── bl_project/         ← BL_Project 用（将来）
│   │
│   ├── cross/              ← プロジェクト横断ナレッジ
│   │   └── index.md
│   │
│   └── handoff/
│       └── latest.md       ← セッション引き継ぎ（致命的地雷リスト含む）
│
└── CLAUDE.md               ← Vault運用指示書（LLM向け）
```

---

## 3階層 CLAUDE.md

```
~/.claude/CLAUDE.md              グローバル（RTK設定・全リポ共通）
Trade_System/.CLAUDE.md          プロジェクト（不変ルール・パラメータ）
REX_Brain_Vault/CLAUDE.md        Vault（運用手順・引き継ぎ・NLM管理）
```

各層は「誰が・いつ読むか」で責務を分離。  
グローバル = 全セッション自動 / プロジェクト = 当該リポ内で自動 / Vault = 明示的読込。

---

## 対象プロジェクト

| プロジェクト | リポジトリ | NLM | 状態 |
|---|---|---|---|
| **Trade_System** | Minato33440/Trade_System | REX_Trade_Brain | ✅ 稼働中 |
| **Setona_HP** | Minato33440/Setona_HP | — | 🔲 将来 |
| **BL_Project** | （未定） | — | 🔲 将来 |

---

## NotebookLM 連携

各プロジェクトの設計文書を NotebookLM に投入し、RAG クエリで横断検索可能。  
NLM ソースの管理は `wiki/{project}/doc_map.md` で一元管理。

| NLM ノートブック | ID | 用途 |
|---|---|---|
| REX_Trade_Brain | `2d41d672-f66f-4036-884a-06e4d6729866` | Trade_System 設計文書 RAG |

---

## 運用フロー

```
セッション開始
  → CLAUDE.md 読込 → handoff/latest.md 読込（地雷リスト確認）
  → 検証チェックリスト回答 → 作業開始

セッション終了（/wrap-up）
  → log.md 追記 → latest.md 更新 → NLM 同期
  → docs/ 旧版 archive 移動 → git push → プロジェクトナレッジ更新
```

詳細は [CLAUDE.md](CLAUDE.md) を参照。

---

## 前身

本リポジトリは [Second_Brain_Lab](https://github.com/Minato33440/Second_Brain_Lab)（凍結）から移行。  
Second_Brain_Lab はナレッジシステムの構築・テスト用リポジトリとして役割を終え、  
本リポジトリが REX_AI 全体の脳として独立運用される。

構築過程のドキュメントは `raw/system_build/` に保管。

---

## ライセンス

Private repository. All rights reserved.
