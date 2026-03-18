from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Story, Blank, Story_Blank, Tag, Story_Tag, ResponseSet, Response
import random

play = Blueprint('play', __name__, url_prefix='/play',
                 template_folder='./templates')


@play.route('/')
def home():
    return render_template('play_home.html')


@play.route('/respond', methods=['GET', 'POST'])
def respond(storyId=''):

    storyId = int(request.args.get('storyId', 28))

    story = Story.query.filter_by(id=storyId).first()
    story_name = story.name
    story_description = story.description
    requestSet = Story_Blank.query.filter_by(story_id=storyId).all()
    blanks = []
    for thisRequest in requestSet:
        thisBlank = Blank.query.filter_by(id=thisRequest.blank_id).first()
        blanks.append(thisBlank)

    if requestSet is None:
        return redirect(url_for('play.home'), error="No requests found for that story!")

    resonseSetId = 1

    if request.method == 'POST':
        return redirect(url_for('play.finishedStory', storyId=story.id, responseSetId=resonseSetId))

    return render_template('respond.html', storyName=story_name, storyDescription=story_description, requestSet=requestSet, enumerate=enumerate, blanks=blanks)


@play.route('/list')
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

    return render_template('list_stories.html', stories=story_list)


def getRandomStory():
    rowCount = int(Story.query.count())
    randomStory = Story.query.offset(int(rowCount*random.random())).first()
    return randomStory


@play.route('/random')
def randomStory():
    thisStory = getRandomStory()
    return redirect(url_for('play.respond', storyId=thisStory.id))


@play.route('/read')
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

    allStoryBlanks = Story_Blank.query.filter_by().all()
    allBlanks = Blank.query.all()

    responseSetBlankInfo = []
    for response in responses:
        story_blank = Story_Blank.query.filter_by(
            id=response.story_blank_id).first()
        blank = Blank.query.filter_by(id=story_blank.blank_id).first()
        blank_name = blank.name
        blank_hint = blank.hint
        responseSetBlankInfo.append(
            {
                "story_blank_id": response.story_blank_id,
                "blank_name": blank_name,
                "blank_hint": blank_hint
            }
        )

    return render_template('finishedStory.html', story=story, responseSet=responseSet, responses=responses, allStoryBlanks=allStoryBlanks, allBlanks=allBlanks, responseSetBlankInfo=responseSetBlankInfo)


@play.route('/responses')
def listResponses():

    storyList = Story.query.all()
    responseSetList = ResponseSet.query.all()

    return render_template('list_responses.html', storyList=storyList, responseSetList=responseSetList)


def getRandomResponse():
    rowCount = int(ResponseSet.query.count())
    randomResponseSet = ResponseSet.query.offset(
        int(rowCount*random.random())).first()
    return randomResponseSet


@play.route('/read/random')
def readRandomResponse():
    thisResponseSet = getRandomResponse()

    return redirect(url_for('play.finishedStory', storyId=thisResponseSet.story_id, responseSetId=thisResponseSet.id))
