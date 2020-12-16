#!/usr/bin/python3
import logging
from sources import app
from sources.utils import read_configs
from sources.models import db
from sources.models import init_application

logging.basicConfig(level=logging.DEBUG)
# TODO: Heroku specific issues(delete data base after shootdown), Database are problems!
init_application(app)
if __name__ == "__main__":
    parameters = read_configs()
    app.run(parameters[0], parameters[1])
