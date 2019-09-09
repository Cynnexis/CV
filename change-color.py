# -*- coding: utf-8 -*-
import os
import re
import argparse
import subprocess
from typing import Optional

INKSCAPE_PATH = "D:\\Apps\\Inkscape\\inkscape.exe"
OUTPUT_IMAGES_SIZE = 512
IMAGES_FOLDER_NAME = "images"

# Parse the arguments
p = argparse.ArgumentParser(prog="Change Color", description="Change the colors of the images and CVs.")
p.add_argument("-p", "--primary-color", default=None, help="The accent color. Default is cyan (#45818E).")
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

# Convert accent color
if args.primary_color is not None:
	if args.primary_color.startswith("0x"):
		args.primary_color = args.primary_color.replace("0x", '#')
	elif not args.primary_color.startswith('#'):
		args.primary_color = '#' + args.primary_color
	
	# Get the old accent color
	old_accent_color = "45818E"
	with open("resume.cls", "r+") as f:
		resume_cls = f.read()
		color_matches = re.findall(r"\\definecolor{primary-color}{HTML}{#?([0-9a-fA-F]{6})}", resume_cls, re.MULTILINE)
		if len(color_matches) > 0:
			old_accent_color = color_matches[0]
		# Replace occurrence in resume.cls
		new_resume_cls, nb_chgmt = re.subn(r"\\definecolor{primary-color}{HTML}{" + old_accent_color + r'}', r"\\definecolor{primary-color}{HTML}{" + re.sub("(#|0x)", '', args.primary_color) + "}", resume_cls, re.IGNORECASE)
		if nb_chgmt > 0:
			f.seek(0)
			f.write(new_resume_cls)
			f.truncate()
	
	# Replace occurrences in images (svg)
	print("Coloring images...")
	for image_path in images_path:
		with open(image_path, 'r+') as f:
			image_content = f.read()
			new_image_content, nb_chgmt = re.subn('#' + old_accent_color, args.primary_color, image_content, flags=re.IGNORECASE)
			if nb_chgmt > 0:
				f.seek(0)
				f.write(new_image_content)
				f.truncate()
				# Call Inkscape
				subprocess.call([INKSCAPE_PATH, "-z", image_path, "-e", image_path.replace(".svg", ".png"), "-C", "-w", str(OUTPUT_IMAGES_SIZE), "-h", str(OUTPUT_IMAGES_SIZE)])

	print("Done!")
