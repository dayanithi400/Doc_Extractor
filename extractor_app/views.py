import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.pdf_parser import extract_pdf_content, extract_tables

from django.shortcuts import render
from .forms import PDFUploadForm
from .models import ExtractedContent
from utils.pdf_parser import extract_pdf_content, extract_tables
from utils.db import store_content
import os
from django.conf import settings


def upload_pdf(request):
    if request.method == "POST":
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']
            upload_dir = settings.MEDIA_ROOT
            os.makedirs(upload_dir, exist_ok=True)

            file_path = os.path.join(upload_dir, uploaded_file.name)
            with open(file_path, 'wb+') as dest:
                for chunk in uploaded_file.chunks():
                    dest.write(chunk)

            # Extract current file's content
            texts, images = extract_pdf_content(file_path)
            tables = extract_tables(file_path)

            # Optional: store in DB if you still want to log it
            for text in texts:
                store_content("text", text)
            for img_path in images:
                store_content("image", img_path)
            for table in tables:
                store_content("table", str(table))

            return render(request, "extractor_app/result.html", {
                "texts": texts,
                "images": [img.replace("static/", "/static/") for img in images],  # Fix path
                "tables": tables
            })
    else:
        form = PDFUploadForm()
    return render(request, "extractor_app/upload.html", {"form": form})
