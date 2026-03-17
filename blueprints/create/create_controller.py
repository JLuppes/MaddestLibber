from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Tag, Story, Story_Tag, Story_Blank, Blank
from blueprints.create.create_forms import NewStoryForm, NewTagForm

create = Blueprint('create', __name__, url_prefix='/create',
                   template_folder='./templates')

blank_start = '~['
blank_end = ']~'
sep_char = '|'
replaced_start = '~+'
replaced_end = '+~'


@create.route('/')
def home():
    return render_template('create_home.html')


def makeNewStory(storyName='', storyDescription='', storyText=''):

    blanks = []

    start = 0
    while True:
        start = storyText.find(blank_start, start)
        end = storyText.find(blank_end, start)
        if start == -1:
            break
        blank_text = storyText[(start+len(blank_start)):end]
        sep_pos = blank_text.find(sep_char, start, end)
        blank_name = blank_text[:sep_pos].strip(
        ) if sep_pos > -1 else blank_text[:end].strip()
        blank_desc = blank_text[sep_pos +
                                len(sep_char):].strip() if sep_pos > -1 else ''
        blanks.append((blank_name, blank_desc))
        start += len(blank_start+blank_end+blank_text)

    try:
        new_story = Story(
            name=storyName,
            description=storyDescription,
            text=storyText
        )
        db.session.add(new_story)
        db.session.commit()
    except ValueError as e:
        db.session.rollback()
        error = f"Error adding story to database: {e}"
        raise ValueError(error)

    pos_counter = 0
    newStoryText = storyText
    for this_blank in blanks:
        try:
            new_blank = Blank(
                name=this_blank[0],
                hint=this_blank[1]
            )
            db.session.add(new_blank)
            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            error = "Error adding new blank: " + e
            flash(error, 'error')
        try:
            new_story_blank = Story_Blank(
                story_id=new_story.id,
                blank_id=new_blank.id,
                position=pos_counter
            )
            db.session.add(new_story_blank)
            db.session.commit()
            pos_counter += 1
        except ValueError as e:
            db.session.rollback()
            error = "Error during story-blank connection: " + e
            raise ValueError(error)
        # Replace blanks in story with story_blank id
        start = newStoryText.find(blank_start)
        end = newStoryText.find(blank_end)

        replacement = replaced_start + str(new_story_blank.id) + replaced_end
        newStoryText = newStoryText[:start] + \
            replacement + newStoryText[end+len(blank_end):]

    # Replace existing story text with our updated version
    try:
        new_story.text = newStoryText
        db.session.commit()
    except ValueError as e:
        error = "Error replacing story text: " + e
        flash(error, 'error')

    return new_story


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
    newTagForm = NewTagForm()
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
                    addingTag = db.session.query(
                        Tag).filter_by(id=thisTag).first()
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
