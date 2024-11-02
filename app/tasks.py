# import celery
from flask import current_app
from .models import PDFDocument
from . import db
# from celery import shared_task
from .celery_worker import celery_work
import PyPDF2

# app = create_app()

#
# def extract_text_from_pdf(file_path):
#     text = ""
#     with open(file_path, "rb") as file:
#         reader = PyPDF2.PdfReader(file)
#         for page in reader.pages:
#             text += page.extract_text() or ""
#     return text


@celery_work.task()
def classify_pdf(pdf_id):
    with current_app.app_context():
        pdf = PDFDocument.query.get(pdf_id)
        if pdf is None:
            return "PDF not found"

        # data = extract_text_from_pdf(pdf.file_url)
        text = ""
        with open(pdf.file_url, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
        print(pdf)

        data = text

        # Simple logic to classify PDFs based on extracted text
        if "warranty" in data.lower() or "issue" in data.lower():
            pdf.category = "warranty"
        elif "transaction" in data.lower() or "rupee" in data.lower():
            pdf.category = "transaction"
        elif "help" in data.lower() or "trouble" in data.lower():
            pdf.category = "troubleshooting"
        else:
            pdf.category = "uncategorized"  # Default category

        db.session.commit()  # Commit changes to the database
        return pdf.category
