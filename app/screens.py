from app import app
from flask import render_template

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/train")
def train():
    return render_template("train.html")

@app.route("/results")
def results():
    return render_template("results.html")

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

