from flask import Flask, redirect, render_template, url_for, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from blog import blog

app = Flask(__name__)
app.secret_key = "my little secrets"
app.permanent_session_lifetime = timedelta(days=30)
app.register_blueprint(blog, url_prefix="/blog")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("blog.home"))
    else:
        return redirect(url_for("login"))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        if "user" in session:
            return redirect(url_for("blog.home"))
        else:
            return render_template("auth/login.html")
    else:
        session.permanent = True
        email = request.form['email']
        password = request.form['password']
        found_email = User.query.filter_by(email=email).first()
        found_password = User.query.filter_by(password=password).first()
        print(found_email, found_password)
        if found_email == None:
            flash("Email is invalid", "error")
            return render_template("auth/login.html")
        elif found_password == None:
            flash("password is invalid", "error")
            return render_template("auth/login.html")
        session['user'] = email
        return redirect(url_for("blog.home"))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        if "user" in session:
            return redirect(url_for("blog.home"))
        else:
            return render_template("auth/register.html")
    else:
        db.create_all()
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        found_user = User.query.filter_by(email=email).first()
        if found_user:
            flash("This email already exist!", "error")
        elif len(password) < 6:
            flash("Password should be at least 6 characters!", "error")
        else:
            user = User(username, email, password)
            db.session.add(user)
            db.session.commit()
            flash("Create account success!", "success")
        return render_template("auth/register.html")


@app.route("/get-user")
def getUser():
    # allUser = User.query.all()
    found_user = User.query.filter_by(email="test@gmail.com").first()
    return f"this is all user found:{found_user.email} {found_user.username}"


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
