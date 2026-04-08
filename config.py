import os

# Get the base directory for the application
basedir = os.path.abspath(os.path.dirname(__file__))

# Pull the db name from the .env file if specified
imported_dbname = os.getenv('DB_NAME', 'app')

# Add the filetype extension to the database name
formed_dbname = imported_dbname if imported_dbname.endswith(
    '.db') else imported_dbname + '.db'

# Build the full URI for the database file
db_uri = 'sqlite:///' + os.path.join(basedir, formed_dbname)

# Tell SQLAlchemy to track modifications
track_modifications = os.getenv('DB_TRACK_MODIFICATIONS', False) == "True"

# Pull in the Secret Key from the .env file
secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

# Provide host address and port
host_addr = os.getenv('HOST_ADDR', '0.0.0.0')
host_port = os.getenv('HOST_PORT', 5000)


class Config:
    DB_NAME = formed_dbname
    SQLALCHEMY_DATABASE_URI = db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = track_modifications
    SECRET_KEY = secret_key
    HOST_ADDR = host_addr
    HOST_PORT = host_port
