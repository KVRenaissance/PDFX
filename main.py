import fitz #PyMuPDF
import PIL.Image # pillow
import io
import re
import tkinter as tk
from tkinter import filedialog
from pdfminer.high_level import extract_pages, extract_text

root = tk.Tk()
root.withdraw()

file_selected = False
file = filedialog.askopenfilename(title="Select your PDF", filetypes=[("PDF files", "*.pdf")])
if file:
    print(f"User selected file path: {file}")
    file_selected = True
else:
    print(f"Nothing selected or invalid selection")

def get_images(file):
    pdf = fitz.open(file)
    counter = 1
    for i in range(len(pdf)):
        page = pdf[i]
        images = page.get_images()
        for image in images:
            base_img = pdf.extract_image(image[0])
            image_data = base_img["image"]
            img = PIL.Image.open(io.BytesIO(image_data))
            extension = base_img["ext"]
            img.save(open(f"image{counter}.{extension}", "wb"))
            counter += 1

def get_chapter_headings(file):
    text = extract_text(file)
    pattern = re.compile(r"^\d{1,2}+\.\s[A-Z][a-z]*(?:\s[A-Za-z]*)*", re.MULTILINE)
    matches = pattern.findall(text)
    clean_matches = [re.sub(r"[\t\n]+", " ", match).strip() for match in matches]
    filtered_matches = [match for match in clean_matches if len(match.split()) >2]

    for match in filtered_matches:
        print(match)

if (file_selected):
    get_chapter_headings(file)