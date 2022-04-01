from app import app, db
from flask import render_template, request, redirect

@app.route("/patients")
def patients():
    sql = "SELECT ssn, patient_name FROM Patients"
    patients = db.session.execute(sql).fetchall()
    return render_template("patients.html", patients=patients)

@app.route("/addpatient", methods=["POST"])
def addpatient():
    ssn = request.form["ssn"]
    patient_name = request.form["patient_name"]
    bloodgroup = request.form["bloodgroup"]
    phenotype_reqs = request.form["phenotype_reqs"]
    try:
        sql = """INSERT INTO Patients (ssn, patient_name, bloodgroup, phenotype_reqs) 
            VALUES (:ssn, :patient_name, :bloodgroup, :phenotype_reqs)"""
        db.session.execute(sql, {"ssn":ssn, "patient_name":patient_name, "bloodgroup":bloodgroup, "phenotype_reqs":phenotype_reqs})
        db.session.commit()
    except:
        print("Unique constraint failed")
    return redirect("/patients")

@app.route("/getpatienttransfusions", methods=["POST"])
def getpatienttransfusions():
    sql = "SELECT ssn, patient_name, bloodgroup, phenotype_reqs FROM Patients"
    patients = db.session.execute(sql).fetchall()
    patient_ssn = request.form["patient_ssn"]
    sql = "SELECT id, ssn, patient_name, bloodgroup, phenotype_reqs FROM Patients WHERE ssn = :patient_ssn"
    patient_by_ssn = db.session.execute(sql, {"patient_ssn":patient_ssn}).fetchone()
    patient_id = patient_by_ssn[0]
    sql = """SELECT donation_number, prod_code_abbrev, prod_code_name, date, department_abbrev FROM Transfusions, Products, Product_codes, Departments
        WHERE Transfusions.product_id = Products.id AND Products.product_code_id = Product_codes.id
        AND Departments.id = Transfusions.department_id AND patient_id = :patient_id"""
    patienttransfusions = db.session.execute(sql, {"patient_id":patient_id}).fetchall()
    return render_template("patientquery.html", patients=patients, patienttransfusions=patienttransfusions, patient_by_ssn=patient_by_ssn)