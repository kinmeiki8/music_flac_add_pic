# FLAC Artwork Embedder using iTunes API

iTunes API (Apple Music) を活用し、検索が難しいアジア圏（日本・韓国・台湾など）の楽曲でも確実に高画質のアルバムアートワークを検索・取得し、FLACファイルに自動で埋め込むスクリプトです。

##  特徴

- **アジア圏の楽曲に強い**: `country` パラメータを最適化し、邦楽やK-POPのメタデータ・画像を正確にヒットさせます。
- **高画質アートワークの取得**: iTunes APIから取得できる画像を自動ダウンロードします。
- **自動埋め込み**: Pythonの `mutagen` ライブラリを使用し、FLACファイルの `PICTURE` メタデータに画像を安全に埋め込みます。

##  動作環境

- Python 3.8以上
- 必須ライブラリ:
  - `requests` (API通信用)
  - `mutagen` (FLACメタデータ操作用)

##  セットアップ

1. 本リポジトリをクローンまたはダウンロードします。
2. 必要な依存ライブラリをインストールします。

```bash
pip install requests mutagen

##  実行

```bash
python music.py
