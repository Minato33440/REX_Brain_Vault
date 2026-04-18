# MCP-DESIGN-CONFIRMED
**Second_Brain_Lab / MCPテスト試験運用 進捗記録簿**
最終更新：2026-04-15

---

## プロジェクト概要

| 項目 | 内容 |
|---|---|
| 目的 | MCP連携の試験運用による実用性評価 |
| 運用方針 | 本番プロジェクトと完全分離・試験専用 |
| 対象環境 | Claude Desktop × Windows |
| リポジトリ | https://github.com/Minato33440/Second_Brain_Lab.git |
| ブランチ | main |
| 実装戦略 | NotebookLM MCP → Obsidian MCP → 両者連携 の段階的検証 |

---

## テストケース管理

| # | 対象 | ステータス | 完了日 |
|---|---|---|---|
| #001 | NotebookLM MCP | ✅ 評価完了 | 2026-04-15 |
| #002 | Obsidian MCP → filesystem MCP で代替 | ✅ REX_Brain_Vault構築完了 | 2026-04-15 |
| #003 | GitHub MCP | ✅ 動作確認完了 | 2026-04-15 |
| #004 | 全MCP連携ワークフロー統合テスト | 🔲 未着手 | - |

---

## #001 NotebookLM MCP

### セットアップ記録

**環境**
- OS：Windows（PC名：Setona）
- Claude Desktop：v1.1617.0 (8d6345)
- uv：0.11.6

**インストール手順**

```powershell
# 1. uv インストール
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2. notebooklm-mcp-cli インストール（fakeredisバージョン固定が必須）
uv tool install notebooklm-mcp-cli --force --with "fakeredis==2.20.0"

# 3. Google認証
nlm config set auth.browser chrome
nlm login

# 4. MCP設定JSON生成
nlm setup add json
# → uvx / New config file を選択
```

**claude_desktop_config.json 設定**

```json
"notebooklm-mcp": {
  "command": "C:\\Users\\Setona\\.local\\bin\\uvx.exe",
  "args": [
    "--from",
    "notebooklm-mcp-cli",
    "notebooklm-mcp"
  ]
}
```

> ⚠️ `command` はフルパス指定が必須（`uvx` のみでは Claude Desktop から認識されない）

---

### トラブルシューティング記録

#### 問題①：ハンマーアイコンが表示されない
- **原因**：MCPサーバーが起動試行すらされていなかった
- **解決**：`command` を `uvx` → フルパス `C:\Users\Setona\.local\bin\uvx.exe` に変更

#### 問題②：Server disconnected（fakeredis ImportError）
```
ImportError: cannot import name 'FakeConnection' from 'fakeredis.aioredis'
```
- **原因**：fakeredis 2.26.0以降で `FakeConnection` が削除された
- **解決**：`fakeredis==2.20.0` に固定してインストール

```powershell
uv tool install notebooklm-mcp-cli --force --with "fakeredis==2.20.0"
```

> ⚠️ `uv tool upgrade notebooklm-mcp-cli` は使わない。fakeredis固定が解除される。  
> ⚠️ `nlm login` は認証のみ。パッケージは更新されない（通知が出るだけ）。  
> ✅ アップデート時は必ず `--force --with "fakeredis==2.20.0"` を付ける。

#### 問題③：アンチウィルスソフトの干渉
- 導入済みのアンチウィルスソフトが反応・削除
- 対象ソフトをアンインストール後、PC再起動で解消

#### 問題④：認証切れ（Cookie期限切れ）
- **症状**：`Authentication expired` エラー
- **解決**：`nlm login` で再認証（約2〜4週間ごとに発生）
- **注意**：`nlm login` はパッケージを更新しない。認証のみ。

#### 問題⑤：設定変更後にMCPが反映されない
- **原因**：Claude Desktop再起動だけでは不足な場合がある
- **解決**：**PCごと再起動**が確実

---

### 最終確認ステータス（2026-04-10）

| 確認項目 | 結果 |
|---|---|
| Claude Desktop Developer設定 | ✅ running |
| コネクタメニュー表示 | ✅ notebooklm-mcp 有効 |
| Google認証アカウント | tomtomaipro@gmail.com |
| Cookies | 48件抽出 |

---

### RAG評価結果（2026-04-15）

**ノートブック**: REX_Trade_Brain  
**ID**: 2d41d672-f66f-4036-884a-06e4d6729866  
**投入ソース**: EX_DESIGN_CONFIRMED-2026-3-31 / HP-DESIGN-CONFIRMED_6

| クエリ | 内容 | 判定 |
|---|---|---|
| ① | 最優先タスク確認（両プロジェクト横断） | ✅ 合格 |
| ② | 固定ネック原則の設計意図（sh_vals.iloc[0]） | ✅ 合格 |
| ③ | ClaudeCode引き継ぎプロンプト自動生成 | ✅ 合格（最重要） |

**総合判定**: ✅ 補助用途として本番導入可

---

### 運用パターン（確定）

| パターン | 内容 |
|---|---|
| スレ引き継ぎ自動化 | 「#026の引き継ぎプロンプトを生成して」→ NotebookLMが即座に生成 |
| 意思決定ログの永続化 | セッション終了時にnote機能で記録 → 次スレでクエリ可能 |
| ソース定期更新 | 指示書#完了時にNotebookLMのソースを差し替え |

---

## #002 Obsidian MCP → filesystem MCP で代替（2026-04-15）

### 設計判断

`mcp-obsidian` npmパッケージは存在しないため、filesystem MCPで代替。  
Obsidianのvaultはmarkdownファイル群なのでfilesystem MCPで機能的に同等。

### REX_Brain_Vault 構築完了

**パス**: `C:\Python\REX_AI\REX_Brain_Vault\`

```
REX_Brain_Vault/
├── CLAUDE.md                    ✅ 運用指示書
├── raw/
│   ├── EX_DESIGN_CONFIRMED-2026-3-31.md   ✅
│   ├── HP-DESIGN-CONFIRMED_6.md           ✅
│   └── スレ引き継ぎ指示書_vol9.md          ✅（過去資産）
└── wiki/
    ├── index.md                 ✅
    ├── log.md                   ✅
    ├── entities/                ✅（4ページ生成済み）
    ├── decisions/               ✅（2ページ生成済み）
    └── handoff/
        └── latest.md            ✅（#003引き継ぎプロンプト入り）
```

---

## #003 GitHub MCP（2026-04-15 完了）

### セットアップ

```json
"github": {
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-github"
  ],
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "（.envで管理）"
  }
}
```

### PAT 設定（Fine-grained）

| 項目 | 設定値 |
|---|---|
| Token name | Claude-MCP |
| Expiration | 90日（2026-07-14） |
| Repository access | Only select repositories（3リポジトリ）|
| Contents | Read and write |
| Metadata | Read-only（自動）|

**対象リポジトリ**:
- Minato33440/Second_Brain_Lab
- Minato33440/Setona_HP
- Minato33440/Trade_System

### トラブルシューティング

| 症状 | 原因 | 解決策 |
|---|---|---|
| Tool execution failed | リポジトリが未選択 | PAT設定でリポジトリを選択 |
| Tool execution failed | Contents権限が未設定 | Add permissions → Contents: Read and write |
| Tool execution failed | PATが無効化済み | 新しいPATを発行してconfigを書き換え |
| チャットにトークン漏洩 | 誤ってスクリーンショット共有 | 即座にRevoke → 再発行 |

> ⚠️ **PATは絶対にチャットに貼らない・スクリーンショットも送らない**

### 動作確認

list_commits（Second_Brain_Lab/main）: ✅ 成功  
このチャットから直接プッシュ可能な状態

---

## 設計方針メモ（意思決定ログ）

| 日付 | 決定事項 | 理由 |
|---|---|---|
| 2026-04-10 | 本番プロジェクトと分離した試験専用リポジトリを作成 | 本番作業フローへの影響ゼロを担保するため |
| 2026-04-10 | fakeredis==2.20.0 に固定 | 2.26.0以降でFakeConnection削除による起動失敗のため |
| 2026-04-10 | uvx はフルパス指定 | Claude DesktopのPATH認識問題を回避するため |
| 2026-04-10 | テスト順序を NotebookLM → Obsidian → 連携 に決定 | クラウド外部記憶を先に安定させてからローカル記憶を構築する段階的アプローチ |
| 2026-04-15 | NotebookLM MCP 本番補助用途として導入可と判定 | RAGクエリ3/3合格・引き継ぎプロンプト自動生成の実用性確認 |
| 2026-04-15 | Obsidian MCPはfilesystem MCPで代替 | mcp-obsidianパッケージ不在・filesystem MCPで機能同等 |
| 2026-04-15 | Vault配置を C:\Python\REX_AI\ に統一 | MCPシステム集約方針・既存Vaultはグローバルとして分離 |
| 2026-04-15 | GitHub MCP Fine-grainedトークン使用 | Classic tokenより安全・最小権限の原則 |
| 2026-04-15 | PATの有効期限は90日 | セキュリティと管理負荷のバランス |
| 2026-04-15 | ブランチはmain（masterではない） | リポジトリ初期化時の設定確認 |
| 2026-04-15 | `nlm login` は認証のみ・パッケージ更新なし | 通知が出るだけで自動更新はされない |
| 2026-04-15 | アップデート時は --force --with "fakeredis==2.20.0" を必ず付ける | uv tool upgrade ではfakeredis固定が解除されるリスクあり |
| 2026-04-15 | Trade System作業はPlanner+Evaluator+ClaudeCodeで独立 | REX_Brain_Systemへの自律システム導入は#026完了後に判断 |

---

## 現在のMCP構成（2026-04-15確定）

```json
{
  "mcpServers": {
    "filesystem": { "paths": ["Desktop", "Downloads", "C:\\Python\\REX_AI"] },
    "notebooklm-mcp": { "status": "✅ running" },
    "github": { "status": "✅ running" },
    "unityMCP": { "status": "✅ running" }
  }
}
```

## 次のSTEP

- [ ] #004 全MCP連携ワークフロー統合テスト（/wrap-upフローの実運用確立）
- [ ] REX_Brain_Vault Ingest継続（EX_DESIGN更新時にソース差し替え運用）
- [ ] PAT有効期限管理（2026-07-14・7日前にGitHubからメール通知）
