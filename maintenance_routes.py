from app import app
from flask import render_template, redirect, request, flash
import maintenance_functions, user

@app.route("/maintenance")
def maintenance():
    user.check_user_role(1)
    product_codes = maintenance_functions.get_product_codes()
    inventories = maintenance_functions.get_inventories()
    departments = maintenance_functions.get_departments_and_inventory()
    return render_template("maintenance.html", product_codes=product_codes, inventories=inventories, departments=departments)

@app.route("/addinventory", methods=["POST"])
def addinventory():
    user.check_user_role(1)
    csrf_token = request.form["csrf_token"]
    user.check_csrf_token(csrf_token)
    inventory_abbrev = request.form["inventory_abbrev"]
    inventory_name = request.form["inventory_name"]
    if len(inventory_abbrev) < 3 or len(inventory_abbrev) > 10 or len(inventory_name) < 3 or len(inventory_name) > 50:
        flash("Syötit väärän pituisen syötteen")
    elif not maintenance_functions.add_inventory(inventory_abbrev, inventory_name):
        flash("Varasto on jo olemassa")
    else:
        user.add_to_log(f"Lisättiin varasto {inventory_abbrev}")
    return redirect("/maintenance")

@app.route("/adddepartment", methods=["POST"])
def adddepartment():
    user.check_user_role(1)
    csrf_token = request.form["csrf_token"]
    user.check_csrf_token(csrf_token)
    department_abbrev = request.form["department_abbrev"]
    department_name = request.form["department_name"]
    inventory_id = request.form["inventory_id"]
    if len(department_abbrev) < 3 or len(department_abbrev) > 10 or len(department_name) < 3 or len(department_name) > 50:
        flash("Syötit väärän pituisen syötteen")  
    elif not maintenance_functions.add_department(department_abbrev, department_name, inventory_id):
        flash("Hoitoyksikkö on jo olemassa")
    else:
        user.add_to_log(f"Lisättiin hoitoyksikkö {department_abbrev}")
    return redirect("/maintenance")

@app.route("/addproductcode", methods=["POST"])
def addproductcode():
    user.check_user_role(1)
    csrf_token = request.form["csrf_token"]
    user.check_csrf_token(csrf_token)
    prod_code_abbrev = request.form["prod_code_abbrev"]
    prod_code_name = request.form["prod_code_name"]
    if len(prod_code_abbrev) < 3 or len(prod_code_abbrev) > 10 or len(prod_code_name) < 3 or len(prod_code_name) > 50:
        flash("Syötit väärän pituisen syötteen")  
    elif not maintenance_functions.add_product_code(prod_code_abbrev, prod_code_name):
        flash("Valmistetyyppi on jo olemassa")
    else:
        user.add_to_log(f"Lisättiin valmistetyyppi {prod_code_abbrev}")
    return redirect("/maintenance")