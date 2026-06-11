import csv
import os
import sys

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_DIR)

from src.fusion.fusion_engine import FusionEngine
from src.modalities.face.face_modality import FaceModality
from src.modalities.voice.voice_modality import VoiceModality


USERS_DIR = "data/users"
OUTPUT_FILE = "docs/experiment_results.csv"

VARIANTS = [
    ("face_only", 1.0, 0.0),
    ("voice_only", 0.0, 1.0),
    ("fusion_50_50", 0.5, 0.5),
    ("fusion_60_40", 0.6, 0.4),
    ("fusion_70_30", 0.7, 0.3),
]


def find_files(user_dir, prefix, extensions):
    files = [
        os.path.join(user_dir, name)
        for name in os.listdir(user_dir)
        if name.startswith(prefix) and name.endswith(extensions)
    ]
    return sorted(files)


def best_score(system, new_features, saved_features):
    scores = []
    for features in saved_features:
        scores.append(system.verify(new_features, features))

    if len(scores) == 0:
        return 0.0

    return max(scores)


def split_enrollment_and_probe(user_dir, kind):
    if kind == "face":
        files = find_files(user_dir, "face_", (".jpg", ".png"))
    else:
        files = find_files(user_dir, "voice_", (".wav", ".mp3"))

    if len(files) < 2:
        return [], None

    return files[:-1], files[-1]


def extract_features_for_files(system, files):
    features = []
    for file_path in files:
        features.append(system.extract_features(file_path))

    return features


def get_users():
    if not os.path.exists(USERS_DIR):
        return []

    users = []
    for name in os.listdir(USERS_DIR):
        path = os.path.join(USERS_DIR, name)
        if os.path.isdir(path):
            users.append(name)

    return users


def run_experiments():
    users = get_users()
    face_system = FaceModality()
    voice_system = VoiceModality()

    if len(users) == 0:
        print("Brak uzytkownikow w data/users.")
        return

    references = {}
    for user in users:
        user_dir = os.path.join(USERS_DIR, user)
        face_enrollment, face_probe = split_enrollment_and_probe(user_dir, "face")
        voice_enrollment, voice_probe = split_enrollment_and_probe(user_dir, "voice")

        references[user] = {
            "face": extract_features_for_files(face_system, face_enrollment),
            "voice": extract_features_for_files(voice_system, voice_enrollment),
            "face_probe": face_probe,
            "voice_probe": voice_probe,
        }

    rows = []

    for probe_user in users:
        face_probe = references[probe_user]["face_probe"]
        voice_probe = references[probe_user]["voice_probe"]

        if face_probe is None or voice_probe is None:
            print(f"Pomijam {probe_user}, bo potrzeba minimum 2 zdjec i 2 nagran.")
            continue

        probe_face = face_system.extract_features(face_probe)
        probe_voice = voice_system.extract_features(voice_probe)

        for candidate in users:
            face_score = best_score(face_system, probe_face, references[candidate]["face"])
            voice_score = best_score(voice_system, probe_voice, references[candidate]["voice"])

            for variant_name, face_weight, voice_weight in VARIANTS:
                fusion = FusionEngine(face_weight=face_weight, voice_weight=voice_weight, threshold=0.7)
                result = fusion.fuse(face_score, voice_score)
                expected_match = probe_user == candidate
                correct = result["access_granted"] == expected_match

                rows.append({
                    "probe_user": probe_user,
                    "candidate_user": candidate,
                    "variant": variant_name,
                    "face_score": round(face_score, 4),
                    "voice_score": round(voice_score, 4),
                    "final_score": result["final_score"],
                    "accepted": result["access_granted"],
                    "expected_match": expected_match,
                    "correct": correct,
                })

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "probe_user",
            "candidate_user",
            "variant",
            "face_score",
            "voice_score",
            "final_score",
            "accepted",
            "expected_match",
            "correct",
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Zapisano wyniki: {OUTPUT_FILE}")
    print(f"Liczba wierszy: {len(rows)}")


if __name__ == "__main__":
    run_experiments()
