# スレ引き継ぎ指示書 vol.9
## セトナ治療院 HP構築プロジェクト
**作成：REX / 2026-04-13**

---

## 1. プロジェクト概要（継続確認）

| 項目 | 内容 |
|------|------|
| 新サイト | https://setona.co.jp（本番稼働中） |
| 旧サイト | https://setona.net/71186/（at-ml.jp・5月末解約予定） |
| サーバー | さくらインターネット / bqn03.sakura.ne.jp |
| CMS | WordPress + Cocoon（子テーマ：cocoon-child-master） |
| GitHub | https://github.com/Minato33440/Setona_HP |

---

## 2. 前スレ（vol.8）からの継続確認事項

### ✅ 完了済み（vol.8まで）
- 全7固定ページ実装・公開
- SSL / HTTPS化
- GA4設定（G-WF0TWQVX8W）
- MailPoet × Brevo メール配信（DKIM/DMARC認証完了）
- 投稿通知メールテンプレート作成・動作確認
- TOPページ「最新のお知らせ」ショートコード実装

---

## 3. 本スレ（vol.9）完了作業

### ㉝ スマホ会員登録バナー帯 + ポップアップモーダル実装

**実装方式（確定）：**
- バナーHTML → `wp_body_open` フックの `setona_custom_header()` 内に配置
  （`wp_footer` に置くとDOM最下部になりstickyが効かないため）
- モーダルHTML + CSS → `wp_footer` 無名関数で出力

**表示条件：**
- TOPページ（`is_front_page()`）+ 投稿ページ（`is_single()`）のみ
- PC（800px以上）は完全非表示

**重要な学習事項：**
> ⚠️ `wp_footer` 出力要素に `position:sticky` は効かない
> → ヘッダー直下に表示したい要素は必ず `wp_body_open` フックに配置する

---

### ㉞ 確認メール（サインアップ承認）日本語化

**設定箇所：**
```
MailPoet → 設定 → サインアップ承認タブ
→「視覚的な購読の確認メールを有効にする」
→「テンプレートエディターを開く」で本文を日本語に編集
```

**確定内容：**
- 件名：「セトナ通信」への購読を確認します
- 本文：日本語に全面書き換え済み
- フッター英語テキストはテンプレートエディターで削除

---

### ㉟ 投稿記事スラッグ・パーマリンク 404エラー解決

**根本対策：パーマリンク構造を数字ベースに変更（確定）**

```
WP管理画面 → 設定 → パーマリンク設定
→「数字ベース」を選択 → 変更を保存
```

変更後のURL形式：`https://setona.co.jp/archives/123`

> ⚠️ 投稿タイトルが日本語でもURLは自動的に数字になるため
> スラッグの手動変換作業・404エラーが完全に解消

> ⚠️ 投稿記事内のリンクはHTMLで直接記述する
> `<a href="https://setona.co.jp/" target="_blank">https://setona.co.jp/</a>`

> ⚠️ 送信済みメールのリンクURLは変更不可。スラッグ変更は次回配信分から反映

---

### ㊱ 投稿HTMLテンプレート作成

**ファイル：** `post-shinki.html`（GitHub管理）

**構成：**
- トップに `<style>` で行間調整CSS追記
- `line-height: 2` / `margin-bottom: 1.4em`
- セクション区切りに `<hr>` 使用
- リンクは `target="_blank"` で別タブ表示

**貼り付け手順：**
```
WP投稿編集画面 → 右上「⋮」→「コードエディター」
→ 全選択削除 → HTMLをペースト → 更新
```

---

### ㊲ サイドバーウィジェット構成変更（確定）

**現在の構成（順番固定）：**
```
① お電話でのご予約
② 店舗概要
③ セトナ会員募集中（MailPoetフォーム）
④ リンクメニュー
⑤ 最近の投稿
⑥ バックナンバー
⑦ かんたん登録用QR（カスタムHTML）← 新設
```

**削除したウィジェット：** カテゴリー（顧客に不要なため）

---

### ㊳ かんたん登録用QRコード設置

**設置場所：** サイドバー最下部（カスタムHTMLウィジェット）
**QR先URL：** `https://setona.co.jp/member-registration/`
**QR生成API：** `api.qrserver.com`（無料・外部API）

**確定HTML：**
```html
<div style="text-align:center; padding:14px 10px;">
  <div style="font-size:13px; font-weight:bold; color:#1a6a4a;
              margin-bottom:12px;">
    かんたん登録用QR
  </div>
  <img src="https://api.qrserver.com/v1/create-qr-code/?size=160x160&data=https://setona.co.jp/member-registration/"
       alt="セトナ会員登録QRコード"
       style="width:160px; height:160px; display:block; margin:0 auto 10px;">
  <p style="font-size:11px; color:#666; line-height:1.7; margin:0;">
    スマホでこちらを読み取っても<br>登録できます
  </p>
</div>
```

---

### ㊴ メール会員登録専用固定ページ作成

| 項目 | 内容 |
|------|------|
| タイトル | メール会員登録 |
| スラッグ | member-registration |
| URL | https://setona.co.jp/member-registration/ |
| MailPoetフォームID | 3（`[mailpoet_form id="3"]`） |

> ⚠️ フォームIDはMailPoet → フォーム編集画面のURLで確認する
> （`id=3` の場合 `[mailpoet_form id="3"]` を使用）

---

### ㊵ ボディ外側背景色 セージグリーン統一

**設定箇所：** 外観 → カスタマイズ → 追加CSS

**追加CSS（確定）：**
```css
/* ── ボディ外側背景：薄いセージグリーン ── */
body,
#wrapper,
.wrap,
#content,
#header,
#footer,
.footer,
.site-footer,
#navi,
.navi-in {
    background-color: #e8f2ec !important;
}
```

> ⚠️ Cocoon のCSSが優先されるため `!important` が必須
> ⚠️ `body` 単体指定では効かない。上記セレクターを全て含めること

---

## 4. 会員登録導線まとめ（確定）

| 導線 | 方法 |
|------|------|
| PCサイドバー | MailPoetフォーム直接入力 |
| PCサイドバーQR | スマホで読み取り → 登録専用ページへ |
| スマホTOPページ | ヘッダーバナー → ポップアップフォーム |
| スマホ投稿ページ | 同上 |

---

## 5. 残タスク

```
[ ] Google Search Console 登録（5月以降でOK）
      → setona2006@gmail.com で登録
      → プロパティ追加 → URL プレフィックス → https://setona.co.jp
      → 所有権確認（SEO SIMPLE PACK経由が簡単）

[ ] at-ml.jp 旧会員への移行案内メール作成・配信（5月）
      → 「新サイト会員登録のお願い」を2〜3回配信
      → 文面はREXに依頼すれば作成可能

[ ] at-ml.jp 解約（5月末）
      → 月9,800円の削減
```

---

## 6. 重要情報（引き継ぎ用）

| 項目 | 値 |
|------|-----|
| WP管理画面 | https://setona.co.jp/wp-admin/ |
| 管理者メール | setona2006@gmail.com |
| お問合せメール | setona@coast.ocn.ne.jp |
| 自社メール | info@setona.co.jp |
| MailPoetフォームID | 3（会員登録フォーム） |
| Brevo SMTPログイン | a78ed9001@smtp-brevo.com |
| さくら会員ID | hml42446 |
| DBサーバー | mysql3114.db.sakura.ne.jp |
| DB名 | bqn03_wp20260404d |
| GA4測定ID | G-WF0TWQVX8W |
| パーマリンク構造 | 数字ベース（archives/123） |
| MailPoet会員登録ページ | https://setona.co.jp/member-registration/ |

---

## 7. 既知の注意事項（追記分）

- **`wp_footer` 出力要素に `position:sticky` は効かない → ヘッダー直下表示は `wp_body_open` フックに配置すること**
- **投稿スラッグは数字ベース設定済み（archives/123）。日本語スラッグは404の原因になるため変更不要**
- **MailPoetフォームIDはWP管理画面のURL（`id=N`）で確認する。サイドバーとページで異なる場合がある**
- **ボディ背景色は `body` 単体では効かない。複数セレクター＋`!important` が必須（Cocoon仕様）**
- **投稿記事内リンクはコードエディター使用時にHTMLで直接記述する**

---

*最終更新：2026-04-13*
*記録：REX（システムエンジニア）*
