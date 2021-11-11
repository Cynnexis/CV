FROM python:3.7.12-bullseye

ARG UID=1000
ARG GID=1000

RUN \
	# Create group & user
	addgroup --gid $GID cv && \
	adduser --home /home/cv cv --shell /bin/bash --uid $UID --gid $GID --disabled-password --gecos "Default user to generate LaTeX files for the resume."

USER cv
