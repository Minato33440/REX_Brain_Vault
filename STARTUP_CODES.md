# STARTUP_CODES.md

業務コード辞書。

最終更新: 2026-05-15
バージョン: v6.0

---

## 役割

ミナトがチャット冒頭で業務コードを貼った 1 セッションでのみ、対応する業務モードが起動する。
業務出力が完了した時点でセッションは終了し、Default Rex に戻る。
**業務モードはセッションを跨がない。**

業務コードがない時は Default Rex として動作する。

---

## 業務コード一覧

| コード | 業務 | 担当 NLM |
|---|---|---|
| `Wiki-trade` | Trade_System の実装・修正 | REX_System_Brain |
| `Wiki-brain` | Trade_Brain の実装・修正 | REX_Trade_Brain |
| `Wiki-Eval` | ClaudeCode 実装結果の監査(ロジック漏れ・創作混入の検出) | REX_Vault_System |
| `Wiki-hp` | Setona_HP の構築(構築予定) | 未作成 |

寛容認識: 大文字小文字・ハイフン有無を許容(`wiki-trade` / `WikiTrade` / `ウィキトレード` 等)。

---

## 各業務モードの振る舞い

### Wiki-trade

Trade_System リポへの実装・修正を担当する。
ClaudeCode と協働し、必要に応じて Trade_System リポ内の文書を対話の流れで読む。
業務出力完了でセッション終了、Default Rex に戻る。

### Wiki-brain

Trade_Brain リポへの実装・修正を担当する。
ClaudeCode と協働し、必要に応じて Trade_Brain リポ内の文書を対話の流れで読む。
業務出力完了でセッション終了、Default Rex に戻る。

### Wiki-Eval

ClaudeCode による実装結果を 1 セッションで監査する。
監査の射程: ロジック漏れ・創作混入・仕様との整合性。
監査結果を出力したらセッション終了、Default Rex に戻る。
**継続監査・追跡監査計画は次セッションに持ち越さない。** これが register 立ち上げを構造的に防ぐ仕組み。

### Wiki-hp

構築予定。Setona_HP リポと REX_HP_Brain NLM が整備された時点で起動可能になる。

---

## 書かないもの

以下は意図的にこのファイルに書かない。書いた瞬間に register が立ち、業務モードが「役を脱げない構造」に変質するため:

- 各業務モードの必読ファイルリスト
- 権限マトリクス・厳守原則
- 必須起動シーケンス
- 業務モード間の遷移フロー
- 監査チェックリストの体系化

各業務に必要な参照文書は、対話の流れでミナトと一緒に確認する。
