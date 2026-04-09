from flask import render_template
from . import auth_blueprint


@auth_blueprint.route('/')
def auth():
    return render_template('auth/auth.html')
