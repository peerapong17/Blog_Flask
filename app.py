from models import User
from __init__ import app, db
from forms import LoginForm, RegisForm
from flask_login import login_user, login_required, logout_user, current_user
from flask import redirect, render_template, url_for, request, flash


@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("blog.home"))
    else:
        return redirect(url_for("login"))


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user == None:
            flash("Email is invalid", "error")
        elif not user.check_password(form.password.data):
            flash("Password is invalid", "error")
        elif user.check_password(form.password.data) and user is not None:
            login_user(user)
            next = request.args.get('next')
            if next == None or not next[0] == '/':
                next = url_for('blog.home')

            return redirect(next)
    return render_template("auth/login.html", form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisForm()
    if request.method == 'POST' and form.validate_on_submit():
        db.create_all()
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash("This email already exist!", "error")
        else:
            user = User(username=form.username.data,
                        email=form.email.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("Create account success!", "success")
            return redirect(url_for("login"))

    return render_template("auth/register.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
