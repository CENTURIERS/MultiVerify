from src.modalities.base import BiometricModality

class VoiceModality(BiometricModality):
    """
    Szkielet dla modalności rozpoznawania głosu.
    Kamil uzupełni to potem o librosa (MFCC) i podobieństwo kosinusowe.
    """
    
    def extract_features(self, file_path):
        print(f"[Voice] Wyciągam cechy z pliku: {file_path}")
        # Na razie zwracamy sztuczną listę jako wektor cech głosu
        return [0.9, 0.8, 0.7, 0.6, 0.5]

    def verify(self, features_a, features_b):
        print("[Voice] Porównuję cechy głosu...")
        # Zwracamy stałą wartość (0.72 oznacza umiarkowane podobieństwo głosu)
        return 0.72
