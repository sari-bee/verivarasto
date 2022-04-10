CREATE TABLE Product_codes (id SERIAL PRIMARY KEY, prod_code_abbrev TEXT UNIQUE, prod_code_name TEXT);
CREATE TABLE Products (id SERIAL PRIMARY KEY, donation_number TEXT UNIQUE, product_code_id INTEGER REFERENCES Product_codes ON DELETE RESTRICT, bloodgroup TEXT, phenotypes TEXT, use_before DATE);
CREATE TABLE Patients (id SERIAL PRIMARY KEY, ssn TEXT UNIQUE, patient_name TEXT, bloodgroup TEXT, phenotype_reqs TEXT);
CREATE TABLE Inventories (id SERIAL PRIMARY KEY, inventory_abbrev TEXT UNIQUE, inventory_name TEXT);
CREATE TABLE Departments (id SERIAL PRIMARY KEY, department_abbrev TEXT UNIQUE, department_name TEXT, inventory_id INTEGER REFERENCES Inventories ON DELETE RESTRICT);
CREATE TABLE Inventory_products (id SERIAL PRIMARY KEY, product_id INTEGER REFERENCES Products ON DELETE CASCADE, inventory_id INTEGER REFERENCES Inventories ON DELETE RESTRICT, status TEXT);
CREATE TABLE Transfusions (id SERIAL PRIMARY KEY, product_id INTEGER REFERENCES Products ON DELETE RESTRICT, patient_id INTEGER REFERENCES Patients ON DELETE RESTRICT, department_id INTEGER REFERENCES Departments ON DELETE RESTRICT, date DATE);
CREATE TABLE Users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT, role INTEGER);
CREATE TABLE Logs (id SERIAL PRIMARY KEY, logtext TEXT, user_id INTEGER REFERENCES Users ON DELETE RESTRICT, date DATE);