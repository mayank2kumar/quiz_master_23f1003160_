from flask_sqlalchemy import SQLAlchemy
from app import app


db = SQLAlchemy(app)
## models

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(32), unique=True, nullable=False)
    username = db.Column(db.String(32), unique=True, nullable=False)
    passhash = db.Column(db.String(512), nullable=False)
    fullname = db.Column(db.String(80), nullable=True)
    qualification = db.Column(db.String(80), nullable=False)
    DOB = db.Column(db.String(80), nullable=False)

    def __init__(self, email, username, passhash, fullname, qualification, DOB):
        self.email = email
        self.username = email
        self.passhash = passhash
        self.fullname = fullname
        self.qualification = qualification
        self.DOB = DOB

class subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject_name = db.Column(db.String(32), unique=True, nullable=False)
    subject_code = db.Column(db.String(32), unique=True, nullable=False)
    subject_description = db.Column(db.String(512), nullable=True)
    subject_credit = db.Column(db.String(80), nullable=False)

class chapter(db.Model):
    __tablename__ = 'chapter'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chapter_name = db.Column(db.String(32), unique=True, nullable=False)
    chapter_description = db.Column(db.String(512), nullable=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))

    ## relationships
    subject = db.relationship('subject', backref='chapter')
    # if we subject.chapter, we get all chapter in that subject
    # if we chapter.subject, we get the subject of that chapter
    # lazy is true, so it will only load when called not automatically

class quiz(db.Model):
    __tablename__ = 'quiz'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quiz_name = db.Column(db.String(32), unique=True, nullable=True)
    quiz_description = db.Column(db.String(512), nullable=True)
    date_of_quiz = db.Column(db.Date, nullable=False)
    time_duration = db.Column(db.Time, nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'))

    ## relationships
    chapter = db.relationship('chapter', backref='quiz')
    # if we chapter.quiz, we get all quiz in that chapter
    # if we quiz.chapter, we get the chapter of that quiz
    # lazy is true, so it will only load when called not automatically


class question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.String(512), nullable=False)
    option1 = db.Column(db.String(512), nullable=False)
    option2 = db.Column(db.String(512), nullable=False)
    option3 = db.Column(db.String(512), nullable=False)
    option4 = db.Column(db.String(512), nullable=False)
    answer = db.Column(db.String(512), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))

    ## relationships
    quiz = db.relationship('quiz', backref='question')
    # if we quiz.question, we get all question in that quiz
    # if we question.quiz, we get the quiz of that question

class score(db.Model):
    __tablename__ = 'score'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    total_score = db.Column(db.Integer, nullable=False)
    time_taken = db.Column(db.Time, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))

    ## relationships
    user = db.relationship('user', backref='score')
    # if we user.score, we get all score of that user
    # if we score.user, we get the user of that score

    quiz = db.relationship('quiz', backref='score')
    # if we quiz.score, we get all score of that quiz
    # if we score.quiz, we get the quiz of that score