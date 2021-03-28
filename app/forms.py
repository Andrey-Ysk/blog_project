from wtforms import Form, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from wtforms.fields.html5 import EmailField
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField


class SignInForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(Form):
    email = EmailField('email', validators=[Email()])
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    repeat_password = PasswordField('repeat_password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class CommentForm(Form):
    comment_text = StringField(widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField('Send')


class PostForm(Form):
    title = StringField('Title', widget=TextArea(), validators=[DataRequired()])
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField('Submit')