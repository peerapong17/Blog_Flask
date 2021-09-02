from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, PasswordField


class RegisForm(FlaskForm):
    username = StringField('Username', [validators.data_required(
    ), validators.Length(min=4, message="Username should be at least 4 characters long")])
    email = StringField(
        'Email', [validators.data_required(), validators.Email()])
    password = PasswordField(
        'Password',  [validators.data_required(), validators.length(min=6, message="Password should be at least 6 characters long")])
    confirm = PasswordField(
        'ConfirmPassword', [validators.data_required(), validators.equal_to("password", message="Password does't match")])
    submit = SubmitField("Register")

    # def check_email(self, field):
    #     if User.query.filter_by(email=field).first():
    #         flash("Your email have been already registered!")


class LoginForm(FlaskForm):
    email = StringField(
        'Email', [validators.data_required(), validators.Email()])
    password = PasswordField(
        'Password',  [validators.data_required()])
    submit = SubmitField("Register")


class InfoForm(FlaskForm):
    firstName = StringField('FirstName', [validators.data_required(
    ), validators.Length(min=6, message="Password should be at least 6 characters long")])
    lastName = StringField(
        'LastName', [validators.data_required(), validators.Length(min=4, max=25)])
    submit = SubmitField("OK")
