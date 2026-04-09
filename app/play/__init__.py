#This bluepint will deal with play functionality

from flask import Blueprint

play_blueprint = Blueprint('play', __name__, template_folder='templates')

from . import views