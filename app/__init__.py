import os
from flask import Flask, render_template
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from config import Config
import logging
from flask.logging import default_handler
from logging.handlers import RotatingFileHandler
from celery import Celery

admin = Admin()
migrate = Migrate()
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL,
                result_backend=Config.RESULT_BACKEND)


def create_app():
    app = Flask(__name__)

    # Configure the flask app instance
    CONFIG_TYPE = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(CONFIG_TYPE)

    # Configure celery
    celery.conf.update(app.config)

    register_blueprints(app)

    initialize_extensions(app)

    register_error_handlers(app)

    configure_logging(app)

    return app


def register_blueprints(app):
    from app.main import main_blueprint
    from app.auth import auth_blueprint
    from app.play import play_blueprint
    from app.create import create_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(play_blueprint, url_prefix='/play')
    app.register_blueprint(create_blueprint, url_prefix='/create')


def initialize_extensions(app):
    from app.models import db

    db.init_app(app)
    create_db(app, db)

    migrate.init_app(app, db)

    admin.init_app(app)
    admin.name = "Maddest Libber Admin"
    configure_admin_pages(app)


def create_db(app, db):
    with app.app_context():
        db.create_all()
        print("Database created at:", app.config['SQLALCHEMY_DATABASE_URI'])


def configure_admin_pages(app):
    from app.models import db, Tag, Story_Tag, Story, Response, ResponseSet
    admin.add_view(ModelView(Tag, db.session))
    admin.add_view(ModelView(Story_Tag, db.session))
    admin.add_view(ModelView(Story, db.session))
    admin.add_view(ModelView(Response, db.session))
    admin.add_view(ModelView(ResponseSet, db.session))


def register_error_handlers(app):

    # 400 - Bad Request
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('400.html'), 400

    # 403 - Forbidden
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('403.html'), 403

    # 404 - Page Not Found
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    # 405 - Method Not Allowed
    @app.errorhandler(405)
    def method_not_allowed(e):
        return render_template('405.html'), 405

    # 500 - Internal Server Error
    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500


def configure_logging(app):

    # Deactivate the default flask logger so that log messages don't get duplicated
    app.logger.removeHandler(default_handler)

    # Create a file handler object
    file_handler = RotatingFileHandler(
        'instance/flaskapp.log', maxBytes=16384, backupCount=20)

    # Set the logging level of the file handler object so that it logs INFO and up
    file_handler.setLevel(logging.INFO)

    # Create a file formatter object
    file_formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(filename)s: %(lineno)d]')

    # Apply the file formatter object to the file handler object
    file_handler.setFormatter(file_formatter)

    # Add file handler object to the logger
    app.logger.addHandler(file_handler)
