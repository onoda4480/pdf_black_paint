import pymupdf
import os
import sys


def load_redact_list(file_path="redact_list.txt"):
    """黒塗りする文字列のリストを読み込む"""
    if not os.path.exists(file_path):
        print(f"エラー: {file_path} が見つかりません")
        print(f"redact_list.example.txt をコピーして {file_path} を作成してください")
        sys.exit(1)

    redact_texts = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # 空行とコメント行（#で始まる行）をスキップ
            if line and not line.startswith("#"):
                redact_texts.append(line)

    return redact_texts


def redact_pdf(input_pdf, output_pdf, redact_texts):
    """PDFから指定された文字列を黒塗りする"""
    doc = pymupdf.open(input_pdf)

    for page in doc:
        for text in redact_texts:
            # 文字列を検索して黒塗り範囲を追加
            text_instances = page.search_for(text)
            for inst in text_instances:
                page.add_redact_annot(inst, fill=(0, 0, 0))  # 黒で塗りつぶし

        # 黒塗りを適用
        page.apply_redactions()

    # 黒塗り済みPDFを保存
    doc.save(output_pdf)
    doc.close()
    print(f"黒塗り完了: {output_pdf}")


if __name__ == "__main__":
    # 黒塗りする文字列を読み込む
    redact_texts = load_redact_list("redact_list.txt")

    if not redact_texts:
        print("警告: 黒塗りする文字列が指定されていません")
        sys.exit(1)

    print(f"黒塗りする文字列: {len(redact_texts)}個")

    # PDFを黒塗り
    input_pdf = "pdf/invoice.pdf"
    output_pdf = "pdf/invoice_redacted.pdf"

    if not os.path.exists(input_pdf):
        print(f"エラー: {input_pdf} が見つかりません")
        sys.exit(1)

    redact_pdf(input_pdf, output_pdf, redact_texts)
