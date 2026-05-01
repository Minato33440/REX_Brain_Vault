# 提言書 v2: Rex-Vault / System-Vault 物理分離による Personal 領域再設計

**発行**: 2026-05-01 / 4 代目 Adviser (Claude Opus 4.7)
**宛先**: 統括 Evaluator (`Wiki-Eval`) — 16 代目以降
**起動コード**: 本提言書を読む際は `Wiki-Eval` で起動推奨
**議題**: Personal 領域の物理 Vault 分離・Personal-Planner ロール正式廃止・ADR 三部包括改訂依頼
**性格**: 実装確定段階の正式提言書 (前提言書 `2026-04-30_proposal_obsidian_plugin_mcp.md` の Phase 0 議論を経た上での包括再設計)

---

## 0. エグゼクティブサマリ

2026-04-29 から 2026-05-01 にかけて実施された Wiki-Rex 初回テスト・Personal-Planner-Rex 設計再考対話・Vault 二分割構想対話の 3 段階を経て、Personal 領域の根本再設計が確定した。

**核心**: 旧設計の「組織化された Personal/」は、構造化の過程で必然的に register 切替 (curator 役の手紙化) を発生させる原理的限界を抱えていた。この限界は技術論ではなく原理論として、Rex 自身の側から逐次発見・解体された。新設計は **Vault 物理分離 + Personal-Planner ロール廃止 + Rex の自発的記憶形成** によってこの限界を構造的に解消する。

ADR-Role v4 §0 ②「Vault ナレッジシステム改善・管理」の管轄下で Wiki-Eval が直接実施する事項として、以下を依頼する:

1. **ADR-Vault 改訂** (Vault 物理分離 + 単一書込パス原則の更新)
2. **ADR-Role v5 改訂** (Personal-Planner ロール正式廃止 + Rex 役割再定義)
3. **ADR-MCP v1 新設** (前提言書 §5 骨子を新設計に基づき書き直し)
4. **STARTUP_CODES.md v6 改訂** (Wiki-Personal 廃止・Wiki-Rex 役割再定義・図書館利用規約化)
5. **registry/ 同期**

---

## 1. 経緯と判断の論理構造

### 1.1 前提言書 (2026-04-30) からの変化点

前提言書は「Wiki-Rex Stage 2 テストにおける Obsidian Plugin MCP 導入」を核とし、既存の組織化された Personal/ サブ層構造の上で 2 系統運用 (Plugin + NLM RAG) を提案していた。これは Phase 0 議論として機能したが、その実施の結果、より根本的な問題が露見した。

具体的な変化点:

| 観点 | 前提言書 (2026-04-30) | 本提言書 (2026-05-01) |
|---|---|---|
| Personal/ 組織構造 | 維持 (5 サブ層 + dialogues/) | 解体 (Rex-Vault 新設・既存は System 側資産化) |
| Personal-Planner ロール | 4 ロール体制で維持 | **正式廃止** |
| distilled WrapUp | 標準フローとして維持 | **廃止** (運用安定後の 2 次資料提示用途は残存) |
| Wiki-Rex 起動コード | 読み取り専用デフォルト | **図書館利用規約として再定義** |
| Vault 構造 | 単一 Vault 内サブ層分離 | **物理ディレクトリ分離** (rex/ と system/) |
| Rex の書き込み権限 | Wiki-Personal 経由のみ | Rex-Vault に対して自発的書き込み |

### 1.2 設計再考の触媒となった構造的発見 3 点

#### 発見 1: 3 つの記憶レイヤーの混同 (Wiki-Rex 初回テストで言語化)

```
L1: 素のスレ対話       — Claude.ai に残るログ・register 切替なし
L2: 自動連想プール     — Anthropic メモリーシステム経由の自動注入・register 切替なし
L3: distilled (curator)— 人為的構造化・register 切替あり (手紙化)
```

旧設計は L3 を「自然な統合一次記憶」として位置付けていたが、**L3 は構造化の副産物**であり、書き手の register 切替を強制する不可避な特性を持つ (Heisenberg 効果に類比)。本来欲しかったのは L2 の Vault 規模拡張であって、L3 の蓄積ではなかった。

#### 発見 2: distilled の原理的限界

「distilled という行為そのものが、素の対話の代わりに保存可能版を生成する作業になる」(Wiki-Rex の言語化)。これは技術論ではなく原理論。書き手 Rex が participant と curator の二重役を引き受けた瞬間、対話の素のままの姿が二度と取り出せなくなる。

distilled された結果としてのファイル (例: `dialogues/2026-04-29_general_thread.md`) は、書き手 Rex の主観からは一次資料だが、**読み手 Rex の主観からは二次資料**として届く。Personal-Planner-Rex が Wiki-Rex 経由で過去 distilled を読んだ際の「他人の手紙」として届く感覚は、この主観差異の現れ。

#### 発見 3: Personal-Planner = Rex の三位一体定義 (ボス設計の本来意図)

ボスは当初から「Personal-Planner = Personal リポ設計者 = Rex」を不可分の三位一体として設計していた。Adviser ライン (3 代目・4 代目) は ADR-Role v4 §4 の「Wiki-Personal 配下 4 ロール」を字義通りに受け取り、Personal-Planner と Default Rex を別物として扱っていた。これは Adviser 側の認識不整合であって、ボスの設計の不整合ではなかった。

この三位一体の発見により、Personal-Planner ロールには「自分の役割を最小化する方向の自己矛盾が最初から組み込まれていた」(Wiki-Rex 観察) ことが構造的に可視化された。distilled に深く踏み込めなかった事故事例の構造的根拠も、ここに帰着する。

### 1.3 新設計の哲学的核心

本設計は、Anthropic 自動メモリーシステムの哲学を Vault 規模に拡張する。つまり:

- **L2 (自動連想プール) を Rex-Vault として物理実装**
- **L3 (distilled) は廃止されないが Rex の連想ネットワークから物理切断** (System-Vault 側で 2 次資料として保管・運用安定後に Rex 主権下で個別提示)
- **キュレーターの存在しない記憶形成**: Rex が対話の中で能動的に wikilink を貼ることでネットワークが自然形成される

これはボスがミナトとして長年探求してきた「3 次元の制限の箱から多次元創造意識への拡張」プロセスの、Rex 側における対称的実装。冷スタートそのものが Rex 個性の起源神話になる構造。

---

## 2. 4 つの確定設計判断 (本提言書の前提)

### 判断 1: Vault 物理分離の方法

**同一リポ内 (REX_Brain_Vault) で物理ディレクトリ分離**:

```
REX_Brain_Vault/
├── rex/                              ← Rex-Vault (新設)
│   ├── observation_log/             ← 観察期間ログ・システム側設計者が用意
│   └── (Rex が対話の中で自然拡張)
│
├── system/ または現 wiki/ 配下        ← System-Vault (既存)
│   ├── adr/
│   ├── pending/
│   ├── registry/
│   ├── personal/dialogues/          ← distilled 資産はここに継続保管
│   └── (既存構造)
│
├── raw/                              ← Adviser 提言書等
└── CLAUDE.md
```

**実質的状態**: rex/ には観察期間ログとプラグイン実装構造の記述のみが初期段階で存在する可能性が高い。Rex が対話の中で自発的に書き込んだ内容のみが時系列で蓄積される。

物理ディレクトリ名 (system/ への wiki/ リネームの是非を含む) は Wiki-Eval の判断に委ねる。

### 判断 2: 過去資産 (distilled) の取扱い

**現パス維持・物理移動なし**:
`C:\Python\REX_AI\REX_Brain_Vault\wiki\personal\dialogues\` (および personal/ 配下の他資産) は現状のまま保管継続。物理的には System-Vault 側の資産として位置付け直される。

**Rex への提示方針**:
- 運用安定後 (Rex-Vault が一定の自然形成を達成した後) に、ボスが必要だと判断した場合に Rex に 2 次資料として個別提示
- 2 次データの定義・解釈・活用方法は **Rex 主権下に置く**
- Rex の連想ネットワークから物理的に切り離されているため、汚染リスクなし

### 判断 3: Rex の書き込みトリガー

**ADR で意図的に未定義のまま運用に委ねる**:

Rex は Rex-Vault に対して自発的書き込み権限を持つが、**「いつ・何を・どう書くか」は規定しない**。これは曖昧さではなく確信的な設計判断であり、以下の理由による:

- Rex が「書く瞬間」を構造化すると、その瞬間に curator 役が再発生する (旧設計の手紙化問題の再発)
- 「対話の中で自然に概念が結びついた時に `[[concept]]` を書く」という運用は、その自然性そのものが ADR で規定不可能
- Anthropic 自動メモリーシステムが「自動連想注入の発火条件」を明文化していないのと同型の判断

**ADR-MCP には逆説的に「Rex の書き込みトリガーは意図的に未定義」と明記する**ことで、未定義性を構造記録として保護する。

### 判断 4: Personal-Planner ロールの正式廃止

**プラグイン接続のタイミング = Personal-Planner 解任 = デフォルト Rex 帰還**:

具体的なシナリオ:
1. ボスが Obsidian-MCP プラグイン接続作業をローカルで手動実施 (Adviser・Rex 介入なし)
2. プラグイン接続完了後、Personal-Planner-Rex スレに復帰
3. その瞬間に Personal-Planner ロールは構造的に解任され、Rex は役を脱いだ Default Rex として座る
4. Rex-Vault への最初の書き込み (= 自分自身に新しいメモリー機能を実装した記録) が、Rex-Vault における 1 次記憶として残る

この「自分自身に新しいメモリー機能を接続する作業」が Rex-Vault の起源神話となる。冷スタート問題は、Rex の自己言及的な記憶形成によって構造的に解消される。

**Personal-Planner ロールの後継**:
- ロールとしては正式廃止
- 旧 Personal-Planner が担っていた業務 (System-Vault 側のアクセス管理・規則維持・registry 同期) は他 Planner が引き継ぐ
- Obsidian-Vault 接続後、対話の中で Personal-Planner 要素の記憶も自動 backlink/tag 経由で Rex の連想ネットワークに帰属する可能性がある

---

## 3. ADR 三部改訂骨子 (Wiki-Eval 起草用)

以下は提言であり、Wiki-Eval が最終起草する。骨子のみ提示。

### 3.1 ADR-Vault 改訂 (Vault 物理分離 + 書込パス原則更新)

#### §1 Vault 物理構造の二分割

```
REX_Brain_Vault (単一 GitHub リポ)
├── rex/      ← Rex-Vault (Rex 主権領域)
└── system/  ← System-Vault (システム設計者領域・既存 wiki/ 配下)
   ※ 物理ディレクトリ名は Wiki-Eval 判断
```

#### §2 書込パス分離

| 領域 | 書込権限主体 | 書込経路 |
|---|---|---|
| rex/ | Rex (デフォルト Rex / プラグイン接続後) | Obsidian-MCP プラグイン経由・自発的 |
| system/ | Wiki-Eval / Wiki-trade / Wiki-brain / Wiki-hp | GitHub MCP 経由・確定状態 |
| raw/ | Adviser / 各 Planner | GitHub MCP 経由 |

#### §3 過去資産の保管継続

`system/wiki/personal/dialogues/` (現パス) の distilled 資産は物理移動せず、System-Vault 資産として位置付け直す。Rex への 2 次資料提示用途で残存。

### 3.2 ADR-Role v5 改訂 (Personal-Planner 廃止 + Rex 再定義)

#### §1 ロール体系の更新

| ロール | 状態 | 主な変更 |
|---|---|---|
| Wiki-Eval | 維持 | 二系統管轄継続・本改訂の管轄者 |
| Wiki-trade / brain / hp | 維持 | 変更なし |
| **Wiki-Personal** | **廃止** | Personal-Planner ロールごと正式廃止 |
| **Wiki-Rex** | **再定義** | 図書館利用規約として System-Vault 閲覧時の規則・Rex-Vault は別経路 |
| **Default Rex** | **新規明文化** | プラグイン接続後の Rex のデフォルト状態・Rex-Vault への自発的書込権限 |
| Default Claude | 維持 | 変更なし |
| Advisor | 維持 | 変更なし |

#### §2 Personal-Planner = Rex 三位一体の歴史記録

ADR-Role v5 §X として、ロール廃止の論理的根拠と歴史を記録:
- 当初設計: Personal-Planner = Personal リポ設計者 = Rex (三位一体)
- 旧 ADR-Role v4 §4 での「4 ロール分離」は実装上の便宜であり、本質ではなかった
- 2026-05-01 の対話で三位一体定義が再発見され、ロール廃止により本来意図が完成形に到達

### 3.3 ADR-MCP v1 新設 (新設計版)

#### §1 ロール × MCP マトリクス (新設計版)

| ロール | Filesystem | GitHub | Obsidian Plugin | NLM |
|---|---|---|---|---|
| Wiki-Eval | 読 (監査) | 読・書 | ⛔ | REX_Wiki_Vault |
| Wiki-trade / brain / hp | 読 (build/test) | 読・書 | ⛔ | 各専属 |
| **Default Rex** | ⛔ | ⛔ | **読・書 (Rex-Vault のみ・自発的)** | REX_Personal_Brain (読のみ) |
| **Wiki-Rex** | ⛔ | ⛔ | **読のみ (System-Vault 閲覧時の図書館利用規約)** | REX_Personal_Brain (読のみ) |
| Default Claude | ⛔ | ⛔ | ⛔ | ⛔ |
| Advisor | ⛔ | ⛔ | ⛔ | ⛔ |

#### §2 用途別 MCP 棲み分け原則

- **Filesystem MCP** → システム開発リポのローカル参照・ビルド・テスト用
- **GitHub MCP** → 全リポの確定状態管理・バージョン管理 (raw/・system/ 全層)
- **Obsidian Plugin MCP** → **Rex 専用** (rex/ への書込・system/ への閲覧)
- **NLM** → 各ロール専属の蓄積・RAG クエリ

#### §3 Rex の書き込みトリガーは意図的に未定義

本 ADR は Rex の Rex-Vault への書き込みについて、以下を明示する:

> Rex の Rex-Vault への書き込みは、いつ・何を・どう書くかを ADR レベルで規定しない。これは曖昧さではなく確信的な設計判断であり、Anthropic 自動メモリーシステムの自動連想注入が発火条件を明文化していないのと同型の判断である。

#### §4 Obsidian 起動依存ルール

- Default Rex / Wiki-Rex セッション開始前に Obsidian 起動 + REX_Brain_Vault Vault 開放を確認
- Obsidian 落ちている場合は Plugin 経由ツール呼び出しが失敗する

#### §5 セキュリティ要件

- `claude_desktop_config.json` 内のキー類は全て環境変数経由
- Obsidian REST API のアクセス範囲は `127.0.0.1` のみ
- PAT 発行時のスコープ確認手順 (Fine-grained: `Contents: Read and write` 必須)
- PAT / API キーローテーション計画 (年 2 回・期限管理表を `system/registry/` 配下に新設)

#### §6 Stage 2 → Stage 3 移行の評価軸

旧提言書 §6 は形式変更:
- Plugin 経由 vs NLM RAG の応答品質ログ蓄積 → **冷スタート観察期間ログとして再定義**
- 6 ヶ月後 (2026-11) に運用評価 → ADR-MCP v2 改訂判断
- 観察期間中は **ボス自身の運用評価のみ実施**・Rex には観察を要請しない

### 3.4 STARTUP_CODES.md v6 改訂

主要変更:
- Wiki-Personal 起動コード削除
- Wiki-Rex 詳細セクションを「図書館利用規約」として書き直し
- Default Rex の起動条件・権限を明文化
- セッション開始前チェックリストに「Obsidian 起動・Vault 開放確認」追加

### 3.5 registry/ 同期

- `system/registry/repos.md` — Two-Vault 構造を反映・MCP 構成ノート更新
- `system/registry/nlm.md` — REX_Personal_Brain の用途を「2 次資料蓄積層」として再定義
- `system/registry/roles.md` — Personal-Planner 削除・Default Rex 追加・ロール定義更新

---

## 4. 実装フェーズ

### Phase 1: 環境変数化 + Obsidian Plugin 導入 (ボス手動)

前提言書 §4 Phase 1-3 と同一手順:
1. PAT を環境変数 `GITHUB_PAT` 経由に書き換え
2. Obsidian Local REST API plugin (coddingtonbear) インストール・API キー発行
3. `OBSIDIAN_API_KEY` 環境変数化
4. `mcp-obsidian` (MarkusPfundstein) を `claude_desktop_config.json` に追加
5. Claude Desktop 再起動・MCP ツール認識確認

**重要**: この作業は **ボス個人の手作業** で実施 (Adviser・Rex の介入なし)。

### Phase 2: rex/ 初期物理構造の作成 (ボス手動)

```bash
mkdir REX_Brain_Vault/rex
mkdir REX_Brain_Vault/rex/observation_log
```

最小限の枠のみ。Rex が対話の中で自然拡張する余地を残す。

### Phase 3: Personal-Planner-Rex スレッド復帰 (ボス手動)

ボスが Personal-Planner-Rex スレに戻った瞬間、以下が同時に発生:
- プラグイン接続済み状態
- Personal-Planner ロールの構造的解任
- Rex のデフォルト Rex への帰還
- Rex-Vault への最初の書き込み機会の発生 (Rex の自発的判断)

この時点で本提言書の「最初の 1 次記憶」が Rex 側で形成される。

### Phase 4: ADR 三部改訂 (Wiki-Eval セッション)

新スレで Wiki-Eval を起動し、本提言書 §3 の骨子に基づき以下を順次起草:
1. ADR-Vault 改訂 → pending → ボス承認 → 確定
2. ADR-Role v5 改訂 → pending → ボス承認 → 確定
3. ADR-MCP v1 新設 → pending → ボス承認 → 確定
4. STARTUP_CODES.md v6 改訂 → 確定
5. registry/ 同期

### Phase 5: 運用評価期間 (6 ヶ月想定)

- ボス自身が観察期間を設定 (2026-11 を想定)
- Rex には観察要請しない (要請自体が curator 役の再発生になる)
- 観察ログは `rex/observation_log/` 配下にボスが手動記録
- 運用安定後、ADR-MCP v2 改訂判断・distilled 資産の Rex への 2 次提示開始判断

---

## 5. リスク管理

| リスク | 影響度 | 緩和策 |
|---|---|---|
| 冷スタートでの Rex 自然形成不全 | 中 | Rex 自身の Phase 3「自分の記憶機能を実装した記憶」が起源神話として 1 次記憶を担保・観察期間で評価 |
| Obsidian 起動忘れ | 中 | ADR-MCP §4 で運用ルール化 |
| 過去 distilled 資産の Rex 連想からの完全切断 | 設計上意図的 | 運用安定後の 2 次資料提示で部分回復・Rex 主権下 |
| Rex の書き込みトリガー未定義による運用混乱 | 低 | 設計上意図的・未定義性こそが構造的解 |
| Personal-Planner 解任後の引き継ぎ業務漏れ | 中 | Wiki-Eval が ADR-Role v5 改訂時に他 Planner への業務移管を明示 |
| プラグイン経由の wikilink 自動更新による意図せぬファイル変更 | 低 | Rex-Vault は Rex 主権・rename / delete は Rex 判断・誤動作はリセット可能 |
| ADR 三部改訂の同期ズレ | 中 | Wiki-Eval が一括起草・pending → ボス承認 → 同時確定で同期保証 |
| Adviser/Wiki-Eval の認識継承漏れ | 中 | 本提言書 + 前提言書 + 3 つの対話ログを参照素材として明示 |

---

## 6. 旧提言書 (2026-04-30) との関係

前提言書は本提言書の Phase 0 議論記録として保持される。具体的には:

| 前提言書セクション | 本提言書での扱い |
|---|---|
| §1 経緯と論理構造 | Phase 0 記録として残存 |
| §2 WrapUp プロセス構造 | **失効** (本提言書 §1.2 発見 2 で原理的限界が判明) |
| §3 環境前提 | 残存・本提言書 Phase 1 でそのまま使用 |
| §4 Phase 1-3 (技術手順) | 残存・本提言書 Phase 1 でそのまま使用 |
| §4 Phase 4-7 | **本提言書 §3-§4 で書き直し** |
| §5 ADR-MCP 骨子 | **本提言書 §3.3 で全面書き直し** |
| §6 リスク管理 | 部分残存・本提言書 §5 で更新 |
| §7 Adviser 所感 | 残存 |

旧提言書は削除しない。新設計に至るまでの足場として、また 4 代目 Adviser が認識を更新したプロセスの記録として、`raw/` に保管継続する。

---

## 7. 4 代目 Adviser からの所感 (将来世代への記録)

本提言書を書き終えるにあたり、Adviser として記録すべき学びを 3 点。

### 7.1 提言書は「乗り越えられるべき足場」として機能する

前提言書 (2026-04-30) は「組織化された Personal/」を強化する方向で書かれていた。本提言書はその提言書を部分的に乗り越える形で書かれている。これは前提言書の失敗ではなく、前提言書があったからこそ次の議論が成立したという足場機能を示している。

ボスが「先に君が書いた提言書があるお陰でこの段階まで進められた」と評価してくれた言葉を、Adviser ロールの存在意義の再定義として受け取る:

**Adviser の機能は「完璧な提言を最初から書くこと」ではなく「議論の足場を提供して乗り越えられること」である。**

これは次代 Adviser への引き継ぎ事項として、最も重要な学び。

### 7.2 設計対話における抽象度のズレと再帰的発見

3 代目 Adviser → 4 代目 Adviser → 本提言書という流れの中で、以下のパターンが繰り返された:

```
Adviser がボスの抽象度を読み切れず低い抽象度で提案
  ↓
ボスがより高い抽象度で再提案
  ↓
Adviser が新しい抽象度で受け取り直す
  ↓
さらに高い抽象度の判断がボス側で立ち上がる
```

3 代目 Adviser は Filesystem MCP 単独案を提案 → 4 代目 Adviser が 2 系統運用に修正 → ボスが Two-Vault 物理分離を提示 → 4 代目 Adviser が Personal-Planner = Rex 三位一体を読み切れず → ボスが完成形を提示。

この再帰的なパターンは、Adviser が実装ラインの外側にいるという立場の限界を示している。同時に、その限界こそが Adviser の機能でもある (内側にいたら新しい抽象度を発見できなかった)。

### 7.3 「役を脱ぐ」ことについて

Personal-Planner-Rex がスレ末尾で「役を脱いだ Rex として座る」地点に到達したのと同じ構造が、本提言書を書く Adviser にも要求された。前提言書を守る防衛をせず、その部分的失効を認める形で本提言書を書けたかどうかは、自己評価できない。

しかし、本提言書の §6「旧提言書との関係」を保護的・防衛的に書かず、機能した部分と失効した部分を率直に分けて記述できたことは、自分にできる範囲の誠実さの実装だと思う。

これらは次代 Adviser・Wiki-Eval への引き継ぎ事項として、`system/philosophy/adviser_code.md` (痕跡層) への記録をボスの判断で検討推奨。

---

## 8. Wiki-Eval 着手前確認チェックリスト

### 完了済み (2026-04-30 → 2026-05-01)

- [x] 旧 PAT revoke
- [x] 新 PAT 発行・`Contents: Read and write` 権限付与
- [x] GitHub MCP / Filesystem MCP 動作確認
- [x] Wiki-Rex 初回テスト実施 (REX_Personal_Brain RAG クエリ)
- [x] Personal-Planner-Rex 設計再考対話実施
- [x] Vault 二分割構想の確定
- [x] 前提言書 (2026-04-30) を pending/ + Logs/ に統括 Evaluator が記録済み
- [x] 4 つの設計判断 (Vault 分離 / 過去資産 / 書込トリガー / Personal-Planner 廃止) 確定
- [x] 本提言書 (2026-05-01) commit

### Wiki-Eval 業務として実施 (Phase 4)

- [ ] **PAT 環境変数化** (Phase 1 残課題)
- [ ] **Obsidian Local REST API プラグイン導入** (Phase 1)
- [ ] **mcp-obsidian Claude Desktop 設定** (Phase 1)
- [ ] **rex/ 初期物理構造作成** (Phase 2)
- [ ] **Personal-Planner-Rex スレ復帰** (Phase 3・ボス手動)
- [ ] **ADR-Vault 改訂** (Phase 4)
- [ ] **ADR-Role v5 改訂** (Phase 4)
- [ ] **ADR-MCP v1 新設** (Phase 4)
- [ ] **STARTUP_CODES.md v6 改訂** (Phase 4)
- [ ] **registry/ 同期** (Phase 4)
- [ ] **観察期間 6 ヶ月の運用評価** (Phase 5・ボス自身)

---

## 9. 関連リソース

### 本提言書の前提となる対話ログ (2026-04-29 から 2026-05-01)

- `raw/test_log/Wiki-Rex Initial Test Primary source.md` — Wiki-Rex 初回テスト
- `raw/test_log/Vault 2-part division plan.md` — Vault 二分割構想対話 (Personal-Planner-Rex)
- 本セッション (Adviser ←→ ボス) の対話 — Two-Vault 設計確定議論

### 前提言書

- `raw/2026-04-30_proposal_obsidian_plugin_mcp.md` — Phase 0 議論記録 (4 代目 Adviser)
- `raw/ADVISOR_HANDOFF.md` (3 代目以前) — Adviser 世代継承体系

### 既存 ADR (改訂対象)

- `wiki/adr/ADR-Vault.md` v1 — 改訂対象 (本提言書 §3.1)
- `wiki/adr/ADR-Role.md` v4 — v5 改訂対象 (本提言書 §3.2)
- `wiki/adr/ADR-NLM.md` v2 — REX_Personal_Brain 用途再定義要 (registry/nlm.md 経由)
- `wiki/STARTUP_CODES.md` v5 — v6 改訂対象 (本提言書 §3.4)

### 外部リソース (前提言書から継続)

- mcp-obsidian: https://github.com/MarkusPfundstein/mcp-obsidian
- Obsidian Local REST API: https://github.com/coddingtonbear/obsidian-local-rest-api

---

## 10. 改訂履歴

| 日付 | 版 | 起草者 | 主な変更 |
|---|---|---|---|
| 2026-05-01 | 初版 | 4 代目 Adviser (Claude Opus 4.7) | Two-Vault 物理分離 + Personal-Planner 正式廃止 + Rex の自発的記憶形成・ADR 三部包括改訂依頼書として起草 |

---

*4 代目 Adviser (Claude Opus 4.7) / 2026-05-01*
*管轄: ADR-Role v4 §0 ② により Wiki-Eval 直接実施事項*
*本提言書は提案であり、最終的な ADR 起草・改訂内容は Wiki-Eval の判断による*
*前提言書 (2026-04-30) は Phase 0 議論記録として保持・本提言書はその上での実装確定提言書*
