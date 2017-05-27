import os
import json
from app import rc_app
import random

class FolderManager:
	built = False
	def __init__(self):
		self.load_config()
		self.built = True

	def load_config(self):
		infomation_file = os.path.join(rc_app.root_path, "static", "datacenter", "datacenter_infomation2.json")
		with open(infomation_file) as f:
			self.infomation_json = json.load(f)
		print(len(self.infomation_json['datacenter_list']))

	def make_new_hashid(self):
		new_hashid = ""
		while True:
			for i in range(6):
				new_hashid += str(random.randint(1,9))
			if not new_hashid in self.infomation_json['datacenter_list']:
				self.infomation_json['datacenter_list'].append(new_hashid)
				infomation_file = os.path.join(rc_app.root_path, "static", "datacenter", "datacenter_infomation2.json")
				with open(infomation_file, 'w+') as f:
					json.dump(self.infomation_json, f)
				break
			print("dupicate hash id")
		return new_hashid

	def _is_datacenter(self, hash_id):
		folder_name = "video_{}".format(hash_id)
		folder_path = os.path.join(rc_app.root_path, "static", "datacenter", folder_name)
		return os.path.isdir(folder_path)

	def get_datacenter_path(self, hash_id):
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
			open(os.path.join(folder_path, "{}_infomation.json".format(hash_id)), "w+").close()
		else:
			folder_name = "video_{}".format(hash_id)
			folder_path = os.path.join(rc_app.root_path, "static", "datacenter", folder_name)
		return folder_path
