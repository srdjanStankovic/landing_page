#!/usr/bin/python3
import logging
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlalchemy import exc
from utils import read_configs, validate_inserted_email, NMR_CONFIG_PAR, email_validation


logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
parameters = [""] * NMR_CONFIG_PAR
input_message =  "Enter E-mail address"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_database.sqlite3'
app.config["SQLALCHEMY_BINDS"] = {"login" : "sqlite:///login.db"}
app.config['SECRET_KEY'] = '8:Y_*%DXNLy}.$9c,x"tZjX(f`#|?{H*/DGasGgBc]<Ud+G&o/*tGeGlkFSI^`&'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
class users_database(db.Model):
   email = db.Column("email", db.String(254), primary_key = True)
   logging.debug("Setup database")
   datetime = db.Column(db.Integer)

   def __init__(self, email, datetime):
      self.email = email
      self.datetime = datetime

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    __bind_key__ = "login"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64), unique=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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

@app.route('/login', methods = ['POST'])
def index_post():
    logging.debug('index_post entrance')

    username = request.form.get('Username')
    password = request.form.get('Password')
    logging.debug("Inserted username is: " + username + "\nInserted password is: " + password)

    username = User.query.filter_by(username=username).first()
    password = User.query.filter_by(password=password).first()
    logging.debug("Inserted username is " + str(username) + " and password is " + str(password))

    if username!=None and password!=None:
        login_user(username)
        return redirect(url_for('view_get'))

    return redirect(url_for('index_get'))

@app.route('/login', methods = ['GET'])
def index_get():
    logging.debug("index_get entrance")

    if current_user.is_authenticated:
        return redirect(url_for('view_get'))

    return render_template("login.html")

@app.route('/view', methods = ['POST'])
def view_post():
    logging.debug("view_post entrance")
    logging.info("You will be logout as " + current_user.username)

    logout_user()
    return redirect(url_for('index_post'))

@app.route('/view', methods = ['GET'])
def view_get():
    logging.debug("view_get entrance")

    if current_user.is_authenticated:
        logging.debug("The logged in user is " + current_user.username)

        users = users_database.query.all()
        readed_dict = {user.email: user.datetime for user in users}
        return render_template("view.html", readed = readed_dict)
    else:
        logging.debug("User isn't authorised!")
        return redirect(url_for('index_get'))

def initialization():
    logging.info("Configuring web server")
    global parameters
    try:
        parameters = read_configs()
        #db.create_all()
    except:
        logging.error("Web server failed to configure!")
        render_template("maintaine.html")

    logging.info("Web server configured!")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

initialization()

#TODO: copy to clipboard all emails, extract it as txt, empty base, insert admin in db!
if __name__ == '__main__':
    app.run(parameters[0], parameters[1], debug=True)
