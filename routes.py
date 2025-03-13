from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db,User,subject,chapter,quiz,question,score
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


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
@auth_required  # its just a Syntactic sugar
def profile():
    return render_template('profile.html', user=User.query.get(session['user_id']))

@app.route('/dashboard')
@auth_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/login')
def login():
    return render_template('login.html')

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
    flash('Login successful')
    return redirect(url_for('index'))

@app.route('/register')
def register():
    return render_template('register.html')

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
    
    user = User(email=email, username=username, password=password, fullname=fullname, qualification=qualification, DOB=DOB)
    db.session.add(user)
    db.session.commit()
    flash('User registered successfully')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully')
    return redirect(url_for('login'))
