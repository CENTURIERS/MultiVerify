class FusionEngine:
    """
    Silnik łączący (fuzujący) wyniki z różnych modalności.
    Oblicza sumę ważoną i podejmuje decyzję.
    """
    
    def __init__(self, face_weight=0.6, voice_weight=0.4, threshold=0.7):
        # Sprawdzamy czy wagi sumują się do 1.0 (inaczej wynik nie miałby sensu)
        if round(face_weight + voice_weight, 2) != 1.0:
            raise ValueError(f"Wagi muszą sumować się do 1.0, a masz: {face_weight + voice_weight}")
        
        self.face_weight = face_weight
        self.voice_weight = voice_weight
        self.threshold = threshold

    def fuse(self, face_score, voice_score):
        """
        Oblicza średnią ważoną i sprawdza, czy przekracza próg (threshold).
        Zwraca słownik z wynikiem i decyzją True/False.
        """
        # Suma ważona: wynik_twarz * waga_twarz + wynik_glos * waga_glos
        final_score = (face_score * self.face_weight) + (voice_score * self.voice_weight)
        
        # Jeśli wynik jest większy lub równy progu, to przyznajemy dostęp
        access_granted = final_score >= self.threshold
        
        return {
            "final_score": round(final_score, 4),
            "access_granted": access_granted
        }
