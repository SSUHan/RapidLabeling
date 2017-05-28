import cv2

def parse_video(video_path, images_path, frame_step):
	cap = cv2.VideoCapture(video_path)
	frameNum = 0
	
	cv2.namedWindow('Detection Window',cv2.WINDOW_NORMAL)
	cv2.resizeWindow('Detection Window', 600,600)
	
	while True:
		ret, frame = cap.read()
		if not ret:
			break
		frameNum += 1
		if frameNum % frame_step != 0:
			continue
		print("Save Image frameNum : ", frameNum)
		resized_frame = cv2.resize(frame, (448, 448))
		cv2.imshow('Detection Window', resized_frame)
		if cv2.waitKey(0) & 0xFF == ord('q'):
			break

	cap.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
	parse_video('/Users/myZZUNG/myworkspace/git-storage/RapidLabeling/app/static/datacenter/video_375145/video_375145.mp4', 30)
