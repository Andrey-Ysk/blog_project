from wtforms import Form, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from wtforms.fields.html5 import EmailField
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField


class SignInForm(Form):
    username = StringField('username', validators=[DataRequired(), Length(min=4, max=32)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Log In')


class RegistrationForm(Form):
    email = EmailField('email', validators=[Email()])
    username = StringField('username', validators=[DataRequired(), Length(min=4, max=32)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8)])
    repeat_password = PasswordField('repeat_password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Sign Up')


class CommentForm(Form):
    comment_text = StringField(widget=TextArea(), validators=[DataRequired(), Length(max=256)])
    submit = SubmitField('Send')


class PostForm(Form):
    title = StringField('Title', widget=TextArea(), validators=[DataRequired(), Length(max=64)])
    body = CKEditorField('Body', validators=[DataRequired(), Length(max=4096)])
    submit = SubmitField('Submit')
