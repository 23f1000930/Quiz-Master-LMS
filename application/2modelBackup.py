#store all models

from .database import db #check/look for this "database.py" file in the current folder that you are existing

#CORRECT: ".database" means, it says to "models.py" that search/look & import "database.py" from there current folder in which your are reciding/existing(but not the root folder)
#INCORRECR: "database" means, it says to "models.py" that search & import "database.py" from the root folder(which gives error)
"""
INCORRECR: "application.database" means, it says to "models.py" that search for application
folder in there current folder & then search "database.py" in that "application" folder
(which gives error, because does not have "application/application/database.py" like structure)
OR
"application.database"> "models.py" will think that there is one more folder in the folder it is 
existing("application") which is "applicatioon and inside that folder we have "database.py" file
"""

# Association table for User-Subject (Students taking subjects)
user_subject = db.Table(
    'user_subject',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('subject_id', db.Integer, db.ForeignKey('subject.id'), primary_key=True)
)

# Association table for Subject-Instructor (Subjects having instructors)
subject_instructor = db.Table(
    'subject_instructor',
    db.Column('subject_id', db.Integer, db.ForeignKey('subject.id'), primary_key=True),
    db.Column('instructor_id', db.Integer, db.ForeignKey('instructor.id'), primary_key=True)
)

class User(db.Model):  # Student Model
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(), nullable=False)
    lastname = db.Column(db.String())

    dob = db.Column(db.Date(), nullable=False)
    gender = db.Column(db.String(), nullable=False)
    bloodgroup = db.Column(db.String(), nullable=False)
    qualification = db.Column(db.String(), nullable=False)

    email = db.Column(db.String(), unique=True, nullable=False)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

    profile_image = db.Column(db.String(), nullable=False)

    type = db.Column(db.String(), default="general")
    subjects = db.relationship('Subject', secondary=user_subject, backref=db.backref('students', lazy='dynamic'))

class Instructor(db.Model):  # Instructor Model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    experience = db.Column(db.Integer)
    description = db.Column(db.String(), nullable=False)

class Subject(db.Model):  # Subject Model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    category = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    sub_image = db.Column(db.String(), nullable=False)

    instructors = db.relationship('Instructor', secondary=subject_instructor, backref=db.backref('subjects', lazy='dynamic'))
    chapters = db.relationship("Chapter",backref = "thatsubject")

class Chapter(db.Model):  # Chapter Model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)

    subject_id = db.Column(db.Integer(),db.ForeignKey("subject.id"),nullable= False)
    lectures = db.relationship("Lecture",backref = "thatlecturechapter")
    quizzes = db.relationship("Quiz",backref = "thatquizchapter")

class Lecture(db.Model):  # Lecture Model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    link = db.Column(db.String(), nullable=False)

    chapter_id = db.Column(db.Integer(),db.ForeignKey("chapter.id"),nullable= False)

    quizzes = db.relationship("Quiz", backref='thisquiz', uselist=False, cascade="all, delete-orphan")

class Quiz(db.Model):  # Quiz Model
    id = db.Column(db.Integer, primary_key=True)
    
    release_date = db.Column(db.DateTime, nullable=False)  # Stores Date & Time
    deadline = db.Column(db.DateTime)  # Stores Date & Time
    time_duration = db.Column(db.Time)  # Stores only Time (hh:mm:ss)
    
    total_attempts = db.Column(db.Integer)

    chapter_id = db.Column(db.Integer(),db.ForeignKey("chapter.id"),nullable= False)
    lecture_id = db.Column(db.Integer(),db.ForeignKey("lecture.id")) 
   