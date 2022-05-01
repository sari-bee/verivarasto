from flask import render_template, redirect, request, flash
from app import app
import product
import status
import maintenance_functions
import user
import search
import transfusion

@app.route("/inventory")
def inventory():
    if not user.check_user_role(1):
        return redirect("/")
    status.set_as_expired()
    inventories = maintenance_functions.get_inventories()
    products = search.get_products_by_status("Käytettävissä")
    listing_type = "Käytettävissä olevat valmisteet"
    if products == []:
        search_message = "Ei hakuehtojen mukaisia valmisteita"
    else:
        search_message = ""
    return render_template("inventory.html", products=products, listing_type=listing_type,
                           inventories=inventories, search_message=search_message)


@app.route("/getproductsbyinventory", methods=["POST"])
def getproductsbyinventory():
    if not user.check_user_role(1):
        return redirect("/")
    inventories = maintenance_functions.get_inventories()
    inventory_id = request.form["inventory_id"].strip()
    if inventory_id == "all":
        products = search.get_all_products()
        listing_type = "Kaikki valmisteet"
    else:
        products = search.get_products_by_inventory(inventory_id)
        inventory_abbrev = maintenance_functions.get_inventory_abbrev(
            inventory_id).inventory_abbrev
        listing_type = "Valmisteet varastossa " + inventory_abbrev
    if products == []:
        search_message = "Ei hakuehtojen mukaisia valmisteita"
    else:
        search_message = ""
    return render_template("inventory.html", products=products, listing_type=listing_type,
                           inventories=inventories, search_message=search_message)


@app.route("/getuseableprodbyinventory", methods=["POST"])
def getuseableprodbyinventory():
    if not user.check_user_role(1):
        return redirect("/")
    inventories = maintenance_functions.get_inventories()
    inventory_id = request.form["inventory_id"].strip()
    if inventory_id == "all":
        products = search.get_products_by_status("Käytettävissä")
        listing_type = "Käytettävissä olevat valmisteet"
    else:
        products = search.get_prod_by_status_and_inventory(
            "Käytettävissä", inventory_id)
        inventory_abbrev = maintenance_functions.get_inventory_abbrev(
            inventory_id).inventory_abbrev
        listing_type = "Käytettävissä olevat valmisteet varastossa " + inventory_abbrev
    if products == []:
        search_message = "Ei hakuehtojen mukaisia valmisteita"
    else:
        search_message = ""
    return render_template("inventory.html", products=products, listing_type=listing_type,
                           inventories=inventories, search_message=search_message)


@app.route("/getprodbybloodgroup", methods=["POST"])
def getprodbybloodgroup():
    if not user.check_user_role(1):
        return redirect("/")
    inventories = maintenance_functions.get_inventories()
    bloodgroup = request.form["bloodgroup"].strip()
    products = search.get_prod_by_status_and_bloodgroup(
        "Käytettävissä", bloodgroup)
    listing_type = "Käytettävissä olevat veriryhmän " + bloodgroup + " valmisteet"
    if products == []:
        search_message = "Ei hakuehtojen mukaisia valmisteita"
    else:
        search_message = ""
    return render_template("inventory.html", products=products, listing_type=listing_type,
                           inventories=inventories, search_message=search_message)


@app.route("/getproductbydonationnumber", methods=["POST"])
def getproductbydonationnumber():
    if not user.check_user_role(1):
        return redirect("/")
    inventories = maintenance_functions.get_inventories()
    donation_number = request.form["donation_number"].strip()
    listing_type = "Valmisteet haulla " + donation_number
    if len(donation_number) < 3 or len(donation_number) > 20:
        flash("Syötit väärän pituisen hakusanan")
        products = []
        search_message = ""
    else:
        products = search.get_product_by_donation_number(donation_number)
        if products == []:
            search_message = "Ei hakuehtojen mukaisia valmisteita"
        else:
            search_message = ""
    return render_template("inventory.html", products=products, listing_type=listing_type,
                           inventories=inventories, search_message=search_message)


@app.route("/products")
def products():
    if not user.check_user_role(1):
        return redirect("/")
    inventories = maintenance_functions.get_inventories()
    product_codes = maintenance_functions.get_product_codes()
    products = product.get_useable_product_listing()
    sent_products = product.get_sent_products()
    return render_template("products.html", product_codes=product_codes,
                           inventories=inventories, products=products, sent_products=sent_products)


@app.route("/addproduct", methods=["POST"])
def addproduct():
    if not user.check_user_role(1):
        return redirect("/")
    csrf_token = request.form["csrf_token"]
    if not user.check_csrf_token(csrf_token):
        return redirect("/")
    donation_number = request.form["donation_number"].strip()
    prod_code_id = request.form["product_code_id"].strip()
    bloodgroup = request.form["bloodgroup"].strip()
    phenotypes = request.form["phenotypes"].strip()
    use_before = request.form["use_before"].strip()
    inventory_id = request.form["inventory_id"].strip()
    if len(donation_number) < 3 or len(donation_number) > 20 or len(phenotypes) > 200:
        flash("Syötit väärän pituisen syötteen")
    elif not product.add_product(donation_number, prod_code_id, bloodgroup, phenotypes, use_before):
        flash("Valmisteen lisääminen ei onnistunut. Onko valmiste jo varastossa?")
    else:
        product_id = product.get_product_id(donation_number).id
        product.add_inventory_product(
            product_id, inventory_id, "Käytettävissä")
        status.set_as_expired()
        inventory_abbrev = maintenance_functions.get_inventory_abbrev(
            inventory_id).inventory_abbrev
        user.add_to_log(
            f"Lisättiin valmiste {donation_number} varastoon {inventory_abbrev}")
        flash(f"Valmiste {donation_number} lisätty onnistuneesti!")
    return redirect("/products")


@app.route("/destroyproduct", methods=["POST"])
def destroyproduct():
    if not user.check_user_role(1):
        return redirect("/")
    csrf_token = request.form["csrf_token"]
    if not user.check_csrf_token(csrf_token):
        return redirect("/")
    product_id = request.form["product_id"].strip()
    reason = request.form["reason"]
    if len(reason) < 3 or len(reason) > 100:
        flash("Syötit väärän pituisen syötteen")
    else:
        status.set_new_status("Hävitetty", product_id)
        donation_number = product.get_donation_number(
            product_id).donation_number
        user.add_to_log(
            f"Hävitettiin valmiste {donation_number}, syy: {reason}")
        flash(f"Valmiste {donation_number} hävitetty")
    return redirect("/products")

@app.route("/returnproduct", methods=["POST"])
def returnproduct():
    if not user.check_user_role(1):
        return redirect("/")
    csrf_token = request.form["csrf_token"]
    if not user.check_csrf_token(csrf_token):
        return redirect("/")
    return_product_id = request.form["return_product_id"].strip()
    transfusion_id = transfusion.get_transfusion_by_product(return_product_id)[0]
    if not transfusion.remove_transfusion(transfusion_id):
        flash("Valmistetta ei voida palauttaa.")
    else:
        status.set_new_status("Käytettävissä", return_product_id)         
        donation_number = product.get_donation_number(return_product_id).donation_number
        user.add_to_log(
            f"Palautettiin valmiste {donation_number} varastoon")
        flash(f"Valmiste {donation_number} palautettu varastoon")
    return redirect("/products")

@app.route("/moveproduct", methods=["POST"])
def moveproduct():
    if not user.check_user_role(1):
        return redirect("/")
    csrf_token = request.form["csrf_token"]
    if not user.check_csrf_token(csrf_token):
        return redirect("/")
    product_id = request.form["product_id"].strip()
    new_inventory_id = request.form["new_inventory_id"].strip()
    product.change_inventories(product_id, new_inventory_id)
    inventory_abbrev = maintenance_functions.get_inventory_abbrev(
        new_inventory_id).inventory_abbrev
    donation_number = product.get_donation_number(product_id).donation_number
    user.add_to_log(
        f"Siirrettiin valmiste {donation_number} varastoon {inventory_abbrev}")
    flash(f"Valmiste {donation_number} siirretty varastoon {inventory_abbrev}")
    return redirect("/products")
