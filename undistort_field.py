"""
Author: Sarah Mallepalle (updated to work in Python 3 by Ethan Douglas)

For a single pass chart image in 'Pass_Charts', extract only the trapezoidal image of the field, 
undistort the field by turning the trapezoid into a rectangle, remove the sideline labels, 
and save the new image to the folder 'Cleaned_Pass_Charts'.
"""

import cv2
import os
from skimage import data, color, img_as_ubyte, io
from skimage import feature
from skimage.feature import canny
from skimage.transform import hough_ellipse
from skimage.draw import ellipse_perimeter
import math
from PIL import Image
from PIL import ImageDraw
import numpy as np



def get_top(image):
	"""
	Function to get the pixel location of the top of the trapezoidal field.
	
	Input:
		image: image from the folder 'Pass_Charts'
	Return:
		top_left: location of the top left of the trapezoidal field
	"""
	frame = cv2.imread(image, 0)
	ret, img = cv2.threshold(frame, 40, 255, cv2.THRESH_BINARY_INV)

	points = np.fliplr(np.argwhere(img==0))

	mid = 600
	top = None
	top_left = None
	top_right = None

	for p in points:
		if (p[0] == mid):
			if (top == None): 
				top = p[1]
				break

	for p in points:
		if (p[1] == top):
			if (top_left == None):
				top_left = p[0]
				break

	return top_left

def make_grey_border(image):
	"""
	Function to add a grey border to the left and right of the trapezoidal field, 
	in order to undistort the trapezoid.
	
	Input:
		image: image from the folder 'Pass_Charts'
	Return:
		top_left: location of the top left of the trapezoidal field
		bordersize: width of the border in pixels added to the image
		border: numpy.ndarray representation of input image with border
		
	"""
	top_left = get_top(image)
	im = cv2.imread(image)
	row, col = im.shape[:2]
	
	grey_color = [108,96,86]

	start = 0
	for i in range(row):
		if (im[i,0,2] > 70): 
			start = i 
			break

	bordersize = int(math.ceil(float(top_left*row)/float(start)) - top_left)

	border = cv2.copyMakeBorder(im, top=0, bottom=0, 
		left=bordersize, right=bordersize, 
		borderType= cv2.BORDER_CONSTANT, value=grey_color)

	return top_left, bordersize, border

def undistort_field(image):
	"""
	Function to undistort the field by turning the trapezoid field image into a rectangle.
	
	Input:
		image: image from the folder 'Pass_Charts'
	Return:
		im_out: undistorted image of the field turned into a rectangle
	"""

	tl, bs, border_image = make_grey_border(image)

	image = cv2.imread(image)

	i_row, i_col = image.shape[:2]
	b_row, b_col = border_image.shape[:2]

	if b_col > 1398: return None
	pts_src = np.array([[0, i_row], [tl+bs, 0], [i_col-tl+bs, 0],[b_col, i_row]])
	pts_dst = np.array([[0, b_row],[0, 0],[b_col, 0],[b_col, b_row]])

	h, status = cv2.findHomography(pts_src, pts_dst)

	im_out = cv2.warpPerspective(border_image, h, (b_col, b_row)) 

	return im_out

def clean_field_70(image):
	"""
	Function that removes the sidelines of an undistorted pass chart field image,
	if the field image shows +70 yards from the line of scrimmage.
	
	Input:
		image: undistorted image, im_out
	Return:
		img: cleaned undistorted image, without sidelines
	"""
	img = Image.open(image)
	grey_color = (86,96,108)
	LOS1 = ((18,587), (86, 601))
	LOS2 = ((1308, 601), (1374,587))

	x0 = 33
	x1 = 0
	x2 = 1362
	x3 = max(img.size[0], 1394)

	l10 = ((x0, 520), (x1, 503))
	r10 = ((x2, 520), (x3, 505))

	l20 = ((x0, 440), (x1, 421))
	r20 = ((x2, 440), (x3, 423))

	l30 = ((x0, 360), (x1, 338))
	r30 = ((x2, 360), (x3, 340))

	l40 = ((x0, 279), (x1, 255))
	r40 = ((x2, 279), (x3, 257))

	l50 = ((x0, 200), (x1, 173))
	r50 = ((x2, 200), (x3, 175))

	l60 = ((x0, 118), (x1, 90))
	r60 = ((x2, 118), (x3, 92))

	l70 = ((x0, 38), (x1, 8))
	r70 = ((x2, 38), (x3, 10))

	sidelines = [LOS1, LOS2, l10, r10, l20, r20, l30, r30,
	            l40, r40, l50, r50, l60, r60, l70, r70
	]



	draw = ImageDraw.Draw(img)

	for number in sidelines: 
		draw.rectangle(number, fill=grey_color)

	return img

def clean_field_50(image):
	"""
	Function that removes the sidelines of an undistorted pass chart field image,
	if the field image shows +50 yards from the line of scrimmage.
	
	Input:
		image: undistorted image, im_out
	Return:
		img: cleaned undistorted image, without sidelines
	"""
	img = Image.open(image)
	grey_color = (86,96,108)
	LOS1 = ((20, 562), (84, 578))
	LOS2 = ((1340, 562), (1278, 578))

	x0 = 33
	x1 = 0
	x2 = 1331
	x3 = max(img.size[0], 1362)

	l10 = ((x0, 476), (x1, 455))
	r10 = ((x2, 476), (x3, 457))

	l20 = ((x0, 373), (x1, 349))
	r20 = ((x2, 373), (x3, 351))

	l30 = ((x0, 269), (x1, 243))
	r30 = ((x2, 269), (x3, 245))

	l40 = ((x0, 165), (x1, 137))
	r40 = ((x2, 165), (x3, 139))

	l50 = ((x0, 60), (x1, 30))
	r50 = ((x2, 60), (x3, 32))

	sidelines = [LOS1, LOS2, l10, r10, l20, r20, 
				l30, r30, l40, r40, l50, r50
	]



	draw = ImageDraw.Draw(img)

	for number in sidelines: 
		draw.rectangle(number, fill=grey_color)

	return img

def clean_field(image):
	"""
	Wrapper function for clean_field_50 and clean_field_70. 
	"""
	u_img = undistort_field(image)
	if u_img is None: 
		return None
	row, col = u_img.shape[:2]

	cv2.imwrite(image, u_img)

	if col > 1370:
		return clean_field_70(image)

	else:
		return clean_field_50(image)



