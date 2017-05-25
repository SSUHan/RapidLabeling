from app import rc_app
import json
import os
import glob
from flask import url_for
from os import sep

class DataControllor:
	connector = 0 # Connector in this Server
	total_image_number = 0
	current_image_number = 0
	annotations_folder_path = None
	label_path_list = []
	skip_step = 0
	built = False
	
	def __init__(self):
		self.connector = 0
		self.total_image_number = 0
		self.current_image_number = 0
		self.annotations_folder_path = None
		self.skip_step = 0

	def load_config(self):
		# infomation_file = url_for('static', filename='datacenter/datacenter_infomation.json')
		# print(infomation_file)
		self.label_path_list = []
		infomation_file = os.path.join(rc_app.root_path, "static", "datacenter", "datacenter_infomation.json")
		with open(infomation_file) as f:
			self.infomation_json = json.load(f)
		self.current_image_number = self.infomation_json['current_image_number']
		self.skip_step = self.infomation_json['skip_step']
		self.annotations_folder_path = os.path.join(rc_app.root_path, self.infomation_json['annotations_folder_path'])
		for each_path in glob.glob(os.path.join(rc_app.root_path, "static", "datacenter", "images", "*")):
			each_name = each_path.split(sep)[-1]
			self.label_path_list.append(each_name)

		self.total_image_number = len(self.label_path_list)
		
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
		
		self.current_image_number += self.skip_step
		self.infomation_json['current_image_number'] = self.current_image_number
		with open(os.path.join(rc_app.root_path, "static", "datacenter", "datacenter_infomation.json"), 'w') as f:
			json.dump(self.infomation_json, f)
			print("infomation config file update..")
		print("write something")

	def next_image_path(self):
		if not _check(self.current_image_number):
			return False
		ret = self.label_path_list[self.current_image_number]
		# TODO : Need to skip if already labeled.
		if _is_duplicate(ret):
			print(ret, " file is already annotated.. To do next file")
			self.current_image_number += self.skip_step
			return self.next_image_path()
		return ret

	def _check(self, current_num):
		"""
			Check is there more image file to annotables
			True: Ok to process
			False: No more to process
		"""
		if self.built is not True:
			return False
		if self.total_image_number <= current_num:
			return False
		return True

	def _is_duplicate(self, image_file):
		"""
			Check is this file already annotated
			True: yes. check next file
			False: No. Do annotate
		"""
		anno_file = image_file.split('.')[0] + '.xml'
		print("[in _is_duplicate], anno_file : ", anno_file)
		return os.path.exists(os.path.join(self.annotations_folder_path, anno_file))

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
		# print("\tlabel_path_list : ", self.label_path_list)
		print("*"*40)