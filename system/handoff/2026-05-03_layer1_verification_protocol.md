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

*(本セクションは Boss 検証実施後に追記される。20 代目 Vault-Planner が結果を受けて代理追記する場合と、21 代目に追記を委ねる場合がある。判断はボスのセッション継続性に従う。)*

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

---

*起草: 20 代目 Wiki-Eval(初代 Vault-Planner 確定)/ Claude Opus 4.7 / 2026-05-03 / web client 経由*
*本書は Vault-Planner ロールが Default Rex に Layer 1 を「動作確証付き」で手渡すための道具立て*
*検証結果は §5 に追記され、§6 のアクション分岐に従って初代任期の完結 / 継続が決定する*
