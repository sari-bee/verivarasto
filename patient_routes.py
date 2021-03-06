from flask import render_template, redirect, request, flash
from app import app
import transfusion
import product
import status
import patient
import maintenance_functions
import user
import search


@app.route("/patients", methods=["GET", "POST"])
def patients():
    if not user.check_user_role(1):
        return redirect("/")
    patients = patient.get_patients()
    search_message = ""
    if request.method == "GET":
        patient_transfusions = []
        patient_by_id = []
    if request.method == "POST":
        patient_id = request.form["patient_id"].strip()
        patient_by_id = patient.get_patient_by_id(patient_id)
        patient_transfusions = transfusion.get_transfusions_by_patient(
            patient_id)
        if patient_transfusions == []:
            search_message = "Ei verensiirtoja"
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
    sent_products = search.get_products_by_status("Siirretty")
    sent_product = []
    search_message = ""
    if request.method == "GET":
        department = []
        department_transfusions = []
    if request.method == "POST":
        department_id = request.form["department_id"].strip()
        department = maintenance_functions.get_department(department_id)
        department_transfusions = transfusion.get_transfusions_by_department(
            department_id)
        if department_transfusions == []:
            search_message = "Ei verensiirtoja"
    return render_template("transfusions.html", products=products, patients=patients,
                           departments=departments, department=department,
                           department_transfusions=department_transfusions,
                           search_message=search_message, sent_product=sent_product,
                           sent_products=sent_products)

@app.route("/transfusionbyproduct", methods = ["POST"])
def transfusionbyproduct():
    if not user.check_user_role(1):
        return redirect("/")
    products = product.get_useable_product_listing()
    patients = patient.get_patients()
    departments = maintenance_functions.get_departments()
    department = []
    department_transfusions = []
    search_message = ""
    sent_products = search.get_products_by_status("Siirretty")
    sent_product_id = request.form["sent_product_id"].strip()
    sent_product = transfusion.get_transfusion_details(sent_product_id)
    return render_template("transfusions.html", products=products, patients=patients,
                           departments=departments, department=department,
                           department_transfusions=department_transfusions,
                           search_message=search_message, sent_product=sent_product,
                           sent_products=sent_products)


@app.route("/addpatient", methods=["POST"])
def addpatient():
    if not user.check_user_role(1):
        return redirect("/")
    csrf_token = request.form["csrf_token"]
    if not user.check_csrf_token(csrf_token):
        return redirect("/")
    patients = patient.get_patients()
    patient_transfusions = []
    patient_by_id = []
    search_message = ""
    ssn = request.form["ssn"].strip()
    patient_name = request.form["patient_name"].strip()
    bloodgroup = request.form["bloodgroup"].strip()
    phenotype_reqs = request.form["phenotype_reqs"].strip()
    if len(ssn) < 3 or len(ssn) > 20:
        flash("Sy??tit v????r??n pituisen henkil??tunnuksen")
    elif len(patient_name) < 3 or len(patient_name) > 50:
        flash("Sy??tit v????r??n pituisen nimen")
    elif len(phenotype_reqs) > 200:
        flash("Fenotyyppikent??ss?? on liikaa teksti??")
    elif not patient.add_patient(ssn, patient_name, bloodgroup, phenotype_reqs):
        flash("Potilaan lis????minen ep??onnistui. Onko potilas jo lis??tty?")
    else:
        user.add_to_log(f"Lis??ttiin potilas {ssn}")
        flash(f"Potilas {ssn} lis??tty")
        return redirect("/patients")
    return render_template("patients.html", patients=patients,
                           patient_transfusions=patient_transfusions, patient_by_id=patient_by_id,
                           search_message=search_message)

@app.route("/newphenotypereq", methods=["POST"])
def newphenotypereq():
    if not user.check_user_role(1):
        return redirect("/")
    csrf_token = request.form["csrf_token"]
    if not user.check_csrf_token(csrf_token):
        return redirect("/")
    search_message = ""
    patients = patient.get_patients()
    new_phenotype_req = request.form["new_phenotype_req"].strip()
    patient_id = request.form["patient_id"]
    patient_by_id = patient.get_patient_by_id(patient_id)
    patient_transfusions = transfusion.get_transfusions_by_patient(
        patient_id)
    if patient_transfusions == []:
        search_message = "Ei verensiirtoja"
    ssn = request.form["patient_ssn"]
    if len(new_phenotype_req) == 0 or len(new_phenotype_req) > 200:
        flash("Tarkista fenotyyppikentt??")
    elif not patient.add_phenotype_reqs(patient_id, new_phenotype_req):
        flash("Fenotyyppivaatimusten lis????minen ep??onnistui, tarkista tiedot ja yrit?? uudelleen")
    else:
        user.add_to_log(f"Lis??ttiin fenotyyppivaatimus {new_phenotype_req} potilaalle {ssn}")
        patient_by_id = patient.get_patient_by_id(patient_id)
    return render_template("patients.html", patients=patients,
                           patient_transfusions=patient_transfusions, patient_by_id=patient_by_id,
                           search_message=search_message)

@app.route("/addtransfusion", methods=["POST"])
def addtransfusion():
    if not user.check_user_role(1):
        return redirect("/")
    csrf_token = request.form["csrf_token"]
    if not user.check_csrf_token(csrf_token):
        return redirect("/")
    products = product.get_useable_product_listing()
    patients = patient.get_patients()
    departments = maintenance_functions.get_departments()
    department = []
    department_transfusions = []
    search_message = ""
    product_id = request.form["product_id"].strip()
    patient_id = request.form["patient_id"].strip()
    department_id = request.form["department_id"].strip()
    date = request.form["date"].strip()
    if not transfusion.add_transfusion(product_id, patient_id, department_id, date):
        flash("Verensiirron lis????minen ep??onnistui")
    else:
        status.set_new_status("Siirretty", product_id)
        donation_number = product.get_donation_number(
            product_id).donation_number
        ssn = patient.get_patient_by_id(patient_id).ssn
        user.add_to_log(
            f"Kirjattiin valmisteen {donation_number} l??hetys potilaalle {ssn}")
        flash(f"Valmiste {donation_number} l??hetetty potilaalle {ssn}")
        return redirect("/transfusions")
    return render_template("transfusions.html", products=products, patients=patients,
                           departments=departments, department=department,
                           department_transfusions=department_transfusions,
                           search_message=search_message)
