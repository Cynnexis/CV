DOCKER_IMAGE=cynnexis/cv
DOCKER_INKSCAPE := docker run --rm -v "$$(pwd):/root/svg/" cynnexis/inkscape --export-overwrite
ALL_GENERATED_512_PNG := images/computer.png images/cv.png images/default_profile.png images/email.png images/flag-ca.png images/flag-es.png images/flag-fr.png images/github.png images/language.png images/lightbulb.png images/linkedin.png images/location.png images/person.png images/phone.png images/poll.png images/profile.png images/running.png images/school.png images/skype.png images/space.png images/work.png images/write.png
ALL_GENERATED_16_PNG := images/cv16.png
ALL_GENERATED_32_PNG := images/cv32.png
ALL_GENERATED_48_PNG := images/cv48.png images/flag-ca48.png images/flag-fr48.png
ALL_GENERATED_PNG_EXCEPT_48 := $(ALL_GENERATED_512_PNG) $(ALL_GENERATED_32_PNG) $(ALL_GENERATED_16_PNG)
ALL_GENERATED_PNG := $(ALL_GENERATED_PNG_EXCEPT_48) $(ALL_GENERATED_48_PNG)
TEX_DEPENDENCIES := resume.cls $(ALL_GENERATED_PNG)
ALL_CV := cv.en.pdf cv.fr.pdf

.PHONY: all clean docker-build docker-rmi docker-kill png cv

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
	@echo "  cv.en.pdf    - Generate the resume in English, as a PDF."
	@echo "  cv.fr.pdf    - Generate the resume in French, as a PDF."
	@echo "  cv.en.docx   - Generate the resume in English, as a DOCX file."
	@echo "  cv.fr.docx   - Generate the resume in French, as a DOCX file."
	@echo ''

all: cv

clean: clean-build clean-pdf clean-image

clean-build:
	rm -f *.aux *.auxlock *.bbl *.blg *.fdb_latexmk *.fls *.lof *.lol *.lot *.out *.synctex *.synctex.gz *.pdfsync *.toc *.4ct *.4tc *.dvi *.idv *.lg *.tmp *.xref *.xdv *.log *.pdf_tex
	rm -rf _minted-*/

clean-pdf:
	rm -f *.pdf

clean-image:
	rm -f $(ALL_GENERATED_PNG_EXCEPT_48)

docker-build:
	docker build -t $(DOCKER_IMAGE) .

docker-rmi:
	docker rmi -f $(DOCKER_IMAGE)

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
images/space.png: images/space.svg
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

# GENERATE PDF

cv.en.pdf: cv.en.tex $(TEX_DEPENDENCIES)
cv.fr.pdf: cv.fr.tex $(TEX_DEPENDENCIES)

$(ALL_CV):
	docker run --rm -v "$$(pwd):/latex" $(DOCKER_IMAGE) make $<

cv: $(ALL_CV)

# GENERATE DOCX

%.docx: %.pdf
	"/c/Program Files/Microsoft Office/root/Office16/WINWORD.exe" $<
