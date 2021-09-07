# from forms import BlogForm
# from models import Blog, Comment
# from flask_login import login_required
# from flask import render_template, request, flash, Blueprint
# from models import Blog
# from __init__ import db
# from flask_login import login_required,  current_user
# from flask import redirect, render_template, url_for, request, flash
# from bluePrint import blog
# import json

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

# @blog.route("/blog")
# def home():
#     blogs = Blog.query.all()
#     return render_template("blog/home.html", blogs=blogs)


# @blog.route("/create-blog", methods=["GET", "POST"])
# @login_required
# def createBlog():
#     form = BlogForm()
#     if request.method == 'POST' and form.validate_on_submit():
#         blog = Blog(userId=current_user.id, title=form.title.data,
#                     content=form.content.data)
#         db.session.add(blog)
#         db.session.commit()
#         form.title.data = ''
#         form.content.data = ''
#         flash("Blog created successfully", "success")

#     return render_template("blog/create_blog.html", form=form)


# @blog.route("/blog-detail/<blogId>")
# @login_required
# def blogDetail(blogId):
#     blog = Blog.query.filter_by(id=blogId).first()
#     comments = Comment.query.filter_by(blogId=blogId).all()
#     return render_template("blog/blog_detail.html", blog=blog, comments=comments)


# @blog.route("/blog/delete/<blogId>")
# @login_required
# def deleteBlog(blogId):
#     blog = Blog.query.filter_by(id=blogId).first()
#     db.session.delete(blog)
#     db.session.commit()
#     flash("Blog deleted", "sucess")
#     return redirect(url_for("userBlog"))


# @blog.route("/blog/update/<blogId>", methods=["GET", "POST"])
# @login_required
# def updateBlog(blogId):
#     blog = Blog.query.filter_by(id=blogId).first()
#     form = BlogForm(title=blog.title, content=blog.content)
#     if request.method == "POST":
#         blog.title = form.title.data
#         blog.content = form.content.data
#         db.session.add(blog)
#         db.session.commit()
#         flash("Blog updated successfully", "success")
#         return redirect(url_for('userBlog'))
#     return render_template("blog/update_blog.html", form=form, blog=blog)


# @blog.route("/comment/<blogId>", methods=["GET", "POST"])
# @login_required
# def addComment(blogId):
#     data = json.loads(request.data)
#     comment = data['comment']
#     comment = Comment(
#         blogId=blogId, userId=current_user.id, username=current_user.username, comment=request.args.get('comment'))
#     db.session.add(comment)
#     db.session.commit()
#     return redirect(url_for('blogDetail', blogId=blogId))


# @blog.route("/user-blog")
# @login_required
# def userBlog():
#     blogs = Blog.query.filter_by(userId=current_user.id).all()
#     return render_template("blog/user_blog.html", blogs=blogs)
