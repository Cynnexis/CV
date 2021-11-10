# -*- coding: utf-8 -*-
import os
import sys
import re
import json
import argparse
from tqdm import tqdm
from typeguard import typechecked
from typing import Dict, List, Iterator, Optional

DEFAULT_TEMPLATE_FILE: str = "cv.template.tex"
DEFAULT_TRANSLATION_DIR: str = "l10n"

translation_filename_pattern: re.Pattern = re.compile(r"^[a-z]{2}\.json$", re.IGNORECASE)
placeholder_pattern: re.Pattern = re.compile(r"\${{\s*([a-z0-9_.]+)\s*}}\$", re.IGNORECASE)
control_for_pattern: re.Pattern = re.compile(r"\${{\s*@for\s+([a-z0-9_]+)\s+in\s+([a-z0-9_.]+)\s*}}\$", re.IGNORECASE)
control_endfor_pattern: re.Pattern = re.compile(r"\${{\s*@endfor\s*}}\$", re.IGNORECASE)
new_line_pattern: re.Pattern = re.compile(r"\r?\n")
instruction_placeholder_possible_chars: List[str] = [
	*[chr(c) for c in range(ord('a'),
							ord('z') + 1)],
	*[chr(c) for c in range(ord('A'),
							ord('Z') + 1)],
	*[chr(c) for c in range(ord('0'),
							ord('9') + 1)],
	'_',
]


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
		tex_file: str = parse_template(template, json_content)
		with open(tex_filename, "w", encoding='utf-8') as f:
			f.write(tex_file)

		progress.update()


def parse_template(template: str, translation_map: Dict[str, str]) -> str:
	# Search for for-loop flow control, beginning with the first one
	for_loop_var: Optional[re.Match] = control_for_pattern.search(template)
	while for_loop_var is not None:
		element_name = for_loop_var.group(1)
		placeholder_name = for_loop_var.group(2)
		if element_name == placeholder_name:
			raise ValueError(f"Error in for-loop: The name of the item cannot be the same as the iterator.")

		if placeholder_name not in translation_map:
			raise ValueError(f"The placeholder variable ${{{{ {placeholder_name} }}}}$ is unbound.")

		if type(translation_map[placeholder_name]) != list:
			raise ValueError(
				f"The placeholder variable ${{{{ {placeholder_name} }}}}$ is not a list, it is not iterable.")

		# TODO: The method used for detected the end of a for-loop doesn't allow nested for-loops
		# Get the for-loop end
		endfor_var: Optional[re.Match] = control_endfor_pattern.search(template[for_loop_var.end():])
		if endfor_var is None:
			raise ValueError(f"The flow control {for_loop_var.group(0)} has no ending.")

		# Extract the body of the loop
		loop_body: str = template[for_loop_var.end():for_loop_var.end() + endfor_var.start()]

		# The body will be replaced by the following variable, that will contain the final result of the body
		filled_body: str = ''

		element: dict
		for element in translation_map[placeholder_name]:
			if type(element) != dict:
				raise ValueError(
					f"The placeholder variable ${{{{ {placeholder_name} }}}}$ does not contain JSON object, it cannot be parsed."
				)

			# Construct list of possible fields for the element, and associate them to their respective value
			fields_map: Dict[str, str] = {}
			for key, value in element.items():
				fields_map[f"{element_name}.{key}"] = value

			# TODO: Make the join customizable by the template
			# Join with a special command
			if len(filled_body) != 0:
				filled_body += f"{get_indent(loop_body)[0]}\\jump\n"

			filled_body += fill_placeholders(loop_body, fields_map)

		template = str_replace(template, filled_body, for_loop_var.start(), for_loop_var.end() + endfor_var.end())
		# Search for the next match
		for_loop_var = control_for_pattern.search(template)

	# Search for placeholder variables
	template = fill_placeholders(template, translation_map)

	return template


def fill_placeholders(template: str, translation_map: Dict[str, str]) -> str:
	# Search for the first match in the given template
	placeholder_var: Optional[re.Match] = placeholder_pattern.search(template)
	while placeholder_var is not None:
		if placeholder_var.group(1) not in translation_map:
			raise ValueError(f"The placeholder variable ${{{{ {placeholder_var.group(1)} }}}}$ is unbound.")

		template = str_replace(template, sanitize_for_latex(translation_map[placeholder_var.group(1)]),
								placeholder_var.start(), placeholder_var.end())
		# Search for the next match
		placeholder_var = placeholder_pattern.search(template)

	return template


def str_replace(string: str, substring: str, start: int, end: int) -> str:
	"""
	Replace a part of the given string by the gven substring. The part to replace is determined by the start and end
	arguments.

	Example:

	>>> str_replace("This is a question", "The following", 0, 4)
	"The following is a question"

	:param string: The string that must be modified.
	:param substring: The substring to add in string.
	:param start: The starting index of the replacing area.
	:param end: The ending index of the replacing area.
	:return: Return the replaced string (containing substring at the given place).
	"""
	assert 0 <= start <= end < len(string)
	return string[:start] + substring + string[end:]


@typechecked
def get_indent(string: str) -> str:
	"""
	Return the first indent string found in the given string.
	:param string: The string to parse.
	:return: Return a substring of the given string that contains the first indent. If the string is the empty or has no
	indented lines, return an empty string.
	"""
	for line in new_line_pattern.split(string):
		indent: str = ''
		for char in line:
			# Construct the indent string
			if char in [' ', '\t']:
				indent += char
			else:
				if len(indent) == 0:
					# If indent is empty, it means that the line has no indent. Skip to the next one
					continue
				else:
					# If the indent is not empty, return it
					return indent

	# If nothing found, it means that the string is not indented. Return an empty string.
	return ''


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
