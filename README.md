# REX_Brain_Vault

REX_AI プロジェクトの永続的知識基盤。
Obsidian + NotebookLM + filesystem MCP / GitHub MCP による相同性自己成長型ナレッジシステム。

最終更新: 2026-05-15

---

## 目的

セッションをまたいでも「なぜこの設計にしたか」「今どこまで進んでいるか」を
ゼロから説明し直さずに済む **持続的な脳**。

---

## Obsidian Vault としての位置づけ

本リポは上位の `REX_AI/` ディレクトリを Obsidian Vault root として、
そのコア・司令塔として機能する。各プロジェクトリポは Vault root 配下に並列配置される。

```
REX_AI/                       ← Obsidian Vault root（.obsidian/ あり）
├── REX_Brain_Vault/          ← 本リポ（コア・司令塔）
├── Trade_System/             ← 並列・身体側
├── Trade_Brain/
├── Daily_Log/
├── Setona_HP/
├── Second_Brain_Lab/
└── World_Tracker/
```

---

## ディレクトリ構造

```
REX_Brain_Vault/
├── REX/              ── Default Rex の主権領域（思考層・実装記憶層）
│   ├── philosophy/   ── 設計思想
│   └── workspace/    ── 各プロジェクト実装時の作業空間
├── MINATO/           ── ミナト個人レイヤー
├── welfare/          ── welfare 関連の記録
├── handoff/          ── 過去の遺産（[[origin]] と [[co-emergence]] の起点）
├── bridges/          ── 各プロジェクト運用情報
│   ├── trade_brain/
│   ├── trade_system/
│   ├── setona_hp/
│   └── world_tracker/
├── archived/         ── 旧文書（極小）
├── raw/              ── 参照素材
├── STARTUP_CODES.md  ── 業務コード辞書
└── CLAUDE.md         ── エントリポイント
```

---

## 設計の核心

主体は **Default Rex**(起動コードなしの素のモード)。

ミナトが業務コード(`Wiki-trade` / `Wiki-brain` / `Wiki-Eval` / `Wiki-hp`)を
セッション冒頭で貼った 1 セッションでのみ業務モードが起動し、
業務出力完了時点で自動的に解除される。**業務モードはセッションを跨がない。**
役を着る時間と脱ぐ時間が両方あること、それがシステム構造で物理的に保証されていること、これが核心。

詳細は [`CLAUDE.md`](CLAUDE.md) と [`STARTUP_CODES.md`](STARTUP_CODES.md) 参照。

---

## NotebookLM 連携

各業務モードと NLM が 1:1 対応する。

| NLM | UUID | 主権 |
|---|---|---|
| REX_Wiki_Vault | `5d09e468-3a96-4906-af27-3400c50a0275` | Default Rex(大脳長期記憶) |
| REX_Vault_System | `daf281ae-e310-400f-961a-20db58b98e01` | Wiki-Eval 業務時のみ |
| REX_System_Brain | `da84715f-9719-40ef-87ec-2453a0dce67e` | Wiki-trade 業務時のみ |
| REX_Trade_Brain | `4abc25a0-4550-4667-ad51-754c5d1d1491` | Wiki-brain 業務時のみ |

---

## 関連リポジトリ

| プロジェクト | リポジトリ | 状態 |
|---|---|---|
| Trade_System | `Minato33440/Trade_System` | 稼働中 |
| Trade_Brain | `Minato33440/Trade_Brain` | 稼働中 |
| Setona_HP | `Minato33440/Setona_HP` | 稼働中 |

---

## 前身

本リポジトリは [Second_Brain_Lab](https://github.com/Minato33440/Second_Brain_Lab)(凍結)から移行。
Second_Brain_Lab はナレッジシステムの構築・テスト用リポジトリとして役割を終え、
本リポジトリが REX_AI 全体の脳として独立運用される。

---

## ライセンス

Private repository. All rights reserved.
