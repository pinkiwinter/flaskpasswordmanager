from flask_sqlalchemy import SQLAlchemy
from .utils import decrypt_data, encrypt_data

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    master_password = db.Column(db.Text, nullable=False)

class UserAccount(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    service = db.Column(db.String(120), nullable=False)
    _username = db.Column(db.String(120), nullable=True, default=None)
    _email = db.Column(db.String(120), nullable=True, default=None)
    _password = db.Column(db.Text, nullable=False)

    @property
    def username(self):
        if self._username is not None:
            user = User.query.get(self.user_id)
            return decrypt_data(self._username, user.master_password)
        else:
            return None

    @username.setter
    def username(self, value):
        if value is not None:
            user = User.query.get(self.user_id)
            self._username = encrypt_data(value, user.master_password)
        else:
            self._username = "-"

    @property
    def email(self):
        if self._email is not None:
            user = User.query.get(self.user_id)
            return decrypt_data(self._email, user.master_password)
        else:
            return None
    
    @email.setter
    def email(self, value):
        if value is not None:
            user = User.query.get(self.user_id)
            self._email = encrypt_data(value, user.master_password) 
        else:
            self._email = "-"

    @property
    def password(self):
        if self._password is not None:
            user = User.query.get(self.user_id)
            return decrypt_data(self._password, user.master_password)
        else:
            return None
    
    @password.setter
    def password(self, value):
        user = User.query.get(self.user_id)
        self._password = encrypt_data(value, user.master_password)