# Rex 道具箱 — Grok OAuth Bridge 運用マニュアル

- 最終更新: 2026-05-22
- 対象: Default Rex / Claude オーケストレーター
- 設計の背景: `Grok_OAuth_Bridge_Architecture.md` を参照

---

## 0. これは何

Claude（Rex）から OAuth-Grok を呼ぶための **道具箱**。ここでは使い方に絞る。「なぜこの設計か」は設計ノート側に置いてある。

---

## 1. 前提（動作条件）

- Claude Desktop で `grok-oauth` MCP が running
- Hermes が OAuth 認証済み（`hermes model` で provider が `xai-oauth`）
- SuperGrok サブスクが有効（日次制限内）

---

## 2. ツール一覧

### `ask_grok(prompt)`
- 用途: 質問・壁打ち・Web/X 検索・画像理解
- 安全度: **高**（ファイル書込なし。toolsets = web / search / vision）
- 例:
  - `ask_grok("最近の金先物のセンチメントを X で調べて要約して")`
  - `ask_grok("この相場観、穴があれば指摘して: ...")`
  - `ask_grok("この画像が何を表しているか説明して")`

### `grok_work(prompt, workdir)`
- 用途: ファイル整理・コード作業・画像生成
- 制約: `workdir` は `C:\Python\REX_AI` 配下のみ。**`REX_Brain_Vault` は不可（拒否される）**。
- 例:
  - `grok_work("このフォルダの .md を一覧化して index.md を作って", "C:\\Python\\REX_AI\\Daily_Log")`
  - `grok_work("サムネ用の簡単な PNG を生成して", "C:\\Python\\REX_AI\\Grok_Vault\\docs\\test")`

---

## 3. ガードレール早見

| やりたいこと | `ask_grok` | `grok_work` |
|---|---|---|
| 質問・検索・画像理解 | ✅ | ✅ |
| ファイル書込 | ❌ | ✅（許可リポのみ） |
| Vault への書込 | ❌ | ❌（拒否） |
| REX_AI 外への書込 | ❌ | ❌（拒否） |
| 端末コマンド実行 | ❌ | ❌ |

---

## 4. トラブルシュート

| 症状 | 原因の当たり | 対処 |
|---|---|---|
| 呼び出しが無言でハング | OAuth 資格情報を見失い対話待ち / 日次制限 | `HERMES_HOME` 注入を確認 / 制限リセットを待つ |
| 「120秒でタイムアウト」 | headless で対話プロンプト | hermes 側の認証状態を確認 |
| 「stdout 空 / returncode=…」 | hermes がエラーを吐いている | 返ってきた `stderr` を読む |
| 「hermes が見つからない」 | PATH 解決失敗 | config の env に `HERMES_BIN`（絶対パス）を追加 |
| スクリプト変更が効かない | 旧プロセスが常駐 | Claude Desktop を **完全再起動**（タスクトレイからも終了） |

---

## 5. Hermes Skill カタログ（Grok 側の能力）

Hermes には現在 **78 スキルが enabled**（builtin 76 + local 2）。これらは Hermes エージェント（= Grok）側の能力で、`ask_grok` / `grok_work` で Grok を呼んだときに活きる。Rex の業務に効きそうな主なものを抜粋（全リストは `hermes skills list`）。

### 研究・情報収集（GM / マクロ向け）
| Skill | 用途 |
|---|---|
| `polymarket` | 予測市場データ（マクロ・イベントのセンチメント） |
| `arxiv` | 論文検索・要約 |
| `blogwatcher` | ブログ / サイトの監視 |
| `llm-wiki` | Wiki 的リサーチ |

X のリアルタイム検索は `ask_grok` で直接、または下記 `grok-xai-bridge` 経由。

### ノート・Vault
| Skill | 用途 |
|---|---|
| `obsidian` | Obsidian Vault 操作（※聖域への書込は bridge 側で拒否。読取 / 別 Vault 用） |

### 開発（リポ作業）
| Skill | 用途 |
|---|---|
| `codebase-inspection` | コードベース把握 |
| `github-pr-workflow` / `github-issues` / `github-repo-management` / `github-code-review` | GitHub 一連 |
| `systematic-debugging` / `test-driven-development` | デバッグ / TDD |
| `plan` / `writing-plans` / `spike` | 設計・計画 |

### ドキュメント・生産性
| Skill | 用途 |
|---|---|
| `notion` / `google-workspace` / `linear` / `airtable` | 各種 SaaS |
| `powerpoint` / `nano-pdf` / `ocr-and-documents` | 資料・PDF・OCR |
| `maps` | 地図 |

### 作図・ビジュアル
| Skill | 用途 |
|---|---|
| `architecture-diagram` / `excalidraw` | 図 |
| `claude-design` / `design-md` | デザイン |
| `pixel-art` / `p5js` / `manim-video` | クリエイティブ |

### ローカル（Minato 自作）
| Skill | カテゴリ | 状態 |
|---|---|---|
| `rex-ai-vault-global` | (なし) | enabled / local |
| `grok-xai-bridge` | xai | enabled / local（**要修正** — 実在しないツール名を参照。修正版を別途用意） |

### スキルの効かせ方（重要・正直な注記）
- スキルは **Hermes エージェント側** の能力。`hermes -z` ワンショットで **自動活性するかは未確定**（`-z` は tools / memory / rules を読むが、skills の自動ロードは仕様上明言されていない）。
- 確実に使うには **`-s <skill>` でプリロード** が要る。現状の `ask_grok` / `grok_work` は `-s` を渡していない。
- → **拡張案**: `grok_work` に `skills` 引数を足し、`hermes -z ... -s <skills>` を渡せるようにすると、特定スキルを明示的に効かせられる。必要になったら実装する。

---

## 6. 関連ファイル

- 設計ノート: `Hermes_Agent\docs\Grok_OAuth_Bridge_Architecture.md`
- 実装: `MCP_Servers\Grok-OAuth\grok_oauth_bridge.py`
- Hermes Skills: `C:\Users\Setona\AppData\Local\hermes\skills\`
