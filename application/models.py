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

class User(db.Model):
    id = db.Column(db.Integer(), primary_key = True)

    firstname = db.Column(db.String(), nullable = False)
    lastname = db.Column(db.String(), nullable = False)

    dob = db.Column(db.Date(), nullable = False)
    gender = db.Column(db.String(), nullable = False)
    bloodgroup = db.Column(db.String(), nullable = False)
    qualification = db.Column(db.String(), nullable = False)

    email = db.Column(db.String(), unique = True, nullable = False)
    username = db.Column(db.String(), unique=True, nullable = False)
    password = db.Column(db.String(), nullable= False)

    profile_image = db.Column(db.String(), nullable= False)

    type = db.Column(db.String(), default ="general")
    details = db.relationship("Subject", backref = "creator") #pictitius column
    """
    if we have one "User" object say "uone" then if we write "uone.details" then it will retrieve all the entries 
    from "Subject" table which belongs to that particular user
    """

class Subject(db.Model):
    id = db.Column(db.Integer(), primary_key= True)
    sub_name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable = False)
    c_name = db.Column(db.String(), nullable = False)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable= False)

    """
    if we have one "Subject" object say "subone" then if we write "subone.creator" then it will give the user object
    which is related to that entry
    """