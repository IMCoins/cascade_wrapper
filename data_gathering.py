import os
import argparse
import logging
import json
import cv2
import pyrealsense2 as rs
import numpy as np
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
	if settings['test']:
		sub_dir += settings['test_dir']

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

def create_sub_batch_dir(config, path_to_batch):
	raw_pos_batch = path_to_batch + config['raw_pos_dir_name']
	if not os.path.exists(raw_pos_batch):
		os.makedirs(raw_pos_batch)
		logging.info('Creating raw positives directory at {}'\
					 .format(os.path.abspath(raw_pos_batch)))

	pos_batch = path_to_batch + config['pos_dir_name']
	if not os.path.exists(pos_batch):
		os.makedirs(pos_batch)
		logging.info('Creating positives directory at {}'\
					 .format(os.path.abspath(pos_batch)))

	neg_batch = path_to_batch + config['neg_dir_name']
	if not os.path.exists(neg_batch):
		os.makedirs(neg_batch)
		logging.info('Creating negatives directory at {}'\
					 .format(os.path.abspath(neg_batch)))

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

	test_imgs = batch_dir + config['test_dir']
	if not os.path.exists(test_imgs):
		os.makedirs(test_imgs)
		logging.info('Creating test directory at {}'\
					 .format(os.path.abspath(test_imgs)))

	if create_sub_batch_dir(config, batch_dir) == 0:
		logging.critical("Failed to create directory in {}"\
						 .format(os.path.abspath(batch_dir)))
		return 0
	if create_sub_batch_dir(config, test_imgs) == 0:
		logging.critical("Failed to create directory in {}"\
						 .format(os.path.abspath(test_imgs)))
		return 0

	return 1

def check_paths(config):
	"""
		Returns:
			0 if behavior is wrong.
			1 if everything is fine.
		Note : At the moment, it always returns 1.
	"""
	if config['images'][-1] != '/':
		config['images'] += '/'

	if config['batch_name'][-1] != '/':
		config['batch_name'] += '/'

	if config['raw_pos_dir_name'][-1] != '/':
		config['raw_pos_dir_name'] += '/'

	if config['pos_dir_name'][-1] != '/':
		config['pos_dir_name'] += '/'

	if config['neg_dir_name'][-1] != '/':
		config['neg_dir_name'] += '/'

	if config['test_dir'][-1] != '/':
		config['test_dir'] += '/'

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

	parser.add_argument('-t', action='store_true')
	args = parser.parse_args(['-tp'])

	logging.basicConfig(level=10)

	with open(os.path.abspath('settings.json'), 'r') as json_file:
		config = json.load(json_file)
		config['test'] = args.t
		config['action'] = args.p

	print "Test:{}\nAction:{}\n".format(config['test'], config['action'])
	data_gathering(config)