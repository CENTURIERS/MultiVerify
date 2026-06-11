import pytest

from src.fusion.fusion_engine import FusionEngine


def test_fusion_grants_access_above_threshold():
    fusion = FusionEngine(face_weight=0.6, voice_weight=0.4, threshold=0.7)

    result = fusion.fuse(face_score=0.9, voice_score=0.8)

    assert result["final_score"] == pytest.approx(0.86)
    assert result["access_granted"] is True


def test_fusion_blocks_access_below_threshold():
    fusion = FusionEngine(face_weight=0.5, voice_weight=0.5, threshold=0.7)

    result = fusion.fuse(face_score=0.5, voice_score=0.6)

    assert result["final_score"] == pytest.approx(0.55)
    assert result["access_granted"] is False


def test_fusion_checks_weights_sum():
    with pytest.raises(ValueError):
        FusionEngine(face_weight=0.7, voice_weight=0.7, threshold=0.7)


def test_fusion_weight_variants():
    scores = (0.8, 0.5)

    result_50_50 = FusionEngine(0.5, 0.5).fuse(*scores)
    result_60_40 = FusionEngine(0.6, 0.4).fuse(*scores)
    result_70_30 = FusionEngine(0.7, 0.3).fuse(*scores)

    assert result_50_50["final_score"] == pytest.approx(0.65)
    assert result_60_40["final_score"] == pytest.approx(0.68)
    assert result_70_30["final_score"] == pytest.approx(0.71)


def test_fusion_and_grants_access_when_both_modalities_pass():
    fusion = FusionEngine(threshold=0.7, strategy="and")

    result = fusion.fuse(face_score=0.9, voice_score=0.8)

    assert result["final_score"] == pytest.approx(0.8)
    assert result["access_granted"] is True
    assert result["strategy"] == "and"


def test_fusion_and_blocks_when_one_modality_fails():
    fusion = FusionEngine(threshold=0.7, strategy="and")

    result = fusion.fuse(face_score=0.9, voice_score=0.6)

    assert result["final_score"] == pytest.approx(0.6)
    assert result["access_granted"] is False


def test_fusion_rejects_unknown_strategy():
    with pytest.raises(ValueError):
        FusionEngine(strategy="invalid")
