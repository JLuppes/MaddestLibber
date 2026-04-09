from app.models import Response, ResponseSet, Story, Story_Tag, Tag
from app import app, db


def seed_data():
    responses = [
        Response(
            id=68001,
            responseset_id=67001,
            text="dog",
            named=False,
            prompt="noun",
            hint="",
            pos=0
        ),
        Response(
            id=68002,
            responseset_id=67001,
            text="eating",
            named=False,
            prompt="verb",
            hint="ending with ing",
            pos=1
        ),
        Response(
            id=68003,
            responseset_id=67001,
            text="banana",
            named=True,
            prompt="noun",
            hint="",
            pos=2
        ),
        Response(
            id=68004,
            responseset_id=67001,
            text="jeepers",
            named=False,
            prompt="exclamation",
            hint="",
            pos=3
        ),
        Response(
            id=68005,
            responseset_id=67001,
            text="scoop",
            named=False,
            prompt="verb",
            hint="",
            pos=4
        ),
        Response(
            id=68006,
            responseset_id=67001,
            text="wash",
            named=False,
            prompt="verb",
            hint="",
            pos=5
        ),
        Response(
            id=68007,
            responseset_id=67001,
            text="under the mailbox",
            named=False,
            prompt="place",
            hint="",
            pos=6
        ),
        Response(
            id=68008,
            responseset_id=67001,
            text="zoom",
            named=False,
            prompt="verb",
            hint="",
            pos=7
        ),
        Response(
            id=68009,
            responseset_id=67001,
            text="holofoil charizard card",
            named=False,
            prompt="noun",
            hint="",
            pos=8
        ),
    ]
    responseSets = [
        ResponseSet(
            id=67001,
            story_id=64001,
            user="A Funny User",
            title="Once Upon a Town",
            description="Just adding some funny stuff to this story"
        )
    ]
    stories = [
        Story(
            id=64001,
            name="A Walk Through Town",
            description="Try to get through town without everything getting silly.",
            text="""Once upon a ~[noun]~, I was ~[verb | ending with "ing"]~ through town, when I saw a ~[*noun]~. I thought, "~[exclamation]~! I never noticed that ~[*noun]~ over there! I should probably ~[verb]~ it."

Needless to say, I quickly ~[verb]~ed my way out of there, and went over to ~[place]~. That's the last time I ~[verb]~ a ~[noun]~ in this town!"""
        )
    ]
    story_tags = [
        Story_Tag(
            id=66001,
            tag_id=65001,
            story_id=64001
        )
    ]
    tags = [
        Tag(
            id=65001,
            name="Funny",
            description="A story that is funny"
        ),
        Tag(
            id=65002,
            name="Scary",
            description="A scary story"
        ),

    ]
    db.session.add_all(responses)
    db.session.add_all(responseSets)
    db.session.add_all(stories)
    db.session.add_all(story_tags)
    db.session.add_all(tags)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        all_stories_count = Story.query.all().count
        if all_stories_count == 0:
            seed_data()
        else: print("Database already has data!")
