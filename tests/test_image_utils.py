"""Tests for src/image_utils.py validation and filter registry."""

import pytest
import numpy as np
from pathlib import Path
from src.image_utils import (
    validate_image_path, load_image, save_image,
    to_grayscale, apply_gaussian_blur, apply_canny_edges,
    apply_histogram_equalization, apply_adaptive_threshold,
    apply_sharpen, apply_filter, draw_bounding_box
)

def test_validate_image_path_valid(blank_image_path):
    validated = validate_image_path(str(blank_image_path))
    assert validated.exists()

def test_validate_image_path_nonexistent():
    with pytest.raises(FileNotFoundError):
        validate_image_path("non_existent_file.png")

def test_validate_image_path_invalid_extension(tmp_path):
    fake_txt = tmp_path / "test.txt"
    fake_txt.write_text("hello")
    with pytest.raises(ValueError, match="Unsupported image format"):
        validate_image_path(str(fake_txt))

def test_grayscale_filter_shape():
    rgb = np.full((100, 100, 3), 128, dtype=np.uint8)
    gray = to_grayscale(rgb)
    assert gray.shape == (100, 100)
    assert gray.dtype == np.uint8

def test_gaussian_blur_dtype_and_shape():
    np.random.seed(42)
    img = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
    blurred = apply_gaussian_blur(img, ksize=(7, 7), sigma=1.5)
    assert blurred.shape == img.shape
    assert blurred.dtype == np.uint8

def test_canny_edges_binary_output():
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    img[25:75, 25:75] = 255
    edges = apply_canny_edges(img, 50, 150)
    assert edges.shape == (100, 100)
    unique_vals = set(np.unique(edges))
    assert unique_vals.issubset({0, 255})
    assert 255 in unique_vals  # Found square edges

def test_histogram_equalization_bgr():
    dark_img = np.full((100, 100, 3), 40, dtype=np.uint8)
    eq = apply_histogram_equalization(dark_img)
    assert eq.shape == dark_img.shape
    assert eq.dtype == np.uint8

def test_adaptive_threshold_binary():
    np.random.seed(123)
    img = np.random.randint(50, 200, (100, 100, 3), dtype=np.uint8)
    thresh = apply_adaptive_threshold(img, block_size=11, c=2)
    assert thresh.shape == (100, 100)
    assert set(np.unique(thresh)).issubset({0, 255})

def test_sharpen_filter():
    img = np.full((50, 50, 3), 100, dtype=np.uint8)
    sharp = apply_sharpen(img)
    assert sharp.shape == img.shape
    assert sharp.dtype == np.uint8

def test_invalid_filter_name_raises():
    img = np.zeros((20, 20, 3), dtype=np.uint8)
    with pytest.raises(ValueError, match="Unknown filter"):
        apply_filter(img, "non_existent_filter")

def test_draw_bounding_box():
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    annotated = draw_bounding_box(img, (10, 10, 40, 40), label="test", color=(0, 255, 0))
    assert annotated.shape == img.shape
    # Check that pixels changed from all zeros
    assert annotated.sum() > 0
