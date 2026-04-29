# Pending Index

進行中の仮決定議論一覧。`Wiki-Eval` がセッション開始時または週次でレビュー対象とする。

最終更新: 2026-04-29（v6.9: Wiki-casual → Wiki-Personal 訂正・casual/ → archived/casual/ 反映）

---

## 進行中議論

| 領域 | ファイル | 起票者 | 起票日 | ADR昇格希望 | ステータス |
|---|---|---|---|---|---|
| (現時点なし) | - | - | - | - | - |

---

## レビュー優先度

| 優先度 | 条件 |
|---|---|
| 高 | ADR Promotion Criteria に該当(他ロール影響/データ整合性/リポ・NLM構成変更) |
| 中 | 単一ロール内の運用改善 |
| 低 | 雑談・所感・将来検討 |

ADR Promotion Criteria は [adr/ADR-Role.md](../adr/ADR-Role.md) "ADR Promotion Criteria" 参照。

---

## 各ロールの記録先（v6.9 で Wiki-casual → Wiki-Personal 訂正）

| ロール | 記録ディレクトリ |
|---|---|
| Wiki-trade | [trade_system/](trade_system/) |
| Wiki-brain | [trade_brain/](trade_brain/) |
| Wiki-hp | [setona_hp/](setona_hp/) (構築予定) |
| Wiki-Personal | [personal/](personal/)（Advisor 役割もここ・旧 `pending/casual/` から改名） |
| Wiki-Rex | （pending 起票権限なし・[ADR-Role v4 §16](../adr/ADR-Role.md) 参照） |
| Wiki-Eval | 上記いずれかにレビューコメントを追記 / または直接ADR本体に反映 |

> **旧 `pending/casual/` ディレクトリ Note**: 14 代目の Wiki-casual → Wiki-Personal 改名で `pending/casual/` → `pending/personal/` への移行が確定。15 代目で物理移行を実施した際は [MOVED] スタブを残置していたが、**2026-04-29 ボス手動 git mv で `wiki/archived/pending-casual/` へ完全アーカイブ化完了**（`pending-casual/` ハイフン命名は `archived/casual/` との同名衝突を回避するため意図的に採用）。詳細は handoff/latest.md v6.10 §Phase Pending-Casual-Archive 参照。

---

## ファイル命名規則

```
pending/<role-dir>/YYYY-MM-DD_<topic>.md
```

例: `pending/trade_system/2026-04-30_volume_alert_phase_d.md`

---

## ファイルフォーマット

```markdown
# <Topic Title>

**起票者**: <Role>
**起票日**: YYYY-MM-DD
**ADR昇格希望**: Yes / No / 未定
**影響範囲**: <他ロール・他リポへの波及>

## 仮決定内容
...

## 根拠・背景
...

## 検討中の論点
...

## レビュー履歴
- YYYY-MM-DD <Reviewer>: <コメント>
```

---

## archived/

ADR昇格・却下が決定したpendingエントリは archived/ に移動。
- 昇格時: 元ファイル名に `[ARCHIVED → ADR-XXX]` flag を追記してmove
- 却下時: 元ファイル名に `[REJECTED]` flag を追記してmove

(初回 archived 移動発生時にディレクトリ自動生成)
