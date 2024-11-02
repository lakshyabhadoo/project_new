from . import db
from datetime import datetime


class PDFDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    file_url = db.Column(db.String(300), nullable=True)
    category = db.Column(db.String(50), nullable=True)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    task_id = db.Column(db.String(120), nullable=True)


class TaskHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reference_id = db.Column(db.String(120), nullable=True)
    status = db.Column(db.String(200), nullable=True)
    # response = db.Column(db.String(200), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
