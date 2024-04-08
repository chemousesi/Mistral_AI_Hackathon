from ExtractPDF import extract_text_from_pdf
from ocr import scanned_pdf_to_txt, image_to_text

def extract_text(path):
    try:
        if path.endswith(".pdf"):
            stream = extract_text_from_pdf(path)
            if stream == "":
                stream = scanned_pdf_to_txt(path)
            return stream
        elif path.endswith(".jpg") or path.endswith(".png") or path.endswith(".jpeg"):
            return image_to_text(path)
        elif path.endswith(".txt") or path.endswith(".docx") or path.endswith(".doc"):
            with open(path, "r") as file:
                return file.read()
    except Exception as e:
        print(f"An error occurred: {e}")
    return None