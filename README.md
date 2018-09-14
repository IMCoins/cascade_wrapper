# Object Recognition

Extia is a french consulting company that is investing in new technologies such as data science and robotics. They are working on a robot that needs to be able to open doors in order to provide diverse services.

## The project

As a consulting engineer, I helped them on my free inter-project time to build a model that would be able to detect the position of door knobs. As the robot needs to be able to detect the door knob, and adjust its grip accordingly, I built a Machine Learning model using the most famous computer vision library : opencv2 and its function CascadeClassifier.

## General Understanding

There are several steps in order to make a good model, and to verify its quality. You will need to gather data, label it, train it and finally test it. In order to test it properly, you also need to gather **another** set of positive pictures which you will need to label again. When all these steps are done, you finally have built a model, and have statistics defining it (true positives, true negatives, false negatives, as long as general statistics).

There are 2 kind of images, the positives and the negatives.

**Positives** images are the images that contain the object you are looking for. You will later need to **label** these images. Meaning you will need to tell the program where to look for in the image, so that it can learn features about your object such as it's length, shape, color and such.

Once you have understood what's the role of a positive image, you need to gather these. And gather them well ! In order to do this, you need to gather a lot of pictures in different general conditions such as different backgrounds, different positions, different distance, different colors, etc... your imagination is the limit.

As for **Negatives**, these are images in which your object **must not** be present. Would it be distance, angle, shape wise, etc...

## How to use

###	Requirements

This repository needs several librairies in order to work properly : 

* **python 2.7**
* **opencv2**
	Reading and modeling.
* **numpy**
	Interpreting images and converting them.
* **scipy**
	Saving images correctly.
* **pyrealsense2**
	Getting camera stream.

As long as some native python librairies : argparse, os, sys, logging and json.

###	Let's get started

There are several modules to use in this project, in order of execution :

* data_gathering.py
* data_labeling.py
* data_training.py
* test.py

All these modules also use a configuration file named `settings.json` that defines the tree of your model, and its global data (training, testing, non-classified positives).

The tree is defined as followed :

	- "images"
		- "batch_name"
			- "raw_pos_dir_name"
				- "generic_image_name" + <number>
			- "pos_dir_name"
				- "generic_image_name" + <number>
			- "neg_dir_name"
				- "generic_image_name" + <number>
			- "output"
				- cascade.xml
				- n_stages.xml
			- "pos_dir_name".txt
			- "neg_dir_name".txt
			- feature.vec
		- "batch_name"
			- ...
	- "images"
		- ...

___

	1. settings.json

In this file, you will find 8 different parameters, these are the fundation of your tree. Note that _keys_ *MUST NOT* be changed. The values can.

Example : in `"images" : "test_classifier/"`, you can only change what is after the `:` character.

Explanation:

* **images**

	This is the parent folder of your project.

* **batch_name** : 

	A batch is an iteration of your project. You can come back to one's batch later on to improve it. (implementation improvement idea : Add a module to merge two batchhes together)

* **generic_image_name** :

	This value defines what will prefix each of your images name when you gather it.

* **raw_pos_dir_name** : 

	This folder is placed in your batch, and is the folder in which the *non*-classified positive images are going.

* **pos_dir_name** :

	This folder is placed in your batch, and is the folder in which the classified positive images are going.

* **neg_dir_name** : 

	This folder is placed in your batch, and is the folder in which the negative images are going.

* **output** : 

	This directory received your trained model. `output` is short for `output` of training.

* **img_ext** : 

	Extension of the images you're going to save while gathering.

___

	2. data_gathering.py

Connect your IntelRealSense camera to your computer and launch this file. A window should open, displaying the current image of your camera. The purpose of this file is to gather data and arrange it as parametered in settings.json.

This file takes one of the two following parameters in order to be launched properly :

-	`-p` will gather the raw positive images (non-classified positives)
-	`-n` will gather the negative images, and assemble the information into a `.txt` file.

There are some commands to use while the program is live and the focus is on the window :

-	`s` will save the current frame in the directory of either the raw positive, or negative.
-	`ESC` will exit the program.

___

	3.	data_labeling.py

The camera is not needed during this operation. If not already done, you can unplug the camera.

Launch the program, and a fixed image will appear. It is awaiting for your input to classify your images. The possible actions are : 

-	`ESC` exits the program.
-	`d` selects the top-left corner of your current selection.
-	`f` selects the bottom-right corner of your current selection.
-	`q` deletes the last selection, if any.
-	`ENTER` sets the image as classified, and displays the next image.

This will generate a `.txt` file in which all the information needed to classify the image are stored. The pattern is as follows...

`<image_path> <number of features to detect> <x1> <y1> <w1> <h1> ... <xn> <yn> <wn> <hn>`

With `x` and `y` being the top-corner position, and `w` and `h` being the width and height of the rectangle encapsulating the feature.

___

	4.	train.py

In order to correctly train your model, you need to have a set of classified positive, and negative images.

Simply launch `python data_training.py`, and your model will train accordingly to the previous steps you've taken.

You can use the `-v` option to tell your program to continue a specific version of your training, or to make a new one. For instance, do `python data_training.py -v 5`, `5` being the version of your model. It is already specified in the program, but the version parameter must be a number.

___

	5.	test.py

<To Be Completed>