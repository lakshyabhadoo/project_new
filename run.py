# from app import create_app
from app.celery_worker import app
# app = create_app()

if __name__ == "__main__":
    app.run(debug=True)