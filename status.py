from datetime import date
from db import db


def set_new_status(status, product_id):
    sql = "UPDATE Inventory_products SET status = :status WHERE product_id = :product_id"
    db.session.execute(sql, {"status": status, "product_id": product_id})
    db.session.commit()


def set_as_expired():
    new_status = "Vanhentunut"
    old_status = "Käytettävissä"
    today = date.today()
    sql = """UPDATE Inventory_products SET status = :new_status
        WHERE product_id IN (SELECT id FROM Products WHERE use_before < :today)
        AND status = :old_status"""
    db.session.execute(sql, {"new_status": new_status,
                       "today": today, "old_status": old_status})
    db.session.commit()
