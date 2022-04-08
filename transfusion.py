from db import db

def get_transfusions():
    sql = """SELECT ssn, patient_name, donation_number, prod_code_abbrev, department_abbrev, date FROM Transfusions, Patients, Products, Product_codes, Departments 
        WHERE Transfusions.department_id = Departments.id AND Transfusions.patient_id = Patients.id 
            AND Transfusions.product_id = Products.id AND Products.product_code_id = Product_codes.id"""
    return db.session.execute(sql).fetchall()

def get_transfusions_by_patient(patient_id):
    sql = """SELECT donation_number, prod_code_abbrev, prod_code_name, bloodgroup, date, department_abbrev
        FROM Transfusions, Products, Product_codes, Departments
        WHERE Transfusions.product_id = Products.id AND Products.product_code_id = Product_codes.id
        AND Departments.id = Transfusions.department_id AND patient_id = :patient_id"""
    return db.session.execute(sql, {"patient_id":patient_id}).fetchall()

def add_transfusion(product_id, patient_id, department_id, date):
    sql = """INSERT INTO Transfusions (product_id, patient_id, department_id, date) 
        VALUES (:product_id, :patient_id, :department_id, :date)"""
    db.session.execute(sql, {"product_id":product_id, "patient_id":patient_id, "department_id":department_id, "date":date})
    db.session.commit()