import pytest

from src.modalities.face.face_modality import FaceModality
from src.modalities.voice.voice_modality import VoiceModality


def test_face_similarity_for_same_vectors():
    face = FaceModality()

    wynik = face.verify([1, 2, 3], [1, 2, 3])

    assert wynik == pytest.approx(1.0)


def test_face_similarity_for_different_vectors():
    face = FaceModality()

    wynik = face.verify([1, 0, 0], [0, 1, 0])

    assert wynik == pytest.approx(0.0)


def test_voice_similarity_for_same_vectors():
    voice = VoiceModality()

    wynik = voice.verify([4, 5, 6], [4, 5, 6])

    assert wynik == pytest.approx(1.0)


def test_voice_similarity_for_zero_vector():
    voice = VoiceModality()

    wynik = voice.verify([0, 0, 0], [1, 2, 3])

    assert wynik == pytest.approx(0.0)
