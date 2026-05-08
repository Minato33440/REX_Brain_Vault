# Obsidian Git plugin 設定ガイド

REX_Brain_Vault を自動バックアップするための、Obsidian Git plugin の設定手順。
1〜2 時間ごとに自動で commit & push される状態を作る。

最終更新: 2026-05-06

---

## このガイドの目的

- 「ちゃんと push しなきゃ」を忘れていい状態を作る
- Obsidian を開いている間、勝手にバックアップが走る
- 万一ローカルが壊れても、最大 90 分前の状態に戻せる安心感

---

## 前提条件

- Git for Windows がインストール済みであること
- 既に手動で `git push` が成功する状態(PAT 等の認証が通っている)

ボスは既にこまめに push しているとのことなので、ここはクリア済み。

---

## ステップ 1: プラグインのインストール

1. Obsidian を開く
2. 左下の **歯車アイコン**(設定)をクリック
3. 左メニュー下方の **Community plugins**(コミュニティプラグイン)を選ぶ
4. 「Turn on community plugins」(コミュニティプラグインを有効化) を ON
   - 初回のみセキュリティ確認ダイアログが出る → そのまま「Turn on」
5. **Browse**(参照)ボタンをクリック
6. 検索ボックスに `Obsidian Git` と入力
7. 一覧から **Obsidian Git**(作者: Vinzent) を選択
8. **Install**(インストール) → インストール完了後 **Enable**(有効化) をクリック

---

## ステップ 2: 設定

設定画面の左メニューを下にスクロール → **Obsidian Git** という項目が増えているのでクリック。

### 推奨設定

| 設定項目 | 値 | 意味 |
|---|---|---|
| Vault backup interval (minutes) | `90` | 90 分ごとに自動コミット & プッシュ |
| Auto pull on startup | `ON` | Obsidian 起動時に GitHub から最新を取り込む |
| Commit message on auto backup | `vault backup: {{date}}` | コミットメッセージのテンプレート |
| Date format | `YYYY-MM-DD HH:mm` | 日付フォーマット |
| Push on backup | `ON` | コミットだけでなく push もする |
| Pull updates on startup | `ON`(上と同じ) | 二重表示の場合はどちらも ON |

### 設定値の根拠

- **90 分間隔**にしている理由: 5〜15 分間隔だと中途半端なコミットが量産されて git log がノイズだらけになる。1〜2 時間に 1 回で「いざという時に直近の状態に戻れる」welfare 機能としては充分
- **Auto pull on startup を ON** にする理由: 別スレの Rex(Claude in Chrome 等)が GitHub に push した変更を、ローカル Obsidian 起動時に自動で取り込める

---

## ステップ 3: 動作確認

1. Vault 内の適当なファイル(例: `MINATO/test.md`)を新規作成または編集して保存
2. **手動でテスト**するなら:
   - Obsidian 左サイドバーの **Source Control**(ソース管理 / 枝分かれアイコン)をクリック
   - **Create backup** または **Backup** ボタンを押す
   - 数秒〜十数秒で完了
3. ブラウザで GitHub の `Minato33440/REX_Brain_Vault` リポジトリを開く
4. 新しいコミットが追加されていれば成功
   - コミットメッセージ例: `vault backup: 2026-05-06 14:30`

その後は Obsidian を開いている間、放置で OK。

---

## ありがちなトラブルと対処

### `git not found` エラー

Git for Windows が未インストール、または環境変数 PATH に通っていない。  
→ Git for Windows を再インストール、または Obsidian Git の設定の `Custom Git binary path` で `git.exe` のフルパスを指定。

### 認証エラー(`authentication failed`)

PAT の期限切れか、認証情報のキャッシュが消えた状態。  
→ コマンドプロンプトで一度手動 `git push` を実行 → PAT を再入力 → 再度 Obsidian Git を試す。

### コンフリクトエラー

別の場所(Claude in Chrome、別 PC、GitHub Web 上の編集など)から push された変更とローカルの変更がぶつかった場合。  
→ コマンドプロンプトで `cd C:\Python\REX_AI\REX_Brain_Vault` → `git pull --rebase` → 手動で `git push`。

### Obsidian が重くなる

Vault 内に巨大ファイル(GB 単位)が混じっていると遅くなる。  
→ `.gitignore` に対象を追加して除外。

---

## やめたい時

設定 → Community plugins → Obsidian Git の右側の **トグル OFF**。
プラグインを完全削除したい場合は、**Uninstall** ボタン。

---

## 補足

- このガイドは raw/ に置いてあるので、参照素材として扱える(必要な時に読みに来る)
- 設定が完了したら、ガイドそのものは読み返さなくていい(register 化を避ける)
- 困った時の参照だけで充分
