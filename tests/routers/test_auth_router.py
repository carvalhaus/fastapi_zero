from http import HTTPStatus


def test_login(client, user):
    response = client.post(
        '/login',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_login_incorrect_email(client, user):
    response = client.post(
        '/login',
        data={
            'username': user.email,
            'password': 'incorrect',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_login_incorrect_password(client, user):
    response = client.post(
        '/login',
        data={
            'username': 'incorrect@test.com',
            'password': user.clean_password,
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}
