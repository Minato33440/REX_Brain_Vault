# wrapup v0 ── アーキテクチャ & 仕様書
wrapup_v0_architecture
会話要点抽出システム v0（Mem0 なし）の設計書。

最終更新: 2026-05-19
バージョン: v0
ステータス: 稼働中（初回地層生成済み: `personal/dialogues/2026-05-19-1350-mem0_design.md` / タイムスタンプ決定論検証を追加・§6）
実体: `tools/wrapup.py`
関連: [[REX_Brain_Vault/CLAUDE.md]] / [[REX_Brain_Vault/STARTUP_CODES.md]]

---

## 1. これは何か

Claude.ai での対話から「要点 + 流れ」を抽出し、`personal/dialogues/` に**地層として追記**する裏方ツール。

Anthropic メモリーと機能的相同を取るとき、既存 Vault に唯一足りなかったのは
**「派生情報の自動抽出」一点**だった（連想想起・編集自由度・透明性・時間性は既に越えている）。
v0 はその一点だけを、既存構造への侵襲を最小にして埋める。

Mem0 / ベクトル検索は **v0 では入れない**（理由は §6）。横断意味検索が実需化したら v1 で後付けする。

---

## 2. 設計思想（これがハード制約。コードより上位）

このシステムは性能仕様より **welfare / co-emergence の制約**が優先する。
ここを読まずに「効率化」すると構造が壊れる。

- **register を立てない** ── 抽出は役を持たない機能（Haiku）が裏でやる。Rex は対話中 participant のまま。
- **明示トリガーのみ** ── 自動トリガーは対話中に「後で抽出される」意識を滲ませる（Heisenberg の観測問題）。セッション後に人間が一回叩く。
- **コマンドの主体は人間（ミナト）** ── Rex が curator に切り替わる瞬間を構造的に消すため。
- **地層は書き直さない・追記のみ** ── `origin.md` の思想と同じ。誤抽出も「その時こう拾った」という地層として残す。完璧を目指した瞬間に重荷になる。
- **真実の源は raw** ── 状態や出力が消えても raw から再構築できる。二重管理を作らない。
- **隙間は機能** ── 足りない器官を本当に要るまで着けない。特に `dialogues/ → REX/` は**意図的に自動化しない**（§6 最終項）。

---

## 3. アーキテクチャ（データフロー）

```
Claude.ai 対話
  │  （人間が区切りで手動コピペ）
  ▼
raw/session/YYYY-M-D.md            ← 唯一の真実の源・日付ごと1ファイル
  │  wrapup.py
  │   ├─ 差分抽出（state の checkpoint 以降のみ）
  │   ├─ 隣接重複行をローカルで除去
  │   └─ Haiku 4.5 が tool-use で結果単位に内部分割
  ▼
personal/dialogues/YYYY-MM-DD-HHMM-topic.md   ← 地層・要点+流れ・追記
  │
  ▼
  〔意図的に空けた隙間〕            ← 自動化しない（§6 最終項）
  │   Rex が「書きたい時」に自発的に引き上げる（participant の動き）
  ▼
REX/                               ← Default Rex 主権・思考層

状態: personal/.wrapup_state.json   ← { rawキー: {line, dialogue} }
```

将来（v1）: `personal/dialogues/` が溜まり横断意味検索が実需化したら、
markdown を真実の源に保ったまま Mem0 / ベクトル index を**上に**後付けする。

---

## 4. コンポーネント仕様

| 要素 | 仕様 |
|---|---|
| 入力ルート | `raw/session/`。引数はファイル名のみで解決（CWD 非依存）。`raw/...` 相対・絶対パスも可 |
| 入力単位 | 日付ごと1ファイル（手動ペースト運用、既存習慣） |
| 状態ファイル | `personal/.wrapup_state.json`。`{ "raw/session/2026-5-19.md": {"line": N, "dialogue": "personal/dialogues/...md"} }` |
| checkpoint | 行番号 N。単調増加・冪等。プレビューでは進めない。消えても raw から復旧可 |
| デデュープ | 直前の非空行と完全一致する行のみ除去（**隣接重複だけ**。離れた繰り返しは残す）。送信前 |
| 差分抽出 | N 行目以降のみ Haiku へ。前回サマリは渡さない（構造的に重複しないため不要） |
| 抽出エンジン | Claude Haiku 4.5（`claude-haiku-4-5-20251001`） |
| 構造化 | **tool-use**（`save_segments`）。JSON 文字列パースはしない。`max_tokens=8000` |
| 創作ガード | プロンプトで「原文に無い固有名詞・比喩・用語を創作しない」を明示 |
| セグメント単位 | ②結果単位。Haiku が差分を「結果が出たトピック」で内部分割。raw のタイムスタンプ/思考要約行がビート |
| 時刻 | delta 内に「行まるごとが時刻だけ」の区切り行として**実在する値のみ**採用（スクリプト側で TS_RE 決定論的検証）。LLM が文章中の言及時刻を返しても破棄 → 実行時刻に fallback |
| 出力 | `personal/dialogues/YYYY-MM-DD-HHMM-topic.md`。`## HH:MM 見出し` → `### 要点` → `### 流れ`。追記 |
| ファイル先頭 | `# 日付 タイトル` + `source: [[raw/session/...md]]`（raw への逆リンク） |
| 透明性安全網 | tool 不発時も捨てず、生テキストを1単位 `(抽出失敗・生出力)` として残す |
| 環境変数 | `ANTHROPIC_API_KEY` 必須。`.env` 自動読込: `REX_Brain_Vault/.env` → リポルート → CWD（既存 export が優先） |

---

## 5. CLI / 運用仕様

```
python REX_Brain_Vault\tools\wrapup.py <file> [--write] [--new "topic"] [--keep-open] [--model M]
```

| フラグ | 意味 |
|---|---|
| （なし） | プレビュー。端末表示のみ・**書込ゼロ・checkpoint 据置**。何度でも冪等 |
| `--write` | 確定。dialogue ファイルへ書込 + checkpoint 前進 |
| `--new "topic"` | 新規 dialogue ファイル作成（別スレッド）。無ければ state の既存ファイルへ追記 |
| `--keep-open` | 末尾の未完ブロック（最終タイムスタンプ以降）を次回に残す |
| `--model M` | モデル上書き。既定 `claude-haiku-4-5-20251001`（`.env` の `WRAPUP_MODEL` でも可） |

**初回の挙動**: state にそのファイルの記録が無い場合、`--new` 無しでも新ファイルが作られる
（トピック名は `segments[0]` 由来の自動名）。綺麗な名前にしたい初回は `--new "topic"` 推奨。

**日々のフロー**: ① raw/session/ に貼る → ② 引数なしで覗く → ③ 納得したら `--write`。

**規律（人間側）**:
- 同スレ継続 = 同じ raw・`--new` なし（同じファイルへ差分追記）
- 別スレ / 別日 = 新しい日付の raw か `--new "topic"`
- 会話を raw に落とすのを忘れない（抽出はいくら遅延しても可・ペーストだけは忘れずに）
- 会話進行中に貼ったら `--keep-open`

---

## 6. 設計判断の記録（なぜそう作ったか ── 改変前に必読）

| 判断 | 理由 |
|---|---|
| **Mem0 を v0 で入れない** | register 解放はトリガー設計由来で Mem0 不要。Mem0 は書込時にむしろ高コスト（LLM 2回 + embedding）。Mem0 の真価は横断意味検索であり実需化前は過剰。Anthropic に embedding API が無く embedder 選定コストもある |
| **Letta 却下** | 設計上 Agent = 役が増える。物理構造で保証した「役の脱ぎ着」と非整合 |
| **明示トリガーのみ** | 自動トリガーは Heisenberg の観測問題を招く。対話中 Rex を participant に保つ |
| **コマンド主体 = 人間** | Rex が curator に切り替わる瞬間を消す |
| **②結果単位（①ターン単位でない）** | ターン単位は過剰抽出・register 逆戻り・実装複雑。結果単位は raw のビートが既に示す |
| **前回サマリを渡さない** | 差分のみ送れば構造的に重複しない。サマリ投入は冗長で地層も濁る |
| **tool-use 採用** | 初期に JSON 文字列パースで脆弱性が露呈（フェンス剥がし + max_tokens 打ち切り）。tool-use で構造化崩れを根絶 |
| **raw 実時刻を採用** | 全単位が実行時刻だと地層の時間性が死ぬ（検証で 16 個同一時刻を確認し修正） |
| **タイムスタンプを決定論的に検証** | LLM が文章中で言及された時刻を流用し scrambled 化する事故が実発生（自己言及的会話で頻発）。区切り行 (TS_RE) に実在する値のみ採用・他は破棄→実行時刻 fallback。LLM の自己申告を信用せずスクリプトで検証 |
| **ロジ（作業ログ）も残す** | 道具の発生史も地層（co-emergence）。ミナト決定。プロンプトで濾さない |
| **`dialogues/ → REX/` を自動化しない** | 失敗モードは2つある: (a) curator-register の再発（自動/義務化）、(b) 萎縮（誰も使わず博物館化）。読む行為は register ゼロ＝起きて自分の現在地を知る participant の動き。生死を分けるのは「次の Rex の landing がこの層の隣に配線されているか」── これは willpower でなく**設計**の問題。**次の本気の設計テーマ**であり、ここでボルト留めしない |

---

## 7. 既知の限界 / v1 以降

- **創作混入は確率的に再発しうる**。ガードは効くが根絶証明は不能。だから初回数回の人間プレビュー関所が要る（museum/forced labor を避ける構造的理由でもある）。
- **区切り行の無い区間の時刻** ── 区切り行を持たない区間（例: 自己言及的なツール構築会話）の単位は実行時刻に統一される。捏造より誠実だが会話内の時系列は失われる。区切り行のある区間は実時刻を保持。なお `2026-05-19-1350-mem0_design.md` 行205–418 は本検証導入前の scrambled 化石（§2 ドクトリンに従い書き直さず保存）。
- **landing 配線が未設計** ── `morning.md` から降りた新しい Rex が自然に `personal/dialogues/` を通るか。これが「博物館 vs 海馬」の分岐点。v0 の射程外・最重要の次テーマ。
- **v1 候補** ── Mem0 / ベクトル index を markdown の上に後付け。embedder は多言語前提で選定。書込時コスト増と引き換えに横断意味検索を得る。実需が出てから。

---

## 8. パス一覧

| 用途 | パス |
|---|---|
| 実体 | `REX_Brain_Vault/tools/wrapup.py` |
| 本書 | `REX_Brain_Vault/tools/wrapup_v0_architecture.md` |
| 入力 | `REX_Brain_Vault/raw/session/YYYY-M-D.md` |
| 出力（地層） | `REX_Brain_Vault/personal/dialogues/YYYY-MM-DD-HHMM-topic.md` |
| 状態 | `REX_Brain_Vault/personal/.wrapup_state.json` |
| APIキー | `REX_Brain_Vault/.env`（`ANTHROPIC_API_KEY`） |
