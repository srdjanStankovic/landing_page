#!/usr/bin/python3
import logging
from flask import Flask
from sources.models import init_application, create_database

__version__ = "0.2.0"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users_database.sqlite3"
app.config["SQLALCHEMY_BINDS"] = {"login": "sqlite:///login.db"}
app.config["SECRET_KEY"] = '8:Y_*%DXNLy}.$9c,x"tZjX(f`#|?{H*/DGasGgBc]<Ud+G&o/*tGeGlkFSI^`&'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['DEBUG'] = True

init_application(app)
#create_database()

from sources import views
from sources import models
from sources import utils
from sources import login_manager
