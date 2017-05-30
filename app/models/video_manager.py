import cv2
from os import sep
import os

def make_frame_name(frameNum, space_size=6):
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
		cv2.imshow('window', resized_frame)
		if cv2.waitKey(0) & 0xFF == ord('q'):
			break

	cap.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
	parse_video('C:\\Users\\SoMa\\myworkspace\\object_detection_testset\\tracking.mp4', 
				'tracking'
				,'.', 30)