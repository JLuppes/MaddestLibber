from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Tag
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


create = Blueprint('create', __name__, url_prefix='/create',
                   template_folder='./templates')


@create.route('/')
def home():
    return render_template('create_home.html')


class NewTagForm(FlaskForm):
    name = StringField('Tag Name', validators=[DataRequired()])
    description = StringField('Tag Description', validators=[DataRequired()])


@create.route('/tag', methods=['GET', 'POST'])
def newTag():

    newTagForm = NewTagForm()

    if newTagForm.validate_on_submit():

        try:
            new_tag = Tag(
                name=request.form.get('name'),
                description=request.form.get('description')
            )
            db.session.add(new_tag)
            db.session.commit()

            flash("Tag Created!", "success")

            return redirect(url_for('main.home'))

        except ValueError as e:
            error = "Error with new tag form!"
            return render_template('create_tag.html', newTagForm=newTagForm, error=error)
    elif newTagForm.is_submitted():
        error = "Form Validation Failed!"
        return render_template('create_tag.html', newTagForm=newTagForm, error=error)

    return render_template('create_tag.html', newTagForm=newTagForm)
