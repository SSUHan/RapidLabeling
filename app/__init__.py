from flask import Flask


rc_app = Flask(__name__)

rc_app.secret_key = 'mysecret'

# DataControllor in Global Modules..
from app.models.data_center import DataControllor
from app.models.folder_manager import FolderManager

dc = DataControllor()
dc.load_config()

fm = FolderManager()

from app.routes import *