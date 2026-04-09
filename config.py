#!/usr/bin/env python

import os
from dotenv import load_dotenv

load_dotenv()

# Get the base directory for the application
basedir = os.path.abspath(os.path.dirname(__file__))

# Pull the db name from the .env file if specified
imported_dbname = os.environ.get('DB_NAME', 'app2')

# Add the filetype extension to the database name
formed_dbname = imported_dbname if imported_dbname.endswith(
    '.db') else imported_dbname + '.db'

# Build the full URI for the database file
db_uri = 'sqlite:///' + os.path.join(basedir, formed_dbname)

# Tell SQLAlchemy to track modifications
track_modifications = os.environ.get('DB_TRACK_MODIFICATIONS', False) == "True"

# Pull in the Secret Key from the .env file
secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')

# Provide host address and port
host_addr = os.environ.get('HOST_ADDR', '0.0.0.0')
host_port = os.environ.get('HOST_PORT', 5000)


class Config(object):
    """
    Base configuration class. Contains default configuration settings + configuration settings applicable to all environments.
    """
    DB_NAME = formed_dbname
    SQLALCHEMY_DATABASE_URI = db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = track_modifications
    SECRET_KEY = secret_key
    HOST_ADDR = host_addr
    FLASK_RUN_PORT = host_port
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
    RESULT_BACKEND = os.getenv('RESULT_BACKEND')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, 'dev.db')

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    MAIL_SUPPRESS_SEND = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, 'test.db')

class ProductionConfig(Config):
    FLASK_ENV = 'production'
    # Postgres database URL has the form postgresql://username:password@hostname/database
    SQLALCHEMY_DATABASE_URI = os.getenv('PROD_DATABASE_URl', default="sqlite:///" + os.path.join(basedir, 'prod.db'))
