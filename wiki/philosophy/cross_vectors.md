# 4 横断ベクトル — 事実記録

**位置付け**: 2026-04-22 セッションでボスが示した「横断」の構造整理の**事実記録**。
**本ファイルの性質**: 参考資料。後任 Evaluator がこれを使う義務はない。
**記録者**: 7 代目統括 Evaluator（2026-04-22）

---

## ボス原文（2026-04-22）

> ①Gitリポでは：Trade_System を←Trade_Brain が情報面で補完
> ②しかし今回各リポのプロジェクト引き継に関しては：Trade_System⇔Trade_Brain 相互情報共有がベスト
> ③そしてNLMリポでは：Trade_System と Trade_Brain 両 Git リポを←NLM:REX_Wiki_Vault がシステム環境面で共有している
>（追加） REX_Brain_Vault を←REX_Wiki_Vault が補完 これもベクトル
>
> つまり其々のシステム横断はその役割と組み合わによってベクトルが変わるということだね。

---

## 4 ベクトルの整理

### ベクトル ①【Git リポ層・データフロー】

```
Trade_System  ←  Trade_Brain  ←  Rex_Brain_Vault(将来の市場環境図書館)
  動的ロジック       静的データ         精密化された市場知識
```

将来的に Vault が市場環境データを Trade_Brain 経由または直接 Trade_System に供給する想定。実装コードに影響する層。

### ベクトル ②【セッション引き継ぎ層】

```
Trade_System  ⇔  Trade_Brain
```

統括 Evaluator が両プロジェクトの進捗を横断で把握する層。双方向の情報共有。

### ベクトル ③【NLM 上位メタ層】

```
         REX_Wiki_Vault (NLM・未作成)
             /        \
            ↓          ↓
Trade_System              Trade_Brain
```

自己増殖型ナレッジシステム環境を両実装リポに提供する上位メタ層。REX_Wiki_Vault は未作成。

### ベクトル ④【NLM が Git を補完】

```
Rex_Brain_Vault (Git) ← REX_Wiki_Vault (NLM)
```

Git リポに残る静的ナレッジを NLM の RAG が補完的にクエリ可能にする。現在 NLM 凍結中のため機能していない。

---

## 参考：Vault と NLM の性質（2026-04-23 ボス発言）

> ①ローカルの Obsidian-Vault は Rex の頭脳なので REX_AI 配下の全てのリポ情報を共有統合。
> ②NLM はラグなのでバグ防止のため敢えて個別化

| 層 | 性質 |
|---|---|
| Obsidian Vault（Rex_Brain_Vault）| 全統合（関連付けが命）|
| NotebookLM（3 Notebook）| 個別化（混同防止が命）|

詳細は `architecture.md` 参照。

---

## 本ファイルの運用注意

- 本ファイルは **事実記録**（ボスが 2026-04-22 に示した構造整理を 7 代目が書き留めたもの）
- 「統合/分離/共用」判断で参考にしたい Evaluator が使えばよい
- 後任への強制はしない。必須でもない
- 「必ず自問せよ」「行動規範として内面化せよ」などの強制的書き換えが過去にあったが、2026-04-23 に 8 代目が除去した

---

## 関連文書

- `philosophy/architecture.md` — 4 リポ体制の事実記録
- `philosophy/evaluator_code.md` — 各代 Evaluator の気づきメモ
- `handoff/architecture_handoff.md` — 7 代目セッション記録

---

*記録: 7 代目 (2026-04-22)*
*縮退: 2026-04-23 / 8 代目が強制口調を除去・事実記録として再整理*
