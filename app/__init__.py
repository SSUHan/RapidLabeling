from flask import Flask


rc_app = Flask(__name__)

rc_app.secret_key = 'mysecret'

# FolderManager in Global Modules..
from app.models.folder_manager import FolderManager

fm = FolderManager()

from app.routes import *