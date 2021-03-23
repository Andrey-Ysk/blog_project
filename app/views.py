from app import app
from flask import render_template, request, redirect, url_for, make_response, session, flash
from .forms import SignInForm, RegistrationForm, CommentForm
from .models import Role, User, Post, Comment, PostRating
from flask_login import login_required, login_user, current_user, logout_user
from app import db


@app.route('/')
def index():
    all_posts = Post.query.all()
    return render_template('index.html', all_posts=all_posts)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_full(post_id):
    post = Post.query.all()[post_id - 1]
    comments_list = Comment.query.filter_by(post_id=post_id).all()
    form = CommentForm(request.form)

    if form.validate():
        comment_text = form.comment_text.data
        return redirect(url_for('post_full'))

    form.comment_text.data = ''

    return render_template('post_full.html', form=form, post=post, comments_list=comments_list)


@app.route('/signin', methods=['GET', 'POST'])
def signin():

    form = SignInForm(request.form)

    if form.validate():
        username = db.session.query(User).filter(User.username == form.username.data).first()
        if username and username.check_password(form.password.data):
            login_user(username)
            return redirect(url_for('index'))

        else:
            flash('You have entered incorrect username or password')

        return redirect(url_for('signin'))

    form.username.data = ''
    form.password.data = ''

    #TODO: validate data

    return render_template('signin.html', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm(request.form)

    # TODO: validate data
    # TODO: if refactoring

    if form.validate():
        if form.password.data != form.repeat_password.data:
            flash('Your password and repeat password do not match')
            return redirect(url_for('registration'))

        if len(form.password.data) < 8:
            flash('Password must be of minimum 8 characters length')
            return redirect(url_for('registration'))

        if len(form.username.data) < 4:
            flash('Username must be of minimum 4 characters length')
            return redirect(url_for('registration'))

        if db.session.query(User).filter(User.email == form.email.data).first():
            flash('This email already taken')
            return redirect(url_for('registration'))

        if db.session.query(User).filter(User.username == form.username.data).first():
            flash('This username already taken')
            return redirect(url_for('registration'))

        new_user = User(email=form.email.data, username=form.username.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('index'))

    form.email.data = ''
    form.username.data = ''
    form.password.data = ''
    form.repeat_password.data = ''

    return render_template('registration.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500