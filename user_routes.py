from flask import render_template, request, redirect, flash
from app import app
import user


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"].strip()
    password = request.form["password"].strip()
    if not user.check_user_credentials(username, password):
        flash("Käyttäjätunnus tai salasana on väärin")
        return render_template("index.html")
    else:
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
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        password2 = request.form["password2"].strip()
        if len(username) < 3 or len(username) > 20 or len(password) < 6 or len(password) > 20:
            flash("Syötit väärän pituisen käyttäjätunnuksen tai salasanan")
            return render_template("register.html")
        if password != password2:
            flash("Salasanat eivät täsmää")
            return render_template("register.html")
        role = 1
        if not user.add_user(username, password, role):
            flash("Käyttäjätunnus on jo käytössä")
            return render_template("register.html")
        flash(f"Rekisteröityminen onnistui, tervetuloa {username}!")
        return redirect("/inventory")
    return render_template("register.html")


@app.route("/changepassword", methods=["POST"])
def change_password():
    if not user.check_user_role(1):
        return redirect("/")
    csrf_token = request.form["csrf_token"]
    if not user.check_csrf_token(csrf_token):
        return redirect("/")
    oldpassword = request.form["oldpassword"].strip()
    newpassword = request.form["newpassword"].strip()
    newpassword2 = request.form["newpassword2"].strip()
    if len(newpassword) < 6 or len(newpassword) > 20:
        flash("Syötit väärän pituisen käyttäjätunnuksen tai salasanan")
    elif newpassword != newpassword2:
        flash("Uudet salasanat eivät täsmää")
    elif not user.change_password(oldpassword, newpassword):
        flash("Salasanan vaihto ei onnistunut. Syötitkö vanhan salasanan oikein?")
    else:
        flash("Salasana vaihdettu onnistuneesti")
    return redirect("/maintenance")


@app.route("/logs")
def logs():
    if not user.check_user_role(1):
        return redirect("/")
    logs = user.get_logs()
    return render_template("logs.html", logs=logs)
