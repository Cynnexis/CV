# -*- coding: utf-8 -*-
import argparse
import copy
import json
import os
import re
import sys
from typing import Dict, List, Optional, Union

from tqdm import tqdm
from typeguard import typechecked

DEFAULT_TEMPLATE_FILE: str = "cv.template.tex"
DEFAULT_TRANSLATION_DIR: str = "l10n"

translation_filename_pattern: re.Pattern = re.compile(r"^[a-z]{2}\.json$", re.IGNORECASE)
placeholder_pattern: re.Pattern = re.compile(r"\${{\s*([a-z0-9_.]+)\s*}}\$", re.IGNORECASE)
control_for_pattern: re.Pattern = re.compile(r"\${{\s*@for\s+([a-z0-9_]+)\s+in\s+([a-z0-9_.]+)\s*}}\$", re.IGNORECASE)
control_join_pattern: re.Pattern = re.compile(r"\${{\s*@join\s*}}\$", re.IGNORECASE)
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
	# noinspection PyUnusedLocal
	template: str = ''
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
	template = parse_for_loop(template, translation_map)
	# Search for for-loop flow control, beginning with the first one
	for_loops: List[ForLoop] = search_for_loops(template)
	for_loop: Optional[ForLoop] = for_loops[0] if len(for_loops) > 0 else None
	while for_loop is not None:
		template = parse_for_loop(template, translation_map)

		# Search for the next match
		for_loops: List[ForLoop] = search_for_loops(template)
		for_loop = for_loops[0] if len(for_loops) > 0 else None

	# Search for placeholder variables
	template = fill_placeholders(template, translation_map)

	return template


def parse_for_loop(template: str, translation_map: Dict[str, str]) -> str:
	"""
	Parse the for-loop in the given template, using the given translation dictionary, that maps placeholder names to
	their respective values.
	:param template: The template containing placeholders and the for-loop. Only the first for-loop will be parsed. If
	the first for-loop contains a nested for-loop, it will be treated as well using recursive calls.
	:param translation_map: The mapping between the placeholder names and their values.
	:return: Return the template but with its first for-loop (and nested loops) parsed. Note that if you want the
	placeholders to be replaced, please call `fill_placeholders` after.
	"""
	# Search for for-loop flow control, beginning with the first one
	for_loop: Optional[ForLoop] = search_for_loops(template)[0]
	if for_loop is None:
		# If none, it means that there is no for-loop in `template`
		return template

	# Get the starting statement
	for_loop_var = for_loop.starting_statement
	element_name = for_loop_var.group(1)
	placeholder_name = for_loop_var.group(2)
	if element_name == placeholder_name:
		raise ValueError(f"Error in for-loop: The name of the item cannot be the same as the iterator.")

	if placeholder_name not in translation_map:
		raise ValueError(f"The placeholder variable ${{{{ {placeholder_name} }}}}$ is unbound.")

	if type(translation_map[placeholder_name]) != list:
		raise ValueError(f"The placeholder variable ${{{{ {placeholder_name} }}}}$ is not a list, it is not iterable.")

	# Get the ending statement
	endfor_var: re.Match = for_loop.ending_statement

	# Extract the body of the loop
	loop_body: str = template[for_loop.body_slice]

	# The body will be replaced by the following variable, that will contain the final result of the body
	filled_body: str = ''

	element: dict
	for element in translation_map[placeholder_name]:
		if type(element) != dict and type(element) != str:
			raise ValueError(
				f"The placeholder variable ${{{{ {placeholder_name} }}}}$ does not contain JSON object or a string, it cannot be parsed."
			)

		# Construct list of possible fields for the element, and associate them to their respective value
		fields_map: Dict[str, str] = {}
		if type(element) == dict:
			for key, value in element.items():
				fields_map[f"{element_name}.{key}"] = value
		else: # if element is a string
			# noinspection PyTypeChecker
			fields_map[element_name] = element

		# Define the scope of the loop body: It contains both the outer scope, plus the placeholder of the list being
		# parsed
		loop_body_scope: Dict[str, str] = {**fields_map, **translation_map}

		# Join with a special command
		if len(filled_body) != 0 and for_loop.join is not None:
			filled_body += for_loop.join

		# Search for nested for-loops in `loop_body`
		nested_for_loops: List[ForLoop] = search_for_loops(loop_body)
		if len(nested_for_loops) > 0:
			current_loop_body = parse_for_loop(loop_body, loop_body_scope)
		else:
			current_loop_body = copy.deepcopy(loop_body)

		filled_body += fill_placeholders(current_loop_body, loop_body_scope)

	template = str_replace(template, filled_body, for_loop_var.start(), endfor_var.end())

	return template


def fill_placeholders(template: str, translation_map: Dict[str, str]) -> str:
	"""
	Fill all detected placeholders in the given template, using the given translation dictionary, that maps placeholder
	names to their respective values.

	Note that this function only translates the placeholders, and not the flow controls.
	:param template: The template containing placeholders.
	:param translation_map: The mapping between the placeholder names and their values.
	:return: Return the template but with all its placeholders replaced by the corresponding values.
	"""
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
def search_for_loops(string: str) -> List['ForLoop']:
	"""
	Search for all for-loops (nested or not) in the given string.
	:param string: The string to parse.
	:return: Return a list of `ForLoop`.
	"""
	# Search for all for-loop statements
	for_loops: List[re.Match] = list(control_for_pattern.finditer(string))
	# Search for all ending statements
	end_loops: List[re.Match] = list(control_endfor_pattern.finditer(string))
	# Declare the list that will be returned
	for_loop_statements: List[ForLoop] = []
	# Also declare a list of all ending statements that have been associated to a starting statements
	associated_ending_statements: List[re.Match] = []

	# For all starting statement, search the corresponding ending statement by finding the nearest (left-to-right) in
	# the string
	for_loop_var: re.Match
	end_loop_var: re.Match
	# Parse the starting statement, from the end to the beginning to allow nested loops
	for for_loop_var in reversed(for_loops):
		lowest_ending_statement: Optional[re.Match] = None
		lowest_distance: Union[int, float] = float('+inf')
		# Parse the ending statement, from the beginning to the end
		for end_loop_var in end_loops:
			# Ignore ending statement that are already associated and that are BEFORE the starting one
			if end_loop_var not in associated_ending_statements and for_loop_var.end() < end_loop_var.start():
				distance = end_loop_var.end() - for_loop_var.start()
				if distance < lowest_distance:
					# If a lower distance is found, select it
					lowest_distance = distance
					lowest_ending_statement = end_loop_var

		if lowest_ending_statement is None:
			raise ValueError(f"Couldn't find an ending statement for the following line:\n{for_loop_var.group(0)}")

		# Now, we have an association between for_loop_var (starting statement) and lowest_ending_statement (ending statement)
		# Get the body of the for-loop
		body_ending_index: int = lowest_ending_statement.start()
		loop_body: str = string[for_loop_var.end():body_ending_index]

		# Search for a join statement in the for-loop body
		join: Optional[str] = None
		join_loop_var: Optional[re.Match] = None
		join_loops: List[re.Match] = list(control_join_pattern.finditer(loop_body))
		if len(join_loops) > 0:
			# A join statement has been found!
			if len(join_loops) != 1:
				raise ValueError(f"Expected 0 or 1 @join statement in for loop, got {len(join_loops)}:\n"
									f"{string[for_loop_var.start():lowest_ending_statement.end()]}")

			join_loop_var = join_loops[0]
			# Extract the body between the loop statement and the ending
			join = string[for_loop_var.end() + join_loop_var.end():lowest_ending_statement.start()]
			# Update the index where the body stops: it is now just before the join statement instead of the ending statement
			body_ending_index = for_loop_var.end() + join_loop_var.start()

		for_loop_statements.append(
			ForLoop(
				starting_statement=for_loop_var,
				body_starting_index=for_loop_var.end(),
				ending_statement=lowest_ending_statement,
				body_ending_index=body_ending_index,
				join_statement=join_loop_var,
				join=join,
			))
		# Register the associated
		associated_ending_statements.append(lowest_ending_statement)

	# Reverse again the list to have the for-loops in the right order (from left to right)
	return list(reversed(for_loop_statements))


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


class ForLoop:
	"""
	Class that represents a for-loop flow structure.
	"""

	@typechecked
	def __init__(self,
					starting_statement: re.Match,
					body_starting_index: int,
					ending_statement: re.Match,
					body_ending_index: int,
					join_statement: Optional[re.Match] = None,
					join: Optional[str] = None):
		self.starting_statement = starting_statement
		self.body_starting_index = body_starting_index
		self.ending_statement = ending_statement
		self.body_ending_index = body_ending_index
		self.join_statement = join_statement
		self.join = join
		assert self.body_starting_index < self.body_ending_index

	@property
	def body_slice(self) -> slice:
		return slice(self.body_starting_index, self.body_ending_index)

	def __len__(self) -> int:
		return self.body_ending_index - self.body_starting_index

	def __str__(self) -> str:
		content: str = f"{self.starting_statement.group(0)}\n\t...\n"
		if self.join_statement is not None:
			content += f"{self.join_statement.group(0)}\n\t...\n"

		content += f"{self.ending_statement.group(0)}"
		return content

	def __repr__(self) -> str:
		return f"ForLoop{{body_starting_index: {self.body_starting_index}, ending_statement: {self.ending_statement}, join: {self.join}}}"


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
