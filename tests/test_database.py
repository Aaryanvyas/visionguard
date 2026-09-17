"""Tests for src/database.py."""

import pytest
from src.database import (
    init_db, start_session, log_detection, log_detections_batch,
    finish_session, get_session, list_sessions
)

def test_init_db_creates_tables(temp_db):
    assert temp_db.exists()
    session = get_session(999, db_path=temp_db)
    assert session is None

def test_start_and_finish_session(temp_db):
    s_id = start_session("test_mod", "sample.jpg", db_path=temp_db)
    assert s_id == 1

    finish_session(s_id, status="completed", summary={"count": 5}, db_path=temp_db)
    s = get_session(s_id, db_path=temp_db)
    assert s["status"] == "completed"
    assert s["summary"]["count"] == 5
    assert s["finished_at"] is not None

def test_log_single_detection(temp_db):
    s_id = start_session("face_detection", "input.jpg", db_path=temp_db)
    d_id = log_detection(s_id, "face", (10, 20, 30, 40), confidence=0.95, db_path=temp_db)
    assert d_id == 1

    s = get_session(s_id, db_path=temp_db)
    assert len(s["detections"]) == 1
    d = s["detections"][0]
    assert d["label"] == "face"
    assert (d["x"], d["y"], d["width"], d["height"]) == (10, 20, 30, 40)

def test_log_detections_batch(temp_db):
    s_id = start_session("object_counting", "shapes.png", db_path=temp_db)
    dets = [
        {"label": "object", "box": (0, 0, 10, 10), "confidence": 1.0},
        {"label": "object", "box": (20, 20, 15, 15), "confidence": 1.0},
    ]
    count = log_detections_batch(s_id, dets, db_path=temp_db)
    assert count == 2
    s = get_session(s_id, db_path=temp_db)
    assert len(s["detections"]) == 2

def test_list_sessions_returns_correct_counts(temp_db):
    s1 = start_session("mod_1", "a.jpg", db_path=temp_db)
    log_detection(s1, "item", (1, 2, 3, 4), db_path=temp_db)
    finish_session(s1, db_path=temp_db)

    s2 = start_session("mod_2", "b.jpg", db_path=temp_db)
    finish_session(s2, db_path=temp_db)

    sessions = list_sessions(limit=5, db_path=temp_db)
    assert len(sessions) == 2
    assert sessions[0]["session_id"] == s2
    assert sessions[0]["detection_count"] == 0
    assert sessions[1]["session_id"] == s1
    assert sessions[1]["detection_count"] == 1

def test_failed_session_status_logging(temp_db):
    s_id = start_session("err_module", "bad.mp4", db_path=temp_db)
    finish_session(s_id, status="failed", summary={"error": "File corrupted"}, db_path=temp_db)
    s = get_session(s_id, db_path=temp_db)
    assert s["status"] == "failed"
    assert "error" in s["summary"]
