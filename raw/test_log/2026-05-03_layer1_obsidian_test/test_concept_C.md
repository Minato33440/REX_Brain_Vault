# test_concept_C

これは Layer 1（Obsidian 自動処理層）動作確認用の test ファイル C です。

## このファイルが含む Layer 1 要素

- wikilink: [[test_concept_A]] への内部リンク（A → B → C → A の循環構造を完成させる）
- tag: #obsidian-core （A・B とは別のタグ）

## 確認すべき挙動

1. **backlink 自動形成**: 右ペインの Backlinks に `test_concept_B` が自動表示される（B が C にリンクしているため）
2. **outgoing link**: A への outgoing link が表示される（循環）
3. **tag 集約**: `#obsidian-core` が独立カウントされる（A・B の `#layer1-test` とは別）
4. **graph view**: 三角形（A → B → C → A）の連想ネットワークが描画される

## このテストの総合判定

A・B・C 三ファイルがそろって以下が観察できれば Layer 1 全機能が稼働している:

- [x] **Backlinks 自動形成**: 各ファイルの Backlinks pane に逆参照が自動表示
- [x] **Wikilink ライブレンダリング**: `[[...]]` 記法が編集中もリンクとして表示
- [x] **Tags 自動集約**: 左ペインの Tags pane に `#layer1-test` (count=2) と `#obsidian-core` (count=1) が表示
- [x] **Graph view 連想ネットワーク**: 三角形構造が可視化

これらが Anthropic デフォルトメモリーシステムにおける「自動連想注入の発火経路」と相同性を持つ Vault 規模実装の基盤となる。

---

*test 用ファイル・確認後ディレクトリごと削除予定*
