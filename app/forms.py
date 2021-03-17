from wtforms import Form, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


class SignInForm(Form):
    email = StringField('email', validators=[Email()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(Form):
    email = StringField('email', validators=[Email()])
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    repeat_password = PasswordField('repeat_password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')