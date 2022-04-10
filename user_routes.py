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
    if not user.check_user_credentials(username, password):
        return render_template("index.html", message="Käyttäjätunnus tai salasana on väärin")
    return redirect("/inventory")

@app.route("/logout")
def logout():
    user.delete_session()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]
        if len(username) < 3 or len(username) > 20 or len(password) < 6 or len(password) > 20:
            return render_template("register.html", message="Syötit väärän pituisen käyttäjätunnuksen tai salasanan")   
        if password != password2:
            return render_template("register.html", message="Salasanat eivät täsmää")
        role = 1
        if not user.add_user(username, password, role):
            return render_template("register.html", message="Käyttäjätunnus on jo käytössä")
        return redirect("/")

@app.route("/changepassword", methods=["POST"])
def change_password():
    user.check_user_role(1)
    csrf_token = request.form["csrf_token"]
    user.check_csrf_token(csrf_token)
    oldpassword = request.form["oldpassword"]
    newpassword = request.form["newpassword"]
    newpassword2 = request.form["newpassword2"]
    if len(newpassword) < 6 or len(newpassword) > 20:
        return render_template("message.html", message="Syötit väärän pituisen käyttäjätunnuksen tai salasanan")   
    if newpassword != newpassword2:
        return render_template("message.html", message="Uudet salasanat eivät täsmää")
    if not user.change_password(oldpassword, newpassword):
        return render_template("message.html", message="Salasanan vaihto ei onnistunut. Syötitkö vanhan salasanan oikein?")
    return render_template("message.html", message="Salasana vaihdettu onnistuneesti")

@app.route("/logs")
def logs():
    user.check_user_role(1)
    logs = user.get_logs()
    return render_template("logs.html", logs=logs)
