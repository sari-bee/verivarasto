from flask import Flask, render_template, request, redirect
from os import getenv
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

import transfusion, products, patients, maintenance, inventory

@app.route("/")
def index():
    return render_template("index.html")