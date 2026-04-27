# ADR Index

統括Evaluator(`Wiki-Eval`)管轄のArchitecture Decision Record一覧。

最終更新: 2026-04-27

---

## 確定ADR一覧

| ADR | タイトル | ステータス | 制定日 | 関連registry |
|---|---|---|---|---|
| [ADR-Role](ADR-Role.md) | Roles and Permissions | Accepted | 2026-04-27 | [registry/roles.md](../registry/roles.md) |
| [ADR-Repo](ADR-Repo.md) | Repository Architecture | Accepted | 2026-04-27 | [registry/repos.md](../registry/repos.md) |
| [ADR-Vault](ADR-Vault.md) | Vault Write Path Unification | Accepted | 2026-04-27 | - |
| [ADR-NLM](ADR-NLM.md) | NLM Architecture (1:1 Principle) | Accepted | 2026-04-27 | [registry/nlm.md](../registry/nlm.md) |

---

## 依存関係

```
ADR-Role (基盤: 全ADRの権限定義 + 1:1 NLM原則)
  ├── ADR-Repo (物理リポ構成)
  │     └── ADR-Vault (Vaultリポへの書込原則)
  └── ADR-NLM (NLM構造 + 担当ロール 1:1)
```

セッション開始時の読込推奨順: ADR-Role → ADR-Repo → ADR-Vault → ADR-NLM

---

## ADR運用ルール

### 制定
- 制定権限: `Wiki-Eval` のみ
- pending/ から昇格してADR化
- 昇格基準は ADR-Role の "ADR Promotion Criteria" 参照

### 改訂
- 既存ADRの内容変更 = supersede
- 新ADRを作成して旧ADRに `[SUPERSEDED by ADR-XXX]` flag を付与
- 旧ADRを `archived/` ディレクトリに移動
- INDEX.md にsupersede関係を記録

### 廃止
- 廃止された決定は `archived/` に移動
- INDEX.md の「廃止ADR」セクションに記録

---

## 廃止ADR

(現時点なし)

---

## archived/

廃止・置換されたADRは archived/ ディレクトリに保管。履歴追跡のため物理削除はしない。  
(初回 archived 移動発生時にディレクトリ自動生成)
