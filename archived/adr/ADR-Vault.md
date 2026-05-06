# ADR-Vault: Vault Write Path Unification

**Status**: Accepted  
**Date**: 2026-04-27  
**Decider**: `13代目統括Evaluator (Opus 4.7)` 
**Depends on**: ADR-Vault

---

## Context

`REX_Brain_Vault` リポは Obsidian Vault の実体であり、複数のAIロールが書込を行う中心的なリソース。過去に以下の事故が発生した:

- ローカルPowerShellでの直接編集 と GitHub MCP commit が混在
- 同一ファイルに対する並行commit による diverge conflict
- どの commit が「正」か判別困難な状態

これを構造的に防ぐため、Vault に対する書込パスを単一化する原則を採用する。

---

## Decision

### 1. 二層アクセス制御の正式採用

| MCP | 操作 | 用途 |
|---|---|---|
| **Filesystem MCP** | **読み取り専用** | Vault内ファイルの参照・検索・監査 |
| **GitHub MCP** | **書き込み専用** | Vault内ファイルの作成・更新・削除 |

**Filesystem MCP は Vault に対して書き込みを行わない。** 書込操作はすべて GitHub MCP 経由で行い、commit履歴を残す。

### 2. 例外条件: Claude Desktop ローカル編集

人間(ミナト本人)が Claude Desktop / エディタ経由でローカル Vault を編集する場合の手順:

1. **必ず事前に `git pull origin main` を実行**
2. ローカル編集
3. `git add` → `git commit` → `git push origin main` で同期

この手順を逸脱すると diverge conflict が再発する。

### 3. AIロールの書込フロー(原則)

```
[AIロール] 書込指示受領
    ↓
[AIロール] GitHub MCP の create_or_update_file を使用
    ↓ SHA取得 → ファイル内容更新
[GitHub] commit記録
    ↓
[ローカル(必要時)] git pull origin main で同期
```

### 4. GitHub MCP 使用時の注意事項

過去の経験則として:

- **`create_or_update_file` は確実**。ファイル単位の sequential update を推奨
- **`push_files` (バルク push) は不安定**。複数ファイル更新時も基本は sequential
- **SHA取得は必須**。既存ファイル更新時は事前に SHA を取得してから put
- **日本語Unicodeを含む `oldText` の指定は注意**。文字列マッチが失敗するケースあり
- **大規模書き換えは `write_file` 相当(create_or_update_file)推奨**。`edit_file` は微修正向け

これらは過去のトラブルシューティングで確立された運用知見。

### 5. Filesystem MCP の現実装

Claude Desktop の `claude_desktop_config.json` で:

```json
"filesystem": {
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-filesystem",
    "C:\\Users\\Setona\\Desktop",
    "C:\\Users\\Setona\\Downloads",
    "C:\\Python\\REX_AI"
  ]
}
```

`C:\Python\REX_AI` 配下を読み取り対象とする。書込操作は **本ADR遵守のため自主的に行わない**(技術的にはMCP API上書込可能だが、運用上禁止)。

将来的に MCP server 側で read-only モードのオプションが提供されたら適用検討。

### 6. ロール別 Vault書込権限(再掲)

| ロール | Vault書込先 |
|---|---|
| `Wiki-Eval` | `wiki/adr/` / `wiki/registry/` / `CLAUDE.md` / 全 pending |
| `Wiki-trade` | `pending/trade_system/` (将来 `wiki/trade_system/` の専属領域も) |
| `Wiki-brain` | `pending/trade_brain/` (将来 `wiki/trade_brain/` の専属領域も) |
| `Wiki-hp` | `pending/setona_hp/` / `wiki/setona_hp/`(構築後) |
| `Wiki-casual` | `pending/casual/` / `casual/` |

### 7. 書込権限の二重ゲート

ロールベースの権限(ADR-Role)と本ADRの書込パス制約は **AND条件**:

- ロールが書込可能 **かつ** GitHub MCP経由 → OK
- ロールが書込可能 だが Filesystem MCP直書き → **禁止**
- ロールが書込不可能 → そもそも書込NG

---

## Consequences

### 利点
- diverge conflict が構造的に防がれる
- 全ての変更が GitHub commit 履歴に残る = 監査可能性
- AIロールが書込先を迷わない(GitHub MCP一択)
- Filesystem MCP の役割が明確化される(検索・参照・監査特化)

### トレードオフ
- GitHub MCP の rate limit が運用上の制約になる可能性
- ローカル編集時のオペレーションコスト(pull → 編集 → push)が固定
- bulk更新時の効率が低い(sequential commit)

### 運用上の注意
- AIロールは「便利だから」と Filesystem MCP の write系API を使ってはならない
- 本ADRは技術的制約ではなく **運用原則** であり、ロール側の自己拘束で守られる
- 違反検知のため、ファイル更新時の commit 履歴を定期確認する

---

## Alternatives Considered

### 案A: Filesystem MCP に書込権限も与える
- **却下**: diverge conflict 再発リスク、変更履歴喪失

### 案B: Vault全体を Read-only / 書込専用ブランチを別途用意
- **却下**: 単一AIインスタンス運用には過剰、PR管理コスト高

### 案C: ロックファイルによる排他制御
- **却下**: AIインスタンス間の状態共有手段が現状なく、実装困難

---

## References

- [ADR-Repo](ADR-Repo.md) - REX_Brain_Vault リポの位置付け
- [ADR-Role](ADR-Role.md) - 各ロールの書込権限
- 旧 Second_Brain_Lab リポ MCP-DESIGN-CONFIRMED.md - MCP試験運用記録(廃止リポ・参照のみ)
