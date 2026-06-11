# Plan działania — MultiVerify

**Temat:** Systemy multimodalne (zaawansowane)  
**Przedmiot:** Biometryczne systemy zabezpieczeń  
**Zespół:** Kacper + Kamil  
**Termin oddania:** 12.06.2026  

---

## Status na dziś

- [x] Struktura projektu (modalności, fuzja, rejestracja, identyfikacja)
- [x] Zdjęcia i nagrania wrzucone do `data/users/kacper/` i `data/users/kamil/`
- [x] Rejestracja użytkowników (`register.py`)
- [x] Działająca identyfikacja (`main.py`)
- [ ] Eksperymenty + metryki (FAR, FRR)
- [x] Dokumentacja LaTeX (szkielet + treść, `docs/latex/praca.pdf`)
- [ ] Uzupełnienie wyników FAR/FRR i wykresów (Kamil)
- [x] README
- [ ] Paczka ZIP do oddania

---

## Podział ról

| Obszar | Kacper | Kamil |
|--------|--------|-------|
| Modalność twarzy + pipeline główny | **główny** | wsparcie |
| Modalność głosu + eksperymenty | wsparcie | **główny** |
| Fuzja + `main.py` / `register.py` | **główny** | testy |
| Metryki, wykresy, CSV | konsultacje | **główny** |
| Dokumentacja LaTeX | rozdz. 1–6 | rozdz. 7–9 + bibliografia |
| Pakowanie ZIP | **główny** | wsparcie |

---

## Jak działa program (przypomnienie)

```
1. Dane w data/users/<user>/face_*.jpg + voice_*.wav
2. python register.py  →  tworzy face_embeddings.npy + voice_embeddings.npy
3. python main.py      →  porównuje NOWE zdjęcie + nagranie z całą bazą (1:N)
4. FusionEngine        →  wynik = 0.6×twarz + 0.4×głos, próg 0.7
5. run_experiments.py  →  porównanie wariantów (face-only, voice-only, fusion)
```

**Probe (test logowania):** używajcie plików, które **nie są jedynym wzorcem w bazie** — najlepiej `face_3.jpg` + `voice_3.wav`, a `face_1`, `face_2`, `voice_1`, `voice_2` zostawcie tylko do rejestracji.

---

# FAZA 0 — Wspólne (dziś, ~1 h)

**Cel:** upewnić się, że dane i środowisko działają.

### Kacper
- [ ] Sprawdzić nazwy plików w `data/users/kacper/` i `data/users/kamil/`:
  - twarz: `face_1.jpg`, `face_2.jpg`, `face_3.jpg` (lub `.png`)
  - głos: `voice_1.wav`, `voice_2.wav`, `voice_3.wav` (lub `.mp3`)
- [ ] `pip install -r requirements.txt`
- [ ] Uruchomić `python register.py` i potwierdzić, że powstały pliki `.npy` w obu folderach

### Kamil
- [ ] To samo sprawdzenie plików po swojej stronie (czy nagrania są słyszalne, twarz widoczna)
- [ ] Uruchomić `pytest` — wszystkie testy muszą przechodzić
- [ ] Zapisać 1 próbę identyfikacji (screenshot konsoli) na później do raportu

### Wspólnie — kryterium sukcesu
- [ ] `register.py` kończy się bez błędów
- [ ] `main.py` z probe Kacpra rozpoznaje Kacpra
- [ ] `main.py` z probe Kamila rozpoznaje Kamila
- [ ] Probe obcej osoby (jeśli macie) → dostęp odmówiony

---

# FAZA 1 — Kod i uruchomienie

## Kacper (~3–4 h)

### 1.1 CLI w `main.py`
- [x] Dodać argumenty z linii poleceń (`argparse`):
  ```bash
  python main.py --face sciezka/do/zdjecia.jpg --voice sciezka/do/nagrania.wav
  ```
- [x] Usunąć hardcoded `nowe_zdjecie.jpg` / `nowe_nagranie.wav`

### 1.2 README.md
- [x] Opis projektu (2–3 zdania)
- [x] Wymagania: Python 3.x, `pip install -r requirements.txt`
- [x] Struktura folderów `data/users/`
- [x] Instrukcja krok po kroku:
  1. wrzuć pliki
  2. `python register.py`
  3. `python main.py --face ... --voice ...`
  4. `python scripts/run_experiments.py`
  5. `pytest`

### 1.3 (Opcjonalnie, +pkt za metody) Druga strategia fuzji
- [x] W `FusionEngine` dodać np. regułę AND: dostęp tylko gdy `face_score >= 0.7 AND voice_score >= 0.7`
- [x] Krótki test w `tests/test_fusion_engine.py`

### 1.4 Weryfikacja końcowa kodu
- [ ] Cały flow działa na świeżym środowisku (jak u prowadzącego)
- [ ] Przekazać Kamilowi działające ścieżki do probe

---

## Kamil (~3–4 h)

### 1.5 Poprawka logiki eksperymentów
- [ ] W `scripts/run_experiments.py`: jako probe używać **ostatniego** pliku (np. `face_3`, `voice_3`), nie `face_1` / `voice_1`
- [ ] Enrollment zostaje na `face_1`, `face_2`, `voice_1`, `voice_2` (albo wszystkie oprócz probe)
- [ ] Uruchomić skrypt i sprawdzić `docs/experiment_results.csv`

### 1.6 Skrypt metryk
- [ ] Utworzyć `scripts/compute_metrics.py` (lub rozszerzyć `run_experiments.py`)
- [ ] Dla każdego wariantu (`face_only`, `voice_only`, `fusion_*`) policzyć:
  - **Accuracy** — % poprawnych decyzji
  - **FAR** (False Accept Rate) — fałszywe akceptacje / liczba prób impostorów
  - **FRR** (False Reject Rate) — fałszywe odrzucenia / liczba prób prawdziwych użytkowników
- [ ] Wynik zapisać do `docs/metrics_summary.csv` lub `.txt`

### 1.7 Wykresy do raportu
- [ ] `docs/charts/far_frr_by_variant.png` — słupki FAR/FRR per wariant
- [ ] `docs/charts/threshold_sweep.png` — wpływ progu 0.5–0.9 na FAR i FRR (fusion 60/40)
- [ ] (Opcjonalnie) tabela accuracy w konsoli / CSV

### 1.8 Testy modalności głosu
- [ ] Krótki opis w notatkach: jak MFCC działa w `voice_modality.py` (do przekazania do rozdziału „Metody”)

---

# FAZA 2 — Dokumentacja LaTeX

**Szablon:** wymagany format z `BSZ_Projekt_Informacje (3).pdf`  
**Cel:** kompletny PDF, ~15–25 stron

## Kacper — rozdziały implementacji i twarzy

| Rozdział | Zawartość | Szac. czas |
|----------|-----------|------------|
| 1. Wprowadzenie | Cel, kontekst (kontrola dostępu), zakres | 45 min |
| 2. Problem i założenia | Dane wejściowe, ograniczenia (jakość zdjęć, szum audio) | 45 min |
| 4. Koncepcja rozwiązania | Schemat blokowy pipeline (diagram!) | 1 h |
| 5. Metody — część twarz | DeepFace, Facenet, embeddingi, cosine similarity | 1 h |
| 5. Metody — fuzja | Late fusion, wzór: `score = w_f×face + w_v×voice` | 30 min |
| 6. Implementacja | Struktura `src/`, opis `register.py`, `main.py`, 2–3 listingi kodu | 1.5 h |

**Diagram do zrobienia:**  
`Enrollment → Ekstrakcja cech → Baza embeddingów → Probe → Porównanie 1:N → Fuzja → Decyzja`

---

## Kamil — rozdziały analizy i głosu

| Rozdział | Zawartość | Szac. czas |
|----------|-----------|------------|
| 3. Analiza istniejących rozwiązań | Min. 3 systemy (np. Face ID, speaker recognition, system komercyjny) + czym MultiVerify się wyróżnia | 1.5 h |
| 5. Metody — część głos | MFCC, librosa, uzasadnienie wyboru | 45 min |
| 7. Wyniki i eksperymenty | Tabele FAR/FRR/accuracy, wykresy z Fazy 1, interpretacja | 2 h |
| 7. Bezpieczeństwo | Spoofing zdjęciem, replay głosu, atak jedną modalnością | 45 min |
| 8. Wnioski | Co działa, co poprawić, zastosowania | 30 min |
| 9. Bibliografia | Min. 5–8 pozycji (DeepFace, MFCC, multimodal biometrics) | 30 min |

### W rozdziale „Wyniki” — obowiązkowo opisać:
- [ ] Porównanie: twarz sama vs głos sam vs fuzja
- [ ] Czy fuzja poprawia wynik względem pojedynczej modalności
- [ ] Wpływ progu `threshold`
- [ ] Wpływ wag (50/50 vs 60/40 vs 70/30)
- [ ] Co działa dobrze / co nie (szczerze)

---

## Wspólne — dokończenie dokumentu (~1 h)

- [ ] Kacper: spis treści, numeracja rysunków/tabel
- [ ] Kamil: spójność terminologii (FAR, FRR, embedding, fuzja)
- [ ] Razem: przeczytać całość, poprawić błędy
- [ ] Wygenerować PDF

---

# FAZA 3 — Oddanie projektu

## Kacper (~45 min)

- [ ] Spakować ZIP:
  ```
  MultiVerify.zip
  ├── dokumentacja.pdf
  ├── dokumentacja/          (źródła LaTeX)
  ├── kod/                   (cały projekt bez .venv, __pycache__)
  ├── README.md
  └── data/users/            (opcjonalnie 1 użytkownik przykładowy LUB instrukcja w README)
  ```
- [ ] Sprawdzić ZIP na czystym folderze — czy da się uruchomić od zera
- [ ] Wgrać na platformę przed deadline

## Kamil (~30 min)

- [ ] Przygotować krótki opis wkładu każdej osoby (na wypadek pytań prowadzącego):
  - **Kacper:** architektura, twarz, fuzja, main/register, rozdziały 1–2, 4–6
  - **Kamil:** głos, eksperymenty, metryki, wykresy, rozdziały 3, 5 (głos), 7–9
- [ ] Zrobić 2–3 screenshoty działania systemu do załącznika PDF

---

# Harmonogram (propozycja)

| Kiedy | Co |
|-------|-----|
| **Dziś wieczór** | Faza 0 + start Fazy 1 (register, CLI, pierwsze eksperymenty) |
| **Jutro rano** | Faza 1 done + start LaTeX (każdy swoje rozdziały) |
| **Jutro popołudnie** | LaTeX done, wykresy, PDF, ZIP |
| **Przed 23:59 12.06** | Upload na platformę |

---

# Checklist przed oddaniem (oboje)

- [ ] `python register.py` — działa
- [ ] `python main.py --face ... --voice ...` — działa
- [ ] `python scripts/run_experiments.py` — CSV powstaje
- [ ] Metryki FAR/FRR policzone i w PDF
- [ ] Min. 2 wykresy w PDF
- [ ] README kompletny
- [ ] `pytest` — green
- [ ] PDF ma wszystkie wymagane rozdziały z wytycznych
- [ ] ZIP zawiera PDF + LaTeX + kod
- [ ] Każdy zna swój wkład i potrafi wyjaśnić swój moduł

---

# Szybka pomoc — komendy

```bash
# Środowisko
pip install -r requirements.txt

# Rejestracja (po wrzuceniu plików)
python register.py

# Identyfikacja (po implementacji CLI)
python main.py --face data/users/kacper/face_3.jpg --voice data/users/kacper/voice_3.wav

# Eksperymenty
python scripts/run_experiments.py

# Testy
pytest
```

---

# Kontakt / blokery

Jeśli coś nie działa, zgłaszajcie od razu:

| Problem | Kto pomaga |
|---------|------------|
| DeepFace / błąd modelu | Kacper |
| Librosa / audio nie wczytuje się | Kamil |
| Fusion / main.py | Kacper |
| Metryki / wykresy | Kamil |
| LaTeX / PDF | ten, kto pisze dany rozdział |

---

*Ostatnia aktualizacja planu: 11.06.2026*
