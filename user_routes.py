from app import app
from flask import render_template, session, request
import user

@app.route("/")
def index():
    return render_template("index.html")

#@app.route("/login", methods=["POST"])
#def login():
#    username = request.form["username"]
#    password = request.form["password"]

