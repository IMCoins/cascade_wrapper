import json
import logging
import argparse

#	intel lib that reads the camera
import pyrealsense2 as rs

#	Read and display the image
import cv2

#	Get the color of an image
import numpy as np

#	Path checking
import os

#	To save the image
from scipy.misc import imsave

def save_img_to_batch(settings, image_to_save):
	"""
		Args:
			settings:dict
				Type help(data_gathering) for more information.
			image_to_save: 3D array (RGB, formatted WxHx3)
		Directory tree will be like:
			- "images"
				- "batch_name"
					- "raw_pos_dir_name"
						- "generic_image_name" + <number>
					- "pos_dir_name"
						- "generic_image_name" + <number>
					- "neg_dir_name"
						- "generic_image_name" + <number>
				- "batch_name"
					...
	"""
	sub_dir = settings['images'] + settings['batch_name']
	if settings['action']:
		sub_dir += settings['raw_pos_dir_name']
	else:
		sub_dir += settings['neg_dir_name']

	images = os.listdir(sub_dir)

	#	Adds a free number after the image_name.
	file_name = settings['generic_image_name'] + str(len(images))
	img_path = '{}{}{}'.format(sub_dir, file_name, settings['img_ext'])
	imsave(img_path, image_to_save)
	logging.info("Image saved at {}".format(img_path))

	#	This updates the .txt file that sums up all the
	#	negative image stored.
	#	NOTE : If you delete one manually, you also need to delete
	#		   the reference in the .txt file.
	if not settings['action']:
		neg_text_file = sub_dir[:-1] + '.txt'
		with open(neg_text_file, "a") as f:
			f.write("./{}\n".format(img_path))

	return 1

def check_directories(config):
	"""	Checks if the directories exists.
		If not, create them as the path have been checked earlier on.
	"""
	if not os.path.exists(config['images']):
		os.makedirs(config['images'])
		logging.info('Creating image directory at {}'\
					 .format(os.path.abspath(config['images'])))

	batch_dir = config['images'] + config['batch_name']
	if not os.path.exists(batch_dir):
		os.makedirs(batch_dir)
		logging.info('Creating batch directory at {}'\
					 .format(os.path.abspath(batch_dir)))

	raw_pos_batch = batch_dir + config['raw_pos_dir_name']
	if not os.path.exists(raw_pos_batch):
		os.makedirs(raw_pos_batch)
		logging.info('Creating batch directory at {}'\
					 .format(os.path.abspath(raw_pos_batch)))

	pos_batch = batch_dir + config['pos_dir_name']
	if not os.path.exists(pos_batch):
		os.makedirs(pos_batch)
		logging.info('Creating batch directory at {}'\
					 .format(os.path.abspath(pos_batch)))

	neg_batch = batch_dir + config['neg_dir_name']
	if not os.path.exists(neg_batch):
		os.makedirs(neg_batch)
		logging.info('Creating batch directory at {}'\
					 .format(os.path.abspath(neg_batch)))

	return 1

def check_paths(config):
	"""
		Returns:
			0 if behavior is wrong.
			1 if everything is fine.
	"""
	if config['images'][-1] != '/':
		logging.critical("'{0}' from 'images' parameter in settings file should be '{0}/'"\
						.format(config['images']))
		return 0

	if config['batch_name'][-1] != '/':
		logging.critical("'{0}' from 'batch_name' parameter in settings file should be '{0}/'"\
						.format(config['batch_name']))
		return 0

	if config['raw_pos_dir_name'][-1] != '/':
		logging.critical("'{0}' from 'raw_pos_dir_name' parameter in settings file should be '{0}/'"\
						.format(config['raw_pos_dir_name']))
		return 0

	if config['pos_dir_name'][-1] != '/':
		logging.critical("'{0}' from 'pos_dir_name' parameter in settings file should be '{0}/'"\
						.format(config['pos_dir_name']))
		return 0

	if config['neg_dir_name'][-1] != '/':
		logging.critical("'{0}' from 'neg_dir_name' parameter in settings file should be '{0}/'"\
						.format(config['neg_dir_name']))
		return 0

	return 1

def gathering_args_checker(func):
	"""	This decorator decides whether the function will be played or not.
		It'll also take care of the pre-processing needed to store the files.
	"""
	def wrapper(config):
		err = check_paths(config)
		if not err:
			logging.critical("Program stopped. Please, change the setting file as previously instructed.")
			return 0

		err = check_directories(config)
		if not err:
			#	In the current implementation, this case is impossible.
			#	The function returns 1 everytime.
			return 0

		logging.info('File will be saved into : {}'\
					 .format(os.path.abspath(config['images'] + config['batch_name'])))
		return func(config)

	return wrapper

@gathering_args_checker
def data_gathering(settings):
	"""	
		Args:
			settings: dict
				This parameter comes from the json settings file.
				You shall not change the keys value, but you can change their
				values in order to custom your experience.
		Returns:
			None. This function is meant to be used as a stand-alone.
		Note:
			You need to correctly close this program using `ESC` keystroke.
			If you don't close it properly, the port of the camera might not
			close properly, and you will need to kill the still
			existing process in order to run this program again.
	"""
	pipe = rs.pipeline()
	profile = pipe.start()
	try:
	  while True:
	  	#	Catches next frame.
	  	frames = pipe.wait_for_frames()

	  	#	Gets the image in "color", at format W x H x 3 (RGB)
		color_frame = frames.get_color_frame()
		rgb_image = np.asanyarray( color_frame.get_data() )

		#	As opencv2 displays image in BGR, converting RGB to BGR.
		bgr_image = rgb_image[..., ::-1]
		cv2.imshow(settings['batch_name'], bgr_image)

		#	cv2 uses waitKey to update the current frame window.
		#	Setting 1 as a parameter, our window seems to update as if
		#	it was a constant stream of image.
		k = cv2.waitKey(1)
		if k == 27:
			break
		elif k == ord('s'):
			save_img_to_batch(settings, rgb_image)
	finally:
		cv2.destroyAllWindows()
		pipe.stop()
		
	return 1

if __name__ == '__main__':
	#	Initiating argument parser.
	parser = argparse.ArgumentParser()

	#	There must be only ONE argument from the group arguments.
	#	The parameter `required=True` means that ONE must also
	#	be present.
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('-p', action='store_true')
	group.add_argument('-n', action='store_false')
	args = parser.parse_args()

	logging.basicConfig(level=10)

	with open(os.path.abspath('settings.json'), 'r') as json_file:
		config = json.load(json_file)
		config['action'] = args.p

	data_gathering(config)