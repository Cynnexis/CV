# CV

![Repository Logo][repo-logo]

![Canadian Flag][en-Logo]
The English version of the résume is [here][cv-en].
The French version is [here][cv-fr].

![French Flag][fr-Logo]
La version française du CV peut être trouvé [ici][cv-fr].
La version anglaise peut être téléchargé [ici][cv-en].

# Build

The following steps will get you a copy of the project and the PDF files (in all languages).

First, clone the project using:

```bash
git clone https://github.com/Cynnexis/CV.git
cd CV
```

Then, use the `Makefile` to build the PDF. Note that this step requires **Docker**.

```bash
make docker-build
make cv
```

After Docker has downloaded all necessary images, and `lualatex` has been executed, you will find `cv.en.pdf` and `cv.fr.pdf` at the root of the project.

To remove only the PDF, execute `make clean-pdf`.

To remove the generated images, execute `make clean-png` (reciprocally `make png` to generate the images).

To remove only the LaTeX built files, use `make clean-build`.

Finally, to remove every generated files, use `make clean`.

[repo-logo]: images/cv48.png
[en-logo]: images/flag-ca48.png
[fr-logo]: images/flag-fr48.png
[cv-en]: cv.en.pdf
[cv-fr]: cv.fr.pdf