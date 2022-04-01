from app import app, db
from flask import render_template, request, redirect

@app.route("/transfusions")
def transfusions():
    status_ok = "Käytettävissä"
    sql = """SELECT donation_number, prod_code_abbrev, bloodgroup FROM Products, Product_codes, Inventory_products 
        WHERE Products.product_code_id = Product_codes.id 
            AND Inventory_products.product_id = Products.id AND status = :status_ok"""
    products = db.session.execute(sql, {"status_ok":status_ok}).fetchall()
    sql = "SELECT ssn, patient_name FROM Patients"
    patients = db.session.execute(sql).fetchall()
    sql = "SELECT department_abbrev, department_name FROM Departments"
    departments = db.session.execute(sql).fetchall()
    sql = """SELECT ssn, patient_name, donation_number, prod_code_abbrev, department_abbrev, date FROM Transfusions, Patients, Products, Product_codes, Departments 
        WHERE Transfusions.department_id = Departments.id AND Transfusions.patient_id = Patients.id 
            AND Transfusions.product_id = Products.id AND Products.product_code_id = Product_codes.id"""
    transfusions = db.session.execute(sql).fetchall()
    return render_template("transfusions.html", products=products, patients=patients, departments=departments, transfusions=transfusions)

@app.route("/addtransfusion", methods=["POST"])
def addtransfusion():
    product_donation_number = request.form["product_donation_number"]
    sql = "SELECT id FROM Products WHERE donation_number = :product_donation_number"
    product_id = db.session.execute(sql, {"product_donation_number":product_donation_number}).fetchone()[0]
    patient_ssn = request.form["patient_ssn"]
    sql = "SELECT id FROM Patients WHERE ssn = :patient_ssn"
    patient_id = db.session.execute(sql, {"patient_ssn":patient_ssn}).fetchone()[0]
    department_abbrev = request.form["department_abbrev"]
    sql = "SELECT id FROM Departments WHERE department_abbrev = :department_abbrev"
    department_id = db.session.execute(sql, {"department_abbrev":department_abbrev}).fetchone()[0]
    date = request.form["date"]
    try:
        sql = """INSERT INTO Transfusions (product_id, patient_id, department_id, date) 
            VALUES (:product_id, :patient_id, :department_id, :date)"""
        db.session.execute(sql, {"product_id":product_id, "patient_id":patient_id, "department_id":department_id, "date":date})
        db.session.commit()
        new_status = "Siirretty"
        sql = "UPDATE Inventory_products SET status = :new_status WHERE product_id = :product_id"
        db.session.execute(sql, {"new_status":new_status, "product_id":product_id})
        db.session.commit()
    except:
        print("Unique constraint failed")
    return redirect("/transfusions")