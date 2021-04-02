from app.models import User


def test_new_user(new_user):
    """
    GIVEN: User model
    WHEN: new User created
    THEN: check name, email, password_hash, role defined correctly
    """
    token = new_user.generate_confirmation_token()

    assert new_user.username == 'user_test24'
    assert new_user.email == 'testuser21@gmail.com'
    assert new_user.password_hash != 'testpassword'
    assert User.check_password(new_user, 'testpassword')
    token = User.generate_confirmation_token(new_user)
    assert User.confirm(new_user, token)


def test_new_post(new_post):
    """
    GIVEN: User model
    WHEN: new Post created
    THEN: check user_id, content, title
    """
    assert new_post.user_id == 1
    assert new_post.content == 'Test text'
    assert new_post.title == 'Title text'
