from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Tag, Story, Story_Tag
from blueprints.create.create_forms import NewStoryForm, NewTagForm

create = Blueprint('create', __name__, url_prefix='/create',
                   template_folder='./templates')


@create.route('/')
def home():
    return render_template('create_home.html')


def makeNewStory(storyName='', storyDescription='', storyText=''):
    try:
        new_story = Story(
            name=storyName,
            description=storyDescription,
            text=storyText
        )
        db.session.add(new_story)
        db.session.commit()
        return new_story
    except ValueError as e:
        db.session.rollback()
        error = f"Error adding story to database: {e}"
        raise ValueError(error)


def makeNewTag(tag_name='', tag_description=''):
    try:
        new_tag = Tag(
            name=tag_name,
            description=tag_description
        )
        db.session.add(new_tag)
        db.session.commit()
        return new_tag
    except Exception as e:
        db.session.rollback()
        error = f"Error adding tag: {e}"
        raise ValueError(error)


def makeStoryTagConnection(story, tag):
    try:
        new_story_tag = Story_Tag(
            tag_id=tag.id,
            story_id=story.id
        )
        thisTag = Tag.query.filter_by(id=tag.id).first()
        thisStory = Tag.query.filter_by(id=story.id).first()
        db.session.add(new_story_tag)
        db.session.commit()
        flash(
            f"Added tag {thisTag.name} to story {thisStory.name}!", 'success')
    except ValueError as e:
        error = "Error adding story-tag connection: " + e
        raise ValueError(error)


@create.route('/story', methods=['GET', 'POST'])
def newStory():
    newStoryForm = NewStoryForm()
    newTagForm = NewTagForm
    tags = Tag.query.all()

    if newStoryForm.validate_on_submit():
        try:
            new_story = makeNewStory(
                newStoryForm.name.data, newStoryForm.description.data, newStoryForm.text.data)
        except Exception as e:
            error = f"Error adding new story after validation: {e}"
            flash(error, 'error')

        list_of_tags = newStoryForm.tagList.data.split(',')
        for thisTag in list_of_tags:
            if len(thisTag) > 0:
                try:
                    addingTag = db.session.query(Tag).filter_by(id=thisTag).first()
                    makeStoryTagConnection(new_story, addingTag)
                except Exception as e:
                    error = f"Error adding story connection for tag {thisTag}: {e}"
                    flash(error, 'error')
                    
        flash("Story added!", 'success')

        return redirect(url_for('play.home'))
    else:
        return render_template('create_story.html', newStoryForm=newStoryForm, newTagForm=newTagForm, tags=tags)


@create.route('/tag', methods=['GET', 'POST'])
def newTag():
    newTagForm = NewTagForm()
    if newTagForm.validate_on_submit():
        try:
            makeNewTag(
                tag_name=request.form.get('name'),
                tag_description=request.form.get('description'))
            flash("Tag Created!", "success")
            return redirect(url_for('create.newTag', newTagForm=newTagForm))
        except ValueError as e:
            error = "Error with new tag form!"
            return render_template('create_tag.html', newTagForm=newTagForm, error=error)
    elif newTagForm.is_submitted():
        error = "Form Validation Failed!"
        return render_template('create_tag.html', newTagForm=newTagForm, error=error)
    return render_template('create_tag.html', newTagForm=newTagForm)
