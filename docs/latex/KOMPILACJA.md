# Kompilacja dokumentacji LaTeX (lokalnie)

## Wymagania

- MiKTeX lub TeX Live (pdfLaTeX + BibTeX)
- Plik `figures/LogoURWydzial.png` (skopiowany z szablonu BSZ)

## Kompilacja

W folderze `docs/latex/`:

```powershell
cd docs\latex
pdflatex praca.tex
bibtex praca
pdflatex praca.tex
pdflatex praca.tex
```

Wynik: `praca.pdf`

## latexmk (opcjonalnie)

```powershell
latexmk -pdf praca.tex
```

## Uwagi

- Po dodaniu wykresów przez Kamila umieść pliki w `docs/latex/figures/` i odkomentuj `\includegraphics` w `chapters/07_wyniki.tex`.
- Uzupełnij tabelę FAR/FRR po uruchomieniu `scripts/compute_metrics.py`.
