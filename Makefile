SHELL := /bin/bash
DOCKER_IMAGE=cynnexis/cv
DOCKER_INKSCAPE := docker run --name="inkscape-generate-png" --rm -v "$$(pwd):/root/svg/" cynnexis/inkscape --export-overwrite
ALL_GENERATED_512_PNG := images/computer.png images/cv.png images/default_profile.png images/email.png images/flag-ca.png images/flag-es.png images/flag-fr.png images/github.png images/language.png images/lightbulb.png images/linkedin.png images/location.png images/person.png images/phone.png images/poll.png images/profile.png images/running.png images/school.png images/skype.png images/work.png images/write.png
ALL_GENERATED_16_PNG := images/cv16.png
ALL_GENERATED_32_PNG := images/cv32.png
ALL_GENERATED_48_PNG := images/cv48.png images/flag-ca48.png images/flag-fr48.png
ALL_GENERATED_PNG := $(ALL_GENERATED_512_PNG) $(ALL_GENERATED_32_PNG) $(ALL_GENERATED_16_PNG) $(ALL_GENERATED_48_PNG)
L10N_FILES := $(wildcard l10n/*.json)
TEX_DEPENDENCIES := resume.cls $(ALL_GENERATED_PNG)

.PHONY: help all clean clean-build clean-pdf clean-png docker-build docker-rmi docker-kill png cv $(DOCKER_IMAGE) cynnexis/cv-generator

.ONESHELL:

help:
	@echo "Makefile for generating the resume in different language."
	@echo ''
	@echo "USAGE: $(MAKE) [COMMAND]"
	@echo ''
	@echo "COMMANDS:"
	@echo ''
	@echo "  help         - Print this page."
	@echo "  all          - Generate the resumes in all available languages."
	@echo "  clean        - Remove all generate files from the project directory."
	@echo "  png          - Build all the images from the SVG files."
	@echo "  docker-build - Build the Docker image from the 'Dockerfile'."
	@echo "  docker-rmi   - Remove the build Docker image."
	@echo "  docker-kill  - Stop and remove all containers, dangling images and unused networks and volumes. Be careful when executing this command!"
	@echo "  cv.%.pdf     - Generate the resume in the language specified by %, as a PDF."
	@echo "  cv.%.docx    - Generate the resume in the language specified by %, as a DOCX file."
	@echo ''

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

clean: clean-build clean-pdf clean-png

clean-build:
	@set -euo pipefail
	rm -f *.aux *.auxlock *.bbl *.blg *.fdb_latexmk *.fls *.lof *.lol *.lot *.out *.synctex *.synctex.gz *.pdfsync *.toc *.4ct *.4tc *.dvi *.idv *.lg *.tmp *.xref *.xdv *.log *.pdf_tex
	rm -rf _minted-*/
	# Remove generated .tex files
	while IFS= read -r -d '' l10n_file; do
		language="$$(basename "$$l10n_file" .json)"
		rm -f "cv.$$language.tex"
	done < <(find l10n/ -type f -iname '*.json' -print0)

clean-pdf:
	rm -f *.pdf

clean-png:
	rm -f $(ALL_GENERATED_PNG)

$(DOCKER_IMAGE): Dockerfile
	docker build -t $@ -f $< .

cynnexis/cv-generator: python.Dockerfile
	docker build -t $@ -f $< --build-arg "UID=$$(id -u)" --build-arg "GID=$$(id -g)" .

docker-build: $(DOCKER_IMAGE) cynnexis/cv-generator

docker-rmi:
	docker rmi -f $(DOCKER_IMAGE) cynnexis/cv-generator

docker-kill:
	docker rm -f $$(docker ps -aq) ; docker rmi -f $$(docker images -f "dangling=true" -q) ; docker system prune -f

# GENERATE PNG OUT OF SVG

images/computer.png: images/computer.svg
images/cv.png: images/cv.svg
images/default_profile.png: images/default_profile.svg
images/email.png: images/email.svg
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
images/write.png: images/write.svg

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
		# Build image if not found
		if ! { docker images '--format={{.Repository}}' | grep -qPe '^cynnexis/cv-generator$$'; } ; then
			$(MAKE) cynnexis/cv-generator
		fi

		docker run \
			-i \
			--rm \
			--name="python-generate-$@" \
			-v "$$(pwd):/cv" \
			--workdir=/cv \
			--user "$$(id -u):$$(id -g)" \
			--entrypoint=bash \
			cynnexis/cv-generator \
				-c "pip install --user -r requirements.txt && python cv_generator.py"
	fi

# GENERATE PDF

cv.%.pdf: cv.%.tex $(TEX_DEPENDENCIES)
	docker run --name="latex-make-$@" --rm -v "$$(pwd):/latex" $(DOCKER_IMAGE) make $<

cv: all

# GENERATE DOCX

%.docx: %.pdf
	"/c/Program Files/Microsoft Office/root/Office16/WINWORD.exe" $<
