"""Tests for src/face_detection.py."""

import pytest
import numpy as np
from src.face_detection import FaceDetector
from src.config import SAMPLES_DIR

def test_face_detection_blank_image_finds_zero(blank_image):
    detector = FaceDetector()
    detections = detector.detect(blank_image)
    assert len(detections) == 0

def test_face_detection_sample_portrait_finds_face():
    portrait_path = SAMPLES_DIR / "portrait.jpg"
    assert portrait_path.exists(), "portrait.jpg missing from samples"
    detector = FaceDetector()
    import cv2
    img = cv2.imread(str(portrait_path))
    detections = detector.detect(img)
    assert len(detections) >= 1
    assert detections[0]["label"] == "face"
    assert len(detections[0]["box"]) == 4

def test_face_detection_annotation_modifies_image(blank_image):
    detector = FaceDetector()
    fake_dets = [{"label": "face", "box": (10, 10, 50, 50), "confidence": 1.0}]
    annotated = detector.annotate(blank_image, fake_dets)
    assert not np.array_equal(blank_image, annotated)

def test_face_detection_invalid_path_raises():
    detector = FaceDetector()
    with pytest.raises(FileNotFoundError):
        detector.process_image("non_existent_path.jpg", log_to_db=False)

def test_face_detection_end_to_end_with_db(temp_db, tmp_path):
    portrait_path = SAMPLES_DIR / "portrait.jpg"
    out_path = tmp_path / "faces_out.jpg"
    detector = FaceDetector()
    result = detector.process_image(
        str(portrait_path),
        output_path=str(out_path),
        log_to_db=True,
        db_path=temp_db
    )
    assert result["session_id"] is not None
    assert result["face_count"] >= 1
    assert out_path.exists()
