#This bluepint will deal with main site navigation

from flask import Blueprint

main_blueprint = Blueprint('main', __name__, template_folder='templates')

from . import views