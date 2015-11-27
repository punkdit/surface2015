

out: surface
	open surface.pdf 

surface: surface.tex refs.bib
	xelatex surface.tex
	bibtex surface
	xelatex surface.tex
	xelatex surface.tex

