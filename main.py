"""
Author: Sarah Mallepalle (updated by Ethan Douglas to work in Python 3)

Main file to extract all pass locations from all images in the folder 
'Cleaned_Pass_Charts', and write player, game, and pass information to 
the file 'pass_locations.csv'
"""

import os
from undistort_field import *
from pass_detection import *
import json
import scipy.misc
import pandas as pd

def get_pass_data(data_file): 
	"""
	Extract the number of complete passes, incomplete passes, touchdowns, and interceptions 
	from a pass chart. 
	"""
	with open(data_file) as _file: 
		data = json.load(_file)
		_file.close()
	n_completions = data["completions"] - data["touchdowns"]
	n_touchdowns = data["touchdowns"]
	n_interceptions = data["interceptions"]
	n_incompletes = data["attempts"] -  n_completions -  n_interceptions - n_touchdowns

	return (n_completions, n_touchdowns, n_interceptions, n_incompletes)

def get_image(folder, data_file):
	"""
	If cleaned image exists, return the file path to the image, 
	otherwise return none.
	"""
	images_path = os.sep.join(folder.split(os.sep)[:-1]) + os.sep + "images" 
	image_file = images_path + os.sep + data_file.split(".")[0] + ".jpeg"
	if not os.path.exists(image_file):
		return None
	else:
		return image_file

def get_game_data(data_file):
	"""
	Extract player name, team, and game ID from the data corresponding to a pass chart image.
	"""	
	with open(data_file) as _file: 
		data = json.load(_file)
		_file.close()
	name = data["firstName"] + " " + data["lastName"]
	team = data["team"]
	game_id = data["gameId"]
	week = data_file.split(os.sep)[-3]
	return (name, team, game_id, week)

def write_pass_locations(image, data, passes):
	"""
	Write player, team, and game information, and locations of all passes to a .csv file.
	"""
	(n_com, n_td, n_int, n_inc) = get_pass_data(data)
	(name, team, game_id, week) = get_game_data(data)
	n_total = n_com + n_td + n_int + n_inc

	pass_cols = ["pass_type", "x", "y"]
	game_cols = ["game_id", "team", "week", "name"]
	pass_df = pd.DataFrame(columns = pass_cols)

	if (image is None): 
		rows_com = pd.DataFrame([["COMPLETE", None, None]]*n_com, 
			columns = pass_cols)
		rows_td = pd.DataFrame([["TOUCHDOWN", None, None]]*n_td, 
			columns = pass_cols)
		rows_int = pd.DataFrame([["INTERCEPTION", None, None]]*n_int, 
			columns = pass_cols)
		rows_inc = pd.DataFrame([["INCOMPLETE", None, None]]*n_inc, 
			columns = pass_cols)
		pass_df = pass_df.append([rows_com, rows_td, rows_int, rows_inc])
		game_df = pd.DataFrame([[game_id, team, week, name]]*pass_df.shape[0], 
			columns = game_cols)
		df = pd.concat([game_df, pass_df.reset_index(drop=True)], axis=1)
		passes = passes.append(df)
		return passes

	if n_com != 0: 
		rows_com = completions(image, n_com)
		pass_df = pass_df.append(rows_com)

	if n_td != 0: 
		rows_td = touchdowns(image, n_td)
		pass_df = pass_df.append(rows_td)

	if n_int != 0: 
		rows_int = interceptions(image, n_int)
		pass_df = pass_df.append(rows_int)

	if n_inc != 0: 
		rows_inc = incompletions(image, n_inc)
		pass_df = pass_df.append(rows_inc)

	game_df = pd.DataFrame([[game_id, team, week, name]]*pass_df.shape[0], 
		columns = game_cols)

	df = pd.concat([game_df, pass_df.reset_index(drop=True)], axis=1)
	passes = passes.append(df)
	return passes


if __name__ == '__main__':

	clean_path = "Cleaned_Pass_Charts"
	passes = pd.DataFrame(columns = ["game_id", "team", "week", "name", "pass_type", "x", "y"])

	pass_chart_folders = [folder[0] for folder in os.walk(clean_path)]
	data_folders = [folder for folder in pass_chart_folders if folder.split(os.sep)[-1] == "data"]

	print("Extracting pass locations...")
	for folder in data_folders:
		data = os.listdir(folder)
		print(folder)
		for data_file in data:
			if not data_file.startswith("."): 
				image = get_image(folder, data_file)
				passes = write_pass_locations(image, os.path.join(folder, data_file), passes)
	passes.to_csv("pass_locations.csv", index=False, header=True)
	print("Done.")
