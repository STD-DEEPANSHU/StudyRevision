import pdfplumber
import requests
from bs4 import BeautifulSoup

def read_pdf(file):
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t
    except Exception as e:
        print("PDF ERROR:", e)
    return text


def read_website(url):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        return soup.get_text()
    except Exception as e:
        print("WEB ERROR:", e)
        return ""


def read_text(text):
    return text
