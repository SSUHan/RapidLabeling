from app import rc_app, fm
from flask import render_template, url_for, jsonify
import os

@rc_app.route('/')
def index_page():
	# image_path = 'app/datacenter/images/dog.jpg'
	# image_path = os.path.join(rc_app.root_path, 'datacenter', 'images', 'dog.jpg')
	image_path = url_for('static', filename='datacenter/images/dog.jpg')
	
	return render_template('index.html', image_path=image_path)

@rc_app.route('/make_dir')
def make_dir():
	to_client = {}
	new_hashid = fm.make_new_hashid()
	to_client['new_hashid'] = new_hashid
	datacenter_path = fm.make_datacenter_path(new_hashid, 'Junsu', 123)
	to_client['datacenter_path'] = datacenter_path
	# fm.make_new_datacenter()
	return jsonify(to_client)