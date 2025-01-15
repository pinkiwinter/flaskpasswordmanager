import pytest
import os
from werkzeug.security import generate_password_hash
from app import create_app, db
from app.models import User, UserAccount
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture
def app():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_DATABASE_URL')
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = os.getenv('TEST_JWT_SECRET_KEY')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def clean_database():
    yield
    for table in reversed(db.metadata.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()


@pytest.fixture()
def user():
    hashed_password = generate_password_hash('password123!')
    user = User(email='user@example.com', master_password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def user_access_token(client, user):
    response = client.post('/login', json={'email': 'user@example.com', 'master_password': 'password123!'})
    assert response.status_code == 200
    assert 'access_token' in response.json

    access_token = response.json['access_token']
    return access_token

@pytest.fixture
def user_account(client, user):
    user_account = UserAccount(service='service', username='username', email='user@email.com', password='password')
    db.session.add(user_account)
    db.session.commit()
    return user_account



