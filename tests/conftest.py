from app.models import User, Post, Comment
from app import create_app, db
import pytest


app = create_app('config.TestingConfig')


def login(client, username, password):
    return client.post('/signin', data = dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


@pytest.fixture(scope='session')
def new_user():
    user = User(username='user_test24', email='testuser21@gmail.com', confirmed=True)
    user.set_password('testpassword')
    return user


@pytest.fixture(scope='session')
def new_post():
    new_post = Post(user_id=1, content='Test text', title='Title text')
    return new_post


@pytest.fixture(scope='session')
def test_client():

    with app.test_client() as test_client:
        with app.app_context():
            db.create_all()
            fill_test_database()
            yield test_client
            db.drop_all()


def fill_test_database():
    user = User(username='Test1', confirmed=True)
    user.set_password('12345678')
    db.session.add(user)
    db.session.flush()

    post = Post(content='Test post content', user_id=user.id, title='Test title')
    db.session.add(post)
    db.session.flush()

    comment = Comment(text='test comment text', user_id=user.id, post_id=post.id)
    db.session.add(comment)
    db.session.flush()

    db.session.commit()