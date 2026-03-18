from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Tag(db.Model):
    """Tag model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(1000))

    story_tags = db.relationship("Story_Tag", backref="tag", lazy=True)
    __tablename__ = "tag"


class Story_Tag(db.Model):
    """Story to Tag relationship model."""
    id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), nullable=False)
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'), nullable=False)

    __tablename__ = "story_tag"


class Story(db.Model):
    """Story model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    text = db.Column(db.String(10000))

    story_tags = db.relationship("Story_Tag", backref="story", lazy=True)
    story_blanks = db.relationship("Story_Blank", backref="story", lazy=True)
    responsesets = db.relationship("ResponseSet", backref="story", lazy=True)
    __tablename__ = "story"


class Story_Blank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'), nullable=False)
    blank_id = db.Column(db.Integer, db.ForeignKey('blank.id'), nullable=False)
    position = db.Column(db.Integer)

    responses = db.relationship("Response", backref="story_blank", lazy=True)
    __tablename__ = "story_blank"


class Response (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story_blank_id = db.Column(db.Integer, db.ForeignKey(
        'story_blank.id'), nullable=False)
    responseset_id = db.Column(db.Integer, db.ForeignKey(
        'responseset.id'), nullable=False)
    text = db.Column(db.String(1000))
    __tablename__ = "response"


class ResponseSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'), nullable=False)
    user = db.Column(db.String(1000))
    title = db.Column(db.String(1000))
    description = db.Column(db.String(1000))

    responses = db.relationship("Response", backref="responseset", lazy=True)
    __tablename__ = "responseset"


class Blank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    hint = db.Column(db.String(1000))

    story_blanks = db.relationship("Story_Blank", backref="blank", lazy=True)
    __tablename__ = "blank"
