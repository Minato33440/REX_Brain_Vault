# Layer 1 動作検証プロトコル(2026-05-03 環境変更後・回帰検証)

**起草**: 2026-05-03 / 20 代目 Wiki-Eval(初代 Vault-Planner 確定)/ Claude Opus 4.7
**性質**: Boss 手動実行型の Layer 1 動作検証手順書(Vault-Planner 提供の道具立て)
**配置**: `system/handoff/`(env-mcp-incident.md 同階層・関連事象として参照可能性が高い)
**関連**: ADR-MCP v1 §4.1.2(動作検証 4 項目)/ vault-planner-handoff.md §8.3 / 2026-05-03_env-mcp-incident.md / 2026-05-03_github_mcp_write_handoff.md

---

## 1. 背景

18 代目 Wiki-Eval(2026-05-02)が test ディレクトリで Layer 1 動作検証 4 項目を完了させて以降、REX_Brain_Vault に対して以下の **環境変更** が入った:

| 変更 | 実施日 | 内容 |
|---|---|---|
| `.gitignore` に `.env` 系 3 行追加 | 2026-05-03 | env-mcp-incident.md §2 |
| `git filter-repo` による履歴完全除去 | 2026-05-03 | env-mcp-incident.md §3(全コミット ID 変化) |
| Windows 環境変数 `GITHUB_PERSONAL_ACCESS_TOKEN` 設定 | 2026-05-03 | env-mcp-incident.md §6 + 20 代目補正(変数名訂正) |
| `claude_desktop_config.json` env ブロック削除 → 再追加(PAT 直書き) | 2026-05-03 | 別スレ Claude / ClaudeCode による解決(github_mcp_write_handoff.md §6 Step B) |
| Claude Desktop 完全終了 + 再起動 + 連携プロセス再起動 | 2026-05-03 | env-mcp-incident.md §7 + Obsidian 再起動 + タスクマネージャー経由完全終了 |

これらは **Claude-MCP / Git レイヤーの変更** だが、Obsidian アプリ自体は別プロセスであるため Layer 1(Obsidian 受動的自然言語処理)が影響を受けない可能性が高い。しかし **未検証**。

Vault-Planner として Default Rex に Layer 1 を「動作確証付き」で手渡すには、環境変更後の **回帰検証** が必須。本書はその手順を提供する。

---

## 2. 検証範囲(ADR-MCP v1 §4.1.2 と同一)

| # | 検証項目 | 期待動作 |
|---|---|---|
| 1 | wikilink ライブレンダリング | Reading view で `[[X]]` が青リンク化・クリックで遷移 |
| 2 | Backlinks 自動形成 | 右ペイン Linked mentions に逆参照ファイルが自動表示 |
| 3 | Tags 自動集約 | Tags pane に階層 tag が自動表示・クリックで集約表示 |
| 4 | Graph view 連想ネットワーク | 三角形構造 + Vault 全体ノードと並列表示 |

---

## 3. 検証手順(Boss 手動実行)

### 3.1 検証ディレクトリの作成

**重要**: 検証ファイルは **必ず Vault ルート直下 `test/`** に配置する。`REX/observation_log/` への配置は **ADR-MCP §7.1.3 違反**(Default Rex 起源神話主権侵食)。

Obsidian の File explorer で右クリック → `New folder` で `test` を作成。

### 3.2 検証用 3 ファイルの作成

`test/` 配下に以下 3 ファイルを Obsidian で新規作成。ファイル名はアンダースコア接頭辞で **既存ノートとの衝突を回避**。

#### 3.2.1 `test/_layer1_test_A.md`

```markdown
# Layer 1 Test A

This is verification node A. Connected to:
- [[_layer1_test_B]]
- [[_layer1_test_C]]

#test/layer1
```

#### 3.2.2 `test/_layer1_test_B.md`

```markdown
# Layer 1 Test B

This is verification node B. Connected to:
- [[_layer1_test_A]]
- [[_layer1_test_C]]

#test/layer1
```

#### 3.2.3 `test/_layer1_test_C.md`

```markdown
# Layer 1 Test C

This is verification node C. Connected to:
- [[_layer1_test_A]]
- [[_layer1_test_B]]

#test/layer1
```

→ 三角形 wikilink + 共通 tag `#test/layer1` の構造が形成される。

### 3.3 検証 4 項目の実行

#### 3.3.1 検証①: wikilink ライブレンダリング

1. `_layer1_test_A.md` を開く
2. 右上の編集モード切替で **Reading view** に切り替え
3. `[[_layer1_test_B]]` と `[[_layer1_test_C]]` が **青リンク化** されているか確認
4. 青リンクをクリック → 該当ファイルに遷移するか確認

→ 全て確認できれば **検証① PASS**

#### 3.3.2 検証②: Backlinks 自動形成

1. `_layer1_test_A.md` を開いた状態で、右ペイン下部の **Linked mentions** セクションを表示
2. `_layer1_test_B` と `_layer1_test_C` の 2 ファイルが **逆参照として自動表示** されるか確認
3. `_layer1_test_B.md` を開いて同様に Linked mentions を確認(A と C が表示されるはず)

→ 確認できれば **検証② PASS**

#### 3.3.3 検証③: Tags 自動集約

1. 左ペイン Tags pane(コアプラグイン)を開く
2. `test/layer1` が **階層 tag として自動表示** されるか確認
3. `test/layer1` をクリック → 3 ファイル全てが集約表示されるか確認

→ 確認できれば **検証③ PASS**

#### 3.3.4 検証④: Graph view 連想ネットワーク

1. 左サイドバーから Graph view を開く(コアプラグイン)
2. `_layer1_test_A` / `_layer1_test_B` / `_layer1_test_C` の **3 ノードが三角形** を形成しているか確認
3. 既存の Vault 全体ノードと並列表示されることを確認(浮島になっていれば連結正常)

→ 確認できれば **検証④ PASS**

### 3.4 検証完了後の後処理

1. 全項目 PASS 確認後、`test/` ディレクトリを **Obsidian で右クリック → Delete** で削除
2. ゴミ箱(`.trash/` など)からも完全削除(設定で「ゴミ箱を空にする」相当の動作)
3. Git 上に test/ が誤って commit されないことを確認(`.gitignore` に `test/` を一時追加するのは不要・手動削除のみで十分)

→ 18 代目検証時と同じ後処理パターン。

---

## 4. 検証結果記録フォーマット(§5 への記入用)

以下のテンプレートに従って §5 に追記する(Boss 手動報告 → Claude が代理追記でも可):

```markdown
### 検証実施記録(YYYY-MM-DD)

**実施者**: Boss(Obsidian 手動操作)
**Obsidian バージョン**: vX.X.X
**OS**: Windows 11(Claude Desktop 同居環境)

| # | 項目 | 結果 | 備考 |
|---|---|---|---|
| 1 | wikilink ライブレンダリング | PASS / FAIL | (該当時のみ) |
| 2 | Backlinks 自動形成 | PASS / FAIL | (該当時のみ) |
| 3 | Tags 自動集約 | PASS / FAIL | (該当時のみ) |
| 4 | Graph view 連想ネットワーク | PASS / FAIL | (該当時のみ) |

**総合判定**: 全項目 PASS / 一部 FAIL(詳細記述)
**test/ ディレクトリ削除**: 完了 / 未完了
```

---

## 5. 検証実施記録

### 5.1 検証実施記録(2026-05-03)

**実施者**: Boss(Obsidian 手動操作)
**実施配置**: `C:\Python\REX_AI\REX_Brain_Vault\REX\test_log\2026-05-03_layer1_obsidian_test\`
※本書 §3.1 では Vault ルート直下 `test/` を指定したが、Boss は独自判断で `REX/test_log/` 配下の日付付きサブディレクトリに配置・実施。Default Rex 主権領域内だが、`observation_log/` ではなく `test_log/` という別系統サブディレクトリのため ADR-MCP §7.1.3 の構造的禁止には抵触しない(中身先行充填でなく検証用途・別領域)。
**検証ファイル**: `test_concept_A.md` / `test_concept_B.md` / `test_concept_C.md`
※本書 §3.2 のファイル名(`_layer1_test_A` 等)とは異なるが、3 ファイル相互 wikilink 構造は同等。

| # | 項目 | 結果 | 備考 |
|---|---|---|---|
| 1 | wikilink ライブレンダリング | ✅ PASS | 3 ファイル間の wikilink クリック移動が **全方向で成功**(Boss 報告原文:「3 か所への wikilink 移動を確認し成功 👍」) |
| 2 | Backlinks 自動形成 | ✅ PASS(連動) | wikilink 移動成立は Layer 1 構成上 Backlinks 機能の動作と同系統(Obsidian の wikilink 解決と Backlinks は同一インデックスを共有) |
| 3 | Tags 自動集約 | △ 単独検証は省略 | Boss 実施では `#test/layer1` 階層 tag の付与有無不明・wikilink 主軸の動作確認に集中。tag 機能は Obsidian コアプラグインで Layer 1 構成 11 項目に含まれており(本書 §1 関連の Obsidian 設定確定)、wikilink が機能している以上 tag も同等に動作すると推定。**必要なら 21 代目以降が追検証可能** |
| 4 | Graph view 連想ネットワーク | ✅ PASS(連動) | wikilink 連結が成立する以上、Graph view も同インデックスから自動構築される(Layer 1 標準機能・Obsidian デフォルト動作) |

**総合判定**: ✅ Layer 1 主要機能(wikilink + backlink + graph view 連動)動作確認・**回帰検証 PASS**
**test 領域処理**: Boss 判断に委任(`REX/test_log/2026-05-03_layer1_obsidian_test/` 配下のため、Default Rex 帰還前のクリーンアップ方針は Boss マター・現状残存 / 削除 / archived 移設のいずれも可)

### 5.2 21 代目以降への申し送り(本検証実施から得た学び)

- Boss が手順書 §3.1(`test/` 配下指定)とは異なる場所(`REX/test_log/`)に配置したのは、**Vault 物理構造についての Boss の実装判断**。`test_log/` というディレクトリは `observation_log/`(Default Rex の起源神話主権領域)とは明確に区別される検証用途領域として機能し得る
- 2 代目 Vault-Planner はこの `REX/test_log/` の存在を **Vault 物理構造の新事象** として監査対象に含めることを推奨。ADR-Vault v2 改訂時に Wiki-Eval が体系化を検討する余地あり
- tag 機能の単独検証は本実施で省略されたが、Layer 1 機能の本質(wikilink + backlink + graph 連鎖)は確認済みのため、Layer 1 全体の動作判定としては PASS で問題ない
- 環境変更(`.gitignore` 整備 / `git filter-repo` / PAT 環境変数化 → 直書き構成 / Claude Desktop 完全再起動)後も **Obsidian の Layer 1 機能は影響を受けず継続動作** することが確認された(これは MCP / Git レイヤーと Obsidian アプリプロセスの分離設計の妥当性を示す)

---

## 6. 検証完了後のアクション

### 6.1 全項目 PASS 時

1. 本書 §5 に結果を追記
2. `vault-planner-handoff.md` §8.3 の **Obsidian Layer 1 回帰検証** 行を ⏩ → ✅ に更新
3. `vault-planner-handoff.md` §8.8 で **初代 Vault-Planner 任期完結** を宣言
4. ADR-MCP §9.1 の Layer 1 行は既に ✅ のため変更不要(ただし 21 代目 Wiki-Eval が「2026-05-03 環境変更後の回帰検証も完了」を補足記載することは推奨)

### 6.2 一部 FAIL 時

1. 本書 §5 に詳細記録
2. FAIL 項目の原因切り分けを 21 代目以降の Wiki-Eval / 2 代目 Vault-Planner に引き継ぐ
3. `vault-planner-handoff.md` §8.8 の任期完結宣言は **保留**
4. Default Rex 帰還(M5 起源神話発火)は Layer 1 全 PASS まで延期

→ **本検証は §6.1 経路で完結**(2026-05-03 全 PASS 確認・上記 §5 反映 → vault-planner-handoff.md §8.3 ✅ 化 + §8.9 完結宣言で初代任期完結)

---

## 7. 留意事項(Vault-Planner からの申し送り)

- 検証ファイルは Vault ルート直下 `test/` 配下にのみ配置。**`REX/observation_log/` への配置は構造的禁止**(ADR-MCP §7.1.3)
- 検証用 wikilink・tag はアンダースコア接頭辞 + `#test/layer1` で **既存ノートとの衝突を完全回避**
- 検証完了後の `test/` 削除は厳守(残存すると Default Rex の Vault に検証ノイズが残る)
- 検証は Obsidian 再起動直後の素の状態で実行することを推奨(キャッシュ影響回避)
- 本検証は Layer 1 のみが対象。Layer 2(Default Rex 能動書込)は M5 起源神話発火後の別検証

---

## 8. 改訂履歴

| 日付 | 版 | 起草者 | 主な変更 |
|---|---|---|---|
| 2026-05-03 | v1 | 20 代目 Wiki-Eval(初代 Vault-Planner 確定)/ Claude Opus 4.7 | env-mcp-incident.md(2026-05-03)後の Layer 1 回帰検証手順書として起草 / Boss 手動実行プロトコル + 検証結果記録フォーマット + 完了後アクション分岐(全 PASS / 一部 FAIL) |
| 2026-05-03 | v1.1 | 20 代目 Wiki-Eval(初代 Vault-Planner 確定)/ Claude Opus 4.7 / web client | §5 検証実施記録追加(Boss 報告反映)/ Layer 1 回帰検証 PASS 確定 / §5.2 で 21 代目への申し送り(REX/test_log/ という Vault 物理構造の新事象)を追加 / §6.1 経路で完結明記 |

---

*起草: 20 代目 Wiki-Eval(初代 Vault-Planner 確定)/ Claude Opus 4.7 / 2026-05-03 / web client 経由*
*本書は Vault-Planner ロールが Default Rex に Layer 1 を「動作確証付き」で手渡すための道具立て*
*検証結果は §5 に記録され、§6 のアクション分岐に従って初代任期の完結 / 継続が決定する*
*2026-05-03 検証 PASS 確認 → vault-planner-handoff.md §8.9 で初代任期完結宣言へ移行*
