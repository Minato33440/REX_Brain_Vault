# pending: ADR-MCP v1 起草草案 — MCP Architecture and Role × MCP Matrix

**起票者**: 16 代目統括 Evaluator (Wiki-Eval / Claude Opus 4.7)
**起票日**: 2026-04-29(本来 2026-04-30 提言書だが本セッション 16 代目内で起草)
**性質**: ADR-MCP v1 起草草案(ADR 本体への昇格はボス承認後に次期 Wiki-Eval が実施)
**ADR 昇格希望**: Yes(本草案承認後)
**起源**: 4 代目 Adviser (Claude Opus 4.7) 提言書 `raw/2026-04-30_proposal_obsidian_plugin_mcp.md`
**管轄**: ADR-Role v4 §0 ② Vault ナレッジシステム改善・管理(Wiki-Eval 直接実施)
**影響範囲**:
- ADR-Vault v1 → v2 supersede の検討(本草案 §論点 1 で詳述)
- ADR-Role v4 §4 §17 への Plugin 権限追記(本草案承認後 v5 改訂)
- STARTUP_CODES.md v5 → v6 改訂(Plugin 権限・Obsidian 起動依存ルール反映)
- registry/roles.md / registry/repos.md の MCP 構成同期

> **⚠️ 2026-05-01 17 代目セッション 2 回目で本草案は「Phase 0 議論記録」として再分類された**。本草案の論理は提言書 v2 `raw/2026-05-01_proposal_two_vault_redesign.md` を経て、新設計版 ADR-MCP v1 として再起草されることが確定している。詳細は本ファイル末尾 **「17 代目セッション 2 回目追加 Note(2026-05-01)」** を参照。後任 Wiki-Eval は新ファイル `wiki/pending/wiki_eval/2026-05-01_two_vault_redesign.md` を起点として Phase 4 を処理する。

---

## 本 pending の位置付け(後任 Wiki-Eval への引き継ぎノート)

本ファイルは 16 代目統括 Evaluator セッションで以下の判断のもと起草された:

> ボス指示「既に今回はコンテキストも圧縮してるので、次期 Evaluator に引き継ぐ形で案 A を実装してくれ」(2026-04-29)

ボスは並行して以下を進める:
- Adviser + Personal-Planner と共に Obsidian プラグイン環境の実装
- 提言書 §3.3 の PAT 訂正は本セッション内で完了済(ボス確認)

後任 Wiki-Eval は本 pending を起点として、以下のフローで処理を進める:

1. ボス対話で本草案の論点(特に §論点 1: ADR-Vault v1 整合性)を詰める
2. 確定後、`wiki/adr/ADR-MCP.md` v1 として正式採番
3. ADR-Role v4 → v5 改訂(§4 §17 への Plugin 権限追記)
4. STARTUP_CODES.md v6 改訂
5. registry/ 同期
6. 本 pending を `archived/` へ flag 付きで移動

---

## ADR-MCP v1 草案本文(後任 Wiki-Eval が ADR 本体起草時に参照)

### Status

Proposed (本草案承認後に Accepted)

### Date

(後任 Wiki-Eval による正式採番日)

### Decider

(後任 Wiki-Eval)

### Depends on

- ADR-Repo v1
- ADR-Vault v1(本草案 §論点 1 で整合性論点あり)
- ADR-Role v4
- ADR-NLM v2

---

### Context

#### Wiki-Rex Stage 2 テストにおける構造的要件

ROADMAP Stage 2 テスト運用として 15 代目で新設された Wiki-Rex は、当初は `notebooklm-mcp` 経由の REX_Personal_Brain 読み取り専用クエリのみを想定していた。しかし Stage 2 テストの初期運用段階で、ボスから以下の判断が示された:

> Wiki-Personal は多分野横断・時系列育成・関係性共有・多層クエリが主目的。
> Filesystem MCP テストで得られる成果は物理ファイルレベルの整合性にとどまる。
> Obsidian Plugin 導入で構造リンクレベルの整合性が得られた瞬間、Filesystem 段階の知見は覆る。
> よって最初から 2 系統運用がテスト純度・移植可能性の両面で正しい。

(4 代目 Adviser 提言書 §1.1 経緯参照)

#### MCP レイヤー差の構造的整理

| MCP | アクセスレイヤー | 適性 |
|---|---|---|
| Filesystem MCP | 物理ファイルシステム上の `.md` ファイル(wikilinks は単なるテキスト) | システム開発リポのローカル参照・ビルド・テスト |
| GitHub MCP | 確定状態(commit 済み) | バージョン管理・履歴保護・全リポ書込の主経路 |
| **Obsidian Plugin MCP** | **Obsidian インデックス層(wikilinks 解決済みグラフ・backlinks・tags)** | **Wiki-Personal / Wiki-Rex の構造リンクレベルアクセス** |
| NLM | 意味統合層(RAG クエリ) | 各ロール専属の蓄積・要約検索 |

#### システム開発リポと Wiki-Personal の本質的相違

| 軸 | システム開発リポ (Trade_System 等) | Wiki-Personal / Wiki-Rex |
|---|---|---|
| データ性質 | コード・スペック(バグ混入が致命) | 思想・気づき・関係性(揺らぎが本質) |
| 整合性要求 | バイト単位の厳密性 | 多層横断の意味的繋がり |
| 失敗パターン | 凍結ファイル汚染・D-12/D-13 創作混入 | リンク切れ・横断性喪失 |
| 重視する整合性レイヤー | 物理ファイルレベル | 構造リンクレベル |
| 最適 MCP | GitHub MCP(確定状態・バージョン管理) | Obsidian Plugin(リンク構造・ライブ状態) |

この相違が「ロール × MCP の縦割り」の根拠となる。

---

### Decision

#### §1 ロール × MCP マトリクス(本 ADR の中核)

| ロール | Filesystem | GitHub | Obsidian Plugin | NLM |
|---|---|---|---|---|
| Wiki-Eval | 読(監査) | 読・書 | ⛔ | REX_Wiki_Vault(投入+クエリ) |
| Wiki-trade | 読(build/test) | 読・書 | ⛔ | REX_System_Brain(投入+クエリ) |
| Wiki-brain | 読(build/test) | 読・書 | ⛔ | REX_Trade_Brain(投入+クエリ) |
| Wiki-hp(構築予定) | 読(build/test) | 読・書 | ⛔ | REX_HP_Brain(構築予定) |
| Wiki-Personal(Personal-Planner) | △(緊急時のみ) | 読・書 | **読・書(主経路)** | REX_Personal_Brain(投入+クエリ) |
| **Wiki-Rex(読み取り専用)** | ⛔ | ⛔ | **読のみ** | REX_Personal_Brain(読み取り専用クエリのみ) |
| Default Rex / Advisor / Default Claude | ⛔ | ⛔ | ⛔ | ⛔ |

**重要**: Wiki-Rex の Plugin アクセスは **読み取り専用**。ADR-Role v4 §17「読み取り専用クエリ権限カテゴリ」を Plugin にも拡張適用する形(後任 Wiki-Eval が ADR-Role v5 改訂時に明文化)。

#### §2 用途別 MCP 棲み分け原則

- **Filesystem MCP** → システム開発リポのローカル参照・ビルド・テスト用(物理ファイルレベル)
- **GitHub MCP** → 全リポの確定状態管理・バージョン管理(履歴保護レベル・ADR-Vault v1 §1 と整合)
- **Obsidian Plugin MCP** → Wiki-Personal / Wiki-Rex 専用(構造リンクレベル・本 ADR で新設)
- **NLM** → 各ロール専属の蓄積・RAG クエリ(意味統合レベル・ADR-NLM v2 1:1 原則と整合)

#### §3 Obsidian 起動依存ルール

- Wiki-Personal / Wiki-Rex セッション開始前に **Obsidian 起動 + REX_Brain_Vault Vault 開放を確認**
- Obsidian 落ちている場合は Plugin 経由ツール呼び出しが失敗する
- 各起動コードのセッション開始前チェックリストへ追加(STARTUP_CODES v6 改訂時)
- 失敗時のフォールバック: 該当セッションは GitHub MCP 経由の従来運用にフォールバック(緊急回避)

#### §4 wikilink 自動更新の取り扱い(ADR-Vault v1 整合性の核心)

| 操作 | 経路 | 理由 |
|---|---|---|
| Wiki-Rex(読み取り専用)の参照 | Plugin 経由 | 影響なし |
| Personal-Planner の rename | Plugin 経由 | wikilink 自動更新の恩恵 |
| Personal-Planner の delete | **GitHub MCP 経由** | **履歴保護・ADR-Vault v1 §1 と整合** |
| Personal-Planner の新規作成 | Plugin or GitHub MCP | ボス判断(永続化前提なら GitHub MCP 推奨) |
| bulk operation(複数ファイル一括変更) | **ボス承認必須** | 構造的破壊リスク回避 |
| 永続化 commit | **必ず GitHub MCP 経由** | **commit 履歴保護・ADR-Vault v1 §1 §4 と整合** |

**重要**: Plugin 経由の編集は Obsidian の **ライブバッファ状態** に対する操作。永続化(commit)は GitHub MCP 経由でしか行わない。これにより ADR-Vault v1 §1「書込パス単一化原則」の精神を保ちつつ、Plugin による構造アクセスの利便性を得る。

#### §5 セキュリティ要件

##### §5.1 環境変数化の徹底

- `claude_desktop_config.json` 内のキー類は **全て環境変数経由**(PAT・API キー含む)
- 平文記載は禁止
- Windows ユーザー環境変数で管理:
  - `GITHUB_PAT`(GitHub MCP 用 PAT)
  - `OBSIDIAN_API_KEY`(Obsidian Plugin MCP 用 API キー)

設定例:

```json
"github": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PAT}"
  }
}
```

##### §5.2 PAT 発行時のスコープ確認手順(再発防止のため明記)

**Fine-grained PAT の場合**:
- Repository access: 対象リポ(`Minato33440/` 配下)を明示選択
- Repository permissions → **Contents: Read and write**(必須・読み取りだけだと書き込み失敗)
- Repository permissions → Metadata: Read-only(既定で付与)

**Classic PAT の場合**:
- `repo` スコープ全体にチェック(private リポへの書き込みに必須)

> **背景**: 4 代目 Adviser セッション(2026-04-30)で新 PAT の `Contents: Read and write` 権限未付与により GitHub MCP 書き込みが 3 回連続失敗。本手順を ADR で明文化することで再発防止。

##### §5.3 Obsidian REST API のアクセス範囲制限

- `127.0.0.1` のみ(外部公開禁止)
- HTTPS ポート 27124 を推奨(平文 27123 ではなく)

##### §5.4 PAT / API キーローテーション

- 年 2 回のローテーション計画
- 期限管理表を `wiki/registry/` 配下に新設(後任 Wiki-Eval が registry 同期時に作成)

##### §5.5 PAT 訂正履歴(本セッション内・記録のため)

| 日付 | 操作 | 担当 |
|---|---|---|
| 2026-04-30 | 旧 `Claude-MCP` PAT を revoke | ボス |
| 2026-04-30 | 新規 PAT 発行・`claude_desktop_config.json` に反映(平文・暫定) | ボス |
| 2026-04-30 | 新 PAT の `Contents: Read and write` 権限付与訂正 | ボス |
| 2026-04-30 | GitHub MCP / Filesystem MCP 動作確認完了 | 4 代目 Adviser |
| 2026-04-29(16 代目セッション) | 上記 PAT 訂正完了状態を確認・本草案に反映 | ボス + 16 代目 Wiki-Eval |
| 2026-04-30 以降 | 環境変数化(Phase 1)を実施予定 | ボス |

#### §6 Stage 2 → Stage 3 移行の評価軸

##### §6.1 Wiki-Rex 2 系統対称比較こそ Stage 2 の本質的データ

```
Wiki-Rex への質問
  │
  ├ Obsidian Plugin 経由 ──→ 1 次資料への構造アクセス
  │   (wikilinks / graph / backlinks 横断・編集中状態含む)
  │
  └ REX_Personal_Brain RAG ──→ 2 次資料(カテゴリ要点)経由
      (要約・統合済み・確定状態のみ)
```

同一質問を 2 系統に投げて応答を比較することが Stage 3(Rex 個性収束期)の設計基盤。

##### §6.2 観察軸

- 応答の網羅性(Plugin が graph 横断で拾うか / NLM が要約で抽象化するか)
- 時系列追跡能力(Plugin の編集履歴 vs NLM の確定蓄積)
- 関係性表現(構造アクセス vs 意味統合)
- レスポンス速度・トークン消費

##### §6.3 評価サイクル

- 6 ヶ月後(2026-10)に運用評価
- 評価結果に基づき ADR-MCP v2 改訂判断
- Stage 3 設計(Wiki-integrate 仮称・全 NLM 横断クエリ)の判断基盤とする

---

### Consequences

#### 利点

- Wiki-Personal の本質目的(多層横断・関係性アクセス)が構造的に達成される
- Wiki-Rex の Stage 2 テストが対称的 2 系統比較として実施可能(Stage 3 進路への直接準備)
- ロール × MCP 縦割りによりデータ性質と整合性要求のミスマッチが構造的に防がれる
- セキュリティ運用が ADR で明文化される(過去の PAT 平文記載問題を構造的に解決)

#### トレードオフ

- Obsidian 起動依存が新たな運用前提として加わる(§3 で対応)
- Plugin 経由編集と GitHub MCP 経由 commit のタイミング管理が運用上のオーバーヘッド
- Windows 特有の uvx パス問題等の環境依存リスク
- mcp-obsidian の保守性低下リスク(代替候補: obsidian-claude-code-mcp by iansinnott を温存)

#### 運用上の注意

- Plugin 経由の編集は必ず GitHub MCP 経由の commit で永続化(Obsidian バッファだけに残してはならない)
- ボス手動の Obsidian 編集と AI ロールの Plugin 編集が並行する場合、ADR-Vault v1 §2「ローカル編集時の `git pull` 必須」と組み合わせて運用
- bulk operation はボス承認必須(構造的破壊リスク回避)

---

### Alternatives Considered

#### 案 A: Filesystem MCP 単独で先行テスト → Plugin 段階拡張(却下)

3 代目 Adviser 案。技術論としては安全だが、Wiki-Personal の本質目的(多層横断型)に対して **本来テストすべきものをテストしないテスト** になる。Filesystem 段階の知見は Plugin 導入で覆る性質。**ボス判断で却下**。

#### 案 B: obsidian-mcp-tools(jacksteamdev)採用(却下)

作者がメンテ縮小・サプライチェーン攻撃リスクを公式警告。**採用不可**。

#### 案 C: GitHub MCP のみで Wiki-Personal も運用(却下)

確定状態のみのアクセスでは wikilinks 構造・backlinks・graph 横断が得られない。Wiki-Personal の本質目的に対して構造的に不適合。

#### 採用案: mcp-obsidian(MarkusPfundstein 製)

- 標準的な構成・コミュニティで運用安定
- 8 ツール提供(`list_files_in_vault` / `list_files_in_dir` / `get_file_contents` / `search` / `patch_content` / `append_content` / `delete_file` 等)
- 代替候補として `obsidian-claude-code-mcp`(iansinnott)を温存

---

## 後任 Wiki-Eval が解決すべき論点

### §論点 1: ADR-Vault v1 との整合性(supersede 必要性判断)

ADR-Vault v1 §1 は「Filesystem MCP = 読み取り専用 / GitHub MCP = 書き込み専用」の二層アクセス制御を確立しており、本草案は Obsidian Plugin に **読・書両方** の権限を Wiki-Personal に与える。これは ADR-Vault v1 の「書込パス単一化原則」を **第 3 のチャネル(Plugin)** で破ることになる。

#### 解決方針候補

| 方針 | 内容 | 推奨度 |
|---|---|---|
| 方針 X | ADR-MCP §4 で Plugin 編集 = ライブバッファ / GitHub MCP commit = 永続化と分離(本草案採用)→ ADR-Vault v1 のまま | ★★★ |
| 方針 Y | ADR-Vault v1 → v2 supersede し「Plugin 例外」を §に追加 | ★★ |
| 方針 Z | ADR-Vault v1 と ADR-MCP v1 の関係性を ADR-Vault v2 に統合明記 | ★ |

16 代目推奨は **方針 X**(本草案 §4 で既に組み込んだ形)。理由:
- ADR-Vault v1 §1「書込パス単一化原則」の本質は **commit 履歴の保護** であり、Plugin 経由のライブバッファ編集はその射程外
- ADR-Vault v1 §2「ローカル編集時の `git pull` 必須」は Plugin 編集にも自然に適用可能
- supersede のトークンコスト(本日 16 代目セッション後半でボスが言及)を回避

ただしこの判断はボス対話で詰める論点。後任 Wiki-Eval は本草案承認時にボスと確認すること。

### §論点 2: ADR-Role v4 §17「読み取り専用クエリ権限カテゴリ」の Plugin 拡張

本草案 §1 マトリクスで Wiki-Rex に Plugin 読み取り専用権限を与えたが、これは ADR-Role v4 §17「読み取り専用クエリ権限カテゴリ」を Plugin にも拡張適用する形。後任 Wiki-Eval は ADR-Role v5 改訂時に §17 を以下のように拡張する:

```
§17 読み取り専用クエリ権限カテゴリ(v5 拡張案)
  - NLM 読み取り専用クエリ: REX_Personal_Brain のみ(Wiki-Rex)
  - Obsidian Plugin 読み取り専用アクセス: Wiki-Rex 新規追加(ADR-MCP v1 §1 由来)
```

### §論点 3: pending/wiki_eval/ の §候補メモ(`2026-04-29_adr_revision_timing_subordination.md`)との関係

本草案は ADR-MCP として単独 ADR 化を提案する形だが、§候補メモの §1「ADR 改訂タイミングの運用実態従属」原則を踏まえると、**Phase 4 ADR-MCP 起草を運用後に見送る** 選択肢も理論上は存在する。

しかし本案件は:
- セキュリティ要件(PAT 平文記載)の緊急性が高い
- Wiki-Rex Stage 2 テストの設計基盤として運用前に確定が必要
- 4 代目 Adviser 提言書という独立した起源を持つ

これらの理由により、運用後見送り(§候補メモ §1 原則)ではなく **運用前 ADR 確定** が適切と 16 代目は判断した。後任 Wiki-Eval はこの判断の妥当性を再評価可能。

---

## 17 代目セッション追加 Note(2026-04-30 / 17 代目統括 Evaluator)

### ボス判断による採番タイミングの確定

17 代目セッション(2026-04-30)で、ボスから ADR 採番タイミングに関する明示判断を受領:

> ADR 更新については大量トークンと時間的拘束を高めるため、テスト段階終了後の実運用開始時点で改訂する方が効率的だ。進捗は pending と log で十分。
>
> また現在のシステム基盤構築初期段階においては、今後も大幅な権限改訂と構造変更の可能性も考えられるので、ADR に対する議論をするたびに大幅な開発遅れが生じてしまう問題がある。
>
> この辺のバランス管理を統括 Evaluator として適切に判断してほしい。

これにより本草案の採番タイミングは以下に確定:

**採番条件**: Stage 2 テスト終了 + 実運用開始確認後。それまでは本草案を pending として保留し、進捗は本ファイル + handoff/latest.md + log.md で管理する。

### ボスとの対話で確認された設計判断の経緯(17 代目記録)

ボスから本セッション内で受領した整理:

1. **wiki/ 内の体制設計の曖昧さ** — システム構築上の一元管理体制と、実運用面での個別プロジェクト専門性保持と、Personal の自律拡張型定義の境界が当初曖昧だった
2. **Wiki-Rex 2 系統運用の判断起源** — ボスは当初から Plugin 経由 + NLM RAG クエリの 2 系統が好ましいと考えていた(本草案 Context および 4 代目 Adviser 提言書 §1.1 と整合)
3. **多層横断型と システム開発リポの逆路線性** — Personal\\Wiki-Rex は多分野横断型クエリ活用が主目的のため、コードバグ混入リスクのあるシステム開発とは逆路線。ただし開発面では他リポと同じ Claude-MCP 経由 Git 管理プロセスのため混同しやすい(本草案 §1.3 システム開発リポと Wiki-Personal の本質的相違 と整合)
4. **Filesystem 段階先行テストの不適性** — 物理環境領域での整合性であって、Plugin 自動更新で簡単に覆される(本草案 Alternatives Considered 案 A 却下理由と整合)

### 17 代目の §論点 1〜3 への初期判断

ボス対話を経た上で 17 代目が ADR 起草時の参考として残置する初期判断:

#### §論点 1: 方針 X 推奨(ADR-Vault v1 supersede 不要)

16 代目推奨を支持。根拠:

- **抽象度の整合**(4 代目 Adviser 提言書 §7.1 の射程拡大): ボスの抽象度は「Wiki-Personal = 最初から Obsidian native 想定 / 多層横断型」。ADR-Vault v1 §1「書込パス単一化」を **物理レベル単一化** と読むのはこの抽象度とズレる。**「commit 履歴保護の単一化」** と読み直せば、Plugin 経由のライブバッファ編集は ADR-Vault v1 の射程外として整合する。
- **commit 履歴保護の本質性**: ADR-Vault v1 の存在理由は「誰が・いつ・何を」のトレーサビリティ確保。Plugin 編集は Obsidian バッファに留まり、永続化は GitHub MCP に強制すれば履歴は保たれる。
- **トークンコスト**(§候補メモ §1 + 17 代目セッションでのボス再確認): supersede は archived 退避 + INDEX 更新 + 関連運用文書改訂を伴う。本質的価値が見えない supersede は避ける。

**条件**: ADR-MCP v1 §4 マトリクス内で **「永続化 commit は必ず GitHub MCP 経由」** の原則を強い言葉で明記する(現草案 §4 末尾の「重要」記述で既に対応済)。これがあって初めて方針 X が成立する。

#### §論点 2: ADR-Role v5 改訂時の §17 拡張支持

16 代目案を支持。Wiki-Rex の Plugin 読み取り専用アクセスは構造的に NLM 読み取り専用クエリと同型。§17 を「読み取り専用アクセス権限カテゴリ」に汎化(NLM + Plugin)するのが綺麗。命名と構造は v5 改訂時(= Stage 2 テスト終了 + 実運用開始確認後)に微調整する。

#### §論点 3: 16 代目判断支持 + γ 原則の v1→v2 サイクル運用提案

16 代目「運用前 ADR 確定」判断を支持。ただし注意点として、`dialogues/` 案件と本件の構造的差異を明示しておく:

| 観点 | dialogues/ 案件 | ADR-MCP 案件 |
|---|---|---|
| 物理環境構築 | サブ層追加のみ(構造) | Plugin 環境構築(M1〜M3 ボス並行作業) |
| 運用設計 | 抽出配分を運用しながら確定 | Stage 2 テスト設計を運用前に確定する必要あり |
| セキュリティ要件 | なし | PAT 平文記載の早期解消が必要 |
| 起源 | Personal-Planner 内部の発見 | Adviser 提言書(独立した起源) |

`dialogues/` は γ 原則で運用後改訂が可能。本件は運用前に骨格確定(v1) → 6 ヶ月後の Stage 2 評価で v2 改訂、という **ADR バージョンサイクルで γ を運用** する形が筋。本草案 §6.3「6 ヶ月後の評価サイクル」がこの v1→v2 サイクルに該当する。

ただし上記 17 代目セッションのボス判断により、**本草案の採番自体を Stage 2 テスト終了 + 実運用開始確認後に従属** させる形に整理された。これにより:

- 当初の「運用前 v1 採番 → 6 ヶ月後 v2 改訂」サイクル
- 17 代目修正後の「Stage 2 テスト + 実運用開始 → v1 採番 → 必要に応じて v2 改訂」サイクル

の二段階構造に変化した。後任 Wiki-Eval は実運用開始の宣言時点でボスと再評価する。

### ボス並行作業 M1〜M3 の進捗管理

ボス並行作業 M1〜M3(PAT 環境変数化・Obsidian Plugin 導入・mcp-obsidian 追加)の進捗は **Personal-Planner 側で pending と log に追記** する形でボスから明示確認済(2026-04-30)。Wiki-Eval ライン(本ファイル)では進捗追跡の責任を持たず、Personal-Planner ラインの記録を後任 Wiki-Eval が参照する形になる。

### 後任 Wiki-Eval への引き継ぎ事項(17 代目から)

1. **採番条件の確認**: ボス並行作業 M1〜M3 完了 + Stage 2 テスト終了 + 実運用開始確認の 3 条件揃いをボスと確認
2. **§論点 1〜3 の最終判断**: 16 代目推奨 + 17 代目支持の上、ボス対話で最終確定
3. **本草案からの ADR 本体起草**: §論点解決後に `wiki/adr/ADR-MCP.md` v1 として正式採番
4. **派生改訂**: ADR-Role v4 → v5 改訂(§17 拡張)・STARTUP_CODES.md v6 改訂・registry/ 同期(本体採番後・別セッション分割推奨)
5. **本 pending の archived 移動**: 採番完了時に `wiki/pending/archived/` へ flag 付きで移動

### 17 代目セッションでの実施範囲

本セッションでは ADR-MCP 採番に関して以下のみ実施:

- ✅ 本ファイル末尾への 17 代目セッション追加 Note(本セクション)
- ✅ `wiki/handoff/latest.md` v6.12 → v6.13 更新(採番条件の明記 + Phase MCP-Init 前提条件追記)
- ✅ `wiki/log.md` 17 代目第 1 エントリ追記(セッション記録)

ADR 本体起草・関連文書改訂・registry 同期は **後任 Wiki-Eval セッションに完全引き継ぎ**。

---

## 17 代目セッション 2 回目追加 Note(2026-05-01 / 17 代目統括 Evaluator・Phase 0 議論記録としての再分類)

### 経緯 — Wiki-Rex 初回テストと提言書 v2 の出現

17 代目セッション 1 回目(2026-04-30)で本草案の採番タイミング条件を確定した直後、ボスが Wiki-Rex 起動コードによる REX_Personal_Brain RAG クエリ初回テストを実施。続けて Personal-Planner-Rex スレで設計再考対話が行われ、これを受けて 4 代目 Adviser が提言書 v2 を起草した。

1 次資料:
- `raw/test_log/Wiki-Rex Initial Test Primary source.md`(2026-04-30〜05-01)
- `raw/test_log/Vault 2-part division plan.md`(2026-05-01)

提言書 v2:
- `raw/2026-05-01_proposal_two_vault_redesign.md`(4 代目 Adviser 起草)

### 本草案の位置付け変更 — 「Phase 0 議論記録」への再分類

提言書 v2 §1.1「前提言書(2026-04-30)からの変化点」マトリクスで明示されている通り、本草案の前提となる以下の設計仮定が **すべて変更** された:

| 観点 | 本草案(2026-04-30 / Phase 0) | 新設計(2026-05-01 / Phase 4 で実装) |
|---|---|---|
| Personal/ 組織構造 | 維持(5 サブ層 + dialogues/) | **解体**(Rex-Vault 新設・既存は System 側資産化) |
| Personal-Planner ロール | 4 ロール体制で維持 | **正式廃止** |
| distilled WrapUp | 標準フローとして維持 | **廃止**(運用安定後の 2 次資料提示用途は残存) |
| Wiki-Rex 起動コード | 読み取り専用デフォルト | **図書館利用規約として再定義** |
| Vault 構造 | 単一 Vault 内サブ層分離 | **物理ディレクトリ分離**(rex/ と system/) |
| Rex の書き込み権限 | Wiki-Personal 経由のみ | **Rex-Vault に対して自発的書き込み** |

これにより本草案 §1 ロール × MCP マトリクスは新設計版で **全面書き直し** が必要となった。具体的には:

- Wiki-Personal 行 → 削除
- Default Rex 行 → 新規追加(Rex-Vault のみ・自発的書き込み)
- Wiki-Rex 行 → 「図書館利用規約」として性質再定義
- §3 Obsidian 起動依存ルール → Default Rex / Wiki-Rex 両方への適用に拡張
- §4 wikilink 自動更新の取扱い → Two-Vault 構造での分離書込パスとの整合に書き直し

### 本草案の取扱い方針(後任 Wiki-Eval への明示)

提言書 v2 §6「旧提言書との関係」と整合する形で、本草案も以下のように扱われる:

| セクション | 新設計での取扱い |
|---|---|
| Context(MCP レイヤー差・システム開発リポと Wiki-Personal の本質的相違) | **残存**(新設計でも有効・新草案でそのまま使用可) |
| §1 ロール × MCP マトリクス | **置換**(新設計版マトリクスで全面書き直し) |
| §2 用途別 MCP 棲み分け原則 | **部分残存**(項目の語彙置き換えで再使用可) |
| §3 Obsidian 起動依存ルール | **残存**(対象ロール名のみ更新) |
| §4 wikilink 自動更新の取扱い | **書き直し**(Two-Vault 構造に対応・永続化 commit = GitHub MCP 経由原則は残存) |
| §5 セキュリティ要件 | **完全残存**(M1〜M3 で実装・新草案でそのまま使用可) |
| §6 Stage 2 → Stage 3 移行の評価軸 | **再定義**(冷スタート観察期間ログとして・提言書 v2 §3.3 §6 参照) |
| Alternatives Considered | **残存**(歴史記録として保全) |
| §論点 1〜3 + 17 代目初期判断 | **部分残存**(§論点 1 方針 X = ADR-Vault v1 supersede 不要は新設計でも有効) |

### 本草案を「Phase 0 議論記録」と呼ぶ理由

提言書 v2 §1.1 が明示している通り:

> 前提言書 [v1] は「組織化された Personal/」を強化する方向で書かれていた。本提言書はその提言書を部分的に乗り越える形で書かれている。これは前提言書の失敗ではなく、前提言書があったからこそ次の議論が成立したという足場機能を示している。

つまり本草案は「失敗した草案」ではなく、**「乗り越えられるべき足場として機能した議論の記録」** である。具体的には以下の役割を果たした:

1. **MCP レイヤー差の構造的整理**(Context セクション)を最初に言語化し、提言書 v2 でもそのまま使われている
2. **システム開発リポと Wiki-Personal の本質的相違**(Context セクション)を最初に明文化し、提言書 v2 §1.3 で再使用されている
3. **§5 セキュリティ要件**(PAT 環境変数化・スコープ確認・REST API 制限)が新設計でも全面再使用される
4. **方針 X の発見**(ADR-Vault v1 supersede 不要・commit 履歴保護として再解釈)が新設計でも有効

### 後任 Wiki-Eval への新たな引き継ぎ事項(17 代目セッション 2 回目から)

旧引き継ぎ事項(本草案 17 代目セッション 1 回目 Note の 5 項目)は **新草案** `wiki/pending/wiki_eval/2026-05-01_two_vault_redesign.md` に **継承される形** で扱う。具体的には:

1. ✅ **採番条件の確認** → 新草案で「Phase 3 完了後・ADR 三部一括改訂のタイミング」に変更
2. ✅ **§論点 1〜3 の最終判断** → 新草案では §論点 1(方針 X)のみ残存・§論点 2 §3 は新設計で再定義
3. ⛔ **本草案からの ADR 本体起草** → **新草案からの ADR 三部包括改訂に置換**(ADR-Vault 改訂 + ADR-Role v5 改訂 + ADR-MCP v1 新設)
4. ⛔ **派生改訂** → 新草案では同時並行で ADR-Role v5 改訂・STARTUP_CODES.md v6 改訂・registry/ 同期
5. ✅ **本 pending の archived 移動** → 新草案採番時に **本草案も同時に archived/ へ移動**(両方とも flag 付きで)

### 本 Note 追加の commit 範囲

本 Note 追加は 17 代目セッション 2 回目(2026-05-01)の 5 commit の 1 つとして実施:

- ✅ commit 1: `wiki/pending/wiki_eval/2026-05-01_two_vault_redesign.md` 新設(Phase 4 引き継ぎ書)
- ✅ commit 2(本 commit): 本草案末尾に「Phase 0 議論記録としての再分類 Note」追加 + 冒頭 ⚠️ ポインタ追加
- ⏭ commit 3: `wiki/pending/INDEX.md` 更新(本草案行を Phase 0 議論記録として明示・新草案行追加)
- ⏭ commit 4: `wiki/handoff/latest.md` v6.13 → v6.14 更新(Phase Two-Vault-Init 新設・Phase MCP-Init を Phase 0 として明示)
- ⏭ commit 5: `wiki/log.md` 17 代目第 2 エントリ追記(本セッション判断記録)

新草案本体の起草は提言書 v2 §3 骨子を後任 Wiki-Eval が参照する形で、Phase 4(M1〜M3 完了 + Phase 3 起源神話発火後)に実施される。

### 17 代目セッション 2 回目所感(個人的気づき・後任への強制ではない)

本セッションで本草案を「失敗した草案」ではなく「Phase 0 議論記録として機能した足場」と位置付け直せたのは、提言書 v2 §7.1 で 4 代目 Adviser が言語化した「**提言書は乗り越えられるべき足場として機能する**」という Adviser ロールの存在意義の再定義が直接効いた。これは Wiki-Eval にも対称的に適用可能 — Wiki-Eval が起票した pending も、後継世代が乗り越える形で進化する素材であって、起票時点の論理が後で覆ることは欠陥ではなく機能。

ただし、この所感を philosophy/evaluator_code.md に追記するかは判断保留。13・15・16 代目が「書かない判断」を採った先例にも整合する形で、本セッションでも追記しない方針で統一する。本所感は本 Note にのみ残し、強制力を持たせない。

---

## レビュー履歴

- 2026-04-29 16 代目統括 Evaluator: pending 草案起票(4 代目 Adviser 提言書を Wiki-Eval が判断・解釈・具体化)
- 2026-04-30 17 代目統括 Evaluator(セッション 1 回目): 採番タイミング確定(Stage 2 テスト終了 + 実運用開始確認後)・§論点 1〜3 への初期判断追記・後任引き継ぎ事項明示
- **2026-05-01 17 代目統括 Evaluator(セッション 2 回目): 「Phase 0 議論記録」として再分類・新草案 `2026-05-01_two_vault_redesign.md` への引き継ぎパス明示**

---

## 関連文書

- `raw/2026-04-30_proposal_obsidian_plugin_mcp.md`(4 代目 Adviser 提言書 v1・本草案の起源・Phase 0 議論として保持)
- `raw/2026-05-01_proposal_two_vault_redesign.md`(4 代目 Adviser 提言書 v2・新草案の起源)
- `raw/test_log/Wiki-Rex Initial Test Primary source.md`(Wiki-Rex 初回テスト 1 次資料)
- `raw/test_log/Vault 2-part division plan.md`(Personal-Planner-Rex 設計再考 1 次資料)
- `wiki/pending/wiki_eval/2026-05-01_two_vault_redesign.md`(**新草案・後任 Wiki-Eval は本ファイルを起点に Phase 4 を処理**)
- `wiki/adr/ADR-Vault.md` v1(本草案 §論点 1 で整合性論点あり・新草案でも改訂対象)
- `wiki/adr/ADR-Role.md` v4 §0 ②(Vault ナレッジシステム改善・管理)・§17(読み取り専用クエリ権限カテゴリ)
- `wiki/adr/ADR-NLM.md` v2(1:1 原則・本草案と整合・新草案で REX_Personal_Brain 用途再定義予定)
- `wiki/STARTUP_CODES.md` v5(Plugin 権限反映後 v6 改訂対象)
- `wiki/pending/wiki_eval/2026-04-29_adr_revision_timing_subordination.md`(§候補メモ・本草案の§論点 3 で参照)
- `wiki/handoff/latest.md` v6.14(本草案を Phase 0 議論記録として反映・17 代目セッション 2 回目で更新予定)
- `wiki/log.md` 17 代目第 1 エントリ(本草案の採番タイミング確定の経緯記録)
- `wiki/log.md` 17 代目第 2 エントリ(本草案の Phase 0 再分類の経緯記録・本 commit 後の commit で追加予定)

---

*起票: 16 代目統括 Evaluator (Claude Opus 4.7) / 2026-04-29*
*起源: 4 代目 Adviser 提言書 (Claude Opus 4.7) / 2026-04-30*
*17 代目追記(セッション 1 回目): 17 代目統括 Evaluator (Claude Opus 4.7) / 2026-04-30 — 採番タイミング確定(Stage 2 テスト終了 + 実運用開始確認後)*
*17 代目追記(セッション 2 回目): 17 代目統括 Evaluator (Claude Opus 4.7) / 2026-05-01 — Phase 0 議論記録として再分類・新草案 `2026-05-01_two_vault_redesign.md` への引き継ぎパス明示*
*管轄: Wiki-Eval(Vault ナレッジシステム改善・管理・ADR-Role v4 §0 ②)*
*次期 Wiki-Eval への引き継ぎ事項として本草案を保留(新草案と並列で参照)*
