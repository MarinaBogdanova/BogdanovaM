from datetime import datetime

##from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import *

from todoapp import app

db = SQLAlchemy(app)


class Todo(db.Model):
    __tablename__ = "todo"
    id = db.Column('id', db.Integer, primary_key=True)
    category_id = db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
    description = db.Column('description', db.Unicode)
    creation_date = db.Column('creation_date', db.Date, default=datetime.utcnow)
    is_done = db.Column('is_done', db.Boolean, default=False)

    category = db.relationship('Category', foreign_keys=category_id, backref="todos")


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.Unicode)
