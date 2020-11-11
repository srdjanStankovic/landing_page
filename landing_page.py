#!/usr/bin/python3

from flask import Flask, render_template

application = Flask(__name__)

@application.route("/")
def landing_page():
    return render_template("index.html")

if __name__ == '__main__':
    application.run("127.127.127.127", 8080, True)
