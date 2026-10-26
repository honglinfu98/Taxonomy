# WWW '27 paper build
MAIN = main
BUILD = build

.PHONY: all pdf pages clean distclean watch camera

all: pdf

pdf:
	latexmk -pdf $(MAIN).tex

watch:
	latexmk -pdf -pvc $(MAIN).tex

## Report total pages and the page on which References start (8-page body rule)
pages: pdf
	@bash scripts/check_pages.sh $(BUILD)/$(MAIN).pdf

## Build a camera-ready PDF (flips \camerareadytrue without editing main.tex)
camera:
	latexmk -pdf -jobname=$(MAIN)-camera -usepretex='\def\forcecamera{}' $(MAIN).tex

clean:
	latexmk -c
	rm -f $(BUILD)/*.bbl $(BUILD)/*.synctex.gz

distclean:
	latexmk -C
	rm -rf $(BUILD)
