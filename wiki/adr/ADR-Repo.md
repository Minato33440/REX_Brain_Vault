# ADR-Repo: Repository Architecture

**Status**: Accepted  
**Date**: 2026-04-27  
**Decider**: `Wiki-Eval`  
**Depends on**: ADR-Role

---

## Context

REX_AIシステムは複数のGitHubリポジトリで構成され、過去にリポ追加・分離・廃止を繰り返してきた。リポ構成の変遷と現状認識のズレが引き継ぎ時の混乱要因となっていた。

主な経緯:
- `UCAR_DIALY` (旧アカウント): 削除済み・存在しない
- `Minato33440/UCAR_DIALY`: 過去に誤認されたが実在しない
- `Trade_Brain`: 2026年4月に Trade_System から分離
- `Second_Brain_Lab`: MCP試験運用後に廃止凍結
- `REX_Brain_Vault`: Obsidian Vault実体として運用中
- `Setona_HP`: 既存・専属ロール体制未整備

これらを ADR で正式に記録し、登録状態は registry/repos.md で動的管理する二層体制にする。

---

## Decision

### 1. アクティブリポ4本構成

| リポ | 役割 | 主担当ロール | MCP接続 |
|---|---|---|---|
| `Minato33440/Trade_System` | コア実装・MTF backtest | `Wiki-trade` | GitHub MCP / Filesystem MCP(R) |
| `Minato33440/Trade_Brain` | マクロ市場知見・裁量overlay | `Wiki-brain` | GitHub MCP / Filesystem MCP(R) |
| `Minato33440/Setona_HP` | 法人サイト | `Wiki-hp` (**構築予定**) | GitHub MCP |
| `Minato33440/REX_Brain_Vault` | Obsidian Vault実体 | `Wiki-Eval` (adr/registry) / 各ロール (担当pending) | GitHub MCP(W) / Filesystem MCP(R) |

詳細は [registry/repos.md](../registry/repos.md) で動的管理。

### 2. Setona_HP の専属ロール体制(構築予定)

`Setona_HP` リポは既に存在し稼働中だが、専属の `Wiki-hp` Planner+ClaudeCode 体制と専用NLM(REX_HP_Brain)が未整備。

#### 現状の準備措置
- `wiki/setona_hp/` 空フォルダ配置(将来の専用Vaultスペース)
- `pending/setona_hp/` 空フォルダ配置(仮決定記録先)
- registry/repos.md に主担当 **(構築予定)** 表記
- ADR-NLM に REX_HP_Brain 構築予定を記載

#### 構築開始時のフロー
1. ボス判断で構築開始
2. REX_HP_Brain NLM をNotebookLMで作成 → UUID取得
3. ADR-NLM 改訂(supersede形式または新ADR制定)
4. registry/nlm.md 更新
5. STARTUP_CODES.md 改訂(Wiki-casual Planner に改訂依頼を pending/casual/ で起票)
6. Wiki-hp 起動コードでの初回セッションを実施

### 3. 廃止リポの記録

| リポ | 状態 | 経緯 |
|---|---|---|
| `Minato33440/Second_Brain_Lab` | 廃止凍結 | MCP試験運用完了後に役目終了 |
| `UCAR_DIALY` (旧アカウント) | 削除済み | 旧アカウント自体が削除 |
| `Minato33440/UCAR_DIALY` | 不存在 | 過去の誤認・実在せず |
| `Minato33440/Daily_Log` | 存在するがMCP接続対象外 | 別用途で運用 |

### 4. 全リポの所属

すべてのアクティブリポは `Minato33440/` 配下に所属。他のorganization・personal account 配下のリポは REX_AI システムの対象外。

### 5. リポ別のロール書込権限

| リポ | 書込可能ロール |
|---|---|
| Trade_System | `Wiki-Eval` / `Wiki-trade` |
| Trade_Brain | `Wiki-Eval` / `Wiki-brain` |
| Setona_HP | `Wiki-Eval` / `Wiki-hp` (構築後) |
| REX_Brain_Vault | `Wiki-Eval`(adr/registry/CLAUDE.md) / 各Planner(pending/<repo>/) / `Wiki-casual`(pending/casual + casual/) |

REX_Brain_Vaultへの書込原則は ADR-Vault で別途定義。

### 6. 新規リポ追加フロー

1. 該当Plannerまたは関係者が pending/ に提案を記録
2. `Wiki-Eval` がレビュー・承認判定
3. 承認時:
   - 本ADRに新規リポを追記(supersede形式または新ADR制定)
   - registry/repos.md に登録
   - ADR-Role の権限マトリクスに該当行を追加
   - 必要に応じて新規起動コード・専用NLMの構築フロー起動
4. pending エントリを archived/ に移動

### 7. リポ廃止フロー

1. 該当Plannerが pending/ に廃止提案
2. `Wiki-Eval` がレビュー・承認判定
3. 承認時:
   - 本ADRの「廃止リポの記録」に追記
   - registry/repos.md から削除(履歴は archived/ に保持)
   - 該当ロールの権限マトリクスから関連エントリ削除
   - 該当NLMがあれば ADR-NLM 改訂で廃止記録

---

## Consequences

### 利点
- リポ構成の変遷が ADR + registry の二層で追跡可能
- 引き継ぎ時に「現存リポ」「廃止リポ」「不存在リポ」が一目で分かる
- 新規追加・廃止のフローが明文化されている
- Wiki-hp の構築予定が予約として記録され、将来の追加が混乱なく実施できる

### トレードオフ
- リポ追加時にADRと registry の両方を更新する必要がある(整合性管理コスト)
- 廃止リポの履歴保持が registry の肥大化を招く可能性

---

## Alternatives Considered

### 案A: registryのみで管理
- **却下**: リポ追加・廃止の理由が記録されず、後の判断根拠が失われる

### 案B: 各リポにADRを1本ずつ作成
- **却下**: 現段階4リポでは過剰分割。10リポ超えたら再検討

### 案C: Wiki-hp を構築完了まで本ADRに記載しない
- **却下**: 既に Setona_HP リポが稼働中で、現状記載しないと「触れていない領域」として認識される。予約記録が安全

---

## References

- [registry/repos.md](../registry/repos.md) - 現在のリポ登録簿
- [ADR-Vault](ADR-Vault.md) - REX_Brain_Vault 書込原則
- [ADR-Role](ADR-Role.md) - 権限マトリクス基盤
- [ADR-NLM](ADR-NLM.md) - REX_HP_Brain 構築予定
