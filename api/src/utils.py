from functools import wraps
from flask import request
from src.models.auth import User

def check_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.get_json()['token']
        token_check = User.decode_token(token)

        if type(token_check) is not str:
            return token_check
        return f(*args, **kwargs)
    return decorated
