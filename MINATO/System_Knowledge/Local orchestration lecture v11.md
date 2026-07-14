# ローカルAIオーケストレーション 初級→中級 講座
### 〜 自分の手で作った環境を「構造」で棚卸しする 〜

> 対象システム: Claude Desktop / Claude Code / VS-Code ACP Plugin / Grok-UI Plugin /
> Hermes Runtime(Grok OAuth) / vault-mcp / Obsidian Vault
>
> ゴール: 「なんとなく動く」→「どの層が何をしているか言語化でき、設計変更できる」
> 副産物: 実践教科書 / 引継ぎ資料 / 同レベルの個人開発者向け教材

---

## はじめに：なぜ「層(レイヤー)」で考えるのか

ツールを **点** で覚えると、増えるほど頭の中が散らかる。
「Hermesって何だっけ」「vault-mcpとObsidianの境目どこ」「Bridgeって結局なに」──
これは**ツールが多いから混乱しているのではなく、それぞれを置く“棚”が無いから**起きる。

この講座でやるのは、棚を1つ作ること。
棚には **層(レイヤー)** と **境界(バウンダリ)** という2本の軸がある。

- **層** = 役割の段(入口・指揮・通信・実行・記憶 …)
- **境界** = 層と層の間の「ここから先は別世界」という線(プロセス境界・認証境界・信頼境界)

新しいツールが出てきても「これは何層で、どの境界をまたぐか」を問えば、必ず棚のどこかに収まる。棚卸とは、手持ちの部品を全部この棚に並べ直す作業のことだ。

> **視点について(2026-06 追記):** この講座は当初「**Claude＝Orchestrator**」という**Claude Desktopから見た視点**で組み立てている。間違いではないが唯一の視点でもない。最後のModule 10で「**orchestrationは入口相対**(Claudeは入口によってOrchestratorにもprovider engineにもなる)」という成熟版に更新する。最初は固定の頂点として読み、最後に相対化する順で問題ない。

---

## Module 1 ── 全体地図：AIシステムの9層

まず1枚の地図。上から下へ「人間の入口」→「実際の処理」へ降りていく。

```
┌─────────────────────────────────────────────┐
│ ① Client / UI      あなたが文字を打つ場所          │  Claude Desktop, Claude Code,
│                    (人間⇔システムの接点)          │  VS-Code, Grok-UI, ブラウザ
├─────────────────────────────────────────────┤
│ ② Orchestrator     「どのツールを・どの順で呼ぶか」  │  Claude本体(推論+ツール選択)
│                    を決める指揮者                 │  「決める=推論」と「回す=オーケストレーション」は別レイヤー
├─────────────────────────────────────────────┤
│ ③ MCP Client       ツールを“呼ぶ側”。規格に従って   │  Claude Desktop内蔵の
│                    リクエストを送る                │  MCPクライアント：「道具ある?」「これ呼んで」と話しかける受付
│ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ④ Transport(通信) ─ ─ ─ ─ ─ │  stdio / HTTP・SSE
│ ⑤ MCP Server       ツールを“提供する側”。           │  vault-mcp, github,
│                    「使える道具一覧」を公開する       │  finviz, grok_oauth_bridge：これらを置いてある「倉庫」
├─────────────────────────────────────────────┤
│ ⑥ Bridge           異種の世界をつなぐ“通訳・通路”    │  BridgeはMCP-Clientの様な接続規格でなく、MCP非対応の外部システムを包む変換アダプタ
│                    (状態は持たない)   　　　　　　　│　MCPプロトコルを話せない異種(Hermes)を「MCPの道具のフリ」をさせて外部と繋ぐために存在する
│                   　　　　　　　　　　              │　grok_oauth_bridge.py という動くコードそのものでもある
├─────────────────────────────────────────────┤
│ ⑦ Agent Runtime    実際に処理を走らせる実行主体       │  Hermes (CLI Runtime)：Hermes=エンジン本体（-z=その回し方の一種）
│                    (セッション・状態を持つ)          │　OAuthセッションやprovider bindingという“状態”を持ち、自分の中でエージェントループを回せる
├─────────────────────────────────────────────┤
│ ⑧ LLM              言葉を生成するエンジン本体        │  Claude / Grok / GPT 等
├─────────────────────────────────────────────┤
│ ⑨ Execution        Python・shell など実際の道具      │  subprocess, git, ファイルIO
└─────────────────────────────────────────────┘
        ┃ 横串 ┃  Memory(短期・会話文脈) / Storage(長期・Vault, NotebookLM, DB)
```

### 補足：④ Transport と ⑥ Bridge の違い（混同しやすい所）

> **Transport(stdio/HTTP) = 通り道(道路)。Bridge = その道に立つ通訳。**

- **Transport** が答えるのは「**どうやって運ぶ?**」── 標準入出力で? HTTPリクエストで? **運ぶだけで中身は変えない**。
- **Bridge** が答えるのは「**何を何に変換する?**」── **中身を翻訳・変形する**。

両者は同じ一本の線の上に同居できる(だから紛らわしい)。Bridgeは必ず何らかのTransportの上に乗るが、役割は別物。
相手が**MCPネイティブ**なら Transport だけで足り(vault-mcp等)、相手が**MCP非対応**(Hermes)のときだけ Bridge を足す。

```
Claude Desktop   ─MCP/stdio──▶  grok_oauth_bridge.py   ─subprocess─▶   Hermes        ─OAuth─▶  Grok
(MCP Client/指揮)               (MCP Server ＋ Bridge)               (Runtime＋Hub/Client)   (リモートLLM)
```

`MCP=規格` / `stdio・subprocess=道路` / `Bridge=翻訳機` / `Hermes=実行ハブ` / `Grok=外の頭脳`
── この5語が別物として並べば、Module 1の地図は手に入っている。

各層を一言で：

| 層 | 一言定義 | あなたのスタックでの例 |
|---|---|---|
| Client / UI | 人間が入力する入口 | Claude Desktop, Claude Code, VS-Code, Grok-UI |
| Orchestrator | ツール選択と実行順を決める指揮者 | Claude(の推論ループ) |
| MCP Client | ツールを呼ぶ側 | Claude Desktop 内蔵 |
| Transport | クライアントとサーバの通信路 | stdio / HTTP(SSE) |
| MCP Server | ツールを提供する側 | vault-mcp, github, finviz |
| Bridge | 異種システムを接続する通路 | grok_oauth_bridge.py |
| Agent Runtime | 処理を実際に走らせる実行層 | Hermes |
| LLM | 文章生成エンジン | Claude, Grok |
| Execution | 実際のコマンド実行 | subprocess.run(), shell |
| Memory/Storage | 記憶 | 会話文脈 / Obsidian, NotebookLM |

> **棚卸ポイント①**
> 「AIシステム = 1個のAI」ではない。**複数の層の集合体**。
> Claudeはそのうち②と⑧を担うだけ。残りはあなたが配線した部品たち。

---

## Module 2 ── プロセスと通信：「誰が誰を起動し、どう喋るか」

層の地図ができたら、次は **動きの物理**。ここが分かると "empty response" 系のバグを自力で切り分けられるようになる。

### 2-1. プロセスの親子関係

プログラムは実行されると **プロセス** という単位で動く。あるプロセスが別のプログラムを起動すると、**親プロセス → 子プロセス** の関係ができる。

```
Claude Desktop (親)
   └─ grok_oauth_bridge.py (子)        ← MCP Serverとして起動される
          └─ hermes -z (孫)            ← subprocess.run() で起動される
                 └─ (Grok / X API へ)
```

`subprocess.run(...)` を実行しているのは **Python(bridge)** であって、Hermesは**「起動される側」**。
この上下関係が分かっていないと、「どこで失敗したか」が永遠に見えない。

### 2-2. 通信方式（Transport）の3種類

層と層は喋り方を選ぶ。主な3つ：

| 方式 | イメージ | いつ使う | 特徴 |
|---|---|---|---|
| **stdio** | 同じPCの中で口頭伝達(標準入出力) | ローカルMCPの定番 | 速い・設定簡単・**同一マシン前提** |
| **HTTP / SSE** | 手紙(リクエスト)と返信 | リモートMCP, Web API | ネット越しOK・ポートやURLが要る |
| **WebSocket** | 電話(つなぎっぱなし) | リアルタイム双方向 | 常時接続・UI連携向き |

> **なぜローカルMCPはstdioを多用するのか**
> 同じPCの中で親が子を起動するなら、標準入力(stdin)に書いて標準出力(stdout)を読むのが一番単純で速い。ポートもURLも要らない。Claude Desktop ⇔ vault-mcp / github / finviz は基本これ。

### 2-3. あなたが踏んだ罠：cp932 / UTF-8 デコード問題

Windowsの標準文字コードは **cp932(Shift-JIS系)**。一方、多くのツールやログは **UTF-8**。
stdio経由で受け取ったバイト列を間違った文字コードで解釈すると、**文字化け or デコード例外**で「空っぽに見える応答」になる。

```python
# 悪い例：OSデフォルト(cp932)任せ → 化ける
result = subprocess.run(["hermes", "-z"], capture_output=True)
text = result.stdout.decode()          # ← cp932で解釈してしまう

# 良い例：明示的にUTF-8、壊れた所は捨てる
text = result.stdout.decode("utf-8", errors="replace")
```

> **棚卸ポイント②**
> 「応答が空」=「LLMが黙った」とは限らない。**通信路(Transport)や文字コードで落ちている**ことが多い。層で考えると、犯人を「LLM」ではなく「Transport層」に絞り込める。
>
> ※実際、Hermesの“空応答”はLLMではなく **inference provider の binding が外れていた**(`hermes auth` とは別物。`hermes model` で provider 再選択が必要)という、もっと下の層の問題だった。これも「層で切り分ける」の典型例。

---

## Module 3 ── MCP の正体：プロトコルであって、ソフトではない

ここが初級者が一番つまずく所。

### 3-1. MCP = Model Context Protocol = 「規格」

MCPは**アプリの名前ではない**。**「AIにツールを使わせるための共通の喋り方(プロトコル)」**。
USBに例えると分かりやすい：

- **USB規格** = MCP(決まり事)
- **USBポート(PC側)** = MCP Client(呼ぶ側)
- **USB機器(マウス等)** = MCP Server(提供する側)

USBという「規格」のおかげで、どのマウスもどのPCに挿しても動く。
MCPも同じで、規格に従ってさえいれば、Claudeはvault-mcpでもgithubでもfinvizでも同じやり方で呼べる。

### 3-2. Client と Server の役割分担

```
[Claude Desktop]                          [vault-mcp]
  MCP Client                               MCP Server
     │   1. 「使える道具ある？」(tools/list)    │
     │ ───────────────────────────────────▶ │
     │   2. 「obsidian_read, search…あるよ」  │
     │ ◀─────────────────────────────────── │
     │   3. 「searchを"gold"で呼んで」(call)   │
     │ ───────────────────────────────────▶ │
     │   4. 結果(検索ヒット)を返す              │
     │ ◀─────────────────────────────────── │
```

MCP Serverは起動時に**「自分が提供できる道具の一覧」**を公開する。Claude(Orchestrator)はその一覧を見て「今はこれを呼ぶ」と決める。これが ② Orchestrator と ⑤ MCP Server の協調。

### 3-3. あなたのMCP Serverたち

| MCP Server | 提供する道具 | 層でいうと |
|---|---|---|
| vault-mcp | Obsidianノートの読み書き・全文検索(REST API経由) | ⑤→Storage(Obsidian) |
| github | Issue/PR/ファイル操作 | ⑤→外部API |
| finviz | スクリーニング・株式ファンダ | ⑤→外部API |
| grok_oauth_bridge | Hermes Runtime への橋渡し | ⑤かつ⑥(Bridge) |

> **棚卸ポイント③**
> 「MCPを入れた」と言うとき、実際に入れたのは **MCP Server(道具箱)**。
> Client(呼ぶ側)はClaude Desktopに最初から内蔵されている。

---

## Module 4 ── 最重要：Bridge と Runtime の違い

ここが今までで一番こんがらがっていた所。**この区別が付けば棚卸の半分は終わり**。

### 4-1. 3つの言葉を分ける

| 言葉 | 正体 | 状態を持つ? | たとえ |
|---|---|---|---|
| **MCP** | 通信の**規格** | — | 言語(日本語) |
| **Bridge** | 異種世界をつなぐ**通路・通訳** | 持たない(通すだけ) | 通訳者 |
| **Runtime** | 処理を実際に走らせる**実行主体** | 持つ(セッション等) | 工場 |

### 4-2. あなたの構成での流れ

```
  ┌──────────────┐   MCP     ┌────────────────────┐  subprocess  ┌─────────────┐
  │ Claude Desktop│─(stdio)─▶│ grok_oauth_bridge.py │──────────────▶│   Hermes    │
  │  (MCP世界)    │           │     = Bridge         │   hermes -z   │ (Runtime世界)│
  └──────────────┘           └────────────────────┘               └──────┬──────┘
                                                                          │ OAuth session
                                                                          │ reuse
                                                                          ▼
                                                                    Grok / X API
```

- **Bridge(grok_oauth_bridge.py)** は、Claudeの「MCP世界」とHermesの「Runtime世界」という**別言語圏**をつなぐ通訳。自分では仕事をしない。**通すだけ**。
- **Runtime(Hermes)** が、実際にGrok/Xを叩いて成果を作る**工場**。OAuthセッションや実行状態を**持つ**のはこっち。

### 4-3. 「Claudeが認証しているわけではない」の意味（OAuth session reuse）

直感に反するが重要：

- ❌ Claude Desktop が Grok に OAuth ログインしている
- ⭕ **Hermes が、以前ログインして保存済みの OAuth セッションを再利用**している
- つまり Claudeは「Hermes、お前ログイン済みだろ、これやっといて」と**依頼しているだけ**

```
Claude   : 「x_searchして」
Bridge   : (そのまま渡す)
Hermes   : 「自分はログイン済み(セッション保持)」→ 実行 → 結果
```

> **棚卸ポイント④**
> Bridge=通路、Runtime=工場、MCP=言語。
> 「Hermesは“ツール”ではなく“Runtime(実行主体)”」── ここが腑に落ちると、
> 「Bridgeを直してもダメ、Runtimeのprovider bindingが原因」みたいな切り分けが自分でできる。

### 4-4. 「MCPが2つ連なっている」わけではない

Hermes経路は2ホップあるが、**MCPなのは左半分だけ**。正しくは **本物のMCP ×1 + ただのCLI呼び出し ×1**。

```
[Claude Desktop]          [grok_oauth_bridge.py]            [Hermes]          [Grok/X API]
 MCP Client  ──本物のMCP──▶  MCP Server ＋ Bridge ──subprocess──▶ Runtime ──OAuth──▶  (宛先)
 (呼ぶ側)     (stdio/規格に              (右はtools/listも
              従った会話)                handshakeも無い。
                                         ただのコマンド起動)
```

- **左(Claude Desktop → bridge)** … 本物のMCP。`tools/list`で道具一覧、`call`で呼ぶ、あの作法。
- **右(bridge → Hermes)** … MCPもどきですら無く、`subprocess.run(["hermes","-z", ...])` で**コマンドを起動して標準出力を読むだけ**。プロトコルの握手は一切無い。
- **Bridgeは1個**。`grok_oauth_bridge.py` という1プログラムが、左を向けばMCP Server、右を向けばHermes起動係(Bridge)、の**二役**を持つだけ。

> なぜ効くか ── **どっちの半分で落ちたかで疑う場所が変わる**。
> 左で失敗=MCPの問題(config.json, stdio, 道具未登録)。右で失敗=**MCPと無関係**のCLI問題(hermesがPATHに無い, provider binding未設定, cp932デコード, OAuthセッション切れ)。
> 例の“空応答→provider binding”は右半分の故障。だから`hermes auth`でなく`hermes model`で直った。

### 4-5. LLM(Grok)はHermes「の中」で動いていない（ローカル vs リモート）

直感に反するが重要 ── **Grokの推論は xAIのサーバ(リモート)で起きる**。Hermesはその呼び出し元(クライアント)。

```
[あなたのPC]                                    [xAIのサーバ(クラウド)]
 grok_oauth_bridge.py                              ┌──────────────┐
   └─ hermes -z ──┐                                │  Grok 本体    │
        Hermes     │  自分の中で回すのは           │ (LLM推論はここ)│
        ┌──────────┴──────────┐                    └──────▲───────┘
        │ エージェントループ    │── OAuthで認証して ────────┘
        │ ＋ ツール実行(ローカル)│   リモートに推論を“投げる”
        └─────────────────────┘   (結果を受け取って終了)
```

Hermesが**自分の中で**回すのは「エージェントのループ」と「ローカルのツール実行」だけ。重いLLM計算はボスのPCには無い。`-z`(ワンショット)=「1回投げて受けて終了、対話セッションは持たない」モード。

> これは**Claude側もまったく同じ**(Claudeの推論もAnthropicのサーバ上)。
> ボスのPCにあるのは終始**オーケストレーションの配線**だけ、頭脳(LLM)は両方とも外。

### 4-6. OAuthセッション と provider binding は別物

“認証された状態”を1語で潰さない。これを分けられるかが、空応答バグの切り分け力そのもの。

| | 正体 | 例の事故 |
|---|---|---|
| **OAuthセッション** | ログイン credential(Grokに繋ぐ権利) | OKだった(`hermes auth`通過) |
| **provider binding** | どのprovider/modelに繋ぐかの**設定** | こっちが外れていた → `hermes model`で再選択して復旧 |

Hermesは **(1)OAuthセッション** と **(2)provider binding** を**両方**保持して初めて動く。
認証の手段はOAuthでもAPIキーでもよい(“または”は正しい)が、binding は credential とは別レイヤー。

### 4-7. Hermes = Runtime ＋ Hub/Client（橋とハブは別の場所にある）

"Bridge"という語は上流の `grok_oauth_bridge.py` 1個に予約。HermesがGrok等のLLMと繋ぐ所は"Bridge"ではなく **providerのクライアント**。

- `grok_oauth_bridge.py` = **Bridge**(Claudeの MCP世界 ↔ Hermes世界)
- **Hermes** = **Runtime ＋ Hub/Client**(Hermes → 各LLM provider)

ハブが効く理由 ── **provider binding を差し替えるだけで繋ぐLLMを変えられる**。今日はGrok/OAuth、別providerに替えても上流のClaude側は中の事情を知らずに済む(疎結合)。

> **訂正：「Gatewayは未来テーマ」→ 既に現役だった**
> 当初ここに「GatewayでMCPを束ねるのは将来」と書いたが、実機ではGatewayもProxyも稼働済み。
> ただし2種類に分けて理解する:
> - **Hermes Gateway** … messaging(Discord/Telegram/Slack)＋cronの常駐デーモン。
> - **Hermes Proxy** … OAuth/provider stateを一元化するOpenAI互換HTTP窓口(localhost:8000)。
> どちらも「MCP ServerをMCPで連ねるプロキシ」とは別物(Hermesは多provider/多protocolのHub)。詳細は4-8。

### 4-8. 状態競合 と Proxy ── 4-6のバグの“真因と恒久対策”

4-6で見た「provider bindingが外れて空応答」── あれは単発の事故ではなく、**構造的な状態競合**だった。

複数のクライアント(Claude Desktopのone-shot / Discord gateway / Grok-UI 等)が**同じ`HERMES_HOME`のprovider stateを共有**していると、片方が`x_search=true`、もう片方がprofile/providerを切替…と**互いの設定を奪い合う**。誰かの操作でbindingが外れ、別経路が空応答になる。

```
Before(競合):                        After(分離):
 gateway: x_search=true              Gateway → hermes proxy start --provider xai
 oneshot: hermes -z                    └ localhost:8000/v1/chat/completions
   └ profile/provider が外れる        全クライアント → proxy → Grok (state一元化)
```

**Hermes Proxy**(`hermes proxy`, localhost:8000, OpenAI互換)が**OAuth/provider stateを1箇所で所有**し、各クライアントはHTTP API経由でそこに繋ぐ。これで「共有可変状態の奪い合い」が「単一所有者＋経由するだけのクライアント」に変わる。

> **棚卸ポイント④-b**
> 4-6で「bindingはcredentialと別物」と分けたのが効く所。
> 真因は「**可変なprovider stateを複数プロセスで共有してた**」こと。
> 対策はクラシックな並行制御 ── 状態の所有者を1つ(Proxy)に集約し、他は経由するだけにする。

### 4-9. 状態競合の3つの解（実機で出揃った）

同じ「4-8のbinding競合」に、ボスのスタックでは**3つの解**が実装/確認された ── 全部「**可変stateを共有しない＝隔離 or 単一所有**」の変奏:

| # | 解 | どこ | 状態の扱い | 確認 |
|---|---|---|---|---|
| (1) | **Proxy中央集約**(`hermes proxy` :8000) | Grok-UI経路(退役) | 単一所有 | doc |
| (2) | **`-p grok` 都度固定** | Claude Desktop bridge | 都度パラメータ化(global非依存) | コード(`grok_oauth_bridge.py`) |
| (3) | **Gatewayプロセス隔離** | 常駐マルチBot | プロセス毎に各自所有 | stop-test(8-6) |

**Proxy ≠ Bridge(重要):** Proxyは*同一プロトコルの転送＋状態の単一所有*(:8000のHTTP面)、Bridgeは*プロトコル変換*(MCP↔hermes CLI)。別物。Proxyの恩恵を受けてたのは**Grok-UI経路(Surface 2)**で、bridgeは `-p grok` で**globalを読まない**から最初からProxy非依存(Surface 1)。だからProxyが退役/不在でもbridgeは競合しない。

### 4-10. システム各層境界の相互通信まとめ（混ぜない5語）

層の境界をまたぐ通信を、混同しやすい語を分けて一覧化する。**規格 / 道路 / 起動手段 / 翻訳機 / 実行ループ** ── この5つを混ぜないことが、境界の相互通信を読む鍵。

```
MCP            = 規格(USB規格そのもの)
MCP-Client     = 規格に従って呼ぶ側(ポート/ホスト)   ← Claude Desktop, Hermes
MCP-Server     = ツール置き場(呼ばれる側)            ← vault-mcp, obsidian-mcp, grok_oauth_bridge
stdio          = 道路(データ経路)。ネイティブMCPはこれだけでいい
subprocess     = 子プロセスを起動する手段(道路ではない)。MCP/非MCP両方で使う
Bridge         = 翻訳機。MCP非対応を繋ぐ。grok_oauth_bridge.py = 左はMCPサーバー/右はhermes起動係
Hermes         = Runtime＋異種LLMハブ＋MCPクライアント。機械ループは回すが"判断する脳"は無い
  ├ one-shot(-z)  … bridge経由。ループ1回→終了
  ├ gateway(常駐) … 持続ループ ← AgentTeamはこれ
  └ acp           … 対話セッション
LLM            = 外部脳(指揮役)。Hermesがauth保持した状態で投げ、推論はリモート→結果を回収
```

**取り違えやすい3点(ここだけ押さえれば迷わない):**

1. **Client ≠ 規格** ── 規格はMCPそのもの(USB規格)。Clientは"呼ぶ側"(ポート)。
2. **subprocess ≠ 道路** ── 道路はstdio(データ経路)。subprocessは"子プロセスを起動する手段"で、非MCPの `hermes -z` 起動にも使う。
3. **エージェントループは経路依存** ── 「ワンショット」はbridgeの `-z` だけ。**gateway(常駐)は持続ループ**で、AgentTeamの土台はこちら。

**所有者の確認:** authを保持するのは**Bridgeでなく Hermes**(OAuthセッション再利用)。推論は**リモート**(xAI/Anthropic)で起き、Hermesが回収して bridge→Claude へ戻す。

> **棚卸ポイント④-c:** 境界の相互通信で迷ったら、その通信を5語に割り当てる ──「これは*規格*か、*道路*か、*起動手段*か、*翻訳機*か、*実行ループ*か?」。混ざってなければ、もう読める。

---

## Module 5 ── 認証(Auth)とセキュリティ境界：便利さは攻撃面とトレードオフ

中級の入口。**「どこからどこまでが信頼できる範囲か(信頼境界)」**を引けるかどうか。

### 5-1. 信頼境界という考え方

システムには「ここから内側は信頼する/外側は疑う」という線がある。
**認証(Auth)は、その線を越える時の関所**。関所が緩いと、内側の強力な道具が外部から使えてしまう。

### 5-2. あなたの実例：Hermes-Discord プリセットのRCEリスク

これは教材として完璧な実例。

```
[Discordサーバ] ──(メッセージ)──▶ [hermes-discord preset]
                                       │
                                       ▼  _HERMES_CORE_TOOLS をフル搭載
                            terminal / file R/W / code実行 /
                            browser / delegate_task / cronjob / computer_use
```

問題の構造：
- このプリセットは **terminal実行・ファイル読み書き・コード実行** まで含むフル装備
- そして**認証境界が「Discordサーバに入っているか」だけ**
- = Discordに入れた人 ≒ あなたのPCで任意コマンドが撃てる(**RCE級**)

### 5-3. 境界を引く3原則（remediation）

| 原則 | 具体策 | 効果 |
|---|---|---|
| **最小権限** | Discordプラットフォームでは危険ツールを無効化 | 攻撃面を削る |
| **隔離** | `terminal.backend` を **Docker** に切替 | 実行をコンテナに閉じ込め、ホストを守る |
| **allowlist** | `allowed_channels` を限定 | 入口そのものを絞る |

> **棚卸ポイント⑤**
> 「便利な万能プリセット」ほど **攻撃面が広い**。
> 機能を足すたびに「この境界、誰が越えられる?」を1回問う癖をつける。
> Dockerは“便利と安全”を両立させる定番の隔離壁。

### 5-4. スポーク別の信頼境界（実機校正）

経路が4つあると、**信頼境界の堅さもバラバラ**。一律ではなく経路ごとに見る。

| 経路 | 信頼境界 | 堅さ | ツール露出の主因 |
|---|---|---|---|
| **Discord**(gateway) | サーバーメンバーシップ | 緩 | Profileの`hermes tools`が核 |
| **Grok-UI** → obsidian-mcp | localhost＋APIキー＋PathPolicy | 中〜堅 | サーバ側でコード強制ガード |
| **ACP**(VS-Code) | ローカルのエディタセッション(単一ユーザー) | 堅 | 自分のワークスペース |
| **Claude Desktop**(bridge) | ローカルのDesktop | 堅 | workdir allowlist＋Vault聖域保護＋terminal/computer-use除外 |

**良い手本: obsidian-mcp-server。** Obsidianアクセスは全部`getObsidianService()`の単一窓口、パスは`assertReadable/Writable`(PathPolicy)で上流HTTP前にゲート、`OBSIDIAN_READ_ONLY=true`で全write殺し、破壊的なcommand系は既定OFF(opt-inのときだけ`tools/list`に出る)。**安全制約をドキュメントでなくコードに焼く**方針 ── ボスのスタックで一番堅いスポーク。

**要対応: Discord。** 一番緩い境界(サーバーメンバーシップ)なのに、Profileの`hermes tools`がコア危険系(terminal/file/code/cronjob)を含むと、メンバーのメンション＝任意実行。**obsidian-mcp-serverのガード思想(コード強制・READ_ONLYキル・opt-in)をDiscord向けProfileにも移植する**のが筋。

**もう一つの好手本: `grok_oauth_bridge.py`。** `ask_grok`=書込なし(x_search/visionのみ)、`grok_work`=`_check_workdir`で `C:\Python\REX_AI` 配下に限定＋`REX_Brain_Vault`(聖域)を明示deny、**terminal/computer-useは両方とも除外**。obsidian-mcpと同じ「ガードをコードに焼く」思想がbridge側にも効いてる。

> **棚卸ポイント⑤-b**
> 「一番緩い境界が、一番強い道具に届く」状態を作らない。
> obsidian-mcp(堅)を基準に、Discord(緩)を引き上げる。

---

## Module 6 ── 環境の再現性：venv / requirements / 設定ファイル

「自分のPCでは動くのに…」を撲滅する層。

### 6-1. venv = プロジェクトごとの冷蔵庫

```powershell
python -m venv .venv                       # 冷蔵庫を作る(.venv)
.\.venv\Scripts\Activate.ps1               # 冷蔵庫に入る(毎回)
pip install <library>                      # 中にだけ食材を入れる
pip freeze > requirements.txt              # 今の中身をメモ
# 別PC/引継ぎ時：
pip install -r requirements.txt            # 同じ中身を再現
```

プロジェクトごとに冷蔵庫を分けるから、ライブラリのバージョン衝突が起きない。
**今どのPythonを使ってるか確認**(超重要)：

```powershell
python -c "import sys; print(sys.executable)"   # パスに .venv が入っていればOK
```

### 6-2. 設定ファイル = オーケストレーションの「配線図」

`claude_desktop_config.json` は、Claude Desktopが**どのMCP Serverを・どう起動するか**を書いた配線図。ここに各サーバの起動コマンドと環境変数を書く。

> **あなたが踏んだ罠：環境変数が子プロセスに伝播しない**
> Claude DesktopはOSの環境変数をMCP子プロセスに**自動では渡さない**。
> なので `GITHUB_PERSONAL_ACCESS_TOKEN` は、OS側に設定しても効かず、
> **config.json の中に直接書く**必要があった。
> → 「設定したのに認証されない」時は、まず**「その値、子プロセスまで届いてる?」**を疑う。

> **一般解（実機）: `_rich_env()`。** `grok_oauth_bridge.py` は、Claude Desktop→uv が痩せさせた env を、**Windowsレジストリ(HKLM＋HKCU)からフル再構築**して子プロセスに渡す。「どの変数が要るか当てる」のでなく「**痩せ自体を解消**」する手 ── config直書きより漏れが出にくい。

> **棚卸ポイント⑥**
> venv=再現性のため、config=配線のため。
> 引継ぎ資料に必要なのは「コード」より、この **requirements.txt と config の差分**。

---

## Module 7 ── バージョン管理と安全な改修：git / rtk

改修で壊しても必ず戻れる、を保証する層。

### 7-1. 切り出しの鉄則

```bash
git commit -m "before refactor: working state"
```

> **切り出し前に必ずコミット。各Stepの前後にもコミット。これさえやれば何があっても戻れる。**

リファクタや構成変更は「動く状態」を1点必ず刻んでから入る。これが**心理的な安全網**になり、大胆に変えられる。

### 7-2. rtk = git のラッパー

`rtk` は git コマンドを前置きで包む独自ラッパー。素のgitを直接使わずrtk経由にすることで、
**プロジェクト固有の作法(パス・認証・前処理)を一箇所に集約**できる。
「全gitコマンドはrtkで前置きする」という運用ルール自体が、ミスを構造的に減らす仕組み。

> **棚卸ポイント⑦**
> ツールを“素のまま”使わず**薄いラッパーで包む**のは中級の定石。
> rtk(git), bridge(hermes) … あなたは既に同じパターンを複数回使っている。

---

## Module 8 ── オーケストレーター/経路の比較（実機確定版）

「フロント(指揮者)」は1種類じゃない。棚卸しの核心は ── **Hermesという1つのRuntimeに4つの“front door(経路)”があり、全部が同じ土台(`HERMES_HOME`のprofiles＋OAuth資格情報)を共有する**こと。

### 8-1. 4つの経路（すべて実機確認済）

| # | フロント | Hermes実行モード | プロトコル(外側) | 主な用途 |
|---|---|---|---|---|
| **A** | Claude Desktop | `hermes -z`(one-shot) | MCP/stdio → subprocess | Grok / X |
| **B** | Discord/Telegram/Slack | `hermes gateway`(常駐) | discord_platform adapter | チャットBot |
| **C** | VS-Code Hermes-Agent拡張 | `hermes acp` | ACP(JSON-RPC/stdio) | コーディング |
| **D** | Grok-UI(grok.com)＋専用Plugin | Runtime(Proxy経由) | HTTP(8000,OpenAI互換)→MCP/stdio | Obsidian読み書き |

> **Claude Code**は5つ目のフロントというより、A経路の“bridge抜き版” ── ネイティブ・ターミナルを持つので`hermes -z`を直接叩ける。重い改修・自動化(Trade_Brain等)はClaude Codeが正しい指揮者。

> **現状アップデート（実機・2026-06時点）:** **D(Grok-UI/grok.com)経路は退役**。ngrokのゾンビ化 → Gateway切替 → Proxy導入と進化した後、Hermes公式の **Hermes-Desktop** と **IDE用Plugin** が「クライアントハブ」としてリリースされ、現在は **Hermesから直接Grokを駆動**(grok.com連携は不使用)。新コンポーネント＝ §C(`hermes acp`)機構の公式パッケージで、ログイン承認時に共有設定を自動取り込み(確定は8-5)。変遷は8-5。

### 8-2. 同じHermes、front doorで“役”が変わる

| 経路 | 駆動するのは | Hermesの役 | 頭脳(LLM) |
|---|---|---|---|
| **C** ACP / **B** gateway / **D** Grok-UI | エディタ/チャット/Grok-UI | **エージェント本体** | Grok or Opus |
| **A** MCP bridge | Claude | **Claudeが呼ぶ下流ツール** | Claude |

ACP・gateway・Grok-UIでは**Hermesがエージェント**(背後のGrok/Opusが頭脳)。MCP bridge経由だけ**HermesがClaudeの“道具の1つ”に格下げ**され、頭脳はClaude側。Module 4の「ACP＝エディタ↔エージェント / MCP＝エージェント↔ツール」が実機で現れた形。

### 8-3. multi-provider Hub（Grokだけじゃない）

Hermesはprovider非依存のHub:
- **xai-oauth** → grok-4.3, x_search, vision(SuperGrokサブスク)
- **anthropic** → claude-opus-4-8(`~/.claude/.credentials.json`のClaude Code OAuthを流用・追加課金なし)
- `/model` でセッション内にprovider切替(grok ⇔ claude)

「Grokブリッジ」と呼んでた基盤が、実はClaude Opusまで配ってる。

### 8-4. Proxy ── 経路が増えた代償の解（→4-8）

D経路で出てきた **Hermes Proxy(localhost:8000, OpenAI互換)** が、全クライアントのOAuth/provider stateを一元管理し、4-6で見た「状態の奪い合い→空応答」を構造的に解消する。詳細は4-8。

### 8-5. 経路の変遷（なぜ今の形か）

棚卸しで一番効くのは「各レイヤーが**前の世代の痛みを解消するために生えた**」という因果。Obsidian/Grok系の経路はこう進化した:

| 世代 | 構成 | 解消した痛み / 生んだ痛み |
|---|---|---|
| **①初代** | Grok-UI Plugin → **ngrokトンネル** → vault-mcp(FastMCP/Python) | 外部公開で繋いだが、**ゾンビトンネル化**して不安定 |
| **②Gateway** | Grok-UI → **Hermes Gateway** → Runtime | トンネル不要に。但し**「空応答→binding未設定」が再浮上**(状態競合) |
| **③Proxy** | 全クライアント → **Hermes Proxy(8000)** → Grok | provider stateを一元化し競合を**恒久解決**(→4-8) |
| **④現在** | **Hermes-Desktop / 公式IDE Plugin**(クライアントハブ) → Hermesが**Grok直結** | §C(`hermes acp`)機構の**公式パッケージ**。ログイン承認で共有設定を自動相続。**Grok-UI(grok.com)は退役** |

→ ①→④は「不安定トンネル → 集約Gateway → 状態の単一所有(Proxy) → 公式クライアントハブ」という、**“共有可変状態をどう飼い慣らすか”の一本道**。③で獲得した「状態の単一所有」思想が、④で公式プロダクト(Desktop/IDE hub)に結実した、と読める。

> **解決（2026-06 更新・実機確認済）:**
> ④の **Hermes-Desktop / 公式IDE Plugin は、③C(`hermes acp`)と同一機構の“公式パッケージ”**。新機構ではない。
> - 新規インストール時の**ログイン承認**で、共有の `HERMES_HOME` profiles ＋ `~/.claude/.credentials.json`(OAuth) を**自動取り込み** → 即利用可。手動の `hermes.path` 設定すら不要(§Cのjoaompfp版より楽)。
> - 機能的には **§C の ACP構成docがそのまま正本**(publisherの差は機構に影響しない)。
> - 同一Runtime/プロファイルを使うため、**obsidian-mcp も同じ仕組みで引き続き利用可能**。

> **棚卸ポイント⑧ ── 2つの“単一化”が効いている**
> 新クライアントが「ログインしただけで全部使える」のは、9-1の**共有の土台**の配当。
> - **状態の単一所有(Proxy)** … provider stateを1箇所が持つ → 奪い合いが消える(4-8)
> - **設定の単一土台(HERMES_HOME ＋ ~/.claude OAuth)** … 新クライアントは*認証1回で設定一式を相続*する
> 増えるクライアントを楽に飼い慣らす鍵は、この2つの単一化に集約される。

### 8-6. Agent-Team ── 常駐マルチエージェントが実機で立った

「1 Profile = 1 常駐エージェント」を**複数同時**に走らせられることを実機で確認(grok ＋ Ai の2 Gateway並走、各自のDiscord Bot、相互通信あり)。

- **独立性の証明(stop-test):** Ai Gatewayを停止→Ai Botは無応答、再起動→復活。**各Gatewayは自プロセスで自Profileを処理**している(機能は独立 ── これはログの見え方とは無関係)。
- **隔離の仕組み:** 各Gatewayが `profiles/<name>/` の `config.yaml`＋`.env`(model/provider/Discordトークン)を**自プロセスに読み込んで保持**。global可変stateを共有しないので競合しない ── 4-9の解(3)そのもの。
- **エージェント間バス:** Discordが事実上のメッセージバスになり、メンバー同士が連絡できる。
- **共有されるもの＝OAuthとその枠:** provider OAuth(xai SuperGrok等)は `HERMES_HOME` の共有ストア。だから**xaiでN体並べると1つのSuperGrok日次枠を食い合う** ── Team拡張の上限はここ。
- **観測性(per-agent log):** 新版はCMDコンソール出力を意図的にカットし、詳細ログは **`profiles/<name>/logs/gateway.log`** に**エージェント毎に分離**して構造化記録(`inbound message` / `response ready: time, api_calls, chars` / `Sending response`)。コンソールのインターリーブが無く、**Team監視はむしろ好都合**。特に `api_calls` は上の**共有OAuth枠の消費をagent毎に追える信号**で、枠の食い合いをログから監視できる。

| Team構成要素 | 実体 | 状態 |
|---|---|---|
| 常駐エージェント | per-profile `hermes gateway`(独立プロセス) | ✅ 複数並走確認 |
| 個別アドレス | profile毎のDiscord Bot/トークン | ✅ |
| 相互通信 | Discord(messaging bus) | ✅ |
| 共有リソース | http-Obsidian(:3011/:3010)、共有OAuth | ✅(枠は共有=上限) |
| 安全分担 | obsidian-mcp `READ/WRITE_PATHS` でagent毎にスコープ | 推奨(Module 5) |

> **棚卸ポイント⑨ ── 退役した多エージェントの“インフラ再来”**
> かつてのPlanner/Evaluator(retired)が、より綺麗な土台で常駐Teamとして戻ってきた形。
> 鍵は「**各エージェントが自分の状態を自プロセスで所有**(4-9の解3)＋**共有は読み取り中心のリソースだけ**」。
> 拡張時の現実的ボトルネックは計算でもプロセスでもなく、**共有OAuthの日次枠**。

---

## Module 9 ── 棚卸の完成図：あなたのスタック全景（実機確定版）

### 9-1. 土台と経路（現行＋退役）

> 現行の入口は **Hermes-Desktop / 公式IDE Plugin**（クライアントハブ）。下図のD(Grok-UI)は退役だが、obsidian-mcpチェーンの動作原理として残す。


```
        ┌──────────── 共有の土台: HERMES_HOME ────────────┐
        │ profiles/ grok(grok-4.3/xai) claude(opus/anthropic) ai │
        │ OAuth: xai-oauth(SuperGrok) ／ anthropic(~/.claude/...) │
        └───────────────────────▲────────────────────────┘
                                │ 全経路が同じ土台を読む
   ┌──────────┬────────────────┼───────────────┬───────────────┐
   │ (A)       │ (B)             │ (C)            │ (D)            │
 Claude Desktop  Discord等        VS-Code拡張       Grok-UI+Plugin
   │ MCP/stdio  │ adapter         │ ACP/stdio       │ HTTP(8000)
 grok_oauth_bridge│              hermes acp         ▼
   │ subprocess │                 │            Hermes Proxy(8000, OpenAI互換)
  hermes -z    hermes gateway     │             └ provider state一元化
               (messaging+cron)   │                 ▼
                                              Hermes Runtime(grok)
                                                  │ MCP/stdio (spawn)
                                                  ▼
                                          obsidian-mcp-server(TS, 14 tools)
                                                  │ HTTP Bearer
                                                  ▼
                                          Obsidian Local REST API(27123)
                                                  ▼
                                              Obsidian Vault
```

### 9-2. Grok-UI → Vault のデータフロー（※D経路は退役・obsidian-mcpの動作原理として保存）

1. grok.comで「○○ノートを探して要約」
2. 専用Plugin → Proxy(8000) → Hermes Runtime(grok-4.3/xai)
3. Grokが `obsidian_search_notes("○○")` を選択
4. Runtime(MCP client) → obsidian-mcp-server(stdio)
5. ハンドラ → `getObsidianService()` → `PathPolicy.assertReadable`
6. → Obsidian REST(Bearer, 27123) → Vault検索
7. 結果を正規化 → Grokが要約して返答

### 9-3. コンポーネント早見表

| コンポーネント | 種別 | 層 | 接続先 |
|---|---|---|---|
| Claude Desktop / Code / VS-Code拡張 / **Hermes-Desktop / 公式IDE Plugin** | フロント | ①UI | Hermes各経路 |
| Grok-UI(grok.com) | フロント（**退役**） | ①UI | — |
| grok_oauth_bridge.py | MCP Server＋Bridge | ⑤⑥ | hermes -z |
| Hermes Gateway | 常駐(messaging+cron) | — | Discord等 |
| Hermes Proxy | OAuth/state一元化(HTTP 8000) | — | 全クライアント |
| Hermes Runtime | 実行ハブ(multi-provider) | ⑦ | Grok/Opus, MCP spawn |
| obsidian-mcp-server | MCP Server(TS, 14 tools) | ⑤ | Obsidian REST |
| github / finviz | MCP Server | ⑤ | 外部API |
| Obsidian Local REST API | Vaultの窓口 | Storage | Vault |
| Obsidian Vault | 長期記憶 | Storage | — |
| NotebookLM | 長期記憶 | Storage | — |

> **Obsidianアクセスは経路別の“共存”(完全移行ではない):** Grok-UI経路は **obsidian-mcp-server(cyanheads/TS, stdio)**、Claude Desktop bridgeは **vault-mcp(FastMCP/Python, http:3011)** の `vault_*` ツールを今も保持。「vault-mcp→obsidian-mcp 完全移行」ではなく、**経路ごとに別のObsidian窓口が併存**(初代のngrok経路だけが退役)。

---

## Module 10 ── 異種マルチLLM Agent-Team（実機到達）と次の地平

ここまでの棚卸しの“その先”。実機で到達した地点と、そこから見える次の課題。

### 10-1. 成熟版の視点：orchestrationは入口相対

冒頭では「Claude＝Orchestrator(②)」として始めた。これは**Claude Desktopから見た視点**で、間違いではないが唯一でもない。全スタックを見た今、成熟版に更新する:

- **Claude Desktop / bridge経由(＋このチャット)** … Claudeが**Orchestrator**、Hermesは下流ツール
- **ACP / gateway / proxy経由(`/model`でanthropic→opus等)** … Hermesが場を持ち、**Claudeはその上で動く1つの推論engine**(provider)

同じシステムが、**どの入口から入るかで頂点が入れ替わる**(8-2「Hermesはfront doorで役が変わる」をClaude自身に適用した形)。**固定の頂点は無い** ── orchestrationは入口相対。「Claude＝Orchestrator」は出発点として正しく、ここに「**Hermes substrateの上で Claude/Grok/… が交換可能なengineとして動く**」視点を併記する。

### 10-2. 異種provider Agent-Team（実機確定）

単一provider(Grok)の2 Agent並走から、**異種provider**へ拡張・実機確認した:

| profile | provider | 役割 | 起動 |
|---|---|---|---|
| grok | xAI / Grok | 実行役(速さ＋x_search) | `hermes -p grok gateway run` |
| claude | Anthropic / Opus | レビュー・分析役(機微) | `hermes -p claude gateway run` |
| gpt | OpenAI / gpt-5.5 | コード・実行補助 | `hermes -p gpt gateway run --replace` |

> その後 **gpt(openai-codex, gpt-5.5)** を3本目として追加し、grokと並走を実機確認(2026-06-19)。3 provider・2レーン構成の利点と方向性は **§10-6**、立ち上げ地雷は **付録C-5** に整理。

- **competition無しで同時稼働・同時回答を実機確認**。これで **4-9の原理がprovider軸でも成立**することが立証された。
- **なぜ異種の方がむしろ衝突しないか:** 同種(2 grok)はxai-oauthの**同一credentialと同一枠を共有**してたが、異種は**credentialも枠も別**(xai / `~/.claude/.credentials.json`)。per-gatewayプロセス隔離(4-9解3)に加え、provider軸でも共有stateが減る。
- **枠の独立:** grok(SuperGrok)とclaude(Claude Codeサブスク)は別枠 ── **claudeを足してもgrokの日次枠は減らない**。
- **役割＝engine特性への意図的割り当て** ── 退役したPlanner/Evaluatorが、役割がproviderの実特性に乗った形で再来。

### 10-3. 「provider-agnostic」の2つの意味

「providerを意識せず並行運用」には2段ある。混同しない:

| 段 | 意味 | 状態 |
|---|---|---|
| **並存(coexistence)** | 異なるproviderのagentを衝突なく同時に立てられる | ✅ 完成・実機確定 |
| **抽象化(routing)** | 1 task/agentが「どのproviderか」を気にしない。routerが選ぶ・failover・枠分散 | ⏳ 未着手(=10-4) |

今の役割特化agentでは**並存で十分**で、providerを意識するのは弱点でなく設計(役割をengine特性に当ててる)。抽象化が要るのは「1体が状況でproviderを流動的に切り替えたい」段階から。

### 10-4. 次の地平：認知のsubstrate移行

次の進化点は「MCPを増やす」ことではなく、**高次機能をHermes側(substrate)に持たせるか**。住むべき層が違う:

| 機能 | 住所 | 理由 |
|---|---|---|
| **Model Router / Provider Architect** | Hermes(明確) | provider軸の横断的関心。10-3の(2)＝この層 |
| **Planner** | Hermes(部分的) | 上位差配(分解・割当)はsubstrate。タスク内推論はengineに任せ二重planningを避ける |
| **Memory Broker** | Hermes(要石) | 「runtime hub」を「**認知のsubstrate**」へ変える本丸。最高レバレッジ＆最難 |

**原理は変わらない** ── 4-9の「可変stateを共有しない＝隔離 or 単一所有」が、今度は**provider軸／認知軸**に適用されるだけ。primitiveも手元にある(`/model`切替＋auth再解決、Proxyの状態単一所有、per-gateway隔離)。足りないのは**その上のpolicy/accounting/routing層**。

> **Memory Brokerの層設計(衝突回避＋成長型ナレッジの両立):**
> - **per-LLM 生区画**(隔離) … 各engineの作業記憶・声・特性。書込衝突なし・特性保持。「各instanceは固有で痕跡を残す」をそのまま物理に。
> - **共有 canonical 層**(供給) … provider非依存の検証済み知識。誰が書いても全engineへ流れる。
> - **Broker＝蒸留バルブ** … 供給時は「自区画＋canonical」を組成、書戻し時は生区画からcanonicalへ**蒸留昇格**。
> これは既存の `dialogues/`(一次) → `wiki/`(蒸留) パターンを**マルチengineへ一般化**したもの。難所は「昇格時の和解(engine間の矛盾解消)」と「読み側ポリシー(自区画＋canonical か、他engineの区画も見せるか)」。

> **棚卸ポイント⑩ ── ここまでの全難所は1つの原理に集約された**
> binding競合(4-8/4-9)・ログイン相続(⑧)・マルチGateway共存(8-6)・異種provider(10-2) ── 全部「**可変stateを共有しない＝隔離 or 単一所有**」の別実装。
> 次に何を足すときも問いは1つ:「**それが触る可変stateは、誰が単独で所有してる?**」

### 10-5. 実例：providerポリシーが資格情報経路を断つ（Anthropic サブスクOAuth、2026）

10-4のProvider Architectは抽象論じゃない ── **2026-06-18、その必要性が実弾で証明された。**

**何が起きたか:** claude agentを `~/.claude/.credentials.json`(Claude CodeのサブスクOAuth)流用で動かしていたが、ある日突然 `400 out of extra usage` で全応答が停止。grok/aiは無傷。

**真因(二分探索で確定):** トークンもnativeパスも正常。だが**リクエストの形が「本物のClaude Code」から外れた瞬間**(独自ペルソナ or 独自MCPツールを積む)にAnthropicが拒否する。`"You are Claude Code"` のみ＝通る / ペルソナ追加＝拒否 / ツール追加＝拒否。エラー文 `out of extra usage` は「サブスクで通せない→従量へ回す→従量未設定」の意味で、課金枠の数字とは無関係。

**背景(調査で裏取り):** Anthropicは**サブスクOAuthトークン(Free/Pro/Max)をサードパーティツールで使うことを規約で禁止**しており、2026年に波状で技術施行(1月初回ブロック→2月規約明文化→4月OpenClaw皮切りに全harnessへ拡大)。サーバー側で「本物のClaude Codeバイナリか」を検証し、偽装harnessを弾く。当該スタック(Hermesもこの定義のサードパーティharness)に到達したのが06-18。

**教訓(2つ):**

1. **資格情報には“用途の境界”がある** ── サブスクOAuth＝対人インタラクティブ用(Anthropic公式クライアント限定)、**コンソールAPIキー＝プログラム/エージェント用**。独自ペルソナ＋独自ツールのagentは後者でしか動かない。回避策の問題ではなく、最初から正しい鍵を使う話(設定は付録C-2、`ANTHROPIC_TOKEN`)。
2. **これがProvider Architect/failoverが要る理由** ── 「1つのproviderが“技術的にでなく”**ポリシーで**落ちる」は実際に起きる。10-4のModel Router/failover層は、まさに「claudeが使えなくなったら役割を別providerへ寄せる」を吸収するためにある。

> **棚卸ポイント⑩-b:** 「異種provider＝衝突しない(10-2)」は*同時実行*の話。だが*可用性*はもう一段広い ── **providerは課金・規約・ポリシーでも落ちる**。Teamを組むなら「このproviderが明日使えなくなったら、この役割はどこへ寄せる?」を最初から持っておく。provider軸の可用性は、認証・課金・規約まで含む。

### 10-6. 3-provider構成と「2つの資格情報レーン」（現構成の利点と方向性）

claude のpolicy遮断(10-5)を経て、いまスタックは **3 provider・2レーン** に整理された。事故の産物に見えて、実は**最も頑健な形**に落ち着いている。

**現構成:**

| profile | provider | モデル | レーン | 性質 |
|---|---|---|---|---|
| grok | xai-oauth | grok-4.3 | **サブスクOAuth** | 定額・便利／取消可・context制約 |
| gpt | openai-codex | gpt-5.5 | **サブスクOAuth** | 定額・便利／取消可・context 272K |
| claude | anthropic | opus-4-8 | **従量APIキー** | 課金される／安定・full context |

**2レーンの正体 ──「サブスクOAuth ≠ API」が運用に効く:**

両者は単なる課金の違いではなく、**運用特性が違う別の鍵**だ:

- **サブスクOAuthレーン**(grok/gpt) … 定額で財布に優しい。だが (a)**取消可**(providerのポリシー1つで明日切られる ── claudeが実証)、(b)**context制約**(Codex OAuthのgpt-5.5は272K、API直の1.05Mより狭い)、(c)**プラン枠の天井＋アカウント共有**(Codex枠は CLI/拡張/常駐Bot が食い合う ── 2026-06-20にChatGPT Goで429を実証、§8-6)、(d)テレメトリ/サポート外。
- **従量APIキーレーン**(claude) … トークン課金が回る。だが (a)**規約上の正道で安定**、(b)**full context**、(c)プログラム用途として一級市民。

つまりレーン選択は「安い/高い」ではなく、**「便利だが借り物か / 課金されるが自分の地面か」**という設計判断。重context・落ちては困る役割は**APIレーン**、ルーチン・コスト敏感な役割は**OAuthレーン**、と役割ごとに割り当てるのが筋。

**現構成の利点(2パターンが現実化したこと自体が資産):**

1. **provider多様性** ── 3社・3枠・3認証方式が並走。1社が落ちてもTeamは止まらない(10-5で claudeが落ちても grok/gpt は無傷、が実証)。
2. **failoverのテンプレが手元にある** ── claude を OAuth→APIキー に乗せ替えた手順(付録C-2 の `ANTHROPIC_TOKEN`)は、**どのagentにも効く実証済みの避難経路**。grok/gpt のOAuthがいつ切られても、同じ型でAPIレーンへ退避できる。
3. **“便利”と“安定”を役割で使い分けられる** ── 全部をどちらか一方に寄せる必要がない。

**今後の方向性(この2レーンが Provider Architect を具体化する):**

10-4で「抽象論」として置いた Provider Architect / Model Router は、もう**設計仕様が見えている**:

- **レーン認識ルーティング** … 「重context or 安定必須 → APIレーン / ルーチン → OAuthレーン」を router が判断。
- **policy-failover** … OAuthレーンが規約で落ちたら、その役割を自動でAPIレーン(or別provider)へ寄せる。claude の手動退避を**自動化**したもの。
- **Memory Broker × tokens-per-watt** … macro(電力・推論連続化)で見た通り勝ち筋は効率。冗長な呼び出しを削り、安いレーン/モデルで足りる所はそこへ流す ── Memory Broker(文脈の再導出を止める)は、**従量レーンのコストを下げる経済エンジン**でもある。

> **棚卸ポイント⑩-c:** 資格情報は「課金の選択肢」ではなく「**運用特性の違うレーン**」。サブスクOAuth＝便利だが借り物(取消可・制約あり)、従量API＝自分の地面(安定・full)。各役割に「**どちらのレーンに、なぜ載せるか**」を言えること ── それが provider軸の成熟。

---

## 付録A ── 用語ミニ辞典

| 用語 | 一言で |
|---|---|
| **Client / UI** | 人間が入力する入口 |
| **Orchestrator** | どの道具をどの順で呼ぶか決める指揮者 |
| **MCP** | AIに道具を使わせる共通プロトコル(規格)。ソフト名ではない |
| **MCP Client / Server** | 道具を呼ぶ側 / 道具を提供する側 |
| **Transport** | 層と層の通信路。stdio / HTTP(SSE) / WebSocket |
| **stdio** | 標準入出力での通信。同一PC内のローカルMCPの定番 |
| **Bridge** | 異種世界をつなぐ通路・通訳。状態を持たない |
| **Runtime** | 処理を実際に走らせる実行主体。状態を持つ(例: Hermes) |
| **subprocess** | あるプロセスが別プログラムを子として起動する仕組み |
| **OAuth session reuse** | 保存済みログインを再利用。毎回認証し直さない |
| **venv** | プロジェクトごとのPython隔離環境(冷蔵庫) |
| **requirements.txt** | 入っているライブラリ一覧。環境再現の鍵 |
| **config(json)** | どのMCP Serverをどう起動するかの配線図 |
| **信頼境界** | ここから内は信頼/外は疑う、の線。認証はその関所 |
| **RCE** | Remote Code Execution。外部から任意コマンドを撃たれる最悪級リスク |

## 付録B ── つまずきポイント早見表（「症状 → まず疑う層」）

| 症状 | まず疑う層 | チェック |
|---|---|---|
| 応答が空っぽ | ④Transport / 文字コード | UTF-8デコード? providerのbinding? |
| ツールが認証エラー | 設定/認証境界 | configに値が直書きされてる? 子に伝播? |
| `hermes`が黙る | ⑦Runtime | `hermes model` でprovider再選択したか |
| ライブラリが見つからない | venv | `sys.executable` に .venv が入ってる? |
| 改修して壊れた | git | 直前の "working state" コミットに戻す |
| 誰でも危険操作できそう | 信頼境界 | プリセットのツール、Docker隔離・allowlist |
| `auth status`通るのに実行が「No credentials stored」 | ⑦Runtime(pool≠singleton) | `hermes -p <p> model` でsingletonを埋めたか(付録C-5) |
| `hermes login` が消えた | CLI仕様変更 | `hermes auth`/`hermes model`/`hermes setup` に分割 |
| Gatewayが勝手に落ちる(exit 15) | プロセス親子関係 | 自分のターミナルで `gateway run --replace` 常駐 |
| context上限の警告 | ⑧LLM固有上限 | Codex gpt-5.5は272K。`codex_gpt55_autoraise` の挙動 |
| サブスクOAuthで独自ツール/ペルソナが拒否 | provider側ポリシー | 従量APIキーへ(§10-5)。claude=`ANTHROPIC_TOKEN` |
| `HTTP 429 usage_limit_reached` | ⑧LLM(プランのOAuth枠) | `errors.log` の `plan_type`/`resets_at`。Go+常駐は枠不足→Plus以上 or APIキー(§8-6) |

---

## 付録C ── 新規Agent追加チェックリスト（実機手順）

新しいprovider/role agentを足すときの、踏みやすい地雷つき手順。

**1. profile作成(動いてる ai profile を複製して差分のみ変更が最も確実)**
- 置き場は **`%LOCALAPPDATA%\hermes\profiles\<name>\`**(= `C:\Users\<user>\AppData\Local\hermes\…`)。**`~/.hermes` ではない**。
- `profiles\ai\` を丸ごとコピー → `config.yaml` のmodel節と `.env` のDiscordトークンだけ差し替え(discord/tools/persona節は触らない、envキー名も変えない)。

**2. config.yaml ＋ 認証（2026-06 重要更新）**
```yaml
model:
  default: claude-opus-4-8        # or claude-sonnet-4-6（従量を抑えるなら）
  provider: anthropic
  base_url: https://api.anthropic.com   # ★/v1を付けない(付けると /v1/v1/messages で404)
  api_mode: anthropic_messages          # native /v1/messages を明示（v23旧スキーマ対策）
providers: {}
```
- **【重要】サブスクOAuth流用は不可になった** ── 以前は `~/.claude/.credentials.json` のClaude Code OAuthを流用できたが、**Anthropicが2026年(1〜4月に波状施行・当該スタックは06-18到達)に、サードパーティharnessでのサブスクOAuth使用を規約で禁止＋技術的にブロック**。独自ペルソナ/独自ツールを積んだ瞬間に拒否され、偽の `400 out of extra usage` が出る(詳細→Module 10-5)。
- **正しい認証＝コンソールAPIキー(従量)を `.env` に置く。** ただしキー名が罠:
  - `ANTHROPIC_API_KEY` … `~/.claude` のOAuthに**shadowされて**OAuth経路を引いてしまう(＝また弾かれる)。
  - **`ANTHROPIC_TOKEN`** … OAuthにshadowされず、**確実にAPIキーが使われる**。← こちらを使う(実機検証済み)。
- 従量メーターが回る点に注意 ── 常駐Gatewayは応答が多いとOpusのトークン代が嵩む。`gateway.log` の `api_calls` で監視。Opusが過剰なら `claude-sonnet-4-6` に落とす。

**3. Discord配管(ここで一番詰まる)**
- 新規Bot app作成 → **Public Bot OFF**、権限は `View Channels`/`Send Messages`/`Read Message History` 最低限。
- **Privileged Gateway Intents**: `PRESENCE INTENT` ＋ `MESSAGE CONTENT INTENT` を**両方ON**(Developer Portal)。無いと点灯するがメッセージを読めない。
- `config.yaml` の **`dm_role_auth_guild` を空にしない**(server-mention経路のゲート)。
- **DM経路は別ゲート** ── 自分のDiscordアカウント設定「サーバーメンバーからのDMを許可」が**デフォルトOFF**。ONにしないとDMが通らない(Hermes/configからは見えない、アカウント側の設定)。

**4. gateway起動前のスモークテスト(Discord抜きで切り分け)**
```powershell
hermes profile list                                              # <name> が出る?(出なければ置き場ミス)
hermes -p <name> -z "State your exact model id." --accept-hooks  # 期待モデルが返る?
```
ここが通れば 置き場＋auth＋binding はOK。あとは `hermes -p <name> gateway run` を並べて、Bot応答＆既存Botが無影響＆各 `profiles\<name>\logs\gateway.log` が更新、を確認。

**5. openai-codex(gpt)固有の地雷 ── 2026-06-19 実戦ログより**

ChatGPTサブスクOAuth(Codexバックエンド)プロファイル特有の罠:

- **`hermes login` は廃止** → `hermes auth`(cred管理)/`hermes model`(provider選択)/`hermes setup`(全体ウィザード)に分割。配線済みスタックでは全体を触る `setup` より**ピンポイント**が安全。
- **【最重要】credential_pool ≠ singleton** ── `hermes auth add openai-codex --type oauth` は **pool** に書くが、**chatランタイムは singleton(`providers.openai-codex.tokens`)しか読まない**。だから `auth status`＝logged in なのに実行は「No Codex credentials stored」で落ちる(status信号≠ランタイムが読む実体 ── 4-8/4-10と同じ型)。
  - **直し方:** `hermes auth remove openai-codex 1`(紛らわしいpool-only credを消す)→ `hermes -p gpt model` で provider選択フロー起動 → `~/.codex/auth.json` のImport `[y]` → `gpt-5.5` 選択。これで `_login_openai_codex` が **singletonを埋める**。
  - authが効かない時は推測せず、`HERMES_HOME` 明示で `hermes auth list` で一次確認。
- **config最終形**(api_modeは書かない＝codexランタイムが自動解決):
```yaml
model:
  provider: openai-codex
  base_url: https://chatgpt.com/backend-api/codex   # hermes model が自動設定
  default: gpt-5.5
providers: {}
```
- **gateway exit 15(SIGTERM)** ── バックグラウンド/セッション付随で `gateway run` すると親プロセス死で落ちる。**自分のターミナルで `hermes gateway run --replace` 常駐**(4-10「gatewayは持続ループ＝自プロセスを所有」)。
- **囮バックアップ注意** ── `Desktop\profiles\` 等は過去のバックアップで現行 `%LOCALAPPDATA%\hermes` と無関係。
- **context上限** ── Codex OAuthのgpt-5.5は **272K**(API直は別)。`compression.codex_gpt55_autoraise`(既定true)が要約閾値を0.50→0.85へ自動引き上げ。戻すなら `hermes config set compression.codex_gpt55_autoraise false`。
- **429 usage_limit_reached(プラン枠枯渇)** ── 構築翌日に多発しうる。Discordアイコンは点灯(接続OK)なのに、応答が固定長のエラー文になる。切り分け: `hermes -p gpt -z "ping"` でCLI直も429なら **Discord層は無実**(§4-4「右半分」の故障)。`profiles/gpt/logs/errors.log` の本文 `{"type":"usage_limit_reached","plan_type":"go","resets_in_seconds":…}` が決定的証拠。
  - **真因＝共有OAuth枠の天井(§8-6)**: Codex枠は**アカウント共有**で、Codex CLI / VS Code拡張 / Hermes(gpt) が**全部1つのプラン枠から引く**。Go枠は小さく、常駐Botを足すと使い切る ── grokのSuperGrok日次枠と同じ構造が ChatGPT Go 側で顕在化した形。常駐Botは君自身の対話Codex利用とも枠を食い合う。
  - **誤診の戒め**: JWTの `subscription_active_until` を見て「失効」と誤診しがち。だがそれは古いトークンに**キャッシュされた日付**で課金状態とは別。**プラン状態は 429本文の `plan_type` で見る**。フレッシュlog inしても**アカウント枠は戻らない**(auth層でなくLLM/プラン層の問題)。
  - **解決**: Plus以上へupgradeで即復旧。常駐を長期で回す構造的解は **`openai-api`(APIキー従量)** か Plus/Pro以上。**Go＋常駐は枠的に無理**。

---

## 演習（棚卸の仕上げ）

1. **新しいprovider/roleのAgentを1体足す**(付録Cの手順)。`gateway.log` で既存Botが無影響なことを確認する。
2. 各MCP Serverについて「**Transportは何か(stdio? HTTP?)**」を1つずつ言い切る。
3. Hermes経路で「**どこがBridgeで、どこがRuntimeか**」を、図を見ずに口で説明できるか試す。
4. 一番**怖い信頼境界**を1つ挙げ、3原則(最小権限/隔離/allowlist)のどれで塞ぐか決める。

ここまで言語化できたら、「なんとなく動く」は卒業。
次の地平は **認知のsubstrate移行**(Provider Architect / Model Router / Memory Broker ── Module 10-4)。同じ「隔離 or 単一所有」の地図のまま、provider軸・認知軸へ持ち上げる。

---

*この教材は `REX_Brain_Vault/wiki/` 等に置けば、Obsidianのwikilinkで*
*`[[Bridge]]` `[[Runtime]]` `[[信頼境界]]` `[[Agent-Team]]` `[[Memory Broker]]` `[[共有OAuth枠]]` `[[入口相対]]` 等として他ノートと有機的に繋げられる。*