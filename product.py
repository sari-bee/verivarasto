from db import db

def get_all_products():
    sql = """SELECT donation_number, prod_code_abbrev, bloodgroup, phenotypes, use_before, inventory_abbrev, status
        FROM Products, Product_codes, Inventory_products, Inventories WHERE Products.product_code_id = Product_codes.id
        AND Products.id = Inventory_products.product_id AND Inventories.id = Inventory_products.inventory_id"""
    return db.session.execute(sql).fetchall()

def get_product_id(donation_number):
    sql = "SELECT id FROM Products WHERE donation_number = :donation_number"
    return db.session.execute(sql, {"donation_number":donation_number}).fetchone()[0]

def get_products_by_status(status):
    sql = """SELECT donation_number, prod_code_abbrev, bloodgroup, phenotypes, use_before, inventory_abbrev, status
        FROM Products, Product_codes, Inventory_products, Inventories WHERE Products.product_code_id = Product_codes.id
        AND Products.id = Inventory_products.product_id AND Inventories.id = Inventory_products.inventory_id
        AND status = :status"""
    return db.session.execute(sql, {"status":status}).fetchall()

def get_product_id_by_donation_number(donation_number):
    sql = "SELECT id FROM Products WHERE donation_number = :donation_number"
    return db.session.execute(sql, {"donation_number":donation_number}).fetchone()

def get_product_by_donation_number(donation_number):
    like_donation_number = "%" + donation_number + "%"
    sql = """SELECT donation_number, prod_code_abbrev, bloodgroup, phenotypes, use_before, inventory_abbrev, status
        FROM Products, Product_codes, Inventory_products, Inventories WHERE Products.product_code_id = Product_codes.id
        AND Products.id = Inventory_products.product_id AND Inventories.id = Inventory_products.inventory_id 
        AND LOWER(donation_number) LIKE LOWER(:donation_number)"""
    return db.session.execute(sql, {"donation_number":like_donation_number}).fetchall()

def get_products_by_inventory(inventory_id):
    sql = """SELECT donation_number, prod_code_abbrev, bloodgroup, phenotypes, use_before, inventory_abbrev, status
        FROM Products, Product_codes, Inventory_products, Inventories WHERE Products.product_code_id = Product_codes.id
        AND Products.id = Inventory_products.product_id AND Inventories.id = Inventory_products.inventory_id
        AND Inventories.id = :inventory_id"""
    return db.session.execute(sql, {"inventory_id":inventory_id}).fetchall()

def add_product(donation_number, product_code_id, bloodgroup, phenotypes, use_before):
    try:
        sql = """INSERT INTO Products (donation_number, product_code_id, bloodgroup, phenotypes, use_before) 
            VALUES (:donation_number, :product_code_id, :bloodgroup, :phenotypes, :use_before)"""
        db.session.execute(sql, {"donation_number":donation_number, "product_code_id":product_code_id, "bloodgroup":bloodgroup, "phenotypes":phenotypes, "use_before":use_before})
        db.session.commit()
        return True
    except:
        return False

def add_inventory_product(product_id, inventory_id, status):
    sql = """INSERT INTO Inventory_products (product_id, inventory_id, status) 
        VALUES (:product_id, :inventory_id, :status)"""
    db.session.execute(sql, {"product_id":product_id, "inventory_id":inventory_id, "status":status})
    db.session.commit()

def change_inventories(product_id, new_inventory_id):
    sql = "UPDATE Inventory_products SET inventory_id = :inventory_id WHERE product_id = :product_id"
    db.session.execute(sql, {"inventory_id":new_inventory_id, "product_id":product_id})
    db.session.commit()