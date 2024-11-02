import os


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///pdf_classifications.db'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app/uploads')
