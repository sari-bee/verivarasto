from db import db

def get_departments():
    sql = """SELECT department_abbrev, department_name, inventory_abbrev
        FROM Departments, Inventories
        WHERE Departments.inventory_id = Inventories.id"""
    return db.session.execute(sql).fetchall()

def get_department_by_abbrev(abbrev):
    sql = "SELECT id FROM Departments WHERE department_abbrev = :abbrev"
    return db.session.execute(sql, {"abbrev":abbrev}).fetchone()

def add_department(abbrev, name, inventory_id):
    try:
        sql = """INSERT INTO Departments (department_abbrev, department_name, inventory_id) 
            VALUES (:abbrev, :name, :inventory_id)"""
        db.session.execute(sql, {"abbrev":abbrev, "name":name, "inventory_id":inventory_id})
        db.session.commit()
    except:
        return False
    return True

def get_inventories():
    sql = "SELECT inventory_abbrev, inventory_name FROM Inventories"
    return db.session.execute(sql).fetchall()

def get_inventory_by_abbrev(abbrev):
    sql = "SELECT id FROM Inventories WHERE inventory_abbrev = :abbrev"
    return db.session.execute(sql, {"abbrev":abbrev}).fetchone()

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
    sql = "SELECT prod_code_abbrev, prod_code_name FROM Product_codes"
    return db.session.execute(sql).fetchall()

def get_product_code_by_abbrev(abbrev):
    sql = "SELECT id FROM Product_codes WHERE prod_code_abbrev = :abbrev"
    return db.session.execute(sql, {"abbrev":abbrev}).fetchone()

def add_product_code(abbrev, name):
    try:
        sql = """INSERT INTO Product_codes (prod_code_abbrev, prod_code_name) 
            VALUES (:abbrev, :name)"""
        db.session.execute(sql, {"abbrev":abbrev, "name":name})
        db.session.commit()
    except:
        return False
    return True