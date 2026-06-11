class FusionEngine:
    """
    Silnik łączący (fuzujący) wyniki z różnych modalności.
    Obsługuje late fusion (suma ważona) oraz regułę AND.
    """

    STRATEGIES = ("weighted", "and")

    def __init__(
        self,
        face_weight=0.6,
        voice_weight=0.4,
        threshold=0.7,
        strategy="weighted",
    ):
        if round(face_weight + voice_weight, 2) != 1.0:
            raise ValueError(f"Wagi muszą sumować się do 1.0, a masz: {face_weight + voice_weight}")

        if strategy not in self.STRATEGIES:
            raise ValueError(f"Nieznana strategia: {strategy}. Dostępne: {self.STRATEGIES}")

        self.face_weight = face_weight
        self.voice_weight = voice_weight
        self.threshold = threshold
        self.strategy = strategy

    def fuse(self, face_score, voice_score):
        """
        Łączy wyniki modalności i zwraca decyzję dostępu.

        weighted: score = w_f * face + w_v * voice, dostęp gdy score >= threshold
        and:      dostęp gdy face >= threshold i voice >= threshold,
                  score = min(face, voice) — do rankingu 1:N
        """
        if self.strategy == "and":
            final_score = min(face_score, voice_score)
            access_granted = face_score >= self.threshold and voice_score >= self.threshold
        else:
            final_score = (face_score * self.face_weight) + (voice_score * self.voice_weight)
            access_granted = final_score >= self.threshold

        return {
            "final_score": round(final_score, 4),
            "access_granted": access_granted,
            "strategy": self.strategy,
        }
