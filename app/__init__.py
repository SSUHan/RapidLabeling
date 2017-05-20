from flask import Flask
print("2", __name__)

rc_app = Flask(__name__)
rc_app.secret_key = 'mysecret'

from app.routes import *