from datetime import date
from app import app, db
from flask import render_template, request, redirect

@app.route("/inventory")
def inventory():
    new_status = "Vanhentunut"
    old_status = "Käytettävissä"
    today = date.today()
    sql = """UPDATE Inventory_products SET status = :new_status 
        WHERE product_id IN (SELECT id FROM Products WHERE use_before < :today) AND status = :old_status"""
    db.session.execute(sql, {"new_status":new_status, "today":today, "old_status":old_status})
    db.session.commit()
    sql = "SELECT inventory_abbrev, inventory_name FROM Inventories"
    inventories = db.session.execute(sql).fetchall()
    sql = """SELECT donation_number, prod_code_abbrev, bloodgroup, phenotypes, use_before, inventory_abbrev, status
        FROM Products, Product_codes, Inventory_products, Inventories WHERE Products.product_code_id = Product_codes.id
        AND Products.id = Inventory_products.product_id AND Inventories.id = Inventory_products.inventory_id
        AND status = :old_status"""
    products = db.session.execute(sql, {"old_status":old_status}).fetchall()
    message = "Käytettävissä olevat valmisteet"
    return render_template("inventory.html", products=products, message=message, inventories=inventories)

@app.route("/getproducts", methods=["POST"])
def getproducts():
    sql = "SELECT inventory_abbrev, inventory_name FROM Inventories"
    inventories = db.session.execute(sql).fetchall()
    status = "Käytettävissä"
    sql = """SELECT donation_number, prod_code_abbrev, bloodgroup, phenotypes, use_before, inventory_abbrev, status
        FROM Products, Product_codes, Inventory_products, Inventories WHERE Products.product_code_id = Product_codes.id
        AND Products.id = Inventory_products.product_id AND Inventories.id = Inventory_products.inventory_id
        AND status = :status"""
    products = db.session.execute(sql, {"status":status}).fetchall()
    message = "Käytettävissä olevat valmisteet"
    return render_template("inventory.html", products=products, message=message, inventories=inventories)

@app.route("/getallproducts", methods=["POST"])
def getallproducts():
    sql = """SELECT donation_number, prod_code_abbrev, bloodgroup, phenotypes, use_before, inventory_abbrev, status
        FROM Products, Product_codes, Inventory_products, Inventories WHERE Products.product_code_id = Product_codes.id
        AND Products.id = Inventory_products.product_id AND Inventories.id = Inventory_products.inventory_id"""
    products = db.session.execute(sql).fetchall()
    sql = "SELECT inventory_abbrev, inventory_name FROM Inventories"
    inventories = db.session.execute(sql).fetchall()
    message = "Kaikki valmisteet"
    return render_template("inventory.html", products=products, message=message, inventories=inventories)

@app.route("/getproductsbyinventory", methods=["POST"])
def getproductsbyinventory():
    inventory_abbrev = request.form["inventory_abbrev"]
    sql = "SELECT id FROM Inventories WHERE inventory_abbrev = :inventory_abbrev"
    inventory_id = db.session.execute(sql, {"inventory_abbrev":inventory_abbrev}).fetchone()[0]
    sql = """SELECT donation_number, prod_code_abbrev, bloodgroup, phenotypes, use_before, inventory_abbrev, status
        FROM Products, Product_codes, Inventory_products, Inventories WHERE Products.product_code_id = Product_codes.id
        AND Products.id = Inventory_products.product_id AND Inventories.id = Inventory_products.inventory_id
        AND Inventories.id = :inventory_id"""
    products = db.session.execute(sql, {"inventory_id":inventory_id}).fetchall()
    sql = "SELECT inventory_abbrev, inventory_name FROM Inventories"
    inventories = db.session.execute(sql).fetchall()
    message = "Valmisteet varastossa " + inventory_abbrev
    return render_template("inventory.html", products=products, message=message, inventories=inventories)

@app.route("/getproductbydonationnumber", methods=["POST"])
def getproductbydonationnumber():
    sql = "SELECT inventory_abbrev, inventory_name FROM Inventories"
    inventories = db.session.execute(sql).fetchall()
    donation_number = request.form["donation_number"]
    sql = """SELECT donation_number, prod_code_abbrev, bloodgroup, phenotypes, use_before, inventory_abbrev, status
        FROM Products, Product_codes, Inventory_products, Inventories WHERE Products.product_code_id = Product_codes.id
        AND Products.id = Inventory_products.product_id AND Inventories.id = Inventory_products.inventory_id 
        AND donation_number = :donation_number"""
    products = db.session.execute(sql, {"donation_number":donation_number}).fetchall()
    message = "Valmiste " + donation_number
    return render_template("inventory.html", products=products, message=message, inventories=inventories)