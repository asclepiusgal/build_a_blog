#!/usr/bin/env python

__author__ = "Jeanna Clark"
__version__ = "1.0"
# July 2, 2017
# Flask Blog App Continued re: LaunchCode students
# Rubric: http://education.launchcode.org/web-fundamentals/assignments/blogz/


from flask import request, render_template, redirect, session, flash
from models import User, Blog
from app import app, db
from hashutils import make_hash, validate_password


@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        if request.endpoint == 'signup':
            return redirect('/signup')
        return redirect('/login')


@app.route('/')
def index():
    title = 'Home page'
    users = User.query.all()
    return render_template('index.html', title=title, users=users)


@app.route('/blog', methods=['GET'])
def blog():
    title = "Build a Blog"

    if request.args:
        post_id = request.args.get('id')
        username = request.args.get('user')

        if post_id:
            post = Blog.query.get(post_id)
            return render_template('one_post.html', title=title, post=post)
        elif username:
            user = User.query.filter_by(username=username).first()
            posts = Blog.query.filter_by(owner_id=user.id).order_by(Blog.date.desc()).all()

            return render_template('single_user.html', title=title, posts=posts)
    else:
        posts = Blog.query.order_by(Blog.date.desc()).all()
        # TODO: insert pagination for blog.html & single_user.html
        return render_template('blog.html', title=title, posts=posts)


@app.route('/new_post', methods=['POST', 'GET'])
def new_post():
    if request.method == ['POST']:
        body = request.form['body']
        blog_title = request.form['title']
        owner = User.query.filter_by(username=session['username']).first()

        if (len(blog_title) > 1) and (len(body) > 1):
            new_entry = Blog(blog_title, body, owner.id)
            db.session.add(new_entry)
            db.session.commit()

            flash('Post added', 'error')
            url = "/?id=" + str(new_entry.id)
            return redirect(url)
        else:
            flash('Title and blog entry are required.', 'error')

    title = "Add a new post"
    return render_template('new_post.html', title=title)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify_password']

        if (len(username) < 3) or (len(password) < 3):
            flash('Username & password must be greater than three characters', 'error')
            redirect('/signup')
        elif password != verify_password:
            flash('Passwords do not match', 'error')
            redirect('/signup')
        elif (username == '') or (password == '') or (verify_password == ''):
            flash('blank input submission', 'error')
            redirect('/signup')
        elif User.query.get(username).username == username:
            flash('already exists for that user', 'error')
            redirect('/login')
        else:
            new_user = User(username, make_hash(password))
            db.session.add(new_user)
            db.session.commit()

            flash('Account created', '')
            session['username'] = username
            redirect('/new_post')

    title = "Sign up"
    return render_template('signup.html', title=title)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and password:
            if validate_password(password, user.password):
                session['username'] = username
                flash('logged in', '')
                return redirect('/new_post')
        else:
            flash('invalid username or password', 'error')
            return redirect('/login')

    title = 'Login'
    return render_template('login.html', title=title)


@app.route('/logout')
def logout():
    del session['username']
    flash('logging out', 'error')
    return redirect('/blog')


if __name__ == '__main__':
    app.run()
