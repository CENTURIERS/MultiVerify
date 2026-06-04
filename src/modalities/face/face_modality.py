from src.modalities.base import BiometricModality

class FaceModality(BiometricModality):
    """
    Szkielet dla modalności rozpoznawania twarzy.
    Kamil uzupełni to potem o prawdziwego DeepFace'a.
    """
    
    def extract_features(self, file_path):
        print(f"[Face] Wyciągam cechy z pliku: {file_path}")
        # Na razie zwracamy sztuczną listę jako wektor cech twarzy
        return [0.1, 0.2, 0.3, 0.4, 0.5]

    def verify(self, features_a, features_b):
        print("[Face] Porównuję cechy twarzy...")
        # Zwracamy stałą wartość (0.85 oznacza wysokie podobieństwo twarzy)
        return 0.85
