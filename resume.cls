\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{resume}[2018/20/12 LaTeX file for resume]
\LoadClass[a4paper,11pt]{article}

% https://www.overleaf.com/learn/latex/How_to_write_a_LaTeX_class_file_and_design_your_own_CV_(Part_1)
% https://www.overleaf.com/learn/latex/How_to_write_a_LaTeX_class_file_and_design_your_own_CV_(Part_2)

\PassOptionsToPackage{table}{xcolor}
\PassOptionsToPackage{top=0cm, bottom=0cm, left=0cm, right=0cm, headsep=0cm}{geometry}
\PassOptionsToPackage{english}{babel}
\RequirePackage{babel}
\RequirePackage{fontspec}
\RequirePackage{titlesec}
\RequirePackage{xcolor}
\RequirePackage{changepage}
\RequirePackage{float}
\RequirePackage{graphicx}
\RequirePackage{verbatim}
\RequirePackage{float}
\RequirePackage{graphicx}
\RequirePackage{csquotes}
\RequirePackage{geometry}
\RequirePackage{hyperref}
\RequirePackage{xparse}
\RequirePackage{ifthen}

\graphicspath{{./images/}}

% Set custom fonts https://www.overleaf.com/learn/latex/Questions/I_have_a_custom_font_I%27d_like_to_load_to_my_document._How_can_I_do_this%3F
\newfontfamily{\gothic}{GOTHIC}[Path=fonts/,Extension=.ttf]
\newfontfamily{\gothicb}{GOTHICB}[Path=fonts/,Extension=.ttf]
\newfontfamily\DejaSans{DejaVu Sans}

\setmainfont{Calibri}
\setsansfont{Calibri}
%\setmonofont{Consola}

% Switch all fonts to sans serif by default (except math expressions)
\renewcommand{\familydefault}{\sfdefault}

\definecolor{primary-color}{HTML}{46b0c7} % #46b0c7
\definecolor{primary-text-color}{HTML}{FFFFFF} % #FFFFFF
\definecolor{h1-color}{HTML}{46b0c7} % #46b0c7
\definecolor{h2-color}{HTML}{000000} % #000000
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
\renewcommand{\labelitemi}{\textcolor{h1-color}{\textbullet}}
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
\newcommand{\profilesize}{100pt}

\newcommand{\link}[2]{\textcolor{link-color}{\underline{\href{#1}{#2}}}}

\newcommand{\myname}{\gothicb\fontsize{18}{0.2}\selectfont\color{primary-text-color}\textbf{Valentin Berger}}
\newcommand{\mytitle}[1]{\color{primary-text-color}\gothic\fontsize{18}{0.2}\selectfont #1}
\newcommand{\jump}[1][0.5]{\vspace{#1\baselineskip}}
\newcommand{\bigjump}{\jump[1.5]}
\newcommand{\Bigjump}{\jump[2]}
\newcommand{\sideicon}[1]{\raisebox{-0.5\height}{\includegraphics[height=18pt]{#1}}}
\newcommand{\icon}[1]{\raisebox{-0.2\height}{\includegraphics[height=18pt]{#1}}}
\newcommand{\lineunder}{\vspace*{-5pt}\par{\color{primary-color}\hrulefill}\\} %\par \hspace*{-4pt}
\newcommand{\grouptitle}[1]{\noindent{\fontsize{12}{\baselinestretch}\selectfont #1}\lineunder}
\newcommand{\entrytitle}[1]{
	\begin{adjustwidth}{\leftspace}{0cm}
		{\fontsize{11}{\baselinestretch}\selectfont\textcolor{h2-color}{\textbf{#1}}}
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

\newcommand{\header}[1]{
	\noindent\fcolorbox{primary-color}{primary-color}{
		\begin{minipage}{\paperwidth}%
			\vspace{0.5cm}
			\begin{minipage}[t]{0.3\paperwidth}
				\hspace{1.5cm}%
				\raisebox{-\profilesize}{
					\includegraphics[width=\profilesize]{profile}%
				}
			\end{minipage}%
			\begin{minipage}[t]{0.65\paperwidth}
				\vspace{0.8cm}
				\myname
				
				\mytitle{#1}
			\end{minipage}
			\vspace{0.5cm}
		\end{minipage}
	}%
}

\newcommand{\sidepanel}[1]{
	\noindent\fcolorbox{margin-background-color}{margin-background-color}{
		\begin{minipage}[t][0.83\textheight]{\firstcolumnwidth}
			\jump[1]
			\begin{adjustwidth}{0.3cm}{0cm}
				#1
			\end{adjustwidth}
		\end{minipage}
	}%
}

\newcommand{\mainpanel}[1]{
	\begin{minipage}[t][0.83\textheight]{\secondcolumnwidth}
		#1
	\end{minipage}%
}

\newcommand{\contact}[2]{
	\firstwindowicon{person}{
		\begin{adjustwidth}{0.3cm}{0cm}
			\grouptitle{#1}
		\end{adjustwidth}
	}

	\jump
	#2%
}

\newcommand{\languages}[2]{
	\Bigjump
	\firstwindowicon{language}{
		\begin{adjustwidth}{0.3cm}{0cm}
			\grouptitle{#1}
		\end{adjustwidth}
	}

	\jump
	#2%
}

\newcommand{\interests}[2]{
	\Bigjump
	\firstwindowicon{lightbulb}{
		\begin{adjustwidth}{0.3cm}{0cm}
			\grouptitle{#1}
		\end{adjustwidth}
	}

	\jump
	#2%
}

\newcommand{\displomas}[2]{
	\jump[1]
	\secondwindowicon{school}{
		\grouptitle{#1}
		
		#2
	}%
}

\newcommand{\work}[2]{
	\bigjump
	\secondwindowicon{work}{
		\grouptitle{#1}
		
		#2
	}%
}

\newcommand{\skills}[2]{
	\bigjump
	\secondwindowicon{poll}{
		\grouptitle{#1}
		
		#2
	}%
}

\newcommand{\iconentry}[3]{
	\firstwindowicon{#1}{
		\entrytitle{#2}
		\entrydescription{#3}
	}
}

\newcommand{\cvfootnote}[2][true]{
	\vfill
	\begin{flushleft}
	\ifthenelse{\equal{\detokenize{#1}}{\detokenize{false}}}{}{\hfill}{\scriptsize\textcolor{muted-color}{#2}} $\quad$%
\end{flushleft}
}
