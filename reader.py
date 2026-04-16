import pdfplumber
import requests
from bs4 import BeautifulSoup

def read_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for p in pdf.pages:
            t = p.extract_text()
            if t:
                text += t
    return text[:10000]

def read_website(url):
    res = requests.get(url, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")
    return soup.get_text()[:10000]
