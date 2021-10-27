# -*- coding: utf-8 -*-
import os
import sys
import re
import json
import argparse
from tqdm import tqdm
from typeguard import typechecked
from typing import Dict

DEFAULT_TEMPLATE_FILE: str = "cv.template.tex"
DEFAULT_TRANSLATION_DIR: str = "l10n"

translation_filename_pattern: re.Pattern = re.compile(r"^[a-z]{2}\.json$", re.IGNORECASE)


@typechecked
def main(template_file: str, translation_dir: str) -> None:
	template = ''
	with open(template_file, mode='r', encoding='utf-8') as f:
		template = f.read()

	if not isinstance(template, str):
		raise ValueError(f"The given template file {template_file} doesn't contain any data.")

	# Save translation files in a dictionary mapping the two-letter languages to their respective file content
	translation_files: Dict[str, str] = {}

	# List files in translation directory
	for filename in os.listdir(translation_dir):
		match: re.Match = translation_filename_pattern.match(filename)
		# If the filename contains two letter in its base name, and is a JSON file, read it
		if match is not None:
			# Extract the base name
			base_filename = filename.split('.')[0]
			if len(base_filename) == 2:
				# Read the file
				with open(os.path.join(translation_dir, filename), mode='r', encoding='utf-8') as f:
					translation_files[base_filename] = f.read()

	# Check translations
	if len(translation_files) == 0:
		print("No translation files found.")
		sys.exit(0)

	# Parse the translation files to JSON and generate the CVs
	progress: tqdm = tqdm(desc="Generating CVs", total=len(translation_files))
	for lang, json_file_content in translation_files.items():
		tex_filename = f"cv.{lang}.tex"
		progress.set_description(f"Generating {tex_filename}")
		json_content: Dict[str, str] = json.loads(json_file_content)
		tex_file: str = fill_placeholders(template, json_content)
		with open(tex_filename, "w", encoding='utf-8') as f:
			f.write(tex_file)

		progress.update()


@typechecked
def fill_placeholders(template: str, translation_map: Dict[str, str]) -> str:
	for key, string in translation_map.items():
		key_pattern: re.Pattern = re.compile(r"\${{\s*" + key + r"\s*}}\$")
		template, num_subs = key_pattern.subn(sanitize_for_latex(string), template)
		#print(f"Replaced /{key_pattern.pattern}/g {num_subs} times")

	return template


@typechecked
def sanitize_for_latex(string: str) -> str:
	"""
	Sanitize the given string for LaTeX file.
	"""
	return string\
           .replace("\n", "\\\\\\\\")\
           .replace("\\n", "\\\\\\\\")\
           .replace("á", "\\'{a}")\
           .replace("é", "\\'{e}")\
           .replace("í", "\\'{i}")\
           .replace("ó", "\\'{o}")\
           .replace("ú", "\\'{u}")\
           .replace("ý", "\\'{y}")\
           .replace("à", "\\`{a}")\
           .replace("è", "\\`{e}")\
           .replace("ì", "\\`{i}")\
           .replace("ò", "\\`{o}")\
           .replace("ù", "\\`{u}")\
           .replace("â", "\\^{a}")\
           .replace("ê", "\\^{e}")\
           .replace("î", "\\^{i}")\
           .replace("ô", "\\^{o}")\
           .replace("û", "\\^{u}")\
           .replace("Á", "\\'{A}")\
           .replace("É", "\\'{E}")\
           .replace("Í", "\\'{I}")\
           .replace("Ó", "\\'{O}")\
           .replace("Ú", "\\'{U}")\
           .replace("Ý", "\\'{Y}")\
           .replace("À", "\\`{A}")\
           .replace("È", "\\`{E}")\
           .replace("Ì", "\\`{I}")\
           .replace("Ò", "\\`{O}")\
           .replace("Ù", "\\`{U}")\
           .replace("Â", "\\^{A}")\
           .replace("Ê", "\\^{E}")\
           .replace("Î", "\\^{I}")\
           .replace("Ô", "\\^{O}")\
           .replace("Û", "\\^{U}")\
           .replace("&", "\\&")\
           .replace("#", "\\#")


if __name__ == "__main__":
	# Parse the arguments
	p = argparse.ArgumentParser(
		prog="CV Generator", description="Generate the LaTeX files from the template and the translation files.")
	p.add_argument(
		"-t",
		"--template",
		default=DEFAULT_TEMPLATE_FILE,
		help=f"The LaTeX template file used to generate the translated LaTeX files. The file must contains the placeholders in order to work. Default is {DEFAULT_TEMPLATE_FILE}."
	)
	p.add_argument(
		"-d",
		"--translation-dir",
		default=DEFAULT_TRANSLATION_DIR,
		help=f"The directory containing all translation files. This directory must contain JSON files where the base file name is the two-letter languages. Default is {DEFAULT_TRANSLATION_DIR}."
	)
	args = p.parse_args()

	main(template_file=args.template, translation_dir=args.translation_dir)
