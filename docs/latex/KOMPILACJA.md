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

## Błąd BibTeX: „I found no \\citation commands”

**Przyczyna:** `bibtex` uruchomił się zanim `pdflatex` wygenerował poprawny plik `praca.aux` (albo `pdflatex` przerwał się błędem).

**Rozwiązanie:**

1. Otwórz terminal w folderze `docs\latex` (nie w głównym MultiVerify).
2. Wyczyść artefakty:
   ```powershell
   Remove-Item praca.aux, praca.bbl, praca.blg, praca.out, praca.toc -ErrorAction SilentlyContinue
   Remove-Item chapters\*.aux -ErrorAction SilentlyContinue
   ```
3. Kompiluj w kolejności:
   ```powershell
   pdflatex praca.tex
   bibtex praca
   pdflatex praca.tex
   pdflatex praca.tex
   ```
   Lub jednym poleceniem: `latexmk -pdf -g praca.tex`

W TeXstudio / VS Code ustaw **katalog roboczy** na `docs/latex`.
