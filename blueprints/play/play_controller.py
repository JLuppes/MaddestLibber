from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Story, Blank, Story_Blank, Tag, Story_Tag
from sqlalchemy.orm import load_only
from sqlalchemy.sql import func
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

    if request.method == 'POST':
        pass

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
