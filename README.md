# Door Knob Detector

## Context

Extia is a french consulting company that is investing in new technologies such as data science and robotics. They are working on a robot that needs to be able to open doors in order to provide diverse services.

## The project

As a consulting engineer, I helped them on my free inter-project time to build a model that would be able to detect the position of door knobs. As the robot needs to be able to detect the door knob, and adjust its grip accordingly, I built a Machine Learning model using the most famous computer vision library : opencv2.

## How to use

###	Requirements

This repository needs several librairies in order to work properly : 

* python 2.7
* opencv2
* numpy
* scipy
* pyrealsense2

###	Let's get started

There are several modules to use in this project, in order of execution :

* data_gathering.py
* data_labeling.py
* train.py
* test.py

___

1. data_gathering.py

Connect your IntelRealSense camera to your computer and launch this file. A window should open, displaying the current image of your camera.

There are some commands to use while the window is opened, and the program, live :

-	`s` will save the current frame in the directory of your choice.
-	`ESC` will exit the program.

2.	data_labeling.py

The camera is not needed during this operation. If not already done, you can unplug the camera.

Launch the program, and a fixed image will appear. It is awaiting for your input to classify your images. The possible actions are : 

-	`ESC` exits the program.
-	`d` selects the top-left corner of your current selection.
-	`f` selects the bottom-right corner of your current selection.
-	`q` deletes the last selection, if any.
-	`ENTER` sets the image as classified, and displays the next image.

3.	train.py

In order to correctly train your model, you need to have a set of positive, and negative images. 
A positive image is an image in which the object you wish to detect is present, and classified.
A negative image is an image in which the object you wish to detect is not present, as opposed to positive images.

4.	test.py

Directory tree will be :
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