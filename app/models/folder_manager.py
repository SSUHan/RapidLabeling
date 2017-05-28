import os
import json
from app import rc_app
import random
from flask import jsonify
from .data_center import DataControllor

class FolderManager:
	built = False
	def __init__(self):
		self.activated_datacontrollor_dict = {}
		
		self.load_config()
		self.built = True

	def load_config(self):
		infomation_file = os.path.join(rc_app.root_path, "static", "datacenter", "foldermanager_infomation.json")
		with open(infomation_file) as f:
			self.infomation_json = json.load(f)
		print(len(self.infomation_json['datacenter_list']))
		self.datacenter_root_path = os.path.join(rc_app.root_path, "static", "datacenter")


	def get_data_controllor(self, hashid):
		if not hashid in self.infomation_json['datacenter_list']:
			# 애초에 hashid가 등록되어 있지 않다면, 에러를 뱉는다
			return False
		
		if hashid in self.activated_datacontrollor_dict:
			# activated 되어있다면 그대로 넘겨주고
			return self.activated_datacontrollor_dict[hashid]
		else:
			# 그렇지 않다면, 새로 만들어서 넘겨주고
			self.activated_datacontrollor_dict[hashid] = DataControllor(self.datacenter_root_path, hashid)
			return self.activated_datacontrollor_dict[hashid]


	def make_new_hashid(self):
		new_hashid = ""
		while True:
			for i in range(6):
				new_hashid += str(random.randint(1,9))
			if not new_hashid in self.infomation_json['datacenter_list']:
				self.infomation_json['datacenter_list'].append(new_hashid)
				infomation_file = os.path.join(rc_app.root_path, "static", "datacenter", "foldermanager_infomation.json")
				with open(infomation_file, 'w+') as f:
					json.dump(self.infomation_json, f)
				break
			print("dupicate hash id")
		return new_hashid

	def _is_datacenter(self, hash_id):
		folder_name = "video_{}".format(hash_id)
		folder_path = os.path.join(rc_app.root_path, "static", "datacenter", folder_name)
		return os.path.isdir(folder_path)

	def make_datacenter_path(self, hash_id, owner, frame_num):
		"""
			if there is not datacenter directory, then make it and return hash id
			make directory for new avi hash id
		"""
		if not self._is_datacenter(hash_id):
			folder_name = "video_{}".format(hash_id)
			folder_path = os.path.join(rc_app.root_path, "static", "datacenter", folder_name)
			os.mkdir(folder_path)
			os.mkdir(os.path.join(folder_path, "annotations"))
			os.mkdir(os.path.join(folder_path, "images"))
			json_file = {}
			json_file['owner'] = owner
			json_file['frame_num'] = frame_num
			json_file['skip_step'] = 1 
			json_file['root_folder_path'] = folder_path
			json_file['images_folder_path'] = os.path.join(folder_path, 'images')
			json_file['annotations_folder_path'] = os.path.join(folder_path, 'annotations')
			json_file['current_image_number'] = 0
			with open(os.path.join(folder_path, "{}_infomation.json".format(hash_id)), "w+") as f:
				json.dump(json_file, f)
		else:
			folder_name = "video_{}".format(hash_id)
			folder_path = os.path.join(rc_app.root_path, "static", "datacenter", folder_name)
		return folder_path

	def remove_all_video_datacenter(self):
		"""
			Remove all video datacenter folders
		"""
		pass