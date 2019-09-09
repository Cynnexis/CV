# -*- coding: utf-8 -*-
import os
import re
import argparse
import subprocess
from typing import Optional

IMAGES_FOLDER_NAME = "images"

# Parse the arguments
p = argparse.ArgumentParser(prog="Change Color", description="Change the colors of the images and CVs.")
p.add_argument("-a", "--accent-color", default=None, help="The accent color. Default is cyan (#45818E).")
args = p.parse_args()

# Get the images
images_filename = []
images_path = []
current_folder_entries = os.listdir('.')
if IMAGES_FOLDER_NAME in current_folder_entries and os.path.isdir(IMAGES_FOLDER_NAME):
	images_folder_entries = os.listdir(IMAGES_FOLDER_NAME)
	for images_entry in images_folder_entries:
		if images_entry.endswith(".svg"):
			images_filename.append(images_entry)
			images_path.append(os.path.abspath(os.path.join(IMAGES_FOLDER_NAME, images_entry)))

for image_filename in images_path:
	print(image_filename)

# Convert accent color
if args.accent_color is not None:
	# Get the old accent color
	old_accent_color = "45818E"
	with open("resume.cls", 'r') as f:
		resume_cls = f.read()
	color_matches = re.findall(r"\\definecolor{primary-color}{HTML}{#?([0-9a-fA-F]{6})}", resume_cls, re.MULTILINE)
	if len(color_matches) > 0:
		old_accent_color = color_matches[0]
	print("old accent color = " + old_accent_color)
	
	# Replace occurrences in images (svg)
	for image_path in images_path:
		with open(image_path, 'r+') as f:
			image_content = f.read()
			image_content = re.sub('#' + old_accent_color, '#' + args.accent_color, image_content)
			f.write(image_content)
