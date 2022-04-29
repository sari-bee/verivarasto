from flask import render_template, redirect, request, flash
from app import app
import transfusion
import product
import status
import patient
import maintenance_functions
import user


@app.route("/patients", methods=["GET", "POST"])
def patients():
    if not user.check_user_role(1):
        return redirect("/")
    patients = patient.get_patients()
    if request.method == "GET":
        patient_transfusions = []
        patient_by_id = []
        search_message = ""
    if request.method == "POST":
        patient_id = request.form["patient_id"]
        patient_by_id = patient.get_patient_by_id(patient_id)
        patient_transfusions = transfusion.get_transfusions_by_patient(
            patient_id)
        if patient_transfusions == []:
            search_message = "Ei verensiirtoja"
        else:
            search_message = ""
    return render_template("patients.html", patients=patients,
                           patient_transfusions=patient_transfusions, patient_by_id=patient_by_id,
                           search_message=search_message)


@app.route("/transfusions", methods=["GET", "POST"])
def transfusions():
    if not user.check_user_role(1):
        return redirect("/")
    products = product.get_useable_product_listing()
    patients = patient.get_patients()
    departments = maintenance_functions.get_departments()
    if request.method == "GET":
        department = []
        department_transfusions = []
        search_message = ""
    if request.method == "POST":
        department_id = request.form["department_id"]
        department = maintenance_functions.get_department(department_id)
        department_transfusions = transfusion.get_transfusions_by_department(
            department_id)
        if department_transfusions == []:
            search_message = "Ei verensiirtoja"
        else:
            search_message = ""
    return render_template("transfusions.html", products=products, patients=patients,
                           departments=departments, department=department,
                           department_transfusions=department_transfusions,
                           search_message=search_message)


@app.route("/addpatient", methods=["POST"])
def addpatient():
    if not user.check_user_role(1):
        return redirect("/")
    csrf_token = request.form["csrf_token"]
    if not user.check_csrf_token(csrf_token):
        return redirect("/")
    ssn = request.form["ssn"]
    patient_name = request.form["patient_name"]
    bloodgroup = request.form["bloodgroup"]
    phenotype_reqs = request.form["phenotype_reqs"]
    if len(ssn) < 3 or len(ssn) > 20:
        flash("Syötit väärän pituisen syötteen")
    elif len(patient_name) < 3 or len(patient_name) > 50:
        flash("Syötit väärän pituisen syötteen")
    elif len(phenotype_reqs) > 200:
        flash("Syötit väärän pituisen syötteen")
    elif not patient.add_patient(ssn, patient_name, bloodgroup, phenotype_reqs):
        flash("Potilaan lisääminen epäonnistui. Onko potilas jo lisätty?")
    else:
        user.add_to_log(f"Lisättiin potilas {ssn}")
        flash(f"Potilas {ssn} lisätty")
    return redirect("/patients")


@app.route("/addtransfusion", methods=["POST"])
def addtransfusion():
    if not user.check_user_role(1):
        return redirect("/")
    csrf_token = request.form["csrf_token"]
    if not user.check_csrf_token(csrf_token):
        return redirect("/")
    product_id = request.form["product_id"]
    patient_id = request.form["patient_id"]
    department_id = request.form["department_id"]
    date = request.form["date"]
    if not transfusion.add_transfusion(product_id, patient_id, department_id, date):
        flash("Verensiirron lisääminen epäonnistui")
    else:
        status.set_new_status("Siirretty", product_id)
        donation_number = product.get_donation_number(
            product_id).donation_number
        ssn = patient.get_patient_by_id(patient_id).ssn
        user.add_to_log(
            f"Kirjattiin valmisteen {donation_number} siirto potilaalle {ssn}")
        flash(f"Valmiste {donation_number} kirjattu potilaalle {ssn}")
    return redirect("/transfusions")
