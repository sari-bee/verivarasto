from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/productcodes")
def productcodes():
    sql = "SELECT * FROM Product_codes"
    product_codes = db.session.execute(sql).fetchall()
    return render_template("productcodes.html", product_codes=product_codes)

@app.route("/addproductcode", methods=["POST"])
def addproductcode():
    prod_code_abbrev = request.form["prod_code_abbrev"]
    prod_code_name = request.form["prod_code_name"]
    sql = "INSERT INTO Product_codes (prod_code_abbrev, prod_code_name) VALUES (:prod_code_abbrev, :prod_code_name)"
    db.session.execute(sql, {"prod_code_abbrev":prod_code_abbrev, "prod_code_name":prod_code_name})
    db.session.commit()
    return redirect("/productcodes")

@app.route("/products")
def products():
    sql = "SELECT inventory_abbrev FROM Inventories"
    inventories = db.session.execute(sql).fetchall()
    sql = "SELECT prod_code_abbrev FROM Product_codes"
    product_codes = db.session.execute(sql).fetchall()
    sql = "SELECT * FROM Products JOIN Product_codes ON Products.product_code_id = Product_codes.id"
    products = db.session.execute(sql).fetchall()
    return render_template("products.html", product_codes=product_codes, products=products, inventories=inventories)

@app.route("/addproduct", methods=["POST"])
def addproduct():
    donation_number = request.form["donation_number"]
    prod_code_abbrev = request.form["prod_code_abbrev"]
    sql = "SELECT * FROM Product_codes WHERE prod_code_abbrev = :prod_code_abbrev"
    product_code_id = db.session.execute(sql, {"prod_code_abbrev":prod_code_abbrev}).fetchone()[0]
    bloodgroup = request.form["bloodgroup"]
    phenotypes = request.form["phenotypes"]
    use_before = request.form["use_before"]
    sql = "INSERT INTO Products (donation_number, product_code_id, bloodgroup, phenotypes, use_before) VALUES (:donation_number, :product_code_id, :bloodgroup, :phenotypes, :use_before)"
    db.session.execute(sql, {"donation_number":donation_number, "product_code_id":product_code_id, "bloodgroup":bloodgroup, "phenotypes":phenotypes, "use_before":use_before})
    db.session.commit()
    sql = "SELECT * FROM Products WHERE donation_number = :donation_number"
    product_id = db.session.execute(sql, {"donation_number":donation_number}).fetchone()[0]
    inventory_abbrev = request.form["inventory_abbrev"]
    sql = "SELECT * FROM Inventories WHERE inventory_abbrev = :inventory_abbrev"
    inventory_id = db.session.execute(sql, {"inventory_abbrev":inventory_abbrev}).fetchone()[0]
    status = "Käytettävissä"
    sql = "INSERT INTO Inventory_products (product_id, inventory_id, status) VALUES (:product_id, :inventory_id, :status)"
    db.session.execute(sql, {"product_id":product_id, "inventory_id":inventory_id, "status":status})
    db.session.commit()
    return redirect("/products")

@app.route("/patients")
def patients():
    sql = "SELECT * FROM Patients"
    patients = db.session.execute(sql).fetchall()
    return render_template("patients.html", patients=patients)

@app.route("/addpatient", methods=["POST"])
def addpatient():
    ssn = request.form["ssn"]
    patient_name = request.form["patient_name"]
    bloodgroup = request.form["bloodgroup"]
    phenotype_reqs = request.form["phenotype_reqs"]
    sql = "INSERT INTO Patients (ssn, patient_name, bloodgroup, phenotype_reqs) VALUES (:ssn, :patient_name, :bloodgroup, :phenotype_reqs)"
    db.session.execute(sql, {"ssn":ssn, "patient_name":patient_name, "bloodgroup":bloodgroup, "phenotype_reqs":phenotype_reqs})
    db.session.commit()
    return redirect("/patients")

@app.route("/inventories")
def inventories():
    sql = "SELECT * FROM Inventories"
    inventories = db.session.execute(sql).fetchall()
    return render_template("inventories.html", inventories=inventories)

@app.route("/addinventory", methods=["POST"])
def addinventory():
    inventory_abbrev = request.form["inventory_abbrev"]
    inventory_name = request.form["inventory_name"]
    sql = "INSERT INTO Inventories (inventory_abbrev, inventory_name) VALUES (:inventory_abbrev, :inventory_name)"
    db.session.execute(sql, {"inventory_abbrev":inventory_abbrev, "inventory_name":inventory_name})
    db.session.commit()
    return redirect("/inventories")

@app.route("/departments")
def departments():
    sql = "SELECT inventory_abbrev FROM Inventories"
    inventories = db.session.execute(sql).fetchall()
    sql = "SELECT * FROM Departments JOIN Inventories ON Departments.inventory_id = Inventories.id"
    departments = db.session.execute(sql).fetchall()
    return render_template("departments.html", inventories=inventories, departments=departments)

@app.route("/adddepartment", methods=["POST"])
def adddepartment():
    department_abbrev = request.form["department_abbrev"]
    department_name = request.form["department_name"]
    inventory_abbrev = request.form["inventory_abbrev"]
    sql = "SELECT * FROM Inventories WHERE inventory_abbrev = :inventory_abbrev"
    inventory_id = db.session.execute(sql, {"inventory_abbrev":inventory_abbrev}).fetchone()[0]
    sql = "INSERT INTO Departments (department_abbrev, department_name, inventory_id) VALUES (:department_abbrev, :department_name, :inventory_id)"
    db.session.execute(sql, {"department_abbrev":department_abbrev, "department_name":department_name, "inventory_id":inventory_id})
    db.session.commit()
    return redirect("/departments")

@app.route("/transfusions")
def transfusions():
    sql = "SELECT donation_number FROM Products"
    products = db.session.execute(sql).fetchall()
    sql = "SELECT ssn FROM Patients"
    patients = db.session.execute(sql).fetchall()
    sql = "SELECT department_abbrev FROM Departments"
    departments = db.session.execute(sql).fetchall()
    sql = "SELECT * FROM Transfusions, Patients, Products, Product_codes, Departments WHERE Transfusions.department_id = Departments.id AND Transfusions.patient_id = Patients.id AND Transfusions.product_id = Products.id AND Products.product_code_id = Product_codes.id"
    transfusions = db.session.execute(sql).fetchall()
    return render_template("transfusions.html", products=products, patients=patients, departments=departments, transfusions=transfusions)

@app.route("/addtransfusion", methods=["POST"])
def addtransfusion():
    product_donation_number = request.form["product_donation_number"]
    sql = "SELECT * FROM Products WHERE donation_number = :product_donation_number"
    product_id = db.session.execute(sql, {"product_donation_number":product_donation_number}).fetchone()[0]
    patient_ssn = request.form["patient_ssn"]
    sql = "SELECT * FROM Patients WHERE ssn = :patient_ssn"
    patient_id = db.session.execute(sql, {"patient_ssn":patient_ssn}).fetchone()[0]
    department_abbrev = request.form["department_abbrev"]
    sql = "SELECT * FROM Departments WHERE department_abbrev = :department_abbrev"
    department_id = db.session.execute(sql, {"department_abbrev":department_abbrev}).fetchone()[0]
    date = request.form["date"]
    sql = "INSERT INTO Transfusions (product_id, patient_id, department_id, date) VALUES (:product_id, :patient_id, :department_id, :date)"
    db.session.execute(sql, {"product_id":product_id, "patient_id":patient_id, "department_id":department_id, "date":date})
    db.session.commit()
    return redirect("/transfusions")