from app import rc_app, fm
from flask import render_template, url_for, jsonify, request
import os

@rc_app.route('/')
def index_page():
	# image_path = 'app/datacenter/images/dog.jpg'
	# image_path = os.path.join(rc_app.root_path, 'datacenter', 'images', 'dog.jpg')
	image_path = url_for('static', filename='datacenter/images/dog.jpg')
	
	return render_template('index.html', image_path=image_path)

@rc_app.route('/make_dir', methods=['POST'])
def make_dir():
	if request.methods == 'POST':
		to_client = {}
		new_hashid = fm.make_new_hashid()
		to_client['new_hashid'] = new_hashid
		datacenter_path = fm.make_datacenter_path(new_hashid, 'Junsu', 123)

		f = request.files['file']
		print("f : ", f)
		print("f.filename : ", f.filename)
		# f.save(f.filename)

		to_client['datacenter_path'] = datacenter_path

	return jsonify(to_client)

@rc_app.route('/video_upload', methods=['GET', "POST"])
def video_upload():
	to_client = {}
	if request.method == 'POST':
		
	return "no"
