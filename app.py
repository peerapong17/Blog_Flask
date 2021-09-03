from models import User, Blog, Comment
from __init__ import app, db
from forms import LoginForm, RegisForm, BlogForm, InfoForm
from flask_login import login_user, login_required, logout_user, current_user
from flask import redirect, render_template, url_for, request, flash


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
def home():
    blogs = Blog.query.all()
    return render_template("blog/home.html", blogs=blogs)


@app.route("/create-blog", methods=["GET", "POST"])
@login_required
def createBlog():
    form = BlogForm()
    if request.method == 'POST' and form.validate_on_submit():
        blog = Blog(userId=current_user.id, title=form.title.data,
                    content=form.content.data)
        db.session.add(blog)
        db.session.commit()
        form.title.data = ''
        form.content.data = ''
        flash("Blog created successfully", "success")

    return render_template("blog/create_blog.html", form=form)


@app.route("/blog-detail/<blogId>")
@login_required
def blogDetail(blogId):
    blog = Blog.query.filter_by(id=blogId).first()
    comments = Comment.query.filter_by(blogId=blogId).all()
    return render_template("blog/blog_detail.html", blog=blog, comments=comments)


@app.route("/blog/delete/<blogId>")
@login_required
def deleteBlog(blogId):
    blog = Blog.query.filter_by(id=blogId).first()
    db.session.delete(blog)
    db.session.commit()
    flash("Blog deleted", "sucess")
    return redirect(url_for("userBlog"))


@app.route("/blog/update/<blogId>", methods=["GET", "POST"])
@login_required
def updateBlog(blogId):
    blog = Blog.query.filter_by(id=blogId).first()
    form = BlogForm(title=blog.title, content=blog.content)
    if request.method == "POST":
        blog.title = form.title.data
        blog.content = form.content.data
        db.session.add(blog)
        db.session.commit()
        flash("Blog updated successfully", "success")
        return redirect(url_for('userBlog'))
    return render_template("blog/update_blog.html", form=form, blog=blog)


@app.route("/comment/<blogId>", methods=["GET", "POST"])
@login_required
def addComment(blogId):
    comment = Comment(
        blogId=blogId, userId=current_user.id, username=current_user.username, comment=request.args.get('comment'))
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('blogDetail', blogId=blogId))


@app.route("/user-blog")
@login_required
def userBlog():
    blogs = Blog.query.filter_by(userId=current_user.id).all()
    return render_template("blog/user_blog.html", blogs=blogs)


@app.route("/user-information", methods=["GET", "POST"])
@login_required
def userInformation():
    form = InfoForm()
    fname = False
    lname = False
    if request.method == 'POST' and form.validate_on_submit():
        fname = form.firstName.data
        lname = form.lastName.data
    return render_template("blog/information.html", form=form, fname=fname, lname=lname)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
