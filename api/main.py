from logging import getLogger

from src import app, api, db, ma
from src.resources.test import RouteOne

from src.resources.auth import (
    Login,
    Logout,
    RefreshToken,
    ChangePassword,
)
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(RefreshToken, "/token")
api.add_resource(ChangePassword, "/changePassword")
api.add_resource(RouteOne, "/route-one")

db.init_app(app)
ma.init_app(app)

if __name__ != '__main__':
    gunicorn_logger = getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)