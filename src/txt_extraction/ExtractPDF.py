# importing required modules 
from pypdf import PdfReader 
  
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path) 
    stream = ""
    for page in reader.pages:
        stream += page.extract_text()
    return stream
