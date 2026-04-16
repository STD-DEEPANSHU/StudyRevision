import pytesseract
from PIL import Image

def read_image(file_path):
    img = Image.open(file_path)
    return pytesseract.image_to_string(img)
