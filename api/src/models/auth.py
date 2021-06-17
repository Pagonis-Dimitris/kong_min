from typing import List
from datetime import datetime, timedelta
from os import getenv
import jwt
import sys
from src import db, app

TOKEN_SECRET = getenv('SECRET_TOKEN') or 'token_secret_dev'
REFRESH_TOKEN_SECRET = getenv('SECRET_REFRESH_TOKEN') or 'devrefreshsecret'


def getTokenError(msg):
    return {
        'success': False,
        'message': msg
    }


class UserModel():
    def __init__(self, userid, username, role):
        self.userid = userid
        self.username = username
        self.role = role


class AuthModel():
    def __init__(self, token, refresh_token):
        self.token = token
        self.refreshToken = refresh_token


class LoginModel():
    def __init__(self, user, auth):
        self.user = user
        self.auth = auth


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    username = db.Column(db.String(200), nullable=False, primary_key=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    @classmethod
    def get_user_by_username(cls, username) -> "Vessel":
        return db.session.query(cls).filter(cls.username == username).first()

    def toUserModel(self) -> "UserModel":
        return UserModel(self.id, self.username, self.role)

    def create_tokens(self, username):
        """
        Generates the Auth Token
        :return: string
        """
        try:

            payload = {
                'exp': datetime.utcnow() + timedelta(days=0, minutes=30),
                'iat': datetime.utcnow(),
                'iss': '{\"user\":1}',
                'user': username
            }

            token = jwt.encode(
                payload,
                TOKEN_SECRET,
                algorithm='HS256'
            )
            refresh_token = jwt.encode(
                {i: payload[i] for i in payload if i != 'exp'},
                REFRESH_TOKEN_SECRET,
                algorithm='HS256'
            )

            return token if isinstance(token, str) else token.decode('utf-8'), refresh_token if isinstance(refresh_token, str) else refresh_token.decode('utf-8')
        except Exception as e:
            print(e)
            return e

    @staticmethod
    def decode_token(token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(token, TOKEN_SECRET, algorithms=["HS256"])
            return payload['user']
        except jwt.ExpiredSignatureError:
            app.logger.warning(f"ExpiredSignatureError with token: {token}")
            return getTokenError('Signature expired. Please log in again.'), 401
        except jwt.InvalidTokenError:
            app.logger.warning(f"InvalidTokenError with token: {token}")
            return getTokenError('Invalid token. Please log in again.'), 401

    @staticmethod
    def decode_refresh_token(refresh_token):
        """
        Validates the auth token
        :param auth_refresh_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(refresh_token, REFRESH_TOKEN_SECRET, algorithms=["HS256"])
            is_blacklisted_token = BlacklistTokens.get_blacklist_token(refresh_token)
            if is_blacklisted_token:
                return getTokenError('Token blacklisted. Please log in again.'), 400
            else:
                payload = {
                    'exp': datetime.utcnow() + timedelta(days=0, minutes=30),
                    'iat': datetime.utcnow(),
                    'user': payload['user']
                }

                token = jwt.encode(
                    payload,
                    TOKEN_SECRET,
                )

                return token if isinstance(token, str) else token.decode('utf-8')
        except jwt.ExpiredSignatureError:
            return getTokenError('Signature expired. Please log in again.'), 400
        except jwt.InvalidTokenError:
            return getTokenError('Invalid token. Please log in again.'), 400

    def update_password(self, password):
        self.password = password
        db.session.commit()


class BlacklistTokens(db.Model):
    __tablename__ = "blacklist_tokens"

    id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    token = db.Column(db.String(300), nullable=False, primary_key=True)
    blacklisted_on = db.Column(db.TIMESTAMP, nullable=False)

    @classmethod
    def get_blacklist_token(cls, token) -> "BlacklistTokens":
        res = db.session.query(cls).filter(cls.token == token).first()
        if res:
            return True
        else:
            return False

    @classmethod
    def add_blacklist_token(cls, token) -> "":
        now_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        blacklisted_token = cls(token=token, blacklisted_on=now_string)
        db.session.add(blacklisted_token)
        db.session.commit()
