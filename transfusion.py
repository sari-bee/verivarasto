from db import db


def get_transfusions_by_department(department_id):
    sql = """SELECT ssn, patient_name, donation_number, prod_code_abbrev, prod_code_name, date
        FROM Transfusions, Patients, Products, Product_codes WHERE Transfusions.patient_id = Patients.id 
        AND Transfusions.product_id = Products.id AND Products.product_code_id = Product_codes.id
        AND department_id = :department_id  ORDER BY Transfusions.id DESC"""
    return db.session.execute(sql, {"department_id": department_id}).fetchall()


def get_transfusions_by_patient(patient_id):
    sql = """SELECT donation_number, prod_code_abbrev, prod_code_name, bloodgroup, phenotypes,
        date, department_abbrev FROM Transfusions, Products, Product_codes, Departments
        WHERE Transfusions.product_id = Products.id AND Products.product_code_id = Product_codes.id
        AND Departments.id = Transfusions.department_id AND patient_id = :patient_id
        ORDER BY Transfusions.id DESC"""
    return db.session.execute(sql, {"patient_id": patient_id}).fetchall()


def add_transfusion(product_id, patient_id, department_id, date):
    try:
        sql = """INSERT INTO Transfusions (product_id, patient_id, department_id, date)
            VALUES (:product_id, :patient_id, :department_id, :date)"""
        db.session.execute(sql, {"product_id": product_id, "patient_id": patient_id,
                                 "department_id": department_id, "date": date})
        db.session.commit()
        return True
    except:
        return False
