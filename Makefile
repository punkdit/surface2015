

out: surface
	open surface.pdf 

surface: surface.tex refs.bib
	pdflatex surface.tex
	bibtex surface
	pdflatex surface.tex
	pdflatex surface.tex

