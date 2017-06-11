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
	
	def __init__(self, datacenter_root_path, hashid):
		self.connector = 0
		self.total_image_number = 0
		self.current_image_number = 0
		self.annotations_folder_path = None
		self.skip_step = 0
		self.hashid = hashid
		self.load_config(datacenter_root_path, hashid)

	def load_config(self, datacenter_root_path, hashid):
		# infomation_file = url_for('static', filename='datacenter/datacenter_infomation.json')
		# print(infomation_file)
		self.label_path_list = []
		self.infomation_path = os.path.join(datacenter_root_path, "video_{}".format(hashid), "{}_infomation.json".format(hashid))
		with open(self.infomation_path) as f:
			self.infomation_json = json.load(f)
		
		self.current_image_number = self.infomation_json['current_image_number']
		self.skip_step = self.infomation_json['skip_step']
		self.annotations_folder_path = self.infomation_json['annotations_folder_path']
		for each_path in glob.glob(os.path.join(self.infomation_json['images_folder_path'], "*")):
			each_name = each_path.split(sep)[-1]
			self.label_path_list.append(each_name)

		self.total_image_number = len(self.label_path_list)
		self.hashid = hashid
		
		self.built = True
		self.print_status()

	def new_connector(self):
		self.connector += 1
		pass

	def save_annotation(self, file_name, xml_data, is_save=True):
		if is_save:
			# if skip image save, then is_save = False
			file_name = file_name.replace('/', sep)
			file_name = file_name.split(sep)[-1]
			xml_file_name = file_name.split('.')[0] +'.xml'
			print(xml_file_name)
			with open(os.path.join(self.annotations_folder_path, xml_file_name), 'w+') as f:
				f.write(xml_data)
				print(xml_file_name, " saved..")
		
		self.current_image_number += self.skip_step
		self.infomation_json['current_image_number'] = self.current_image_number
		with open(self.infomation_path, 'w') as f:
			json.dump(self.infomation_json, f)
			print("infomation config file update..")

	def back_image_path(self):
		if not self._check(self.current_image_number - self.skip_step):
			return False, False, False
		self.current_image_number -= self.skip_step
		self.infomation_json['current_image_number'] = self.current_image_number
		with open(self.infomation_path, 'w') as f:
			json.dump(self.infomation_json, f)
			print("infomation config file update..")
		
		ret = self.label_path_list[self.current_image_number]
		if self._is_duplicate(ret):
			anno_file = ret.split('.')[0] + '.xml'
			print(ret, " file is already annotated.. then, get xml file")
			dup_xml_file = os.path.join(self.annotations_folder_path, anno_file)
			with open(dup_xml_file, 'r') as f:
				dup_xml_data = f.read()
			# self.current_image_number += self.skip_step
			return "video_{}/images/".format(self.hashid), ret, dup_xml_data # self.next_image_path()
		return "video_{}/images/".format(self.hashid), ret, False

	def next_image_path(self):
		if not self._check(self.current_image_number):
			return False, False, False
		ret = self.label_path_list[self.current_image_number]
		# TODO : Need to skip if already labeled.
		if self._is_duplicate(ret):
			anno_file = ret.split('.')[0] + '.xml'
			print(ret, " file is already annotated.. then, get xml file")
			dup_xml_file = os.path.join(self.annotations_folder_path, anno_file)
			with open(dup_xml_file, 'r') as f:
				dup_xml_data = f.read()
			# self.current_image_number += self.skip_step
			return "video_{}/images/".format(self.hashid), ret, dup_xml_data # self.next_image_path()
		return "video_{}/images/".format(self.hashid), ret, False

	def _check(self, current_num):
		"""
			Check is there more image file to annotables
			True: Ok to process
			False: No more to process
		"""
		if self.built is not True:
			return False
		if self.total_image_number <= current_num or current_num < 0:
			return False
		return True

	def _is_duplicate(self, image_file):
		"""
			Check is this file already annotated
			True: yes. check next file
			False: No. Do annotate
		"""
		anno_file = image_file.split('.')[0] + '.xml'
		# print("[in _is_duplicate], anno_file : ", anno_file)
		return os.path.exists(os.path.join(self.annotations_folder_path, anno_file))

	def print_status(self):
		print("*"*40)
		print("Current Connector : {}\n\
Total Image Number : {}\n\
Current Image Number : {}\n\
Built : {}\n\
Annotations Folder path : {}"\
			.format(self.connector, 
				self.total_image_number, 
				self.current_image_number, 
				self.built,
				self.annotations_folder_path))
		# print("\tlabel_path_list : ", self.label_path_list)
		print("*"*40)



def split_datacenter(src_folder_path, dst_folder_path, train_rates=0.8):
	"""
		datacenter/
			annotations/
			images/
		로 나눠져있는 데이터에 대해서 train_rates 만큼 trainval 과 test set 으로 나눠주는 기능을 담당할 것
		src_folder_path 는 datacenter 가 올것이고
		dst_folder_path 아래에 annotations/ 와 images/ 가 생성될 예정이다.
		return trainval_indexs, test_indexs
	"""
	src_anno_path = os.path.join(src_folder_path, 'annotations')

def _split(folder_path, train_rates=0.8):
	from numpy.random import permutation as perm
	import numpy as np
	files = [f for f in os.listdir(folder_path) if f.split('.')[-1] == 'xml' or f.split('.')[-1] == 'png']
	files_size = len(files)
	shuffle_idx = perm(np.arange(files_size))
	trainval_size = int(files_size*train_rates)
	return shuffle_idx[:trainval_size], shuffle_idx[trainval_size:]


