from flask import render_template, request, url_for, session
from sqlalchemy.sql import and_
from Ostrich import app
from Ostrich import models


@app.route('/')
def index():
    feed=models.User.query.all()
    return render_template("index.html", name="___", feed=feed)

@app.route('/posted', methods=["GET","POST"])
def posted():
    name = request.form['name']
    location = request.form['location']
    course = request.form['course']
    shirt = request.form['shirt']
    new_post = models.User(name, location, course, shirt)
    models.db.session.add(new_post)
    models.db.session.commit()
    feed=models.User.query.all()
    session['idNum'] = new_post.id
    return render_template("logged_in.html", name=name, feed=feed)


@app.route('/logged_out')
def logged_out():
    idNum = session.get('idNum', None)
    user = models.User.query.filter_by(id=idNum).first()
    models.db.session.delete(user)
    models.db.session.commit()
    feed = models.User.query.all()
    return render_template("index.html", feed=feed, idNum=idNum)

@app.route('/filterLocation', methods=["GET", "POST"])
def filterLocation():
    location = request.form['location']
    filteredFeed = models.User.query.filter_by(location=location).all()
    return render_template("index.html", feed=filteredFeed)

@app.route('/filterCourse', methods=["GET", "POST"])
def filterCourse():
    course = request.form['course']
    filteredFeed = models.User.query.filter_by(course=course).all()
    return render_template("index.html", feed=filteredFeed)


