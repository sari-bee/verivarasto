from app import app, db
from flask import render_template, request, redirect

@app.route("/products")
def products():
    sql = "SELECT inventory_abbrev, inventory_name FROM Inventories"
    inventories = db.session.execute(sql).fetchall()
    sql = "SELECT prod_code_abbrev, prod_code_name FROM Product_codes"
    product_codes = db.session.execute(sql).fetchall()
    return render_template("products.html", product_codes=product_codes, inventories=inventories)

@app.route("/addproduct", methods=["POST"])
def addproduct():
    donation_number = request.form["donation_number"]
    prod_code_abbrev = request.form["prod_code_abbrev"]
    sql = "SELECT id FROM Product_codes WHERE prod_code_abbrev = :prod_code_abbrev"
    product_code_id = db.session.execute(sql, {"prod_code_abbrev":prod_code_abbrev}).fetchone()[0]
    bloodgroup = request.form["bloodgroup"]
    phenotypes = request.form["phenotypes"]
    use_before = request.form["use_before"]
    try:
        sql = """INSERT INTO Products (donation_number, product_code_id, bloodgroup, phenotypes, use_before) 
            VALUES (:donation_number, :product_code_id, :bloodgroup, :phenotypes, :use_before)"""
        db.session.execute(sql, {"donation_number":donation_number, "product_code_id":product_code_id, "bloodgroup":bloodgroup, "phenotypes":phenotypes, "use_before":use_before})
        db.session.commit()
        sql = "SELECT id FROM Products WHERE donation_number = :donation_number"
        product_id = db.session.execute(sql, {"donation_number":donation_number}).fetchone()[0]
        inventory_abbrev = request.form["inventory_abbrev"]
        sql = "SELECT id FROM Inventories WHERE inventory_abbrev = :inventory_abbrev"
        inventory_id = db.session.execute(sql, {"inventory_abbrev":inventory_abbrev}).fetchone()[0]
        status = "Käytettävissä"
        sql = """INSERT INTO Inventory_products (product_id, inventory_id, status) 
            VALUES (:product_id, :inventory_id, :status)"""
        db.session.execute(sql, {"product_id":product_id, "inventory_id":inventory_id, "status":status})
        db.session.commit()
    except:
        print("Unique constraint failed")
    return redirect("/inventory")