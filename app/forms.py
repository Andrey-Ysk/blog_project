from wtforms import Form, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from wtforms.widgets import TextArea


class SignInForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(Form):
    email = StringField('email', validators=[Email()])
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    repeat_password = PasswordField('repeat_password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class CommentForm(Form):
    comment_text = StringField(widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField('Send')