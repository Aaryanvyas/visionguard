"""Generates JSON, CSV, and Matplotlib analytics reports from SQLite sessions."""

import csv
import json
from pathlib import Path
from typing import Dict, Any, Optional
import matplotlib
matplotlib.use("Agg")  # Headless backend
import matplotlib.pyplot as plt
from src.config import OUTPUT_DIR
from src.database import get_session, list_sessions
from src.logger_setup import logger

def export_session_json(session_id: int, output_dir: Optional[str] = None, db_path: Optional[Path] = None) -> Path:
    """Exports full session metadata and detections to formatted JSON."""
    session = get_session(session_id, db_path=db_path)
    if not session:
        raise ValueError(f"Session #{session_id} not found in database.")

    out_dir = Path(output_dir or OUTPUT_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"session_{session_id}_report.json"

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(session, f, indent=2)

    logger.info("Exported JSON report -> %s", out_file)
    return out_file

def export_session_csv(session_id: int, output_dir: Optional[str] = None, db_path: Optional[Path] = None) -> Path:
    """Exports detections of a session into CSV format."""
    session = get_session(session_id, db_path=db_path)
    if not session:
        raise ValueError(f"Session #{session_id} not found in database.")

    out_dir = Path(output_dir or OUTPUT_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"session_{session_id}_detections.csv"

    detections = session.get("detections", [])
    fieldnames = ["detection_id", "session_id", "frame_index", "label", "x", "y", "width", "height", "confidence", "created_at"]

    with open(out_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for d in detections:
            writer.writerow({k: d.get(k) for k in fieldnames})

    logger.info("Exported CSV report -> %s", out_file)
    return out_file

def generate_analytics_chart(limit: int = 10, output_path: Optional[str] = None, db_path: Optional[Path] = None) -> Path:
    """Generates a styled bar chart comparing detection counts across recent sessions."""
    sessions = list_sessions(limit=limit, db_path=db_path)
    # Reverse so oldest in window is on the left
    sessions = list(reversed(sessions))

    out_p = Path(output_path or (OUTPUT_DIR / "session_analytics.png"))
    out_p.parent.mkdir(parents=True, exist_ok=True)

    labels = [f"#{s['session_id']}\n{s['module'].split('_')[0]}" for s in sessions] if sessions else ["None"]
    counts = [s.get("detection_count", 0) for s in sessions] if sessions else [0]

    # Color palette
    palette = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f"]
    colors = [palette[i % len(palette)] for i in range(len(counts))]

    plt.figure(figsize=(8, 4.5), dpi=150)
    bars = plt.bar(labels, counts, color=colors, width=0.55, edgecolor="#333333", linewidth=0.8)
    plt.title("Detections per Recent Session", fontsize=12, fontweight="bold", pad=12)
    plt.xlabel("Session", fontsize=10, labelpad=8)
    plt.ylabel("Detections", fontsize=10, labelpad=8)
    plt.grid(axis="y", linestyle="--", alpha=0.5)

    # Annotate bar values on top
    for bar in bars:
        h = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, h + 0.5, str(int(h)), ha="center", va="bottom", fontsize=9)

    plt.tight_layout()
    plt.savefig(str(out_p))
    plt.close()

    logger.info("Generated analytics chart -> %s", out_p)
    return out_p

def generate_full_report(session_id: int, output_dir: Optional[str] = None, db_path: Optional[Path] = None) -> Dict[str, Any]:
    """Generates JSON, CSV, and chart for a completed session."""
    json_path = export_session_json(session_id, output_dir, db_path)
    csv_path = export_session_csv(session_id, output_dir, db_path)
    chart_path = generate_analytics_chart(limit=10, output_path=None if not output_dir else str(Path(output_dir) / "analytics_chart.png"), db_path=db_path)

    return {
        "session_id": session_id,
        "json_path": str(json_path),
        "csv_path": str(csv_path),
        "chart_path": str(chart_path)
    }
