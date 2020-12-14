#!/usr/bin/python3
import logging
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from sqlalchemy import exc
from utils import (
    read_configs,
    validate_inserted_email,
    NMR_CONFIG_PAR,
    email_validation,
    SUBSCRIBED_USERS_FILE_NAME,
)


logging.basicConfig(level=logging.DEBUG)
parameters = [""] * NMR_CONFIG_PAR
input_message = "Enter E-mail address"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users_database.sqlite3"
app.config["SQLALCHEMY_BINDS"] = {"login": "sqlite:///login.db"}
app.config[
    "SECRET_KEY"
] = '8:Y_*%DXNLy}.$9c,x"tZjX(f`#|?{H*/DGasGgBc]<Ud+G&o/*tGeGlkFSI^`&'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


class users_database(db.Model):
    logging.debug("Setup database")
    email = db.Column("email", db.String(254), primary_key=True)
    datetime = db.Column(db.Integer)

    def __init__(self, email, datetime):
        self.email = email
        self.datetime = datetime


def get_user_list():
    users = users_database.query.all()

    return {user.email: user.datetime for user in users}


def insert_new_entrance(new_entrance):
    db.session.add(new_entrance)
    db.session.commit()


def empty_user_list():
    db.session.query(users_database).delete()
    db.session.commit()

def rollback_database():
    db.session.rollback()

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


@app.route("/", methods=["GET"])
def landing_page_get():
    logging.debug("landing_page_get entrance")

    return render_template(
        "index.html", parameters=parameters, input_message=input_message
    )


@app.route("/", methods=["POST"])
def landing_page_post():
    email = ""
    global input_message
    logging.debug("landing_page_post entrance")

    if "submit" in request.form:
        email = request.form.get("email")
        validation = validate_inserted_email(email)
        logging.debug("Entered email is: " + email)

        if validation == email_validation.NONE:
            input_message = "Enter E-mail address"
        elif validation == email_validation.TRUE:
            utc = datetime.utcnow()

            try:
                insert_new_entrance(users_database(email, utc))
                input_message = "Enter E-mail address"
                logging.debug(input_message)
                return redirect(url_for("thanks_for_subscribing"))
            except exc.IntegrityError:
                rollback_database()
                input_message = "User already exist. Please enter new email."
                logging.error("User already exist!")
            except:
                rollback_database()
                input_message = "Please enter again"
                logging.error("Failed to enter new record in the database!")
        else:
            input_message = "Not valid email. Please enter new email."
            logging.error("Not valid email. Please enter new email.")
    else:
        logging.error("Unknown form inserted")

    return redirect(url_for("landing_page_get"))


@app.route("/thanks_for_subscribing", methods=["GET"])
def thanks_for_subscribing():
    logging.debug("thanks_for_subscribing entrance")

    return render_template(
        "thanks_for_subscribing.html",
        parameters=parameters,
        input_message=input_message,
    )


@app.route("/login", methods=["POST"])
def index_post():
    logging.debug("index_post entrance")

    username = request.form.get("Username")
    password = request.form.get("Password")
    logging.debug(
        "Inserted username is: " + username + "\nInserted password is: " + password
    )

    username = User.query.filter_by(username=username).first()
    password = User.query.filter_by(password=password).first()
    logging.debug(
        "Inserted username is " + str(username) + " and password is " + str(password)
    )

    if username != None and password != None:
        login_user(username)
        return redirect(url_for("view_get"))

    return redirect(url_for("index_get"))


@app.route("/login", methods=["GET"])
def index_get():
    logging.debug("index_get entrance")

    if current_user.is_authenticated:
        return redirect(url_for("view_get"))

    return render_template("login.html")


@app.route("/" + SUBSCRIBED_USERS_FILE_NAME)
def generate_download_csv():
    def generate():
        returned_dict = get_user_list()
        logging.debug(returned_dict)
        for email, dattime in returned_dict.items():
            logging.debug(email + " " + dattime)
            yield "".join(email) + "".join(",") + "".join(dattime) + "\n"

    return Response(generate(), mimetype="text/csv")


@app.route("/view", methods=["POST"])
def view_post():
    logging.debug("view_post entrance")
    logging.info("You will be logout as " + current_user.username)

    if "log_out" in request.form:
        logging.debug("Logout user")
        logout_user()
        return redirect(url_for("index_post"))

    elif "refresh_page" in request.form:
        logging.debug("Refresh page")
        return redirect(url_for("view_get"))

    elif "empty_list" in request.form:
        logging.debug("Empty list")

        empty_user_list()
        return redirect(url_for("view_get"))

    elif "export_users_list" in request.form:
        logging.debug("Export user list")

        return redirect("/" + SUBSCRIBED_USERS_FILE_NAME)

    else:
        logging.debug("Unknown form validation occurs!")
        return redirect(url_for("view_get"))


@app.route("/view", methods=["GET"])
def view_get():
    logging.debug("view_get entrance")

    if current_user.is_authenticated:
        logging.debug("You are logged in as " + current_user.username)
        return render_template("view.html", readed=get_user_list())
    else:
        logging.debug("User isn't authorised!")
        return redirect(url_for("index_get"))


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


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


initialization()

# TODO: Heroku specific issues(delete data base after shootdown), refactor, session problem
if __name__ == "__main__":
    app.run(parameters[0], parameters[1], debug=True)
