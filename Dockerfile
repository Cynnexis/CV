FROM cynnexis/latex

RUN mkdir /latex
WORKDIR /latex

# Setting environment variables for both image and future containers
ARG DEBIAN_FRONTEND=noninteractive
ENV DEBIAN_FRONTEND=noninteractive
ARG OSFONTDIR="/usr/share/fonts:/usr/local/share/fonts:/root/.fonts"
ENV OSFONTDIR="/usr/share/fonts:/usr/local/share/fonts:/root/.fonts"

# Update font cache
RUN luaotfload-tool --update

COPY . .
# Compile LaTeX documents using LuaLaTeX
CMD [ "bash", "-c", "DEBIAN_FRONTEND=noninteractive lualatex -shell-escape -halt-on-error -interaction=batchmode -output-directory . cv.en.tex && lualatex -shell-escape -halt-on-error -interaction=batchmode -output-directory . cv.fr.tex" ]