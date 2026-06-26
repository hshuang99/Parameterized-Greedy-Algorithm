# ---- Config ----
MAIN := main
SRCDIR := ./Thesis
BUILDDIR := build

# Make TeX/Biber search SRCDIR (and subfolders) for .cls/.sty/.bib/images
export TEXINPUTS := $(SRCDIR)//:
export BIBINPUTS := $(SRCDIR)//:

PDFLATEX := pdflatex -interaction=nonstopmode -halt-on-error -file-line-error \
            -output-directory=$(BUILDDIR)
BIBER := biber

SOURCES := $(wildcard $(SRCDIR)/*.tex) $(wildcard $(SRCDIR)/*.bib) $(wildcard $(SRCDIR)/back/*.bib)

.PHONY: all clean distclean

all: $(MAIN).pdf

$(BUILDDIR):
	mkdir -p $(BUILDDIR)

$(MAIN).pdf: $(BUILDDIR) $(SOURCES)
	$(PDFLATEX) $(SRCDIR)/$(MAIN).tex
	$(BIBER) $(BUILDDIR)/$(MAIN)
	$(PDFLATEX) $(SRCDIR)/$(MAIN).tex
	$(PDFLATEX) $(SRCDIR)/$(MAIN).tex
	cp $(BUILDDIR)/$(MAIN).pdf .

clean:
	rm -rf $(BUILDDIR)

distclean: clean
	rm -f $(MAIN).pdf
