#!/usr/bin/python3
import logging
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from utils import read_configs, validate_inserted_email

logging.basicConfig(level=logging.DEBUG)
application = Flask(__name__)
parameters = [""] * 5

application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_database.sqlite3'

db = SQLAlchemy(application)
class users_database(db.Model):
   id = db.Column('users_id', db.Integer, primary_key = True)
   email = db.Column(db.String(254))
   datetime = db.Column(db.Integer)

   def __init__(self, email, datetime):
      self.email = email
      self.datetime = datetime

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
            try:
                db.session.add(entrance)
                db.session.commit()
            except:
                #TODO: raise popup
                logging.error("Failed to enter new record in the database!")
            #TODO: send welcome email!
        else:
            #TODO: raise popup
            logging.error("Not valid email!")

    return render_template("index.html", parameters = parameters)


if __name__ == '__main__':
    logging.info("Web server started!")
    db.create_all()
    parameters = read_configs()
    application.run(parameters[0], parameters[1], True)
