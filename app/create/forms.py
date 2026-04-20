
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, HiddenField, BooleanField
from wtforms.validators import DataRequired


class NewStoryForm(FlaskForm):
    name = StringField('Story Name', validators=[DataRequired()])
    description = StringField('Story Description')
    text = TextAreaField('Story Text', validators=[DataRequired()])
    tagList = HiddenField("Tags")


class NewBlankForm(FlaskForm):
    prompt = StringField('Prompt', validators=[DataRequired()])
    hint = StringField('Hint')
    named = BooleanField('Named Blank?')


class NewTagForm(FlaskForm):
    name = StringField('Tag Name', validators=[DataRequired()])
    description = StringField("Tag Description")
