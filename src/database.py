"""SQLite persistence layer for VisionGuard sessions and detections."""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from src.config import DEFAULT_DB_PATH
from src.logger_setup import logger

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS sessions (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    module TEXT NOT NULL,
    source_path TEXT NOT NULL,
    started_at TEXT NOT NULL,
    finished_at TEXT,
    status TEXT NOT NULL,
    summary_json TEXT
);

CREATE TABLE IF NOT EXISTS detections (
    detection_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    frame_index INTEGER DEFAULT 0,
    label TEXT NOT NULL,
    x INTEGER NOT NULL,
    y INTEGER NOT NULL,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    confidence REAL DEFAULT 1.0,
    created_at TEXT NOT NULL,
    FOREIGN KEY (session_id) REFERENCES sessions (session_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_detections_session_id ON detections(session_id);
"""

def get_connection(db_path: Optional[Path] = None) -> sqlite3.Connection:
    """Returns a SQLite connection with row factory enabled."""
    target_path = Path(db_path or DEFAULT_DB_PATH)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(target_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db(db_path: Optional[Path] = None) -> None:
    """Initializes SQLite tables and indexes."""
    with get_connection(db_path) as conn:
        conn.executescript(SCHEMA_SQL)
        conn.commit()
    logger.debug("Database initialized at %s", db_path or DEFAULT_DB_PATH)

def start_session(module: str, source_path: str, db_path: Optional[Path] = None) -> int:
    """Creates a new analysis session record with 'running' status."""
    init_db(db_path)
    now_str = datetime.now().isoformat()
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO sessions (module, source_path, started_at, status) VALUES (?, ?, ?, ?)",
            (module, str(source_path), now_str, "running")
        )
        conn.commit()
        session_id = cursor.lastrowid
    logger.info("Started session %d for module '%s' on %s", session_id, module, source_path)
    return session_id

def log_detection(
    session_id: int,
    label: str,
    box: tuple,
    frame_index: int = 0,
    confidence: float = 1.0,
    db_path: Optional[Path] = None
) -> int:
    """Logs a single detected entity for an active session."""
    x, y, w, h = box
    now_str = datetime.now().isoformat()
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO detections 
               (session_id, frame_index, label, x, y, width, height, confidence, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (session_id, frame_index, label, int(x), int(y), int(w), int(h), float(confidence), now_str)
        )
        conn.commit()
        return cursor.lastrowid

def log_detections_batch(
    session_id: int,
    detections: List[Dict[str, Any]],
    db_path: Optional[Path] = None
) -> int:
    """Logs a list of detections efficiently in a single transaction."""
    if not detections:
        return 0
    now_str = datetime.now().isoformat()
    records = []
    for d in detections:
        x, y, w, h = d.get("box", (0, 0, 0, 0))
        records.append((
            session_id,
            d.get("frame_index", 0),
            d.get("label", "object"),
            int(x),
            int(y),
            int(w),
            int(h),
            float(d.get("confidence", 1.0)),
            now_str
        ))
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.executemany(
            """INSERT INTO detections 
               (session_id, frame_index, label, x, y, width, height, confidence, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            records
        )
        conn.commit()
        return cursor.rowcount

def finish_session(
    session_id: int,
    status: str = "completed",
    summary: Optional[Dict[str, Any]] = None,
    db_path: Optional[Path] = None
) -> None:
    """Finalizes an existing session record with completion timestamp and summary."""
    now_str = datetime.now().isoformat()
    summary_str = json.dumps(summary or {})
    with get_connection(db_path) as conn:
        conn.execute(
            "UPDATE sessions SET finished_at = ?, status = ?, summary_json = ? WHERE session_id = ?",
            (now_str, status, summary_str, session_id)
        )
        conn.commit()
    logger.info("Finalized session %d with status '%s'", session_id, status)

def get_session(session_id: int, db_path: Optional[Path] = None) -> Optional[Dict[str, Any]]:
    """Retrieves session metadata and associated detections by ID."""
    init_db(db_path)
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,))
        row = cursor.fetchone()
        if not row:
            return None
        session = dict(row)
        if session.get("summary_json"):
            try:
                session["summary"] = json.loads(session["summary_json"])
            except Exception:
                session["summary"] = {}

        cursor.execute("SELECT * FROM detections WHERE session_id = ? ORDER BY detection_id ASC", (session_id,))
        session["detections"] = [dict(d) for d in cursor.fetchall()]
        return session

def list_sessions(limit: int = 10, db_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Returns a list of recent sessions with detection counts."""
    init_db(db_path)
    query = """
    SELECT 
        s.session_id, s.module, s.source_path, s.started_at, s.finished_at, s.status, s.summary_json,
        COUNT(d.detection_id) AS detection_count
    FROM sessions s
    LEFT JOIN detections d ON s.session_id = d.session_id
    GROUP BY s.session_id
    ORDER BY s.session_id DESC
    LIMIT ?
    """
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (limit,))
        results = []
        for r in cursor.fetchall():
            d = dict(r)
            if d.get("summary_json"):
                try:
                    d["summary"] = json.loads(d["summary_json"])
                except Exception:
                    d["summary"] = {}
            results.append(d)
        return results
