import cv2
from os import sep

def parse_video(video_path, images_path, frame_step):
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
		
		if cv2.waitKey(0) & 0xFF == ord('q'):
			break

	cap.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
	parse_video('C:\\Users\\SoMa\\myworkspace\\object_detection_testset\\tracking.mp4', '.', 30)
