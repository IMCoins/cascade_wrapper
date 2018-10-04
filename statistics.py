def positive_image_stats(objs_found, nb_objs):
	"""	Update our general positive image stats.

		Args:
			objs_found : int
				Number of objects found in image.
			nb_objs : int
				Total number of objects in image.

		Returns:
			tuple: (true_pos, false_neg, true_neg, false_pos)
	"""
	true_pos = 0
	false_neg = 0
	false_pos = 0

	#	If our match is correct, just set the true_pos value.
	if objs_found == nb_objs:
		true_pos += objs_found
	else:

		#	Otherwise...
		#	If the number of objects found is superior, the excedents are false positives...
		#	Else... the excedents are false_negatives.
		diff = nb_objs - objs_found
		if diff > 0:
			true_pos += nb_objs - diff
			false_neg += diff
		else:
			true_pos = nb_objs
			false_pos += abs(diff)

	return (true_pos, false_neg, 0, false_pos)

def negative_image_stats(objs_found):
	"""	Update our general negative image stats.

		Args:
			objs_found : int
				Number of objects found in image.

		Returns:
			tuple: (true_pos, false_neg, true_neg, false_pos)
	"""
	true_neg = 0
	false_pos = 0
	if objs_found == 0:
		true_neg = 1
	else:
		false_pos = objs_found

	return (0, 0, true_neg, false_pos)


if __name__ == '__main__':
	total_positives = 40
	total_negatives = 40
	print (positive_image_stats(3, 1))
	print (negative_image_stats(0))