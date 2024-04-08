# read pdf files of scan and convert them to text 
import pytesseract
import pdf2image


def scanned_pdf_to_txt(pdf_file):
    images = pdf2image.convert_from_path(pdf_file)
    text = ""
    for i, image in enumerate(images):
        # image.save("image" + str(i) + ".jpg", "JPEG")
        text += image_to_text(image)
    return text

def image_to_text(image_file):
    return pytesseract.image_to_string(image_file)