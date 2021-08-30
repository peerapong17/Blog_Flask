from flask import render_template, session, Blueprint, redirect, url_for

blog = Blueprint("blog", __name__,static_folder="static", template_folder="templates")

@blog.route("/")
def home():
    if "user" in session:
        return render_template("blog/home.html", user=session['user'])
    else:
        return redirect(url_for("login"))

@blog.route("/create-blog")
def createBlog():
    if "user" in session:
        return render_template("blog/create_blog.html")
    else:
        return redirect(url_for("login"))


@blog.route("/user-blog")
def userBlog():
    if "user" in session:
        return render_template("blog/user_blog.html")
    else:
        return redirect(url_for("login"))