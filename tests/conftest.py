"""Shared Pytest fixtures for VisionGuard test suite."""

import pytest
import numpy as np
import cv2
import tempfile
from pathlib import Path
from src.database import init_db

@pytest.fixture
def temp_db(tmp_path):
    """Provides a fresh, isolated SQLite database file for each test."""
    db_file = tmp_path / "test_visionguard.db"
    init_db(db_file)
    return db_file

@pytest.fixture
def blank_image():
    """Returns a pure black 400x400 3-channel test image."""
    return np.zeros((400, 400, 3), dtype=np.uint8)

@pytest.fixture
def blank_image_path(tmp_path, blank_image):
    """Saves a blank image to a temporary file path."""
    p = tmp_path / "blank.png"
    cv2.imwrite(str(p), blank_image)
    return p

@pytest.fixture
def synthetic_4_shapes_path(tmp_path):
    """Creates a temporary image containing exactly 4 well-separated black shapes."""
    img = np.ones((500, 500, 3), dtype=np.uint8) * 255
    # Shape 1: Top-Left square
    cv2.rectangle(img, (50, 50), (120, 120), (0, 0, 0), -1)
    # Shape 2: Top-Right circle
    cv2.circle(img, (380, 80), 40, (0, 0, 0), -1)
    # Shape 3: Bottom-Left circle
    cv2.circle(img, (100, 380), 35, (0, 0, 0), -1)
    # Shape 4: Bottom-Right rectangle
    cv2.rectangle(img, (320, 320), (420, 400), (0, 0, 0), -1)

    p = tmp_path / "four_shapes.png"
    cv2.imwrite(str(p), img)
    return p

@pytest.fixture
def synthetic_moving_video_path(tmp_path):
    """Creates a small 40-frame synthetic video with a moving circle."""
    p = tmp_path / "moving_test.mp4"
    w, h = 320, 240
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(p), fourcc, 20.0, (w, h))
    if not writer.isOpened():
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        writer = cv2.VideoWriter(str(p), fourcc, 20.0, (w, h))

    bg = np.ones((h, w, 3), dtype=np.uint8) * 30
    for f in range(40):
        frame = bg.copy()
        if f >= 10:
            cx = int(50 + (f - 10) * 6)
            cy = 120
            cv2.circle(frame, (cx, cy), 28, (0, 180, 255), -1)
        writer.write(frame)
    writer.release()
    return p
