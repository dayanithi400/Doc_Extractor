import fitz  # PyMuPDF
import os
import uuid
import pdfplumber

from django.conf import settings
UPLOAD_DIR = settings.MEDIA_ROOT


def extract_pdf_content(file_path):
    texts = []
    image_paths = []

    doc = fitz.open(file_path)
    for i, page in enumerate(doc):
        # Extract text
        text = page.get_text()
        texts.append(text.strip())

        # Extract images
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_filename = f"{uuid.uuid4()}.{image_ext}"
            image_path = os.path.join(UPLOAD_DIR, image_filename)

            # Make sure folder exists
            os.makedirs(UPLOAD_DIR, exist_ok=True)

            with open(image_path, "wb") as img_file:
                img_file.write(image_bytes)

            image_paths.append(image_path)

    doc.close()
    return texts, image_paths

def extract_tables(file_path):
    tables = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                tables.append(table)
    return tables
