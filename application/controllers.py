#contains all the routes & view functions
from flask import Flask,render_template,redirect,request
from flask import current_app as app #it refers to the "app" object created in "app.py" or "app.py" itself
#from app import app  ---->not used because it leads to circular import when we import "controllers.py" in "app.py"

from .models import *# both resides in same folder
import random
import string

#each endpoint with a combination of particular http method gives a particular resource

@app.route("/login",methods=["GET","POST"]) #url with specific http method gives specific 
def login():
    if request.method == "POST":
        username = request.form.get("username")
        pwd = request.form.get("pwd")
        this_user = User.query.filter_by(username=username).first()  # "this_user"gives object with specified username if it exists & in () LHS attribute "name" is "User" table/class/model attribute, RHS is data fetched from form 
        if this_user:
            if this_user.password == pwd:
                if this_user.type == "admin":
                    return redirect("/admin")
                else:
                    return render_template("user_dash.html",this_user= this_user)
            else:
                return render_template("incorrect_p.html")
        else:
            return render_template("not_exist.html")
    
    return render_template("login.html")

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email= request.form.get("email")
        pwd = request.form.get("pwd")
        user_name = User.query.filter_by(username=username).first()
        user_email = User.query.filter_by(email=email).first()
        if user_name or user_email:
            return render_template("already.html")
        else:
            new_user = User(username=username,email=email,password=pwd)#LHS attribute name in table, RHS is data fetched from form 
            db.session.add(new_user)
            db.session.commit()
            return redirect("/login")
        
    return render_template("register.html")

@app.route("/admin")
def admin_dash():
    this_user = User.query.filter_by(type="admin").first()
    all_info = Subject.query.all()
    return render_template("admin_dash.html", this_user=this_user, all_info=all_info)

@app.route("/home")
def home():
    return render_template("home.html",)

@app.route("/about")
def about():
    return render_template("about.html",)

@app.route("/contact")
def contact():
    return render_template("contact.html",)

@app.route("/help")
def help():
    return render_template("help.html",)

@app.route("/subject")
def subject():
    return render_template("subject.html",)


@app.route("/user_home")
def test():
    return render_template("user_home.html",)

@app.route("/user_subject")
def user_subject():
    return render_template("user_subject.html",)