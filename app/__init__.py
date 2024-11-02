from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from .celery_worker import make_celery
from .config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    # celery = make_celery(app)

    # Register blueprints or routes
    from .views import main as main_blueprint
    app.register_blueprint(main_blueprint)#, url_prefix='/')

    # Create all tables defined in models.py if they don't exist
    with app.app_context():
        # Import and register your tasks here to avoid circular imports
        # from . import tasks
        # create all database tables
        db.create_all()

    return app
