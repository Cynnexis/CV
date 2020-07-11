#!/bin/bash

command=""
if [[ $# == 0 ]]; then
	echo "No arguments passed. Assuming \"make\""
	command="make"
else
	command=$1
fi

if [[ "$command" == "make" ]]; then
	if [[ $# -le 1 ]]; then
		echo "make> No file given. Listing all CV TeX files in current directory."
		filename=$(ls cv.*.tex)
		echo "Listing TeX:" $filename
	else
		filename=${@:2}
		echo "make> Given filename $filename"
	fi
fi

exit_code=0

# Parse command
if [[ $command == "make" ]]; then
	LATEX="lualatex -shell-escape -interaction=batchmode -halt-on-error -file-line-error -output-directory ."
	for f in $filename; do
		echo "Compiling $f..."
		$LATEX $f | tee -a build.log pdflatex1.log
		$LATEX $f | tee -a build.log pdflatex2.log
		# Get the exit code of the command before the pipe operation ($LATEX)
		exit_code="${PIPESTATUS[0]}"
	done
	echo "The log of the build can be found at $(pwd)/build.log"
else
	echo -e "Couldn't interpret command '$command'.\nAll arguments: $*"
	exit_code=1
fi

echo $exit_code
exit $exit_code
