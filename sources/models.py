#!/usr/bin/python3
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    UserMixin,
)

db = SQLAlchemy()

class users_database(db.Model):
    email = db.Column("email", db.String(254), primary_key=True)
    datetime = db.Column(db.Integer)

    def __init__(self, email, datetime):
        self.email = email
        self.datetime = datetime


class User(UserMixin, db.Model):
    __bind_key__ = "login"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64), unique=True)

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

def create_database():
    db.create_all()

def init_application(app):
    db.init_app(app)
