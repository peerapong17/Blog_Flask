import os
from models import User, Blog, Comment
from __init__ import app, db, basedir
from forms import LoginForm, RegisForm, BlogForm, InfoForm
from flask_login import login_user, login_required, logout_user, current_user
from flask import redirect, render_template, url_for, request, flash
from werkzeug.utils import secure_filename
from flask_wtf.file import FileField
from flask_wtf import FlaskForm

# categories = ["Travel", "Food", "Culture", "Tradition"]
blogs = Blog.query.all()
foodLength = len([a for a in blogs if a.category == "fd"])
travelLength = len([a for a in blogs if a.category == "trv"])
cultureLength = len([a for a in blogs if a.category == "cul"])
traditionLength = len([a for a in blogs if a.category == "tra"])
categories = [{"name": "Travel", "length": travelLength},
              {"name": "Food", "length": foodLength}, {"name": "Culture", "length": cultureLength}, {"name": "Tradition", "length": traditionLength}]


class UploadForm(FlaskForm):
    file = FileField()


@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
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
            login_user(user, remember=True)
            next = request.args.get('next')
            if next == None or not next[0] == '/':
                next = url_for('home')
            return redirect(next)
    return render_template("auth/login.html", form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisForm()
    if request.method == 'POST' and form.validate_on_submit():
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


@app.route("/blog")
@login_required
def home():
    blogs = Blog.query.all()
    return render_template("blog/home.html", blogs=blogs, categories=categories)


@app.route("/blog/<blog_category>")
@login_required
def blogFilteredByCategory(blog_category):
    category = ''
    if blog_category == "Travel":
        category = "trv"
    elif blog_category == "Food":
        category = "fd"
    elif blog_category == "Culture":
        category = "cul"
    else:
        category = "tra"
    blogs = Blog.query.filter_by(category=category).all()
    return render_template("blog/home.html", blogs=blogs, categories=categories)


@app.route("/create-blog", methods=["GET", "POST"])
@login_required
def createBlog():
    form = BlogForm()
    formFile = UploadForm()
    if request.method == 'POST' and form.validate_on_submit():
        filename = secure_filename(formFile.file.data.filename)
        formFile.file.data.save(os.path.join(
            basedir, app.config['UPLOAD_FOLDER'], filename))
        image_url = url_for('static', filename='uploads/' + filename)
        blog = Blog(userId=current_user.id, title=form.title.data,
                    content=form.content.data, image=image_url, category=form.category.data, username=current_user.username)
        db.session.add(blog)
        db.session.commit()
        form.title.data = ''
        form.content.data = ''
        flash("Blog created successfully", "success")

    return render_template("blog/create_blog.html", form=form, formFile=formFile)


@ app.route("/blog-detail/<blogId>")
@ login_required
def blogDetail(blogId):
    blog = Blog.query.filter_by(id=blogId).first()
    comments = Comment.query.filter_by(blogId=blogId).all()
    return render_template("blog/blog_detail.html", blog=blog, comments=comments)


@ app.route("/blog/delete/<blogId>")
@ login_required
def deleteBlog(blogId):
    blog = Blog.query.filter_by(id=blogId).first()
    db.session.delete(blog)
    db.session.commit()
    flash("Blog deleted", "sucess")
    return redirect(url_for("userBlog"))


@ app.route("/blog/update/<blogId>", methods=["GET", "POST"])
@ login_required
def updateBlog(blogId):
    formFile = UploadForm()
    blog = Blog.query.filter_by(id=blogId).first()
    category = ''
    if blog.category == "trv":
        category = "Travel"
    elif blog.category == "fd":
        category = "Food"
    elif blog.category == "cul":
        category = "Culture"
    else:
        category = "Tradition"
    form = BlogForm(title=blog.title, content=blog.content, category=category)

    if request.method == "POST" and form.validate_on_submit():
        filename = secure_filename(formFile.file.data.filename)
        formFile.file.data.save(os.path.join(
            basedir, app.config['UPLOAD_FOLDER'], filename))
        image_url = url_for('static', filename='uploads/' + filename)
        blog.title = form.title.data
        blog.content = form.content.data
        blog.category = form.category.data
        blog.image = image_url
        db.session.add(blog)
        db.session.commit()
        flash("Blog updated successfully", "success")
        return redirect(url_for('userBlog'))
    return render_template("blog/update_blog.html", form=form, blog=blog, formFile=formFile)


@ app.route("/comment/<blogId>", methods=["GET", "POST"])
@ login_required
def addComment(blogId):
    comment = Comment(
        blogId=blogId, userId=current_user.id, username=current_user.username, comment=request.args.get('comment'))
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('blogDetail', blogId=blogId))


@ app.route("/user-blog")
@ login_required
def userBlog():
    blogs = Blog.query.filter_by(userId=current_user.id).all()
    return render_template("blog/user_blog.html", blogs=blogs)


@ app.route("/user-information", methods=["GET", "POST"])
@ login_required
def userInformation():
    form = InfoForm()
    fname = False
    lname = False
    if request.method == 'POST' and form.validate_on_submit():
        fname = form.firstName.data
        lname = form.lastName.data
    return render_template("blog/information.html", form=form, fname=fname, lname=lname)


@ app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
