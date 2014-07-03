#!/bin/bash

mv .stuff/* .

pdflatex Main.tex

mv *.aux .stuff
mv *.log .stuff
mv *.lot .stuff
mv *.lof .stuff
mv *.blg .stuff
mv *.out .stuff
mv *.toc .stuff
mv *.bbl .stuff
mv *.fdb_latexmk .stuff

evince Main.pdf &
