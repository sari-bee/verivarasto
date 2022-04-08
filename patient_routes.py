from app import app
from flask import render_template, redirect, request
import transfusion, product, status, patient, maintenance_functions, user

@app.route("/patients")
def patients():
    user.check_user_role(1)
    patients = patient.get_patients()
    return render_template("patients.html", patients=patients)

@app.route("/transfusions")
def transfusions():
    user.check_user_role(1)
    product_status = "Käytettävissä"
    products = product.get_products_by_status(product_status)
    patients = patient.get_patients()
    departments = maintenance_functions.get_departments()
    transfusions = transfusion.get_transfusions()
    return render_template("transfusions.html", products=products, patients=patients, departments=departments, transfusions=transfusions)

@app.route("/getpatienttransfusions", methods=["POST"])
def getpatienttransfusions():
    user.check_user_role(1)
    patients = patient.get_patients()
    ssn = request.form["patient_ssn"]
    patient_by_ssn = patient.get_patient_by_ssn(ssn)
    patient_transfusions = transfusion.get_transfusions_by_patient(patient_by_ssn[0])
    return render_template("patientquery.html", patients=patients, patient_transfusions=patient_transfusions, patient_by_ssn=patient_by_ssn)

@app.route("/addpatient", methods=["POST"])
def addpatient():
    user.check_user_role(1)
    csrf_token = request.form["csrf_token"]
    user.check_csrf_token(csrf_token)
    ssn = request.form["ssn"]
    patient_name = request.form["patient_name"]
    bloodgroup = request.form["bloodgroup"]
    phenotype_reqs = request.form["phenotype_reqs"]
    try:
        patient.add_patient(ssn, patient_name, bloodgroup, phenotype_reqs)
    except:
        print("Virhe")
    return redirect("/patients")

@app.route("/addtransfusion", methods=["POST"])
def addtransfusion():
    user.check_user_role(1)
    csrf_token = request.form["csrf_token"]
    user.check_csrf_token(csrf_token)
    donation_number = request.form["product_donation_number"]
    product_id = product.get_product_id_by_donation_number(donation_number)[0]
    ssn = request.form["patient_ssn"]
    patient_id = patient.get_patient_id_by_ssn(ssn)[0]
    department_abbrev = request.form["department_abbrev"]
    department_id = maintenance_functions.get_department_by_abbrev(department_abbrev)[0]
    date = request.form["date"]
    new_status = "Siirretty"
    try:
        transfusion.add_transfusion(product_id, patient_id, department_id, date)
        status.set_new_status(new_status, product_id)
    except:
        print("Virhe")
    return redirect("/transfusions")

