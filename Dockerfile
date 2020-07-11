FROM cynnexis/latex

RUN mkdir /latex
WORKDIR /latex

# Setting environment variables for both image and future containers
ARG DEBIAN_FRONTEND=noninteractive
ENV DEBIAN_FRONTEND=noninteractive
ARG OSFONTDIR="/usr/share/fonts:/usr/local/share/fonts:/root/.fonts"
ENV OSFONTDIR="/usr/share/fonts:/usr/local/share/fonts:/root/.fonts"

# Install dependencies
RUN apt-get install -qy dos2unix

# Update font cache
RUN luaotfload-tool --update

COPY . .

# Some files on Windows use CRLF newlines. It is incompatible with UNIX.
RUN dos2unix docker-entrypoint.sh && chmod a+rwx docker-entrypoint.sh

ENTRYPOINT ["bash", "./docker-entrypoint.sh"]
