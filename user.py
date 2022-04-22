import os
from datetime import date
from werkzeug.security import check_password_hash, generate_password_hash
from flask import abort, session
from db import db


def add_user(username, password, role):
    try:
        hash = generate_password_hash(password)
        sql = "INSERT INTO Users (username, password, role) VALUES (:username, :password, :role)"
        db.session.execute(
            sql, {"username": username, "password": hash, "role": role})
        db.session.commit()
    except:
        return False
    return True


def check_user_credentials(username, password):
    sql = "SELECT password, role FROM Users WHERE username = :username"
    user = db.session.execute(sql, {"username": username}).fetchone()
    if not user:
        return False
    hash = user.password
    if check_password_hash(hash, password):
        session["username"] = username
        session["role"] = user.role
        session["csrf_token"] = os.urandom(16).hex()
        return True
    return False


def change_password(oldpassword, newpassword):
    sql = "SELECT password FROM Users WHERE username = :username"
    hashedpassword = db.session.execute(
        sql, {"username": session["username"]}).fetchone()[0]
    if check_password_hash(hashedpassword, oldpassword):
        try:
            hash = generate_password_hash(newpassword)
            sql = "UPDATE Users SET password = :password WHERE username = :username"
            db.session.execute(
                sql, {"password": hash, "username": session["username"]})
            db.session.commit()
            return True
        except:
            return False
    else:
        return False


def delete_session():
    if session:
        del session["username"]
        del session["role"]
        del session["csrf_token"]


def check_csrf_token(csrf_token):
    if session["csrf_token"] != csrf_token:
        abort(403)


def check_user_role(role):
    if session.get("role", 0) != role:
        abort(403)


def get_logs():
    sql = """SELECT logtext, username, date FROM Logs, Users
        WHERE Users.id = Logs.user_id ORDER BY Logs.id DESC"""
    return db.session.execute(sql).fetchall()


def add_to_log(logtext):
    sql = "SELECT id FROM Users WHERE username = :username"
    user_id = db.session.execute(
        sql, {"username": session["username"]}).fetchone()[0]
    sql = "INSERT INTO Logs (logtext, user_id, date) VALUES (:logtext, :user_id, :date)"
    db.session.execute(
        sql, {"logtext": logtext, "user_id": user_id, "date": date.today()})
    db.session.commit()
