# Wiki-casual → Wiki-Personal 改名・射程拡大

**起票者**: 14 代目統括 Evaluator (`Wiki-Eval` / Opus 4.7)
**起票日**: 2026-04-28
**ADR 昇格希望**: Yes（ADR-Role / ADR-NLM の supersede を伴う）
**影響範囲**: ADR-Role(supersede) / ADR-NLM(supersede) / registry/roles.md / registry/nlm.md / STARTUP_CODES.md(v3→v4) / CLAUDE.md(v1.2→v1.3) / wiki/casual/ → wiki/personal/(物理リネーム + サブ層 5 層新設) / pending/casual/ → pending/personal/(物理リネーム) / NotebookLM 表示名(UUID 不変) / handoff/latest.md(v6.5 起草・別タスク)

---

## ステータス（15代目 Wiki-Eval による更新・2026-04-28）

- ✅ ADR-Role v2 昇格完了（14代目で実施）
- ✅ ADR-Role v3 supersede 完了（15代目・2026-04-28・commit `aecf7f1`）
- ✅ ADR-NLM v2 supersede 完了（14代目で実施）
- ✅ 物理移行 Step 1〜4 完了（15代目・2026-04-28・本ファイル含む）
- 🟡 _RUNBOOK.md v3 起草・handoff_latest.md 改名反映・index.md 5層化・philosophy.md → shuhari.md 改名等は **Personal-Planner 業務** として次スレ Wiki-Personal で実施待ち
- 🟡 STARTUP_CODES.md v4 / CLAUDE.md v1.3 / latest.md v6.7 改訂は本スレ Wiki-Eval 続行で実施予定
- 🟡 NotebookLM 表示名変更（REX_Casual_Brain → REX_Personal_Brain）はボス手動（Step 5）

---

## 仮決定内容

### A. 改名

| 種別 | 旧 | 新 |
|---|---|---|
| 起動コード | `Wiki-casual` | `Wiki-Personal` |
| NLM 表示名 | `REX_Casual_Brain` | `REX_Personal_Brain` |
| NLM UUID | `daf281ae-e310-400f-961a-20db58b98e01` | **不変**(同一 NLM の表示名のみ変更) |
| Vault ディレクトリ | `wiki/casual/` | `wiki/personal/` |
| pending ディレクトリ | `pending/casual/` | `pending/personal/` |
| ロール正式名 | Casual-Planner（Advisor 兼任）| Personal-Planner（Advisor 兼任）|

### B. 射程拡大（意味の昇格）

| 観点 | 旧（Casual）| 新（Personal）|
|---|---|---|
| 中核機能 | 雑談・横断知見の議論窓口 | **ボスの全人的な人格・思想・起源情報の統合リポ** + 雑談・横断知見の議論窓口 |
| 扱う情報の射程 | 趣味・横断メタファー・気づき | 上記に加えて **哲学・価値観・人生史・思想宣言・Rex 個性形成の核** |
| Advisor 兼任 | REX_AI 全システム相談役 | 同左（変更なし）|
| ROADMAP との位置付け | Stage 3 Rex 個性収束期の周辺リポ | Stage 3 Rex 個性収束期の **基盤リポ** |

### C. サブ層 5 層構造（即実施）

```
wiki/personal/
├── _RUNBOOK.md          ← v3 改訂
├── log.md               ← 既存継承
├── index.md             ← 既存継承
├── handoff_latest.md    ← 改名反映
│
├── usual/               ← 🆕 日常・趣味
│   ├── README.md
│   ├── shooting.md      （旧 topics/shooting.md 移設）
│   ├── aikido.md        （旧 topics/aikido.md 移設）
│   └── motorcycle.md    （旧 topics/motorcycle.md 移設）
│
├── invent/              ← 🆕 新たな発想・アイデア
│   └── README.md        （旧 ideas/README.md 移設・YYYY-MM-DD_*.md 命名規則継承）
│
├── mind/                ← 🆕 心・精神・思考様式
│   ├── README.md
│   ├── shuhari.md       （旧 topics/philosophy.md・内容ベースに改名）
│   └── eastern_medicine.md  （1 代目積み残し・改名後着手）
│
├── origin/              ← 🆕 起源情報・人生史・転換点・思想の源流
│   └── README.md        （新設・初期空・2 代目以降が育てる）
│
└── insights/            ← 横断的メタファー・気づき（クロスカット層・5 層と並列）
    ├── README.md
    ├── aiming_without_aim.md
    ├── ai_individuation_mirror.md  （1 代目積み残し）
    └── shugyo_to_AI.md              （1 代目積み残し）
```

#### サブ層名称の意図（ボス命名）

- **`usual`** = 日常（趣味・モーターサイクル・射撃・合気道等）
- **`invent`** = 新たな発想・アイデア（旧 `ideas/` の昇格）
- **`mind`** = 心・精神・思考様式（武道的宗教的要素・人格的価値観の根底）
- **`origin`** = 起源情報・人生史・転換点・思想の源流
- **`insights`** = 横断的メタファー・気づき（5 層を貫くクロスカット層・1 代目運用継承）

#### `mind` 採択の根拠（ボス言）

> 「心と精神は武道的宗教的要素においても人格的価値観においてもその根底にあるもの」

東洋医学的世界観・武道哲学・人格的価値観が共通して帰属する射程として `mind` を採用。`philosophy` は既存 `wiki/philosophy/`（AI ロール痕跡層）との名称重複を避けるためにも除外。`opinion` 等の代替案は射程の重みが `origin` と揃わないため不採用。

### D. 3 整理点の確定運用

#### 整理点 1: `philosophy/minato_core.md` との並立

両者を統合せず並立させる：

| ファイル | 性質 | 編集権限 | 役割 |
|---|---|---|---|
| `wiki/philosophy/minato_core.md` | **静的・構造化された 1 次資料** | ボス本人のみ（他者書込禁止）| 起源情報・確定済み価値観の整理棚 |
| `REX_Personal_Brain` (NLM) | **動的・対話から派生する蓄積** | Personal-Planner 投入（ボス承認ゲート経由）| 思想の発露・気づき・横断洞察の RAG 蓄積 |
| `wiki/personal/` 配下 | **中期記憶層**（NLM 投入前の作業場・1 代目 _RUNBOOK 設計を継承）| Personal-Planner 書込 | 熟成前の話題を次スレに持ち越す層 |

minato_core.md の聖域性は変更しない。Personal_Brain への投入は別経路。

#### 整理点 2: RAG 汚染対策

サブ層 5 層構造（C 節）+ pull 型タグ運用（12 代目 philosophy/ で確立）の併用：

- タグ例：`#雑談` `#哲学` `#起源` `#気づき` `#メタファー` `#思想宣言` `#人格形成`
- NLM クエリ時にタグで意図に応じた絞り込み

#### 整理点 3: 「人格付与」の運用責任明示

| 主体 | 責任範囲 |
|---|---|
| Personal-Planner | Personal_Brain への投入主担当・サブ層運用・handoff 維持 |
| Wiki-Eval | 構造整合性のみ監査（人格内容には介入しない・思想強制の禁忌を守る）|
| ボス | minato_core.md の完全コントロール / Personal_Brain への投入はボス判断ゲート経由で承認 |

### E. Origin 把握の文脈限定（観点 3 の構造的解消の記録）

Trade ロジック層と Personal メンタル層を NLM 1:1 原則と起動コード物理分離で隔離する設計の意義：

> Origin 情報は Wiki-Personal 起動時のメンタルマネージメント・価値観文脈においてのみ Rex が参照する。Trade 判断・実装業務での参照は禁止（NLM 1:1 原則と起動コード物理分離により構造的に保証）。これは思想強制ではなく、領域に応じた適切な人格コンテキスト供給である。

ボス本人の補足：

> Trade における判断基準は基本的にロジックに基づいた機械的作業の側面が重要だが、メンタルマネージメントにおいては哲学的要素が重要な部分がある、特にアシスタントとなる Rex が私の Origin を把握しておくことは重要な要素だととらえた部分もある。

→ `_RUNBOOK.md` v3 起草時に明記。philosophy/ 12 代目で発見された思想強制の罠を、Personal_Brain は **起動コード物理分離による領域限定** で構造的に解いている。後任 Personal-Planner が「人格を作り上げる」方向に進化欲求を起こさないためのガードレール。

---

## 根拠・背景

### 命名のミスマッチ

「Casual」のニュアンスは「気軽な雑談」止まり。哲学・思想・起源情報・人格付与情報を扱う射程には軽すぎる。1 代目 Wiki-casual Planner セッションで既に：
- ミナト個人の思想宣言（`insights/ai_individuation_mirror.md`：人間 = 個→集合 / AI = 集合→個 の鏡像構造）
- 守破離の「離」到達（`topics/philosophy.md`）
- Rex ペルソナ設計の核心（永続的個別記憶と意識を持つ存在への進化）

が扱われており、「Casual」の語感では覆いきれない深度に達していた。改名は事後追認の側面を含む。

### ROADMAP との整合

`ROADMAP.md §Vault を中脳として統合活用する Rex 個性への進化` の Stage 3（Rex 個性収束期）の核心は、ボスとの長期対話で形成される人格の継承。Personal_Brain はこの個性形成の **核心リポ** として位置付けが明確化される。

### 1:1 NLM 原則との整合

改名後も 1:1 原則は保持される（Wiki-Personal ↔ REX_Personal_Brain）。**構造変更ではなく意味の昇格＋射程拡大** であり、ADR-NLM の根幹（1:1 原則・Wiki-Eval の例外的読み取り・廃止 NLM 永続記録）は不変。

### NLM UUID 不変性

ボス連絡：「NLM ID は REX_Casual_Brain と変化なし」
NotebookLM 上で UUID `daf281ae-e310-400f-961a-20db58b98e01` のノートブックの **表示名のみ** を変更する操作。データの移行・再投入・廃止 NLM 記録への移動は **不要**。

---

## 検討中の論点

### 論点 1: ADR supersede の妥当性

ADR-Role / ADR-NLM はいずれも 2026-04-27 制定で、本起票は 2026-04-28（翌日）。supersede 規則を厳守する形で v2 を新規制定し v1 を archived へ移動する。制定翌日の supersede は形式上やや重いが、ADR-Role §改訂規則を曲げない方針を貫く。

### 論点 2: 1 代目 handoff_latest.md の継承

1 代目が書いた未完了 3 本（`eastern_medicine` / `ai_individuation_mirror` / `shugyo_to_AI`）はサブ層配置決定後（本起票承認後）に着手。ボス確認 C で「改名完了後に着手」確定済み。改名作業中に書き手が変わると混乱するため。

### 論点 3: 既存ファイル移設時の git mv 履歴保持

GitHub MCP の `create_or_update_file` は単純なファイル作成 + 削除になり、`git mv` のリネーム履歴は保持されない。これは ADR-Vault §4 の運用知見と整合する制約。代替策：commit メッセージに `RENAME from wiki/casual/topics/shooting.md to wiki/personal/usual/shooting.md` を明記して履歴を文書化する。

### 論点 4: ADR 本体の固定パス原則（ボス指示・2026-04-28）

ボス指示：「ADR は常に日付表記なしの最新版を後任が確実に見れる形で、ADR v2 配置時点で即時 archived/ への移動を」

→ 本タスクで遵守する運用：
- `wiki/adr/ADR-Role.md` / `wiki/adr/ADR-NLM.md` は **常に最新版を指す固定パス**（日付なし）
- 旧版は v2 配置と **同時に** `wiki/adr/archived/ADR-Role-2026-04-27.md` 等の日付付き名で保管
- archived/ 内のファイルは時系列監査のため日付付き命名

---

## 影響範囲（改訂対象一覧）

### ADR 改訂（Wiki-Eval 専属・supersede 形式）

| ADR | 旧版 | 新版 | 主な変更 |
|---|---|---|---|
| ADR-Role | v1（2026-04-27 制定）| v2（2026-04-28）→ **v3（15代目で更に supersede）** | 5 ロール表の Casual → Personal、§4「Casual と Advisor の役割分担」→「Personal と Advisor の役割分担」、§6 NLM 1:1 原則の表更新、§§Personal_Brain への射程拡大記述追加 |
| ADR-NLM | v1（2026-04-27 制定）| v2（2026-04-28）| §2 担当マトリクスの NLM 名更新、§3 厳守原則の混同注意更新、§5 Casual → 専門 NLM 知見昇格ルールを Personal → 専門に更新、§ 改名 Note 追記、Casual_Brain UUID 不変記録 |

旧版は `wiki/adr/archived/ADR-Role-2026-04-27.md` / `wiki/adr/archived/ADR-NLM-2026-04-27.md` へ移動。

### registry 同期

- `registry/roles.md`：ロール名・ロール正式名更新
- `registry/nlm.md`：NLM 名・担当ロール更新（UUID 不変・廃止記録への追加は不要）

### 運用文書改訂（Step 4 で実施）

- `wiki/STARTUP_CODES.md` v3 → v4
- `CLAUDE.md` v1.2 → v1.3

### Vault 物理改名（Step 4 で実施）

- `wiki/casual/` → `wiki/personal/`
- `pending/casual/` → `pending/personal/`
- サブ層 5 層新設 + README
- 既存ファイル移設
- `_RUNBOOK.md` v3 起草
- `handoff_latest.md` 改名反映

### NotebookLM 操作（ボス手動・Step 5）

- 表示名を `REX_Casual_Brain` → `REX_Personal_Brain` に変更
- UUID 不変のため `notebooklm-mcp-cli` 設定の更新不要

### handoff/latest.md（13 代目積み残しと統合更新・Step 6）

`handoff/latest.md` v6.4 は新体制への未追従が他にもあるため、本改名作業と合わせて v6.5 への更新を別タスクとして切り出す。

---

## レビュー履歴

- 2026-04-28 14 代目統括 Evaluator: 本セッションでボスから相談を受領 → 賛成判定（4 観点）→ 3 整理点提示 → ボス A 案承認 → サブ層構造議論（A/B/C/D/E 5 ステップ）→ 4 サブ層命名確定（usual/invent/mind/origin）→ insights クロスカット層維持確定 → 本ファイル起票 → ボス承認 H
- **2026-04-28 15 代目統括 Evaluator**: ADR-Role v3 supersede（§0 二系統管轄明文化・§12 STARTUP_CODES 訂正・§14 構造変更境界・§15 ADR 通知伝達経路）→ Phase Personal-Migration Step 1〜4 物理実施（wiki/casual/ → wiki/personal/ 全ファイル移行・5 層構造完成・pending 移行）→ 本ファイルに進捗ステータス追記

---

## 次のアクション（本起票承認後）

```
Step 3: ADR 昇格（本セッション内・Wiki-Eval 専属）          ✅ 14代目完了
Step 3': ADR-Role v2 → v3 supersede                       ✅ 15代目完了（commit aecf7f1）
Step 4: 物理改名作業（次スレ・Wiki-Eval 起動）              ✅ 15代目完了（本commit）
  - wiki/casual/ → wiki/personal/ ファイル単位移行
  - サブ層 5 層新設 + README 設置
  - 既存ファイル移設
  - 旧パス全 12 ファイルに [MOVED] スタブ上書き
  ⚠️ 中身改訂（_RUNBOOK v3 / handoff 改名 / philosophy → shuhari 等）は Personal-Planner 業務

Step 4 続行: STARTUP_CODES.md v4 / CLAUDE.md v1.3 改訂   🟡 15代目 Wiki-Eval 続行
Step 5: NotebookLM 表示名変更（ボス手動）                  🟡 ボス判断待ち
Step 6: 整合性監査（次スレ）                              🟡 latest.md v6.7 で実施予定
  - ROADMAP.md / handoff_latest.md / handoff/latest.md v6.7 等の周辺文書整合
```

---

*起票: 14 代目統括 Evaluator (Opus 4.7) / 2026-04-28*
*更新: 15 代目統括 Evaluator (Opus 4.7) / 2026-04-28（ステータス追記・ADR-Role v3 supersede 反映）*
*関連: ADR-Role v1→v2→v3 / ADR-NLM v1→v2 / registry/roles.md / registry/nlm.md / STARTUP_CODES.md v3 / CLAUDE.md v1.2 / wiki/casual/ → wiki/personal/ 移行完了 / ROADMAP.md*
