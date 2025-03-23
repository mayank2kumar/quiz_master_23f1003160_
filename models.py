from flask_sqlalchemy import SQLAlchemy
from app import app
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy(app)
## models

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(32), unique=True, nullable=False)
    username = db.Column(db.String(32), unique=True, nullable=False)
    passhash = db.Column(db.String(512), nullable=False)
    fullname = db.Column(db.String(80), nullable=False)
    qualification = db.Column(db.String(80), nullable=True)
    DOB = db.Column(db.String(80), nullable=True)
    is_admin = db.Column(db.Boolean, default=False, nullable=True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    # so when someone tries to get the password it will raise this error.

    def __init__(self, email, username, password, fullname, qualification, DOB,is_admin):
        self.email = email
        self.username = username
        self.passhash = generate_password_hash(password)
        self.fullname = fullname
        self.qualification = qualification
        self.DOB = DOB
        self.is_admin = is_admin
    def check_password(self, password):
        return check_password_hash(self.passhash, password)  
              

class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject_name = db.Column(db.String(32), unique=True, nullable=False)
    subject_code = db.Column(db.String(32), unique=True, nullable=False)
    subject_description = db.Column(db.String(512), nullable=True)
    subject_credit = db.Column(db.String(80), nullable=False)

class Chapter(db.Model):
    __tablename__ = 'chapter'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chapter_name = db.Column(db.String(32), unique=True, nullable=False)
    chapter_description = db.Column(db.String(512), nullable=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))

    ## relationships
    subject = db.relationship('Subject', backref=db.backref('chapters', lazy=True))
    # if we subject.chapter, we get all chapter in that subject
    # if we chapter.subject, we get the subject of that chapter
    # lazy is true, so it will only load when called not automatically

class Quiz(db.Model):
    __tablename__ = 'quiz'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quiz_name = db.Column(db.String(32), unique=False, nullable=True)
    quiz_description = db.Column(db.String(512), nullable=True)
    time_duration = db.Column(db.String(5), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'))

    ## relationships
    chapter = db.relationship('Chapter',  backref='quiz', lazy=True)
    
    # if we chapter.quiz, we get all quiz in that chapter
    # if we quiz.chapter, we get the chapter of that quiz
    # lazy is true, so it will only load when called not automatically


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_text = db.Column(db.String(512), nullable=False)
    option1 = db.Column(db.String(512), nullable=False)
    option2 = db.Column(db.String(512), nullable=False)
    option3 = db.Column(db.String(512), nullable=False)
    option4 = db.Column(db.String(512), nullable=False)
    answer = db.Column(db.String(512), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'),nullable=False)
    question_title = db.Column(db.String(512), nullable=False)
    ## relationships
    quiz = db.relationship('Quiz', backref='questions', lazy=True)
    # if we quiz.question, we get all question in that quiz
    # if we question.quiz, we get the quiz of that question

class Score(db.Model):
    __tablename__ = 'score'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    total_score = db.Column(db.Integer, nullable=False)
    time_taken = db.Column(db.Time, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))

    ## relationships
    # user = db.relationship('User', db.backref('scores', lazy=True))
    # if we user.score, we get all score of that user
    # if we score.user, we get the user of that score

    # quiz = db.relationship('Quiz', db.backref('scores', lazy=True))
    # if we quiz.score, we get all score of that quiz
    # if we score.quiz, we get the quiz of that score


# creeate database if not exists
with app.app_context():
    db.create_all()
    # create admin user if not exists
    if not User.query.filter_by(is_admin=True).first():
        admin = User(username='admin',password='admin',is_admin=True,DOB='',qualification='',fullname='',email='')
        db.session.add(admin)
        db.session.commit()
        # create a default admin user if not exists
        # this is a default admin user with username and password as admin
        # it will be created at start of app when database is created
        # so no one else will be able to create admin user as it is already created