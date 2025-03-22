#contains all the routes & view functions
#Flask → The web framework used to create the web application.
from flask import Flask,render_template,redirect,request, jsonify
from flask import current_app as app #it refers to the "app" object created in "app.py" or "app.py" itself
#from app import app  ---->not used because it leads to circular import when we import "controllers.py" in "app.py"

from .models import *# both resides in same folder
import random
import string
from datetime import datetime
import os #Used for working with file paths.
#each endpoint with a combination of particular http method gives a particular resource


#Handling Image Uploads
UPLOAD_FOLDER = "static/uploads"  # Defines where uploaded files will be stored.
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER # Defines where uploaded files will be stored.

@app.route("/login",methods=["GET","POST"])#url with specific http method gives specific 
def login():
    if request.method == "POST":
        username = request.form.get("username")
        pwd = request.form.get("pwd")
        this_user = User.query.filter_by(username=username).first()
        if this_user:
            if this_user.password == pwd:
                if this_user.type == "admin":
                    return redirect("/admin_home")
                else:
                    return redirect(f"/user_home/{this_user.id}")
            else:
                return render_template("incorrect_p.html")
        else:
            return render_template("not_exist.html")
    
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        firstname = request.form['f_name']
        lastname = request.form['l_name']
        
        # Convert DOB from YYYY-MM-DD (default input format) to a Python date object
        dob_str = request.form['dob']
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()

        gender = request.form['gender']
        blood_group = request.form['blood_group']
        qualification = request.form['qualification']

        email = request.form.get('email')
        username = request.form.get('username')
        pwd = request.form.get("pwd")

        profile_image = request.files["profile_image"]  # Retrieves the uploaded file
        
        profile_image_filename = None  # Default to None in case no image is uploaded
        if profile_image and profile_image.filename:
            profile_image_filename = profile_image.filename  # Store only the filename
            profile_image_path = os.path.join(app.config["UPLOAD_FOLDER"], profile_image_filename)
            profile_image.save(profile_image_path)  # Save the file

        existing_username = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()
        if existing_username or existing_email:
            return render_template("already.html")
        else:
            new_user = User(
                firstname=firstname,
                lastname=lastname,
                dob=dob,  # Store as a proper date object
                gender=gender,
                bloodgroup=blood_group,
                qualification=qualification,
                email=email,
                username=username,
                password=pwd,
                profile_image=profile_image_filename,  # Store filename, not the FileStorage object
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect("/login")

    return render_template("register.html")
    
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


#ADMIN ROUTE & FUNCTION 
@app.route("/admin_home")
def admin_home():
    this_user = User.query.filter_by(type="admin").first()
    return render_template("admin/admin_home.html", profile_image=this_user.profile_image, profile_name=this_user.firstname)

@app.route("/admin_subject", methods=["GET", "POST"])
def admin_subject():
    if request.method == 'GET':
        subjects=Subject.query.all()
        this_user = User.query.filter_by(type="admin").first()
        return render_template("admin/admin_subject.html", profile_image=this_user.profile_image, profile_name=this_user.firstname, subjects=subjects)

    if request.method == 'POST':
        subject = request.form['sub_name']
        category = request.form['category']
        description = request.form['description']

        sub_image = request.files["sub_image"]  

        sub_image_filename = None 
        if sub_image and sub_image.filename:
            sub_image_filename = sub_image.filename 
            sub_image_path = os.path.join(app.config["UPLOAD_FOLDER"],sub_image_filename)
            sub_image.save(sub_image_path)

        existing_subject = Subject.query.filter_by(name=subject).first()
        if existing_subject:
            return render_template("already.html")
        else:
            new_subject = Subject(
                name=subject,
                category=category,
                description=description,
                sub_image=sub_image_filename,  # Store filename, not the FileStorage object
            )
            db.session.add(new_subject)
            db.session.commit()
            return redirect("/admin_subject")
        
@app.route("/get_subject/<int:subject_id>", methods=["GET", "POST"])
def get_subject(subject_id):
    if request.method == 'GET':
        subject=Subject.query.filter_by(id=subject_id).first()
        if subject:
            # Convert SQLAlchemy object to dictionary
            subject_data = {
            "id": subject.id,
            "name": subject.name,
            "description": subject.description,
            "category": subject.category
            }
            print("gfhffhgjgj",jsonify(subject_data))
            return jsonify(subject_data)
        else:
            return jsonify({"error": "Subject not found"}), 404
    # # if request.method == 'POST':
    #     subject = request.form['sub_name']
    #     category = request.form['category']
    #     description = request.form['description']

    #     sub_image = request.files["sub_image"]  

    #     sub_image_filename = None 
    #     if sub_image and sub_image.filename:
    #         sub_image_filename = sub_image.filename 
    #         sub_image_path = os.path.join(app.config["UPLOAD_FOLDER"],sub_image_filename)
    #         sub_image.save(sub_image_path)

    #     existing_subject = Subject.query.filter_by(name=subject).first()
    #     if existing_subject:
    #         return render_template("already.html")
    #     else:
    #         new_subject = Subject(
    #             name=subject,
    #             category=category,
    #             description=description,
    #             sub_image=sub_image_filename,  # Store filename, not the FileStorage object
    #         )
    #         db.session.add(new_subject)
    #         db.session.commit()
    #         return redirect("/admin_subject")

@app.route("/admin_module")
def admin_module():
    this_user = User.query.filter_by(type="admin").first()
    return render_template("admin/admin_module.html",profile_image=this_user.profile_image, profile_name=this_user.firstname)

@app.route("/admin_user")
def admin_user():
    this_user = User.query.filter_by(type="admin").first()
    return render_template("admin/admin_user.html",profile_image=this_user.profile_image, profile_name=this_user.firstname)

 
#USER ROUTE & FUNCTION 
@app.route("/user_home/<int:user_id>")
def user_home(user_id):
    this_user = User.query.filter_by(id=user_id).first()
    return render_template("user/user_home.html", profile_image=this_user.profile_image, profile_name=this_user.firstname)

@app.route("/user_subject")
def user_subject():
    return render_template("user/user_subject.html",)

@app.route("/user_module")
def user_module():
    return render_template("user/user_module.html")