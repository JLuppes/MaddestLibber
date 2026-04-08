from models import db, Blank, Response, ResponseSet, Story, Story_Blank, Story_Tag, Tag
from app import app


def seed_data():
    blanks = []
    responses = []
    responseSets = []
    stories = [
        Story(
            id=64001,
            name="A Walk Through Town",
            description="Try to get through town without everything getting silly.",
            text = """Once upon a ~+1+~, I was ~+2+~ through town, when I saw a ~+3+~. I thought, "~+4+~! I never noticed that ~+5+~ over there! I should probably ~+6+~ it."

Needless to say, I quickly ~+7+~ed my way out of there, and went over to ~+8+~. That's the last time I ~+9+~ a ~+10+~ in this town!"""
        )
    ]
    story_blanks = []
    story_tags = []
    tags = []
    db.session.add_all(blanks, responses, responseSets, stories, story_blanks, story_tags, tags)
    db.session.commit()

with app.app_context():
    seed_data()
