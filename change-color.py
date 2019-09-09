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
images_path = []
current_folder_entries = os.listdir('.')
if IMAGES_FOLDER_NAME in current_folder_entries and os.path.isdir(IMAGES_FOLDER_NAME):
	images_folder_entries = os.listdir(IMAGES_FOLDER_NAME)
	for images_entry in images_folder_entries:
		if images_entry.endswith(".svg"):
			images_path.append(os.path.abspath(os.path.join(IMAGES_FOLDER_NAME, images_entry)))


def change_color(new_color: str, default_old_color: str, color_name: str, update_image: bool):
	if new_color is not None:
		if new_color.startswith("0x"):
			new_color = new_color.replace("0x", '#')
		elif not new_color.startswith('#'):
			new_color = '#' + new_color
		
		# Get the old color
		old_color = default_old_color
		with open("resume.cls", "r+") as f:
			resume_cls = f.read()
			color_matches = re.findall(r"\\definecolor{" + color_name + r"-color}{HTML}{#?([0-9a-fA-F]{6})}", resume_cls, re.MULTILINE)
			if len(color_matches) > 0:
				old_color = color_matches[0]
			# Replace occurrence in resume.cls
			new_resume_cls, nb_chgmt = re.subn(r"\\definecolor{" + color_name + r"}{HTML}{" + old_color + r'}', r"\\definecolor{" + color_name + "}{HTML}{" + re.sub("(#|0x)", '', new_color) + "}", resume_cls, re.IGNORECASE)
			if nb_chgmt > 0:
				f.seek(0)
				f.write(new_resume_cls)
				f.truncate()
		
		# Replace occurrences in images (svg)
		if update_image:
			print("Coloring images...")
			for image_path in images_path:
				with open(image_path, 'r+') as f:
					image_content = f.read()
					new_image_content, nb_chgmt = re.subn('#' + old_color, args.primary_color, image_content, flags=re.IGNORECASE)
					if nb_chgmt > 0:
						f.seek(0)
						f.write(new_image_content)
						f.truncate()
						# Call Inkscape
						subprocess.call([INKSCAPE_PATH, "-z", image_path, "-e", image_path.replace(".svg", ".png"), "-C", "-w", str(OUTPUT_IMAGES_SIZE), "-h", str(OUTPUT_IMAGES_SIZE)])
			
			print("Done!")


change_color(args.primary_color, "45818E", "primary-color", True)
