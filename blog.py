# from forms import BlogForm, InfoForm
# from flask_login import login_required
# from flask import render_template, Blueprint, request, flash
# from models import Blog
# from __init__ import db

# blog = Blueprint("blog", __name__, static_folder="static",
#                  template_folder="templates")



# @blog.route("/")
# @login_required
# def home():
#     return render_template("blog/home.html")


# @blog.route("/create-blog", methods=["GET", "POST"])
# @login_required
# def createBlog():
#     form = BlogForm()
#     if request.method == "POST":
#         blog = Blog(title=form.title.data, content=form.content.data)
#         db.session.add(blog)
#         db.session.commit()
#         flash("Blog created successfully")

#     return render_template("blog/create_blog.html", form=form)


# @blog.route("/user-blog")
# @login_required
# def userBlog():
#     return render_template("blog/user_blog.html")


# @blog.route("/user-information", methods=["GET", "POST"])
# @login_required
# def userInformation():
#     form = InfoForm()
#     fname = False
#     lname = False
#     if request.method == 'POST' and form.validate_on_submit():
#         fname = form.firstName.data
#         lname = form.lastName.data
#     return render_template("blog/information.html", form=form, fname=fname, lname=lname)
