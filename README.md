# Door Knob Detector

## Context

Extia is a french consulting company that is investing in new technologies such as data science and robotics. They are working on a robot that needs to be able to open doors in order to provide diverse services.

## The project

As a consulting engineer, I helped them on my free inter-project time to build a model that would be able to detect the position of door knobs. As the robot needs to be able to detect the door knob, and adjust its grip accordingly, I built a Machine Learning model using the most famous computer vision library : opencv2 and its function CascadeClassifier.

## How to use

###	Requirements

This repository needs several librairies in order to work properly : 

* python 2.7
* opencv2 : Reading and modeling.
* numpy : Interpreting images and converting them.
* scipy : Saving images correctly.
* pyrealsense2 : Getting camera stream.

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

* images

	This is the parent folder of your project.

* batch_name : 

	A batch is an iteration of your project. You can come back to one's batch later on to improve it. (implementation improvement idea : Add a module to merge two batchhes together)

* generic_image_name :

	This value defines what will prefix each of your images name when you gather it.

* raw_pos_dir_name : 

	This folder is placed in your batch, and is the folder in which the *non*-classified positive images are going.

* pos_dir_name :

	This folder is placed in your batch, and is the folder in which the classified positive images are going.

* neg_dir_name : 

	This folder is placed in your batch, and is the folder in which the negative images are going.

* output : 

	This directory received your trained model. `output` is short for `output` of training.

* img_ext : 

	Extension of the images you're going to save while gathering.


	2. data_gathering.py

Connect your IntelRealSense camera to your computer and launch this file. A window should open, displaying the current image of your camera. The purpose of this file is to gather data and arrange it as parametered in settings.json.

This file takes one of the two following parameters in order to be launched properly :

-	`-p` 
-	`-n`

There are some commands to use while the window is opened, and the program, live :

-	`s` will save the current frame in the directory of your choice.
-	`ESC` will exit the program.

ff
	3.	data_labeling.py

The camera is not needed during this operation. If not already done, you can unplug the camera.

Launch the program, and a fixed image will appear. It is awaiting for your input to classify your images. The possible actions are : 

-	`ESC` exits the program.
-	`d` selects the top-left corner of your current selection.
-	`f` selects the bottom-right corner of your current selection.
-	`q` deletes the last selection, if any.
-	`ENTER` sets the image as classified, and displays the next image.


ff
	4.	train.py

In order to correctly train your model, you need to have a set of positive, and negative images. 
A positive image is an image in which the object you wish to detect is present, and classified.
A negative image is an image in which the object you wish to detect is not present, as opposed to positive images.

	5.	test.py

ggg