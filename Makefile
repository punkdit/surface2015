

slides: slides.tex 
	xelatex slides.tex

out: surface
	open surface.pdf 
	cp surface.pdf ~/home/Dropbox

surface: surface.tex refs.bib
	xelatex surface.tex
	bibtex surface
	xelatex surface.tex
	xelatex surface.tex

