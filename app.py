from os import getenv
from flask import Flask

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import maintenance_routes
import patient_routes
import product_routes
import user_routes
