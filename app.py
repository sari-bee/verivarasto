from flask import Flask
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import user_routes, product_routes, patient_routes, maintenance_routes