# GCVisionAPI Code Explanation

このドキュメントでは、OCRツールアプリケーションのコード構造と主要な関数について説明します。

## 主要なライブラリとインポート

```python
import streamlit as st
from google.cloud import vision
from google.oauth2 import service_account
import os
import json
from pdf2image import convert_from_bytes
import io
```

- `streamlit`: Webアプリケーションのフロントエンド構築に使用
- `google.cloud.vision`: Google Cloud Vision APIを利用したOCR処理に使用
- `google.oauth2.service_account`: Google Cloud認証に使用
- `pdf2image`: PDFファイルを画像に変換するために使用

## グローバル変数

```python
MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB
SUPPORTED_TYPES = ["png", "jpg", "jpeg", "pdf"]
MAX_IMAGES = 5
```

これらの変数は、アップロードされるファイルの制限を定義します。

## 関数の説明

### `load_markdown_file(filename)`

指定されたMarkdownファイルを読み込み、その内容を文字列として返します。

### `transcribe_image(image_content)`

画像コンテンツを受け取り、Google Cloud Vision APIを使用してOCR処理を行います。

1. Heroku環境変数から認証情報を読み込みます。
2. Vision APIのクライアントを初期化します。
3. 画像に対してOCR処理を実行し、抽出されたテキストを返します。

### `process_pdf(pdf_file)`

PDFファイルを処理し、各ページのテキストを抽出します。

1. PDFファイルを画像に変換します。
2. 各画像に対して`transcribe_image`関数を呼び出し、OCR処理を行います。
3. 全ページのテキストを結合して返します。

### `process_multiple_images(uploaded_files)`

複数の画像ファイルを処理します。

1. アップロードされた各ファイルに対してOCR処理を実行します。
2. サポートされていない形式のファイルがあれば警告を表示します。
3. 全画像のテキストを結合して返します。

### `show_setting_modal()`

アプリケーションの説明とプライバシーガイドラインを表示するモーダルを作成します。

1. "アプリについて"と"プライバシーガイドライン"の2つのタブを作成します。
2. 各タブの内容をMarkdownファイルから読み込んで表示します。

### `main()`

アプリケーションのメイン関数です。

1. ファイルアップロードのインターフェースを作成します。
2. アップロードされたファイルを検証し、サイズと数の制限をチェックします。
3. PDFファイルか画像ファイルかを判断し、適切な処理関数を呼び出します。
4. OCR処理の結果を表示し、ダウンロードボタンを提供します。
5. アプリの説明を表示するボタンを作成します。

## コードの流れ

1. ユーザーがファイルをアップロードします。
2. アップロードされたファイルの数とサイズが制限内かチェックします。
3. PDFファイルの場合は`process_pdf`関数、複数の画像ファイルの場合は`process_multiple_images`関数を呼び出します。
4. OCR処理の結果を表示し、テキストのダウンロードオプションを提供します。
5. ユーザーが「アプリの説明」ボタンをクリックすると、`show_setting_modal`関数が呼び出されます。

## 注意点

- このアプリケーションはHeroku環境での実行を想定しています。
- Google Cloud認証情報は環境変数から読み込まれます。
- エラーハンドリングはPDF処理時のみ実装されています。他の部分でのエラーハンドリングを強化することをお勧めします。
- 大量のファイルやサイズの大きなファイルを処理する際のパフォーマンスに注意が必要です。

