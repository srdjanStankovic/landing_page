#!/usr/bin/python3
import logging
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from datetime import datetime
from utils import read_configs, validate_inserted_email, NMR_CONFIG_PAR, email_validation


logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
parameters = [""] * NMR_CONFIG_PAR
input_message =  "Enter E-mail address"

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

@app.route("/", methods = ['GET'])
def landing_page_get():
    logging.debug("It's GET")

    return render_template("index.html", parameters = parameters, input_message = input_message)

@app.route("/", methods = ['POST'])
def landing_page_post():
    email = ''
    global input_message
    logging.debug("It's POST")
    logging.info("Web server started!")

    email = request.form.get('email')
    validation = validate_inserted_email(email)
    logging.debug("Entered email is: " + email)

    if validation == email_validation.NONE:
        input_message = "Enter E-mail address"
    elif validation == email_validation.TRUE:
        utc = datetime.utcnow()
        entrance = users_database(email, utc)
        try:
            db.session.add(entrance)
            db.session.commit()
            input_message = "Thanks for subscribing"
            logging.debug(input_message)
        except exc.IntegrityError:
            db.session.rollback()
            input_message = "User already exist. Please enter new email."
            logging.error("User already exist!")
        except:
            input_message = "Please enter again"
            logging.error("Failed to enter new record in the database!")
    else:
        input_message = "Not valid email. Please enter new email."
        logging.error("Not valid email. Please enter new email.")

    return redirect(url_for("landing_page_get"))

@app.route("/view", methods=['POST'])
def view():
    logging.debug("Inside view")
    users = users_database.query.all()
    readed_dict = {user.email: user.datetime for user in users}

    return render_template("login.html", readed = readed_dict)


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
    app.run(parameters[0], parameters[1], debug=True)
