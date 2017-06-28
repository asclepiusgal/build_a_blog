#!/usr/bin/env python

__author__ = "Jeanna Clark"
__version__ = "1.0"
# June 26, 2017
# Flask Blog App re: LaunchCode students
# Rubric: http://education.launchcode.org/web-fundamentals/assignments/build-a-blog/


from flask import Flask, request, render_template, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/blog'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'super_secret_key'
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    date = db.Column(db.DateTime)

    def __init__(self, title, body, date=None):
        self.title = title
        self.body = body
        if date is None:
            date = datetime.utcnow()
        self.date = date


@app.route('/', methods=['GET'])
def index():
    title = "Build a Blog"

    if request.args:
        post_id = request.args.get('id')
        post = Blog.query.get(post_id)
        return render_template('one_post.html', title=title, post=post)
    else:
        posts = Blog.query.order_by(Blog.date.desc()).all()
        return render_template('blog.html', title=title, posts=posts)


@app.route('/new_post', methods=['POST', 'GET'])
def new_post():

    if request.method == ['POST']:
        body = request.form['body']
        blog_title = request.form['title']

        if (len(blog_title) > 1) or (len(body) > 1):
            new_entry = Blog(blog_title, body)
            db.session.add(new_entry)
            db.session.commit()
            flash('error', 'Post added')
            url = "/?id=" + str(new_entry.id)
            return redirect(url)
        else:
            flash('error', 'Title and blog entry are required.')

    title = "Add a new post"
    return render_template('new_post.html', title=title)


if __name__ == '__main__':
    app.run()
