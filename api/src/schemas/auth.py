from src import ma
from marshmallow import fields

class UserSchema(ma.Schema):
    userid = fields.Integer()
    username = fields.String()
    role = fields.String()
    fleet = fields.String()

class AuthTokenSchema(ma.Schema):
    token = fields.String()
    refreshToken = fields.String()

class LoginSchema(ma.Schema):
    user = fields.Nested(UserSchema)
    auth = fields.Nested(AuthTokenSchema)