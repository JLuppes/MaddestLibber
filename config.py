import os
basedir = os.path.abspath(os.path.dirname(__file__))

imported_dbname = os.getenv('DB_NAME', 'app')
formed_dbname = imported_dbname if imported_dbname.endswith('.db') else imported_dbname + '.db'

class Config:
    DB_NAME = formed_dbname
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, formed_dbname)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    HOST_ADDR = os.getenv('HOST_ADDR', '0.0.0.0')
    HOST_PORT = os.getenv('HOST_PORT', 5000)