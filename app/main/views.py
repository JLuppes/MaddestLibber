from flask import render_template, current_app
from . import main_blueprint


@main_blueprint.route('/')
def home():
    current_app.logger.info("Index page loading")
    return render_template('main/index.html')
