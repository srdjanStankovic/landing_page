#!/usr/bin/python3
import logging
from sources import app
from sources.utils import read_configs, initialization
from sources.models import db, users_database

logging.basicConfig(level=logging.DEBUG)
# TODO: Heroku specific issues(delete data base after shootdown), Database are problems!
if __name__ == "__main__":
    #initialization()
    parameters = read_configs()
    app.run(parameters[0], parameters[1])
