#contains all the routes & view functions
#Flask → The web framework used to create the web application.
from flask import Flask,render_template,redirect,request, jsonify, send_from_directory
from flask import current_app as app #it refers to the "app" object created in "app.py" or "app.py" itself
#from app import app  ---->not used because it leads to circular import when we import "controllers.py" in "app.py"

from .models import *# both resides in same folder
import random
import string
from datetime import datetime, time
import os #Used for working with file paths.
#each endpoint with a combination of particular http method gives a particular resource


#Handling Image Uploads
UPLOAD_FOLDER = "static/uploads"  # Defines where uploaded files will be stored.
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER # Defines where uploaded files will be stored.

#query.get() ----------->fetches only first record with primary key

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

        # strptime() stands for "string parse time" and is a method in Python's datetime 
        # module that converts a date-time string into a datetime object.
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


@app.route("/admin_instructor", defaults={'optional': None}, methods=["GET", "POST"])
@app.route("/admin_instructor/<optional>", methods=["GET", "POST"])  #for creating api for showing instructors in subject create form only
def admin_instructor(optional):
    if request.method == 'GET':
        instructors=Instructor.query.all()
        if optional == "all_instructors":
            # Return JSON response when optional parameter is provided
            # list of instructor dictionary
            all_instructors = [{"id": instructor.id, "name": instructor.name} for instructor in instructors]
            return jsonify(all_instructors) 
        else:
            this_user = User.query.filter_by(type="admin").first()
            return render_template("admin/admin_instructor.html", profile_image=this_user.profile_image, profile_name=this_user.firstname, instructors=instructors)

    if request.method == 'POST':
        inst_name = request.form['inst_name']
        exp_years = request.form['exp_years']
        inst_desp = request.form['inst_desp']

        inst_image = request.files["inst_image"]  

        existing_instructor = Instructor.query.filter_by(name=inst_name).first()
        if existing_instructor:
            return render_template("already.html")
        else:
            #uploading Image
            inst_image_filename = None 
            if inst_image and inst_image.filename:
                inst_image_filename = inst_image.filename 
                inst_image_path = os.path.join(app.config["UPLOAD_FOLDER"],inst_image_filename)
                inst_image.save(inst_image_path)

            new_instructor = Instructor(
                name=inst_name,
                experience=exp_years,
                description=inst_desp,
                inst_image=inst_image_filename,  # Store filename, not the FileStorage object
            )
            db.session.add(new_instructor)
            db.session.commit()
            return redirect("/admin_instructor")


#----------------------------------------ABOVE IS AN API IMPLEMENTATION ------------------------------------------------------------------------
@app.route("/modify_instructor/<int:instructor_id>", methods=["GET", "POST"])
def modify_instructor(instructor_id):
    if request.method == 'GET':
        instructor=Instructor.query.filter_by(id=instructor_id).first()
        if instructor:
            # Convert SQLAlchemy object to dictionary
            instructor_data = {
            "id": instructor.id,
            "name": instructor.name,
            "experience": instructor.experience,
            "description": instructor.description,
            "inst_image": instructor.inst_image
            }
            print("INSTRUCTOR DATA",jsonify(instructor_data))
            return jsonify(instructor_data)
        else:
            return jsonify({"error": "Instructor not found"}), 404
        
    if request.method == 'POST':
        instructor = Instructor.query.get(instructor_id)
        if instructor:
            instructor.name = request.form['mod_inst_name']
            instructor.experience = request.form['mod_exp_years']
            instructor.description = request.form['mod_inst_desp']

            # Check if an image is uploaded
            if 'mod_inst_image' in request.files:
                file = request.files['mod_inst_image']
                if file and file.filename:
                    # Remove previous image if exists
                    if instructor.inst_image:
                        old_image_path = os.path.join('static/uploads/', instructor.inst_image)
                        if os.path.exists(old_image_path):
                            os.remove(old_image_path)

                    # Save the new image
                    filename = file.filename
                    new_image_path = os.path.join('static/uploads/', filename)
                    file.save(new_image_path)

                    # Update subject image path
                    instructor.inst_image = filename

            db.session.commit()
            return redirect("/admin_instructor")
        return render_template("notfound.html")
#--------------------------------------------------------------------------------------------------------------------



@app.route("/admin_subject", methods=["GET", "POST"])
def admin_subject():
    if request.method == 'GET':
        subjects=Subject.query.all()
        this_user = User.query.filter_by(type="admin").first()
        return render_template("admin/admin_subject.html", profile_image=this_user.profile_image, profile_name=this_user.firstname, subjects=subjects)

    if request.method == 'POST':
        subject_name = request.form['sub_name']
        category = request.form['category']
        description = request.form['description']

        sub_image = request.files["sub_image"]  

        existing_subject = Subject.query.filter_by(name=subject_name).first()
        if existing_subject:
            return render_template("already.html")
        else:
            #uploading Image
            sub_image_filename = None 
            if sub_image and sub_image.filename:
                sub_image_filename = sub_image.filename 
                sub_image_path = os.path.join(app.config["UPLOAD_FOLDER"],sub_image_filename)
                sub_image.save(sub_image_path)

            new_subject = Subject(
                name=subject_name,
                category=category,
                description=description,
                sub_image=sub_image_filename,  # Store filename, not the FileStorage object
            )
            db.session.add(new_subject)
            db.session.commit()

            #HANDLING ADDING OF INSRUCTORS IN A SUBJECT
            instructors = Instructor.query.all()
            instructors_ids = [instructor.id for instructor in instructors]
            print(instructors_ids)
            selected_instructors = []
            for i in instructors_ids:
                if str(i) in request.form:
                    selected_instructors.append(int(request.form[str(i)]))
            
            #fetching all instructors object for list of "selected_instructors"
            #equivalent to SELECT * FROM instructor WHERE id IN (2, 4, 6);
            # means-> five/fetch those instructors such that there id belongs to "selected_instructors"
            instructors = Instructor.query.filter(Instructor.id.in_(selected_instructors)).all()        
            new_subject.instructors.extend(instructors) # Add multiple instructors, adds all instructors at once to the subject.
            db.session.commit()

            return redirect("/admin_subject")


#----------------------------------------ABOVE IS AN API IMPLEMENTATION ------------------------------------------------------------------------
@app.route("/modify_subject/<int:subject_id>", methods=["GET", "POST"])
def modify_subject(subject_id):
    if request.method == 'GET':
        subject=Subject.query.filter_by(id=subject_id).first()
        if subject:
            # Convert SQLAlchemy object to dictionary
            subject_data = {
            "id": subject.id,
            "name": subject.name,
            "description": subject.description,
            "category": subject.category,
            "sub_image": subject.sub_image,
            "selected_instructors": [
                    {
                        "id": instructor.id,
                        "name": instructor.name,
                        # "experience": instructor.experience,
                        # "description": instructor.description,          #-------->NOT NEEDED
                        # "inst_image": instructor.inst_image
                    }
                    for instructor in subject.instructors  # Convert Instructor objects to dict
                ],
                "all_instructors": [
                    {
                        "id": instructor.id,
                        "name": instructor.name,
                        # "experience": instructor.experience,
                        # "description": instructor.description,         #-------->NOT NEEDED
                        # "inst_image": instructor.inst_image
                    }
                    for instructor in Instructor.query.all()  # Convert Instructor objects to dict
                ]     
            }
            #subject.instructors , Returns a list of Instructor objects
            print("SUBJECT DATA",jsonify(subject_data))
            return jsonify(subject_data)
        else:
            return jsonify({"error": "Subject not found"}), 404
        
    if request.method == 'POST':
        subject = Subject.query.get(subject_id)
        if subject:
            subject.name = request.form['mod_sub_name']
            subject.category = request.form['mod_category']
            subject.description = request.form['mod_description']

            # Check if an image is uploaded
            if 'mod_sub_image' in request.files:
                file = request.files['mod_sub_image']
                if file and file.filename:
                    # Remove previous image if exists
                    if subject.sub_image:
                        old_image_path = os.path.join('static/uploads/', subject.sub_image)
                        if os.path.exists(old_image_path):
                            os.remove(old_image_path)

                    # Save the new image
                    filename = file.filename
                    new_image_path = os.path.join('static/uploads/', filename)
                    file.save(new_image_path)

                    # Update subject image path
                    subject.sub_image = filename



            #HANDLING Modifying OF INSRUCTORS IN A SUBJECT

            # Clear the instructors relationship
            subject.instructors.clear()

            #Adding New instructors relationship
            instructors = Instructor.query.all()
            instructors_ids = [instructor.id for instructor in instructors]
            print(instructors_ids)
            selected_instructors = []
            for i in instructors_ids:
                if str(i) in request.form:
                    selected_instructors.append(int(request.form[str(i)]))
            instructors = Instructor.query.filter(Instructor.id.in_(selected_instructors)).all()        
            subject.instructors.extend(instructors) # Add multiple instructors, adds all instructors at once to the subject.

            db.session.commit()
            return redirect("/admin_subject")
        return render_template("notfound.html")
#--------------------------------------------------------------------------------------------------------------------


@app.route("/admin_module/<int:subject_id>", methods=["GET", "POST"])
def admin_module(subject_id):
    if request.method == 'GET':
        subject = Subject.query.get(subject_id)
        chapters = Chapter.query.filter_by(subject_id=subject_id).all()


        #FOR SHOWING "LECTURES" & "QUIZZES" ON SUBJECT SPECIFIC & CHAPTER AREA
        chapter_ids = [chapter.id for chapter in chapters]

        lectures = {}
        quizzes = {}

        #either use this
        # quizzes = Quiz.query.filter(Quiz.chapter_id.in_(chapter_ids)).all()
        # lectures = Lecture.query.filter(Lecture.chapter_id.in_(chapter_ids)).all()
        #or below this
        for chapter_id in chapter_ids:
            lectures[chapter_id] = Lecture.query.filter_by(chapter_id=chapter_id).all()
            quizzes[chapter_id] = Quiz.query.filter_by(chapter_id=chapter_id).all()
            print(quizzes)



        this_user = User.query.filter_by(type="admin").first()
        return render_template("admin/admin_module.html", subject=subject, chapters=chapters, lectures=lectures,quizzes=quizzes, profile_image=this_user.profile_image, profile_name=this_user.firstname)
    
    if request.method == 'POST':
        chapter_name = request.form['chapter_name']
        chapter_desp = request.form.get('chapter_desp')

        #OR existing_chapter = Chapter.query.get(name=chapter_name)
        existing_chapter = Chapter.query.filter_by(name=chapter_name).first()
        if existing_chapter:
            return render_template("already.html")
        else:
            new_chapter = Chapter(
                name=chapter_name,
                description=chapter_desp,
                subject_id=subject_id
            )

            db.session.add(new_chapter)
            db.session.commit()
            return redirect(f"/admin_module/{subject_id}")


#----------------------------------------ABOVE IS AN API IMPLEMENTATION ------------------------------------------------------------------------
@app.route("/modify_module/<int:chapter_id>", methods=["GET", "POST"])
def modify_module(chapter_id):
    if request.method == 'GET':
        chapter=Chapter.query.filter_by(id=chapter_id).first()
        if chapter:
            # Convert SQLAlchemy object to dictionary
            chapter_data = {
            "id": chapter.id,
            "name": chapter.name,
            "description": chapter.description
            }
            print("CHAPTER DATA",jsonify(chapter_data))
            return jsonify(chapter_data)
        else:
            return jsonify({"error": "Chapter not found"}), 404
        
    if request.method == 'POST':
        chapter = Chapter.query.get(chapter_id)
        if chapter:
            chapter.name = request.form['mod_chapter_name']
            chapter.description = request.form['mod_chapter_desp']

            db.session.commit()
            subject_id = chapter.that_chap_sub.id
            return redirect(f"/admin_module/{subject_id}")
        return render_template("notfound.html")
#------------------------------------------------------------------------------------------------------------------------------------------------



@app.route("/admin_lecture/<int:chapter_id>", methods=["GET", "POST"])
@app.route("/admin_lecture/<int:chapter_id>/<optional>", methods=["GET", "POST"])  #for creating api for showing lectures in quiz create form only
def admin_lecture(chapter_id, optional):
    if request.method == 'GET':
        lectures=Lecture.query.filter_by(chapter_id=chapter_id)
        if optional == "all_lectures":
            # Return JSON response when optional parameter is provided
            # list of lectures dictionary
            all_lectures = [{"id": lecture.id, "name": lecture.name, "link":lecture.link} for lecture in lectures]
            return jsonify(all_lectures) 
        
    if request.method == 'POST':
        lecture_name = request.form['lecture_name']
        description = request.form['lect_desp']
        link = request.form['lect_link']

        #OR existing_lecture = Lecture.query.get(name=lecture_name)
        existing_lecture = Lecture.query.filter_by(name=lecture_name).first()
        if existing_lecture:
            return render_template("already.html")
        else:
            new_lecture = Lecture(
                name=lecture_name,
                description=description,
                link = link,
                chapter_id = chapter_id
            )

            db.session.add(new_lecture)
            db.session.commit()

            chapter = Chapter.query.get(chapter_id)
            subject_id = chapter.that_chap_sub.id
            return redirect(f"/admin_module/{subject_id}")

#----------------------------------------ABOVE IS AN API IMPLEMENTATION ------------------------------------------------------------------------
@app.route("/modify_lecture/<int:lecture_id>", methods=["GET", "POST"])
def modify_lecture(lecture_id):
    if request.method == 'GET':
        lecture=Lecture.query.filter_by(id=lecture_id).first()
        if lecture:
            # Convert SQLAlchemy object to dictionary
            lecture_data = {
            "id": lecture.id,
            "name": lecture.name,
            "description": lecture.description,
            "link": lecture.link
            }
            print("LECTURE DATA",jsonify(lecture_data))
            return jsonify(lecture_data)
        else:
            return jsonify({"error": "Lecture not found"}), 404
    if request.method == 'POST':
        lecture = Lecture.query.get(lecture_id)
        if lecture:
            lecture.name = request.form['mod_lecture_name']
            lecture.description = request.form['mod_lect_desp']
            lecture.link = request.form['mod_lect_link']

            db.session.commit()

            chapter = lecture.thatlecturechapter
            subject_id = chapter.that_chap_sub.id
            return redirect(f"/admin_module/{subject_id}")
        return render_template("notfound.html")    
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route("/admin_quiz/<int:chapter_id>", methods=["GET", "POST"])
def admin_quiz(chapter_id):
    if request.method == 'POST':
        release_date_str = request.form['release_date']  # '2025-03-07T10:07'
        deadline_str = request.form['deadline']  # '2025-03-08T10:07'
        time_duration_str = request.form['time_duration']  # '14:07' (hh:mm)
        total_attempts = request.form['total_attempts']
        lecture_id = request.form.get('oneLecture', None)

        # Convert strings to proper datetime and time objects
        # strptime() stands for "string parse time" and is a method in Python's datetime 
        # module that converts a date-time string into a datetime object.
        release_date = datetime.strptime(release_date_str, "%Y-%m-%dT%H:%M")
        deadline = datetime.strptime(deadline_str, "%Y-%m-%dT%H:%M") if deadline_str else None
        if time_duration_str:
            hours, minutes = map(int, time_duration_str.split(":")) 
            time_duration = time(hour=hours, minute=minutes)
        else:
            time_duration = None

        total_attempts = int(total_attempts) if total_attempts else None
        lecture_id = int(lecture_id) if lecture_id else None

        new_quiz = Quiz(
            release_date=release_date,
            deadline=deadline,
            time_duration=time_duration,
            total_attempts=total_attempts,
            chapter_id=chapter_id,
            lecture_id=lecture_id
        )     

        db.session.add(new_quiz)
        db.session.commit()

        chapter = Chapter.query.get(chapter_id)
        subject_id = chapter.that_chap_sub.id
        return redirect(f"/admin_module/{subject_id}")

@app.route("/modify_quiz/<int:quiz_id>", methods=["GET", "POST"])
def modify_quiz(quiz_id):
    if request.method == 'GET':
        quiz=Quiz.query.filter_by(id=quiz_id).first()
        if quiz:
            chapter_id = quiz.chapter_id  # OR chapter_id = quiz.thatquizchapter.id
            print("cccccccccccc", chapter_id)
            lectures = Lecture.query.filter_by(chapter_id=chapter_id).all()
            # Convert SQLAlchemy object to dictionary
            quiz_data = {
                "id": quiz.id,
                "release_date": quiz.release_date.isoformat(),
                "deadline": quiz.deadline.isoformat() if quiz.deadline else None,
                "time_duration": str(quiz.time_duration) if quiz.time_duration else None,  # Convert time to string
                "total_attempts": quiz.total_attempts if quiz.total_attempts else None,
                "all_lectures": [
                    {
                        "id": lecture.id,
                        "name": lecture.name,
                        "link": lecture.link
                    } for lecture in lectures
                ],
                "selected_lecture": quiz.lecture_id
                }

            #  isoformat(): Converts datetime objects into a JSON-friendly string format (YYYY-MM-DDTHH:MM:SS).
            # str(quiz.time_duration): Converts datetime.time into "HH:MM:SS", making it serializable.
            # str(datetime_object) will return "YYYY-MM-DD HH:MM:SS" (which is readable but not strictly JSON standard).
            # str(time_object) will return "HH:MM:SS" (which works fine).
            print("Quiz DATA",jsonify(quiz_data))
            return jsonify(quiz_data)
        else:
            return jsonify({"error": "Subject not found"}), 404

    if request.method == 'POST' :
        quiz = Quiz.query.get(quiz_id)
        if quiz:
            release_date_str = request.form['mod_release_date']  # '2025-03-07T10:07'
            deadline_str = request.form['mod_deadline']  # '2025-03-08T10:07'
            total_attempts = request.form['mod_total_attempts'] 

            # # in this case  20:02:00 (don't know why it comes in HH:MM:SS IN SS=00 FORMAT INSTEAD OF ONLY HH:MM)
            # time_duration_str = request.form['mod_time_duration']  # 14:07:00 instead of '14:07' (hh:mm)
            # # #So we have to remove extra SS
            # time_duration_str = time_duration_str[:len(time_duration_str)-3]    # '14:07'
            # print("time_duration", type(time_duration_str), time_duration_str)

            time_duration_str = request.form['mod_time_duration']
            """
            1. assigning value first time in quiz modify form to "time_duration" field gives value in HH:MM
            2. but updating value of "time_duration" field in quiz modify form gives value in HH:MM:SS where SS is always 00
            """

            lecture_id = request.form.get('mod_oneLecture', None)

            release_date = datetime.strptime(release_date_str, "%Y-%m-%dT%H:%M")
            deadline = datetime.strptime(deadline_str, "%Y-%m-%dT%H:%M") if deadline_str else None
            if time_duration_str:
                if len(time_duration_str) > 5:
                    time_duration_str = time_duration_str[:len(time_duration_str)-3]
                hours, minutes = map(int, time_duration_str.split(":")) 
                time_duration = time(hour=hours, minute=minutes)
            else:
                time_duration = None

            total_attempts = int(total_attempts) if total_attempts else None
            lecture_id = int(lecture_id) if lecture_id else None

            quiz.release_date = release_date
            quiz.deadline = deadline
            quiz.time_duration = time_duration
            quiz.total_attempts = total_attempts
            quiz.lecture_id = lecture_id
            

            db.session.commit()

            chapter = quiz.thatquizchapter
            subject_id = chapter.that_chap_sub.id
            return redirect(f"/admin_module/{subject_id}")
        return render_template("notfound.html")  





















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


@app.route("/user_test")
def user_test():
    return render_template("testttttt.html")

@app.route("/user_test1")
def user_test1():
    return render_template("user/1user_module.html")