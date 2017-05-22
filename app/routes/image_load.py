from app import rc_app, dc
from flask import jsonify, json, request, url_for
import os

@rc_app.route('/next_image', methods=['GET', 'POST'])
def next_image():
	from_client = request.form
	print("request", type(request), request)
	print("from client json : ", type(from_client), from_client['key1'])
	print("next image function called ")
	to_client = {}
	to_client['image_name'] = '00001.jpg'
	# infomation_file = os.path.join(rc_app.root_path, "static", "datacenter", "datacenter_infomation.json")
	# load infomation json file from datacenter
	# type(infomation_json) : dict
	# infomation_json = json.load(open(infomation_file))
	dc.print_status()
	return "hello"
	


@rc_app.route('/datacenter/<name>')
def get_image(name):
	img_path = url_for('static', filename='datacenter/images/'+name+'.jpg')
	print(img_path)
	return '<img src=' + img_path + '>'