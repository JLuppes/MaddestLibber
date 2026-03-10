from flask import Flask
from config import Config
from models import db
from blueprints.main import main_controller
from dotenv import load_dotenv
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

app.secret_key = app.config['SECRET_KEY']

admin = Admin(app, name='maddestlibber')

# Initializes the app
db.init_app(app)

with app.app_context():
    db.create_all()
    print("Database created at:", app.config['SQLALCHEMY_DATABASE_URI'])

app.register_blueprint(main_controller.main)

if __name__ == '__main__':
    app.run(debug=True)
