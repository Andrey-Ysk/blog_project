from tests.conftest import login, logout, app
from app.models import User


def test_registration_new_user(test_client):
    """
    GIVEN: Flask app with test conf
    WHEN: /registration page registration new user and confirm
    THEN: user registered, user login, user confirmed
    """
    response = test_client.post('/registration', data=dict(
        username = 'Test4',
        email = 'testemailTest4@test4.com',
        password = 12345678,
        repeat_password = 12345678
    ))
    assert response.status_code == 302

    response = login(test_client, 'Test4', 12345678)
    assert b"A confirmation email has been send to you by email" in response.data
    assert b"Test4" in response.data
    assert b"Log-out" in response.data

    user = User.query.filter_by(email='testemailTest4@test4.com').first()
    token = user.generate_confirmation_token().decode("utf-8")
    response = test_client.get('/confirm/{}'.format(token),
                               follow_redirects=True)
    assert response.status_code == 200
    assert b"You have confirm your account!" in response.data


def test_login_logout(test_client):
    """
    GIVEN: Flask app with test conf
    WHEN: '/' page with login/logout + login with invalid username, password
    THEN: check valid response + signin error
    """
    rv = login(test_client, app.config['USERNAME'], app.config['PASSWORD'])
    assert b"BLOG" in rv.data
    assert b"Log-out" in rv.data
    assert b'You have entered incorrect username or password' not in rv.data

    rv = logout(test_client)
    assert b"BLOG" in rv.data
    assert b"Sign-In" in rv.data
    assert b"Registration" in rv.data
    assert b"You have entered incorrect username or password" not in rv.data

    rv = login(test_client, app.config['USERNAME'] + 'x', app.config['PASSWORD'])
    assert b"You have entered incorrect username or password" in rv.data

    rv = login(test_client, app.config['USERNAME'], app.config['PASSWORD'] + 'x')
    assert b"You have entered incorrect username or password" in rv.data