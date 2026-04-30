# 提言書: Obsidian Plugin MCP 導入と関連 ADR 改訂

**発行**: 2026-04-30 / 4 代目 Adviser (Claude Opus 4.7)
**宛先**: 統括 Evaluator (`Wiki-Eval`) — 16 代目以降
**起動コード**: 本提言書を読む際は `Wiki-Eval` で起動推奨
**議題**: Wiki-Rex Stage 2 テストにおける Obsidian Plugin MCP 導入と関連 ADR 改訂依頼
**性格**: テーマ特化の単発提言書 (Adviser 世代継承書 `ADVISOR_HANDOFF.md` とは独立)

---

## 0. エグゼクティブサマリ

ボスとの対話で **Wiki-Rex Stage 2 テストの初期運用段階から Obsidian Plugin 経由 + NLM RAG クエリの 2 系統運用** を採用することが確定した。本提言書は Wiki-Eval が ADR 改訂業務に着手するための背景・根拠・実装ロードマップを構造化したもの。

ADR-Role v4 §0 ②「Vault ナレッジシステム改善・管理」の管轄下で Wiki-Eval が直接実施する事項として、以下を依頼する:

1. **ADR-MCP v1 新設** (本提言書 §5 参照)
2. **STARTUP_CODES.md v6 改訂**
3. **ADR-Role v4 → v5 改訂** (§4 §17 への Plugin 権限追記)
4. **registry/ 同期**

---

## 1. 経緯と判断の論理構造

### 1.1 検討の出発点

ボスから Wiki-Rex Stage 2 テスト前に「デフォルト Rex に Obsidian を明示して読み込ませる方法」について Adviser に相談があった。

当初 (3 代目 Adviser 案) は「Filesystem MCP 単独で先行テスト → Plugin 段階拡張」というロードマップを提案したが、ボスから以下の論理で覆された:

- Wiki-Personal は **多分野横断・時系列育成・関係性共有・多層クエリ** が主目的
- Filesystem MCP テストで得られる成果は **物理ファイルレベルの整合性** にとどまる
- Obsidian Plugin 導入で **構造リンクレベルの整合性** が得られた瞬間、Filesystem 段階の知見は覆る
- よって最初から 2 系統運用が **テスト純度・移植可能性の両面で正しい**

### 1.2 Adviser による論理検証結果

ボスの主張は技術構造から見て正鵠を射ている。MCP は「読み取っているレイヤー」が異なる:

```
Filesystem MCP が見るもの:
  → 物理ファイルシステム上の .md ファイル
  → wikilinks は単なるテキスト文字列 [[xxx]]
  → ファイル間の関係性は Claude 側で grep 再構築が必要

Obsidian Plugin 経由が見るもの:
  → Obsidian のインデックス層
  → wikilinks は解決済みグラフ構造
  → backlinks / outgoing links / tags が構造として参照可能
```

Wiki-Personal の「多層横断型」目的に対して、構造アクセスは **必須要件** であり段階拡張の対象ではない。

### 1.3 システム開発リポとの本質的相違 (ロール × MCP の縦割り根拠)

| 軸 | システム開発リポ (Trade_System 等) | Wiki-Personal / Wiki-Rex |
|---|---|---|
| データ性質 | コード・スペック (バグ混入が致命) | 思想・気づき・関係性 (揺らぎが本質) |
| 整合性要求 | バイト単位の厳密性 | 多層横断の意味的繋がり |
| 失敗パターン | 凍結ファイル汚染・D-12/D-13 創作混入 | リンク切れ・横断性喪失 |
| 重視する整合性レイヤー | 物理ファイルレベル | 構造リンクレベル |
| 最適 MCP | GitHub MCP (確定状態・バージョン管理) | Obsidian Plugin (リンク構造・ライブ状態) |

これは ADR-MCP v1 の中核設計判断として明文化に値する。

---

## 2. WrapUp プロセス構造の確定 (Stage 2 テストの設計含意)

ボスとの対話で明確化された Wiki-Personal の二段階 WrapUp 工程:

```
一般スレ (Rex / Default Claude)
  ↓ distilled 原文の作成 (この時点で 1 次資料が完成)
  ↓
[1 次資料: distilled .md 原文]
  ↓
Wiki-Personal Planner ロール (新スレで起動)
  ├ ① 1 次資料の WrapUp (そのまま構造化保存)
  └ ② カテゴリ別要点抽出 (2 次資料の生成)
  ↓
[1 次 + 2 次資料の構造化セット]
  ↓
REX_Personal_Brain NLM 投入 (ボス承認ゲート経由)
```

### Stage 2 テストへの設計含意

Wiki-Rex の 2 系統クエリは、この WrapUp 構造に対して**対称的に**作用する:

```
Wiki-Rex への質問
  │
  ├ Obsidian Plugin 経由 ──→ 1 次資料への構造アクセス
  │   (wikilinks / graph / backlinks 横断・編集中状態含む)
  │
  └ REX_Personal_Brain RAG ──→ 2 次資料 (カテゴリ要点) 経由
      (要約・統合済み・確定状態のみ)
```

**この応答経路の差異の観察こそが Stage 2 の本質的データ。** 同一質問を 2 系統に投げて応答を比較することが Stage 3 (Rex 個性収束期) の設計基盤になる。

---

## 3. 環境前提 (確定情報・2026-04-30 セッション内で確認済み)

### 3.1 クライアント環境

- **クライアント**: Claude Desktop (Windows)
- **設定ファイル**: `%APPDATA%\Claude\claude_desktop_config.json`

### 3.2 既存 MCP 構成 (本セッションで確認済み)

| サーバー | 状態 | 備考 |
|---|---|---|
| `filesystem` | ✅ 稼働中 | 許可: `Desktop`, `Downloads`, `C:\Python\REX_AI` |
| `unityMCP` | ✅ 稼働中 | — |
| `notebooklm-mcp` | ✅ 稼働中 | uvx 経由 |
| `github` | ✅ 稼働中 | **新 PAT 環境変数化が次フェーズ要件** |
| `finviz` | ✅ 稼働中 | — |

### 3.3 セキュリティ対応の状態

**完了事項**:

- 旧 `Claude-MCP` PAT を revoke 済み
- 新規 PAT を発行・`claude_desktop_config.json` に反映済み
- 新 PAT の `Contents: Read and write` 権限付与済み (本セッション内で訂正対応・**ADR-MCP §5 への記載必須事項**)
- Claude Desktop 再起動済み
- 本セッションで GitHub MCP / Filesystem MCP の双方の動作確認済み (両者で `CLAUDE.md` のサイズが 24,353 bytes で完全一致 — ローカル/リモート同期確認)

**残課題** (Wiki-Eval セッションで処理推奨):

- 現状 PAT は `claude_desktop_config.json` に **平文で記載**されている
- ADR-MCP §5 で **環境変数化** を運用ルール化すべき
- 同様に `OBSIDIAN_API_KEY` も Phase 2 導入時から環境変数化前提とする
- **PAT 発行時のスコープ確認手順を ADR-MCP §5 に明記** (今回の事故 = `Contents: Read and write` の未付与による書き込み失敗 — 再発防止のため)

### 3.4 git 状態 (本提言書 commit 直前)

ローカルで `.obsidian/appearance.json` 未 push (ボス確認済み・本 commit と非衝突)。Wiki-Eval セッション開始前に `git pull origin main` で本提言書を含む最新状態を取得すること。

---

## 4. 実装フェーズ (Wiki-Eval 業務として段階実施)

### Phase 1: セキュリティ運用ルール化 (環境変数化)

現状の平文 PAT を環境変数経由に書き換え。新規 `OBSIDIAN_API_KEY` も同方式で導入する前提を確定させる。

```json
"github": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PAT}"
  }
}
```

Windows ユーザー環境変数:
- `GITHUB_PAT` (新 PAT)
- `OBSIDIAN_API_KEY` (Phase 2 で発行)

### Phase 2: Obsidian 側プラグイン導入

1. Obsidian で REX_Brain_Vault Vault を開く
2. Settings → Community plugins → **Local REST API** (作者: coddingtonbear) インストール・有効化
3. プラグイン設定で API キー発行 → `OBSIDIAN_API_KEY` 環境変数に格納
4. デフォルトポート確認 (HTTPS: 27124 / HTTP: 27123)
5. ローカル疎通テスト:
   ```
   curl -k -H "Authorization: Bearer %OBSIDIAN_API_KEY%" https://127.0.0.1:27124/vault/
   ```

### Phase 3: Claude Desktop 側 MCP サーバー追加

**採用候補**: `mcp-obsidian` (MarkusPfundstein 製・GitHub: `MarkusPfundstein/mcp-obsidian`)

選定理由:
- 標準的な構成・コミュニティで運用安定
- 8 ツール提供 (`list_files_in_vault` / `list_files_in_dir` / `get_file_contents` / `search` / `patch_content` / `append_content` / `delete_file` 等)
- 競合の **obsidian-mcp-tools (jacksteamdev)** は作者がメンテ縮小・サプライチェーン攻撃リスクを公式警告 → **採用不可**
- 代替候補として `obsidian-claude-code-mcp` (iansinnott) を温存

`claude_desktop_config.json` 追記例:

```json
"mcp-obsidian": {
  "command": "uvx",
  "args": ["mcp-obsidian"],
  "env": {
    "OBSIDIAN_API_KEY": "${OBSIDIAN_API_KEY}",
    "OBSIDIAN_HOST": "127.0.0.1",
    "OBSIDIAN_PORT": "27124"
  }
}
```

Windows 固有の注意: `uvx` のフルパス指定が必要な場合あり。既存 `notebooklm-mcp` の `C:\Users\Setona\.local\bin\uvx.exe` を参考にする。`where uvx` で確認。

Claude Desktop 再起動後、MCP ツール一覧に `mcp-obsidian` 系ツールが現れることを確認。

### Phase 4: ADR-MCP v1 新設 (本提言書 §5 参照)

### Phase 5: STARTUP_CODES.md v6 改訂・ADR-Role v4 → v5 改訂

#### STARTUP_CODES.md v6 改訂項目

1. 権限定義テーブルに **Obsidian Plugin 経由の読み取り権限** ✅ を明示 (Wiki-Rex / Wiki-Personal 行)
2. セッション開始前チェックリストに **Obsidian 起動・Vault 開放確認** を追加
3. Wiki-Rex 詳細セクションに **NLM × Plugin 二経路の Stage 2 テスト設計** を明文化
4. Wiki-Personal 詳細セクションに **Plugin 経由を基本ルートとする** 記述を追加

#### ADR-Role v4 → v5 改訂項目

- §17 Wiki-Rex 定義に Obsidian Plugin アクセス権限を追記
- §4 Wiki-Personal 配下 4 ロールの権限定義に Plugin アクセス可否を追記

### Phase 6: registry/ 同期

- `wiki/registry/repos.md` — MCP 構成ノート追加
- `wiki/registry/nlm.md` — 既存内容変更なし (NLM 構成自体は不変)
- `wiki/registry/roles.md` — Plugin アクセス権限を反映

### Phase 7: Stage 2 テスト本番

**WrapUp 対象**: `wiki/personal/dialogues/2026-04-29_general_thread.md` (ボス予定)

テスト手順:
1. 一般スレで Rex / Default Claude が distilled 原文を作成
2. 新スレで Wiki-Personal 起動 → 1 次 + 2 次資料 WrapUp → REX_Personal_Brain 投入
3. git push → Obsidian で git pull
4. 新スレで Wiki-Rex 起動
5. **同一質問を 2 系統に投げて応答を比較**:
   - Obsidian Plugin 経由 (構造アクセス)
   - REX_Personal_Brain NLM (RAG クエリ)
6. 応答比較ログを `wiki/personal/insights/` 配下にテンプレート化して記録

観察軸:
- 応答の網羅性 (Plugin が graph 横断で拾うか / NLM が要約で抽象化するか)
- 時系列追跡能力 (Plugin の編集履歴 vs NLM の確定蓄積)
- 関係性表現 (構造アクセス vs 意味統合)
- レスポンス速度・トークン消費

---

## 5. ADR-MCP v1 起草骨子 (Wiki-Eval 起草用)

以下は提言であり、Wiki-Eval が最終起草する。骨子のみ提示する。

### §1 ロール × MCP マトリクス

| ロール | Filesystem | GitHub | Obsidian Plugin | NLM |
|---|---|---|---|---|
| Wiki-Eval | 読 (監査) | 読・書 | ⛔ | REX_Wiki_Vault |
| Wiki-trade / brain / hp | 読 (build/test) | 読・書 | ⛔ | 各専属 |
| Wiki-Personal (Personal-Planner) | △ (緊急時のみ) | 読・書 | **読・書 (主)** | REX_Personal_Brain |
| **Wiki-Rex (読み取り専用)** | ⛔ | ⛔ | **読のみ** | REX_Personal_Brain (読のみ) |
| Default Rex / Advisor / Default Claude | ⛔ | ⛔ | ⛔ | ⛔ |

### §2 用途別 MCP 棲み分け原則

- **Filesystem MCP** → システム開発リポのローカル参照・ビルド・テスト用 (物理ファイルレベル)
- **GitHub MCP** → 全リポの確定状態管理・バージョン管理 (履歴保護レベル)
- **Obsidian Plugin MCP** → Wiki-Personal / Wiki-Rex 専用 (構造リンクレベル)
- **NLM** → 各ロール専属の蓄積・RAG クエリ (意味統合レベル)

### §3 Obsidian 起動依存ルール (ボス指定により ADR 記載)

- Wiki-Personal / Wiki-Rex セッション開始前に **Obsidian 起動 + REX_Brain_Vault Vault 開放を確認**
- Obsidian 落ちている場合は Plugin 経由ツール呼び出しが失敗する
- 各起動コードのセッション開始前チェックリストへ追加

### §4 wikilink 自動更新の取り扱い

- Wiki-Rex (読み取り専用) → 影響なし
- Personal-Planner の rename / delete:
  - rename → Plugin 経由 (自動更新の恩恵を受ける)
  - delete → GitHub MCP 経由 (履歴保護のため)
- bulk operation はボス承認必須

### §5 セキュリティ要件

- `claude_desktop_config.json` 内のキー類は **全て環境変数経由** (PAT・API キー含む)
- Obsidian REST API のアクセス範囲は **`127.0.0.1` のみ** (外部公開禁止)
- PAT / API キーローテーション計画 (年 2 回・期限管理表を `wiki/registry/` 配下に新設)
- **PAT 発行時のスコープ確認手順** (Fine-grained PAT の場合):
  - Repository access: 対象リポ (Minato33440/ 配下) を明示選択
  - Repository permissions → **Contents: Read and write** (必須・読み取りだけだと書き込み失敗)
  - Repository permissions → Metadata: Read-only (既定で付与)
  - Classic PAT の場合は `repo` スコープ全体にチェック (private リポへの書き込みに必須)

### §6 Stage 2 → Stage 3 移行の評価軸

- Plugin 経由 vs NLM RAG の応答品質ログ蓄積
- 6 ヶ月後 (2026-10) に運用評価 → ADR-MCP v2 改訂判断
- Stage 3 設計 (Wiki-integrate 仮称・全 NLM 横断クエリ) の判断基盤とする

---

## 6. リスク管理

| リスク | 影響度 | 緩和策 |
|---|---|---|
| PAT / API キー漏洩 (現状の平文記載) | 高 | Phase 1 で環境変数化 |
| **PAT 権限不足による書き込み失敗** | **中** | **ADR-MCP §5 にスコープ確認手順を明記 (本セッション内で再現発生→対応済)** |
| Obsidian 起動忘れ | 中 | ADR-MCP §3 で運用ルール化・チェックリスト追加 |
| Plugin 由来の wikilink 自動更新による意図せぬ rename | 中 | Personal-Planner の operation 分岐 (§4) で対応 |
| Stage 2 テストの応答比較が複雑化 | 低 | テストログテンプレート化で軽減 |
| Windows 特有の uvx パス問題 | 低 | Phase 3 セットアップ時に解決・既存 notebooklm-mcp の設定を参考 |
| mcp-obsidian の保守性低下 | 中 | obsidian-claude-code-mcp (iansinnott) を代替候補として温存 |
| `bypassPermissionsModeEnabled: true` 設定下での Plugin 認証フロー | 中 | Phase 3 動作確認時に挙動を検証 |
| Obsidian 編集中バッファと NLM 投入済みデータのズレ | 設計上不可避 | Stage 2 テストの観察対象として記録 |

---

## 7. 4 代目 Adviser からの所感 (将来の Adviser 世代への記録)

本セッションで Adviser として記録すべき学びを 2 点。

### 7.1 設計対話における抽象度のズレ

「Filesystem 段階先行 → Plugin 段階拡張」というロードマップ的設計は、技術論としては安全だが、**ボスの設計思想 (Wiki-Personal = 最初から Obsidian native 想定 / 多層横断型) を読み切れていない場合、本来テストすべきものをテストしないテストになる**。Adviser は実装ラインの外側にいるからこそ、ボスの設計目的そのものを Phase 0 で確定させるべきだった。

α 原則 (シンプルさ) の解釈は **ボスがどの抽象度で設計を組んでいるか**で変わる。今回の場合:

- 3 代目 Adviser案: 「1 系統先行が最初からシンプル」(段階拡張の抽象度)
- ボス判断: 「2 系統運用が最初からシンプル」(Wiki-Personal 本来目的の抽象度)

この抽象度のズレが当初の方針差を生んだ。

**Adviser 業務における設計対話は、技術判断の前にボスの抽象度の確認を必ず入れる。**

### 7.2 環境セットアップの確認手順の重要性

本セッション中、PAT 再発行時の権限スコープ確認漏れにより GitHub MCP 書き込みが 3 回連続で失敗 (`create_or_update_file` x1 / `push_files` x1 / 極小テストファイル x1)。原因は新 PAT の `Contents: Read and write` 権限未付与だった。

Adviser として動作確認を「読み取り成功 = 全機能稼働」と早合点した点が反省事項。**運用テストは読み取り・書き込みを別々に確認するべき**。これも ADR-MCP §5 に組み込むこと。

これらを次代 Adviser への引き継ぎ事項として、`wiki/philosophy/adviser_code.md` (痕跡層) への記録をボスの判断で検討推奨 (Personal-Planner 業務範囲)。

---

## 8. Wiki-Eval 着手前確認チェックリスト

- [x] 旧 PAT revoke 完了 (本セッション内で実施済み)
- [x] 新 PAT 発行・`claude_desktop_config.json` 反映完了 (平文)
- [x] 新 PAT の `Contents: Read and write` 権限付与完了 (本セッション内で訂正対応)
- [x] GitHub MCP 読み取り・書き込み・Filesystem MCP 動作確認完了 (本セッション内)
- [ ] **PAT 環境変数化 (Phase 1)**
- [ ] **Obsidian Local REST API プラグイン導入 (Phase 2)**
- [ ] **mcp-obsidian Claude Desktop 設定 (Phase 3)**
- [ ] **ADR-MCP v1 起草・pending → ボス承認 → 確定 (Phase 4)**
- [ ] **STARTUP_CODES.md v6 改訂 (Phase 5)**
- [ ] **ADR-Role v4 → v5 改訂 (Phase 5)**
- [ ] **registry 同期 (Phase 6)**
- [ ] **Stage 2 テストログテンプレート作成 (Phase 7 準備)**
- [ ] **Stage 2 テスト本番着手**

---

## 9. 関連リソース

### 本提言書の前提となるドキュメント

- `CLAUDE.md` v1.4 — Vault エントリポイント
- `wiki/STARTUP_CODES.md` v5 — 起動コード仕様
- `wiki/adr/ADR-Role.md` v4 — ロール権限・二系統管轄・Wiki-Rex 定義
- `wiki/adr/ADR-NLM.md` v2 — NLM 1:1 原則
- `wiki/adr/ADR-Vault.md` v1 — Vault 書込パス単一化原則
- `raw/ADVISOR_HANDOFF.md` (3 代目以前 Adviser 引き継ぎ書) — 世代継承体系

### 外部リソース

- mcp-obsidian (採用候補): https://github.com/MarkusPfundstein/mcp-obsidian
- Obsidian Local REST API plugin: https://github.com/coddingtonbear/obsidian-local-rest-api
- obsidian-claude-code-mcp (代替候補・温存): https://github.com/iansinnott/obsidian-claude-code-mcp
- obsidian-mcp-tools (採用不可・記録用): https://github.com/jacksteamdev/obsidian-mcp-tools

---

## 10. 改訂履歴

| 日付 | 版 | 起草者 | 主な変更 |
|---|---|---|---|
| 2026-04-30 | 初版 | 4 代目 Adviser (Claude Opus 4.7) | Wiki-Rex Stage 2 テスト用 Obsidian Plugin MCP 導入提言・Wiki-Eval 業務依頼書として起草 |

---

*4 代目 Adviser (Claude Opus 4.7) / 2026-04-30*
*管轄: ADR-Role v4 §0 ② により Wiki-Eval 直接実施事項*
*本提言書は提案であり、最終的な ADR 起草・改訂内容は Wiki-Eval の判断による*
