from flask import Flask, render_template, request, redirect, url_for
from wtforms import Form, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
import os


basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SECRET_KEY'] = '62wtyds6t36qf48u4h3256'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    posts = db.relationship('Post', backref='user')
    comments = db.relationship('Comment', backref='user')

    def __repr__(self):
        return '<User %r>' % self.username


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.DateTime)
    title = db.Column(db.String(64))
    rating = db.Column(db.Integer)
    comments = db.relationship('Comment', backref='post')

    def __repr__(self):
        return '<Post %r>' % self.title


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(256))
    date = db.Column(db.DateTime)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Comment %r' % self.text


# PostRating = db.Table('posts_rating',
#     db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
#     db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
# )


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    email = None
    password = None
    form = SignInForm(request.form)

    if form.validate():
        email = form.email.data
        password = form.password.data
        return redirect(url_for('signin'))

    form.email.data = ''
    form.password.data = ''

    return render_template('signin.html', form=form, email=email, password=password)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    email = None
    username = None
    password = None
    repeat_password = None
    form = RegistrationForm(request.form)

    if form.validate():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        repeat_password = form.repeat_password.data
        return redirect(url_for('registration'))

    form.email.data = ''
    form.username.data = ''
    form.password.data = ''
    form.repeat_password.data = ''

    return render_template('registration.html', form=form, email=email, username=username, password=password, repeat_password=repeat_password)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
