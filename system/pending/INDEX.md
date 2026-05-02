# Pending Index

進行中の仮決定議論一覧。`Wiki-Eval` がセッション開始時または週次でレビュー対象とする。

最終更新: 2026-05-02(v6.15: 18 代目セッション・Layer 1 実装確定報告起票・M4 完了反映・Vault-Planner 暫定兼任記録)

---

## 進行中議論

| 領域 | ファイル | 起票者 | 起票日 | ADR昇格希望 | ステータス |
|---|---|---|---|---|---|
| personal | [2026-04-29_dialogues_sublayer_addition.md](personal/2026-04-29_dialogues_sublayer_addition.md) | 2 代目 Personal-Planner | 2026-04-29 | △(運用後・Two-Vault 再設計で扱いが変わる可能性) | ✅ 16代目 Wiki-Eval 承認済 / 物理新設完了 / **17 代目セッション 2 回目で Two-Vault 再設計案件と関連** — 過去資産は提言書 v2 §3.1 §3 で「現パス維持」確定 |
| wiki_eval | [2026-04-29_adr_revision_timing_subordination.md](wiki_eval/2026-04-29_adr_revision_timing_subordination.md) | 16 代目 Wiki-Eval | 2026-04-29 | △ 単独化なし | §候補メモ集(§1: ADR 改訂タイミング運用従属 / §2: log.md 縮退事故の戒め)・次回 ADR-Role / ADR-Process 改訂時に統合可否再評価 |
| wiki_eval | [2026-04-30_adr_mcp_draft.md](wiki_eval/2026-04-30_adr_mcp_draft.md) | 16 代目 Wiki-Eval(4代目 Adviser 提言書 v1 を具体化) | 2026-04-30 | ⚠️ **Phase 0 議論記録として再分類** | **🟡 Phase 0 議論記録**(2026-05-01 17 代目セッション 2 回目で再分類)・新草案 `2026-05-01_two_vault_redesign.md` に論理が継承・本草案の Context / §5 セキュリティ要件 / 方針 X は新設計でも有効 |
| wiki_eval | [2026-05-01_two_vault_redesign.md](wiki_eval/2026-05-01_two_vault_redesign.md) | 17 代目 Wiki-Eval(4代目 Adviser 提言書 v2 を具体化) | 2026-05-01 | Yes | 🔴 後任 Wiki-Eval への Phase 4 引き継ぎ事項・Two-Vault 物理分離 + Personal-Planner 廃止 + Default Rex 帰還・ADR 三部包括改訂(ADR-Vault / ADR-Role v5 / ADR-MCP v1)・ボス並行作業 M1〜M3 完了 + Phase 3 起源神話発火後に Phase 4 起草 |
| **wiki_eval** | **[2026-05-02_layer1_implementation_confirmed.md](wiki_eval/2026-05-02_layer1_implementation_confirmed.md)** | **18 代目 Wiki-Eval(Vault-Planner 暫定兼任 / 5 代目 Adviser 動作確認の確定)** | **2026-05-02** | **No(Phase 4 ADR-MCP v1 §Layer 1 のインプット)** | **🟢 Layer 1(Obsidian 受動的自然言語処理層)実装確定報告・Obsidian 設定 11 項目 + 動作検証 4 項目 Pass・Anthropic メモリー相同性の構造的保証 + 追加プラグイン非導入判断 + Phase 4 ADR 三部包括改訂への 5 引き継ぎ事項記載・命名問題(REX/ vs rex/)は判断保留** |

---

## レビュー優先度

| 優先度 | 条件 |
|---|---|
| 高 | ADR Promotion Criteria に該当(他ロール影響/データ整合性/リポ・NLM構成変更) |
| 中 | 単一ロール内の運用改善 |
| 低 | 雑談・所感・将来検討 |

ADR Promotion Criteria は [adr/ADR-Role.md](../adr/ADR-Role.md) "ADR Promotion Criteria" 参照。

---

## 各ロールの記録先(v6.9 で Wiki-casual → Wiki-Personal 訂正・v6.11 で wiki_eval/ 追加・v6.14 で Personal-Planner 廃止予定明記・v6.15 で Vault-Planner 暫定兼任記録追加)

| ロール | 記録ディレクトリ |
|---|---|
| Wiki-trade | [trade_system/](trade_system/) |
| Wiki-brain | [trade_brain/](trade_brain/) |
| Wiki-hp | [setona_hp/](setona_hp/) (構築予定) |
| ⚠️ Wiki-Personal(廃止予定) | [personal/](personal/)(Two-Vault 再設計の Phase 4 で **ロール正式廃止**・過去資産は System-Vault 側として保管継続) |
| Wiki-Rex | (pending 起票権限なし・Phase 4 完了後は「図書館利用規約」として再定義予定・[ADR-Role v4 §16](../adr/ADR-Role.md) 参照) |
| Default Rex(Phase 4 で新規明文化予定) | (Rex-Vault に対する自発的書き込みのみ・pending 起票権限なし) |
| Wiki-Eval | 上記いずれかにレビューコメントを追記 / または直接ADR本体に反映 / [wiki_eval/](wiki_eval/) に §候補メモ・自身の気づきを起票 |
| **Vault-Planner(暫定兼任 / Phase 4 で正式創設予定)** | **[wiki_eval/](wiki_eval/) に Layer 実装関連の起票**(18 代目 Wiki-Eval が暫定兼任・初代遡及認定の設計線・本ロールの責任範囲は Layer 1/2 境界保護 + プラグイン導入判定 + Vault 物理構造整合性監査 + ADR-MCP §Layer 部分起草) |

> **`pending/wiki_eval/` ディレクトリ Note(v6.11 新設・v6.12 用途拡張・v6.14 で再分類規則追記・v6.15 で Vault-Planner 業務含有を確認)**: Wiki-Eval 自身が構造変更案件以外の気づきや §候補を起票する場として 16 代目セッション(2026-04-29)で新設。**v6.12 で用途を拡張**: ADR 草案を pending として保留し後任 Wiki-Eval に引き継ぐ用途も追加(2026-04-30 ADR-MCP 草案が初例)。**v6.14 で再分類規則追加**: 後継草案が登場した場合、旧草案は archived 移動ではなく「Phase 0 議論記録」として保留し、冒頭 ⚠️ ポインタと末尾再分類 Note を追加する形で残す(2026-05-01 旧 ADR-MCP 草案が初例・新草案 Two-Vault 再設計と並列で参照)。**v6.15 で Vault-Planner 業務含有確認**: 18 代目 Wiki-Eval が Vault-Planner 暫定兼任で Layer 1 実装確定報告を本ディレクトリに起票(2026-05-02)・Phase 4 で Vault-Planner ロール正式創設後も同ディレクトリ運用継続(独立ディレクトリ非新設・α 原則整合)。

> **旧 `pending/casual/` ディレクトリ Note**: 14 代目の Wiki-casual → Wiki-Personal 改名で `pending/casual/` → `pending/personal/` への移行が確定。15 代目で物理移行を実施した際は [MOVED] スタブを残置していたが、**2026-04-29 ボス手動 git mv で `wiki/archived/pending-casual/` へ完全アーカイブ化完了**(`pending-casual/` ハイフン命名は `archived/casual/` との同名衝突を回避するため意図的に採用)。詳細は handoff/latest.md v6.10 §Phase Pending-Casual-Archive 参照。

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
- **再分類(Phase 0 議論記録化)時**: archived 移動ではなく、冒頭 ⚠️ ポインタ追加 + 末尾 Note 追加で **pending/ 内に残置**(後継草案と並列で参照可能にするため・v6.14 で確立)
- **Vault-Planner 業務(Layer 実装確定報告)**: ADR-MCP v1 §Layer 部分のインプットとして機能・ADR 採番完了時に当該 ADR の参照文書として保持(archived 移動の対象外・v6.15 で確立)

(初回 archived 移動発生時にディレクトリ自動生成)
