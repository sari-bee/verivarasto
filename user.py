from werkzeug.security import check_password_hash, generate_password_hash
import os
from flask import abort, request, session
from db import db

def add_user(username, password, role):
    hash = generate_password_hash(password)
    try:
        sql = "INSERT INTO Users (username, password, role) VALUES (:username, :password, :role)"
        db.session.execute(sql, {"username":username, "password":hash, "role":role})
        db.session.commit()
    except:
        return False
    return True

def check_user_credentials(username, password):
    sql = "SELECT id, password, role FROM Users WHERE username=:username"
    user = db.session.execute(sql, {"username":username}).fetchone()
    if not user:
        return False
    else:
        hash = user.password
        if check_password_hash(hash, password):
            session["username"] = username
            session["role"] = user.role
            session["csrf_token"] = os.urandom(16).hex()
            return True
        else:
            return False

def delete_session():
    del session["username"]
    del session["role"]
    del session["csrf_token"]

def check_csrf_token(csrf_token):
    if session["csrf_token"] != csrf_token:
        abort(403)

def check_user_role(role):
    if session.get("role", 0) != role:
        abort(403)


