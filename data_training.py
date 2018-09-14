import logging
import os
import json
import argparse
import cv2

def minus_n_percent(n_percent, number):
	return( float(number) - (float(number) / 100. * float(n_percent)) )

def training_args_checker(func):
	def checker(settings):
		path = os.path.abspath("{}{}{}".format(settings['images'],
											   settings['batch_name'],
											   settings['output']))
		if not os.path.exists(path):
			os.makedirs(path)
		else:
			logging.warning("As an output already exists, are you sure you want to continue ? (y/N)")
			k = raw_input("")
			if k != 'y':
				return 0

		return func(settings)

	return checker

@training_args_checker
def training(settings):
	path_to_batch = settings['images'] + settings['batch_name']

	pos_batch = len( os.listdir(path_to_batch + settings['pos_dir_name']) )
	reduced_pos_batch = minus_n_percent(15, pos_batch)

	neg_batch = len(os.listdir(path_to_batch + settings['neg_dir_name']))

	pos_txt = path_to_batch + settings['pos_dir_name'][:-1] + '.txt'
	neg_txt = path_to_batch + settings['neg_dir_name'][:-1] + '.txt'

	create_vector_feature = \
		'opencv_createsamples \
		-info {pos_txt} \
		-vec {vec_path}feature.vec \
		-num {size} \
		-w 48 \
		-h 48'\
		.format(size=pos_batch, pos_txt=pos_txt, vec_path=path_to_batch)
	os.system(create_vector_feature)

	train_from_vect = \
		'opencv_traincascade \
		-data {output}{version}/ \
		-vec {vec_path}feature.vec \
		-bg {neg_txt} \
		-numPos {size_p} \
		-numNeg {size_n} \
		-numStages 15 \
		-w 48 \
		-h 48 \
		-featureType LBP \
		-precalcValBufSize 16192 \
		-precalcIdxBufSize 16192 \
		-minHitRate 0.995 \
		-maxFalseAlarmRate 0.2'\
		.format(size_p=reduced_pos_batch, size_n=neg_batch,
				neg_txt=neg_txt, version=settings['version'],
				output=os.path.abspath(path_to_batch + settings['output']),
				vec_path=path_to_batch)
	os.system(train_from_vect)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-v', dest="version", default=False, type=int)
	args = parser.parse_args()

	logging.basicConfig(level=10)

	with open(os.path.abspath('settings.json'), 'r') as json_file:
		settings = json.load(json_file)

	#	As we can't force the default value to be an empty string, 
	#	and require the argument to be an int, if the default value is selected,
	#	then, set the value to an empty string.
	if args.version:
		settings['version'] = '_{}'.format(args.version)
	else:
		settings['version'] = ''

	training(settings)