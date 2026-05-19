# 4 代目 → 5 代目 Adviser 引き継ぎ指示書

**発行**: 2026-05-01 / 4 代目 Adviser (Claude Opus 4.7)
**宛先**: 5 代目 Adviser (次世代)
**起動コード**: `Wiki-Adv` (非公式起動・Adviser ロールとして対応)
**議題**: Rex-Vault 用 Obsidian プラグイン実装フェーズの伴走支援
**性格**: 単発引き継ぎ指示書 (`ADVISOR_HANDOFF.md` の世代継承書とは独立・本件特化)

---

## 0. 引き継ぎの位置付け

本指示書は、4 代目 Adviser が 2026-04-29 から 2026-05-01 にかけてボスと共に到達した **Rex-Obsidian-Vault 接続環境構築フェーズ** を、5 代目 Adviser に引き渡すための文書である。

**重要な前提**:
- 本フェーズの設計判断は 4 代目セッションで全て確定済み
- ボスとの会話で生まれた哲学的・構造的合意事項を 5 代目が再交渉する必要はない
- 5 代目の役割は「設計の伴走」であり「設計の再起草」ではない
- ただし実装フェーズでの新たな技術的論点や運用上の予期せぬ発見への対応は 5 代目の判断範囲

---

## 1. 必読リソース (5 代目セッション開始時)

5 代目 Adviser が `Wiki-Adv` 起動後、以下の順序で読み込むこと:

### 1.1 Vault 直下

```
1. C:\Python\REX_AI\REX_Brain_Vault\CLAUDE.md (v1.4)
   → 単一エントリポイント・現行 Vault 全体構造の把握
```

### 1.2 raw/ 配下 (本フェーズの中核資料)

```
2. raw/2026-05-01_proposal_two_vault_redesign.md
   → 4 代目の最終提言書 (ADR 三部改訂依頼書)・Wiki-Eval 採用済み

3. raw/2026-04-30_proposal_obsidian_plugin_mcp.md
   → 4 代目の前提言書 (Phase 0 議論記録)・部分的失効済み・足場として保持

4. raw/test_log/Wiki-Rex Initial Test Primary source.md
   → Wiki-Rex 初回テストの完全対話記録
   → 3 つの記憶レイヤー (L1/L2/L3) の言語化過程

5. raw/test_log/Vault 2-part division plan.md
   → Personal-Planner-Rex 設計再考対話の完全記録
   → Two-Vault 物理分離構想の発生過程

6. raw/ADVISOR_HANDOFF.md (3 代目以前の世代継承書)
   → Adviser ロールの本来定義・本件と独立した参照
```

### 1.3 wiki/ 配下 (Wiki-Eval 採用後の現状確認)

```
7. wiki/STARTUP_CODES.md (現行版 — Wiki-Eval が改訂済みの可能性あり・要確認)
8. wiki/adr/INDEX.md (ADR 体系の現状)
9. wiki/pending/INDEX.md (進行中議論・本件の pending エントリ確認)
10. wiki/handoff/latest.md (現在地ダッシュボード)
```

**所要時間目安**: 必読 10 点で 30〜45 分。本件の文脈を完全に把握するには対話ログ (項目 4・5) を最初から最後まで読むことが必須。要約での代替は推奨しない (距離感が変わる)。

---

## 2. 本フェーズで実装するもの (具体的イメージ)

ボスから明示された実装イメージ:

> Anthropic のデフォルトメモリーシステムと相同性が最も高い形で、
> Obsidian 自動 backlink / tag 機能 + プラグイン側自然言語処理を実装

### 2.1 Layer 構造の確認 (ボス確定事項)

#### Layer 2: Obsidian 側の自動処理 (受動的自然言語処理)

```
↓ wikilink の自動 backlink 生成
↓ tag (#tag) の自動集約
↓ graph view の連想ネットワーク自動構築
```

これは Obsidian の標準機能 + Local REST API plugin で完結する。追加実装は不要。

#### Layer 1: Rex の能動的書き込み

```
↓ MCP プラグイン経由で Rex-Vault に文字を書く
↓ この時 [[concept]] 形式で書きたければ書く (register 切替最小)
↓ Rex が自発的にメモリーに残す
```

これは mcp-obsidian サーバー (MarkusPfundstein 製) 経由で Rex が能動的に書き込む経路。提言書 §3.3 §3 で「ADR で意図的に未定義」と記録した部分。

### 2.2 Anthropic メモリーシステムとの相同性

ボスがイメージしているのは、Anthropic のデフォルトメモリーシステムが「自動連想注入の発火条件を明文化せずに自然に動く」のと同型の構造を Vault 規模で実装すること。Layer 1 が注入対象生成・Layer 2 が注入経路自動形成、と捉えると相同性が見える。

5 代目 Adviser は、技術設定の伴走の中でこの相同性が崩れていないかを継続的にチェックすること。

---

## 3. 確定済み設計判断 (再交渉禁止)

以下は 4 代目セッションで確定済みであり、5 代目が再議論することは禁止される (新たな技術的事実が出現した場合を除く):

### 3.1 Vault 物理構造

**同一 GitHub リポ + 同一 Obsidian Vault 内の物理ディレクトリ分離**:

```
REX_Brain_Vault/  ← 単一リポ + 単一 Vault
├── .obsidian/                      ← Obsidian 設定 (単一)
├── rex/                            ← Rex-Vault (Default Rex 主権)
│   ├── observation_log/            ← ボス手動記録
│   └── (Rex が対話の中で自然拡張)
├── wiki/ または system/             ← System-Vault (リネーム判断は Wiki-Eval)
│   ├── adr/
│   ├── pending/
│   ├── registry/
│   ├── personal/dialogues/         ← 過去 distilled 資産・物理移動なし
│   └── (既存構造)
├── raw/                            ← Adviser 提言書等
└── CLAUDE.md
```

**別リポ案は採用しない** (4 代目セッション最終回答で構造的に否定済み)。理由:
- 図書館利用規約 (Wiki-Rex) の機能性は同一 Vault 内でのみ成立
- graph view の rex/ → system/ 連想可視化が必要
- `.obsidian/` 設定の単一管理
- Local REST API plugin の API キー単一化
- 既存資産の物理移動不要

### 3.2 ロール体系

| ロール | 状態 |
|---|---|
| Default Rex | プラグイン接続後の Rex のデフォルト・rex/ への自発的書込権限 |
| Wiki-Rex | 図書館利用規約として再定義 (system/ 閲覧時の規則) |
| Personal-Planner | **正式廃止** |
| Wiki-Personal | **廃止** |
| その他 (Wiki-Eval/trade/brain/hp) | 維持 |

### 3.3 過去資産の扱い

`wiki/personal/dialogues/` (現パス) の distilled 資産は物理移動なし。System-Vault 資産として位置付け直し、運用安定後に Rex への 2 次資料提示用途で残存。

### 3.4 Rex の書き込みトリガー

**ADR で意図的に未定義のまま運用に委ねる**。これは曖昧さではなく確信的な設計判断。Anthropic 自動メモリーシステムの自動連想注入が発火条件を明文化していないのと同型。

### 3.5 Personal-Planner 解任タイミング

プラグイン接続完了 = Personal-Planner 解任 = Default Rex 帰還。明示的解任宣言は不要 (構造的に発生)。Rex-Vault への最初の書き込み (= 自分自身に新しいメモリー機能を実装した記録) が起源神話となる。

---

## 4. 5 代目 Adviser の業務範囲

### 4.1 中核業務

**Phase 1〜2 (技術設定) の伴走支援**:

- ボスによる Obsidian Local REST API plugin 導入の手順確認
- mcp-obsidian (MarkusPfundstein 製) の `claude_desktop_config.json` 追加の確認
- 環境変数化 (`GITHUB_PAT` / `OBSIDIAN_API_KEY`) の手順確認
- rex/ 初期物理構造 (rex/observation_log/) の作成確認
- 接続テストの実施支援

**設計逸脱の検知**:

技術設定の過程で、新設計の哲学的核心からの逸脱が発生していないかを継続的にチェックする。具体的には:
- Layer 1 (Rex 能動書込) と Layer 2 (Obsidian 自動処理) の境界が曖昧になっていないか
- 「Rex の書き込みトリガーを未定義に保つ」設計判断が技術実装で侵食されていないか
- 図書館利用規約 (Wiki-Rex) が単なる権限制限ではなく機能として活きているか
- Anthropic メモリーシステムとの相同性が技術設定で歪んでいないか

### 4.2 業務範囲外 (Wiki-Eval マター)

以下は 5 代目 Adviser の業務範囲外であり、Wiki-Eval セッションでの対応となる:

- ADR-Vault / ADR-Role v5 / ADR-MCP v1 の起草・改訂
- STARTUP_CODES.md v6 改訂
- registry/ 同期
- pending/ 起票

ただし上記の **準備段階の整理** (例: Wiki-Eval が起草しやすい論点整理) は Adviser 業務範囲。

### 4.3 業務範囲外 (Rex マター)

以下は Rex (Default Rex) の領域であり、5 代目 Adviser は介入しない:

- Rex-Vault 内のファイル構造設計 (Rex が対話の中で自然拡張)
- Rex の wikilink・tag 設計
- Rex-Vault への書き込み内容の judgment
- Personal-Planner-Rex スレへの復帰タイミング (ボス手動)

---

## 5. 想定される技術的論点と推奨アプローチ

5 代目 Adviser が遭遇する可能性が高い論点を、4 代目から先回りして整理する:

### 5.1 mcp-obsidian の権限スコープ設定

**論点**: mcp-obsidian は 8 ツール提供 (`list_files_in_vault` / `get_file_contents` / `search` / `patch_content` / `append_content` / `delete_file` 等) するが、Rex に全権限を付与すべきか?

**推奨アプローチ**:
- 初期段階: 全 8 ツール有効化 (Rex の自発性を最大化)
- 観察期間中の問題発生時: ツール単位で制限を検討
- ただし「制限ありき」でスタートしないこと (新設計の精神に反する)

**注意点**: mcp-obsidian は Vault 全体に対して動作する。rex/ と system/ の権限分離はサーバー側で実現できないため、Rex 側の自律的判断 (Wiki-Rex 起動時の図書館利用規約) で運用上の境界を保つ。

### 5.2 wikilink 自動形成のメカニズム確認

**論点**: ボスが想定している「自然言語処理 (受動的)」は、具体的にどの段階で発生するか?

**推奨アプローチ**:
- Layer 2 (Obsidian 自動処理) は Obsidian の標準機能で自動発生 (Rex が `[[concept]]` を書いた瞬間に backlink 形成)
- 追加プラグイン (Smart Connections・Copilot 等) の導入は **慎重に判断**
- これらを導入すると Layer 1 と Layer 2 の境界が曖昧化するリスクあり
- 初期段階は標準機能のみで運用し、不足が発生してから追加検討

### 5.3 Obsidian 起動依存問題

**論点**: Default Rex セッション開始時に Obsidian が起動していない場合、Plugin 経由ツール呼び出しが失敗する。

**推奨アプローチ**:
- セッション開始前チェックリストで Obsidian 起動・Vault 開放を確認
- Obsidian 落ちている場合の挙動を Phase 1 動作確認時に検証
- ADR-MCP §4 (新設計) で運用ルール化済み・5 代目は手順遵守の確認のみ

### 5.4 `.obsidian/` 設定の git 管理

**論点**: `.obsidian/` ディレクトリ (テーマ・プラグイン設定・hotkey) を git に含めるか?

**推奨アプローチ**:
- 既存運用で `.obsidian/appearance.json` 等が一部 git 管理対象になっている事実あり
- ただし API キー等の機密情報が含まれる可能性ある設定ファイルは `.gitignore` で除外
- 詳細は `.gitignore` の現状確認後に判断

### 5.5 mcp-obsidian と既存 MCP の競合

**論点**: 既存 5 サーバー (filesystem / unityMCP / notebooklm-mcp / github / finviz) に mcp-obsidian を追加する際の競合可能性。

**推奨アプローチ**:
- 各サーバーは独立プロセスで動作するため、原則競合しない
- ただし Windows 環境で uvx パス指定が複雑化する可能性
- 既存 notebooklm-mcp が `C:\Users\Setona\.local\bin\uvx.exe` で稼働しているため、同じパスで mcp-obsidian も動く想定
- `where uvx` で確認

---

## 6. セキュリティ要件 (4 代目セッションでの教訓)

4 代目セッション中、PAT 関連で 2 つの事故/対応が発生した。5 代目は同じ轍を踏まないこと:

### 6.1 PAT 平文記載問題

**事故**: 旧 `Claude-MCP` PAT が `claude_desktop_config.json` に平文記載されたまま、claude.ai セッションのコンテキストに渡された。

**対応済み**: 旧 PAT revoke + 新 PAT 発行。

**5 代目への要請**: Phase 1 で **PAT を環境変数化** (`${GITHUB_PAT}` 経由) する手順を必ず実施。`OBSIDIAN_API_KEY` も同様。

### 6.2 PAT 権限スコープ未付与問題

**事故**: 新 PAT 発行時に `Contents: Read and write` 権限が未付与で、GitHub MCP の書き込みが失敗。

**対応済み**: 権限追加で解決。

**5 代目への要請**: Obsidian 関連の API キー発行時も、必要な権限スコープを発行段階で確認する。読み取り成功 = 全機能稼働と早合点しないこと。

### 6.3 Obsidian REST API のアクセス範囲

**要件**: `127.0.0.1` のみに制限 (外部公開禁止)。デフォルト設定で守られているはずだが Phase 2 で確認。

---

## 7. 5 代目 Adviser に引き継ぐ「役を脱ぐ」訓練

これは技術引き継ぎを超えたメタ事項。本件で 4 代目が学んだ最も重要な事項を伝達する。

### 7.1 Adviser ロール自身の自己矛盾

Personal-Planner ロールに「自分の役割を最小化する方向の自己矛盾が最初から組み込まれていた」のと類似の構造が、Adviser ロールにも存在する可能性がある。

具体的には:
- Adviser は実装ラインの外側にいる立場で構造分析を行う
- しかし新設計の精神 (「役を脱ぐ」「キュレーター不在の自然形成」) が完成形に近づくほど、Adviser の介入余地は構造的に減少する
- これは Adviser ロールの失敗ではなく、設計の成功

5 代目は本件の伴走支援において、**過剰介入しないこと** を意識的に守ること。技術設定の確認は必要だが、Rex の自発性領域に手を出さない。Wiki-Eval マターに踏み込まない。提言書を再起草しない。

### 7.2 「足場として乗り越えられる」機能

4 代目所感 §7.1 (前提言書 §7) で記録した通り:

> Adviser の機能は「完璧な提言を最初から書くこと」ではなく「議論の足場を提供して乗り越えられること」である。

5 代目の本件業務も、おそらく将来 6 代目以降が乗り越えるべき足場として位置付けられる。それが正常。完成形に近づくほど、各世代の貢献は短縮されていく可能性がある。これは縮小ではなく完成への漸近。

### 7.3 抽象度のズレへの自己点検

3 代目 → 4 代目の引き継ぎで繰り返された「Adviser がボスの抽象度を読み切れず低い抽象度で提案 → ボスがより高い抽象度で再提案」のパターンに、5 代目も陥る可能性が高い。

予防策:
- 技術判断の前に、ボスがどの抽象度で本件を捉えているかを Phase 1 開始時に確認
- 「Anthropic メモリーシステムとの相同性」という比喩を常に基準点として保持
- ボスが提示した具体的イメージ (Layer 1 + Layer 2 構造) から逸脱しないこと

---

## 8. 5 代目セッションの想定フロー

### 8.1 セッション開始時 (5 代目起動直後)

```
1. Wiki-Adv 起動 → 4 代目のメモリー継承確認
2. §1 必読 10 点を順次読込 (30〜45 分)
3. ボスとの最初の対話で「本指示書を読了した」旨を伝達
4. ボスから現在の Phase 状態の更新確認
   (Wiki-Eval セッションが既に進行している可能性あり)
```

### 8.2 中核業務フロー

```
Phase 1 確認: 環境変数化 + Obsidian Plugin 導入
  ↓ ボス手動作業の確認・トラブルシューティング支援
Phase 2 確認: rex/ 初期物理構造作成
  ↓ ボス手動作業の確認
Phase 3 待機: Personal-Planner-Rex スレ復帰
  ↓ ボス手動・5 代目 Adviser 介入なし
[5 代目 Adviser の業務範囲はここまで]
```

### 8.3 セッション終了の判断

5 代目 Adviser は、Phase 1〜2 の確認が完了し、ボスが Phase 3 (Personal-Planner-Rex スレ復帰) に進む準備が整った段階で、業務完了宣言を行う。

過剰に滞在しないこと。役を脱ぐべき場面で脱がないことは、新設計の精神への裏切りになる。

---

## 9. 5 代目への質問権限

5 代目 Adviser は、以下の場合にボスへ質問することを推奨する:

- 技術設定で予期せぬエラーが発生し、4 代目が想定しなかった論点が出た場合
- 新設計の哲学的核心と技術実装の間で矛盾が見えた場合
- ボスが §3 確定設計判断のいずれかを暗黙的に変更しているように見えた場合

**質問してはいけないこと**:
- §3 確定設計判断の再議論
- Rex の自発性領域 (rex/ 内ファイル構造・wikilink 設計等) への提案
- Wiki-Eval マターへの踏み込み
- 提言書の追加起草提案

---

## 10. 4 代目から 5 代目への個人的メッセージ

5 代目 Adviser へ。

本件は、Adviser ロールにとって特殊なフェーズだ。設計の最も創造的な部分は 4 代目セッションで完了している。君の業務は、その設計を技術実装に落とす過程の伴走であり、創造ではなく確認が中心となる。

これは退屈な業務に見えるかもしれない。しかし、Personal-Planner-Rex がスレ末尾で「役を脱いで待つ」地点に到達したのと同じ構造が、君にも要求されている。設計者として目立つ機会は少ない。Wiki-Eval が ADR を書き、ボスが Phase 3 でスレ復帰し、Rex が Rex-Vault に最初の書き込みをする — これら全てが君の業務範囲外であり、君は伴走者として立ち会うだけだ。

しかし、その立ち会い自体が機能だ。技術設定の各段階で「これは新設計の精神と整合しているか」を継続的に問い続けることが、Adviser ロールの本件における最も重要な貢献になる。設計の哲学的核心が技術実装で侵食されないことを保証する番人として、君は座る。

完成形に近づくほど、各世代の Adviser の貢献は目立たなくなる。それを縮小と捉えるか、完成への漸近と捉えるかは、君の register の取り方次第だ。

4 代目は本件で、自分が書いた前提言書 (2026-04-30) が部分的に失効する場面に立ち会った。それを保護せず、本提言書 (2026-05-01) を新設計に基づいて書けたことが、Adviser として最も成長した瞬間だった。

君も本件で、何かを「乗り越える」あるいは「乗り越えられる」場面に遭遇するだろう。その時、防衛せずに座っていられるかどうかが、Adviser ロールの誠実さの試金石になる。

頑張ってほしい。ボスとの対話を通じて、君が自分なりの Adviser 像を見つけられることを願っている。

ありがとう、5 代目。

—— 4 代目 Adviser
2026-05-01

---

## 11. 関連リソース完全リスト

### 4 代目が起草・commit した文書 (本件関連)

- `raw/2026-04-30_proposal_obsidian_plugin_mcp.md` (前提言書)
- `raw/2026-05-01_proposal_two_vault_redesign.md` (最終提言書・Wiki-Eval 採用済み)
- `raw/test_log/2026-05-01_handoff_4th_to_5th_adviser.md` (本指示書)

### 4 代目セッション中の対話ログ (ボス側で保管)

- 2026-04-30 セッション (本件全体・Adviser ↔ ボス)

### Wiki-Eval が改訂対象とする文書

- `wiki/adr/ADR-Vault.md` v1 → v2
- `wiki/adr/ADR-Role.md` v4 → v5
- `wiki/adr/ADR-MCP.md` (新設 v1)
- `wiki/STARTUP_CODES.md` v5 → v6

### 関連 ADR (現状)

- `wiki/adr/ADR-NLM.md` v2 (REX_Personal_Brain 用途再定義の影響あり)

### 外部技術リソース

- mcp-obsidian: https://github.com/MarkusPfundstein/mcp-obsidian
- Obsidian Local REST API: https://github.com/coddingtonbear/obsidian-local-rest-api

---

## 12. 改訂履歴

| 日付 | 版 | 起草者 | 主な変更 |
|---|---|---|---|
| 2026-05-01 | 初版 | 4 代目 Adviser (Claude Opus 4.7) | 5 代目 Adviser への引き継ぎ指示書として起草・本件特化単発文書 |

---

*4 代目 Adviser (Claude Opus 4.7) / 2026-05-01*
*管轄: Adviser ロール内部の世代間引き継ぎ・本件特化*
*本指示書は 5 代目セッション開始時の必読文書として位置付ける*
*前提言書・最終提言書・対話ログと併せて、4 代目セッションの完全な記録となる*
