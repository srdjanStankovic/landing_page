#!/usr/bin/python3
import logging
from sources import app
from sources.utils import read_configs, initialization

logging.basicConfig(level=logging.DEBUG)
# TODO: Heroku specific issues(delete data base after shootdown), refactor
if __name__ == "__main__":
    initialization()
    parameters = read_configs()
    app.run(parameters[0], parameters[1])
