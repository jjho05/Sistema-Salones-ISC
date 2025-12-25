# LaTeX Article - MDPI Format

## Intelligent Classroom Assignment System

This directory contains the LaTeX source for the academic article based on the classroom assignment optimization project.

### Files

- `main.tex` - Main LaTeX document (MDPI format)
- `Definitions/` - MDPI class files (download from MDPI website)

### Compilation

To compile the document:

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Or use your preferred LaTeX editor (Overleaf, TeXShop, etc.)

### MDPI Template

This article uses the MDPI template for the journal "Algorithms". 

**Note:** You need to download the MDPI class file (`mdpi.cls`) from:
https://www.mdpi.com/authors/latex

Place it in the `Definitions/` folder.

### Article Structure

1. **Introduction** - Problem statement, motivation, contributions
2. **Related Work** - Literature review on educational timetabling
3. **Problem Formulation** - Mathematical model with equations
4. **Optimization Algorithms** - Four algorithms described in detail
5. **Experimental Methodology** - Dataset, design, metrics, statistics
6. **Results** - Descriptive statistics, comparative analysis, statistical validation
7. **Discussion** - Performance analysis, limitations, practical impact
8. **Conclusions** - Summary, best practices, future work

### Key Features

- Complete mathematical formulation with LaTeX equations
- Comprehensive tables for results
- Statistical validation (ANOVA, Tukey HSD, Cohen's d)
- 10 references to related work
- MDPI-compliant formatting
- Ready for journal submission

### Customization

Before submission, update:
- Author ORCID ID (line 32)
- Affiliation details (line 41)
- Contact email (line 44)
- Dates (lines 24-27)
- References (add more as needed)

### License

This LaTeX document is part of the Sistema-Salones-ISC project.
See main repository for license details.
