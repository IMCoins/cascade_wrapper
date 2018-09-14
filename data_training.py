import logging

def minus_n_percent(n_percent, number):
	return( float(number) - (float(number) / 100. * float(n_percent)) )

def training(settings):
	path_to_batch = settings['images'] + settings['batch_name']

	pos_batch = len( os.listdir(path_to_batch + settings['pos_dir_name']) )
	reduced_pos_batch = minus_n_percent(15, positive_set_size)

	neg_batch = len(os.listdir(path_to_batch + settings['neg_dir_name']))

	pos_txt = path_to_batch + settings['pos_dir_name'][:-1] + '.txt'
	neg_txt = path_to_batch + settings['neg_dir_name'][:-1] + '.txt'

	create_vector_feature = 
		'opencv_createsamples \
		-info {pos_txt} \
		-vec feature.vec \
		-num {size} \
		-w 48 \
		-h 48'\
		.format(size=pos_batch, pos_txt=pos_txt)
	os.system(create_vector_feature)

	train_from_vect = 
		'opencv_traincascade \
		-data output/ \
		-vec feature.vec \
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
		.format(size_p=reduced_pos_batch, size_n=neg_batch, neg_txt=neg_txt)
	os.system(train_from_vect)

	folder_path = 'output'.format(version)
	if not os.path.exists(folder_path):
		os.makedirs(folder_path)

if __name__ == '__main__':
	logging.basicConfig(level=10)

	with open(os.path.abspath('settings.json'), 'r') as json_file:
		settings = json.load(json_file)

	training(settings)