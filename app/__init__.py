from flask import Flask
print("2", __name__)

rc_app = Flask(__name__)
# print(rc_app.root_path)
rc_app.secret_key = 'mysecret'

from app.routes import *