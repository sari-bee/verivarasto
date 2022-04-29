import os
from datetime import date
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from db import db


def add_user(username, password, role):
    try:
        salt = str(os.urandom(16))
        hashed_password = generate_password_hash(password + salt)
        sql = "INSERT INTO Users (username, password, salt, role) VALUES (:username, :password, :salt, :role)"
        db.session.execute(
            sql, {"username":username, "password":hashed_password, "salt":salt, "role":role})
        db.session.commit()
    except:
        return False
    return True


def check_user_credentials(username, password):
    sql = "SELECT password, salt, role FROM Users WHERE username = :username"
    user = db.session.execute(sql, {"username":username}).fetchone()
    if not user:
        return False
    hashed_password = user.password
    salted_password = password + user.salt
    if check_password_hash(hashed_password, salted_password):
        session["username"] = username
        session["role"] = user.role
        session["csrf_token"] = os.urandom(16).hex()
        return True
    return False


def change_password(oldpassword, newpassword):
    sql = "SELECT password, salt FROM Users WHERE username = :username"
    user = db.session.execute(
        sql, {"username": session["username"]}).fetchone()
    old_hashed_password = user.password
    old_salted_password = oldpassword + user.salt
    if check_password_hash(old_hashed_password, old_salted_password):
        try:
            salt = str(os.urandom(16))
            new_hashed_password = generate_password_hash(newpassword + salt)
            sql = "UPDATE Users SET password = :password, salt = :salt WHERE username = :username"
            db.session.execute(
                sql, {"password":new_hashed_password, "salt":salt, "username":session["username"]})
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
        return False
    return True

def check_user_role(role):
    if session.get("role", 0) != role:
        return False
    return True


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
        sql, {"logtext":logtext, "user_id":user_id, "date":date.today()})
    db.session.commit()