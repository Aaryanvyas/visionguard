"""Tests for src/motion_detection.py."""

import pytest
import numpy as np
import cv2
from src.motion_detection import MotionDetector

def test_motion_detector_initialization():
    detector = MotionDetector(min_area=500)
    assert detector.min_area == 500
    assert detector.subtractor is not None

def test_motion_detector_static_frame_no_motion():
    detector = MotionDetector(min_area=200)
    static_frame = np.full((200, 200, 3), 80, dtype=np.uint8)

    # Feed multiple identical static frames to establish background
    for idx in range(15):
        dets, mask = detector.process_frame(static_frame, frame_index=idx)

    # Static frame should yield zero motion detections
    assert len(dets) == 0

def test_motion_detector_moving_object_detected():
    # Tuned for realistic synthetic frame size & contour area
    detector = MotionDetector(min_area=300)
    bg = np.full((300, 400, 3), 40, dtype=np.uint8)

    # Establish static background
    for i in range(15):
        detector.process_frame(bg, frame_index=i)

    # Introduce a prominent moving bright rectangle
    moving_frame = bg.copy()
    cv2.rectangle(moving_frame, (100, 100), (200, 200), (240, 240, 240), -1)
    dets, mask = detector.process_frame(moving_frame, frame_index=16)

    assert len(dets) >= 1
    assert dets[0]["label"] == "motion"
    assert dets[0]["area"] >= 300

def test_motion_detector_video_processing_pipeline(synthetic_moving_video_path, temp_db, tmp_path):
    out_video = tmp_path / "annotated_motion.mp4"
    detector = MotionDetector(min_area=300)

    result = detector.process_video(
        str(synthetic_moving_video_path),
        output_path=str(out_video),
        max_frames=30,
        log_to_db=True,
        db_path=temp_db
    )

    assert result["total_frames"] == 30
    assert result["motion_events"] > 0
    assert out_video.exists()
