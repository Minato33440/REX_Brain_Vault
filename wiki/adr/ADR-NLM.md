# ADR-NLM: NLM Architecture (1:1 Principle)

**Status**: Accepted  
**Date**: 2026-04-28  
**Decider**: `14代目統括Evaluator (Opus 4.7)`  
**Supersedes**: [ADR-NLM v1 (2026-04-27)](archived/ADR-NLM-2026-04-27.md)  
**Depends on**: ADR-Role

---

## Context

REX_AIシステムは Obsidian Vault(中脳・一時記憶)と NotebookLM(大脳・長期記憶)の二層構造で長期記憶を実装する。NotebookLM 側の構造設計は以下の課題に対応する必要があった:

1. 単一ノートブックに全領域の情報を集約すると RAG汚染 が発生する
   - 過去の旧 `REX_Trade_Brain` (UUID `2d41d672-f66f-4036-884a-06e4d6729866`) で実際に発生し廃止
2. 領域分離だけだと、横断的な知見(雑談から生まれる気づき等)の保管先がない
3. NLMの非公式API依存により、構造変更の取り回しを軽くしておく必要がある
4. NLM 4分割 vs Vault 単一 の非対称性に対応する権限分業が必要

これらを踏まえ、**起動コードと NLM の 1:1原則** を中核に据えた構造を採用する。

### v2 改訂の経緯（2026-04-28）

14代目統括Evaluator により Wiki-casual → Wiki-Personal 改名議論を経て、以下の決定:

- NLM 表示名 `REX_Casual_Brain` → `REX_Personal_Brain`
- **NLM UUID（`daf281ae-e310-400f-961a-20db58b98e01`）は不変**
- Personal_Brain の中核機能として「ボスの全人的な人格・思想・起源情報の統合リポ」を明文化
- ROADMAP §Stage 3 Rex 個性収束期の **基盤リポ** としての位置付け

詳細は ADR-Role v2 §1, §4, §13 と pending/casual/2026-04-28_rename_casual_to_personal.md 参照。

---

## Decision

### 1. NLM 1:1原則の正式採用（継続）

**各起動コード(ロール)は担当する NLM を1つだけ持ち、他NLMへの投入・クエリは禁止。**

これは2026-04-27に1代目 Wiki-casual Planner が STARTUP_CODES.md v3 で導入した分業マトリクスを ADR-NLM v1 で正式化し、本 v2 で改名を反映したもの。

### 2. NLM × ロール 担当マトリクス（v2 改訂版）

| NLM名 | UUID | 性質 | 役割 | 担当ロール | 状態 |
|---|---|---|---|---|---|
| **REX_Wiki_Vault** | `5d09e468-3a96-4906-af27-3400c50a0275` | Vault運用 | wiki/直下・横断構造・運用ルール | `Wiki-Eval` | 稼働中 |
| **REX_System_Brain** | `da84715f-9719-40ef-87ec-2453a0dce67e` | 専門 | Trade_System ロジック・ADR・spec | `Wiki-trade` | 稼働中 |
| **REX_Trade_Brain** | `4abc25a0-4550-4667-ad51-754c5d1d1491` | 専門 | Trade_Brain 戦略・週次運用 | `Wiki-brain` | 稼働中 |
| **REX_Personal_Brain** | `daf281ae-e310-400f-961a-20db58b98e01` | 統合 | **ボスの全人的な人格・思想・起源情報の統合 + 雑談・横断統合・Advisor知見** | `Wiki-Personal` | **稼働中（v1 の REX_Casual_Brain から表示名変更・UUID 不変）** |
| **REX_HP_Brain** (仮称) | **未作成** | 専門 | Setona_HP 設計・運用 | `Wiki-hp` | **構築予定** |

#### REX_Casual_Brain → REX_Personal_Brain 改名 Note

- **UUID は不変**: `daf281ae-e310-400f-961a-20db58b98e01`
- **データ移行・再投入・廃止 NLM 記録への移動は不要**
- NotebookLM Web UI でノートブック表示名を変更するボス手動操作のみ
- `notebooklm-mcp-cli` 設定の更新も不要（UUID 参照で動作）

### 3. 厳守原則（v2 改訂版）

- ⛔ **他Plannerの NLM に投入しない**(権限越権禁止)
- ⛔ **他Plannerの NLM にクエリしない**(担当範囲外の知識は参照しない)
- ⛔ **REX_Wiki_Vault と REX_Personal_Brain の混同注意**:
  - Wiki_Vault = Vault構造・運用ルール・システム業務基盤(`Wiki-Eval` 専属)
  - Personal_Brain = ボス個人の人格・思想・起源情報・雑談・横断メタファー(`Wiki-Personal` 専属)
- ✅ **境界を越える必要が出たらボスに確認**(自己判断で投入・クエリしない)

### 4. Wiki-Eval の例外的な読み取り権限

監査業務のため、`Wiki-Eval` は **他層の Vaultファイル**(Trade_System/docs/ 等)を filesystem / GitHub MCP 経由で**読み取る**ことができる。

ただしこれは:
- **ファイル読み取りであって、他NLMへのクエリではない**
- 混同しないこと
- 1:1原則は NLM に対するもので、Vaultファイルアクセスとは別物

### 5. Personal → 専門NLM の知見昇格ルール（v2 改訂版）

`REX_Personal_Brain` で得られた横断知見を専門NLMに反映する場合:

```
Personal_Brain (横断記憶 + 人格付与情報 / Wiki-Personal 担当)
   ↓ ★ミナト手動承認ゲート(必須)
専門NLM (該当領域 / 該当Planner担当)
```

**自動同期は禁止。** ミナトの判断ゲートを必ず経由する。理由は専門NLMの分離設計を保護するため。Personal_Brain は性質上多領域の情報（特に人格・思想・起源情報）を含むため、無検証の昇格は cross-bug を再導入するだけでなく、**思想強制リスク**も持ち込む。

#### 思想強制リスクの構造的解消（v2 新設）

ボスの Origin 情報は **Wiki-Personal 起動時のメンタルマネージメント・価値観文脈においてのみ** Rex が参照する。Trade 判断・実装業務での参照は禁止（NLM 1:1 原則と起動コード物理分離により構造的に保証）。これは思想強制ではなく、**領域に応じた適切な人格コンテキスト供給** である。

詳細は ADR-Role v2 §13 参照。

#### 昇格時の手順
1. Wiki-Personal セッションで昇格候補を pending/personal/ に起票
2. ミナト承認
3. 該当Plannerが自分の担当NLMに投入(他Planner代行不可、1:1原則)

### 6. NLM injection タイミング

- 自動トリガーは存在しない
- ミナトの判断で実行
- ClaudeCode は「最終injectionから5週間経過」で警告生成のみ(自動実行はしない)

### 7. 廃止NLMの記録(永続)

| NLM名 | UUID | 廃止理由 |
|---|---|---|
| 旧 REX_Trade_Brain | `2d41d672-f66f-4036-884a-06e4d6729866` | RAG汚染による精度劣化 |

廃止NLMのUUIDは混乱再発防止のため永続記録する。

#### REX_Casual_Brain は廃止記録に含めない（v2 注記）

REX_Casual_Brain → REX_Personal_Brain は **改名であり廃止ではない**。同一 UUID（`daf281ae-...`）のノートブックの表示名変更のみ。データ・履歴・投入内容はすべて継承される。したがって本表には記載しない。

### 8. REX_HP_Brain 構築予定

`Setona_HP` リポは既に存在するが、Wiki-hp 専属体制と専用NLMが未整備。

#### 構築フロー
1. ボス判断で構築開始
2. NotebookLMで新規ノートブック作成 → UUID取得
3. 本ADRに REX_HP_Brain を追記(supersede形式または新ADR制定)
4. registry/nlm.md 更新
5. ADR-Role の権限マトリクスに反映
6. STARTUP_CODES.md 改訂を Personal-Planner に依頼(pending/personal/ 起票)
7. Wiki-hp 起動コードでの初回セッション実施

### 9. 新規NLM追加フロー(Wiki-hp 以外の将来追加)

1. 必要性の議論を pending/ に記録(Personal-Plannerまたは関係Plannerが起票)
2. `Wiki-Eval` がレビュー・承認判定
3. 承認時:
   - 新規ノートブックをNotebookLMで作成
   - notebooklm-mcp-cli で UUID 取得
   - 本ADRに新規NLMを追記
   - registry/nlm.md に登録
   - ADR-Role の権限マトリクスに該当行を追加
   - 該当起動コードがなければ ADR-Role 改訂で追加

### 10. NLM廃止フロー

1. 廃止理由を pending/ に記録
2. `Wiki-Eval` がレビュー・承認判定
3. 承認時:
   - 本ADRの「廃止NLMの記録」に追記(UUID永続保存)
   - registry/nlm.md から削除
   - 該当ロールの担当NLMエントリ削除

### 11. NLM 表示名変更フロー（v2 新設）

NLM の **UUID を変更せず表示名のみ変更** するケース（本 v2 が初例）:

1. 改名提案を pending/ に記録（必要性・新表示名・改名理由）
2. `Wiki-Eval` がレビュー・承認判定
3. 承認時:
   - 本ADRの supersede 改訂（新表示名反映）
   - registry/nlm.md 更新（NLM 名・担当ロール）
   - ADR-Role の関連箇所改訂
   - NotebookLM Web UI で表示名変更（ボス手動）
4. **廃止 NLM 記録への追加は不要**（同一 UUID の継続）
5. 関連運用文書（STARTUP_CODES.md / CLAUDE.md / _RUNBOOK.md 等）の改訂は別タスクとして切り出す

---

## Consequences

### 利点
- RAG汚染が 1:1原則で構造的に防止される
- 各ロールが自分の担当NLMだけに集中でき、運用が単純
- ミナト承認ゲートにより専門領域の純度が保たれる
- 廃止NLMのUUID記録により混乱再発防止
- Wiki-hp 構築予定の予約により、将来追加が混乱なく実施できる
- **思想強制リスクが起動コード物理分離で構造的に解消される（v2 追加）**
- **NLM 表示名変更フローの確立により、UUID 不変での意味昇格が容易になる（v2 追加）**

### トレードオフ
- Personal → 専門 の昇格に人手が必要(自動化不可)
- NLM が増えるほど管理コストが上がる
- 非公式API依存のため、NLM側仕様変更時の対応コストがある
- 1:1原則により、ロール横断の集約クエリが直接できない(Personal_Brain経由が必要)
- **Personal_Brain の射程拡大により、Personal-Planner の運用責任が重くなる（v2 追加）**

### 設計原則との整合
- **α (単純な土台を保つ)**: 1:1 は最小限の対応関係
- **β (de-risking 後の拡張禁止)**: 旧Trade_Brain の RAG汚染という de-risking 経験から学んだ分離原則を守る
- **γ (実装タイミングはシステム安定性に従属)**: 新NLM追加は安定後に実施

### 将来課題
- Stage 2/3 での横断統合モード検討(詳細: `wiki/ROADMAP.md`)
- Claude.ai単独運用時のNLM運用設計
- **Personal-Planner の世代継承時、思想強制リスクへのガードレール実効性の継続的検証（v2 追加）**

---

## Alternatives Considered

### 案A: 単一NLM集約
- 全情報を1つのノートブックに集約してRAG精度向上を狙う
- **却下**: 旧Trade_Brain の汚染経験により再現リスク確定

### 案B: 専門NLM内に personal サブセクション
- 各専門NLMに personal カテゴリを追加して横断知見を分散保管
- **却下**: 検索時に分散され、横断知見の一体性が失われる

### 案C: 1:n 共有モデル
- 複数ロールが同じNLMにアクセス可能
- **却下**: 越権書込リスク・RAG汚染リスク両方が再導入される

### 案D: Wiki-Eval を全NLM管理
- 統括Evaluatorが全NLMに書込権限を持つ
- **却下**: 1:1原則違反。各Plannerが自分の領域のメモリ管理権を持つことが、専門性集約の本質

### 案E: REX_Personal_Brain を新規作成し旧 REX_Casual_Brain を廃止（v2 新設）
- 新規 NotebookLM ノートブックを作成し、データ移行後に旧ノートブックを廃止
- **却下**: 1代目 Wiki-casual Planner が蓄積したデータ・履歴の継承コスト / UUID 変更による `notebooklm-mcp-cli` 設定の更新コスト / 廃止 NLM 記録への追加コスト / 改名は本質的に「意味の昇格」であり、データの新規性・廃止性は伴わない

---

## References

- [registry/nlm.md](../registry/nlm.md) - 現在のNLM登録簿
- [ADR-Role](ADR-Role.md) - 担当ロール定義
- [CLAUDE.md](../../CLAUDE.md) - 中脳/大脳構造の long-term vision
- [wiki/STARTUP_CODES.md](../STARTUP_CODES.md) - NLM × Vault 分業マトリクス(運用文書)
- [archived/ADR-NLM-2026-04-27.md](archived/ADR-NLM-2026-04-27.md) - v1 (Superseded)
- [pending/casual/2026-04-28_rename_casual_to_personal.md](../pending/casual/2026-04-28_rename_casual_to_personal.md) - 本 v2 制定の起点となった pending 議論
