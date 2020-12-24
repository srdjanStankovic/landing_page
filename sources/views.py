#!/usr/bin/python3
import logging
from sources import app
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, Response, session, stream_with_context
from sqlalchemy import exc
from flask_login import (
    login_user,
    logout_user,
    current_user,
)
from sources.utils import (
    validate_inserted_email,
    email_validation,
    SUBSCRIBED_USERS_FILE_NAME,
    BROWSER_SESSION_LIFETIME,
    read_configs,
)
from sources.models import (
    get_user_list,
    insert_new_entrance,
    empty_user_list,
    rollback_database,
    User,
    users_database,
)

input_message = "Enter E-mail address"

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=BROWSER_SESSION_LIFETIME)

@app.route("/", methods=["GET"])
def landing_page_get():
    logging.debug("landing_page_get entrance")

    global input_message

    if not "already_participated" in session:
        logging.debug("Not already_participated")
        input_message = "Enter E-mail address"
    parameters = read_configs()
    logging.debug(input_message)
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
                logging.debug("Succesull user database entrance.")
                input_message = "Thanks for subscribing."
                logging.debug(input_message)
                session["already_participated"] = True
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
    logging.debug("Entrance generate_download_csv")
    def generate():
        returned_dict = get_user_list()
        logging.debug(returned_dict)
        for email, dattime in returned_dict.items():
            logging.debug(email + " " + dattime)
            yield "".join(email) + "".join(",") + "".join(dattime) + "\n"

    return Response(stream_with_context(generate()), mimetype="text/csv")


@app.route("/view", methods=["POST"])
def view_post():
    logging.debug("view_post entrance")

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

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
