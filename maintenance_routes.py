from flask import render_template, redirect, request, flash
from app import app
import maintenance_functions
import user


@app.route("/maintenance")
def maintenance():
    if not user.check_user_role(1):
        return redirect("/")
    product_codes = maintenance_functions.get_product_codes()
    inventories = maintenance_functions.get_inventories()
    departments = maintenance_functions.get_departments_and_inventory()
    return render_template("maintenance.html", product_codes=product_codes,
                           inventories=inventories, departments=departments)


@app.route("/addinventory", methods=["POST"])
def addinventory():
    if not user.check_user_role(1):
        return redirect("/")
    csrf_token = request.form["csrf_token"]
    if not user.check_csrf_token(csrf_token):
        return redirect("/")
    product_codes = maintenance_functions.get_product_codes()
    inventories = maintenance_functions.get_inventories()
    departments = maintenance_functions.get_departments_and_inventory()
    inventory_abbrev = request.form["inventory_abbrev"].strip()
    inventory_name = request.form["inventory_name"].strip()
    if len(inventory_abbrev) < 3 or len(inventory_abbrev) > 10:
        flash("Syötit väärän pituisen varaston lyhenteen")
    elif len(inventory_name) < 3 or len(inventory_name) > 50:
        flash("Syötit väärän pituisen varaston nimen")
    elif not maintenance_functions.add_inventory(inventory_abbrev, inventory_name):
        flash("Varasto on jo olemassa")
    else:
        user.add_to_log(f"Lisättiin varasto {inventory_abbrev}")
        return redirect("/maintenance")
    return render_template("maintenance.html", product_codes=product_codes,
                           inventories=inventories, departments=departments)


@app.route("/adddepartment", methods=["POST"])
def adddepartment():
    if not user.check_user_role(1):
        return redirect("/")
    csrf_token = request.form["csrf_token"]
    if not user.check_csrf_token(csrf_token):
        return redirect("/")
    product_codes = maintenance_functions.get_product_codes()
    inventories = maintenance_functions.get_inventories()
    departments = maintenance_functions.get_departments_and_inventory()
    department_abbrev = request.form["department_abbrev"].strip()
    department_name = request.form["department_name"].strip()
    inventory_id = request.form["inventory_id"].strip()
    inventory_abbrev = maintenance_functions.get_inventory_abbrev_name(inventory_id)[0]
    inventory_name = maintenance_functions.get_inventory_abbrev_name(inventory_id)[1]
    if len(department_abbrev) < 3 or len(department_abbrev) > 10:
        flash("Syötit väärän pituisen hoitoyksikön lyhenteen")
    elif len(department_name) < 3 or len(department_name) > 50:
        flash("Syötit väärän pituisen hoitoyksikön nimen")
    elif not maintenance_functions.add_department(department_abbrev,
                                                  department_name, inventory_id):
        flash("Hoitoyksikkö on jo olemassa")
    else:
        user.add_to_log(f"Lisättiin hoitoyksikkö {department_abbrev}")
        return redirect("/maintenance")
    return render_template("maintenance.html", product_codes=product_codes,
                           inventories=inventories, departments=departments,
                           inventory_abbrev=inventory_abbrev, inventory_name=inventory_name)


@app.route("/addproductcode", methods=["POST"])
def addproductcode():
    if not user.check_user_role(1):
        return redirect("/")
    csrf_token = request.form["csrf_token"]
    if not user.check_csrf_token(csrf_token):
        return redirect("/")
    product_codes = maintenance_functions.get_product_codes()
    inventories = maintenance_functions.get_inventories()
    departments = maintenance_functions.get_departments_and_inventory()
    prod_code_abbrev = request.form["prod_code_abbrev"].strip()
    prod_code_name = request.form["prod_code_name"].strip()
    if len(prod_code_abbrev) < 3 or len(prod_code_abbrev) > 10:
        flash("Syötit väärän pituisen valmisteen lyhenteen")
    elif len(prod_code_name) < 3 or len(prod_code_name) > 50:
        flash("Syötit väärän pituisen valmisteen nimen")
    elif not maintenance_functions.add_product_code(prod_code_abbrev, prod_code_name):
        flash("Valmistetyyppi on jo olemassa")
    else:
        user.add_to_log(f"Lisättiin valmistetyyppi {prod_code_abbrev}")
        return redirect("/maintenance")
    return render_template("maintenance.html", product_codes=product_codes,
                           inventories=inventories, departments=departments)
