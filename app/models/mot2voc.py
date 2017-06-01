# PETS09-S2L1
import cv2
import dicttoxml
from xml.dom.minidom import parseString
import os

def make_frame_name(frameNum, space_size=6):
	"""
		36 -> return 000036
	"""
	frame_num_str = str(frameNum)
	zero_str = ''
	for i in range(space_size-len(frame_num_str)):
		zero_str += '0'

	return zero_str+frame_num_str

def parse_video(video_path, image_name, images_folder_path, frame_step):
	"""
		video_path : video file location
		image_name : image prefix name
		images_folder_path : dest image folder path
		frame_step : step size for saving image from video
	"""
	if not isinstance(frame_step, int):
		frame_step = 60 # default 
	
	cap = cv2.VideoCapture(video_path)
	frameNum = 0
	
	while True:
		ret, frame = cap.read()
		if not ret:
			break
		frameNum += 1
		if frameNum % frame_step != 0:
			continue
		print("Save Image frameNum : ", frameNum)
		resized_frame = cv2.resize(frame, (448, 448))
		cv2.imwrite(os.path.join(images_folder_path, image_name+"_{}.png".format(make_frame_name(frameNum))), resized_frame)
		
	cap.release()
	cv2.destroyAllWindows()


def mot_gt2_voc_xml(origin_wh, target_wh, total_frame_num, file_name, annotations_path='annotations'):

	origin_w, origin_h =origin_wh
	rapid_w, rapid_h = target_wh

	obj = []
	for i in range(total_frame_num+1):
		obj.append([])
	print(len(obj))

	with open('gt/gt.txt', 'r') as f:
		lines= f.readlines()
		for i in range(len(lines)):
			one_words = lines[i].split(',')
			frame_num = int(one_words[0])
			object_id = int(one_words[1])
			xmin = float(one_words[2])
			ymin = float(one_words[3])
			width = float(one_words[4])
			hights = float(one_words[5])

			new_xmin = int(xmin/origin_w*rapid_w)
			new_ymin = int(ymin/origin_h*rapid_h)
			new_xmax = int((xmin+width)/origin_w*rapid_w)
			new_ymax = int((ymin+hights)/origin_h*rapid_h)
			obj[frame_num].append(('person', new_xmin, new_ymin, new_xmax, new_ymax))

	frame_num = 0
	for each_frame in obj:
		if len(each_frame) == 0:
			continue
		
		frame_num += 1
		each_obj = {'annotation':[{'filename':'{}_{}.png'.format(file_name,make_frame_name(frame_num))}, 
								{'owner':'JunsuLee'},
								{'size':{'width':rapid_w,
										'height':rapid_h,
										'depth':3}}]}
		for _class, xmin, ymin, xmax, ymax in each_frame:
			each_obj['annotation'].append({'object':{'name':_class, 
													'xmin':xmin,
													'ymin':ymin,
													'xmax':xmax,
													'ymax':ymax}})

		xml = dicttoxml.dicttoxml(each_obj, root=False, attr_type=False)
		dom = parseString(xml)
		with open(os.path.join(annotations_path, '{}_{}.xml'.format(file_name, make_frame_name(frame_num))), 'w+') as f:
			f.write(dom.toprettyxml())

# class_color = (255, 255, 0)

if __name__ == '__main__':
	"""
		Folder Structure : 
		root/
			gt/
				gt.txt
			street.avi
			annotations/
			images/
			mot2voc.py
	"""
	parse_video('street.avi', 'street', 'images', 1)
	mot_gt2_voc_xml((768, 576), (448, 448), 795, 'street')


# video_path = 'street.avi'
# cap = cv2.VideoCapture(video_path)
# frame_num = 1
# while True:
# 	ret, frame = cap.read()
# 	if not ret:
# 		break
# 	resized_frame = cv2.resize(frame, (448, 448))
	
# 	for _class, xmin, ymin, xmax, ymax in obj[frame_num]:
# 		cv2.rectangle(resized_frame,
# 			(xmin, ymin), (xmax, ymax),
# 			class_color, 2)

# 		cv2.putText(resized_frame, _class, (int(xmin), int(ymin-12)), 2, 1.5, class_color)
# 	cv2.imshow('window', resized_frame)
# 	wk = cv2.waitKey(0)
# 	if wk & 0xFF == ord('q'):
# 		break
# 	frame_num += 1 

# cap.release()
# cv2.destroyAllWindows()
