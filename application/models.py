from .database import db

# Association table for User-Subject (Students taking subjects)
user_subject = db.Table(
    'user_subject',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), primary_key=True),
    db.Column('subject_id', db.Integer, db.ForeignKey('subject.id', ondelete="CASCADE"), primary_key=True)
)

# Association table for Subject-Instructor (Subjects having instructors)
subject_instructor = db.Table(
    'subject_instructor',
    db.Column('subject_id', db.Integer, db.ForeignKey('subject.id', ondelete="CASCADE"), primary_key=True),
    db.Column('instructor_id', db.Integer, db.ForeignKey('instructor.id', ondelete="CASCADE"), primary_key=True)
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

    subjects = db.relationship('Subject', secondary=user_subject, backref='thatuser')
    scores = db.relationship("Score", backref="thatuser", cascade="all, delete-orphan")

class Instructor(db.Model):  # Instructor Model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    experience = db.Column(db.Integer)
    description = db.Column(db.String(), nullable=False)
    inst_image = db.Column(db.String(), nullable=False)

class Subject(db.Model):  # Subject Model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    category = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    sub_image = db.Column(db.String(), nullable=False)

    instructors = db.relationship('Instructor', secondary=subject_instructor, backref='that_inst_sub')
    chapters = db.relationship("Chapter", backref="that_chap_sub", cascade="all, delete-orphan")

class Chapter(db.Model):  # Chapter Model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)

    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id", ondelete="CASCADE"), nullable=False)
    lectures = db.relationship("Lecture", backref="thatlecturechapter", cascade="all, delete-orphan")
    quizzes = db.relationship("Quiz", backref="thatquizchapter", cascade="all, delete-orphan")

class Lecture(db.Model):  # Lecture Model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    link = db.Column(db.String(), nullable=False)

    chapter_id = db.Column(db.Integer, db.ForeignKey("chapter.id", ondelete="CASCADE"), nullable=False)

    quizzes = db.relationship("Quiz", backref='thisquiz', cascade="all, delete-orphan")

#backref="thisquiz" this must be backref="thislecture"

class Quiz(db.Model):  # Quiz Model
    id = db.Column(db.Integer, primary_key=True)

    release_date = db.Column(db.DateTime, nullable=False)  # Stores Date & Time
    deadline = db.Column(db.DateTime)  # Stores Date & Time
    time_duration = db.Column(db.Time)  # Stores only Time (hh:mm:ss)

    total_attempts = db.Column(db.Integer)

    chapter_id = db.Column(db.Integer, db.ForeignKey("chapter.id", ondelete="CASCADE"), nullable=False)
    lecture_id = db.Column(db.Integer, db.ForeignKey("lecture.id", ondelete="CASCADE"))

    questions = db.relationship("Question", backref="thatquiz", cascade="all, delete-orphan")
    scores = db.relationship("Score", backref="thatquiz", cascade="all, delete-orphan")

class Question(db.Model):  # Question Model
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(), nullable=False)
    question_statement = db.Column(db.String(), nullable=False)
    marks = db.Column(db.Integer(), nullable=False)
    answer = db.Column(db.String(), nullable=False)

    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id", ondelete="CASCADE"), nullable=False)

class Score(db.Model):  # Score Model
    id = db.Column(db.Integer, primary_key=True)
    time_stamp_of_last_attempt = db.Column(db.DateTime, nullable=False)
    time_taken = db.Column(db.DateTime)
    user_answer = db.Column(db.String(), nullable=False)
    total_score = db.Column(db.Integer(), nullable=False)

    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
