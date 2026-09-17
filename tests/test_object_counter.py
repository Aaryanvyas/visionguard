"""Tests for src/object_counter.py."""

import pytest
import cv2
from src.object_counter import ObjectCounter
from src.config import SAMPLES_DIR

def test_object_counter_initialization():
    counter = ObjectCounter(min_area=250)
    assert counter.min_area == 250

def test_object_counter_blank_image_finds_zero(blank_image):
    counter = ObjectCounter()
    objects, thresh = counter.count(blank_image)
    assert len(objects) == 0

def test_object_counter_exact_count_synthetic_4_shapes(synthetic_4_shapes_path):
    counter = ObjectCounter(min_area=300)
    img = cv2.imread(str(synthetic_4_shapes_path))
    objects, _ = counter.count(img)
    assert len(objects) == 4, f"Expected exactly 4 shapes, got {len(objects)}"

def test_object_counter_exact_count_sample_7_shapes():
    shapes_path = SAMPLES_DIR / "shapes.png"
    assert shapes_path.exists()
    counter = ObjectCounter(min_area=300)
    img = cv2.imread(str(shapes_path))
    objects, _ = counter.count(img)
    assert len(objects) == 7, f"Expected exactly 7 shapes, got {len(objects)}"

def test_object_counter_end_to_end_with_db(synthetic_4_shapes_path, temp_db, tmp_path):
    out_path = tmp_path / "counted.png"
    counter = ObjectCounter(min_area=300)
    result = counter.process_image(
        str(synthetic_4_shapes_path),
        output_path=str(out_path),
        log_to_db=True,
        db_path=temp_db
    )
    assert result["session_id"] is not None
    assert result["object_count"] == 4
    assert result["avg_area"] > 0
    assert out_path.exists()
