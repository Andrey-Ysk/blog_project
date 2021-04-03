from tests.conftest import login, logout, app


def test_index_page(test_client):
    """
    GIVEN: Flask app with test conf
    WHEN: '/' page request
    THEN: check valid response
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"BLOG" in response.data
    assert b"Sign-In" in response.data
    assert b"Registration" in response.data


def test_signin_page(test_client):
    """
    GIVEN: Flask app with test conf
    WHEN: /signin page request
    THEN: check valid response
    """
    response = test_client.get('/signin')
    assert response.status_code == 200
    assert b"Log In" in response.data
    assert b"Username" in response.data
    assert b"Password" in response.data
    assert b"Forgot password?" in response.data


def test_registration_page(test_client):
    """
    GIVEN: Flask app with test conf
    WHEN: /registration page request
    THEN: check valid response
    """
    response = test_client.get('/registration')
    assert response.status_code == 200
    assert b"Registration" in response.data
    assert b"Email" in response.data
    assert b"Username" in response.data
    assert b"Password" in response.data
    assert b"Repeat password" in response.data
    assert b"Sign Up" in response.data


def test_post_full_page(test_client):
    """
    GIVEN: Flask app with test conf
    WHEN: /post/* page request
    THEN: check valid response
    """
    response = test_client.get('/post/1')
    assert response.status_code == 200
    assert b"Test post content" in response.data
    assert b"Test title" in response.data


def test_post_comment(test_client):
    """
    GIVEN: Flask app with test conf
    WHEN: /post/* comment section page request
    THEN: check valid response
    """
    response = test_client.get('/post/1')
    assert response.status_code == 200
    assert b"test comment text" in response.data


def test_add_post_auth(test_client):
    """
    GIVEN: Flask app with test conf
    WHEN: '/' on login/logout user
    THEN: "Add post" visible on login, hide on logout
    #TODO: add_post only confirmed USER access
    """
    rv = login(test_client, app.config['USERNAME'], app.config['PASSWORD'])
    assert b"Add post" in rv.data

    rv = logout(test_client)
    assert b"Add post" not in rv.data


def test_add_post(test_client):
    """
    GIVEN: Flask app with test conf
    WHEN: '/add_post' POST method with data, login/logout
    THEN: check possible to add post login user, cant add on logout
    """
    login(test_client, app.config['USERNAME'], app.config['PASSWORD'])
    rv = test_client.post('/add_post', data=dict(
        title='Hello',
        body='World'
    ), follow_redirects=True)
    assert b"Hello" in rv.data
    assert b"World" in rv.data

    logout(test_client)
    rv = test_client.post('/add_post', data=dict(
        title='NOTHello',
        body='NOTWorld'
    ), follow_redirects=True)
    assert b"NOTHello" not in rv.data
    assert b"NOTWorld" not in rv.data


def test_post_vote(test_client):
    """
    GIVEN: Flask app with test conf
    WHEN: '/post_full' rating section, valid rating count and message - login "vote up"/"vote up" after vote/logout vote
    THEN: vote == 1 without message/error message "already vote"/error message "need login"
    """
    login(test_client, app.config['USERNAME'], app.config['PASSWORD'])
    res = test_client.get('/post_full_vote', query_string=dict(vote='up'))
    assert b"\"rating\": 1" in res.data

    res = test_client.get('/post_full_vote', query_string=dict(vote='up'))
    assert b"You already rate this post" in res.data

    logout(test_client)
    rv = test_client.get('/post_full_vote')
    assert b"You need login for rate this post" in rv.data
