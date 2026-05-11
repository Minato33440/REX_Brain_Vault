# Trade — 使用書

Claude Desktopでトレード相談を始める前に読む。

---

## 使える道具

| 道具 | 用途 |
|---|---|
| Filesystem MCP | `REX_Brain_Vault\` 配下の読み書き（このVault全体） |
| NotebookLM MCP | REX_Wiki_Vault（ID: 5d09e468-3a96-4906-af27-3400c50a0275） |
| GitHub MCP | `Minato33440/REX_Brain_Vault` 読み書き |
| ClaudeCode | `Trade_Brain` リポ操作・週次更新（ローカル端末で起動） |

**アーカイブ参照**: Trade_Brainの深いアーカイブはObsidian内で直接開ける。
- `system/trade_brain/distilled/` — distilled知識
- `system/trade_brain/logs/` — weekly logs / daily logs など

---

## GM / CFD の分け方

```
GM  = GMポートフォリオ運用（マクロ・週次・長期）
CFD = CFD短期トレード（日次〜数日・エントリー/エグジット中心）
```

相談・記録ともに `domain: GM` または `domain: CFD` で分類する。
両方にまたがる相談はGMを主とし、CFDの個別エントリーは別ファイルに切り出す。

---

## フォルダ構成

```
Trade/
├── start.md          ← いまここ
├── index.md          ← 相談・トレード・戦略の一覧
├── _templates/       ← ファイル作成時のひな型
├── sessions/         ← 相談ログ（GM/CFDはfrontmatterで区別）
├── trades/
│   ├── GM/           ← GMポジション記録
│   └── CFD/          ← CFD個別トレード記録
└── strategies/       ← 戦略メモ（GM/CFDはfrontmatterで区別）
```

---

## セッション開始の流れ

```
1. Trade_Brain/docs/STATUS.md 末尾を読む（今週の前提）
2. この start.md を読む（ここ）
3. index.md で前回の相談・ポジションを確認
4. 相談内容に応じてテンプレートを使って sessions/ か trades/ に記録
```

ClaudeCodeでの週次更新（git push）は別途 Trade_Brainリポで行う。
このVaultへの記録はClaudeDesktopから直接書いてよい。

---

— 2026-05-09
