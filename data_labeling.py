import os
import argparse
import logging
import json
import cv2
import sys

from data_gathering import check_paths

def check_directories(settings):
	"""	Checks if the directories exists.
		If not, it means the data hasn't been previously gathered as it must.
	"""
	if not os.path.exists(settings['images']):
		logging.critical("The directory {} doesn't exist. You must gather data before trying to label it."\
						 .format(os.path.abspath(settings['images'])))
		return 0

	batch_dir = settings['images'] + settings['batch_name']
	if not os.path.exists(batch_dir):
		logging.critical("The directory {} doesn't exist. You must gather data before trying to label it."\
						 .format(os.path.abspath(batch_dir)))
		return 0

	raw_pos_batch = batch_dir + settings['raw_pos_dir_name']
	if not os.path.exists(raw_pos_batch):
		logging.critical("The directory {} doesn't exist. You must gather data before trying to label it."\
						 .format(os.path.abspath(raw_pos_batch)))
		return 0

	return 1

def classifier_args_checker(func):
	def wrapper(settings):
		err = check_directories(settings)
		if not err:
			logging.critical("Stopping program after directory checking.")
			return 0

		err = check_paths(settings)
		if not err:
			logging.critical("Stopping program after path checking.")
			return 0

		return func(settings)

	return wrapper

def format_obj_display(stack):
	"""
	"""
	if len(stack) > 0:
		mess = ""
		for idx, obj in enumerate(stack, start=1):
			mess += "\t{}_ top-left corner : {}, bottom-right corner : {}\n"\
					.format(idx, obj[0], obj[1])
		return mess
	else:
		return ("\tNo object at the moment.")

_x, _y = 0, 0
def func(event,x,y,flags,params):
	"""
	"""
	global _x, _y

	#	If we do have both corners set...
	if params['top'] and params['bot']:

		#	... and properly set (meaning the top-left actually in the top-left for instance)
		if (params['top'][0] < params['bot'][0]) and (params['top'][1] < params['bot'][1]):
			#	Save current image, and draw.
			params['images'].append( params['images'][-1].copy() )
			params['stack'].append( [params['top'], params['bot']] )
			cv2.rectangle(params['images'][-1], params['top'], params['bot'], params['color'])
		else:
			#	Do nothing. Rectangle is not good.
			logging.info("Your rectangle cannot be drawn as the bottom-right corner is above the top-left corner.")
		
		#	Resetting corners, as it's either invalid, or used.
		params['top'], params['bot'] = None, None

	_x, _y = x, y

def classify_image(settings, parameters, image_name):
	"""
	"""
	path = settings['images'] + settings['batch_name']
	if settings['action']:
		path += settings['test_dir']
	line = "./{} {} ".format( settings['pos_dir_name'] + image_name, len(parameters['stack']) )
	for coord in parameters['stack']:
		x, y, w, h = coord[0][0], coord[0][1], coord[1][0] - coord[0][0], coord[1][1] - coord[0][1]
		line += "{} {} {} {} ".format(x, y, w, h)

	with open(path + settings['pos_dir_name'][:-1] + '.txt', "a") as f:
		f.write(line + '\n')
		os.rename(path + settings['raw_pos_dir_name'] + image_name,
				  path + settings['pos_dir_name'] + image_name)

@classifier_args_checker
def image_classifier(settings):
	"""
		Args:
			settings: dict
				This parameter comes from the json settings file.
				You shall not change the keys value, but you can change their
				values in order to custom your experience.
		Returns:
			None. This function is meant to be used as a stand-alone.
	"""
	path = settings['images'] + settings['batch_name'] + settings['raw_pos_dir_name']
	images = os.listdir(path)
	for image_name in images:
		#	Opening new image from non-classified images.
		image = cv2.imread(path + image_name)

		#	Setting basic parameters.
		parameters = {
			'top' : None,
			'bot' : None,
			'color' : (0, 255, 0),
			'stack' : [],
			'images' : [image.copy()]
		}

		while True:
			cv2.imshow('img', parameters['images'][-1])
			cv2.setMouseCallback('img', func, parameters)
			k = cv2.waitKey(1)
			if k == 27: # ESC KEYSTROKE
				sys.exit()
			elif k == ord('d'):
				parameters['top'] = _x, _y
			elif k == ord('f'):
				parameters['bot'] = _x, _y
			elif k == ord('q'):
				try:
					parameters['stack'].pop(-1)
					parameters['images'].pop(-1)
				except IndexError:
					logging.info("You cannot delete more figures as there are None.")
			elif k == 10 or k == 13: # ENTER KEYSTROKE
				logging.info('NEXT')
				classify_image(settings, parameters, image_name)
				break
			elif k == ord('h'):
				logging.info("You have currently selected {} objects, at :\n{}"\
							 .format(len(parameters['stack']),
							 		 format_obj_display(parameters['stack'])))

	return

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-t', action='store_true')
	args = parser.parse_args(['-t'])

	logging.basicConfig(level=10)

	with open(os.path.abspath('settings.json'), 'r') as json_file:
		config = json.load(json_file)
		config['action'] = args.t

	image_classifier(config)