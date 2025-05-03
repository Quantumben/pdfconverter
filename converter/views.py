from django.shortcuts import render
from .forms import PDFUploadForm
from .models import UploadedPDF
from pdf2docx import Converter
import os
from django.conf import settings


# Create your views here.
def upload_pdf(request):
    docx_file = None
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_pdf = form.save()

            pdf_path = uploaded_pdf.file.path
            docx_path = os.path.splitext(pdf_path)[0] + '.docx'

            cv = Converter(pdf_path)
            cv.convert(docx_path, start=0, end=None)
            cv.close()

            docx_file = os.path.basename(docx_path)
    else:
        form = PDFUploadForm()

    return render(request, 'converter/upload.html', {
        'form': form,
        'docx_file': docx_file
    })