from flask import Blueprint, render_template, request, redirect, url_for
play = Blueprint('play', __name__, url_prefix='/play', template_folder='./templates')

@play.route('/')
def home():
    return render_template('play_home.html')
