#!/usr/bin/python3
import logging
import yaml
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)
application = Flask(__name__)

## TODO: setup base with email and date&time
utc = datetime.utcnow()
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_base.sqlite3'

db = SQLAlchemy(application)
class users_base(db.Model):
   id = db.Column('users_id', db.Integer, primary_key = True)
   email = db.Column(db.String(254))
   datetime = db.Column(db.Integer)

   def __init__(self, email, datetime):
      self.email = email
      self.datetime = datetime

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
    db.create_all()
    parameters = read_configs()
    application.run(parameters[0], parameters[1], True)
