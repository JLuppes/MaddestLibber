from flask import Blueprint, render_template, request, redirect, url_for
create = Blueprint('create', __name__, url_prefix='/create', template_folder='./templates')

@create.route('/')
def home():
    return render_template('create_home.html')
