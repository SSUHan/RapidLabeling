from app import rc_app
from flask import render_template
import os
@rc_app.route('/')
def index_page():
	image_path = 'app/datacenter/images/dog.jpg'
	return render_template('index.html', image_path=image_path)