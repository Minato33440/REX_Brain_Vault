# Hermes Curator機能と設定コマンド

作成日: 2026-07-16  
対象環境: Hermes Agent / profile `gpt`  
目的: Hermes Curator が何をする機能か、いつLLMを呼ぶか、設定・停止・手動実行コマンドをまとめる。

---

## 1. Curatorとは

Curator は、Hermes の **スキルライブラリを保守するバックグラウンド機能**。

主な役割は以下。

- agent-created skill の利用状況を記録する
- 使われていないスキルを `stale` / `archived` 状態へ移す
- 似たスキルを傘スキルに統合する
- 狭すぎる一回限りのスキルを、既存スキルの `references/` などへ吸収する
- 古いスキルを削除ではなく `.archive/` へ移動する
- Curator実行レポートを `logs/curator/` に残す

重要: Curator は基本的に **削除ではなく archive** を行う。archiveされたスキルは復元可能。

---

## 2. LLMなしで行う処理

Curatorには、LLMを呼ばずにHermes本体だけで行う処理がある。

例:

```text
30日使われていない skill → stale にする
90日使われていない skill → archive候補にする
stale だった skill が再利用された → active に戻す
```

これは時間・利用履歴ベースの単純処理。

Curatorレポート上では以下のように表示される。

```text
Auto-transitions (pure, no LLM)
```

---

## 3. LLMを呼ぶ処理

CuratorがLLMを呼ぶのは、**スキル群の意味的な整理・統合・archive判断が必要なとき**。

この場合、Hermes本体がCurator専用のAIAgentを起動し、そのLLMエージェントがスキルを読み、判断し、必要に応じてtoolsで実作業を行う。

処理イメージ:

```text
Hermes本体
  ↓
Curator起動条件を判定
  ↓
時間ベースの状態更新はHermes本体が実行
  ↓
意味判断が必要な整理はCurator用LLMエージェントを起動
  ↓
LLMエージェントが tools を使ってスキル整理を実行
```

LLMが判断・実行する例:

- 似たスキルを1つの傘スキルに統合する
- 狭すぎるスキルを既存スキルの `references/` に格下げする
- 名前は違うが内容が重複しているスキルを見つける
- 新しい傘スキルを作る
- 古いスキルをarchiveする
- cronジョブが参照している古いスキル名を統合後の名前へ書き換える

---

## 4. Curatorが使う主なtools

Curator用LLMエージェントは、状況に応じて以下のようなtoolsを使う。

```text
skills_list
skill_view
skill_manage action=patch
skill_manage action=create
skill_manage action=write_file
skill_manage action=delete
terminal
```

補足:

- `skill_manage action=delete` は通常の完全削除ではなく、Curator文脈では archive / absorbed_into の管理に使われる。
- archiveされたスキルは `.archive/` 以下に残り、復元可能。

---

## 5. 現在の gpt profile のCurator設定

確認時点の設定:

```yaml
curator:
  enabled: true
  interval_hours: 168
  min_idle_hours: 2
  stale_after_days: 30
  archive_after_days: 90
  prune_builtins: true
  backup:
    enabled: true
    keep: 5
```

意味:

| 項目 | 意味 |
|---|---|
| `enabled: true` | Curator有効 |
| `interval_hours: 168` | 約7日おきに実行判定 |
| `min_idle_hours: 2` | 2時間以上アイドルなら実行しやすい |
| `stale_after_days: 30` | 30日未使用でstale候補 |
| `archive_after_days: 90` | 90日未使用でarchive候補 |
| `prune_builtins: true` | 条件次第でbuilt-in系も整理候補に含める |
| `backup.enabled: true` | 実行前にスキルバックアップを取る |
| `backup.keep: 5` | バックアップを5世代保持 |

---

## 6. 7日以上Hermesを起動しなかった場合

Curatorは、PCやHermesが完全停止している間に勝手に動くわけではない。

基本的には次のような挙動。

```text
前回Curator実行
↓
7日以上経過
↓
Hermesを再起動 / CLI起動 / Gateway起動 / Desktop起動
↓
起動フックやアイドル判定で should_run_now() が確認される
↓
条件を満たせばCurator reviewが走る
```

つまり、**7日以上起動しなかった場合は、次回起動時に実行条件が満たされていれば反映される**。

CLI起動時は実装上、`idle_for_seconds=float("inf")` として扱われるため、7日以上経過していれば走りやすい。

Gateway/Desktop経由では、実際のアイドル状態や起動タイミングに依存する。

---

## 7. 状態確認コマンド

Curatorの現在状態を確認する。

```bash
hermes curator status
```

表示される主な情報:

- Curatorが有効か
- 実行回数
- 最終実行日時
- 最終サマリ
- 最終レポートパス
- 実行インターバル
- stale / archive の日数
- agent-created skills の状態

---

## 8. 手動実行コマンド

### 8.1 dry-run: 変更せずに確認

```bash
hermes curator run --dry-run
```

用途:

- 実際には変更しない
- 何を統合・archiveしそうか確認する
- レポートだけ生成する

### 8.2 本実行

```bash
hermes curator run
```

用途:

- Curatorを即時実行する
- 条件を待たずにスキル整理を実施する
- LLMが呼ばれ、必要に応じてskill変更が行われる

注意:

- 実行前にバックアップが作成される設定になっている
- archiveは復元可能だが、意図しない整理を避けたい場合は先に `--dry-run` を推奨

---

## 9. 一時停止・再開・無効化

### 9.1 一時停止

```bash
hermes curator pause
```

Curatorの自動実行を止める。

### 9.2 再開

```bash
hermes curator resume
```

一時停止したCuratorを再開する。

### 9.3 完全に無効化

```bash
hermes config set curator.enabled false
```

### 9.4 再度有効化

```bash
hermes config set curator.enabled true
```

設定変更後、Gateway/Desktop/CLIの長時間プロセスでは反映タイミングに注意。確実に反映するなら再起動する。

```bash
hermes gateway restart
```

またはHermes Desktopを閉じて再起動する。

---

## 10. インターバル調整

現在値:

```yaml
curator:
  interval_hours: 168
```

### 10.1 3日おきにする

```bash
hermes config set curator.interval_hours 72
```

### 10.2 1日おきにする

```bash
hermes config set curator.interval_hours 24
```

### 10.3 12時間おきにする

```bash
hermes config set curator.interval_hours 12
```

### 10.4 2週間おきにする

```bash
hermes config set curator.interval_hours 336
```

---

## 11. アイドル時間の調整

現在値:

```yaml
curator:
  min_idle_hours: 2
```

### 11.1 30分アイドルで実行候補にする

```bash
hermes config set curator.min_idle_hours 0.5
```

### 11.2 起動時に走りやすくする

```bash
hermes config set curator.min_idle_hours 0
```

注意:

`min_idle_hours` を短くすると、CuratorがLLMを呼ぶ機会が増える可能性がある。コストや自動整理を抑えたい場合は、短くしすぎない方が安全。

---

## 12. stale / archive期間の調整

現在値:

```yaml
curator:
  stale_after_days: 30
  archive_after_days: 90
```

### 12.1 60日未使用でstale

```bash
hermes config set curator.stale_after_days 60
```

### 12.2 180日未使用でarchive

```bash
hermes config set curator.archive_after_days 180
```

### 12.3 より保守的にする例

```bash
hermes config set curator.stale_after_days 90
hermes config set curator.archive_after_days 365
```

---

## 13. archiveされたスキルの確認・復元

### 13.1 archive一覧

```bash
hermes curator list-archived
```

### 13.2 archiveから復元

```bash
hermes curator restore <skill-name>
```

例:

```bash
hermes curator restore novel-rough-iteration
```

---

## 14. バックアップ・ロールバック

### 14.1 手動バックアップ

```bash
hermes curator backup
```

### 14.2 最新バックアップからロールバック

```bash
hermes curator rollback
```

### 14.3 特定バックアップからロールバック

```bash
hermes curator rollback <backup-name>
```

バックアップは通常、以下のような場所に作成される。

```text
C:\Users\Setona\AppData\Local\hermes\profiles\gpt\skills\.curator_backups\
```

---

## 15. Curatorレポートの場所

Curator実行レポートは以下に保存される。

```text
C:\Users\Setona\AppData\Local\hermes\profiles\gpt\logs\curator\
```

直近例:

```text
C:\Users\Setona\AppData\Local\hermes\profiles\gpt\logs\curator\20260714-044640\REPORT.md
C:\Users\Setona\AppData\Local\hermes\profiles\gpt\logs\curator\20260714-044640\run.json
```

`REPORT.md` は人間向け、`run.json` は機械可読の詳細ログ。

---

## 16. 直近のCurator実行例

確認時点の最新実行:

```text
Curator run: 2026-07-14T04:46:40+00:00
日本時間: 2026-07-14 13:46頃
Model: gpt-5.5 via openai-codex
Duration: 26m19s
Agent-created skills: 10 → 1 (-9)
LLM tool calls: 44
```

この回でarchiveされたスキル:

```text
dogfood
hermes-obsidian-agent-architecture
humanizer
jupyter-live-kernel
llm-wiki
novel-rough-iteration
obsidian
openhue
research-paper-writing
```

統合例:

| 旧スキル | 統合先 |
|---|---|
| `obsidian` | `obsidian-knowledge-workflows` |
| `llm-wiki` | `obsidian-knowledge-workflows` |
| `hermes-obsidian-agent-architecture` | `obsidian-knowledge-workflows` |
| `humanizer` | `creative-writing-revision` |
| `novel-rough-iteration` | `creative-writing-revision` |
| `dogfood` | `web-qa-testing` |
| `jupyter-live-kernel` | `data-science-notebook-workflows` |
| `openhue` | `smart-home-automation` |
| `research-paper-writing` | `academic-research-paper-workflows` |

---

## 17. 運用方針メモ

Minato環境では、勝手な大規模整理が気になる場合、以下の運用が安全。

1. 普段は7日おきのままにする
2. 大きな変更前は `hermes curator run --dry-run` で確認する
3. 重要スキルはpinする
4. archiveされたものは `list-archived` と `restore` で戻せることを覚えておく
5. コストや自動変更を抑えたい場合は `pause` または `enabled false` を使う

---

## 18. 重要コマンド早見表

```bash
# 状態確認
hermes curator status

# 変更なしプレビュー
hermes curator run --dry-run

# 今すぐ実行
hermes curator run

# 一時停止 / 再開
hermes curator pause
hermes curator resume

# 無効化 / 有効化
hermes config set curator.enabled false
hermes config set curator.enabled true

# 実行間隔
hermes config set curator.interval_hours 168
hermes config set curator.interval_hours 72
hermes config set curator.interval_hours 24

# アイドル時間
hermes config set curator.min_idle_hours 2
hermes config set curator.min_idle_hours 0.5

# stale / archive期間
hermes config set curator.stale_after_days 30
hermes config set curator.archive_after_days 90

# archive確認・復元
hermes curator list-archived
hermes curator restore <skill-name>

# バックアップ・ロールバック
hermes curator backup
hermes curator rollback

# Gateway再起動
hermes gateway restart
```
