# HP-DESIGN-CONFIRMED_6.md
## セトナ治療院 HP構築 作業進捗記録

**プロジェクト名**：有限会社セトナ HP自社管理環境構築  
**担当**：湊ミナト（ディレクター）／ REX（システムエンジニア）／ ClaudeCode（実装担当）
**リポジトリ**：https://github.com/Minato33440/Setona_HP  

---

## ✅ 確定済み方針

| 項目 | 内容 |
|------|------|
| 新ドメイン | setona.co.jp（さくらインターネット取得・法人名義） |
| サーバー | さくらインターネット スタンダード（既存契約・bqn03.sakura.ne.jp） |
| CMS | WordPress 最新版 |
| テーマ | Cocoon（子テーマ：cocoon-child-master 有効化済み） |
| メール配信 | MailPoet × Brevo（設定完了・DNS認証反映待ち） |
| お問合せ | Contact Form 7 |
| SEO | SEO SIMPLE PACK |
| デザイン | `Setona_v4.html` を設計書として採用（確定） |
| 画像パス（ローカル） | `data/png/` フォルダに統一（**小文字必須**） |
| 画像パス（WP実装後） | `/wp-content/themes/cocoon-child-master/images/` |
| ナビゲーション | PC：横スクロール式 / スマホ：`<select>`ドロップダウン式 |
| サイドバー | 右サイドバー固定（スマホ時は本文下に移動） |
| 旧ドメイン | setona.net は at-ml.jp のまま当面継続（新旧並行運用） |
| DNS切り替え | 不要（setona.co.jp は完全新規ドメインのため即時公開可） |

---

## 🏗️ システム管理アーキテクチャ（2026-04-07 確認・整理）

### 全体構造の理解

本プロジェクトの環境は「さくら管理」と「WordPress管理」の二層構造になっている。

```
┌─────────────────────────────────────────────────┐
│              さくら管理領域                        │
│                                                   │
│  ・コントロールパネル（ドメイン・サーバー設定）       │
│  ・phpMyAdmin（DB管理ツール）                      │
│                                                   │
│  ┌──────────────────────────────────────────┐    │
│  │  MySQL データベース（器はさくら管理）        │    │
│  │  DB名：bqn03_wp20260404d                  │    │
│  │                                            │    │
│  │  ┌──────────────────────────────────┐    │    │
│  │  │  DB の中身（WPが読み書き）          │    │    │
│  │  │  wpposts   / wpoptions / wpusers  │    │    │
│  │  └──────────────────────────────────┘    │    │
│  └──────────────────────────────────────────┘    │
│                                                   │
│  ┌──────────────────────────────────────────┐    │
│  │  ファイルシステム（Webサーバー）            │    │
│  │  ~/www/setona.co.jp/                      │    │
│  │                                            │    │
│  │  ・WordPressコア（自動インストール済み）     │    │
│  │  ・wp-config.php（DB接続情報・橋渡し役）    │    │
│  │  ・テーマファイル（FTPでアップロード）       │    │
│  │  ・画像ファイル（FTPでアップロード）         │    │
│  └──────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

### 管理手段の使い分け

| 操作対象 | 管理手段 | 理由 |
|---------|---------|------|
| ドメイン・サーバー設定 | さくらコンパネ | さくらの管理領域 |
| DBの器（作成・削除） | さくらコンパネ | さくらの管理領域 |
| DBの中身（コンテンツ・設定） | WP管理画面 | WPが通常の読み書き担当 |
| DBの中身（強制・一括操作） | phpMyAdmin | SQL直接実行が必要な場合 |
| テーマファイル・画像 | FTP（FileZilla） | ファイルシステム上にある |
| wp-config.php | FTP（FileZilla） | ファイルシステム上にある |
| プラグイン | WP管理画面（またはFTP） | どちらでも可 |

> **原則：「データ」はDB経由、「ファイル」はFTP経由。さくらコンパネはその両方の器を管理するだけ。**

---

## 📋 作業ログ

### 2026-04-04〜04-07（詳細はHP-DESIGN-CONFIRMED_4.md参照）

- WP基盤構築・テーマ・プラグイン導入
- 全7固定ページ コンテンツ実装
- 画像アップロード・パス修正
- ナビ・サイドバー・ボトムナビ設定
- 予約カレンダーページ（ID:43）実装
- GitHub リポジトリ パス修正プッシュ完了

---

### 2026-04-08（詳細はHP-DESIGN-CONFIRMED_5.md参照）

- 各ページ表示確認・レイアウト修正（スタッフ・本院・美容コース）
- Contact Form 7 設定（フォームID: a71a300）
- メールリンク修正（旧空メール廃止・自社メール統一）
- SSL証明書（Let's Encrypt）設定・https化完了
- 検索インデックスON → **setona.co.jp 正式公開**
- 旧サイト（at-ml.jp）への移行案内掲載
- GA4設定（測定ID: G-WF0TWQVX8W）

---

### 2026-04-09

#### ㉓ MailPoet × Brevo 設定

**① Brevoアカウント作成**

- URL：https://www.brevo.com
- 登録メール：setona2006@gmail.com
- 会社名：Setona.,co.ltd
- 無料プランで登録完了

**② DNSレコード追加（ドメイン認証）**

さくらインターネット DNSゾーン編集に以下3レコードを追加：

| # | 種別 | ホスト名 | 値 |
|---|------|---------|-----|
| 1 | TXT | `brevo1._domainkey` | `brevo-code:d2066c67ef2e40ad37945f3eb85c0a74` |
| 2 | CNAME | `brevo2._domainkey` | `b2.setona-co-jp.dkim.brevo.com.`（末尾ドット必須） |
| 3 | TXT | `_dmarc` | `"v=DMARC1; p=none; rua=mailto:rua@dmarc.brevo.com"` |

> ⚠️ **CNAMEレコードの値に末尾ドット（`.`）が必須**  
> さくらのDNSパネルはCNAME参照先を内部検証するため、外部ドメインはそのままでは保存エラーになる。  
> FQDNとして末尾に `.` を付けることで検証をバイパスできる。

> ⚠️ **DMARCのTXT値はダブルクォーテーションで囲む**  
> さくらのDNSパネルの仕様上、複数要素を含むTXT値は引用符が必要。

> ⚠️ **さくらDNSの「新規エントリー追加」はページ最下部の「追加する」ボタンを使う**  
> 各エントリー内の「追加する」はそのドメイン配下へのレコード追加（ホスト名なし）なので別物。

**③ MailPoetアカウント接続**

- MailPoetスタータープラン登録（最大500購読者・無料）
- アクティベーションキー（MailPoet APIキー）をWP管理画面で入力・接続完了

**④ SMTP設定（Brevo経由送信）**

MailPoet → 設定 → 送信方法 → SMTPポートを選択して以下を設定：

| 項目 | 値 |
|------|-----|
| SMTPホスト名 | `smtp-relay.brevo.com` |
| SMTPポート | `587` |
| ログイン | `setona2006@gmail.com` |
| パスワード | BrevoのSMTPキー（.envで管理） |
| 安全な接続 | `TLS` |
| 認証 | `はい` |

> ⚠️ **MailPoetの送信方法選択肢にBrevoは表示されない**  
> 「あなたのプロバイダを選択」のドロップダウンにBrevoはない。  
> → 「SMTPポート」を選択してBrevoのSMTP情報を手動入力する。

**⑤ テスト送信確認**

- テストメール送信 → setona2006@gmail.com で受信確認 ✅
- 件名「MailPoet で送信できます！」が届いた

#### ㉔ info@setona.co.jp メールアドレス作成

送信者をフリーメール（@gmail.com）から自社ドメインに変更するため作成。

| 項目 | 値 |
|------|-----|
| メールアドレス | `info@setona.co.jp` |
| 作成場所 | さくらコントロールパネル → メールボックス |
| メール容量 | 1GB |
| 受信設定 | 受信する |
| 迷惑メールフィルター | 簡易・迷惑メールフォルダに保存 |
| ウイルスチェック | 有効 |

- Brevoの送信者として `info@setona.co.jp` を追加済み
- ドメイン認証はDNS反映待ち（最大48時間）

---

## 🔴 残タスク（優先順）

```
[✅] Brevoアカウント作成
[✅] DNSレコード追加（DKIM・DMARC）
[✅] MailPoetアカウント接続・SMTP設定
[✅] テスト送信確認
[✅] info@setona.co.jp 作成
[⏳] Brevoドメイン認証の最終確認
      → Brevo管理画面 → Senders & IP → Domains
      → setona.co.jp の✅を確認（DNS反映後・最大48時間）
[⏳] MailPoetの送信者をinfo@setona.co.jpに変更
      → ドメイン認証完了後に実施
[ ] Google Search Console登録
      → analytics.google.com と同じ setona2006@gmail.com で登録
      → プロパティ追加 → URL プレフィックス → https://setona.co.jp
      → 所有権確認（HTMLファイル or SEO SIMPLE PACK経由）
[ ] メール会員登録フォーム作成・サイト設置
      → MailPoetフォームを作成
      → TOPページ・サイドバーの仮リンクを正式フォームに差し替え
[ ] MailPoet × Brevo テンプレート作成
      → セトナ治療院ブランドに合わせたメールテンプレート作成
[ ] at-ml.jp解約（5月末）
      → 旧会員への移行促進（5月配信で2〜3回案内）後に実施
      → 月9,800円の削減
```

---

## 📅 移行スケジュール

| 時期 | アクション |
|------|-----------|
| 4月中 | MailPoet × Brevo設定完了・会員登録フォーム設置 |
| 5月配信分 | at-ml.jpから「新サイト会員登録のお願い」を2〜3回配信 |
| 5月末 | at-ml.jp解約（月9,800円削減） |
| 6月〜 | setona.co.jp側で新規リストに配信開始 |

---

## 📌 重要情報

| 項目 | 値 |
|------|-----|
| WP管理画面 | https://setona.co.jp/wp-admin/ |
| 管理者メール | setona2006@gmail.com |
| お問合せメール | setona@coast.ocn.ne.jp |
| 自社メール（新規） | info@setona.co.jp（さくら作成済み） |
| CF7フォームID | a71a300 |
| さくら会員ID | hml42446 |
| DBサーバー | mysql3114.db.sakura.ne.jp |
| DB名 | bqn03_wp20260404d |
| GA4 測定ID | G-WF0TWQVX8W |
| MailPoet APIキー | 9d543e05ce90598ed5f2fcb127f67d1a |
| Brevo SMTPホスト | smtp-relay.brevo.com:587 / TLS |
| Brevo SMTPログイン | setona2006@gmail.com |
| Brevo SMTP Key | .envで管理（チャットに記載しない） |
| 旧サイト | https://setona.net/71186/（at-ml.jp・月9,800円）|
| GitHub | https://github.com/Minato33440/Setona_HP |
| Googleカレンダー共有URL | https://calendar.google.com/calendar/u/0?cid=MjM2NzZkOWJhMDQ5ZmEwOWU0ODE0ZjAxMTFkNDM5M2Y1MzZhMTUxOGI5MDM1YjUzNjgxOTRmNmFhMjE2YTViMUBncm91cC5jYWxlbmRhci5nb29nbGUuY29t |

---

## ⚠️ 既知の注意事項

- 画像パスは必ず小文字 `data/png/`（`Data/png/` は誤り）
- WP実装後の正しい画像パス：`/wp-content/themes/cocoon-child-master/images/`
- ブラウザキャッシュ：画像差し替え後はCtrl+Shift+R（Mac: Cmd+Shift+R）で強制リロード
- WPのscriptタグ制約：ページ本文の`<script>`はsave時に削除される → JSはfunctions.phpへ
- FileZillaはサイトマネージャーから接続（クイック接続バー不可）
- さくらのFTPパスワードは会員ログインPWとは別（サーバーPW）
- phpMyAdminのパスワードはFTPパスワードとは別（wp-config.phpのDB_PASSWORDを使用）
- All In One SEO・Yoast SEO はCocoonと競合するため絶対に入れない
- GA4の旧測定ID `G-8HQP97H7QR` は未使用・正式IDは `G-WF0TWQVX8W`
- **APIキー・SMTPキー等の機密情報はチャットに貼らず.envで管理する**
- **BrevoのCNAMEレコードは末尾ドット付きFQDNで登録する（さくらDNS仕様）**
- **DMARCレコードの値はダブルクォーテーションで囲む（さくらDNS仕様）**
- **MailPoetの送信方法でBrevoを選ぶ場合は「SMTPポート」を選択して手動設定**
- メール会員リンク：現在は仮（setona@coast.ocn.ne.jp）→ MailPoetフォーム作成後に差し替え

---

*最終更新：2026-04-09*  
*記録：REX（システムエンジニア）*
