\NeedsTeXFormat{LaTeX2e}
%\ProvidesClass{nthu_thesis}[2025/07  by NTHU LIB DSLIN]

\LoadClass[12pt, UTF8, openany,oneside]{ctexbook}

\usepackage{geometry}

%\usepackage{showframe} % for viewing margins 
\usepackage{pdfpages}

\usepackage{csquotes}
\usepackage[UTF8, fontset=none]{ctex}
\defaultfontfeatures{ Scale=MatchUppercase,
                      Ligatures=TeX,
                      Renderer=HarfBuzz }

\usepackage{braket}
\usepackage{tikz} 
\usepackage{algorithm}
\usepackage{algpseudocode}
% Define custom Match-Case blocks
\algblockdefx[Match]{Match}{EndMatch}[1]{\textbf{match} #1 \textbf{do}}{\textbf{end match}}
\algblockdefx[Case]{Case}{EndCase}[1]{\textbf{case} #1:}{}
% Tell LaTeX to stop printing end statements for individual cases to keep it clean
\algnotext{EndCase} 
\usepackage{array}
\usepackage{quantikz}
\usepackage{circuitikz}
\usepackage{tabularx}
% Define a new centered column type with identical distributed widths
\newcolumntype{C}{>{\centering\arraybackslash}X} 




 % Options
\DeclareOption{master}{\gdef\@degreeZH{碩}}
\DeclareOption{doctor}{\gdef\@degreeZH{博}}
%\DeclareOption{nowatermark}{\gdef\nowatermark{1}}
\ProcessOptions\relax   %must be inserted after all the option-handling commands were typed.
%-------------------------------------------------------------
% [字體大小設定]
% Command	10pt	11pt	12pt
% \tiny	     5	6	6
% \scriptsize	7	8	8
%\footnotesize	8	9	10
%\small	9	10	10.95
%\normalsize (default)	10	10.95	12
%\large	12	12	14.4
%\Large	14.4	14.4	17.28
%\LARGE	17.28	17.28	20.74
%\huge	20.74	20.74	24.88
%\Huge	24.88	24.88	24.88

%-------------------------------------------------------------
% [字體設定]
\setmainfont{Latin Modern Roman}[Scale=1.0]          	%襯線字體
% - \setsansfont{}          	非襯字體
% - \setmonofont{}          	等寬字體
\setCJKmainfont{Noto Serif CJK SC}			%中文襯線字體
\setCJKsansfont{Noto Sans CJK SC}			%中文非襯字體
\setCJKmonofont{Noto Sans Mono CJK SC}			%中文等寬字體
%
\usepackage{anyfontsize}
\usepackage{fontspec} %加這個就可以設定字體
\setmainfont{Times New Roman} % Set font for Latin script (English)
\setsansfont{Arial}  %The elements that require a sans font
\setmonofont[Color={0019D4}]{Courier New} %Everything to be formatted with a monospaced (typewriter-like)


% Set font for Traditional Chinese and alternative  % AR PL KaitiM GB for 文鼎 PL 中楷
% \setCJKmainfont{TW-Kai}

% Set language to Traditional Chinese explicitly
 % ctexset configurationra
\ctexset{
  contentsname = Table of Contents, % "Table of Contents" in Traditional Chinese
  appendixname = Appendix, % "Appendix" in Traditional Chinese
  listfigurename = List of Figures,
  listtablename = List of Tables,
  bibname = Bibliography, % Bibliography title
  tablename = Table,
  abstractname = Abstract,
  chapter={
    name = { Chapter\ },
      number = \arabic{chapter}, % Arabic numerals for clarity in thesis
      % number = \chinese{chapter}, % or Chinese numerals 
    format = \huge\bfseries\centering, % ~18pt, bold, centered
    beforeskip = -1.0\baselineskip,
    afterskip = 0.5\baselineskip,
  },
  section={
    % name = {節},
    format = \Large\bfseries, % ~14pt, bold
    beforeskip = 0.5\baselineskip,
    afterskip = 0.5\baselineskip,
  },
  subsection={
    format = \large\bfseries, % ~12pt, bold
    beforeskip =0.5\baselineskip,
    afterskip = 0.5\baselineskip,
  }
}


\usepackage{emptypage}  %prevents page numbers and headings from appearing on empty pages.

% --------------------------------------------------
% 設定行距
\usepackage{setspace}
\setstretch{1.5}  % gives MS Word-like 1.5x spacing across fonts
% Set global line spacing (e.g., for English) %清大註冊組論文格式規定 中英文都是1.5
%\onehalfspacing % ~1.25x spacing only 


% Single spacing for specific elements
\AtBeginEnvironment{thebibliography}{\singlespacing} % Bibliography
\AtBeginEnvironment{figure}{\singlespacing} % Figure captions
\AtBeginEnvironment{table}{\singlespacing} % Table captions

\usepackage[skip=10pt plus1pt, indent=30pt]{parskip}

\usepackage{titlesec}  %for title spacing

%\titlespacing*{\chapter}{0pt}{-20pt}{15pt}
\titlespacing*{\chapter}
   {0pt}% left
   {-2em}% before
   {2em}% after

\xeCJKsetup{CJKglue=\hskip 0.2em plus 0.1em minus 0.1em} % set spacing between chinese characters and latin


\usepackage[style=ieee]{biblatex}  %  參考文獻 這裡用 IEEE bibliography style here, can be change to plain (science), alpha, and abbrv, apa，ieeetr
\addbibresource{back/references.bib}
\usepackage[english]{babel}   %needed for above line

\usepackage{amsmath, amsthm, amssymb}   % improve math presentation
\usepackage{ulem, CJKulem}              % 下劃線、雙下劃線與波浪紋效果

\usepackage{booktabs}                   % 改善表格設置
\usepackage{tabularx} % extra features for tabular environment


\usepackage[allow-number-unit-breaks]{siunitx}
\usepackage{hyphenat}

\usepackage[dvipsnames]{xcolor} %xcolor is more flexible, dvipsnames loads 68 named colors (CMYK)

\usepackage[colorlinks=true, urlcolor=blue, linkcolor=red]{hyperref}
%\usepackage[final]{hyperref} % adds hyper links inside the generated pdf file
\hypersetup{colorlinks=true,linkcolor=black,citecolor=blue,filecolor=magenta,urlcolor=blue}

\usepackage{ragged2e} % for line alignment justify options
%\setlength{\parindent}{30pt}
\usepackage{indentfirst}
\usepackage{romannum}
\usepackage{scalefnt}

\usepackage{nomencl} % for symbols
\makenomenclature  %needed to couple with above line
\usepackage{glossaries} % for abbreviations
\makeglossaries


\usepackage{multirow}
\setlength{\arrayrulewidth}{0.3mm} %sets the thickness of the borders of the table. In the example is 0.5mm but you can use other units—see the article Lengths in LaTeX for a complete list.
\setlength{\tabcolsep}{18pt} %The space between the text and the left/right border of its containing cell is set to 18pt with this command. Again, you may use other units if needed.
\renewcommand{\arraystretch}{1.5} %The height of each row is set to 1.5 relative to its default height.


\usepackage{graphicx}           % figures need this
\graphicspath{ {./figures/} }% drag figures in this directory 

%\usepackage{background} % for full page image setting
\usepackage[width=.75\textwidth]{caption} %figure captions need this

% Caption settings
\captionsetup[figure]{name=Figure, font=normalsize, labelfont=bf} % 10pt captions, bold label % ensures it doesn’t revert to "图".
\captionsetup[table]{name=Table, font=normalsize, labelfont=bf} % Apply to tables if needed

\usepackage{wrapfig}  
\usepackage[labelformat=simple]{subcaption} %subfigure captions need this

\usepackage[absolute,overlay]{textpos}

\usepackage{enumitem} % Ensure proper handling of enumerate environments



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% define absolute path to images %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
\graphicspath{{./images/}}%
% if you like to seperate figures in each chapters
% \appendgraphicspath{{./figures/chapter01/}}
% \appendgraphicspath{{./figures/chapter02/}}
%\appendgraphicspath{{./figures/chapter03/}}
%\appendgraphicspath{{./figures/chapter04/}}
%\appendgraphicspath{{./figures/chapter05/}}
%\appendgraphicspath{{./figures/chapter10/}}



% Chapter format in TOC
% Preamble and settings
\usepackage{tocloft}  % Added for TOC customization

% Configure TOC title format with tocloft
\setlength{\cftbeforetoctitleskip}{1\baselineskip} % Space before TOC title
\setlength{\cftaftertoctitleskip}{1\baselineskip} % Space after TOC title
% Increase font size of chapter titles in TOC
\renewcommand{\cftchapfont}{\large\bfseries} % ~18pt,Larger, (bold) chapter titles in TOC

% TOC title formatting
\renewcommand{\cfttoctitlefont}{\Huge\bfseries\centering}
%\renewcommand{\cfttoctitlefont}{\hspace*{\fill}\Huge\bfseries}
\renewcommand{\cftaftertoctitle}{\hspace*{\fill}}


\setcounter{tocdepth}{2}                   % 設定目錄深度
\setcounter{secnumdepth}{2}                % 設定編號深度
% Insert table of contents
%\setcounter{tocdepth}{-1} -- only parts
%\setcounter{tocdepth}{0} -- only parts and chapters
%\setcounter{tocdepth}{1} -- part,chapters,sections
%\setcounter{tocdepth}{2} -- part,chapters,sections, subsections
%\setcounter{tocdepth}{3} -- part,chapters,sections, subsections,sub


% [附錄]
% \appendix{NUM}{TITLE}
%
\usepackage[titletoc,toc,title]{appendix}
\usepackage{blindtext}

