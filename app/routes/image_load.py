from app import rc_app, dc
from flask import jsonify, json, request, url_for
import os

@rc_app.route('/start_labeling', methods=["GET"])
def start_labeling():
	to_client = {}
	to_client['new_file_name'] = dc.next_image_path()
	to_client['total_image_number'] = dc.total_image_number
	to_client['current_image_number'] = dc.current_image_number
	to_client['skip_step'] = dc.skip_step
	dc.print_status()
	return jsonify(to_client)

@rc_app.route('/next_image', methods=['GET', 'POST'])
def next_image():
	from_client = request.form
	print(from_client['file_name'])
	print("next image function called ")
	to_client = {}
	# TODO : Get new image from DataControllor
	if dc.built:
		print("is built is True..")
		dc.save_annotation(from_client['file_name'], from_client['xml_data'])
		to_client['new_file_name'] = dc.next_image_path()
		to_client['total_image_number'] = dc.total_image_number
		to_client['current_image_number'] = dc.current_image_number
		to_client['skip_step'] = dc.skip_step

	print(to_client)
	# infomation_file = os.path.join(rc_app.root_path, "static", "datacenter", "datacenter_infomation.json")
	# load infomation json file from datacenter
	# type(infomation_json) : dict
	# infomation_json = json.load(open(infomation_file))
	dc.print_status()
	return jsonify(to_client)
	


@rc_app.route('/datacenter/<name>')
def get_image(name):
	img_path = url_for('static', filename='datacenter/images/'+name+'.jpg')
	print(img_path)
	return '<img src=' + img_path + '>'