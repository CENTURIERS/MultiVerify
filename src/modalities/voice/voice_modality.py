from src.modalities.base import BiometricModality
import numpy as np

class VoiceModality(BiometricModality):
    """
    Modalność rozpoznawania głosu.
    Wyciąga proste cechy MFCC z nagrania.
    """

    def __init__(self, sample_rate=16000, n_mfcc=13):
        self.sample_rate = sample_rate
        self.n_mfcc = n_mfcc
    
    def extract_features(self, file_path):
        print(f"[Voice] Wyciągam cechy z pliku: {file_path}")

        import librosa

        audio, sr = librosa.load(file_path, sr=self.sample_rate, mono=True)
        mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=self.n_mfcc)

        avg = np.mean(mfcc, axis=1)
        std = np.std(mfcc, axis=1)

        return np.concatenate([avg, std])

    def verify(self, features_a, features_b):
        print("[Voice] Porównuję cechy głosu...")

        vec_a = np.array(features_a, dtype=float).ravel()
        vec_b = np.array(features_b, dtype=float).ravel()

        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)

        if norm_a == 0 or norm_b == 0:
            return 0.0

        similarity = float(np.dot(vec_a, vec_b) / (norm_a * norm_b))
        return max(0.0, min(1.0, similarity))
