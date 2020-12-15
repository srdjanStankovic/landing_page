#!/usr/bin/python3
from sources import app
from flask_login import (
    LoginManager,
    )

from sources.models import (
    User
)


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
