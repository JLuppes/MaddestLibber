
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, HiddenField
from wtforms.validators import DataRequired


class NewStoryForm(FlaskForm):
    name = StringField('Story Name', validators=[DataRequired()])
    description = StringField('Story Description')
    text = TextAreaField('Story Text', validators=[DataRequired()])
    tags = HiddenField("Tags")


class NewTagForm(FlaskForm):
    name = StringField('Tag Name', validators=[DataRequired()])
    description = StringField("Tag Description")
