# ADR Index

統括Evaluator(`Wiki-Eval`)管轄のArchitecture Decision Record一覧。

最終更新: 2026-04-28

---

## 確定ADR一覧

| ADR | タイトル | ステータス | 制定日 | バージョン | 関連registry |
|---|---|---|---|---|---|
| [ADR-Role](ADR-Role.md) | Roles and Permissions | Accepted | 2026-04-28 | v2 | [registry/roles.md](../registry/roles.md) |
| [ADR-Repo](ADR-Repo.md) | Repository Architecture | Accepted | 2026-04-27 | v1 | [registry/repos.md](../registry/repos.md) |
| [ADR-Vault](ADR-Vault.md) | Vault Write Path Unification | Accepted | 2026-04-27 | v1 | - |
| [ADR-NLM](ADR-NLM.md) | NLM Architecture (1:1 Principle) | Accepted | 2026-04-28 | v2 | [registry/nlm.md](../registry/nlm.md) |

> **ADR 本体は常に最新版を指す固定パス**（日付・バージョンをファイル名に含めない）。詳細は ADR-Role v2 §10 参照。

---

## Supersede 履歴

| 旧 ADR | 新 ADR | Supersede 日 | 主な変更 |
|---|---|---|---|
| [ADR-Role v1](archived/ADR-Role-2026-04-27.md) | [ADR-Role v2](ADR-Role.md) | 2026-04-28 | Wiki-casual → Wiki-Personal 改名・射程拡大・ADR本体の固定パス原則新設・思想強制リスク構造的解消 |
| [ADR-NLM v1](archived/ADR-NLM-2026-04-27.md) | [ADR-NLM v2](ADR-NLM.md) | 2026-04-28 | REX_Casual_Brain → REX_Personal_Brain 表示名変更（UUID不変）・改名フロー新設 |

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
- 新ADRを作成して旧ADRに `[SUPERSEDED by ADR-XXX vN (Date)]` flag を付与
- 旧ADRを `archived/` ディレクトリに `<ADR名>-<制定日>.md` の形で移動
- INDEX.md に supersede 関係を記録
- **本体ファイル名は常に固定**（`ADR-Role.md` / `ADR-NLM.md` 等・日付やバージョンを含めない）
- 詳細は ADR-Role v2 §10「ADR本体の固定パス原則」参照

### 廃止
- 廃止された決定は `archived/` に移動
- INDEX.md の「廃止ADR」セクションに記録

---

## 廃止ADR

(現時点なし)

---

## archived/

廃止・置換されたADRは archived/ ディレクトリに保管。履歴追跡のため物理削除はしない。

### 現在 archived/ 内のファイル

| ファイル | 役割 |
|---|---|
| [ADR-Role-2026-04-27.md](archived/ADR-Role-2026-04-27.md) | ADR-Role v1（13代目制定・14代目 v2 で supersede）|
| [ADR-NLM-2026-04-27.md](archived/ADR-NLM-2026-04-27.md) | ADR-NLM v1（13代目制定・14代目 v2 で supersede）|
