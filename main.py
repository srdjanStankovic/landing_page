#!/usr/bin/python3
import logging
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from utils import read_configs, validate_inserted_email, NMR_CONFIG_PAR

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
parameters = [""] * 8

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_database.sqlite3'

db = SQLAlchemy(app)
class users_database(db.Model):
   logging.debug("Setup database")
   email = db.Column("email", db.String(254), primary_key = True)
   datetime = db.Column(db.Integer)

   def __init__(self, email, datetime):
      self.email = email
      self.datetime = datetime

@app.route("/",methods = ['POST', 'GET'])
def landing_page():
    logging.info("Web server started!")

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

def initialization():
    logging.info("Configuring web server")
    global parameters
    try:
        parameters = read_configs()
        db.create_all()
    except:
        logging.error("Web server failed to configure!")
        render_template("maintaine.html")

    logging.info("Web server configured!")

initialization()

if __name__ == '__main__':
    app.run(debug=True)
