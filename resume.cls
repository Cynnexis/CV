\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{resume}[2018/20/12 LaTeX file for resume]
\LoadClass[a4paper,11pt]{article}

% https://www.overleaf.com/learn/latex/How_to_write_a_LaTeX_class_file_and_design_your_own_CV_(Part_1)
% https://www.overleaf.com/learn/latex/How_to_write_a_LaTeX_class_file_and_design_your_own_CV_(Part_2)

\PassOptionsToPackage{table}{xcolor}
\RequirePackage{fontspec}
\RequirePackage{titlesec}
\RequirePackage{xcolor}
\RequirePackage{changepage}
\RequirePackage{float}
\RequirePackage{graphicx}

% Set custom fonts https://www.overleaf.com/learn/latex/Questions/I_have_a_custom_font_I%27d_like_to_load_to_my_document._How_can_I_do_this%3F
\newfontfamily{\gothic}{GOTHIC}[Extension=.ttf]
\newfontfamily{\gothicb}{GOTHICB}[Extension=.ttf]
\newfontfamily\DejaSans{DejaVu Sans}

\setmainfont{Calibri}
\setsansfont{Calibri}
%\setmonofont{Consola}

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
\def\hrulefill{\leavevmode\leaders\hrule height 1.5pt\hfill\kern\z@}

% Line spacing, see https://www.overleaf.com/learn/latex/Paragraph_formatting
\setlength{\parindent}{0cm}
\setlength{\parskip}{0cm}
\renewcommand{\baselinestretch}{0.7}
\renewcommand{\linespread}{0}

% Change color of bullet points
\renewcommand{\labelitemi}{\textcolor{primary-color}{\textbullet}}
\renewcommand{\labelitemii}{\textcolor{h2-color}{\textbullet}}
\renewcommand{\labelitemiii}{\textcolor{h3-color}{\textbullet}}

\newcommand{\firstcolumnwidth}{0.30\textwidth}
\newcommand{\secondcolumnwidth}{0.65\textwidth}
\newcommand{\iconcolumnwidth}{0.1\textwidth}
\newcommand{\textcolumnwidth}{0.9\textwidth}
\newcommand{\firsticoncolumnwidth}{0.1\textwidth}
\newcommand{\firsttextcolumnwidth}{0.8\textwidth}%.9
\newcommand{\secondiconcolumnwidth}{0.05\textwidth}
\newcommand{\secondtextcolumnwidth}{0.88\textwidth}
\newcommand{\leftspace}{0.2cm}

\newcommand{\link}[2]{\textcolor{link-color}{\underline{\href{#1}{#2}}}}

\newcommand{\myname}{\hspace{4cm}\gothicb\fontsize{18}{0.2}\selectfont\color{primary-text-color}\textbf{Valentin Berger}}
\newcommand{\mytitle}[1]{
	\begin{adjustwidth}{4cm}{0cm}
		\color{primary-text-color}\gothic\fontsize{18}{0.2}\selectfont #1
	\end{adjustwidth}
}
\newcommand{\jump}[1][0.5]{\vspace{#1\baselineskip}}
\newcommand{\bigjump}{\jump[1.5]}
\newcommand{\Bigjump}{\jump[2]}
\newcommand{\sideicon}[1]{\raisebox{-0.5\height}{\includegraphics[height=18pt]{#1}}}
\newcommand{\icon}[1]{\raisebox{-0.2\height}{\includegraphics[height=18pt]{#1}}}
\newcommand{\lineunder}{\vspace*{-5pt}\par{\color{primary-color}\hrulefill}\\} %\par \hspace*{-4pt}
\newcommand{\grouptitle}[1]{\noindent{\fontsize{12}{\baselinestretch}\selectfont #1}\lineunder}
\newcommand{\entrytitle}[1]{
	\begin{adjustwidth}{\leftspace}{0cm}
		{\fontsize{11}{\baselinestretch}\selectfont\textbf{#1}}
	\end{adjustwidth}
}
\newcommand{\entrydescription}[1]{
	\begin{adjustwidth}{\leftspace}{0cm}
		{\fontsize{10}{\baselinestretch}\selectfont #1}
	\end{adjustwidth}
}
\newcommand{\entrydate}[1]{
	\begin{adjustwidth}{\leftspace}{0cm}
		{\fontsize{10}{\baselinestretch}\selectfont\textcolor{h3-color}{#1}}
	\end{adjustwidth}
}

% TODO: Check minipage options
\newcommand{\window}[5][0cm]{%
	\begin{minipage}[t]{#4}%
		#2%
	\end{minipage}%
	\hspace{#1}%
	\begin{minipage}[t]{#5}
		#3
	\end{minipage}%
}
\newcommand{\windowicon}[5][0cm]{\window[#1]{\icon{#2}}{#3}{#4}{#5}}
\newcommand{\firstwindow}[3][0cm]{\window[#1]{#2}{#3}{\firsticoncolumnwidth}{\firsttextcolumnwidth}}
\newcommand{\firstwindowicon}[3][0cm]{\window[#1]{\sideicon{#2}}{#3}{\firsticoncolumnwidth}{\firsttextcolumnwidth}}
\newcommand{\secondwindow}[3][0.2cm]{\window[#1]{#2}{#3}{\secondiconcolumnwidth}{\secondtextcolumnwidth}}
\newcommand{\secondwindowicon}[3][0.2cm]{\windowicon[#1]{#2}{#3}{\secondiconcolumnwidth}{\secondtextcolumnwidth}}
