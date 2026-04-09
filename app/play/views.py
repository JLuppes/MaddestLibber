from flask import render_template, request, redirect, url_for, flash
from app.models import db, Story, Tag, Story_Tag, ResponseSet, Response
import random

from . import play_blueprint


blank_start = '~['
blank_end = ']~'
named_blank_tag = '*'
sep_char = '|'
replaced_start = '~+'
replaced_end = '+~'


@play_blueprint.route('/')
def home():
    return render_template('play/play_home.html')


def getBlanks(text):
    blanks = []
    start = 0
    blank_pos = 0
    while True:
        start = text.find(blank_start, start)
        end = text.find(blank_end, start)
        if start == -1:
            break
        blank_text = text[(start+len(blank_start)):end]
        sep_pos = blank_text.find(sep_char)
        blank_prompt = blank_text[:sep_pos].strip(
        ) if sep_pos > -1 else blank_text[:end].strip()
        blank_named = blank_prompt.startswith(named_blank_tag)
        blank_prompt = blank_prompt.removeprefix(named_blank_tag)
        blank_hint = blank_text[sep_pos +
                                len(sep_char):].strip() if sep_pos > -1 else ''

        previously_named = False
        if blank_named:
            for blank in blanks:
                if blank[2] and blank[0] == blank_prompt:
                    previously_named = True
        if not blank_named or (blank_named and not previously_named):
            blanks.append((blank_prompt, blank_hint, blank_named, blank_pos))
        start += len(blank_start+blank_end+blank_text)
        blank_pos += 1
    return blanks


@play_blueprint.route('/respond', methods=['GET', 'POST'])
def respond(storyId=''):

    storyId = int(request.args.get('storyId'))

    story = Story.query.filter_by(id=storyId).first()

    if story is None:
        error = "No story id provided or story not found!"
        flash(error, 'error')
        return redirect(url_for('play.listStories'))

    story_name = story.name
    story_description = story.description

    if request.method == 'POST':
        story_id = request.form.get('story_id')
        user = request.form.get('userName', 'Anonymous')
        title = request.form.get('responseTitle', 'Untitled')
        description = request.form.get('responseDescription', 'No description')

        try:
            new_response_set = ResponseSet(
                story_id=story_id,
                user=user,
                title=title,
                description=description
            )
            db.session.add(new_response_set)
            db.session.commit()
            flash("Response added successfully!", 'success')
        except ValueError as e:
            db.session.rollback()
            error = "Error adding response set: " + e
            flash(error, 'error')

        responses = request.form.getlist('response')
        response_prompts = request.form.getlist('response-prompt')
        response_hints = request.form.getlist('response-hint')
        response_nameds = request.form.getlist('response-named')

        response_pos = 0
        for i, response in enumerate(responses):
            try:
                newResponse = Response(
                    responseset_id=new_response_set.id,
                    text=response,
                    named=response_nameds[i] == 'True',
                    prompt=response_prompts[i],
                    hint=response_hints[i],
                    pos=response_pos
                )
                db.session.add(newResponse)
                db.session.commit()
                response_pos += 1
            except ValueError as e:
                db.session.rollback()
                error = "Error adding response: " + e
                flash(error, 'error')

        return redirect(url_for('play.finishedStory', storyId=story_id, responseSetId=new_response_set.id))

    blanks = getBlanks(story.text)

    return render_template('play/respond.html', storyName=story_name, storyDescription=story_description, storyId=story.id, enumerate=enumerate, blanks=blanks)


@play_blueprint.route('/list')
def listStories():

    stories = Story.query.all()

    story_list = []

    for thisStory in stories:

        this_story_tags = Story_Tag.query.filter_by(
            story_id=thisStory.id).all()
        tagList = []
        for thisStoryTag in this_story_tags:
            thisTag = Tag.query.filter_by(id=thisStoryTag.tag_id).first()
            tagList.append(thisTag)

        story_list.append((thisStory, tagList))

    return render_template('play/list_stories.html', stories=story_list)


def getRandomStory():
    rowCount = int(Story.query.count())
    randomStory = Story.query.offset(int(rowCount*random.random())).first()
    return randomStory


@play_blueprint.route('/random')
def randomStory():
    return redirect(url_for('play.respond', storyId=getRandomStory().id))


@play_blueprint.route('/read')
def finishedStory():

    storyId = request.args.get('storyId', default=-1, type=int)
    responseSetId = request.args.get('responseSetId', default=-1, type=int)

    if storyId == -1 or responseSetId == -1:
        error = "No story or response set indicated!"
        flash(error, 'error')
        return redirect(url_for('play.home'))

    story = Story.query.filter_by(id=storyId).first()
    responseSet = ResponseSet.query.filter_by(id=responseSetId).first()
    responses = Response.query.filter_by(responseset_id=responseSetId).all()

    responseSetBlankInfo = []
    for response in responses:
        responseSetBlankInfo.append(
            {
                "blank_text": response.text,
                "blank_name": response.prompt,
                "blank_hint": response.hint,
                "blank_named": response.named,
                "blank_pos": response.pos
            }
        )

    return render_template('play/finishedStory.html', story=story, responseSet=responseSet, responses=responses, responseSetBlankInfo=responseSetBlankInfo)


@play_blueprint.route('/responses')
def listResponses():

    storyList = Story.query.all()
    responseSetList = ResponseSet.query.all()

    return render_template('play/list_responses.html', storyList=storyList, responseSetList=responseSetList)


def getRandomResponse():
    rowCount = int(ResponseSet.query.count())
    randomResponseSet = ResponseSet.query.offset(
        int(rowCount*random.random())).first()
    return randomResponseSet


@play_blueprint.route('/read/random')
def readRandomResponse():
    thisResponseSet = getRandomResponse()

    return redirect(url_for('play.finishedStory', storyId=thisResponseSet.story_id, responseSetId=thisResponseSet.id))
