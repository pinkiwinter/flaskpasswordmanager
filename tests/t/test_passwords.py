from app.models import UserAccount

def test_add_account(client, user, user_access_token):
    response = client.post('/accounts/add', headers={'Authorization': f'Bearer {user_access_token}'}, json={'service': 'example_service', 'username': 'example_username', 'email': 'example@email.com', 'password': 'example_password'})
    assert response.status_code == 201

    account = UserAccount.query.filter_by(user_id=user.id, service='example_service').first()
    assert account is not None

def test_get_accounts(client, user_access_token):
    response = client.get('/accounts', headers={'Authorization': f'Bearer {user_access_token}'})
    assert response.status_code == 200