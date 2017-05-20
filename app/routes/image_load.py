from app import rc_app
from flask import jsonify

@rc_app.route('/n_image')
def next_image():
	print("next image function called ")
	to_client = {}
	# TODO :  load next image path
	to_client['image_name'] = '00001.jpg'

	# return jsonify(to_client)
	return '../datacenter/images/dog.jpg'