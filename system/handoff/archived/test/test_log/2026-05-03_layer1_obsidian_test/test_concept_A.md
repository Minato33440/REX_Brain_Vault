# test_concept_A

これは Layer 1（Obsidian 自動処理層）動作確認用の test ファイル A です。

## このファイルが含む Layer 1 要素

- wikilink: [[test_concept_B]] への内部リンク
- tag: #layer1-test

## 確認すべき挙動

1. **wikilink レンダリング**: `[[test_concept_B]]` がライブプレビュー上で青いリンクとして表示される
2. **outgoing link**: 右ペインに「B への outgoing link」が表示される
3. **tag 集約**: 左ペインの Tags pane で `#layer1-test` がカウントされる
4. **graph view**: A から B への矢印が描画される

---

*test 用ファイル・確認後ディレクトリごと削除予定*
