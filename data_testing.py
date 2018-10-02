import cv2
import os
import json
import pyrealsense2 as rs
import numpy as np
from scipy.misc import imsave

def save_image(objects, image, folder):
	all_images = os.listdir('./{}img'.format(folder))

	name = "temp_{}.jpg".format(str(len(all_images)))
	with open("./{}gen.txt".format(folder), "a") as out:
		line = "./{}img/{} {}".format(folder, name, len(objects))
		for (x, y, w, h) in objects:
			line += " {} {} {} {}".format(x, y, w, h)
		out.write(line)

	imsave("./{}img/{}".format(folder, name), image)

def streaming_test(cascade, image_folder):
	pipe = rs.pipeline()
	profile = pipe.start()
	try:
		while True:
			frames = pipe.wait_for_frames()
			color_frame = frames.get_color_frame()
			image = np.asanyarray( color_frame.get_data() )[..., ::-1]

			gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			objects = cascade.detectMultiScale(gray_image)
			for (x, y, w, h) in objects:
				image = np.ascontiguousarray(image, dtype=np.uint16)
				cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 1)

			cv2.imshow('', image)
			k = cv2.waitKey(1) & 0xFF
			if k == 27: # Escape has been pressed
				break

			if not isinstance(objects, tuple):
				save_image(objects, image, image_folder)
	finally:
		cv2.destroyAllWindows()
		pipe.stop()

def test_batch(cascade):
	pass

def path_checker(func):
	def wrapper(*args, **kwargs):
		if 'default_saving_folder' in kwargs and\
		   kwargs['default_saving_folder'][-1] != '/':
			kwargs['default_saving_folder'] += '/'

		if not os.path.exists(kwargs['default_saving_folder']):
			os.makedirs(kwargs['default_saving_folder'])
		if not os.path.exists(kwargs['default_saving_folder'] + 'img/'):
			os.makedirs(kwargs['default_saving_folder'] + 'img/')

		return func(*args, **kwargs)
	return wrapper

@path_checker
def main(settings,
		 stream = False,
		 default_saving_folder = "default_test/"):
	print "./{}cascade.xml".format(settings['output'])
	cascade = cv2.CascadeClassifier( "./{}{}{}cascade.xml"\
		.format(settings['images'], settings['batch_name'], settings['output']) )
	if stream:
		streaming_test(cascade, default_saving_folder)
	else:
		test_batch(cascade)

if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument("--stream", action='store_true',
		help = "Activate streaming testing, instead of batch testing")
	parser.add_argument("--folder", default='default_test/')
	args = parser.parse_args(['--stream'])

	with open(os.path.abspath('settings.json'), 'r') as json_file:
		settings = json.load(json_file)
	main(settings, args.stream, default_saving_folder = args.folder)