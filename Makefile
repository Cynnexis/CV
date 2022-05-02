SHELL := /bin/bash
DOCKER_LATEX_IMAGE=cynnexis/latex:1.0.1
DOCKER_PYTHON_IMAGE=python:3.7.12-bullseye
DOCKER_INKSCAPE_IMAGE=cynnexis/inkscape
DOCKER_INKSCAPE := docker run --name="inkscape-generate-png" --rm -v "$$(pwd):/root/svg/" $(DOCKER_INKSCAPE_IMAGE) --export-overwrite
ALL_GENERATED_512_PNG := images/auto-stories.png images/computer.png images/cv.png images/default_profile.png images/email.png images/explore.png images/flag-ca.png images/flag-es.png images/flag-fr.png images/github.png images/language.png images/lightbulb.png images/linkedin.png images/location.png images/person.png images/phone.png images/poll.png images/profile.png images/running.png images/school.png images/skype.png images/work.png
ALL_GENERATED_16_PNG := images/cv16.png
ALL_GENERATED_32_PNG := images/cv32.png
ALL_GENERATED_48_PNG := images/cv48.png images/flag-ca48.png images/flag-fr48.png
ALL_GENERATED_PNG := $(ALL_GENERATED_512_PNG) $(ALL_GENERATED_32_PNG) $(ALL_GENERATED_16_PNG) $(ALL_GENERATED_48_PNG)
L10N_FILES := $(wildcard l10n/*.json)
TEX_DEPENDENCIES := resume.cls $(ALL_GENERATED_PNG)

.ONESHELL:

.PHONY: help
help:
	@echo "Makefile for generating the resume in different language."
	@echo ''
	@echo "USAGE: $(MAKE) [COMMAND]"
	@echo ''
	@echo "COMMANDS:"
	@echo ''
	@echo "  help      - Print this page."
	@echo "  all       - Generate the resumes in all available languages."
	@echo "  clean     - Remove all generate files from the project directory."
	@echo "  open      - Open all generated PDF files using 'xdg-open'."
	@echo "  pull      - Pull all necessary Docker images."
	@echo "  png       - Build all the images from the SVG files."
	@echo "  cv.%.pdf  - Generate the resume in the language specified by %, as a PDF."
	@echo "  cv.%.docx - Generate the resume in the language specified by %, as a DOCX file."
	@echo ''

.PHONY: all
all:
	@set -euo pipefail
	# Get the list of all available languages
	languages=()
	while IFS= read -rd $$'\0' l10n_file; do
		languages+=("$$(basename "$$l10n_file" .json)")
	done < <(find l10n/ -type f -iname '*.json' -print0)

	# Build the resumes
	for lang in "$${languages[@]}"; do
		$(MAKE) "cv.$$lang.pdf"
	done

.PHONY: clean
clean: clean-build clean-pdf clean-png

.PHONY: clean-build
clean-build:
	@set -euo pipefail
	rm -f *.aux *.auxlock *.bbl *.blg *.fdb_latexmk *.fls *.lof *.lol *.lot *.out *.synctex *.synctex.gz *.pdfsync *.toc *.4ct *.4tc *.dvi *.idv *.lg *.tmp *.xref *.xdv *.log *.pdf_tex
	rm -rf _minted-*/
	# Remove generated .tex files
	while IFS= read -r -d '' l10n_file; do
		language="$$(basename "$$l10n_file" .json)"
		rm -f "cv.$$language.tex"
	done < <(find l10n/ -type f -iname '*.json' -print0)

.PHONY: clean-pdf
clean-pdf:
	rm -f *.pdf

.PHONY: clean-png
clean-png:
	rm -f $(ALL_GENERATED_PNG)

.PHONY: lint
lint:
	yapf -ir .

.PHONY: pull
pull:
	@set -euo pipefail
	images=("$(DOCKER_LATEX_IMAGE)" "$(DOCKER_PYTHON_IMAGE)" "$(DOCKER_INKSCAPE_IMAGE)")
	for image in "$${images[@]}"; do
		docker pull "$$image"
	done

.PHONY: open
open:
	@set -euo pipefail
	if ! command -v xdg-open &> /dev/null; then
		echo 'Cannot open the PDF files: The program xdg-open is not installed.' 1>&2
		exit 1
	fi

	while IFS= read -r -d '' file; do
		echo "Opening \"$$file\"..."
		xdg-open "$$file" &> /dev/null &
	done < <(find . -maxdepth 1 -name '*.pdf' -print0)
	echo 'Done.'

# GENERATE PNG OUT OF SVG

images/auto-stories.png: images/auto-stories.svg
images/computer.png: images/computer.svg
images/cv.png: images/cv.svg
images/default_profile.png: images/default_profile.svg
images/email.png: images/email.svg
images/explore.png: images/explore.svg
images/flag-ca.png: images/flag-ca.svg
images/flag-es.png: images/flag-es.svg
images/flag-fr.png: images/flag-fr.svg
images/github.png: images/github.svg
images/language.png: images/language.svg
images/lightbulb.png: images/lightbulb.svg
images/linkedin.png: images/linkedin.svg
images/location.png: images/location.svg
images/person.png: images/person.svg
images/phone.png: images/phone.svg
images/poll.png: images/poll.svg
images/profile.png: images/profile.svg
images/running.png: images/running.post.svg
images/school.png: images/school.svg
images/skype.png: images/skype.svg
images/work.png: images/work.svg

$(ALL_GENERATED_512_PNG):
	$(DOCKER_INKSCAPE) -C --export-filename "/root/svg/$@" -w 512 -h 512 "/root/svg/$<"

images/cv16.png: images/cv.svg
	$(DOCKER_INKSCAPE) -C --export-filename "/root/svg/$@" -w 16 -h 16 "/root/svg/$<"

images/cv32.png: images/cv.svg
	$(DOCKER_INKSCAPE) -C --export-filename "/root/svg/$@" -w 32 -h 32 "/root/svg/$<"

images/cv48.png: images/cv.svg
images/flag-ca48.png: images/flag-ca.svg
images/flag-fr48.png: images/flag-fr.svg

$(ALL_GENERATED_48_PNG):
	# 48-sized PNG are exported according to the drawing, not the canvas
	$(DOCKER_INKSCAPE) -D --export-filename "/root/svg/$@" -w 48 "/root/svg/$<"

.PHONY: png
png: $(ALL_GENERATED_PNG)

# GENERATE TEX FILES

cv.%.tex: cv_generator.py cv.template.tex l10n/%.json
	@set -euo pipefail
	if [[ "$@" = "cv.template.tex" ]]; then
		exit 0
	fi

	# Search for the Python 3 executable
	python_exec=python3
	if ! command -v "$$python_exec" &> /dev/null; then
		if command -v python &> /dev/null; then
			python_exec=python
		else
			# No executable found
			python_exec=
		fi
	fi

	if [[ -n $$python_exec ]]; then
		# If an executable is found, check the version
		python_version_minor=$("$$python_exec" --version | grep -oPe '^Python\s+3\.\K([0-9]+)')
		if [[ -z $$python_version_minor || "$$python_version_minor" -lt 7 ]]; then
			# If the version is less than 3.7, assume there is no Python executable
			python_exec=
		fi
	fi

	# If the python executable is found, use it to generate the CV
	if [[ -n $$python_exec ]]; then
		$$python_exec --version
		if [[ ! -f .pip-requirements ]]; then
			$$python_exec -m pip install --user -r requirements.txt
			touch .pip-requirements
		fi
		python3 cv_generator.py
	else
		# Otherwise, use Docker

		docker run \
			-i \
			--rm \
			--name="python-generate-$@" \
			-v "$$(pwd):/cv" \
			--workdir=/cv \
			--entrypoint=bash \
			"$(DOCKER_PYTHON_IMAGE)" \
				-c "pip install --user -r requirements.txt && python cv_generator.py && chown $$(id -u):$$(id -g) *.tex"
	fi

# GENERATE PDF

cv.%.pdf: cv.%.tex $(TEX_DEPENDENCIES)
	@set -euo pipefail

	PS4='$$ '
	set -x
	docker run \
		-i \
		--rm \
		--name="latex-make-$@" \
		-v "$$(pwd):/latex" \
		--workdir=/latex \
		--entrypoint=/bin/bash \
		$(DOCKER_LATEX_IMAGE) \
			-c "/latex/docker-entrypoint.sh make $<"
	
	{ set +x; } 2> /dev/null

.PHONY: cv
cv: all

# GENERATE DOCX

%.docx: %.pdf
	"/c/Program Files/Microsoft Office/root/Office16/WINWORD.exe" $<
