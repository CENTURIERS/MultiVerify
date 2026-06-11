# MultiVerify

System multimodalnej identyfikacji użytkownika na podstawie **twarzy** i **głosu**.  
Projekt na przedmiot *Biometryczne systemy zabezpieczeń* — temat: *Systemy multimodalne (zaawansowane)*.

## Wymagania

- **Python 3.11 lub 3.12** (nie używaj 3.14 — TensorFlow/DeepFace nie działają)
- Windows / Linux / macOS
- Połączenie z internetem przy **pierwszym** uruchomieniu (pobranie modelu Facenet)

## Instalacja

```powershell
# 1. Wejdź do folderu projektu
cd MultiVerify

# 2. Utwórz i aktywuj środowisko wirtualne
py -3.12 -m venv .venv
.\.venv\Scripts\Activate

# 3. Zainstaluj zależności
pip install -r requirements.txt
```

## Struktura danych

Dla każdego użytkownika utwórz folder w `data/users/`:

```
data/users/
├── kacper/
│   ├── face_1.jpg
│   ├── face_2.jpg
│   ├── face_3.jpg
│   ├── voice_1.mp3   (lub .wav)
│   ├── voice_2.mp3
│   └── voice_3.mp3
└── kamil/
    └── ...
```

**Konwencja nazw:**
- Twarz: `face_*.jpg` lub `face_*.png`
- Głos: `voice_*.wav` lub `voice_*.mp3` (WAV jest najbardziej niezawodny)

**Git:** w repozytorium są tylko puste foldery użytkowników (`.gitkeep`). Zdjęcia, nagrania i pliki `.npy` nie trafiają do gita — dodaj je lokalnie przed `register.py`.

## Uruchomienie

### 1. Rejestracja użytkowników (enrollment)

Przetwarza wszystkie foldery w `data/users/` i zapisuje embeddingi:

```powershell
python register.py
```

Powstaną pliki `face_embeddings.npy` i `voice_embeddings.npy` w każdym folderze użytkownika.

### 2. Identyfikacja (logowanie 1:N)

Podaj **nowe** zdjęcie i nagranie (probe) — najlepiej `face_3` + `voice_3`:

```powershell
python main.py --face data/users/kacper/face_3.jpg --voice data/users/kacper/voice_3.mp3
```

Opcjonalne parametry:

```powershell
python main.py --face ... --voice ... --threshold 0.85 --strategy weighted
python main.py --face ... --voice ... --strategy and
```

| Parametr | Domyślnie | Opis |
|----------|-----------|------|
| `--face` | — | Ścieżka do zdjęcia probe |
| `--voice` | — | Ścieżka do nagrania probe |
| `--threshold` | `0.7` | Próg akceptacji |
| `--strategy` | `weighted` | `weighted` (suma ważona 60/40) lub `and` (obie modalności muszą przejść próg) |

### 3. Eksperymenty (porównanie wariantów fuzji)

```powershell
python scripts/run_experiments.py
```

Wynik: `docs/experiment_results.csv`

### 4. Testy jednostkowe

```powershell
pytest
```

## Jak działa system

```
Enrollment:  zdjęcia + nagrania → ekstrakcja cech → baza embeddingów (.npy)
Identyfikacja: probe (twarz + głos) → porównanie z każdym użytkownikiem → fuzja → decyzja
```

- **Twarz:** DeepFace (model Facenet) → embedding + cosine similarity
- **Głos:** MFCC (librosa) → cosine similarity
- **Fuzja:** late fusion — suma ważona lub reguła AND

## Struktura projektu

```
MultiVerify/
├── main.py              # identyfikacja 1:N
├── register.py          # rejestracja użytkowników
├── src/
│   ├── modalities/      # twarz, głos
│   └── fusion/          # silnik fuzji
├── scripts/
│   └── run_experiments.py
├── data/users/          # dane biometryczne
└── tests/
```

## Rozwiązywanie problemów

| Problem | Rozwiązanie |
|---------|-------------|
| `tensorflow` nie instaluje się | Użyj Pythona 3.12, nie 3.14 |
| Błąd przy MP3 | Przekonwertuj na WAV lub zainstaluj `ffmpeg` |
| `ImgNotFound` | Sprawdź ścieżkę w `--face` / `--voice` |
| Pierwsze uruchomienie wolne | DeepFace pobiera model Facenet (~90 MB) |

## Autorzy

Kacper + Kamil — projekt zespołowy BSZ.
