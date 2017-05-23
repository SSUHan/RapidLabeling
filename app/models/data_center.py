from app import rc_app
import json
import os
import glob
from flask import url_for

class DataControllor:
	connector = 0 # Connector in this Server
	total_image_number = 0
	current_image_number = 0
	annotations_folder_path = None
	label_path_list = []
	built = False
	
	def __init__(self):
		self.connector = 0
		self.total_image_number = 0
		self.current_image_number = 0
		self.annotations_folder_path = None

	def load_config(self):
		# infomation_file = url_for('static', filename='datacenter/datacenter_infomation.json')
		# print(infomation_file)
		self.label_path_list = []
		infomation_file = os.path.join(rc_app.root_path, "static", "datacenter", "datacenter_infomation.json")
		with open(infomation_file) as f:
			infomation_json = json.load(f)
		self.total_image_number = infomation_json['total_image_number']
		self.current_image_number = infomation_json['current_image_number']
		self.annotations_folder_path = os.path.join(rc_app.root_path, infomation_json['annotations_folder_path'])
		for each_path in glob.glob(os.path.join(rc_app.root_path, "static", "datacenter", "images", "*")):
			each_name = each_path.split('/')[-1]
			self.label_path_list.append(each_name)
		
		self.built = True
		self.print_status()

	def new_connector(self):
		self.connector += 1
		pass

	def save_annotation(self, file_name, xml_data):
		xml_file_name = file_name.split('.')[0] +'.xml'
		print(xml_file_name)
		with open(os.path.join(self.annotations_folder_path, xml_file_name), 'w+') as f:
			f.write(xml_data)
			print("write something")

	def next_image_path(self):
		self.current_image_number += 1
		if self.built is not True:
			return False
		if self.total_image_number <= self.current_image_number:
			return False
		return self.label_path_list[self.current_image_number]

	def print_status(self):
		print("*"*40)
		print("\tCurrent Connector : {}\n\
			\tTotal Image Number : {}\n\
			\tCurrent Image Number : {}\n\
			\tBuilt : {}\n\
			\tAnnotations Folder path : {}"\
			.format(self.connector, 
				self.total_image_number, 
				self.current_image_number, 
				self.built,
				self.annotations_folder_path))
		print("\tlabel_path_list : ", self.label_path_list)
		print("*"*40)