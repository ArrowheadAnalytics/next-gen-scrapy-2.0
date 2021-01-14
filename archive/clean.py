"""
Author: Sarah Mallepalle (updated by Ethan Douglas to work in Python 3)

For every pass chart image, extract only the trapezoidal image of the field, 
undistort the field by turning the trapezoid into a rectangle, remove the sideline labels, 
and save the new image to the folder 'Cleaned_Pass_Charts'.

Folder format: ./Cleaned_Pass_Charts/[team]/[season]/[week]/{[images], [data]}/[last_name]_[first_name]_[positon].{jpeg, txt}
Example: 
	Image path = ./Cleaned_Pass_Charts/philadelphia-eagles/2017/super-bowl/images/Foles_Nick_QB.jpeg
	Data path = ./Cleaned_Pass_Charts/philadelphia-eagles/2017/super-bowl/data/Foles_Nick_QB.txt

"""

import cv2
import os
from undistort_field import *
from pass_detection import *
import json
import scipy.misc

def new_image(image):

	img_name = image.split(os.sep)[-1].split(".")[0]
	img = cv2.imread(image)

	if (img.shape[0:2] == (1200, 1200)):
		crop_img = img[0:680, 0:1200]
		temp_name = img_name + "_temp.jpg"
		cv2.imwrite(temp_name, crop_img)
	else:
		print("Image must be of size (1200, 1200)")
		return

	clean_img = clean_field(temp_name)
	write_path = clean_path + os.sep + os.sep.join(image.split(os.sep)[1:-1]) 
	if not os.path.exists(write_path): os.makedirs(write_path)

	if (clean_img != None):
		write_name = write_path + os.sep + img_name + ".jpeg"
		scipy.misc.imsave(write_name, clean_img)
	os.remove(temp_name)

def new_data(folder, image): 
	data_path = os.sep.join(folder.split(os.sep)[:-1]) + os.sep + "data" 
	data_file = data_path + os.sep + image.split(".")[0] + ".txt"
	new_data_path = clean_path + os.sep + os.sep.join(folder.split(os.sep)[1:-1]) + os.sep + "data" 
	new_data_file = new_data_path + os.sep + image.split(".")[0] + ".txt"


	if not os.path.exists(new_data_path): 
		os.makedirs(new_data_path)

	with open(data_file) as _file: 
		old_data = json.load(_file)
		new_data = {key: old_data[key] for key in keys}
	with open(new_data_file, "w") as _file:
		json.dump(new_data, _file)



if __name__ == '__main__':
	keys = ['completions', 'passingYards', 'touchdowns', 'playerNameSlug', 
		'teamId', 'interceptions',  'playerName', 'season', 'position',
		'type', 'week', 'gameId', 'esbId', 'firstName', 'lastName', 
		'attempts', 'team'
	]

	clean_path = "Cleaned_Pass_Charts"

	if not os.path.exists(clean_path): os.makedirs(clean_path)

	pass_chart_folders = [folder[0] for folder in os.walk("Pass_Charts")]
	image_folders = [folder for folder in pass_chart_folders if folder.split(os.sep)[-1] == "images"]
	print("Cleaning images and data...")
	for folder in image_folders:
		#print folder 
		images = os.listdir(folder)
		for image in images:
			if not image.startswith("."): 
				new_image(os.path.join(folder, image))
				new_data(folder, image)
	print("Done.")



