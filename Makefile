

out: surface
	open surface.pdf 
	cp surface.pdf ~/home/Dropbox

surface: surface.tex refs.bib
	xelatex surface.tex
	bibtex surface
	xelatex surface.tex
	xelatex surface.tex

slides: slides.tex 
	xelatex slides.tex

