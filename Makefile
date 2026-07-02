# --- Configuration ---
# Source directory where your .tex and .bib files live
SRC_DIR      := Thesis

# Name of your main LaTeX file (without the .tex extension)
MAIN_TARGET  := main

# Output PDF name (defaults to main target name)
OUTPUT_PDF   := $(MAIN_TARGET).pdf

# --- File Tracking ---
# Automatically find all dependency files in the source directory
TEX_FILES    := $(wildcard $(SRC_DIR)/*.tex)
BIB_FILES    := $(wildcard $(SRC_DIR)/*.bib)
PRE_FILES    := $(wildcard $(SRC_DIR)/*.cls)
ALL_DEPS     := $(TEX_FILES) $(PRE_FILES) $(BIB_FILES)

# Scratch directory for all auxiliary/intermediate build files.
# Removed entirely once the final PDF has been copied out.
BUILD_DIR    := Build

# --- Build Commands ---
# TEXINPUTS lets xelatex find .cls/.sty files that live in SRC_DIR
# BIBINPUTS lets biber find .bib files that live under SRC_DIR (e.g. Thesis/back/)
# (the trailing double-colon keeps the default TeX search paths too)
export TEXINPUTS := $(CURDIR)/$(SRC_DIR)//:
export BIBINPUTS := $(CURDIR)/$(SRC_DIR)//:
XELATEX      := xelatex -interaction=nonstopmode -halt-on-error
BIBER        := biber

# --- Rules ---
.PHONY: all clean purge

# Default target
all: $(OUTPUT_PDF)

# Main build recipe
$(OUTPUT_PDF): $(ALL_DEPS)
	@mkdir -p $(BUILD_DIR)

	@echo "==> Step 1: Initial XeLaTeX pass..."
	$(XELATEX) -output-directory=$(BUILD_DIR) $(SRC_DIR)/$(MAIN_TARGET).tex

	@echo "==> Step 2: Running Biber for references..."
	cd $(BUILD_DIR) && $(BIBER) $(MAIN_TARGET)

	@echo "==> Step 3: Second XeLaTeX pass..."
	$(XELATEX) -output-directory=$(BUILD_DIR) $(SRC_DIR)/$(MAIN_TARGET).tex

	@echo "==> Step 4: Final XeLaTeX pass for cross-references..."
	$(XELATEX) -output-directory=$(BUILD_DIR) $(SRC_DIR)/$(MAIN_TARGET).tex

	@echo "==> Step 5: Extracting PDF and cleaning up..."
	cp $(BUILD_DIR)/$(MAIN_TARGET).pdf $(OUTPUT_PDF)
	rm -rf $(BUILD_DIR)
	@echo "==> Build complete: $(OUTPUT_PDF)"

# Remove the scratch build directory, if it was left behind by a failed build
clean:
	rm -rf $(BUILD_DIR)

# Clean everything including the PDF
purge: clean
	rm -f $(OUTPUT_PDF)
