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
p.add_argument("-t", "--primary-text-color", default=None, help="The text color with the primary color as a background. Default is white (#FFFFFF).")
p.add_argument("--h1-color", default=None, help="The header 1 color. Default is cyan (#45818E).")
p.add_argument("--h2-color", default=None, help="The header 2 color. Used for bullet. Default is cyan (#294d55).")
p.add_argument("--h3-color", default=None, help="The header 2 color. Used for bullet and date. Default is grey (#938690).")
p.add_argument("--link-color", default=None, help="The link color. Default is blue (#185BC1).")
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
			color_matches = re.findall(r"\\definecolor\{" + color_name + r"\}\{HTML\}\{#?([0-9a-fA-F]{6})\}", resume_cls, re.MULTILINE)
			if len(color_matches) > 0:
				old_color = color_matches[0]
			# Replace occurrence in resume.cls
			new_resume_cls, nb_chgmt = re.subn(r"\\definecolor\{" + color_name + r"\}\{HTML\}\{" + old_color + r'\}', r"\\definecolor{" + color_name + "}{HTML}{" + re.sub("(#|0x)", '', new_color) + "}", resume_cls, re.IGNORECASE)
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
					new_image_content, nb_chgmt = re.subn('#' + old_color, new_color, image_content, flags=re.IGNORECASE)
					if nb_chgmt > 0:
						f.seek(0)
						f.write(new_image_content)
						f.truncate()
						# Call Inkscape
						subprocess.call([INKSCAPE_PATH, "-z", image_path, "-e", image_path.replace(".svg", ".png"), "-C", "-w", str(OUTPUT_IMAGES_SIZE), "-h", str(OUTPUT_IMAGES_SIZE)])
			
			print("Done!")


change_color(args.primary_color, "45818E", "primary-color", True)
change_color(args.primary_text_color, "FFFFFF", "primary-text-color", False)
change_color(args.h1_color, "45818E", "h1-color", False)
change_color(args.h2_color, "294d55", "h2-color", False)
change_color(args.h3_color, "938690", "h3-color", False)
change_color(args.link_color, "185BC1", "link-color", False)
