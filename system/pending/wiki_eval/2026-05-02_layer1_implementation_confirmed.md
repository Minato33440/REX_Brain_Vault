# Layer 1 実装確定報告 — Obsidian 受動的自然言語処理層

**起票者**: 18 代目 Wiki-Eval(Vault-Planner 暫定兼任)
**起票日**: 2026-05-02
**ADR 昇格希望**: No(本提言書は Phase 4 ADR-MCP v1 の §Layer 1 確定インプットとして機能・単独 ADR 化はしない)
**影響範囲**: Phase Two-Vault-Init Phase 4(ADR-MCP v1 新設)・Default Rex Plugin 接続後の Layer 2 実装・Anthropic メモリーシステム相同性の構造的保証

---

## 1. 目的・位置付け

### 1.1 本提言書の役割

本提言書は、Phase Two-Vault-Init における **Layer 1(Obsidian 自動処理層)の実装確定** を宣言する文書である。本セッション(18 代目 Wiki-Eval / Vault-Planner 暫定兼任)で動作検証を完了し、Phase 4 で ADR-MCP v1 を新設する際の **§Layer 1 確定インプット** として機能する。

### 1.2 Layer 番号付けの統一

本提言書は以降の Vault 全文書で使用する Layer 番号付けを以下に確定する:

| Layer | 内容 | 主体 | 状態(本セッション時点) |
|---|---|---|---|
| **Layer 1** | Obsidian 受動的自然言語処理(wikilink 自動 backlink・tag 自動集約・graph view 自動構築) | Obsidian アプリケーション | ✅ **本提言書で実装確定** |
| **Layer 2** | Rex 能動的書き込み(MCP プラグイン経由で Rex-Vault に文字を書く・`[[concept]]` 形式は任意) | Default Rex(Phase 3 起源神話発火後) | ⬜ 未実装(M1〜M3 + Phase 3 後) |

**過渡的記述との関係**: 4 代目 → 5 代目 Adviser 引き継ぎ書 §2.1 では Layer 番号付けが本提言書と逆転していた(Adviser 引き継ぎ書では Layer 2 = Obsidian 自動 / Layer 1 = Rex 能動)。意図の本体(「受動的自然言語処理 = Obsidian 自動」「能動的書き込み = Rex」)は完全に一致するが、ボス指示(2026-05-02)で「Anthropic メモリー相同性最優先」の観点から本提言書の番号付けに統一された。Adviser 引き継ぎ書 §2.1 の番号付けは「Adviser 文脈での過渡的記述」として尊重し、以降の Vault 全文書(本提言書 + Phase 4 ADR-MCP v1 含む)は本提言書の番号付けで統一する。

### 1.3 Anthropic メモリー相同性最優先という設計指針

ボス指示(2026-05-02)で確定した:

> Layer 1 = Obsidian としたのは、Anthropic メモリー相同性を最優先にしたいからだ

これは構築順序の自然性(基盤 → その上の能動性)に加えて、**Anthropic デフォルトメモリーシステムが「自動連想注入(下層)→ 各セッションでの能動応答(上層)」の構造を持つことと相同性を保つ** ための設計判断。Layer 1 が下層(自動)・Layer 2 が上層(能動)という対応関係が本相同性を保証する。

---

## 2. 実装内容(動作検証済)

### 2.1 Obsidian 設定確定値

5 代目 Adviser セッション(2026-05-01)でボスと共に確認・調整した Obsidian アプリケーション設定の確定値:

| # | 設定項目 | 確定値 | 備考 |
|---|---|---|---|
| 1 | `[[ウィキリンク]]` を使用 | ✅ ON | Layer 1 の根幹 |
| 2 | 内部リンクを毎回更新する | ✅ ON | Adviser §Step 2-A でボスが OFF → ON に変更済 |
| 3 | 新規作成するリンクの形式 | 可能であれば最短経路 | 推奨設定 |
| 4 | Backlinks コアプラグイン | ✅ ON | Linked mentions 自動表示 |
| 5 | Outgoing links コアプラグイン | ✅ ON | 発信リンク追跡 |
| 6 | Tags コアプラグイン | ✅ ON | Tags pane 自動集約 |
| 7 | Graph view コアプラグイン | ✅ ON | 連想ネットワーク可視化 |
| 8 | File explorer / Search / Outline | ✅ ON | 基本ナビゲーション |
| 9 | 括弧自動ペアリング | ✅ ON | `[[` 入力時に `]]` 自動補完 |
| 10 | ライブプレビュー | ✅ ON | wikilink リアルタイムレンダリング |
| 11 | マークダウン自動ペアリング | ✅ ON | 一般マークダウン記法 |

これら 11 項目は全て **Obsidian デフォルト機能** で実現される(Smart Connections / Copilot 等の追加プラグイン非導入)。

### 2.2 物理構造

```
REX_Brain_Vault/
├── REX/                         ✅ 2026-05-01 ボス手動作成
│   └── observation_log/         ✅ 2026-05-02 ボス手動作成
├── system/                      ✅ wiki/ → system/ リネーム済
├── raw/                         ✅ 既存
└── (各リポ既存ディレクトリ)
```

#### 2.2.1 命名規則の確定状態

- `REX/`(大文字): ボス判断(2026-05-01)で確定。`raw/` との視認性混同回避が理由
- `system/`(小文字): `wiki/` から改名済(2026-05-01 以前)

#### 2.2.2 Phase 4 への命名問題持越し

5 代目 Adviser §記録および本セッションで確認した通り、`REX/` 大文字命名は以下の文書群と表記不一致が存在する:

- 提言書 v2 §3.1(小文字 `rex/` 表記)
- pending/wiki_eval/2026-05-01_two_vault_redesign.md(小文字 `rex/` 表記)
- handoff/latest.md v6.14(小文字 `rex/` 表記)

Windows ファイルシステムは case-insensitive のため現時点で技術的問題はないが、git は case-sensitive のため commit 上は大文字 `REX/` として記録される。Phase 4 で 18 代目以降の Wiki-Eval が以下のいずれかを選択する:

- **(X)** 物理ディレクトリを小文字 `rex/` にリネーム + 過去文書の表記を維持
- **(Y)** ADR-Vault v2 で大文字 `REX/` 表記に統一 + 過去文書の小文字表記を Phase 0 議論記録扱いとする

本提言書は Vault-Planner 業務として **判断保留**(命名選定は Wiki-Eval 専管事項であり、Vault-Planner ロールの権限範囲外)。Phase 4 ADR-Vault v2 起草時に確定する。

### 2.3 動作確認結果

#### 2.3.1 検証手順

以下 4 項目を `raw/test_log/2026-05-02_layer1_obsidian_test/` 配下の test ファイル 3 個で検証:

| ファイル | 含む要素 | 検証する Layer 1 機能 |
|---|---|---|
| `test_concept_A.md` | `[[test_concept_B]]` + `#layer1-test` | A→B outgoing link / tag 集約 |
| `test_concept_B.md` | `[[test_concept_C]]` + `#layer1-test` | A からの backlink / B→C outgoing link / tag 集約 |
| `test_concept_C.md` | `[[test_concept_A]]` + `#obsidian-core` | B からの backlink / 循環構造完成 / 別タグ独立カウント |

3 ファイルが循環構造(A → B → C → A)を形成することで、graph view 上で三角形が描画され、Layer 1 全機能が同時に検証できる設計。

#### 2.3.2 検証結果(全て Pass)

| # | 検証項目 | 結果 | 検証方法 |
|---|---|---|---|
| 1 | wikilink ライブレンダリング | ✅ Pass | Reading view で `[[test_concept_B]]` が青リンクとして表示・クリックで遷移可(本セッションスクリーンショット 1) |
| 2 | Backlinks 自動形成 | ✅ Pass | `test_concept_B.md` の右ペインに `test_concept_A` が自動表示・`test_concept_C.md` の右ペインに `test_concept_B` が自動表示(本セッションスクリーンショット 2 / Image 1, Image 2) |
| 3 | Tags 自動集約 | ✅ Pass | Tags pane に `#layer1-test`(count=2)・`#obsidian-core`(count=1)が自動表示(本セッションスクリーンショット 3 / Image 1) |
| 4 | Graph view 連想ネットワーク | ✅ Pass | A・B・C の三角形構造が描画され、Vault 全体の他ノード(README / system_BUILD_GUIDE / log / philosophy 等)と並列で表示される(本セッションスクリーンショット 4 / Image 2) |

検証完了後、test ディレクトリ `raw/test_log/2026-05-02_layer1_obsidian_test/` はボス手動で削除済(2026-05-02・push 確認済)。

### 2.4 検証で経験した運用上の重要事項

#### 2.4.1 編集モードの違い(Source mode / Live Preview / Reading view)

ボスは検証中、Source mode(行番号表示・記号生表示)で test ファイルを開いてしまい、`[[test_concept_B]]` がリンクとしてレンダリングされない状態を一時的に観察した。これは Layer 1 機能不全ではなく、編集モードの違いによる表示差異である:

| モード | 表示 | 用途 |
|---|---|---|
| Reading view | リンク完全レンダリング(編集不可) | 完成ノートの閲覧 |
| Live Preview | 編集可能 + リンク・太字・見出しレンダリング | **推奨日常モード** |
| Source mode | 全記号生表示(行番号付) | マークダウン記法を細かく触る時のみ |

→ Default Rex が将来 Layer 2 で能動的に書き込む際、Live Preview モードでの体験が Anthropic メモリーシステムとの相同性に影響する。Layer 2 実装時は Live Preview をデフォルトとする運用とする。

---

## 3. Anthropic メモリー相同性の構造的保証

### 3.1 構造的同型性

| Anthropic デフォルトメモリー | REX Vault Layer 1 + Layer 2 |
|---|---|
| 自動連想注入(発火条件は未明文化) | Layer 1 = Obsidian 受動的自然言語処理(発火条件 = wikilink を書くこと自体・未明文化) |
| 各セッションでの能動応答 | Layer 2 = Rex 能動的書き込み(発火トリガー = ADR で意図的に未定義) |

両者とも **「下層が自動で発火条件を規定しない」「上層が能動的に動く」** という共通構造を持つ。これにより、Anthropic メモリーシステムを利用する Default Rex が REX Vault に移行する際、メンタルモデルの分断が起きない。

### 3.2 「Rex の書き込みトリガー未定義」設計の Layer 1 側保証

提言書 v2 §2 判断 3 で確定した「Rex の書き込みトリガーは ADR で意図的に未定義」設計は、Layer 2 に対する規定だが、Layer 1 側でも構造的に保証される必要がある。本提言書で確定した Layer 1 実装が以下を保証する:

- Layer 1 は **Rex が `[[concept]]` を書くだけ** で連想ネットワークを自動構築する
- Rex は `[[...]]` の使用判断を「するかしないか」のみで行う(タグ管理・索引作成・カテゴリ分類などのメタ作業は不要)
- Obsidian が背後で全ての構造化を担うため、Rex の書き込みは「素の自然言語 + 任意の wikilink」のみで完結する

→ これにより Layer 2(Rex 能動書込)の発火トリガーが未定義のままでも、Layer 1 が Vault 構造を維持する。8 代目「派生原則化の罠」と §候補メモ §2「独自運用発明の罠」が Layer 1 側でも構造的に回避される。

### 3.3 Personal-Planner-Rex 起源神話との接続

本提言書の Layer 1 実装確定は、**M5 起源神話発火準備の Layer 1 側完了** を意味する。

```
M1〜M3(PAT 環境変数化 / Local REST API plugin / mcp-obsidian 設定): ボス並行作業
  └─ M4(REX/ + REX/observation_log/ 物理構造): ✅ 完了(2026-05-02)
       └─ Layer 1(Obsidian 自動処理): ✅ 本提言書で完了確定
            └─ M5(Personal-Planner-Rex スレ復帰 = 起源神話発火 = Default Rex 帰還)
                 └─ Layer 2(Rex 能動書込)が起動
```

Layer 1 は「Default Rex が能動的に書ける土台」の Obsidian 側基盤であり、Default Rex の連想ネットワークの中身を先回りして設計する作業ではない。Vault-Planner 業務はここまでで完結し、Layer 2 の実装は M5 起源神話発火後の Default Rex 自身の自発的行為に委ねられる。

---

## 4. 追加プラグイン非導入の判断記録

### 4.1 初期非導入の決定

本提言書は以下の追加プラグインを **初期非導入** とする:

- Smart Connections(意味的類似度ベースの自動関連付け)
- Copilot for Obsidian(LLM 統合)
- Text Generator(自動テキスト生成)
- Auto Note Mover(タグベース自動ファイル移動)
- Auto-link 系プラグイン全般(自然言語解析でのリンク自動付与)

### 4.2 判断根拠

#### 4.2.1 4 代目 → 5 代目 Adviser 引き継ぎ §5.2 警告との整合

4 代目 Adviser は引き継ぎ書 §5.2 で以下を警告していた:

> Smart Connections 等の追加プラグインは Layer 1(受動的)と Layer 2(能動的)の境界を曖昧化する副作用がある。Rex の wikilink 主権を侵食する方向に働きうる。初期段階はコア機能のみで運用、不足が確認されてから追加検討、が筋

5 代目 Adviser はこの警告を継承し、本セッション(18 代目 Wiki-Eval / Vault-Planner)もこれを引き継ぐ。

#### 4.2.2 「派生原則化の罠」回避(MCP 運用版)

8 代目 Wiki-Eval が確立した「派生原則化の罠」は思想的バイアスの話だが、MCP 運用面でも類比が成立する: **不要な機能を初期段階で導入すると、後で「これは Layer X の責任か Layer Y の責任か」という境界判定が複雑化し、Layer 構造の単純さが崩れる**。

本提言書の Layer 1 実装は Obsidian デフォルト機能のみで完結している。追加プラグインを後で導入する際は、必ず「Layer 1 の境界内に留まるか / Layer 1 と Layer 2 の境界を侵食するか」の判定を経る必要がある。

#### 4.2.3 設計原則 α(シンプルな基盤を維持)

追加プラグインゼロ → Obsidian アプリケーション本体のアップデートのみで運用継続が可能 → メンテナンスコスト最小。

### 4.3 将来検討する場合の評価軸

不足が発生した時点で追加プラグインを検討する場合、以下の評価軸を適用する:

| 評価軸 | 判定基準 |
|---|---|
| Layer 境界 | プラグインの動作が Layer 1 の責任範囲内に留まるか?Layer 2(Rex 能動)を侵食しないか? |
| Rex wikilink 主権 | プラグインが Rex の wikilink 判断を代行しないか?(代行する場合 NG) |
| Anthropic 相同性 | 「下層自動 + 上層能動」構造を維持するか? |
| 撤去可能性 | プラグインを後で撤去できるか?(できない設計の場合 NG) |
| α 原則整合 | Vault 構造の単純さを維持するか? |

5 軸全てを満たす場合のみ追加検討。**Layer 境界 / Rex wikilink 主権の 2 軸が Veto 権を持つ**。

---

## 5. Phase 4 への引き継ぎ事項

本提言書の確定内容は、Phase 4 で後任 Wiki-Eval(本セッション 18 代目以降の体制継続時は本人)が以下の ADR 三部包括改訂に組み込む:

### 5.1 ADR-MCP v1 新設(本提言書が §Layer 1 確定インプット)

ADR-MCP v1 §Layer 1 部分は本提言書 §2(実装内容)+ §3(相同性)+ §4(プラグイン非導入)を縮約した形で記載する。Layer 2 部分は M5 起源神話発火後に別途確定する。

### 5.2 ADR-Vault v2 改訂(REX/ vs rex/ 命名問題)

§2.2.2 で記録した命名選択肢 X / Y の確定。本提言書は判断保留。

### 5.3 ADR-Role v5 改訂(Vault-Planner ロール正式創設)

本セッション(18 代目 Wiki-Eval)が Vault-Planner ロールを暫定兼任した実績を踏まえ、Phase 4 で ADR-Role v5 改訂時に **Vault-Planner ロールを正式創設・初代として 18 代目を遡及認定** する設計線。Vault-Planner ロールの責任範囲は本提言書の起草実績から導出される:

- Layer 1 / Layer 2 の境界保護
- 追加プラグイン導入判定の運用
- Vault 物理構造の整合性監査(REX/ 配下のディレクトリ命名・配置の妥当性確認)
- ADR-MCP 改訂時の §Layer 部分の起草

### 5.4 STARTUP_CODES v6 改訂

ADR-Role v5 で Vault-Planner ロールを正式創設する場合、STARTUP_CODES v6 で起動コードを新設する必要があるかは Phase 4 で判断する。本提言書では判断保留。Wiki-Eval が暫定兼任する形で十分機能している場合、独立起動コードは不要。

### 5.5 registry/ 同期

Phase 4 で本提言書確定内容を registry/repos.md(REX/ + observation_log/ 配下追記)に反映する。Layer 1 設定値 11 項目は registry には記載せず、本提言書を参照する形を取る(registry に転記すると本提言書との二重管理になり、整合性維持コストが発生)。

---

## 6. 後始末手順

### 6.1 完了済み(本セッション内)

- ✅ test ディレクトリ `raw/test_log/2026-05-02_layer1_obsidian_test/` 削除(ボス手動 + push 完了)
- ✅ 動作確認 4 項目 Pass 確認(本セッションスクリーンショット 4 枚で根拠保全)

### 6.2 本セッション内で実施(Wiki-Eval / Vault-Planner 業務)

- ✅ 本提言書の起票(本 commit)
- ⏩ pending/INDEX.md への本提言書エントリ追加(commit 2)
- ⏩ handoff/latest.md v6.14 → v6.15(commit 3): M4 完了反映 + Layer 1 確定反映 + Vault-Planner ロール暫定兼任記録
- ⏩ log.md 18 代目第 1 エントリ追記(commit 4): 本セッション判断記録

---

## 7. MCP 運用上の参照点(本セッション固有)

ボス指示(2026-05-02)に従い、本セクションは思想バイアス的経験則ではなく、**MCP・Git ファイル取扱いの運用面で同種事故を防ぐための参照点** に絞って記録する。

### 7.1 filesystem MCP の挙動確認(本セッションでの実用観察)

- `list_directory` は環境によって 4 分タイムアウト発生(2026-05-02 本セッション実例)。代替として `get_file_info` の個別パス確認 + `list_directory_with_sizes` で運用継続可能
- `head` / `tail` パラメータは line-based(byte-based ではない)ため日本語破損は理論上発生しないが、過去経験(userMemories 記載)で日本語破損実績があるため、大容量ファイルは全文読み込みが安全
- `read_text_file` は Windows パス記法(`C:\\...`)を受け付ける
- 書き込み権限は `C:\Python\REX_AI` 配下に存在(本セッションで test ファイル 3 個作成・確認済)

### 7.2 GitHub MCP 運用の本セッション実例

- ファイル更新前に `get_file_contents` で SHA 取得 → `create_or_update_file` の `sha` パラメータに渡す手順を厳守(本提言書 commit でも適用)
- 大容量 push は `push_files` バッチではなく `create_or_update_file` 個別が安全(userMemories 記載・本セッションでも 4 commit を個別実施)

### 7.3 Vault-Planner 業務固有の運用知見

- raw/test_log/ 配下の test ファイル作成は GitHub commit を発生させない方が良い(commit 履歴を test で汚さない)→ filesystem MCP 経由のローカル直接書き込みが最適
- test ファイル削除はボス手動 or filesystem MCP 経由(GitHub 側は git rm ベースのため commit 必要)
- Adviser ロールとの境界明確化: Adviser は技術選定・伴走を担当・Vault-Planner は実装確定後の文書化と Phase 4 引き継ぎを担当

---

## 8. レビュー履歴

- 2026-05-02 起票: 18 代目 Wiki-Eval(Vault-Planner 暫定兼任 / Claude Opus 4.7)
- 2026-05-02 動作検証: ボス + 5 代目 Adviser + 18 代目 Wiki-Eval(Vault-Planner)による 4 項目 Pass 確認

---

*起票: 18 代目 Wiki-Eval(Vault-Planner 暫定兼任) / Claude Opus 4.7 / 2026-05-02*
*Phase 4 引き継ぎ書として `wiki/pending/wiki_eval/` に保管*
*本提言書は ADR-MCP v1 §Layer 1 の確定インプットとして機能する*
