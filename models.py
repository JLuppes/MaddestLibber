from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# class Review(db.Model):
#     """Review model."""
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100))
#     director = db.Column(db.String(100))
#     review = db.Column(db.Text)
#     user = db.Column(db.String(100))
#     movie_id = db.Column(db.Integer, db.ForeignKey('movie_data.id'), nullable=False)
#     __tablename__ = "review"


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


class Completed_Answer(db.Model):
    """Completed Story to Answer relationship model."""
    id = db.Column(db.Integer, primary_key=True)
    completedstory_id = db.Column(db.Integer, db.ForeignKey(
        'completedstory.id'), nullable=False)
    answer_id = db.Column(db.Integer, db.ForeignKey(
        'answer.id'), nullable=False)
    rank = db.Column(db.Integer)
    __tablename__ = "completed_answer"


class RequestSet(db.Model):
    """Request Set model."""
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'), nullable=False)
    description = db.Column(db.String(1000))

    answers = db.relationship("Answer", backref="requestset", lazy=True)
    requestset_blanks = db.relationship(
        "RequestSet_Blank", backref="requestset", lazy=True)
    __tablename__ = "requestset"


class Story(db.Model):
    """Story model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    text = db.Column(db.String(10000))

    story_tags = db.relationship("Story_Tag", backref="story", lazy=True)
    completedstories = db.relationship(
        "CompletedStory", backref="story", lazy=True)
    __tablename__ = "story"


class CompletedStory(db.Model):
    """Completed Story model."""
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'), nullable=False)

    completedanswers = db.relationship(
        "Completed_Answer", backref="completedstory", lazy=True)
    __tablename__ = "completedstory"


class Answer(db.Model):
    """Answer model."""
    id = db.Column(db.Integer, primary_key=True)
    requestset_id = db.Column(db.Integer, db.ForeignKey(
        'requestset.id'), nullable=False)
    blanktype_id = db.Column(db.Integer, db.ForeignKey(
        'blanktype.id'), nullable=False)
    text = db.Column(db.String(100))

    completedanswers = db.relationship(
        "Completed_Answer", backref="answer", lazy=True)
    __tablename__ = "answer"


class RequestSet_Blank(db.Model):
    """Request Set to Blank relationship model."""
    id = db.Column(db.Integer, primary_key=True)
    requestset_id = db.Column(db.Integer, db.ForeignKey(
        'requestset.id'), nullable=False)
    blanktype_id = db.Column(db.Integer, db.ForeignKey(
        'blanktype.id'), nullable=False)

    __tablename__ = "request_blank"


class BlankType(db.Model):
    """Blank Type model."""
    id = db.Column(db.Integer, primary_key=True)
    blanktype_id = db.Column(db.Integer, db.ForeignKey(
        'blanktype.id'), nullable=False)
    partofspeech = db.Column(db.String(100))
    tense = db.Column(db.String(100))
    description = db.Column(db.String(1000))

    answers = db.relationship("Answer", backref="blanktype", lazy=True)
    requestset_blanks = db.relationship(
        "RequestSet_Blank", backref="blanktype", lazy=True)
    __tablename__ = "blanktype"
