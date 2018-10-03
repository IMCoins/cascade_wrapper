import os
import cv2
import sys
import pyrealsense2 as rs
import numpy as np
from scipy.misc import imsave

def save_image(result, image):
	if not os.path.exists('./temporary'):
		os.makedirs('./temporary')
	if not os.path.exists('./temporary/img'):
		os.makedirs('./temporary/img')
	all_images = os.listdir("./temporary/img")

	name = "temp_" + str(len(all_images)) + ".jpg"
	print name
	with open("./temporary/gen.txt", "a") as f:
		for (x, y, w, h) in result:
			f.write("./temporary/img/{} 1 {} {} {} {}\n".format(name, x, y, w, h))

	imsave("./temporary/img/{}".format(name), image)

def main_2(xml):
	cascade = cv2.CascadeClassifier(xml)
	path = '/home/louis/Documents/python_project/model_trainer/test_classifier/Batch_Kilian_2/test_images/positives_test.txt'
	with open(path) as f:
		lines = f.readlines()
		for line in lines:
			instruction = line.split()
			name = instruction.pop(0)
			file_name = name.split('/')[-1]
			nb = instruction.pop(0)

			img = cv2.imread(name)
			gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			result = cascade.detectMultiScale(gray_image)
			for (x, y, w, h) in result:
				# image = np.ascontiguousarray(img, dtype=np.uint16)
				cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0))

			cv2.imshow(file_name, img)
			cv2.waitKey(0)
			cv2.destroyWindow(file_name)

def main(path_to_xml):
	cascade = cv2.CascadeClassifier(path_to_xml)
	path = '/home/louis/Documents/python_project/model_trainer/test_classifier/Batch_Kilian_2/test_images/positives_test.txt'
	with open(path) as f:
		lines = f.readlines()
		img = cv2.imread(lines[0].split()[0])
		cv2.imshow('', img)
		cv2.waitKey(0)
	# pipe = rs.pipeline()
	# profile = pipe.start()
	sys.exit()
	try:
		while True:
			frames = pipe.wait_for_frames()
			color_frame = frames.get_color_frame()
			image = np.asanyarray(color_frame.get_data())[..., ::-1]

			gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			result = cascade.detectMultiScale(gray_image)
			for (x, y, w, h) in result:
				image = np.ascontiguousarray(image, dtype=np.uint16)
				cv2.rectangle(result, (x, y), (x+w, y+h), (0, 255, 0))
			cv2.imshow('Blehbleh', image)

			k = cv2.waitKey(1) & 0xFF
			if k == 27:
				break

			if not isinstance(result, tuple):
				print result
				# for x, y, w, h in result:
				# 	print x, y, w, h
				# save_image(result, image)
	finally:
		cv2.destroyAllWindows()
		pipe.stop()

if __name__ == '__main__':
	PATH_TO_XMl = "./test_classifier/Batch_Kilian_2/output/cascade.xml"
	# PATH_TO_XMl = "haarface.xml"
	main_2(PATH_TO_XMl)