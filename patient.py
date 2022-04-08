from db import db

def get_patients():
    sql = "SELECT ssn, patient_name, bloodgroup, phenotype_reqs FROM Patients"
    return db.session.execute(sql).fetchall()

def get_patient_by_ssn(ssn):
    sql = "SELECT id, ssn, patient_name, bloodgroup, phenotype_reqs FROM Patients WHERE ssn = :ssn"
    return db.session.execute(sql, {"ssn":ssn}).fetchone()

def get_patient_id_by_ssn(ssn):
    sql = "SELECT id FROM Patients WHERE ssn = :ssn"
    return db.session.execute(sql, {"ssn":ssn}).fetchone()

def add_patient(ssn, patient_name, bloodgroup, phenotype_reqs):
    sql = """INSERT INTO Patients (ssn, patient_name, bloodgroup, phenotype_reqs) 
        VALUES (:ssn, :patient_name, :bloodgroup, :phenotype_reqs)"""
    db.session.execute(sql, {"ssn":ssn, "patient_name":patient_name, "bloodgroup":bloodgroup, "phenotype_reqs":phenotype_reqs})
    db.session.commit()