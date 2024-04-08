# read pdf files of scan and convert them to text 

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Replace with your path if different


import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os 
import pdf2image


pdf_file = "Voltaire-rue-17.161.pdf"


images = convert_from_path(pdf_file)

text =""

for i, image in enumerate(images):
    image.save("image"+str(i)+".jpg", "JPEG")
    text += pytesseract.image_to_string(image)

print(text)


with open("output.txt", "w") as f:
    f.write(text)