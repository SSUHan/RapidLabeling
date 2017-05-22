from app import rc_app
import json
import os

class DataControllor:
	connector = 0 # Connector in this Server
	total_image_number = 0
	current_image_number = 0
	built = False
	
	def __init__(self):
		self.connector = 0
		self.total_image_number = 0
		self.current_image_number = 0

	def load_config(self):
		infomation_file = os.path.join(rc_app.root_path, "static", "datacenter", "datacenter_infomation.json")
		with open(infomation_file) as f:
			infomation_json = json.load(f)
		self.total_image_number = infomation_json['total_image_number']
		self.current_image_number = infomation_json['current_image_number']
		self.print_status()

	def new_connector(self):
		self.connector += 1
		pass

	def next_image_path(self):
		pass

	def print_status(self):
		print("*"*40)
		print("\tCurrent Connector : {}\n\tTotal Image Number : {}\n\tCurrent Image Number : {}".format(self.connector, self.total_image_number, self.current_image_number))
		print("*"*40)