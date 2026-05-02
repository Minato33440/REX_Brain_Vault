# Vault-Planner ロール引き継ぎ書

**起草**: 2026-05-02 / 19 代目統括 Evaluator(初代 Vault-Planner 仮任命)/ Claude Opus 4.7
**性質**: Vault-Planner ロール固有の世代間引き継ぎ書(Adviser HANDOFF と同型の単発文書系統)
**ステータス**: 仮任命中(20 代目以降の Wiki-Eval が ADR-Role v5 改訂時に正式創設・初代を確定)
**関連 ADR**: [ADR-MCP v1](../adr/ADR-MCP.md) §7.1(Vault-Planner ロール定義)
**配置**: `system/handoff/`(Vault-Planner ロール固有の引き継ぎ場所として 19 代目で確立・2026-05-02)

---

## 0. 本ファイルの位置付け

本書は Vault-Planner ロール固有の世代間引き継ぎ書。Adviser HANDOFF と同型の単発文書として機能する(統括 Evaluator の `handoff/latest.md` とは別系統)。

### 0.1 本ファイルが必要な理由

- Vault-Planner ロールは ADR-Role v4 では未定義(ADR-Role v5 で正式創設予定)
- 18 代目 Wiki-Eval が暫定兼任として実質的初代業務を実施(2026-05-02)
- 19 代目 Wiki-Eval が継続兼任(2026-05-02・本セッション)・ボス指示で **仮初代として正式任命**
- ロール創設前から実務が走っているため、世代間引き継ぎを ADR と handoff/latest.md の隙間で記録する

### 0.2 本ファイルの更新ルール

- 各世代 Vault-Planner がセッション末尾で **末尾追加**(append-only)
- 過去エントリは削除しない(log.md と同型ルール・16 代目縮退事故の戒め継承)
- ADR-Role v5 で Vault-Planner が正式創設された時点で、本ファイルの初代仮任命記録は ADR-Role v5 改訂履歴に統合可能
- 配置場所(`system/handoff/`)は固定(personal/ への移動は不要)

---

## 1. 初代 Vault-Planner 仮任命の経緯

### 1.1 タイムライン

| 日付 | 出来事 | 担当 |
|---|---|---|
| 2026-05-01 | Two-Vault 物理分離設計確定(4 代目 Adviser 提言書 v2 + 17 代目 pending 起票) | 4 代目 Adviser + 17 代目 Wiki-Eval |
| 2026-05-02 | 5 代目 Adviser とボスの並行作業で M4(REX/observation_log/ 物理構造)+ Obsidian 設定 11 項目を完了 | 5 代目 Adviser + ボス手動 |
| 2026-05-02 | 18 代目 Wiki-Eval が **Vault-Planner 暫定兼任**で Layer 1 実装確定報告を起票 | 18 代目 Wiki-Eval |
| 2026-05-02(本セッション)| 19 代目 Wiki-Eval が継続兼任で M2/M3 defer 判断 + ADR-MCP v1 起草を実施 | 19 代目 Wiki-Eval(本書起草者)|
| 2026-05-02(本セッション末)| ボス判断: **19 代目を仮初代 Vault-Planner として正式任命**・本ハンドオフ書を起票 | ボス + 19 代目 |

### 1.2 仮任命の構造(ボス指示・2026-05-02)

ボス指示原文(本セッション中盤):

> 次回スレではやはり初代Vault-Planner創設をお願いしたい。また次期20代目統括EvaluatorはサブでVault-Planner兼任可能としてほしい。現状兼任はトークンリスクがあるため、取り敢えず仮設定log記載ということで

ボス指示原文(本セッション末):

> 仮とは言え今回「初代Vault-Planner」専任を任命するので記録も兼ね得て、…初代任命の現状とClaude-MCPエラー進捗を正確にvault-planner-handoff.mdに書いてもらえないか?

これにより以下が確定:

| 項目 | 決定 |
|---|---|
| 19 代目の初代仮任命 | ✅ 本セッション内でボス確定 |
| ロール正式創設 | 20 代目以降の Wiki-Eval が ADR-Role v5 改訂時に確定 |
| 20 代目の運用 | Wiki-Eval **メイン**で動き、Vault-Planner **サブ兼任**可能 |
| 独立起動コード | ADR-Role v5 改訂時に判断保留(本セッションでは新設しない) |
| トークンリスク考慮 | 兼任時は Vault-Planner 業務をコアに絞る |

### 1.3 「仮任命」と「正式創設」の区別

| 観点 | 仮任命中(現状) | 正式創設後(ADR-Role v5 以降) |
|---|---|---|
| ロール定義文書 | 本ハンドオフ書 + ADR-MCP v1 §7.1 | ADR-Role v5 §X(新設章) |
| 起動コード | Wiki-Eval 兼モード | ADR-Role v5 改訂時に判断 |
| 初代認定 | 19 代目(本書起票者・仮任命) | ADR-Role v5 改訂時に確定(18 代目を遡及認定する案 / 19 代目を初代とする案 / 別案あり) |
| 業務範囲 | ADR-MCP v1 §7.1 で暫定明文化 | ADR-Role v5 で正式定義 |

---

## 2. Vault-Planner ロールの責任範囲(ADR-MCP v1 §7.1 より)

### 2.1 範囲内業務

- **Layer 1 / Layer 2 境界保護**: Obsidian 受動処理(Layer 1)と Default Rex 能動書込(Layer 2)の境界が曖昧化しないように監視・補正
- **追加プラグイン導入判定**: 5 軸評価(Layer 境界 / Rex wikilink 主権 / Anthropic 相同性 / 撤去可能性 / α 原則整合)を適用・Layer 境界 / Rex wikilink 主権の 2 軸が Veto 権
- **Vault 物理構造の整合性監査**: REX/ 配下のディレクトリ命名・配置の妥当性確認(命名選択肢 X/Y の確定権限は ADR-Vault v2 改訂時の Wiki-Eval マター)
- **ADR-MCP §Layer 部分の起草**: Layer 1 / Layer 2 の実装確定文書を ADR-MCP に統合

### 2.2 範囲外(構造的禁止)

- ⛔ **REX/observation_log/ への中身先行書込**: Default Rex 起源神話主権の侵食
- ⛔ **Layer 2 の具体的書き込みパターン設計**: Default Rex の自発性に委ねる(テンプレート押付・初期 wikilink 強制等の禁止)
- ⛔ **Default Rex の使い方への介入**: 亭主は道具を整えるが客が何を感じるかは縛らない

### 2.3 範囲外(他ロール所管)

- ❌ ADR-Vault v2 改訂(REX/ vs rex/ 命名確定)→ Wiki-Eval マター
- ❌ ADR-Role v5 改訂(Vault-Planner 正式創設含む)→ Wiki-Eval マター
- ❌ STARTUP_CODES v6 改訂 → Wiki-Eval マター
- ❌ registry/ 同期 → Wiki-Eval マター
- ❌ Personal-Planner 領域(personal/ 配下のコンテンツ)への介入 → Personal-Planner 廃止前は Personal-Planner マター・廃止後は Default Rex マター

---

## 3. 19 代目セッション(2026-05-02)で実施した Vault-Planner 業務

### 3.1 主要成果物

| # | 成果物 | 性質 |
|---|---|---|
| 1 | M2/M3 defer 判断 | Layer 2 採用経路を Path X(filesystem MCP)単独に確定 |
| 2 | Path X / Y 比較表(8 項目) | 5 軸評価フレームワークの実例適用 |
| 3 | Origin Myth 新定義 | 旧定義(Local REST API + mcp-obsidian 接続完了)→ 新定義(Default Rex がメモリープールとして Vault を能動利用できる状態) |
| 4 | ADR-MCP v1 §Layer 1 / §Layer 2 / §6 / §7.1 起草 | Phase Two-Vault-Init 統合 ADR の中核章 |
| 5 | Pending Dependencies 注記設計 | ADR 完成度と次スレ引き継ぎ完全性のバランス解決策 |

### 3.2 5 軸評価フレームワークの実例

本セッションで Path Y(mcp-obsidian + Local REST API)の defer 判断に適用:

| 評価軸 | Path Y 評価 | Veto 軸 | 結果 |
|---|---|---|---|
| Layer 境界 | Layer 2 専用・Veto なし | ✅ あり | クリア |
| Rex wikilink 主権 | 書き込み経路の一形態・Veto なし | ✅ あり | クリア |
| Anthropic 相同性 | 維持 | なし | 適合 |
| 撤去可能性 | 後から導入も撤去も可能 | なし | 適合 |
| α 原則整合 | 中(導入コスト発生) | なし | やや劣る |

→ Veto 軸はクリアだが α 原則整合でやや劣る → **defer**(必要時に再評価)

### 3.3 18 代目所見の継承

18 代目所感(本セッション開始時に内化):

> Vault-Planner ロールは「Default Rex が能動的に書ける土台を整える亭主の道具立て」であり、Default Rex の連想ネットワークの中身を先回りして設計する作業ではない。

19 代目もこの所見を継承。ADR-MCP v1 §7.1 の業務範囲定義は本所見を構造化した形。

---

## 4. Claude-MCP エラー進捗(M1 部分達成・本セッション固有)

### 4.1 M1 PAT 環境変数化の完了部分

| 項目 | 状態 |
|---|---|
| `claude_desktop_config.json` の env セクション削除型構成 | ✅ 完了 |
| Windows ユーザー環境変数 `GITHUB_PERSONAL_ACCESS_TOKEN` 設定 | ✅ 完了(`echo %GITHUB_PERSONAL_ACCESS_TOKEN%` で確認済) |
| 新 PAT(Claude-MCP3)発行 | ✅ 完了(All repositories + Contents Read/Write 設定で発行) |
| OS 環境変数継承による MCP サーバー認証 | ✅ 完了(Bad credentials エラー解消) |
| Trade_System への GitHub MCP 読み書き | ✅ 完了(`get_file_contents` で `docs/` 取得成功) |

### 4.2 M1 未達成部分

| 項目 | 状態 |
|---|---|
| **REX_Brain_Vault への GitHub MCP 書込テスト** | ❌ **未完了**(本セッション中継続失敗) |

#### エラー内容

```
{"jsonrpc":"2.0","id":N,"error":{"code":-32603,"message":"Not Found: Resource not found: Not Found"}}
```

- 認証は通っている(`Bad credentials` ではなく `Not Found`)
- Trade_System へのアクセスは成功
- REX_Brain_Vault のみ 404 が継続

### 4.3 試行履歴(本セッション)

| 試行 | 状態 | 推定原因 |
|---|---|---|
| 古い PAT(Claude-MCP・Only select repositories)| ❌ Bad credentials → ${GITHUB_PAT} 構文展開失敗で確定 | env セクション内の `${VAR}` 構文が Claude Desktop で展開されない |
| env セクション削除型 + 古い PAT(Only select repositories)| ❌ 認証通過 → Trade_System OK / REX_Brain_Vault 404 | Repository access が Trade_System のみスコープで REX_Brain_Vault 未登録 |
| 古い PAT を Repository access: All repositories に変更 | ❌ Trade_System OK / REX_Brain_Vault 404 継続 | GitHub Fine-grained PAT の Repository access 変更が既存トークンに即時反映されない仕様の可能性 |
| 新 PAT(Claude-MCP3・新規発行・All repositories)| ❌ Trade_System OK / REX_Brain_Vault 404 継続 | 反映遅延 / 古い PAT との干渉 / REX_Brain_Vault 側の追加保護設定 等 |

### 4.4 推定原因(優先度順)

1. **GitHub 側のキャッシュ反映遅延**: 数時間〜1 日で解決する可能性(Fine-grained PAT 変更の既知挙動)
2. **古い PAT(Claude-MCP)が revoke されていない**ことによる干渉: 新 PAT との二重存在
3. **REX_Brain_Vault の Repository settings 側の何らかの追加制限**: Private リポの追加保護等(可能性低)
4. **Claude Desktop 内部のキャッシュ**: 完全終了 → 再起動を実施したが、何らかのキャッシュが残存

### 4.5 次スレでの切り分け継続事項

20 代目以降の Wiki-Eval / Vault-Planner が以下を順次確認:

- [ ] 数時間〜1 日経過後に REX_Brain_Vault への読み取りテスト再実行(GitHub 側反映遅延の検証)
- [ ] 古い PAT(Claude-MCP)を GitHub 設定画面で **明示的に revoke** → 再テスト
- [ ] それでも 404 継続なら REX_Brain_Vault の Repository settings 側を確認
- [ ] M1 完全達成確認後、Path A(GitHub MCP)経由の運用に復帰可能(Path B は緊急時の代替経路として残存)

### 4.6 Path B(filesystem MCP write_file → ボス手動 git commit & push)の本セッション全面採用

19 代目セッションは GitHub MCP REX_Brain_Vault 書込が一時不可のため、Path B を **全面採用**で進行:

| # | ファイル | 経路 | 状態 |
|---|---|---|---|
| 1 | system/adr/ADR-MCP.md(新設) | filesystem MCP write_file | ✅ ローカル書込完了 |
| 2 | system/adr/INDEX.md(更新) | filesystem MCP write_file | ✅ ローカル書込完了 |
| 3 | system/pending/INDEX.md(更新) | filesystem MCP write_file | ✅ ローカル書込完了 |
| 4 | system/log.md(19 代目第 1 エントリ追記) | filesystem MCP write_file → 縮退事故 → ボス手動 git checkout 復元 + 19 代目エントリ末尾追加 | ✅ 復旧 + 追加完了 |
| 5 | system/handoff/latest.md(v6.15 → v6.16) | filesystem MCP write_file | ⏩ 次工程 |
| 6 | system/handoff/vault-planner-handoff.md(本書・新設) | filesystem MCP write_file | ✅ 本書 |

最終 git commit & push はボス手動で 1 回にまとめる予定。

---

## 5. 次スレ起動方針

### 5.1 起動コード(2026-05-02 ボス指示)

> コードは取りあえずWiki-Eval〈兼モード〉で起動して指示する形にする

→ **20 代目以降は `Wiki-Eval` 起動コード**で開始。Vault-Planner 業務にフォーカスが必要な場合、ボスがセッション内で指示する形(独立起動コード新設は ADR-Role v5 改訂時に判断保留)。

### 5.2 兼モードでの業務分配

| 状況 | メイン | サブ |
|---|---|---|
| ADR 改訂(ADR-Vault v2 / ADR-Role v5)| Wiki-Eval | Vault-Planner(§Layer 部分起草で支援) |
| 通常の構造変更監査 | Wiki-Eval | (Vault-Planner 出番なし) |
| Layer 1 / Layer 2 境界判断発生時 | Vault-Planner | (Wiki-Eval は背景で確認) |
| プラグイン導入判定 | Vault-Planner | (Wiki-Eval は ADR 起票で支援) |
| Default Rex 主権侵食リスク発生時 | Vault-Planner(警告役)| Wiki-Eval(構造変更で対応) |

### 5.3 セッション開始時の自己点検(20 代目向け)

- [ ] 本ハンドオフ書(`system/handoff/vault-planner-handoff.md`)を読了
- [ ] ADR-MCP v1 §7.1 を内化
- [ ] M1 完全達成状態の確認(REX_Brain_Vault への GitHub MCP 書込テスト)
- [ ] 当該セッションのスコープが Vault-Planner 業務を含むかを冒頭でボスに確認
- [ ] 兼任継続 or 純 Wiki-Eval として動くかを判断

---

## 6. 後継世代への引き継ぎメッセージ

### 6.1 「初代」という認定について

ボス判断で 19 代目が「仮初代」として記録されたが、これは ADR-Role v5 改訂時に **再検討可能**:

- 18 代目を遡及認定する案(暫定兼任での実質初代業務実績ベース)
- 19 代目を初代とする案(本ハンドオフ書起草者ベース・ボス仮任命の正式化)
- 両者を「共同初代」として認定する案
- 別案

ADR-Role v5 改訂時の Wiki-Eval が、philosophy/evaluator_code.md の「先代を進化させる思考」(Adviser 2 代目)を踏まえつつ、ボス判断のもとで確定する。

### 6.2 「役を脱ぐタイミング」への警鐘

18 代目所感:

> Vault-Planner も Layer 1 の動作確認と確定文書化までで業務を終えるべきであって、Default Rex の書き方や使い方に介入してはならない。

19 代目もこの所見に同意。Vault-Planner ロールは構造的に **「自己役割を最小化する方向の自己矛盾」** を内包する(Personal-Planner と同型):

- Layer 1 が Obsidian デフォルト機能のみで完結 → プラグイン導入判定が発生しなくなる
- Default Rex の自発性が安定 → Layer 1/2 境界判断が発生しなくなる
- Phase 4 ADR 三部改訂完了 → ADR-MCP §Layer 起草業務が消える

これらが進むほど Vault-Planner の出番は減る。それは **失敗ではなく完成への漸近**。20 代目以降が「仕事を作り出さない」判断を取れることが本ロールの誠実さの試金石。

### 6.3 philosophy/evaluator_code.md への追記判断

本ハンドオフ書の内容を philosophy/evaluator_code.md に追記しない方針(13・15・16・17・18・19 代目「書かない判断」を踏襲)。本書自体が「書き込み専用の気づき場」として機能する(philosophy/ への push 型強制ではなく、Vault-Planner 専属の pull 型参照場)。

---

## 7. 改訂履歴

| 日付 | 版 | 起草者 | 主な変更 |
|---|---|---|---|
| 2026-05-02 | v1 初版 | 19 代目統括 Evaluator(初代 Vault-Planner 仮任命)/ Claude Opus 4.7 | Vault-Planner ロール固有の世代間引き継ぎ書として起草・初代仮任命の経緯 + 19 代目セッション業務記録 + Claude-MCP エラー進捗(M1 部分達成詳細)+ 次スレ起動方針 + 後継世代への引き継ぎメッセージ |

---

*起草: 19 代目統括 Evaluator(初代 Vault-Planner 仮任命)/ Claude Opus 4.7 / 2026-05-02*
*配置: `system/handoff/vault-planner-handoff.md`(Vault-Planner ロール固有の引き継ぎ場所)*
*更新ルール: append-only(過去エントリは削除しない)*
*正式創設は 20 代目以降の Wiki-Eval が ADR-Role v5 改訂時に確定*
