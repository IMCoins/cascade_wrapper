import cv2
import os
import json
import pyrealsense2 as rs
import numpy as np

from scipy.misc import imsave
from show_image_label import next_rect

from geometry import Rectangle, Point

from statistics import positive_image_stats, negative_image_stats
from dashboard import show_data

#	Graph and Best matching algorithms
import networkx as nx
from networkx.algorithms.bipartite.matching import maximum_matching as mm

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

			# if objects is a tuple, it is an empty tuple.
			# else it is a list, and it has detected elements.
			if not isinstance(objects, tuple):
				save_image(objects, image, image_folder)
	finally:
		cv2.destroyAllWindows()
		pipe.stop()

def does_rect_overlap(pred_rect, rectangles, threshold):
	found = []

	pred_area = pred_rect.area
	for rect in rectangles:
		area_diff = pred_area - rect.get_common_area(pred_rect)

		percentage_diff = pred_area / area_diff * 100
		if percentage_diff > threshold:
			rectangles.remove(rect)
			found += [[pred_rect, rect]]

	return found

def test_batch(cascade, settings):
	path_to_images = settings['images'] + settings['batch_name'] + settings['test_dir']
	pos_summary = path_to_images + settings['pos_dir_name'][:-1] + '.txt'
	neg_summary = path_to_images + settings['neg_dir_name'][:-1] + '.txt'


	# stats = true_pos, false_neg, true_neg, false_pos
	stats = np.array( [0, 0, 0 ,0] )
	with open(pos_summary) as pos:
		lines = pos.readlines()
		for instructions in lines:
			#	Instantiation of graph, used for best_matching algorithm.
			pos_graph = nx.Graph()

			elements = instructions.split(' ')

			#	Storing name of image to make predictions on, and the number of objects in it.
			name = elements.pop(0)
			nb_objs = int(elements.pop(0))

			#	Objects contain the real position of all the objects in image.
			gen = next_rect(elements)
			real_objects = [obj for obj in gen]

			#	Opening image and making predictions on it.
			image = cv2.imread(name)
			gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			pred_objects = cascade.detectMultiScale(gray_image)

			#	Threshold as to "minimum percentage of similitude for acceptance"
			threshold = 90

			#	Linking each predicted rectangle to real objects that match the % threshold.
			for found in pred_objects:
				top = Point(found[0], found[1])
				bot = Point(found[0] + found[2], found[1] + found[3])
				curr_found = Rectangle(top, bot)
				pos_graph.add_node(curr_found)
				ok = does_rect_overlap(curr_found, real_objects, threshold)
				for pred_rect, rect in ok:
					pos_graph.add_edge(pred_rect, rect)
		
			#	Now that our graph is done, let's check in our subgraphs, and count
			#	the maximum elements that match our objects.
			subgraphs = nx.connected_component_subgraphs(pos_graph)
			objs_found = 0
			for graph in subgraphs:
				if len(graph.nodes) == 2:
					# print 'eh'
					objs_found += 1
				else:
					# print 'oh'
					max_match = mm(graph)
					objs_found += len(max_match)
					
			#	Update our general positive image stats:
			stats += positive_image_stats(objs_found ,nb_objs)

	with open(neg_summary) as neg:
		lines = neg.readlines()
		for instructions in lines:
			instructions = instructions.strip('\n')

			image = cv2.imread(instructions)
			gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			pred_objects = cascade.detectMultiScale(gray_image)

			#	Update out general stats.
			stats += negative_image_stats( len(pred_objects) )

	show = True
	if show:
		show_data(*stats)
	return 1

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
	cascade = cv2.CascadeClassifier( "./{}{}{}cascade.xml"\
		.format(settings['images'], settings['batch_name'], settings['output']) )
	if stream:
		streaming_test(cascade, default_saving_folder)
	else:
		test_batch(cascade, settings)

if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument("--stream", action='store_true',
		help = "Activate streaming testing, instead of batch testing")
	parser.add_argument("--folder", default='default_test/')
	args = parser.parse_args()

	with open(os.path.abspath('settings.json'), 'r') as json_file:
		settings = json.load(json_file)
	main(settings, args.stream, default_saving_folder = args.folder)