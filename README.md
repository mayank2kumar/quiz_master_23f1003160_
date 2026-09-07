# Quiz Master

A web-based **Quiz Management and Examination Preparation System** built using Flask, Flask-SQLAlchemy, SQLite, Jinja2, HTML, CSS, and Bootstrap.

The application provides separate functionality for **Administrators** and **Students/Users**. Administrators can manage subjects, chapters, quizzes, and questions, while users can register, attempt quizzes, and view their performance.

---

## Live Demo

### Website

**[Open Quiz Master Live Website](https://mayankkumar1.pythonanywhere.com/)**

### Admin Login

| Field    | Value         |
| -------- | ------------- |
| Username | `admin`       |
| Password | `admin`       |
| Role     | Administrator |

---

# Table of Contents

* [About the Project](#about-the-project)
* [Project Objectives](#project-objectives)
* [Key Features](#key-features)
* [User Roles](#user-roles)
* [Technology Stack](#technology-stack)
* [Project Structure](#project-structure)
* [Database Design](#database-design)
* [Application Workflow](#application-workflow)
* [Requirements](#requirements)
* [Installation and Setup](#installation-and-setup)
* [Environment Variables](#environment-variables)
* [Running the Application Locally](#running-the-application-locally)

---

# About the Project

**Quiz Master** is a web-based quiz management system.

The application is designed to provide a centralized platform where an administrator can create and manage educational content and registered users can participate in quizzes and track their performance.

The system uses a role-based approach:

* **Administrator** manages the complete quiz system.
* **Users/Students** register and attempt available quizzes.
* Quiz scores are stored in the database and can be viewed for performance analysis.

The project is built with Flask on the backend and uses Jinja2 templates with HTML/CSS/Bootstrap for the frontend.

---

# Project Objectives

The main objectives of Quiz Master are:

1. Provide an online platform for conducting quizzes.
2. Allow administrators to manage subjects and chapters.
3. Allow administrators to create and manage quizzes.
4. Allow administrators to add and manage questions.
5. Allow users to register and securely log in.
6. Allow users to attempt available quizzes.
7. Calculate and store quiz scores.
8. Allow users to review their quiz performance.
9. Provide a simple and user-friendly interface.
10. Demonstrate the implementation of a complete Flask-based web application.

---

# Key Features

## Administrator Features

* Administrator authentication
* Admin dashboard
* Subject management
* Chapter management
* Quiz management
* Question management
* Add, edit and delete quiz content
* View registered users
* Manage educational content
* View quiz-related information

## User Features

* User registration
* User login/logout
* Browse available subjects
* Browse chapters and quizzes
* Attempt quizzes
* Time-limited quizzes
* Automatic score calculation
* Store quiz results
* View previous performance
* Track quiz scores

## General Features

* Role-based access
* Session-based authentication
* SQLite database
* Password hashing
* Flask-based routing
* Jinja2 template rendering
* Responsive frontend
* Persistent quiz data

---

# User Roles

## 1. Administrator

The administrator has privileged access to the application.

The administrator can:

* Manage subjects
* Manage chapters
* Create quizzes
* Edit quizzes
* Delete quizzes
* Add questions
* Edit questions
* Delete questions
* Manage quiz content
* View application data

### Default Administrator

```text
Username: admin
Password: admin
```

---

## 2. User / Student

A normal registered user can:

* Create an account
* Log in
* Browse available quizzes
* Attempt quizzes
* Submit answers
* Receive quiz results
* View previous scores

Normal users do not have access to administrator functionality.

---

# Technology Stack

| Technology       | Purpose                                 |
| ---------------- | --------------------------------------- |
| Python           | Programming language                    |
| Flask            | Backend web framework                   |
| Flask-SQLAlchemy | Database ORM                            |
| SQLAlchemy       | Database interaction                    |
| SQLite           | Database                                |
| Jinja2           | Server-side templating                  |
| HTML5            | Frontend structure                      |
| CSS3             | Styling                                 |
| Bootstrap        | Responsive UI                           |
| Werkzeug         | Password hashing and security utilities |
| python-dotenv    | Environment variable management         |
| Git              | Version control                         |
| GitHub           | Source code hosting                     |
| PythonAnywhere   | Web hosting/deployment                  |

---

# Project Structure

```text
quiz_master_23f1003160_/
│
├── templates/
│   ├── ...
│   └── ...
│
├── app.py
├── config.py
├── models.py
├── routes.py
├── requirement.txt
├── README.md
├── .gitignore
└── MAD1 Project Report.pdf
```

## Important Files

### `app.py`

The main Flask application file.

It:

* Creates the Flask application.
* Loads the configuration.
* Loads the database models.
* Loads application routes.

The application object is created using:

```python
app = Flask(__name__)
```

---

### `config.py`

Handles application configuration.

The application reads configuration values from environment variables using `python-dotenv`.

The main configuration variables are:

```text
SQLALCHEMY_DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS
SECRET_KEY
```

---

### `models.py`

Contains the SQLAlchemy database models.

The project currently defines models for:

* User
* Subject
* Chapter
* Quiz
* Question
* Score

The application also creates database tables automatically when the models are loaded.

---

### `routes.py`

Contains the application's Flask routes and application logic.

Routes handle:

* Authentication
* Registration
* Login
* Logout
* Administrator functionality
* Subject management
* Chapter management
* Quiz management
* Question management
* Quiz attempts
* Score/results functionality

---

### `templates/`

Contains the Jinja2 HTML templates used by the application.

---

### `requirement.txt`

Contains the Python packages required to run the application.

Install them using:

```bash
pip install -r requirement.txt
```

---

# Database Design

The application uses **SQLite** through Flask-SQLAlchemy.

The primary database entities are:

```text
User
 │
 └── Score
       │
       └── Quiz
             │
             └── Question

Subject
 │
 └── Chapter
       │
       └── Quiz
```

## User

Stores registered user information.

Important fields include:

* ID
* Email
* Username
* Password hash
* Full name
* Qualification
* Date of birth
* Administrator status

Passwords are stored as password hashes rather than plain-text passwords.

---

## Subject

Represents an academic subject.

Example:

```text
Subject:
    Python Programming
```

A subject can contain multiple chapters.

---

## Chapter

Represents a chapter within a subject.

Example:

```text
Python Programming
    ├── Introduction
    ├── Variables
    ├── Functions
    └── Object-Oriented Programming
```

---

## Quiz

Represents an individual quiz associated with a chapter.

A quiz contains information such as:

* Quiz name
* Description
* Time duration
* Chapter

---

## Question

Stores individual questions belonging to a quiz.

Each question contains:

* Question text
* Four options
* Correct answer
* Question title
* Quiz association

---

## Score

Stores user quiz performance.

The score model stores information such as:

* Total score
* Obtained score
* Percentage
* Time taken
* User
* Quiz

---

# Application Workflow

The general workflow is:

```text
User
  │
  ▼
Registration
  │
  ▼
Login
  │
  ▼
Dashboard
  │
  ▼
Select Subject
  │
  ▼
Select Chapter
  │
  ▼
Select Quiz
  │
  ▼
Attempt Quiz
  │
  ▼
Submit Answers
  │
  ▼
Score Calculation
  │
  ▼
Result
  │
  ▼
Score History
```

The administrator workflow is:

```text
Administrator Login
        │
        ▼
   Admin Dashboard
        │
        ├── Subjects
        │      └── Chapters
        │
        ├── Quizzes
        │      └── Questions
        │
        └── Users / Results
```

---

# Requirements

Before running the project, make sure the following are installed:

* Python 3.10 or newer
* Git
* pip
* A web browser

Recommended:

```text
Python 3.13
```

---

# Installation and Setup

## 1. Clone the Repository

Open a terminal or command prompt.

```bash
git clone https://github.com/mayank2kumar/quiz_master_23f1003160_.git
```

Move into the project directory:

```bash
cd quiz_master_23f1003160_
```

---

# 2. Create a Virtual Environment

Creating a virtual environment is recommended so that project dependencies remain isolated from other Python projects.

## Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

You should see:

```text
(venv)
```

in your terminal.

---

## Linux / macOS

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

---

# 3. Upgrade pip

```bash
python -m pip install --upgrade pip
```

---

# 4. Install Dependencies

The project uses `requirement.txt`.

Run:

```bash
pip install -r requirement.txt
```

---

# 5. Configure Environment Variables

The project uses environment variables for configuration.

Create a file named:

```text
.env
```

in the root directory.

Example:

```env
SQLALCHEMY_DATABASE_URI=sqlite:///quiz_master.db
SQLALCHEMY_TRACK_MODIFICATIONS=False
SECRET_KEY=replace-this-with-a-secure-secret-key
```

For local development, the SQLite database can be stored in the project directory.

---

# 6. Do Not Commit `.env`

The `.env` file contains configuration values and secrets.

Do not upload it to GitHub.

The repository already uses `.gitignore` to exclude environment-specific files.

Your repository should contain:

```text
.gitignore
```

and should not contain:

```text
.env
```

---

# Running the Application Locally

After installing the dependencies and configuring `.env`, run:

```bash
python app.py
```

If your local setup uses Flask's development server configuration, open the URL shown in the terminal, typically:

```text
http://127.0.0.1:5000/
```

or:

```text
http://localhost:5000/
```

---

# Default Admin Account

The application creates a default administrator when an administrator does not already exist in the database.

```text
Username: admin
Password: admin
```
