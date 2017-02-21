

slides: slides.tex 
	xelatex slides.tex

out: surface
	open surface.pdf 
	cp surface.pdf ~/home/Dropbox

meaning: meaning.tex refs.bib
	xelatex meaning.tex
	bibtex meaning
	xelatex meaning.tex
	xelatex meaning.tex


surface: surface.tex refs.bib
	xelatex surface.tex
	bibtex surface
	xelatex surface.tex
	xelatex surface.tex

