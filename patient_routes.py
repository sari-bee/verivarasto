from app import app
from flask import render_template, redirect, request
import transfusion, product, status, patient, maintenance_functions, user

@app.route("/patients", methods=["GET", "POST"])
def patients():
    user.check_user_role(1)
    patients = patient.get_patients()
    if request.method == "GET":
        patient_transfusions = []
        patient_by_ssn = []
    if request.method == "POST":
        ssn = request.form["patient_ssn"]
        patient_by_ssn = patient.get_patient_by_ssn(ssn)
        patient_transfusions = transfusion.get_transfusions_by_patient(patient_by_ssn[0])
    return render_template("patients.html", patients=patients, patient_transfusions=patient_transfusions, patient_by_ssn=patient_by_ssn)

@app.route("/transfusions", methods=["GET", "POST"])
def transfusions():
    user.check_user_role(1)
    product_status = "Käytettävissä"
    products = product.get_products_by_status(product_status)
    patients = patient.get_patients()
    departments = maintenance_functions.get_departments()
    if request.method == "GET":
        department = []
        department_transfusions = []
    if request.method == "POST":
        department = request.form["department"]
        department_id = maintenance_functions.get_department_by_abbrev(department)[0]
        department_transfusions = transfusion.get_transfusions_by_department(department_id)
    return render_template("transfusions.html", products=products, patients=patients, departments=departments, department=department, department_transfusions=department_transfusions)

@app.route("/addpatient", methods=["POST"])
def addpatient():
    user.check_user_role(1)
    csrf_token = request.form["csrf_token"]
    user.check_csrf_token(csrf_token)
    ssn = request.form["ssn"]
    patient_name = request.form["patient_name"]
    bloodgroup = request.form["bloodgroup"]
    phenotype_reqs = request.form["phenotype_reqs"]
    if len(ssn) < 3 or len(ssn) > 20 or len(patient_name) < 3 or len(patient_name) > 50 or len(phenotype_reqs) > 200:
        return render_template("message.html", message="Syötit väärän pituisen syötteen")  
    if not patient.add_patient(ssn, patient_name, bloodgroup, phenotype_reqs):
        return render_template("message.html", message="Potilaan lisääminen epäonnistui. Onko potilas jo lisätty?")
    user.add_to_log(f"Lisättiin potilas {ssn}")
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
    if not transfusion.add_transfusion(product_id, patient_id, department_id, date):
        return render_template("message.html", message="Verensiirron lisääminen epäonnistui")
    status.set_new_status(new_status, product_id)
    user.add_to_log(f"Kirjattiin valmisteen {donation_number} siirto potilaalle {ssn}")
    return redirect("/transfusions")

