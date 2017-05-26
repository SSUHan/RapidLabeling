from app import rc_app
from flask import render_template, url_for
import os
@rc_app.route('/')
def index_page():
	# image_path = 'app/datacenter/images/dog.jpg'
	# image_path = os.path.join(rc_app.root_path, 'datacenter', 'images', 'dog.jpg')
	image_path = url_for('static', filename='datacenter/images/dog.jpg')
	
	return render_template('index.html', image_path=image_path)