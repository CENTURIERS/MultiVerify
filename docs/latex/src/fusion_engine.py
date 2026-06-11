def fuse(self, face_score, voice_score):
    if self.strategy == "and":
        final_score = min(face_score, voice_score)
        access_granted = (
            face_score >= self.threshold
            and voice_score >= self.threshold
        )
    else:
        final_score = (
            face_score * self.face_weight
            + voice_score * self.voice_weight
        )
        access_granted = final_score >= self.threshold

    return {
        "final_score": round(final_score, 4),
        "access_granted": access_granted,
        "strategy": self.strategy,
    }
