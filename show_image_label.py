import cv2

def get_corners(rect):
	"""
		Args:
			rect: list
				Data is supposed to be formatted such as rect = [x, y, width, height]
		Returns:
			Properly formatted top left and bottom right corners of the given rectangle.
	"""
	top_left_corner = int(rect[0]), int(rect[1])
	bottom_right_corner = int(rect[0]) + int(rect[2]), int(rect[1]) + int(rect[3])
	return (top_left_corner, bottom_right_corner)

def next_rect(elements):
	"""	Args:
			elements: list
				elements should be formatted such as [x, y, w, h, ..., xn, yn, wn, hn]
		Yields:
			Both top left and bottom right corners of the next rectangle in list.
	"""
	while elements:
		top_corner, bottom_corner = get_corners(elements[:4])
		elements = elements[4:]
		yield top_corner, bottom_corner

def main(images_summary, specific=[]):
	"""
		Args:
			images_summary: path
				images_summary is a .txt file that sums up the location of the images
				to read, and to display the rectangles on.
			specific: list
				default : empty list
				If specific has names in it, only the lines with the names given in specific
				parameter will be kept.

	"""
	with open(images_summary) as f:
		lines = f.readlines()
		for instructions in lines:
			# Line format is :
			# <name> <nb_objs> <x> <y> <width> <height> ... <x_n> <y_n> <width_n> <height_n>
			elements = instructions.split(" ")
			name = elements.pop(0)
			nb_objs = elements.pop(0)

			if specific:
				parsed_name = name.split('/')[-1]
				if parsed_name not in specific:
					continue

			try:
				img = cv2.imread(name)

				#	Displays all the rectangle into the image we just read.
				gen = next_rect(elements)
				for _ in range(int(nb_objs)):
					top_corner, bottom_corner = next(gen)
					cv2.rectangle(img, top_corner, bottom_corner, (0, 255, 0), 1)

				#	Displays window and wait for input.
				cv2.imshow(name, img)
				cv2.moveWindow(name, 400, 100)
				k = cv2.waitKey(0) & 0xFF
				if k == 27:
					break
			finally:
				#	This will destroy the current window even though we're breaking the loop.
				cv2.destroyWindow(name)

if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('gen_file',
		help = "Path to file in which are registered the images name and the rectangles to draw")
	parser.add_argument('--images', default = [], nargs = '+',
		help = "Specific images to seek, instead of all images if not specified")
	args = parser.parse_args()

	main(args.gen_file, args.images)