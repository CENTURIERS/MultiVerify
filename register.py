import os

from src.modalities.face.face_modality import FaceModality
from src.modalities.voice.voice_modality import VoiceModality

USERS_DIR = "data/users"

def register_user(username):
    """
    Rejestruje użytkownika — wczytuje jego zdjęcia i nagrania z folderu,
    wyciąga cechy (embeddingi) i zapisuje je do późniejszego porównania.
    """
    user_dir = os.path.join(USERS_DIR, username)

    if not os.path.exists(user_dir):
        print(f"Nie znaleziono folderu dla użytkownika: {user_dir}")
        print("Stwórz folder i wrzuć tam zdjęcia (face_1.jpg itd.) oraz nagrania (voice_1.wav itd.).")
        return

    # Znajdź wszystkie zdjęcia twarzy i nagrania głosu w folderze użytkownika
    face_files = [f for f in os.listdir(user_dir) if f.startswith("face_") and f.endswith((".jpg", ".png"))]
    voice_files = [f for f in os.listdir(user_dir) if f.startswith("voice_") and f.endswith((".wav", ".mp3"))]

    print(f"=== Rejestracja użytkownika: {username} ===")
    print(f"Znaleziono {len(face_files)} zdjęć twarzy i {len(voice_files)} nagrań głosu.")

    if len(face_files) == 0 and len(voice_files) == 0:
        print("Brak plików do przetworzenia! Wrzuć zdjęcia i nagrania do folderu.")
        return

    face_system = FaceModality()
    voice_system = VoiceModality()

    # Wyciągamy cechy z każdego zdjęcia twarzy
    face_features = []
    for face_file in face_files:
        full_path = os.path.join(user_dir, face_file)
        features = face_system.extract_features(full_path)
        face_features.append(features)
        print(f"  Przetworzono: {face_file}")

    # Wyciągamy cechy z każdego nagrania głosu
    voice_features = []
    for voice_file in voice_files:
        full_path = os.path.join(user_dir, voice_file)
        features = voice_system.extract_features(full_path)
        voice_features.append(features)
        print(f"  Przetworzono: {voice_file}")

    print(f"\nZarejestrowano {username}: {len(face_features)} wzorców twarzy, {len(voice_features)} wzorców głosu.")
    print("(Na razie to stuby — prawdziwe embeddingi pojawią się po implementacji Kamila)\n")

    # Kamil: tutaj w przyszłości zapis embeddingów do plików .npy
    # np. np.save(os.path.join(user_dir, "face_embeddings.npy"), face_features)

    return {"face_features": face_features, "voice_features": voice_features}


def list_users():
    """Wypisuje wszystkich zarejestrowanych użytkowników (foldery w data/users/)."""
    if not os.path.exists(USERS_DIR):
        print("Brak folderu data/users/!")
        return []

    users = [name for name in os.listdir(USERS_DIR) if os.path.isdir(os.path.join(USERS_DIR, name))]
    print(f"Zarejestrowani użytkownicy ({len(users)}): {', '.join(users)}")
    return users


if __name__ == "__main__":
    print("=== MultiVerify — Rejestracja ===\n")
    users = list_users()
    for user in users:
        register_user(user)
