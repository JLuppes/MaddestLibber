#This bluepint will deal with create functionality

from flask import Blueprint

create_blueprint = Blueprint('create', __name__, template_folder='templates')

from . import views