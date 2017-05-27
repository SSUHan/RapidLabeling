from app import rc_app, dc
from flask import jsonify, json, request, url_for
import os

@rc_app.route('/start_labeling', methods=["GET"])
def start_labeling():
	to_client = {}
	to_client['new_file_name'], to_client['new_xml_data'] = dc.next_image_path()
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
	if dc.built:
		dc.save_annotation(from_client['file_name'], from_client['xml_data'])
		to_client['new_file_name'], to_client['new_xml_data'] = dc.next_image_path()
		to_client['total_image_number'] = dc.total_image_number
		to_client['current_image_number'] = dc.current_image_number
		to_client['skip_step'] = dc.skip_step
	
	dc.print_status()
	return jsonify(to_client)

@rc_app.route('/skip_image', methods=['GET', 'POST'])
def skip_image():
	from_client = request.form
	print("skip image function called ")
	to_client = {}
	if dc.built:
		dc.save_annotation(from_client['file_name'], None, is_save=False) # for skip frame
		to_client['new_file_name'], to_client['new_xml_data'] = dc.next_image_path()
		to_client['total_image_number'] = dc.total_image_number
		to_client['current_image_number'] = dc.current_image_number
		to_client['skip_step'] = dc.skip_step

	dc.print_status()
	return jsonify(to_client)
	


@rc_app.route('/datacenter/<name>')
def get_image(name):
	img_path = url_for('static', filename='datacenter/images/'+name+'.jpg')
	print(img_path)
	return '<img src=' + img_path + '>'