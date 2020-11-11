#!/usr/bin/python3
import logging
import yaml
from flask import Flask, render_template
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)
application = Flask(__name__)

## TODO: setup base with email and date&time
utc = datetime.utcnow()

def read_configs():
    parameters = [""] * 5

    with open(r'config.yaml') as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        fruits_list = yaml.load(file, Loader=yaml.FullLoader)

        for key, value in fruits_list.items():
            logging.info(key + " : " + str(value))

            if key == "host":
                parameters[0] = value
            if key == "port":
                parameters[1] = value
            elif key == "facebook":
                parameters[2] = value
            elif key == "instagram":
                parameters[3] = value
            elif key == "youtube":
                parameters[4] = value
            else:
                logging.error("Unsupported key: " + key)
        logging.info(parameters)
        return parameters

@application.route("/")
def landing_page():
    return render_template("index.html", parameters = parameters)

if __name__ == '__main__':
    logging.info("Application started!")
    parameters = read_configs()
    application.run(parameters[0], parameters[1], True)
