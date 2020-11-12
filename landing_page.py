#!/usr/bin/python3
import logging
import yaml
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from email_validator import validate_email, EmailNotValidError

logging.basicConfig(level=logging.DEBUG)
application = Flask(__name__)

application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_database.sqlite3'

db = SQLAlchemy(application)
class users_database(db.Model):
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

def validate_inserted_email(email):
    logging.debug(email)
    if email == None:
        return False

    try:
      valid = validate_email(email)
      email = valid.email
    except EmailNotValidError as e:
      # email is not valid, exception message is human-readable
      logging.error(str(e))
      return False

    return True

@application.route("/",methods = ['POST', 'GET'])
def landing_page():
    if request.method == "POST":
        logging.debug("It's POST")
    elif request.method == "GET":
        email = request.args.get('email')
        if validate_inserted_email(email):
            logging.debug("It's GET\n Email is: " + email)

            utc = datetime.utcnow()
            entrance = users_database(email, utc)
            db.session.add(entrance)
            db.session.commit()
        else:
            #TODO: raise oninvalid
            logging.error("Not valid email!")

    return render_template("index.html", parameters = parameters)


if __name__ == '__main__':
    logging.info("Web server started!")
    db.create_all()
    parameters = read_configs()
    application.run(parameters[0], parameters[1], True)
