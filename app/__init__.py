from flask import Flask

rc_app = Flask(__name__)

from app.routes import *