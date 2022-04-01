from app import app, db
from flask import render_template, request, redirect

@app.route("/maintenance")
def maintenance():
    sql = "SELECT prod_code_abbrev, prod_code_name FROM Product_codes"
    product_codes = db.session.execute(sql).fetchall()
    sql = "SELECT inventory_abbrev, inventory_name FROM Inventories"
    inventories = db.session.execute(sql).fetchall()
    sql = """SELECT department_abbrev, department_name, inventory_abbrev FROM Departments, Inventories 
        WHERE Departments.inventory_id = Inventories.id"""
    departments = db.session.execute(sql).fetchall()
    return render_template("maintenance.html", product_codes=product_codes, inventories=inventories, departments=departments)

@app.route("/addinventory", methods=["POST"])
def addinventory():
    inventory_abbrev = request.form["inventory_abbrev"]
    inventory_name = request.form["inventory_name"]
    try:
        sql = """INSERT INTO Inventories (inventory_abbrev, inventory_name) 
            VALUES (:inventory_abbrev, :inventory_name)"""
        db.session.execute(sql, {"inventory_abbrev":inventory_abbrev, "inventory_name":inventory_name})
        db.session.commit()
    except:
        print("Unique constraint failed")
    return redirect("/maintenance")

@app.route("/adddepartment", methods=["POST"])
def adddepartment():
    department_abbrev = request.form["department_abbrev"]
    department_name = request.form["department_name"]
    inventory_abbrev = request.form["inventory_abbrev"]
    sql = "SELECT id FROM Inventories WHERE inventory_abbrev = :inventory_abbrev"
    inventory_id = db.session.execute(sql, {"inventory_abbrev":inventory_abbrev}).fetchone()[0]
    try:
        sql = """INSERT INTO Departments (department_abbrev, department_name, inventory_id) 
            VALUES (:department_abbrev, :department_name, :inventory_id)"""
        db.session.execute(sql, {"department_abbrev":department_abbrev, "department_name":department_name, "inventory_id":inventory_id})
        db.session.commit()
    except:
        print("Unique constraint failed")
    return redirect("/maintenance")

@app.route("/addproductcode", methods=["POST"])
def addproductcode():
    prod_code_abbrev = request.form["prod_code_abbrev"]
    prod_code_name = request.form["prod_code_name"]
    try:
        sql = """INSERT INTO Product_codes (prod_code_abbrev, prod_code_name) 
            VALUES (:prod_code_abbrev, :prod_code_name)"""
        db.session.execute(sql, {"prod_code_abbrev":prod_code_abbrev, "prod_code_name":prod_code_name})
        db.session.commit()
    except:
        print("Unique constraint failed")
    return redirect("/maintenance")