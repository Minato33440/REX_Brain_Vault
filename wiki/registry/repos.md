# Repository Registry

REX_AI システムが管理するGitHubリポジトリの登録簿(現在の状態)。

最終更新: 2026-04-27  
管轄: `Wiki-Eval`

> 本ファイルは「現在の登録状態」を記録する。決定の理由・経緯は [adr/ADR-Repo.md](../adr/ADR-Repo.md) を参照。

---

## アクティブリポ

| リポ名 | URL | 役割 | 主担当ロール | MCP接続 |
|---|---|---|---|---|
| Trade_System | https://github.com/Minato33440/Trade_System | コア実装・MTF backtest | `Wiki-trade` | GitHub MCP / Filesystem MCP(R) |
| Trade_Brain | https://github.com/Minato33440/Trade_Brain | マクロ市場知見・裁量overlay | `Wiki-brain` | GitHub MCP / Filesystem MCP(R) |
| Setona_HP | https://github.com/Minato33440/Setona_HP | 法人サイト | `Wiki-hp` (**構築予定**) | GitHub MCP |
| REX_Brain_Vault | https://github.com/Minato33440/REX_Brain_Vault | Obsidian Vault実体 | `Wiki-Eval`(adr/registry/CLAUDE.md) / 各ロール(担当pending) | GitHub MCP(W) / Filesystem MCP(R) |

---

## 廃止リポ

| リポ名 | 廃止日 | 経緯 |
|---|---|---|
| Second_Brain_Lab | 2026-04(目安) | MCP試験運用完了後に役目終了 |

---

## 不存在リポ(混乱防止のための記録)

| 誤認されたリポ名 | 状態 |
|---|---|
| `UCAR_DIALY` (旧アカウント) | 旧アカウント自体が削除済み |
| `Minato33440/UCAR_DIALY` | 過去に誤認されたが実在しない |

---

## 接続対象外リポ

| リポ名 | 状態 |
|---|---|
| `Minato33440/Daily_Log` | 存在するが REX_AI MCP 接続対象外 |

---

## 構築予定の体制

### Setona_HP - Wiki-hp 専属体制

`Setona_HP` リポは既に存在し稼働中だが、専属の `Wiki-hp` Planner+ClaudeCode 体制と専用NLM(REX_HP_Brain)が未整備。

#### 現状の準備措置
- `wiki/setona_hp/` 空フォルダ配置済み
- `pending/setona_hp/` 空フォルダ配置済み
- ADR-Role / ADR-Repo / ADR-NLM に予約項目記載済み

詳細フロー: [adr/ADR-Repo.md](../adr/ADR-Repo.md) "Setona_HP の専属ロール体制(構築予定)"

---

## 更新ルール

- **更新権限**: `Wiki-Eval` のみ
- **更新タイミング**:
  - リポ新規追加時(ADR-Repo に基づく承認後)
  - リポ廃止時(ADR-Repo に基づく承認後)
  - リポ役割変更時(ADR-Repo 改訂と同時)
- **更新方法**: GitHub MCP 経由のみ (ADR-Vault 遵守)
