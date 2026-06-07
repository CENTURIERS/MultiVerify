import os
import numpy as np

from src.modalities.face.face_modality import FaceModality
from src.modalities.voice.voice_modality import VoiceModality
from src.fusion.fusion_engine import FusionEngine

USERS_DIR = "data/users"

def best_score(system, new_features, saved_features):
    """
    Porownuje nowe cechy z kilkoma wzorcami i bierze najlepszy wynik.
    """
    scores = []
    for features in saved_features:
        scores.append(system.verify(new_features, features))

    if len(scores) == 0:
        return 0.0

    return max(scores)

def identify(face_file, voice_file):
    """
    Identyfikacja 1:N — bierze nowe zdjecie i nagranie,
    porownuje ze wszystkimi uzytkownikami w bazie i mowi kto to jest.
    """
    print("=== System Multimodalny MultiVerify ===\n")
    print(f"Nowe zdjecie:   {face_file}")
    print(f"Nowe nagranie:  {voice_file}\n")

    face_system = FaceModality()
    voice_system = VoiceModality()
    fusion_system = FusionEngine(face_weight=0.6, voice_weight=0.4, threshold=0.7)

    # Wyciagamy cechy z nowych danych (osoba probujaca sie zalogowac)
    new_face_features = face_system.extract_features(face_file)
    new_voice_features = voice_system.extract_features(voice_file)

    # Przechodzimy po wszystkich uzytkownikach w bazie
    users = [name for name in os.listdir(USERS_DIR) if os.path.isdir(os.path.join(USERS_DIR, name))]

    if len(users) == 0:
        print("Baza uzytkownikow jest pusta! Najpierw zarejestruj kogos (register.py).")
        return

    print(f"Porownuje z {len(users)} uzytkownikami w bazie...\n")

    results = []

    for username in users:
        user_dir = os.path.join(USERS_DIR, username)

        # Szukamy zapisanych embeddingow, a jesli ich nie ma to plikow z danymi
        face_embeddings_path = os.path.join(user_dir, "face_embeddings.npy")
        voice_embeddings_path = os.path.join(user_dir, "voice_embeddings.npy")

        face_files = [f for f in os.listdir(user_dir) if f.startswith("face_") and f.endswith((".jpg", ".png"))]
        voice_files = [f for f in os.listdir(user_dir) if f.startswith("voice_") and f.endswith((".wav", ".mp3"))]

        if os.path.exists(face_embeddings_path):
            face_features = np.load(face_embeddings_path, allow_pickle=True)
            face_score = best_score(face_system, new_face_features, face_features)
        elif face_files:
            face_scores = []
            for face_name in face_files:
                ref_face_path = os.path.join(user_dir, face_name)
                ref_face_features = face_system.extract_features(ref_face_path)
                face_scores.append(face_system.verify(new_face_features, ref_face_features))
            face_score = max(face_scores)
        else:
            face_score = 0.0

        if os.path.exists(voice_embeddings_path):
            voice_features = np.load(voice_embeddings_path, allow_pickle=True)
            voice_score = best_score(voice_system, new_voice_features, voice_features)
        elif voice_files:
            voice_scores = []
            for voice_name in voice_files:
                ref_voice_path = os.path.join(user_dir, voice_name)
                ref_voice_features = voice_system.extract_features(ref_voice_path)
                voice_scores.append(voice_system.verify(new_voice_features, ref_voice_features))
            voice_score = max(voice_scores)
        else:
            voice_score = 0.0

        # Fuzja wynikow
        fusion_result = fusion_system.fuse(face_score, voice_score)

        results.append({
            "username": username,
            "face_score": face_score,
            "voice_score": voice_score,
            "final_score": fusion_result["final_score"],
            "access_granted": fusion_result["access_granted"]
        })

        print(f"  {username}: twarz={face_score:.2f}, glos={voice_score:.2f}, "
              f"fuzja={fusion_result['final_score']:.4f} "
              f"{'-> DOPASOWANIE' if fusion_result['access_granted'] else ''}")

    # Szukamy najlepszego dopasowania
    best_match = max(results, key=lambda r: r["final_score"])

    print("\n=== WYNIK IDENTYFIKACJI ===")
    if best_match["access_granted"]:
        print(f"Zidentyfikowano jako: {best_match['username']} (wynik: {best_match['final_score']:.4f})")
        print("Dostep PRZYZNANY")
    else:
        print("Nie rozpoznano zadnego uzytkownika z bazy.")
        print("Dostep ODMOWIONY")
    print("===========================")

    return best_match


if __name__ == "__main__":
    # Przykladowe pliki wejsciowe (na etapie stubbow nie musza istniec)
    identify(
        face_file="nowe_zdjecie.jpg",
        voice_file="nowe_nagranie.wav"
    )
