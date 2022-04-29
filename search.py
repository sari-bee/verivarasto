from db import db


def get_all_products():
    sql = """SELECT donation_number, prod_code_abbrev, bloodgroup, phenotypes, use_before,
        inventory_abbrev, status FROM Products, Product_codes, Inventory_products, Inventories
        WHERE Products.product_code_id = Product_codes.id
        AND Products.id = Inventory_products.product_id
        AND Inventories.id = Inventory_products.inventory_id ORDER BY Products.id DESC"""
    return db.session.execute(sql).fetchall()


def get_products_by_status(status):
    sql = """SELECT donation_number, prod_code_abbrev, bloodgroup, phenotypes, use_before,
        inventory_abbrev, status FROM Products, Product_codes, Inventory_products, Inventories
        WHERE Products.product_code_id = Product_codes.id
        AND Products.id = Inventory_products.product_id
        AND Inventories.id = Inventory_products.inventory_id
        AND status = :status ORDER BY Products.id DESC"""
    return db.session.execute(sql, {"status":status}).fetchall()


def get_products_by_inventory(inventory_id):
    sql = """SELECT donation_number, prod_code_abbrev, bloodgroup, phenotypes, use_before,
        inventory_abbrev, status FROM Products, Product_codes, Inventory_products, Inventories
        WHERE Products.product_code_id = Product_codes.id
        AND Products.id = Inventory_products.product_id
        AND Inventories.id = Inventory_products.inventory_id
        AND Inventories.id = :inventory_id ORDER BY Products.id DESC"""
    return db.session.execute(sql, {"inventory_id":inventory_id}).fetchall()


def get_prod_by_status_and_inventory(status, inventory_id):
    sql = """SELECT donation_number, prod_code_abbrev, bloodgroup, phenotypes, use_before,
        inventory_abbrev, status FROM Products, Product_codes, Inventory_products, Inventories
        WHERE Products.product_code_id = Product_codes.id
        AND Products.id = Inventory_products.product_id
        AND Inventories.id = Inventory_products.inventory_id
        AND Inventories.id = :inventory_id AND status = :status ORDER BY Products.id DESC"""
    return db.session.execute(sql, {"inventory_id":inventory_id, "status":status}).fetchall()


def get_prod_by_status_and_bloodgroup(status, bloodgroup):
    sql = """SELECT donation_number, prod_code_abbrev, bloodgroup, phenotypes, use_before,
        inventory_abbrev, status FROM Products, Product_codes, Inventory_products, Inventories
        WHERE Products.product_code_id = Product_codes.id
        AND Products.id = Inventory_products.product_id
        AND Inventories.id = Inventory_products.inventory_id
        AND bloodgroup = :bloodgroup AND status = :status ORDER BY Products.id DESC"""
    return db.session.execute(sql, {"bloodgroup":bloodgroup, "status":status}).fetchall()


def get_product_by_donation_number(donation_number):
    like_donation_number = "%" + donation_number + "%"
    sql = """SELECT donation_number, prod_code_abbrev, bloodgroup, phenotypes, use_before,
        inventory_abbrev, status FROM Products, Product_codes, Inventory_products, Inventories
        WHERE Products.product_code_id = Product_codes.id
        AND Products.id = Inventory_products.product_id
        AND Inventories.id = Inventory_products.inventory_id 
        AND LOWER(donation_number) LIKE LOWER(:donation_number) ORDER BY Products.id DESC"""
    return db.session.execute(sql, {"donation_number":like_donation_number}).fetchall()
