\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{resume}[2011/03/26 My custom CV class]
\LoadClass{article}

% https://www.overleaf.com/learn/latex/How_to_write_a_LaTeX_class_file_and_design_your_own_CV_(Part_1)
% https://www.overleaf.com/learn/latex/How_to_write_a_LaTeX_class_file_and_design_your_own_CV_(Part_2)

\PassOptionsToPackage{T1}{fontenc}
\PassOptionsToPackage{table}{xcolor}
\RequirePackage{fontenc}
\RequirePackage{titlesec}
\RequirePackage{xcolor}
\RequirePackage{changepage}
\RequirePackage{float}
\RequirePackage{graphicx}

% Change font (see all fonts at https://www.overleaf.com/learn/latex/Font_typefaces)
\usepackage{lmodern}

% Switch all fonts to sans serif by default (except math expressions)
\renewcommand{\familydefault}{\sfdefault}

\definecolor{primary-color}{HTML}{45818E} % #45818E
\definecolor{light-primary-color}{HTML}{6facb9} % #6facb9
\definecolor{dark-primary-color}{HTML}{294d55} % #294d55
\definecolor{primary-text-color}{HTML}{FFFFFF} % #FFFFFF
\definecolor{h1-color}{HTML}{45818E} % #45818E
\definecolor{h2-color}{HTML}{294d55} % #294d55
\definecolor{h3-color}{HTML}{938690} % #938690
\definecolor{link-color}{HTML}{185BC1} % #185BC1

\definecolor{muted-color}{HTML}{3E4550} % #3E4550
\definecolor{margin-background-color}{HTML}{EEEEEE} % #EEEEEE

% Change the thickness of the horizontal bar
\def\hrulefill{\leavevmode\leaders\hrule height 1.2pt\hfill\kern\z@}

% Line spacing, see https://www.overleaf.com/learn/latex/Paragraph_formatting
\setlength{\parindent}{0cm}
\setlength{\parskip}{0cm}
\renewcommand{\baselinestretch}{0.8}
\renewcommand{\linespread}{0}

% Change color of bullet points
\renewcommand{\labelitemi}{\textcolor{primary-color}{\textbullet}}
\renewcommand{\labelitemii}{\textcolor{h2-color}{\textbullet}}
\renewcommand{\labelitemiii}{\textcolor{h3-color}{\textbullet}}

\newcommand{\firstcolumnwidth}{0.25\textwidth}
\newcommand{\secondcolumnwidth}{0.70\textwidth}
\newcommand{\leftspace}{0.2cm}

\newcommand{\link}[2]{\textcolor{link-color}{\underline{\href{#1}{#2}}}}

\newcommand{\myname}{\hspace{4cm}\fontfamily{qag}\selectfont\huge\color{primary-text-color}\textbf{Valentin Berger}}
\newcommand{\mytitle}[1]{
	\begin{adjustwidth}{4cm}{0cm}
		\color{primary-text-color}\fontfamily{qag}\selectfont\huge #1
	\end{adjustwidth}
}
\newcommand{\jump}{\vspace{0.4\baselineskip}}
\newcommand{\bigjump}{\vspace{0.6\baselineskip}}
\newcommand{\icon}[1]{\raisebox{-0.2\height}{\includegraphics[height=15pt]{#1}}}
\newcommand{\sideicon}[1]{\centering\raisebox{-0.5\height}{\includegraphics[height=15pt]{#1}}}
\newcommand{\lineunder}{\vspace*{-5pt}\par{\color{primary-color}\hrulefill}\\} %\par \hspace*{-4pt}
\newcommand{\group}[2]{
	\noindent\icon{#1} {\normalsize\fontfamily{qag}\selectfont\textbf{#2}}\lineunder
}
\newcommand{\entrytitle}[1]{
	\begin{adjustwidth}{\leftspace}{0cm}
		{\normalsize\textbf{#1}}
	\end{adjustwidth}
}
\newcommand{\entrydescription}[1]{
	\begin{adjustwidth}{\leftspace}{0cm}
		{\normalsize #1}
	\end{adjustwidth}
}
\newcommand{\entrydate}[1]{
	\begin{adjustwidth}{\leftspace}{0cm}
		{\small\textcolor{h3-color}{#1}}
	\end{adjustwidth}
}
