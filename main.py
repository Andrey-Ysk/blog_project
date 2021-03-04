from flask import Flask, render_template, request, session, redirect, url_for
from wtforms import Form, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


app = Flask(__name__)
app.config['SECRET_KEY'] = '62wtyds6t36qf48u4h3256'

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
        form.email.data = ''
        form.password.data = ''
        return redirect(url_for('signin'))
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
        form.email.data = ''
        form.username.data = ''
        form.password.data = ''
        form.repeat_password.data = ''
        return redirect(url_for('registration'))
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
