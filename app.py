import streamlit as st
from google.cloud import vision
from google.oauth2 import service_account
import os
import json
from pdf2image import convert_from_bytes
import io

MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB
SUPPORTED_TYPES = ["png", "jpg", "jpeg", "pdf"]
MAX_IMAGES = 5


def load_markdown_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()


def transcribe_image(image_content):
    # Heroku環境での認証情報の読み込み
    credentials_json = json.loads(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    credentials = service_account.Credentials.from_service_account_info(credentials_json)
    client = vision.ImageAnnotatorClient(credentials=credentials)

    image = vision.Image(content=image_content)

    # OCR execution
    response = client.document_text_detection(image=image)
    return response.full_text_annotation.text


def process_pdf(pdf_file):
    try:
        pdf_bytes = pdf_file.read()
        images = convert_from_bytes(pdf_bytes)

        all_text = ""
        for i, image in enumerate(images):
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

            text = transcribe_image(img_byte_arr)
            all_text += f"--- ページ {i + 1} ---\n{text}\n\n"

        return all_text
    except Exception as e:
        st.error(f"PDFの処理中にエラーが発生しました: {str(e)}")
        return None


def process_multiple_images(uploaded_files):
    all_text = ""
    for i, file in enumerate(uploaded_files):
        if file.type.split('/')[1] in SUPPORTED_TYPES:
            text = transcribe_image(file.read())
            all_text += f"--- 画像 {i + 1} ---\n{text}\n\n"
        else:
            st.warning(f"ファイル '{file.name}' はサポートされていない形式です。スキップします。")
    return all_text


def show_setting_modal():
    with st.expander("説明"):
        tab1, tab2 = st.tabs(["アプリについて", "プライバシーガイドライン"])

        with tab1:
            readme_content = load_markdown_file("README.md")
            st.markdown(readme_content)

        with tab2:
            privacy_content = load_markdown_file("privacy_guidelines.md")
            st.markdown(privacy_content)


def main():
    st.title("画像ファイルのOCRツール")

    uploaded_files = st.file_uploader("5枚までの画像ファイルまたは1つのPDFファイル(20ページまで)をアップロードしてください",
                                      type=SUPPORTED_TYPES, accept_multiple_files=True)

    if uploaded_files:
        total_size = sum(file.size for file in uploaded_files)
        if total_size <= MAX_FILE_SIZE and len(uploaded_files) <= MAX_IMAGES:
            transcription_message = st.empty()
            transcription_message.subheader("OCR処理中…")

            if len(uploaded_files) == 1 and uploaded_files[0].type == "application/pdf":
                transcript = process_pdf(uploaded_files[0])
            else:
                transcript = process_multiple_images(uploaded_files)

            transcription_message.empty()

            if transcript:
                st.subheader("出力結果")
                st.text_area("OCR文章", transcript, height=500)
                st.download_button("ダウンロード", transcript.encode("utf-8"), "transcription.txt", "text/plain")
        elif total_size > MAX_FILE_SIZE:
            st.error("ファイルサイズの合計が大きすぎます。合計200MB以下のファイルをアップロードしてください。")
        else:
            st.error(f"アップロードできる画像は最大{MAX_IMAGES}枚までです。")

    if st.button("アプリの説明"):
        show_setting_modal()


if __name__ == "__main__":
    main()
