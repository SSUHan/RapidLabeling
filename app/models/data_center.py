from app import rc_app
import json
import os
import glob
from flask import url_for
from os import sep
from xml.etree.ElementTree import Element, SubElement, dump, parse, ElementTree

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



def split_datacenter(src_folder_path, train_rates=0.8):
	"""
		datacenter/
			annotations/
			images/
		로 나눠져있는 데이터에 대해서 train_rates 만큼 trainval 과 test set 으로 나눠주는 기능을 담당할 것
		src_folder_path 는 datacenter 가 올것이고
		src_folder_path + '_trainval',
		src_folder_path + '_test' 아래에 annotations/ 와 images/ 가 생성될 예정이다.
		return trainval_indexs, test_indexs
	"""
	from shutil import copyfile
	
	src_anno_path = os.path.join(src_folder_path, 'annotations')
	src_images_path = os.path.join(src_folder_path, 'images')
	anno_files, trainval_indexs, test_indexs = _split(src_anno_pathc, train_rates)
	
	trainval_folder_path = _make_datacetner_folder(src_folder_path+'_trainval')
	test_folder_path = _make_datacetner_folder(src_folder_path+'_test')
	
	# Make trainval datacenter folder
	for i in trainval_indexs:
		copyfile(os.path.join(src_anno_path, anno_files[i]), os.path.join(trainval_folder_path, 'annotations', anno_files[i]))
		copyfile(os.path.join(src_images_path, anno_files[i].split('.')[0]+'.png'), os.path.join(trainval_folder_path, 'images', anno_files[i].split('.')[0]+'.png'))
	
	# Make test datacenter folder
	for i in test_indexs:
		copyfile(os.path.join(src_anno_pathc, anno_files[i]), os.path.join(test_folder_path, 'annotations', anno_files[i]))
		copyfile(os.path.join(src_images_path, anno_files[i].split('.')[0]+'.png'), os.path.join(test_folder_path, 'images', anno_files[i].split('.')[0]+'.png'))

def _split(folder_path, train_rates=0.8):
	from numpy.random import permutation as perm
	import numpy as np
	files = [f for f in os.listdir(folder_path) if f.split('.')[-1] == 'xml' or f.split('.')[-1] == 'png']
	files_size = len(files)
	shuffle_idx = perm(np.arange(files_size))
	trainval_size = int(files_size*train_rates)
	return files, shuffle_idx[:trainval_size], shuffle_idx[trainval_size:]

def _make_datacetner_folder(new_folder_path):
	os.mkdir(new_folder_path)
	os.mkdir(os.path.join(new_folder_path, "annotations"))
	os.mkdir(os.path.join(new_folder_path, "images"))
	return new_folder_path

def to_zipfile(target_folder_path, zipfile_path):
	"""
		target_folder_path 하위에 있는 annotations 와 images 를 압축하여 파일로 만들어 리턴하도록한다.
	"""
	import zipfile
	with zipfile.ZipFile(zipfile_path, 'w') as zip_fp:
		for folder, subfolders, files in os.walk(target_folder_path):
			for file in files:
				if file.endswith('.xml') or file.endswith('.png'):
					print(file)
					zip_fp.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), target_folder_path), compress_type = zipfile.ZIP_DEFLATED)

def reverse_data(target_folder_path):
	import cv2
	
	anno_folder_path = os.path.join(target_folder_path, 'annotations')
	image_folder_path = os.path.join(target_folder_path, 'images')
	for file in os.listdir(image_folder_path):
		if file.endswith('.png'):
			print(file)
			origin_img = cv2.imread(os.path.join(image_folder_path, file))
			reversed_img = cv2.flip(origin_img,1)
			cv2.imwrite(os.path.join(image_folder_path, 'reversed_'+file), reversed_img)
	for file in os.listdir(anno_folder_path):
		if file.endswith('.xml'):
			print(file)
			_reverse_xml(anno_folder_path, file)
	

def _reverse_xml(target_folder_path, target_xml_name):
	tree = parse(os.path.join(target_folder_path, target_xml_name))
	note = tree.getroot()
	# dump(note)
	# print("*"*20)
	if note.find('item') is None:
		filename = note.find('filename').text
		note.find('filename').text = 'reversed_'+filename
		size = note.find('size')
		width = int(size.find('width').text)
		height = int(size.find('height').text)
		for obj in note.findall('object'):
			if obj.find('bndbox'):
				bndbox = obj.find('bndbox')
				xmin = int(float(bndbox.find('xmin').text))
				xmax = int(float(bndbox.find('xmax').text))
				bndbox.find('xmin').text = str(width - xmax)
				bndbox.find('xmax').text = str(width - xmin)
			else:
				xmin = int(float(obj.find('xmin').text))
				xmax = int(float(obj.find('xmax').text))
				obj.find('xmin').text = str(width - xmax)
				obj.find('xmax').text = str(width - xmin)
	else:
		# MOT -> VOC format file
		items = note.findall('item')
		for each_item in items:
			
			if each_item.find('filename') is not None:
				filename = each_item.find('filename').text
				each_item.find('filename').text = 'reversed_'+filename
			
			elif each_item.find('size'):
			
				size = each_item.find('size')
				width = int(size.find('width').text)
				height = int(size.find('height').text)

			elif each_item.find('object'):
				
				for obj in each_item.findall('object'):
					
					if obj.find('bndbox'):
						
						bndbox = obj.find('bndbox')
						xmin = int(float(bndbox.find('xmin').text))
						xmax = int(float(bndbox.find('xmax').text))
						bndbox.find('xmin').text = str(width - xmax)
						bndbox.find('xmax').text = str(width - xmin)
					else:
					
						xmin = int(float(obj.find('xmin').text))
						xmax = int(float(obj.find('xmax').text))
						obj.find('xmin').text = str(width - xmax)
						obj.find('xmax').text = str(width - xmin)

	# dump(note)
	ElementTree(note).write(os.path.join(target_folder_path, 'reversed_'+target_xml_name))