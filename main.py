#!/usr/bin/python3
import logging
from sources import app
from sources.utils import read_configs
from sources.models import db
from sources.models import init_application

logging.basicConfig(level=logging.DEBUG)

# TODO: Heroku specific issues(delete data base after shootdown), Database are problems!
if __name__ == "__main__":
    logging.info("Starting web server")

    parameters = read_configs()
    try:
        app.run(parameters[0], parameters[1])
    except:
        logging.error("Web server failed to start!")
