# test_concept_B

これは Layer 1（Obsidian 自動処理層）動作確認用の test ファイル B です。

## このファイルが含む Layer 1 要素

- wikilink: [[test_concept_C]] への内部リンク
- tag: #layer1-test

## 確認すべき挙動

1. **backlink 自動形成**: 右ペインの Backlinks に `test_concept_A` が自動表示される（A が B にリンクしているため）
2. **outgoing link**: 右ペインに C への outgoing link が表示される
3. **tag 集約**: `#layer1-test` が A と合算される（カウント 2）
4. **graph view**: A → B → C の中継ノードとして描画される

---

*test 用ファイル・確認後ディレクトリごと削除予定*
