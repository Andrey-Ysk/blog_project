from app import app
from flask import render_template, request, redirect, url_for, make_response, session
from .forms import SignInForm, RegistrationForm, CommentForm
from .models import Role, User, Post, Comment, PostRating
from flask_login import login_required, login_user, current_user, logout_user
from app import db


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/post/<post_id>', methods=['GET', 'POST'])
def post_full(post_id):
    comment_text = None
    form = CommentForm(request.form)

    if form.validate():
        comment_text = form.comment_text.data
        return redirect(url_for('post_full'))

    form.comment_text.data = ''

    return render_template('post_full.html', form=form, comment_text=comment_text)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    username = None
    password = None
    form = SignInForm(request.form)

    if form.validate():
        username = db.session.query(User).filter(User.username == form.username.data).first()
        if username and username.check_password(form.password.data):
            login_user(username)
            return redirect(url_for('index'))

        return redirect(url_for('signin'))

    form.username.data = ''
    form.password.data = ''
    #TODO: flash error signin
    #TODO: validate data
    return render_template('signin.html', form=form, username=username, password=password)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    email = None
    username = None
    password = None
    repeat_password = None
    form = RegistrationForm(request.form)

    # TODO: validate data

    if form.validate():
        if password != repeat_password:
            pass
            #TODO: flash error

        if db.session.query(User).filter(User.email == form.email.data).first():
            pass
            #TODO: flash error

        if db.session.query(User).filter(User.username == form.username.data).first():
            pass
            #TODO: flash error

        new_user = User(email=form.email.data, username=form.username.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()

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