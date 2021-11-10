FROM cynnexis/latex

RUN mkdir /latex
WORKDIR /latex

# Setting environment variables for both image and container
ENV DEBIAN_FRONTEND=noninteractive
ENV OSFONTDIR="/usr/share/fonts:/usr/local/share/fonts:/root/.fonts"

ENV TERM=xterm-256color

COPY . .

RUN \
    apt-get update && \
    apt-get install -qqy dos2unix && \
    rm -rf /var/lib/apt/lists/* && \
    # Update font cache
    luaotfload-tool --update && \
    # Some files on Windows use CRLF newlines. It is incompatible with UNIX.
    dos2unix docker-entrypoint.sh && \
    chmod a+rwx docker-entrypoint.sh

ENTRYPOINT ["bash", "./docker-entrypoint.sh"]
