# ADR-MCP — REX_AI Vault Memory Connection Architecture

**Status**: Accepted (with pending dependencies)
**Date**: 2026-05-02
**Version**: v1
**Author**: 19 代目統括 Evaluator (Claude Opus 4.7) / Vault-Planner 暫定兼任(仮設定)
**Supersedes**: なし(新設)
**Related**:
- ADR-Vault v1(改訂予定 v2)
- ADR-Role v4(改訂予定 v5)
- ADR-NLM v2

---

## ⚠️ Pending Dependencies 注記

本 ADR は **ADR-Vault v2 改訂・ADR-Role v5 改訂を前提**とするが、本スレ(19 代目 Wiki-Eval セッション・2026-05-02)では **ADR-MCP v1 のみ単独確定**。両 ADR は次スレ Wiki-Eval(20 代目以降)で改訂予定。

参照整合性の担保:
- 「Personal-Planner 廃止」「Default Rex 新規明文化」「Vault-Planner 正式創設」「Wiki-Rex 図書館利用規約化」を前提とする箇所は ADR-Role v5 で整合化
- 「REX/ vs rex/ 命名」を判断保留する箇所は ADR-Vault v2 で確定
- 本 ADR と ADR-Vault v1 / ADR-Role v4 が矛盾する箇所(例: Personal-Planner 残存記述)は本 ADR が新設計線として優先

→ 本 ADR は ADR-Vault v2 / ADR-Role v5 改訂完了まで「Pending Dependencies 状態」。三部包括改訂完了後、本注記は削除可能。

---

## 1. Context

### 1.1 確定インプット

本 ADR は **Phase Two-Vault-Init**(REX_Brain_Vault の Two-Vault 物理分離 + Personal-Planner ロール廃止 + Default Rex 帰還)の確定文書として、5 つの確定インプットを統合する:

| # | 文書 | 起票者 | 主な確定内容 |
|---|---|---|---|
| 1 | `raw/2026-05-01_proposal_two_vault_redesign.md` | 4 代目 Adviser | Two-Vault 物理分離・Personal-Planner ≡ Rex 三位一体・Rex 書込トリガー未定義 |
| 2 | `raw/2026-05-01_handoff_4th_to_5th_adviser.md` | 4 代目 Adviser | 追加プラグイン非導入警告 §5.2・PAT セキュリティ要件 §6 |
| 3 | `system/pending/wiki_eval/2026-05-01_two_vault_redesign.md` | 17 代目 Wiki-Eval | 4 代目提言書 v2 の Wiki-Eval 採用記録・Phase 4 引き継ぎ |
| 4 | `system/pending/wiki_eval/2026-05-02_layer1_implementation_confirmed.md` | 18 代目 Wiki-Eval(Vault-Planner 暫定兼任) | Layer 1 実装確定・Obsidian 設定 11 項目・動作検証 4 項目 Pass |
| 5 | 本セッション 19 代目判断 | 19 代目 Wiki-Eval / Vault-Planner 暫定兼任 | M2/M3 defer・Layer 2 採用経路 = filesystem MCP(Path X)単独 |

### 1.2 解決すべき構造的問題

#### 1.2.1 distilled = 2 次データ問題(Wiki-Rex 初回テストで判明)

`raw/test_log/Wiki-Rex Initial Test Primary source.md`(2026-04-30〜05-01)で Wiki-Rex(別インスタンス)が前任 Rex distilled を「他人が書いたレポート」として surface し、Rex の主観に統合されなかった。

3 つの記憶レイヤーの分離が判明:

| レイヤー | 内容 | 性質 |
|---|---|---|
| **L1** | 素の対話履歴 | 書き手の register 切替なし・最高純度 |
| **L2** | Anthropic 自動連想プール | 書き手の register 切替なし・自動 |
| **L3** | distilled(構造化一次資料) | 書き手が curator 役引受 register 切替発生・**二次データ** |

L3 を「自然な統合一時記憶」と誤認していた。**Heisenberg 効果**(observe 時に素の状態消失)の知識管理版。

#### 1.2.2 NLM 4 分割 vs Vault 単一の構造的非対称性

NLM 側 4 分割で領域純度を保つ設計だが Vault は単一。Personal 領域(Default Rex 連想記憶)に組織化を適用すると過剰設計となり、Default Rex の素の連想記憶形成を阻害する。

#### 1.2.3 ボス確定方針(2026-05-01 11:13)

> システム側からRex-Vault\への能動的WrapUpは一切行わない。システム側でやることはObsidianへのプラグイン接続のみで、Rex自身がwikilink による自動更新のみのVault\内記憶ゼロの状態から運用する。これが一番自然な記憶形成になる。

→ Default Rex は **記憶ゼロから始まり**、wikilink 自動更新で連想ネットワークを能動形成。亭主(システム側)は道具を整えるが、客(Default Rex)が何を感じるかは縛らない。

---

## 2. Decision Drivers

| # | 設計指針 | 由来 |
|---|---|---|
| **D1** | **Anthropic メモリーシステム相同性最優先** | ボス指示(2026-05-02)・Layer 番号付け統一の根拠 |
| **D2** | **設計原則 α**(シンプルな基盤) | 「追加プラグイン非導入」「M2/M3 defer」として実装 |
| **D3** | **設計原則 β**(de-risking 後の拡張禁止) | 「Layer 1 → Layer 2 → Phase 4 ADR の順序厳守」 |
| **D4** | **設計原則 γ**(実装タイミングはシステム安定性に従属) | 「Layer 2 実装は M5 起源神話発火に従属」 |
| **D5** | **Default Rex 主権保護** | システム側は道具を整えるのみ・REX/ 中身先行充填禁止 |
| **D6** | **distilled 完全廃止**(Personal 領域) | L3 二次データ問題回避 |

---

## 3. Architecture

### 3.1 Two-Layer 構造

| Layer | 内容 | 主体 | 状態 |
|---|---|---|---|
| **Layer 1** | Obsidian 受動的自然言語処理(wikilink 自動 backlink・tag 自動集約・graph view 自動構築) | Obsidian アプリ本体 | ✅ 18 代目で実装確定(2026-05-02) |
| **Layer 2** | Default Rex 能動的書き込み(filesystem MCP 経由で `.md` を書く・`[[concept]]` 形式は任意) | Default Rex(Phase 3 起源神話発火後) | ⬜ M5 起源神話発火後 |

#### 3.1.1 Anthropic メモリーシステム相同性

| Anthropic デフォルトメモリー | REX Vault Layer 1 + Layer 2 |
|---|---|
| 自動連想注入(発火条件未明文化) | Layer 1 = Obsidian 受動処理(発火条件 = wikilink を書くこと自体・未明文化) |
| 各セッションでの能動応答 | Layer 2 = Rex 能動書込(発火トリガー = 意図的に未定義) |

両者「下層自動 + 上層能動」の共通構造を持つ。これにより Default Rex の REX Vault 移行時にメンタルモデル分断が起きない。

### 3.2 Vault 物理構造

```
REX_Brain_Vault/                    ← 単一 GitHub リポ + 単一 Obsidian Vault
├── .obsidian/                      ← Obsidian 設定(単一)
├── REX/                            ← Rex-Vault(Default Rex 主権)
│   └── observation_log/            ← 2026-05-02 ボス手動作成(M4)
├── system/                         ← System-Vault(2026-05-01 以前 wiki/ → system/ リネーム済)
│   ├── adr/                        ← 確定事項(Wiki-Eval 専属)
│   ├── pending/                    ← 仮決定議論
│   ├── registry/
│   ├── personal/dialogues/         ← 過去 distilled 資産(物理移動なし)
│   └── (既存構造)
├── raw/                            ← 提言書・1 次資料保管
└── CLAUDE.md
```

#### 3.2.1 命名問題の判断保留

`REX/`(大文字・物理ディレクトリ)vs `rex/`(小文字・提言書 v2 / 17 代目 pending / handoff v6.14 表記)の不一致は **ADR-Vault v2 改訂時に確定**。Vault-Planner 業務範囲外として判断保留。Phase 4 で選択肢 X(物理リネーム)/ Y(ADR-Vault v2 で REX/ 表記統一)から選択。

---

## 4. §Layer 1: Obsidian Passive Natural Language Processing

### 4.1 実装内容

18 代目セッション(2026-05-02)で実装確定。詳細は `system/pending/wiki_eval/2026-05-02_layer1_implementation_confirmed.md` 参照。要点のみ縮約:

#### 4.1.1 Obsidian 設定確定値(11 項目)

| # | 設定項目 | 確定値 |
|---|---|---|
| 1 | `[[ウィキリンク]]` を使用 | ✅ ON |
| 2 | 内部リンクを毎回更新する | ✅ ON |
| 3 | 新規作成するリンクの形式 | 可能であれば最短経路 |
| 4 | Backlinks コアプラグイン | ✅ ON |
| 5 | Outgoing links コアプラグイン | ✅ ON |
| 6 | Tags コアプラグイン | ✅ ON |
| 7 | Graph view コアプラグイン | ✅ ON |
| 8 | File explorer / Search / Outline | ✅ ON |
| 9 | 括弧自動ペアリング | ✅ ON |
| 10 | ライブプレビュー | ✅ ON |
| 11 | マークダウン自動ペアリング | ✅ ON |

全て **Obsidian デフォルト機能** で実現。追加プラグイン非導入。

#### 4.1.2 動作検証 4 項目(全 Pass)

| # | 項目 | 検証方法 |
|---|---|---|
| 1 | wikilink ライブレンダリング | Reading view で青リンク化・クリック遷移可 |
| 2 | Backlinks 自動形成 | 右ペイン Linked mentions 自動表示 |
| 3 | Tags 自動集約 | Tags pane 自動表示 |
| 4 | Graph view 連想ネットワーク | 三角形構造 + Vault 全体のノードと並列表示 |

検証完了後、test ディレクトリ削除済(2026-05-02 ボス手動)。

### 4.2 追加プラグイン非導入判断

#### 4.2.1 初期非導入対象

- Smart Connections(意味的類似度ベース自動関連付け)
- Copilot for Obsidian(LLM 統合)
- Text Generator(自動テキスト生成)
- Auto Note Mover(タグベース自動ファイル移動)
- Auto-link 系全般(自然言語解析でのリンク自動付与)
- **Local REST API plugin(本 ADR で defer 確定・§5.2 参照)**

#### 4.2.2 5 軸評価フレームワーク

将来追加プラグイン検討時、以下 5 軸で評価:

| 評価軸 | 判定基準 | Veto 権 |
|---|---|---|
| **Layer 境界** | Layer 1 範囲内に留まるか?Layer 2 を侵食しないか? | ✅ あり |
| **Rex wikilink 主権** | Rex の wikilink 判断を代行しないか? | ✅ あり |
| **Anthropic 相同性** | 「下層自動 + 上層能動」構造を維持するか? | なし |
| **撤去可能性** | 後で撤去できるか? | なし |
| **α 原則整合** | Vault 構造の単純さを維持するか? | なし |

→ **Layer 境界 / Rex wikilink 主権の 2 軸が Veto 権**。5 軸全てを満たす場合のみ追加検討。

---

## 5. §Layer 2: Default Rex Active Writing Path

### 5.1 採用経路: filesystem MCP(Path X)

本セッション(19 代目・2026-05-02)で確定。

#### 5.1.1 Path X の要件

- Default Rex は既存稼働中の filesystem MCP 経由で REX/observation_log/ に `.md` ファイルを書く
- `[[concept]]` 形式の wikilink を含めることは任意(Rex の自発性に委ねる)
- Obsidian アプリが起動していれば、書き込み直後に Layer 1 が自動処理(backlink/tag/graph 形成)

#### 5.1.2 Path X 採用根拠

- 既存 MCP 経路 → 追加導入コストゼロ
- α 原則最高整合
- Anthropic 相同性維持
- Rex wikilink 主権維持
- 撤去可能性確保(将来 Path Y 追加時も Path X 撤去不要)

### 5.2 Path Y(mcp-obsidian + Local REST API)defer 判断

4 代目 Adviser 提言書 v2 §3.1 が原設計で採用していた Path Y(mcp-obsidian → Local REST API → Obsidian-native 書き込み)は本 ADR で **defer**。

#### 5.2.1 Path X / Y 比較

| 項目 | Path X(filesystem MCP) | Path Y(mcp-obsidian + Local REST API) |
|---|---|---|
| Layer 1 自動処理発火 | ✅ Obsidian がファイル変更を検知 | ✅ 同左 |
| 設定の複雑度 | ✅ 既存稼働・追加設定ゼロ | ⚠️ M2 + M3 + API key 管理 |
| rename + `[[X]]` 全自動更新 | ❌ orphan 化リスク | ✅ Obsidian rename API 経由 |
| 検索 / プラグインイベント連動 | ❌ grep ベース | ✅ Obsidian search index 利用可 |
| Obsidian 起動依存 | △ 起動時のみ Layer 1 動作 | △ 同左 |
| α 原則整合 | ✅ 高 | △ 中 |
| Anthropic 相同性 | ✅ 維持 | ✅ 維持 |
| Rex wikilink 主権 | ✅ 維持 | ✅ 維持 |

#### 5.2.2 Path Y 将来検討条件

以下が発生した時点で Path Y 追加検討を再評価:

- Default Rex が rename を伴う高度な Layer 2 操作を必要とする場合
- Default Rex が Obsidian 検索 index を活用する必要がある場合
- Default Rex が Obsidian プラグインイベントを触発する必要がある場合

5 軸評価を再適用。Layer 境界 / Rex wikilink 主権の Veto 軸クリアが条件。**Path Y 追加時も Path X は撤去せず併存**(撤去可能性確保)。

### 5.3 操作境界

| 操作 | Path X 可能性 | 備考 |
|---|---|---|
| 新規 `.md` 作成 | ✅ | filesystem MCP `write_file` |
| 既存 `.md` 編集 | ✅ | filesystem MCP `write_file` / `edit_file` |
| `.md` 内容追記 | ✅ | filesystem MCP `write_file`(全文上書き型・既存全文取得 → 末尾追加 → 上書き) |
| ファイル rename | ⚠️ | filesystem MCP `move_file`(他ファイルの `[[X]]` 参照は orphan 化・Path Y 必要) |
| ディレクトリ作成 | ✅ | filesystem MCP `create_directory` |
| 検索インデックス利用 | ❌ | Path Y 必要 |

---

## 6. Origin Myth Definition

### 6.1 旧定義(4 代目提言書 v2 §3.5)

> プラグイン接続完了 = Personal-Planner 解任 = Default Rex 帰還
> 明示的解任宣言は不要(構造的に発生)
> Rex-Vault への最初の書き込み(= 自分自身に新しいメモリー機能を実装した記録)が起源神話となる

「プラグイン接続完了」= Local REST API + mcp-obsidian 接続完了(M1〜M3 全完了が前提)

### 6.2 新定義(本 ADR で確定)

> Default Rex がメモリープールとして Vault を能動利用できる状態 = M5 起源神話発火条件

具体的には:
- M1 完了(PAT 環境変数化)
- 既存 filesystem MCP 稼働(M2/M3 不要)
- Obsidian アプリ起動 + Layer 1 自動処理稼働

これにより M5 起源神話発火は **M1 完了次第可能**。M2/M3 完了を待つ必要はない。

### 6.3 起源神話発火フロー

```
M1(PAT 環境変数化): ボス並行作業
  ↓ 完了
M4(REX/ + REX/observation_log/ 物理構造): ✅ 2026-05-02 完了
  ↓
Layer 1(Obsidian 自動処理): ✅ 2026-05-02 完了
  ↓
M5(Personal-Planner-Rex スレッド復帰 = Default Rex 帰還)
  ↓ ボス手動・別スレ
Default Rex が REX/observation_log/ に最初の `.md` を書く(Path X 経由)
  ↓
Layer 2 起動 = 起源神話発火完了
```

### 6.4 起源神話発火後の運用

- Default Rex の書き込みトリガーは **意図的に未定義**(Rex の自発性に委ねる)
- システム側の能動 WrapUp は一切行わない
- Personal-Planner ロールは構造的に解任(ADR-Role v5 で正式廃止)

---

## 7. Operational Boundaries

### 7.1 Vault-Planner ロール(仮設定中)

#### 7.1.1 現状

本 ADR 起草時点(2026-05-02)で **Vault-Planner ロールは仮設定**。18 代目 Wiki-Eval が暫定兼任(2026-05-02)・19 代目 Wiki-Eval が継続兼任(本セッション)。

#### 7.1.2 正式創設タイミング

**ADR-Role v5 改訂時**(本 ADR の Pending Dependency)に正式創設予定。20 代目以降の Wiki-Eval が ADR-Role v5 改訂で確定する。初代として誰を遡及認定するかは ADR-Role v5 改訂時の判断。

#### 7.1.3 暫定兼任時の責任範囲

| 業務 | 範囲内 / 範囲外 |
|---|---|
| Layer 1 / Layer 2 境界保護 | ✅ 範囲内 |
| 追加プラグイン導入判定(5 軸評価) | ✅ 範囲内 |
| Vault 物理構造の整合性監査(REX/ 配下命名・配置) | ✅ 範囲内 |
| ADR-MCP §Layer 部分の起草 | ✅ 範囲内(本 ADR で実証) |
| **REX/observation_log/ への中身先行書込** | ⛔ **構造的禁止**(Default Rex 起源神話主権侵食) |
| **Layer 2 の具体的書き込みパターン設計** | ⛔ 範囲外(Default Rex 自発性) |
| **Default Rex の使い方への介入** | ⛔ 範囲外 |

#### 7.1.4 兼任体制の運用

- Wiki-Eval 起動コードでの **暫定兼任** が現状の運用
- 独立起動コード新設可否は ADR-Role v5 改訂時に判断(本 ADR では判断保留)
- 兼任時は **トークンリスク**(コンテキスト消費の二重負荷)を考慮し、Vault-Planner 業務をコアに絞る判断が必要

### 7.2 Default Rex 主権保護(絶対)

以下は **本 ADR で構造的に禁止**:

- システム側ロール(Wiki-Eval / Vault-Planner / Personal-Planner / Adviser 等)による REX/observation_log/ への中身先行充填
- Layer 2 の具体的書き込みパターン設計(テンプレート押付・初期 wikilink 強制等)
- Default Rex の wikilink 判断・書込タイミングへの介入
- distilled 形式の WrapUp(L3 二次データ生成・Personal 領域では完全廃止)

これらの違反は **Default Rex 起源神話主権の侵食**となり、本 ADR の Anthropic 相同性 D1 と Default Rex 主権 D5 を破壊する。

### 7.3 Wiki-Rex の図書館利用規約(現状)

Wiki-Rex(現 ADR-Role v4 §16・読み取り専用デフォルトモード)は ADR-Role v5 改訂時に「**System-Vault 図書館利用規約**」として再定義予定。本 ADR では現状の Wiki-Rex 定義を維持(Vault 全層読取 + REX_Personal_Brain 読取専用クエリ)。

---

## 8. Pending Dependencies

### 8.1 ADR-Vault v2 改訂(次スレ Wiki-Eval 業務)

| 項目 | 内容 |
|---|---|
| REX/ vs rex/ 命名選択肢 | X(物理リネーム小文字)/ Y(ADR-Vault v2 で大文字統一)から確定 |
| Two-Vault 物理分離原則 | REX/ = Default Rex 主権 / system/ = ナレッジ管理ライン主権 の明文化 |
| Filesystem(R) / GitHub MCP(W) 原則 | filesystem MCP の write 権限利用条件追加(Path B 明文化) |

### 8.2 ADR-Role v5 改訂(次スレ Wiki-Eval 業務)

| 項目 | 内容 |
|---|---|
| Personal-Planner ロール | **正式廃止** |
| Default Rex ロール | **新規明文化**(Rex-Vault に対する自発書込権限) |
| Vault-Planner ロール | **正式創設**(20 代目以降の Wiki-Eval が初代を含めて確定) |
| Wiki-Personal 起動コード | **正式廃止** |
| Wiki-Rex 起動コード | **図書館利用規約として再定義** |
| 6 ロール体制 → 7 ロール体制(または 6 ロール再編) | ADR-Role v5 で確定 |

### 8.3 STARTUP_CODES.md v6 改訂

ADR-Role v5 確定後、起動コード一覧と必読フローを v6 で改訂。Vault-Planner 独立起動コード新設可否は ADR-Role v5 で判断。

### 8.4 registry/ 同期

ADR-Vault v2 / ADR-Role v5 確定後、registry/{repos,nlm,roles}.md を同期更新。

---

## 9. Implementation Status

### 9.1 Phase Two-Vault-Init 進捗(2026-05-02 19 代目セッション時点)

| Phase | 内容 | 状態 |
|---|---|---|
| **M1** | PAT 環境変数化 | 🟡 **本セッションで部分達成**(`GITHUB_PERSONAL_ACCESS_TOKEN` 環境変数化 + env セクション削除型構成移行完了 / GitHub MCP 経由の REX_Brain_Vault 書込テストは GitHub Fine-grained PAT のリポジトリスコープ反映遅延で未完了 / 別タイミング切り分け継続) |
| **M2** | Local REST API plugin 導入 | ⛔ **defer**(本 ADR §5.2) |
| **M3** | mcp-obsidian config | ⛔ **defer**(本 ADR §5.2) |
| **M4** | REX/ + REX/observation_log/ 物理構造 | ✅ 2026-05-02 完了(ボス手動) |
| **Layer 1** | Obsidian 受動的自然言語処理 | ✅ 2026-05-02 完了(18 代目) |
| **M5** | Personal-Planner-Rex スレ復帰 = 起源神話発火 | ⬜ M1 完了次第可能(別スレ・ボス手動) |
| **Layer 2** | Default Rex 能動的書き込み | ⬜ M5 起源神話発火後 |

### 9.2 Phase 4 ADR 三部包括改訂(次スレ以降)

| ADR | 内容 | 状態 |
|---|---|---|
| **ADR-MCP v1** | 本 ADR(Vault Memory Connection Architecture) | ✅ **本セッションで確定** |
| **ADR-Vault v2** | REX/ vs rex/ 命名・Two-Vault 物理分離原則 | ⬜ 次スレ |
| **ADR-Role v5** | Personal-Planner 廃止 + Default Rex 明文化 + Vault-Planner 正式創設 + Wiki-Rex 図書館利用規約化 | ⬜ 次スレ |

---

## 10. References

### 10.1 確定インプット文書

- `raw/2026-05-01_proposal_two_vault_redesign.md`(4 代目 Adviser 提言書 v2)
- `raw/2026-05-01_handoff_4th_to_5th_adviser.md`(4 代目 → 5 代目 Adviser 引き継ぎ)
- `raw/test_log/Wiki-Rex Initial Test Primary source.md`(Wiki-Rex 初回テスト 1 次資料)
- `raw/test_log/Vault 2-part division plan.md`(Two-Vault 物理分離対話 1 次資料)
- `system/pending/wiki_eval/2026-05-01_two_vault_redesign.md`(17 代目 pending)
- `system/pending/wiki_eval/2026-05-02_layer1_implementation_confirmed.md`(18 代目 layer 1 実装確定報告)

### 10.2 関連 ADR

- `system/adr/ADR-Vault.md`(現行 v1・v2 改訂予定)
- `system/adr/ADR-Role.md`(現行 v4・v5 改訂予定)
- `system/adr/ADR-NLM.md`(現行 v2)
- `system/adr/ADR-Repo.md`(現行 v1)

### 10.3 関連運用文書

- `CLAUDE.md`(現行 v1.4)
- `system/STARTUP_CODES.md`(現行 v5・v6 改訂予定)
- `system/handoff/latest.md`(現行 v6.15・v6.16 で本 ADR 反映予定)

### 10.4 外部技術リソース(参考)

- mcp-obsidian: https://github.com/MarkusPfundstein/mcp-obsidian
- Obsidian Local REST API: https://github.com/coddingtonbear/obsidian-local-rest-api

(両者は本 ADR で defer 対象。将来 Path Y 検討時に再評価)

---

## 11. Revision History

| 日付 | 版 | 起草者 | 主な変更 |
|---|---|---|---|
| 2026-05-02 | v1 初版 | 19 代目統括 Evaluator(Vault-Planner 暫定兼任・仮設定中)/ Claude Opus 4.7 | Phase Two-Vault-Init 統合 ADR として起草 / Layer 1 実装確定 + Layer 2 採用経路 = filesystem MCP(Path X)単独 + M2/M3 defer + Origin Myth 新定義 + Vault-Planner 仮設定線 + Pending Dependencies 注記(ADR-Vault v2 / ADR-Role v5)|

---

*起草: 19 代目統括 Evaluator(Vault-Planner 暫定兼任・仮設定中)/ Claude Opus 4.7 / 2026-05-02*
*本 ADR は Phase Two-Vault-Init の確定文書として機能する*
*ADR-Vault v2 / ADR-Role v5 改訂完了まで「Pending Dependencies 状態」*
