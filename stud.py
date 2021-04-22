from flask import Flask,render_template,flash, redirect,url_for,session,logging,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
app = Flask(__name__)
app.secret_key="project123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users1.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
admin=Admin(app)





headings = ("Day", "1", "2", "3", "4", "5", "6")

data = (
    ("Monday", "MM", "GTC","SS","ASDL","ASDL","ASDL"),
    ("Tuesday", "GTC", "GTC","SC","TOC","MM","DC"),
    ("Wednesday", "SC", "SS","GTC","MM","TOC","DP"),
    ("Thursday", "SS", "GTC","SC","TOC","DC","DC"),
    ("Friday", "TOC", "DC","SS","SSL","SSDL","SSL"),
)



class student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    dob = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))
    attendance = db.relationship('attendance', backref='back1', lazy=True)
    marks = db.relationship('marks', backref='back2', lazy=True)



class attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(80))
    date =  db.Column(db.DateTime)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'),nullable=False)

class marks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mark=db.Column(db.Integer,nullable=False)
    subject = db.Column(db.String(100))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'),nullable=False)


admin.add_view(ModelView(student,db.session))
admin.add_view(ModelView(marks,db.session))
admin.add_view(ModelView(attendance,db.session))




class staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100))
    password=db.Column(db.String(100))
    email=db.Column(db.String(100))
admin.add_view(ModelView(staff,db.session))

@app.route("/afterstudentlogin",methods=["GET", "POST"])
def afterstudentlogin():
    if "studentname" in session:
        studentname=session["studentname"].title()
        return render_template("afterstudentlogin.html",content=studentname)
    if "studentname" not in session:
        return redirect(url_for("login"))




@app.route("/timetable")
def timetable():
    return render_template("tt.html", headings= headings, data=data)

@app.route("/acedamiccalender")
def acedamiccalender():
    return render_template("cal1.html")

@app.route("/staffacedamiccalender")
def staffacedamiccalender():
    return render_template("cal.html")



@app.route("/studentprofile",methods=["GET", "POST"])
def studentprofile():
    sname=session["studentname"]
    passw = session["passs"]
    found_user=student.query.filter_by(name=sname,password=passw).first()
    if found_user:
        idd=found_user.id
        session["id"]=idd
        em=found_user.email
        ne=sname.title()
        db=found_user.dob
        return render_template("studentprofile.html",name=ne,email=em,dob=db,id=session["id"])

@app.route("/viewattendance")
def viewattendance():
    namee = session["studentname"]
    passwo = session["passs"]
    idd = session["id"]
    attview = attendance.query.filter_by(student_id=idd).all()

    return render_template("attendanceview.html",att=attview)

@app.route("/logout")
def logout():
    return redirect(url_for("login"))

@app.route("/viewmarklist")
def viewmarklist():
    namee = session["studentname"]
    passwo = session["passs"]
    idd = session["id"]
    markview = marks.query.filter_by(student_id=idd).all()

    return render_template("viewmarks.html",maark=markview)


@app.route("/")
def index():
    return render_template("home.html")





@app.route("/stafflogin",methods=["GET", "POST"])
def stafflogin():
    if request.method == "POST":
        staffuname = request.form["staffuname"]
        staffpassw = request.form["staffpassw"]
        session["staffpasss"]=staffpassw

        login = staff.query.filter_by(name=staffuname, password=staffpassw).first()
        if login is not None:
            session["staffname"]=staffuname
            return redirect(url_for("afterstafflogin"))
        else:
            return redirect(url_for("staffregister"))
    return render_template("stafflogin.html")

@app.route("/staffregister", methods=["GET", "POST"])
def staffregister():
    if request.method == "POST":
        staffuname = request.form['staffuname']
        staffmail = request.form['staffmail']
        staffpassw = request.form['staffpassw']


        registers = staff(name = staffuname, email = staffmail, password = staffpassw,)
        db.session.add(registers)
        db.session.commit()

        return redirect(url_for("stafflogin"))
    return render_template("staffregister.html")


@app.route("/afterstafflogin",methods=["GET", "POST"])
def afterstafflogin():
    if "staffname" in session:
        staffname=session["staffname"].title()
        return render_template("afterstafflogin.html",content=staffname)
    if "staffname" not in session:
        return redirect(url_for("stafflogin"))






@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]
        session["passs"]=passw

        login = student.query.filter_by(name=uname, password=passw).first()
        if login is not None:
            session["studentname"]=uname
            return redirect(url_for("afterstudentlogin"))
        else:
            return redirect(url_for("register"))
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']
        dobb = request.form['dob']
        dobb=str(dobb)
        register = student(name = uname, dob = dobb, email = mail, password = passw,)
        db.session.add(register)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("register.html")

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
