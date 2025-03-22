#This file act as a master file for all files of "application" because we have to import this file into the all files of "application"
from flask import Flask
from application.database import db #3 database
 
app = None

def create_app():
    app = Flask(__name__) #consider this file(module) as a server code for web application 
    app.debug = True
    app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///quizmaster.sqlite3"#3 database,  "quizmaster.sqlite3"-->name of database file
    db.init_app(app) #3 database,  it connects our "db" object of "database.py" to "app.py" or "app" object
    app.app_context().push() #runtime error, it brings everything under context of flask application
    return app

app = create_app()
from application.controllers import * #2 controllers,"*"-->means everything defines in "controllers.py"
""""
"from application.models import *"
we not use this because it makes our "app.py" file bulky so we made indirect connection of "models.py"
file by importing it into "controllers.py" file
"""

if __name__ == "__main__":
    app.run()

"""
By doing all things by setting up all files of "application" folder & "app.py"we have to go 
1. in pythpn shell & run "from app import *" then "instance" folder is created.
2. then run "db.created_all()" creates database file with name "quizmaster.sqlite3" as specified in "app.py"
inside "instance" folder is created
3.
"""
