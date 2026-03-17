from flask import Flask
from config import Config
from models import db, Tag, Story_Tag, Story, Story_Blank, Response, ResponseSet, Blank
from blueprints.main import main_controller
from blueprints.create import create_controller
from blueprints.play import play_controller
from dotenv import load_dotenv
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

app.secret_key = app.config['SECRET_KEY']

admin = Admin(app, name='MaddestLibber Admin')

# Initializes the app
db.init_app(app)

with app.app_context():
    db.create_all()
    print("Database created at:", app.config['SQLALCHEMY_DATABASE_URI'])

app.register_blueprint(main_controller.main)
app.register_blueprint(create_controller.create)
app.register_blueprint(play_controller.play)

admin.add_view(ModelView(Tag, db.session))
admin.add_view(ModelView(Story_Tag, db.session))
admin.add_view(ModelView(Story, db.session))
admin.add_view(ModelView(Story_Blank, db.session))
admin.add_view(ModelView(Response, db.session))
admin.add_view(ModelView(ResponseSet, db.session))
admin.add_view(ModelView(Blank, db.session))

if __name__ == '__main__':
    app.run(debug=True)
