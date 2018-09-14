import pyrealsense2 as rs
import numpy as np
import cv2
import os
from scipy.misc import imsave

def save_image(result, image):
	all_images = os.listdir("./temporary/img")

	name = "temp_" + str(len(all_images)) + ".jpg"
	print name
	with open("./temporary/gen.txt", "a") as f:
		for (x, y, w, h) in result:
			f.write("./temporary/img/{} 1 {} {} {} {}\n".format(name, x, y, w, h))

	imsave("./temporary/img/{}".format(name), image)

def main(path_to_xml):
	cascade = cv2.CascadeClassifier(path_to_xml)

	pipe = rs.pipeline()
	profile = pipe.start()
	try:
		while True:
			frames = pipe.wait_for_frames()
			color_frame = frames.get_color_frame()
			image = np.asanyarray(color_frame.get_data())[..., ::-1]

			gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			result = cascade.detectMultiScale(gray_image)
			# for (x, y, w, h) in result:
			# 	image = np.ascontiguousarray(image, dtype=np.uint16)
			# 	cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0))
			cv2.imshow('Blehbleh', image)

			k = cv2.waitKey(1) & 0xFF
			if k == 27:
				break

			if not isinstance(result, tuple):
				for x, y, w, h in result:
					print x, y, w, h
				save_image(result, image)
	finally:
		cv2.destroyAllWindows()
		pipe.stop()

if __name__ == '__main__':
	PATH_TO_XMl = "./output/cascade.xml"
	main(PATH_TO_XMl)