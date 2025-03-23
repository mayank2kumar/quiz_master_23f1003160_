from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db,User,Subject,Chapter,Quiz,Question,Score
from functools import wraps
from app import app

def auth_required(func):
    @wraps(func)
    # works on the base of session cokkies 
    def inner(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to continue')
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return inner

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('is_admin') == False:
            flash("Access Denied: Admins Only", "danger")
            return redirect(url_for('index'))  # Redirect to home if not admin
        return f(*args, **kwargs)
    return decorated_function

def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('is_admin') == True:
            flash("Access Denied: Users Only", "danger")
            return redirect(url_for('index'))  # Redirect to home if not a regular user
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user_management')
@auth_required
@admin_required
def user_management():
    users = User.query.filter_by(is_admin=False).all()
    return render_template('user_management.html', users=users)

@app.route('/delete_user')
@auth_required
@admin_required
def delete_user():
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully')
    return redirect(url_for('user_management'))




@app.route('/edit_question')
@auth_required
@admin_required
def edit_question():
    question_id = request.args.get('question_id')
    question = Question.query.get(question_id)
    return render_template('edit_question.html', question=question)

@app.route('/edit_question', methods=['POST'])
@auth_required
@admin_required
def edit_question_post():
    question_id = request.args.get('question_id')
    question_text = request.form['question_text']
    option1 = request.form['option1']
    option2 = request.form['option2']
    option3 = request.form['option3']
    option4 = request.form['option4']
    answer = request.form['answer']
    question_title = request.form['question_title']
    question = Question.query.filter_by(question_text=question_text).first()
    question = Question.query.get(question_id)
    question.question_text = question_text
    question.option1 = option1
    question.option2 = option2
    question.option3 = option3
    question.option4 = option4
    question.answer = answer
    question.question_title = question_title

    db.session.commit()
    flash('Question updated successfully')
    return redirect(url_for('quiz'))






@app.route('/delete_question')
@auth_required
@admin_required
def delete_question():
    question_id = request.args.get('question_id')
    question = Question.query.get(question_id)
    db.session.delete(question)
    db.session.commit()
    flash('Question deleted successfully')
    return redirect(url_for('quiz'))



@app.route('/new_question')
@auth_required
@admin_required
def new_question():
    quiz_id = request.args.get('quiz_id')
    quiz = Quiz.query.get(quiz_id)
    return render_template('new_question.html', quiz=quiz)

@app.route('/new_question', methods=['POST'])
@auth_required
@admin_required
def new_question_post():
    question_text = request.form['question_text']
    option1 = request.form['option1']
    option2 = request.form['option2']
    option3 = request.form['option3']
    option4 = request.form['option4']
    answer = request.form['answer']
    quiz_id = request.form['quiz_id']
    question_title = request.form['question_title']
    question = Question(question_text=question_text, option1=option1, option2=option2, option3=option3, option4=option4, answer=answer, quiz_id=quiz_id, question_title=question_title)
    db.session.add(question)
    db.session.commit()
    flash('Question added successfully')
    return redirect(url_for('quiz'))



@app.route('/quiz')
@auth_required
@admin_required
def quiz():
    quizs = Quiz.query.all()
    return render_template('quiz.html', user=User.query.get(session['user_id']), quizs=quizs)

@app.route('/new_quiz')
@auth_required
@admin_required
def new_quiz():
    # chapter_id = request.args.get('chapter_id')
    # chapter = Chapter.query.get(chapter_id)
    chapters = Chapter.query.all()  
    return render_template('new_quiz.html', chapters=chapters)

@app.route('/new_quiz', methods=['POST'])
@auth_required
@admin_required
def new_quiz_post():
    quiz_name = request.form['quiz_name']
    quiz_description = request.form['quiz_description']
    chapter_id = request.form['chapter_id']
    time_duration = request.form['time_duration']
    quiz = Quiz(quiz_name=quiz_name, quiz_description=quiz_description, time_duration=time_duration, chapter_id=chapter_id)
    db.session.add(quiz)
    db.session.commit()
    flash('Quiz added successfully')
    return redirect(url_for('quiz'))

@app.route('/edit_quiz')
@auth_required
@admin_required
def edit_quiz():
    quiz_id = request.args.get('quiz_id')
    quiz = Quiz.query.get(quiz_id)
    chapters = Chapter.query.all()
    return render_template('edit_quiz.html', quiz=quiz, chapters=chapters)

@app.route('/edit_quiz', methods=['POST'])
@auth_required
@admin_required
def edit_quiz_post():
    quiz_id = request.args.get('quiz_id')
    quiz_name = request.form['quiz_name']
    quiz_description = request.form['quiz_description']
    # chapter_id = request.form['chapter_id']
    time_duration = request.form['time_duration']
    quiz = Quiz.query.filter_by(quiz_name=quiz_name).first()
    quiz = Quiz.query.get(quiz_id)
    quiz.quiz_name = quiz_name
    quiz.quiz_description = quiz_description
    # quiz.chapter_id = chapter_id
    quiz.time_duration = time_duration
    db.session.commit()
    flash('Quiz updated successfully')
    return redirect(url_for('quiz'))

@app.route('/delete_quiz')
@auth_required
@admin_required
def delete_quiz():
    quiz_id = request.args.get('quiz_id')
    quiz = Quiz.query.get(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    flash('Quiz deleted successfully')
    return redirect(url_for('quiz'))


@app.route('/admin_home')
@auth_required
@admin_required
def admin_home():
    subjects = Subject.query.all()
    return render_template('admin_home.html', user=User.query.get(session['user_id']), subjects=subjects)

@app.route('/new_chapter')
@auth_required
@admin_required
def new_chapter():
    subject_id = request.args.get('subject_id')
    subject = Subject.query.get(subject_id)
    return render_template('new_chapter.html', subject=subject)

@app.route('/new_chapter', methods=['POST'])
@auth_required
@admin_required
def new_chapter_post():
    chapter_name = request.form['chapter_name']
    chapter_description = request.form['chapter_description']
    subject_id = request.form['subject_id']  # Get the subject ID from form data
    chapter = Chapter(chapter_name=chapter_name, chapter_description=chapter_description, subject_id=subject_id)
    db.session.add(chapter)
    db.session.commit()
    flash('Chapter added successfully')
    return redirect(url_for('admin_home'))

@app.route('/edit_chapter')
@auth_required
@admin_required
def edit_chapter():
    chapter_id = request.args.get('chapter_id')
    chapter = Chapter.query.get(chapter_id)
    return render_template('edit_chapter.html', chapter=chapter)

@app.route('/edit_chapter', methods=['POST'])
@auth_required
@admin_required
def edit_chapter_post():
    chapter_id = request.args.get('chapter_id')
    chapter_name = request.form['chapter_name']
    chapter_description = request.form['chapter_description']
    existing_chapter = Chapter.query.filter(Chapter.id != chapter_id, Chapter.chapter_name == chapter_name).first()
    if existing_chapter:
        flash('Chapter with the same name already exists')
        return redirect(url_for('edit_chapter', chapter_id=chapter_id))
    chapter = Chapter.query.get(chapter_id)
    chapter.chapter_name = chapter_name
    chapter.chapter_description = chapter_description
    db.session.commit()
    flash('Chapter updated successfully')
    return redirect(url_for('admin_home'))

@app.route('/delete_chapter')
@auth_required
@admin_required
def delete_chapter():
    chapter_id = request.args.get('chapter_id')
    chapter = Chapter.query.get(chapter_id)
    db.session.delete(chapter)
    db.session.commit()
    flash('Chapter deleted successfully')
    return redirect(url_for('admin_home'))


@app.route('/new_subject')
@auth_required
@admin_required
def new_subject():
    return render_template('new_subject.html', user=User.query.get(session['user_id']))

@app.route('/new_subject', methods=['POST'])
@auth_required
@admin_required
def new_subject_post():
    subject_name = request.form['subject_name'] 
    subject_description = request.form['subject_description']
    subject_code = request.form['subject_code']
    subject_credit = request.form['subject_credit']
    
    subject = Subject(subject_name=subject_name, subject_description=subject_description, subject_code=subject_code, subject_credit=subject_credit)
    db.session.add(subject)
    db.session.commit()
    flash('Subject added successfully')
    return redirect(url_for('admin_home'))

@app.route('/edit_subject')
@auth_required
@admin_required
def edit_subject():
    subject_id = request.args.get('subject_id')
    subject = Subject.query.get(subject_id)
    return render_template('edit_subject.html', subject=subject)

@app.route('/edit_subject', methods=['POST'])
@auth_required
@admin_required
def edit_subject_post():
    subject_id = request.args.get('subject_id')
    subject_name = request.form['subject_name']
    subject_description = request.form['subject_description']
    subject_code = request.form['subject_code']
    subject_credit = request.form['subject_credit']
    subject = Subject.query.filter_by(subject_code=subject_code).first()
    existing_subject = Subject.query.filter(Subject.id != subject_id, Subject.subject_code == subject_code).first()
    if existing_subject:
        flash('Subject with the same code already exists')
        return redirect(url_for('edit_subject', subject_id=subject_id))
    
    existing_subject = Subject.query.filter(Subject.id != subject_id, Subject.subject_name == subject_name).first()
    if existing_subject:
        flash('Subject with the same name already exists')
        return redirect(url_for('edit_subject', subject_id=subject_id))
    subject = Subject.query.get(subject_id)
    subject.subject_name = subject_name
    subject.subject_description = subject_description
    subject.subject_code = subject_code
    subject.subject_credit = subject_credit
    db.session.commit()
    flash('Subject updated successfully')
    return redirect(url_for('admin_home'))

@app.route('/delete_subject')
@auth_required
@admin_required
def delete_subject():
    subject_id = request.args.get('subject_id')
    subject = Subject.query.get(subject_id)
    db.session.delete(subject)
    db.session.commit()
    flash('Subject deleted successfully')
    return redirect(url_for('admin_home'))



@app.route('/summary')
@auth_required
def summary():
    return render_template('summary.html', user=User.query.get(session['user_id']))

@app.route('/score')
@auth_required  # its just a Syntactic sugar
@user_required
def score():
        return render_template('score.html', user=User.query.get(session['user_id']))

@app.route('/login')
def login():
    if 'user_id' not in session:
        return render_template('login.html')
    else:
        flash('You are already logged in')
        return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if username == '' or password == '':
        flash('Username or password cannot be empty')
        return redirect(url_for('login'))
    if not user:
        flash('User does not exist')
        return redirect(url_for('login'))
    if not user.check_password(password):
        flash('Password does not match')
        return redirect(url_for('login'))
    # login successful
    session['user_id'] = user.id
    session['is_admin'] = user.is_admin
    session['username'] = user.username
    flash('Login successful')
    if user.is_admin:
        return redirect(url_for('admin_home'))
    else:
        return redirect(url_for('index'))
    # return render_template('index.html', user=User.query.get(session['user_id']))

@app.route('/register')
def register():
    if 'user_id' not in session:
        return render_template('register.html')
    else:
        flash('You are already logged in')
        return redirect(url_for('index'))

@app.route('/register', methods=['POST'])
def register_post():
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    Confirm_Password = request.form['confirm_password']
    fullname = request.form['fullname']
    qualification = request.form['qualification']
    DOB = request.form['dob']

    if username != email.split('@')[0]:
        flash('Username must be the same as the email id without @gmail.com')
        return redirect(url_for('register'))
    
    user = User.query.filter_by(username=username).first()
    if user:
        flash('User with the same username already exists')
        return redirect(url_for('register'))
    
    if password != Confirm_Password:
        flash('Password does not match')
        return redirect(url_for('register'))
    
    if username == '' or password == '':
        flash('Username or password cannot be empty')
        return redirect(url_for('register'))
    
    if fullname == '':
        flash('name cannot be empty')
        return redirect(url_for('register'))
    user = User(email=email, username=username, password=password, fullname=fullname, qualification=qualification, DOB=DOB,is_admin=False)
    db.session.add(user)
    db.session.commit()
    flash('User registered successfully')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully')
    return redirect(url_for('login'))

from flask import jsonify

@app.route('/debug')
def debug():
    return jsonify(dict(session))  # Convert session to JSON and return
