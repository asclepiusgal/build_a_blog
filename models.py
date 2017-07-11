#!/usr/bin/env python

__author__ = "Jeanna Clark"
__version__ = "1.0"
# July 2, 2017
# Flask Blog App Continued re: LaunchCode students
# Rubric: http://education.launchcode.org/web-fundamentals/assignments/blogz/

from datetime import datetime
from app import db


class Blog(db.Model):
    __tablename__ = 'blog'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime)

    def __init__(self, title, body, owner_id, date=None):
        self.title = title
        self.body = body
        self.owner_id = owner_id
        if date is None:
            date = datetime.utcnow()
        self.date = date


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(300))
    blogs = db.relationship('Blog', backref='user')

    def __init__(self, username, password):
        self.username = username
        self.password = password
