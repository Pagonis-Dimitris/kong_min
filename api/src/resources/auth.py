from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required

from src import bcrypt
from src.models.auth import User, BlacklistTokens, LoginModel, AuthModel
from src.schemas.auth import LoginSchema
from src.utils import check_token

VESSELS_NOT_FOUND = "Vessels don't exist"
MALFORMED_REQUEST = "Malformed request"

loginSchema = LoginSchema()

def response(success, payload, status): return {'success': success, 'payload': payload}, status

class Login(Resource):
    """
    User Login Resource
    """
    @classmethod
    def post(csl):
        # get the post data
        request_body = request.get_json()
        try:
            # fetch the user data
            user = User.get_user_by_username(request_body['username'])
            if user and bcrypt.check_password_hash(
                user.password, request_body['password']
            ):
                auth_token, auth_refresh_token = user.create_tokens(user.username)
                
                loginPayload = LoginModel(user.toUserModel(), AuthModel(auth_token, auth_refresh_token))
                return response(True, loginSchema.dump(loginPayload), 200)
            return response(False, {'error': 'Invalid username or password'}, 201)
        except Exception as e:
            print(e)
            return response(False, {'error': 'Something went wrong'}, 500)

class Logout(Resource):
    """
    Logout Resource
    """
    @classmethod
    def post(csl):
        try:
            request_body = request.get_json()
            refresh_token = request_body['refreshToken']
            blacklist_check = BlacklistTokens.get_blacklist_token(refresh_token)
            if not blacklist_check:
                # insert the token
                BlacklistTokens.add_blacklist_token(refresh_token)
                return response(True, {'message': 'Successfully logged out'}, 200)
            return response(False, {'message': 'Invalid refresh token'}, 201)
        except Exception as e:
            print(e)
            return response(True, {'message': 'Something went wrong'}, 200)

class RefreshToken(Resource):
    """
    Refresh Token Resource
    """
    @classmethod
    def post(self):
        try:
            request_body = request.get_json()
            refresh_token = request_body['refreshToken']

            check_refresh_token = User.decode_refresh_token(refresh_token)
            if type(check_refresh_token) is str:
                return response(True, {'token': check_refresh_token}, 200)
            return check_refresh_token
        except Exception as e:
            print(e)
            response(False, {'error': 'Something went wrong'}, 500)

class ChangePassword(Resource):
    """
    Change Password Resource
    """
    @classmethod
    @check_token
    def post(self):
        try:
            request_body = request.get_json()
            username = request_body['username']
            user = User.get_user_by_username(username)

            if user:
                oldPassword = request_body['oldPassword']
            
                if bcrypt.check_password_hash(
                    user.password, oldPassword
                ):
                    password = request_body['password']
                    pass_hash = bcrypt.generate_password_hash(password).decode('utf-8')
                    user.update_password(pass_hash)

                    return {'success': True}, 200
                    
                return response(False, {'error': 'Incorrect password'}, 201)

            return response(False, {'error': 'Incorrect username'}, 201)
        except Exception as e:
            print(e)
            response(False, {'error': 'Something went wrong'}, 500)