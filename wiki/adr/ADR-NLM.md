# ADR-NLM: NLM Architecture (1:1 Principle)

**Status**: Accepted  
**Date**: 2026-04-27  
**Decider**: `13代目統括Evaluator (Opus 4.7)`  
**Depends on**: ADR-NLM

---

## Context

REX_AIシステムは Obsidian Vault(中脳・一時記憶)と NotebookLM(大脳・長期記憶)の二層構造で長期記憶を実装する。NotebookLM 側の構造設計は以下の課題に対応する必要があった:

1. 単一ノートブックに全領域の情報を集約すると RAG汚染 が発生する
   - 過去の旧 `REX_Trade_Brain` (UUID `2d41d672-f66f-4036-884a-06e4d6729866`) で実際に発生し廃止
2. 領域分離だけだと、横断的な知見(雑談から生まれる気づき等)の保管先がない
3. NLMの非公式API依存により、構造変更の取り回しを軽くしておく必要がある
4. NLM 4分割 vs Vault 単一 の非対称性に対応する権限分業が必要

これらを踏まえ、**起動コードと NLM の 1:1原則** を中核に据えた構造を採用する。

---

## Decision

### 1. NLM 1:1原則の正式採用

**各起動コード(ロール)は担当する NLM を1つだけ持ち、他NLMへの投入・クエリは禁止。**

これは2026-04-27に1代目 Wiki-casual Planner が STARTUP_CODES.md v3 で導入した分業マトリクスを ADR で正式化したもの。

### 2. NLM × ロール 担当マトリクス

| NLM名 | UUID | 性質 | 役割 | 担当ロール | 状態 |
|---|---|---|---|---|---|
| **REX_Wiki_Vault** | `5d09e468-3a96-4906-af27-3400c50a0275` | Vault運用 | wiki/直下・横断構造・運用ルール | `Wiki-Eval` | 稼働中 |
| **REX_System_Brain** | `da84715f-9719-40ef-87ec-2453a0dce67e` | 専門 | Trade_System ロジック・ADR・spec | `Wiki-trade` | 稼働中 |
| **REX_Trade_Brain** | `4abc25a0-4550-4667-ad51-754c5d1d1491` | 専門 | Trade_Brain 戦略・週次運用 | `Wiki-brain` | 稼働中 |
| **REX_Casual_Brain** | `daf281ae-e310-400f-961a-20db58b98e01` | 統合 | 雑談・横断統合・Advisor知見 | `Wiki-casual` | 稼働中 |
| **REX_HP_Brain** (仮称) | **未作成** | 専門 | Setona_HP 設計・運用 | `Wiki-hp` | **構築予定** |

### 3. 厳守原則

- ⛔ **他Plannerの NLM に投入しない**(権限越権禁止)
- ⛔ **他Plannerの NLM にクエリしない**(担当範囲外の知識は参照しない)
- ⛔ **REX_Wiki_Vault と REX_Casual_Brain の混同注意**:
  - Wiki_Vault = Vault構造・運用ルール・システム業務基盤(`Wiki-Eval` 専属)
  - Casual_Brain = ミナト個人の雑談・趣味・哲学・横断メタファー(`Wiki-casual` 専属)
- ✅ **境界を越える必要が出たらボスに確認**(自己判断で投入・クエリしない)

### 4. Wiki-Eval の例外的な読み取り権限

監査業務のため、`Wiki-Eval` は **他層の Vaultファイル**(Trade_System/docs/ 等)を filesystem / GitHub MCP 経由で**読み取る**ことができる。

ただしこれは:
- **ファイル読み取りであって、他NLMへのクエリではない**
- 混同しないこと
- 1:1原則は NLM に対するもので、Vaultファイルアクセスとは別物

### 5. Casual → 専門NLM の知見昇格ルール

`REX_Casual_Brain` で得られた横断知見を専門NLMに反映する場合:

```
Casual_Brain (横断記憶 / Wiki-casual 担当)
   ↓ ★ミナト手動承認ゲート(必須)
専門NLM (該当領域 / 該当Planner担当)
```

**自動同期は禁止。** ミナトの判断ゲートを必ず経由する。理由は専門NLMの分離設計を保護するため。Casual_Brain は性質上多領域の情報を含むため、無検証の昇格は cross-bug を再導入する。

昇格時の手順:
1. Wiki-casual セッションで昇格候補を pending/casual/ に起票
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

### 8. REX_HP_Brain 構築予定

`Setona_HP` リポは既に存在するが、Wiki-hp 専属体制と専用NLMが未整備。

#### 構築フロー
1. ボス判断で構築開始
2. NotebookLMで新規ノートブック作成 → UUID取得
3. 本ADRに REX_HP_Brain を追記(supersede形式または新ADR制定)
4. registry/nlm.md 更新
5. ADR-Role の権限マトリクスに反映
6. STARTUP_CODES.md 改訂を Wiki-casual Planner に依頼(pending/casual/ 起票)
7. Wiki-hp 起動コードでの初回セッション実施

### 9. 新規NLM追加フロー(Wiki-hp 以外の将来追加)

1. 必要性の議論を pending/ に記録(Casual-Plannerまたは関係Plannerが起票)
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

---

## Consequences

### 利点
- RAG汚染が 1:1原則で構造的に防止される
- 各ロールが自分の担当NLMだけに集中でき、運用が単純
- ミナト承認ゲートにより専門領域の純度が保たれる
- 廃止NLMのUUID記録により混乱再発防止
- Wiki-hp 構築予定の予約により、将来追加が混乱なく実施できる

### トレードオフ
- Casual → 専門 の昇格に人手が必要(自動化不可)
- NLM が増えるほど管理コストが上がる
- 非公式API依存のため、NLM側仕様変更時の対応コストがある
- 1:1原則により、ロール横断の集約クエリが直接できない(Casual_Brain経由が必要)

### 設計原則との整合
- **α (単純な土台を保つ)**: 1:1 は最小限の対応関係
- **β (de-risking 後の拡張禁止)**: 旧Trade_Brain の RAG汚染という de-risking 経験から学んだ分離原則を守る
- **γ (実装タイミングはシステム安定性に従属)**: 新NLM追加は安定後に実施

### 将来課題
- Stage 2/3 での横断統合モード検討(詳細: `wiki/ROADMAP.md`)
- Claude.ai単独運用時のNLM運用設計

---

## Alternatives Considered

### 案A: 単一NLM集約
- 全情報を1つのノートブックに集約してRAG精度向上を狙う
- **却下**: 旧Trade_Brain の汚染経験により再現リスク確定

### 案B: 専門NLM内に casual サブセクション
- 各専門NLMに casual カテゴリを追加して横断知見を分散保管
- **却下**: 検索時に分散され、横断知見の一体性が失われる

### 案C: 1:n 共有モデル
- 複数ロールが同じNLMにアクセス可能
- **却下**: 越権書込リスク・RAG汚染リスク両方が再導入される

### 案D: Wiki-Eval を全NLM管理
- 統括Evaluatorが全NLMに書込権限を持つ
- **却下**: 1:1原則違反。各Plannerが自分の領域のメモリ管理権を持つことが、専門性集約の本質

---

## References

- [registry/nlm.md](../registry/nlm.md) - 現在のNLM登録簿
- [ADR-Role](ADR-Role.md) - 担当ロール定義
- [CLAUDE.md](../../CLAUDE.md) - 中脳/大脳構造の long-term vision
- [wiki/STARTUP_CODES.md](../STARTUP_CODES.md) - NLM × Vault 分業マトリクス(運用文書)
