#!/usr/bin/env python

__author__ = "Jeanna Clark"
__version__ = "1.0"
# July 2, 2017
# Flask Blog App Continued re: LaunchCode students
# Rubric: http://education.launchcode.org/web-fundamentals/assignments/blogz/


from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, static_url_path='/static')
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/blog'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'super_secret_key'
app.static_folder = 'static'
db = SQLAlchemy(app)
