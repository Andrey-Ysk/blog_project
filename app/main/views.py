from app import db
from . import main
from .forms import SignInForm, RegistrationForm, CommentForm, PostForm
from flask import render_template, request, redirect, url_for, session, flash, jsonify, current_app
from app.models import User, Post, Comment, PostRating
from flask_login import login_required, login_user, current_user, logout_user
from app.email import send_email


@main.route('/', methods=['GET'], defaults={"page": 1})
@main.route('/<int:page>', methods=['GET'])
def index(page):
    per_page = current_app.config['POST_PER_PAGE']
    posts = Post.query.order_by(Post.id.desc()).paginate(page, per_page, error_out=True)
    return render_template('index.html', posts=posts)


@main.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_full(post_id):
    session['post_id'] = post_id
    post = Post.query.get_or_404(post_id)
    comments_list = Comment.query.filter_by(post_id=post_id).all()
    form = CommentForm(request.form)
    # TODO: validate data
    if form.validate():
        new_comment = Comment(user_id=current_user.id, post_id=post_id, text=form.comment_text.data)
        db.session.add(new_comment)
        db.session.commit()
        form.comment_text.data = ''

        return redirect(url_for('.post_full', post_id=post_id))

    form.comment_text.data = ''

    return render_template('post_full.html', form=form, post=post, comments_list=comments_list)


@main.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    if not current_user.confirmed:
        return redirect(url_for('.index'))

    form = PostForm(request.form)

    # TODO: validate data
    if form.validate():
        new_post = Post(content=form.body.data, user_id=current_user.id, title=form.title.data)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('.index'))

    form.title.data = ''
    form.body.data = ''

    return render_template('add_post.html', form=form)


@main.route('/post_full_vote')
def post_full_vote():

    if not current_user.is_authenticated:
        return jsonify(alert='You need login for rate this post')

    post_id = session.get('post_id')
    user_vote_exist = db.session.query(PostRating).filter(PostRating.c.user_id == current_user.id,
                                                          PostRating.c.post_id == post_id).all()
    vote = request.args.get('vote')
    current_post = Post.query.get(post_id)

    if not user_vote_exist:

        if vote == 'up':
            current_post.rating += 1
            current_post.users.append(current_user)
            db.session.add(current_post)
            db.session.commit()
            return jsonify(rating=current_post.rating)

        if vote == 'down':
            current_post.rating -= 1
            current_post.users.append(current_user)
            db.session.add(current_post)
            db.session.commit()
            return jsonify(rating=current_post.rating)

    else:
        return jsonify(alert='You already rate this post')


@main.route('/signin', methods=['GET', 'POST'])
def signin():

    next_page = request.args.get('next')
    form = SignInForm(request.form)

    if form.validate():
        username = db.session.query(User).filter(User.username == form.username.data).first()
        if username and username.check_password(form.password.data):
            login_user(username)
            # fix view confirm login_requred lost next parameter
            if next_page:
                return redirect(next_page)

            return redirect(url_for('.index'))

        else:
            flash('You have entered incorrect username or password')

        return redirect(url_for('.signin'))

    form.username.data = ''
    form.password.data = ''

    # TODO: validate data

    return render_template('auth/signin.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.index'))


@main.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm(request.form)

    # TODO: validate data
    # TODO: if refactoring

    if form.validate():
        if form.password.data != form.repeat_password.data:
            flash('Your password and repeat password do not match')
            return redirect(url_for('.registration'))

        if len(form.password.data) < 8:
            flash('Password must be of minimum 8 characters length')
            return redirect(url_for('.registration'))

        if len(form.username.data) < 4:
            flash('Username must be of minimum 4 characters length')
            return redirect(url_for('.registration'))

        if db.session.query(User).filter(User.email == form.email.data).first():
            flash('This email already taken')
            return redirect(url_for('.registration'))

        if db.session.query(User).filter(User.username == form.username.data).first():
            flash('This username already taken')
            return redirect(url_for('.registration'))

        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()

        token = new_user.generate_confirmation_token()
        send_email(new_user.email, 'Confirm Your Account', 'auth/confirm', user=new_user, token=token)
        flash('A confirmation email has been send to you by email')

        return redirect(url_for('.index'))

    form.email.data = ''
    form.username.data = ''
    form.password.data = ''
    form.repeat_password.data = ''

    return render_template('auth/registration.html', form=form)


@main.route('/confirm/<token>', methods=['GET', 'POST'])
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('.index'))
    if current_user.confirm(token):
        flash('You have confirm your account!')
    else:
        flash('The confirmation link is invalid or expired')

    return redirect(url_for('.index'))


@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
