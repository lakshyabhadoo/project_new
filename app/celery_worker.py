from celery import Celery
from . import create_app


def make_celery(app):
    celery_ = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'], broker=app.config['CELERY_BROKER_URL'])
    celery_.conf.update(app.config)
    celery_.autodiscover_tasks()
    return celery_


app = create_app()  # Create an instance of your Flask app
with app.app_context():
    from .tasks import classify_pdf

celery_work = make_celery(app)  # Create a Celery instance
