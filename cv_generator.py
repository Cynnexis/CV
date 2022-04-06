#!/usr/bin/env python
import argparse
import json
import os
import re
import sys
from typing import Dict, Union, Any

from typeguard import typechecked
import jinja2 as j2

DEFAULT_TEMPLATE_FILE: str = "cv.template.tex"
DEFAULT_TRANSLATION_DIR: str = "l10n"

translation_filename_pattern: re.Pattern = re.compile(r"^[a-z]{2}(?:_[a-z]{2})?\.json$", re.IGNORECASE)


@typechecked
def main(template_file: str, translation_dir: str) -> None:
	# noinspection PyUnusedLocal
	template_content: str = ''
	with open(template_file, mode='r', encoding='utf-8') as f:
		template_content = f.read()

	template: j2.Template = j2.Template(
		template_content,
		variable_start_string="${{",
		variable_end_string="}}$",
		block_start_string="@{{",
		block_end_string="}}@",
		trim_blocks=True,
		lstrip_blocks=True,
	)

	if not isinstance(template_content, str):
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
	for lang, json_file_content in translation_files.items():
		tex_filename = f"cv.{lang}.tex"
		print(f"Generating {tex_filename}...")
		json_content: Dict[str, Any] = json.loads(json_file_content)
		# Sanitize the translations
		json_content = deep_sanitize(json_content)
		tex_file: str = template.render(**json_content)
		with open(tex_filename, "w", encoding='utf-8') as f:
			f.write(tex_file)


@typechecked
def deep_sanitize(data: Union[dict, list, str], ignore_none_json_dtype: bool = False) -> Union[dict, list, str]:
	if isinstance(data, str):
		data = sanitize_for_latex(data)
	elif isinstance(data, list):
		for i, datum in enumerate(data):
			data[i] = deep_sanitize(datum, ignore_none_json_dtype=ignore_none_json_dtype)
	elif isinstance(data, dict):
		for key in data.keys():
			data[key] = deep_sanitize(data[key], ignore_none_json_dtype=ignore_none_json_dtype)
	elif ignore_none_json_dtype and data is not None and not isinstance(data, int) and not isinstance(
		data, float) and not isinstance(data, bool):
		raise ValueError(f'Cannot decipher value {type(data)}: {data}.')

	return data


@typechecked
def sanitize_for_latex(string: str) -> str:
	"""
	Sanitize the given string for LaTeX file.
	"""
	replace_mapping: Dict[str, str] = {
		"\n": "\\\\",
		"\\n": "\\\\",
		"á": "\\'{a}",
		"é": "\\'{e}",
		"í": "\\'{i}",
		"ó": "\\'{o}",
		"ú": "\\'{u}",
		"ý": "\\'{y}",
		"à": "\\`{a}",
		"è": "\\`{e}",
		"ì": "\\`{i}",
		"ò": "\\`{o}",
		"ù": "\\`{u}",
		"â": "\\^{a}",
		"ê": "\\^{e}",
		"î": "\\^{i}",
		"ô": "\\^{o}",
		"û": "\\^{u}",
		"Á": "\\'{A}",
		"É": "\\'{E}",
		"Í": "\\'{I}",
		"Ó": "\\'{O}",
		"Ú": "\\'{U}",
		"Ý": "\\'{Y}",
		"À": "\\`{A}",
		"È": "\\`{E}",
		"Ì": "\\`{I}",
		"Ò": "\\`{O}",
		"Ù": "\\`{U}",
		"Â": "\\^{A}",
		"Ê": "\\^{E}",
		"Î": "\\^{I}",
		"Ô": "\\^{O}",
		"Û": "\\^{U}",
		"&": "\\&",
		"#": "\\#",
	}
	for key, value in replace_mapping.items():
		string = string.replace(key, value)

	return string


if __name__ == "__main__":
	# Parse the arguments
	p = argparse.ArgumentParser(
		prog="CV Generator",
		description="Generate the LaTeX files from the template and the translation files.",
	)
	p.add_argument(
		"-t",
		"--template",
		default=DEFAULT_TEMPLATE_FILE,
		help=f"The LaTeX template file used to generate the translated LaTeX files. The file must contains the placeholders in order to work. Default is {DEFAULT_TEMPLATE_FILE}.",
	)
	p.add_argument(
		"-d",
		"--translation-dir",
		default=DEFAULT_TRANSLATION_DIR,
		help=f"The directory containing all translation files. This directory must contain JSON files where the base file name is the two-letter languages. Default is {DEFAULT_TRANSLATION_DIR}.",
	)
	args = p.parse_args()

	main(template_file=args.template, translation_dir=args.translation_dir)
