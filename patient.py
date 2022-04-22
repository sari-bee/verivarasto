from db import db


def get_patients():
    sql = "SELECT id, ssn, patient_name FROM Patients"
    return db.session.execute(sql).fetchall()


def get_patient_by_id(patient_id):
    sql = """SELECT id, ssn, patient_name, bloodgroup, phenotype_reqs
        FROM Patients WHERE id = :patient_id"""
    return db.session.execute(sql, {"patient_id": patient_id}).fetchone()


def add_patient(ssn, patient_name, bloodgroup, phenotype_reqs):
    try:
        sql = """INSERT INTO Patients (ssn, patient_name, bloodgroup, phenotype_reqs)
            VALUES (:ssn, :patient_name, :bloodgroup, :phenotype_reqs)"""
        db.session.execute(sql, {"ssn": ssn, "patient_name": patient_name,
                                 "bloodgroup": bloodgroup, "phenotype_reqs": phenotype_reqs})
        db.session.commit()
        return True
    except:
        return False
