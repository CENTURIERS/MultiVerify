from src.modalities.base import BiometricModality
import numpy as np

class FaceModality(BiometricModality):
    """
    Modalność rozpoznawania twarzy.
    Do wyciągania embeddingów używa DeepFace.
    """

    def __init__(self, model_name="Facenet"):
        self.model_name = model_name
    
    def extract_features(self, file_path):
        print(f"[Face] Wyciągam cechy z pliku: {file_path}")

        from deepface import DeepFace

        result = DeepFace.represent(
            img_path=file_path,
            model_name=self.model_name,
            enforce_detection=False
        )

        if isinstance(result, list):
            embedding = result[0]["embedding"]
        else:
            embedding = result["embedding"]

        return np.array(embedding, dtype=float)

    def verify(self, features_a, features_b):
        print("[Face] Porównuję cechy twarzy...")

        vec_a = np.array(features_a, dtype=float).ravel()
        vec_b = np.array(features_b, dtype=float).ravel()

        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)

        if norm_a == 0 or norm_b == 0:
            return 0.0

        similarity = float(np.dot(vec_a, vec_b) / (norm_a * norm_b))
        return max(0.0, min(1.0, similarity))
