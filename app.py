import streamlit as st
import pymupdf
import io


def redact_pdf_from_bytes(pdf_bytes, redact_texts):
    """PDFバイトデータから指定された文字列を黒塗りする"""
    # バイトデータからPDFを開く
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")

    redaction_count = 0

    for page in doc:
        for text in redact_texts:
            # 文字列を検索して黒塗り範囲を追加
            text_instances = page.search_for(text)
            for inst in text_instances:
                page.add_redact_annot(inst, fill=(0, 0, 0))  # 黒で塗りつぶし
                redaction_count += 1

        # 黒塗りを適用
        page.apply_redactions()

    # 黒塗り済みPDFをバイトデータとして保存
    output_bytes = doc.tobytes()
    doc.close()

    return output_bytes, redaction_count


# Streamlitアプリのメイン部分
st.set_page_config(page_title="PDF黒塗りツール", page_icon="📄")

st.title("📄 PDF黒塗りツール")
st.markdown("PDFファイルから指定した文字列を黒塗りにします")

# サイドバーに説明を追加
with st.sidebar:
    st.header("使い方")
    st.markdown("""
    1. PDFファイルをアップロード
    2. 黒塗りしたい文字列を入力（1行に1つ）
    3. 「黒塗り実行」ボタンをクリック
    4. 黒塗り済みPDFをダウンロード
    """)

    st.header("注意事項")
    st.markdown("""
    - アップロードされたファイルは処理後に削除されます
    - 黒塗りは元に戻せません
    - 必ず元ファイルのバックアップを取ってください
    """)

# PDFファイルのアップロード
uploaded_file = st.file_uploader(
    "PDFファイルを選択してください",
    type=["pdf"],
    help="黒塗りしたいPDFファイルをアップロードしてください"
)

# 黒塗りする文字列の入力
st.subheader("黒塗りする文字列")
redact_input = st.text_area(
    "黒塗りしたい文字列を入力してください（1行に1つ）",
    height=200,
    placeholder="例：\n山田太郎\n東京都渋谷区〇〇1-2-3\n090-1234-5678",
    help="黒塗りしたい文字列を1行に1つずつ入力してください"
)

# 黒塗り実行ボタン
if st.button("🖊️ 黒塗り実行", type="primary", use_container_width=True):
    if not uploaded_file:
        st.error("PDFファイルをアップロードしてください")
    elif not redact_input.strip():
        st.error("黒塗りする文字列を入力してください")
    else:
        try:
            # 黒塗りする文字列のリストを作成
            redact_texts = [
                line.strip()
                for line in redact_input.split("\n")
                if line.strip() and not line.strip().startswith("#")
            ]

            if not redact_texts:
                st.error("有効な黒塗り文字列がありません")
            else:
                with st.spinner("黒塗り処理中..."):
                    # PDFファイルを読み込む
                    pdf_bytes = uploaded_file.read()

                    # 黒塗り処理を実行
                    output_bytes, redaction_count = redact_pdf_from_bytes(
                        pdf_bytes, redact_texts
                    )

                st.success(f"✅ 黒塗り完了！（{redaction_count}箇所を黒塗りしました）")

                # ダウンロードボタン
                st.download_button(
                    label="📥 黒塗り済みPDFをダウンロード",
                    data=output_bytes,
                    file_name=f"redacted_{uploaded_file.name}",
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True
                )

        except Exception as e:
            st.error(f"エラーが発生しました: {str(e)}")

# プレビュー表示
if uploaded_file:
    st.divider()
    st.subheader("アップロードされたファイル")
    st.info(f"ファイル名: {uploaded_file.name} | サイズ: {uploaded_file.size / 1024:.2f} KB")