import os

from src.modalities.face.face_modality import FaceModality
from src.modalities.voice.voice_modality import VoiceModality
from src.fusion.fusion_engine import FusionEngine

USERS_DIR = "data/users"

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

        # Szukamy zdjec i nagran tego uzytkownika
        face_files = [f for f in os.listdir(user_dir) if f.startswith("face_") and f.endswith((".jpg", ".png"))]
        voice_files = [f for f in os.listdir(user_dir) if f.startswith("voice_") and f.endswith((".wav", ".mp3"))]

        # Porownujemy twarz z pierwszym zdjeciem uzytkownika (na razie uproszczone)
        if face_files:
            ref_face_path = os.path.join(user_dir, face_files[0])
            ref_face_features = face_system.extract_features(ref_face_path)
            face_score = face_system.verify(new_face_features, ref_face_features)
        else:
            face_score = 0.0

        # Porownujemy glos z pierwszym nagraniem uzytkownika
        if voice_files:
            ref_voice_path = os.path.join(user_dir, voice_files[0])
            ref_voice_features = voice_system.extract_features(ref_voice_path)
            voice_score = voice_system.verify(new_voice_features, ref_voice_features)
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
