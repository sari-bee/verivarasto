from app import app
from flask import render_template, redirect, request
import maintenance_functions, user

@app.route("/maintenance")
def maintenance():
    user.check_user_role(1)
    product_codes = maintenance_functions.get_product_codes()
    inventories = maintenance_functions.get_inventories()
    departments = maintenance_functions.get_departments()
    return render_template("maintenance.html", product_codes=product_codes, inventories=inventories, departments=departments)

@app.route("/addinventory", methods=["POST"])
def addinventory():
    user.check_user_role(1)
    csrf_token = request.form["csrf_token"]
    user.check_csrf_token(csrf_token)
    inventory_abbrev = request.form["inventory_abbrev"]
    inventory_name = request.form["inventory_name"]
    try:
        maintenance_functions.add_inventory(inventory_abbrev, inventory_name)
    except:
        print("Virhe")
    return redirect("/maintenance")

@app.route("/adddepartment", methods=["POST"])
def adddepartment():
    user.check_user_role(1)
    csrf_token = request.form["csrf_token"]
    user.check_csrf_token(csrf_token)
    department_abbrev = request.form["department_abbrev"]
    department_name = request.form["department_name"]
    inventory_abbrev = request.form["inventory_abbrev"]
    inventory_id = maintenance_functions.get_inventory_by_abbrev(inventory_abbrev)[0]
    try:
        maintenance_functions.add_department(department_abbrev, department_name, inventory_id)
    except:
        print("Virhe")
    return redirect("/maintenance")

@app.route("/addproductcode", methods=["POST"])
def addproductcode():
    user.check_user_role(1)
    csrf_token = request.form["csrf_token"]
    user.check_csrf_token(csrf_token)
    prod_code_abbrev = request.form["prod_code_abbrev"]
    prod_code_name = request.form["prod_code_name"]
    try:
        maintenance_functions.add_product_code(prod_code_abbrev, prod_code_name)
    except:
        print("Virhe")
    return redirect("/maintenance")