from app import app
from flask import render_template, request, redirect, url_for, make_response, session
from .forms import SignInForm, RegistrationForm
from .models import Role, User, Post, Comment, PostRating


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