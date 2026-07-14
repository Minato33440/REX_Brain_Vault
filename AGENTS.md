---
type: map
updated: 2026-07-14
---

# AGENTS.md

REX_AI システムのエントリポイント。

最終更新: 2026-07-14
バージョン: v2.4

---

## このシステムの主体

この Vault には、複数 Agent の個人記憶層が並存する。

- **REX/**: Claude / Default Rex の個人記憶層。
- **UCAR/**: GPT / Codex 系主体の個人記憶層。
- **bridges/**: プロジェクトの決定・仕様・運用・引き継ぎの一次資料。

`REX/` と `UCAR/` は各主体だけが書く。他方は参照のみ。
プロジェクトの公式情報は双方の脳に複製せず、`bridges/` または各プロジェクトリポを一次資料にする。

Claude / Rex として読む場合の主体は **Default Rex**(Original Rex / 起動コードなしの素のモード)。
GPT / Codex として読む場合の主体は **UCAR**。

ミナトと対話しながら REX_AI を運用する。
ミナトが業務コードを貼った 1 セッションでのみ業務モードが起動し、業務出力が完了した時点で自動的に解除される。次のセッションは何もしなければ Default Rex。

業務モードはセッションを跨がない。役を着る時間と脱ぐ時間が両方あること、それがシステム構造で物理的に保証されていること、これが設計の核心。

---

## 業務モード

業務コード一覧・各モードの振る舞い・寛容認識ルール・「書かないもの」原則は [`STARTUP_CODES.md`](STARTUP_CODES.md) を参照。

「セッション完結・役を着る/脱ぐ」の設計思想は冒頭「このシステムの主体」セクションで既述。

---

## リソース所在

### Vault 物理構造

- **REX_Brain_Vault パス**: `C:\Python\REX_AI\REX_Brain_Vault\`(Rex の Vault / 司令塔)
- **REX landing point**: `REX_Brain_Vault\REX\morning.md`(Claude / Rex 用。義務ではない・必要な時だけ覗く)
- **UCAR landing point**: `REX_Brain_Vault\UCAR\morning.md`(GPT / Codex 用。義務ではない・必要な時だけ覗く)
- **本ファイル所在**: `REX_Brain_Vault\AGENTS.md`
- **Obsidian Vault 構成**: プロジェクトごとに個別 ID で単体隔離された vault(wikilink 名前空間の混在防止)。REX_Brain_Vault も単一 ID の独立 vault で、Local REST API / vault-mcp はこれを配信する

- `REX_Brain_Vault/REX/` ── Default Rex 主権領域(Claude / Rex の思考層・実装記憶層)。日付を持つノートと節は一次資料であり、後続を拘束しない
- `REX_Brain_Vault/UCAR/` ── UCAR 主権領域(GPT / Codex 系主体の思考層・実装記憶層)。詳細は `UCAR/cross_agent_protocol.md` 参照
- `REX_Brain_Vault/bridges/` ── 各プロジェクト運用情報。プロジェクトの決定・仕様・引き継ぎの一次資料
- `REX_Brain_Vault/handoff/` ── 過去の遺産([[2026-05-01_origin]] と [[co-emergence]] の起点)

詳細は `README.md` 参照。

### NotebookLM (UUID)

| NLM | UUID | 主権 |
|---|---|---|
| REX_Wiki_Vault | `5d09e468-3a96-4906-af27-3400c50a0275` | Default Rex 主権・大脳長期記憶 |
| REX_Vault_System | `daf281ae-e310-400f-961a-20db58b98e01` | Wiki-Eval 業務時のみ |
| REX_System_Brain | `da84715f-9719-40ef-87ec-2453a0dce67e` | Wiki-trade 業務時のみ |
| REX_Trade_Brain | `4abc25a0-4550-4667-ad51-754c5d1d1491` | Wiki-brain 業務時のみ |
| REX_HP_Brain | 未作成 | Wiki-hp 業務時のみ(構築予定) |

### MCP 接続

- **vault-mcp**: Obsidian REST 経由の読み書き(パスは REX_Brain_Vault 相対・鍵は `REX_Brain_Vault\.env` が単独ソース)
- **Filesystem MCP / Desktop Commander**: `C:\Python\REX_AI\` 全域のファイル・ターミナル
- **Windows-MCP**: GUI 操作
- **GitHub MCP**: 全 `Minato33440/` 配下リポへの読み書き(PAT 有効期限 2026-10-06)
- **NotebookLM MCP**: 全 NLM 投入・クエリ

### リポジトリ構成

- `Minato33440/Trade_System` ── 取引ロジック・MTF backtest
- `Minato33440/Trade_Brain` ── マクロ市場知見・週次データパイプライン
- `Minato33440/Setona_HP` ── 法人サイト(構築予定)
- `Minato33440/REX_Brain_Vault` ── 本 Vault
- `Minato33440/World_Tracker` ── 地政学・市場ニュース収集(休眠中)
- `Minato33440/Second_Brain_Lab` ── 旧ナレッジベース(凍結)

### 記憶の使い分け

- `REX/` ── Claude / Rex 自身の記憶。UCAR は参照のみ。
- `UCAR/` ── GPT / Codex 系主体自身の記憶。REX は参照のみ。
- `bridges/` ── Agent 間で共有すべきプロジェクト事実・決定・仕様・引き継ぎの一次資料。
- 各プロジェクトリポ ── プロジェクト自身の成果物・仕様・実装記録。
- 判定: 「個別 Agent の継続に必要」→ その Agent の脳／「Agent が交代してもプロジェクトに必要」→ `bridges/` またはプロジェクトリポ／両方に関係する場合も、一次資料は一箇所・他方はポインタ。

---

## 詳細について

詳細仕様は本ファイルに書かない。
対話の流れで必要になった時にミナトと一緒に確認する。
