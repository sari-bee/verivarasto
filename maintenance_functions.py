from db import db


def get_departments():
    sql = """SELECT id, department_abbrev, department_name FROM Departments"""
    return db.session.execute(sql).fetchall()


def get_departments_and_inventory():
    sql = """SELECT department_abbrev, department_name, inventory_abbrev
        FROM Departments, Inventories
        WHERE Departments.inventory_id = Inventories.id"""
    return db.session.execute(sql).fetchall()


def get_department(department_id):
    sql = "SELECT department_abbrev, department_name FROM Departments WHERE id = :department_id"
    return db.session.execute(sql, {"department_id":department_id}).fetchone()


def add_department(abbrev, name, inventory_id):
    try:
        sql = """INSERT INTO Departments (department_abbrev, department_name, inventory_id)
            VALUES (:abbrev, :name, :inventory_id)"""
        db.session.execute(
            sql, {"abbrev":abbrev, "name":name, "inventory_id":inventory_id})
        db.session.commit()
    except:
        return False
    return True


def get_inventories():
    sql = "SELECT id, inventory_abbrev, inventory_name FROM Inventories"
    return db.session.execute(sql).fetchall()

def get_inventory_abbrev(inventory_id):
    sql = "SELECT inventory_abbrev FROM Inventories WHERE id = :inventory_id"
    return db.session.execute(sql, {"inventory_id":inventory_id}).fetchone()

def get_inventory_abbrev_name(inventory_id):
    sql = "SELECT inventory_abbrev, inventory_name FROM Inventories WHERE id = :inventory_id"
    return db.session.execute(sql, {"inventory_id":inventory_id}).fetchone()

def add_inventory(abbrev, name):
    try:
        sql = """INSERT INTO Inventories (inventory_abbrev, inventory_name)
            VALUES (:abbrev, :name)"""
        db.session.execute(sql, {"abbrev":abbrev, "name":name})
        db.session.commit()
    except:
        return False
    return True

def get_product_codes():
    sql = "SELECT id, prod_code_abbrev, prod_code_name FROM Product_codes"
    return db.session.execute(sql).fetchall()

def get_prod_abbrev_name(prod_code_id):
    sql = "SELECT prod_code_abbrev, prod_code_name FROM Product_codes WHERE id = :prod_code_id"
    return db.session.execute(sql, {"prod_code_id":prod_code_id}).fetchone()

def add_product_code(abbrev, name):
    try:
        sql = """INSERT INTO Product_codes (prod_code_abbrev, prod_code_name)
            VALUES (:abbrev, :name)"""
        db.session.execute(sql, {"abbrev":abbrev, "name":name})
        db.session.commit()
    except:
        return False
    return True
