from app import app
from flask import render_template, redirect, request
import product, status, maintenance_functions, user

@app.route("/inventory")
def inventory():
    user.check_user_role(1)
    status.set_as_expired()
    return redirect("/getproducts")

@app.route("/getproducts")
def getproducts():
    user.check_user_role(1)
    inventories = maintenance_functions.get_inventories()
    product_status = "Käytettävissä"
    products = product.get_products_by_status(product_status)
    message = "Käytettävissä olevat valmisteet"
    return render_template("inventory.html", products=products, message=message, inventories=inventories)

@app.route("/getallproducts")
def getallproducts():
    user.check_user_role(1)
    inventories = maintenance_functions.get_inventories()
    products = product.get_all_products()
    message = "Kaikki valmisteet"
    return render_template("inventory.html", products=products, message=message, inventories=inventories)

@app.route("/getproductsbyinventory", methods=["POST"])
def getproductsbyinventory():
    user.check_user_role(1)
    inventory_abbrev = request.form["inventory_abbrev"]
    inventory_id = maintenance_functions.get_inventory_by_abbrev(inventory_abbrev)[0]
    products = product.get_products_by_inventory(inventory_id)
    inventories = maintenance_functions.get_inventories()
    message = "Valmisteet varastossa " + inventory_abbrev
    return render_template("inventory.html", products=products, message=message, inventories=inventories)

@app.route("/getproductbydonationnumber", methods=["POST"])
def getproductbydonationnumber():
    user.check_user_role(1)
    inventories = maintenance_functions.get_inventories()
    donation_number = request.form["donation_number"]
    if len(donation_number) < 3 or len(donation_number) > 20:
        return render_template("message.html", message="Syötit väärän pituisen hakusanan")   
    products = product.get_product_by_donation_number(donation_number)
    message = "Valmisteet haulla " + donation_number
    return render_template("inventory.html", products=products, message=message, inventories=inventories)

@app.route("/products")
def products():
    user.check_user_role(1)
    inventories = maintenance_functions.get_inventories()
    product_codes = maintenance_functions.get_product_codes()
    product_status = "Käytettävissä"
    products = product.get_products_by_status(product_status)
    return render_template("products.html", product_codes=product_codes, inventories=inventories, products=products)

@app.route("/addproduct", methods=["POST"])
def addproduct():
    user.check_user_role(1)
    csrf_token = request.form["csrf_token"]
    user.check_csrf_token(csrf_token)
    donation_number = request.form["donation_number"]
    prod_code_abbrev = request.form["prod_code_abbrev"]
    product_code_id = maintenance_functions.get_product_code_by_abbrev(prod_code_abbrev)[0]
    bloodgroup = request.form["bloodgroup"]
    phenotypes = request.form["phenotypes"]
    if len(donation_number) < 3 or len(donation_number) > 20 or len(phenotypes) > 200:
        return render_template("message.html", message="Syötit väärän pituisen syötteen")  
    use_before = request.form["use_before"]
    inventory_abbrev = request.form["inventory_abbrev"]
    inventory_id = maintenance_functions.get_inventory_by_abbrev(inventory_abbrev)[0]
    product_status = "Käytettävissä"
    if not product.add_product(donation_number, product_code_id, bloodgroup, phenotypes, use_before):
        return render_template("message.html", message="Valmisteen lisääminen ei onnistunut. Onko valmiste jo varastossa?")
    product_id = product.get_product_id(donation_number)
    product.add_inventory_product(product_id, inventory_id, product_status)
    user.add_to_log(f"Lisättiin valmiste {donation_number} varastoon {inventory_abbrev}")
    return redirect("/inventory")

@app.route("/destroyproduct", methods=["POST"])
def destroyproduct():
    user.check_user_role(1)
    csrf_token = request.form["csrf_token"]
    user.check_csrf_token(csrf_token)
    donation_number = request.form["product_donation_number"]
    product_id = product.get_product_id_by_donation_number(donation_number)[0]
    product_status = "Hävitetty"
    status.set_new_status(product_status, product_id)
    reason = request.form["reason"]
    if len(reason) < 3 or len(reason) > 100:
        return render_template("message.html", message="Syötit väärän pituisen syötteen")          
    user.add_to_log(f"Hävitettiin valmiste {donation_number}, syy: {reason}")
    return redirect("/inventory")

@app.route("/moveproduct", methods=["POST"])
def moveproduct():
    user.check_user_role(1)
    csrf_token = request.form["csrf_token"]
    user.check_csrf_token(csrf_token)
    donation_number = request.form["product_donation_number"]
    product_id = product.get_product_id_by_donation_number(donation_number)[0]
    new_inventory_abbrev = request.form["new_inventory_abbrev"]
    new_inventory_id = maintenance_functions.get_inventory_by_abbrev(new_inventory_abbrev)[0]
    product.change_inventories(product_id, new_inventory_id)
    user.add_to_log(f"Siirrettiin valmiste {donation_number} varastoon {new_inventory_abbrev}")
    return redirect("/inventory")