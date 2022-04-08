from app import app
from flask import render_template, session, request, redirect
import user

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if user.check_user_credentials(username, password):
        return redirect("/inventory")
    else:
        return redirect("/")

@app.route("/logout")
def logout():
    user.delete_session()
    return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/newuser", methods=["POST"])
def newuser():
    username = request.form["username"]
    password = request.form["password"]
    role = 1
    user.add_user(username, password, role)
    return redirect("/")


