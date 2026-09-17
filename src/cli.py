"""Command-Line Interface parser and dispatcher for VisionGuard."""

import argparse
import sys
from pathlib import Path
from src.image_utils import load_image, save_image, apply_filter, FILTER_MAP
from src.face_detection import FaceDetector
from src.motion_detection import MotionDetector
from src.object_counter import ObjectCounter
from src.report_generator import generate_full_report, generate_analytics_chart
from src.database import list_sessions
from src.logger_setup import logger

def build_parser() -> argparse.ArgumentParser:
    """Constructs the top-level argument parser and subcommands."""
    parser = argparse.ArgumentParser(
        prog="visionguard",
        description="VisionGuard: Modular Computer Vision Surveillance and Analytics Toolkit"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Command: faces
    p_faces = subparsers.add_parser("faces", help="Detect faces in an input image")
    p_faces.add_argument("--input", "-i", required=True, help="Path to input image")
    p_faces.add_argument("--output", "-o", default="data/output/faces_annotated.jpg", help="Path to save annotated image")
    p_faces.add_argument("--scale-factor", type=float, default=1.1, help="Haar cascade scaleFactor")
    p_faces.add_argument("--min-neighbors", type=int, default=5, help="Haar cascade minNeighbors")

    # Command: motion
    p_motion = subparsers.add_parser("motion", help="Detect motion across video frames using MOG2")
    p_motion.add_argument("--input", "-i", required=True, help="Path to input video file")
    p_motion.add_argument("--output", "-o", default="data/output/motion_annotated.mp4", help="Path to save output video")
    p_motion.add_argument("--min-area", type=int, default=800, help="Minimum contour area to register as motion")
    p_motion.add_argument("--max-frames", type=int, default=None, help="Maximum number of frames to process")

    # Command: count
    p_count = subparsers.add_parser("count", help="Count discrete objects via contour analysis")
    p_count.add_argument("--input", "-i", required=True, help="Path to input image")
    p_count.add_argument("--output", "-o", default="data/output/count_annotated.png", help="Path to save annotated image")
    p_count.add_argument("--min-area", type=int, default=300, help="Minimum contour area for objects")

    # Command: enhance
    p_enhance = subparsers.add_parser("enhance", help="Apply image enhancement or spatial filter")
    p_enhance.add_argument("--input", "-i", required=True, help="Path to input image")
    p_enhance.add_argument("--output", "-o", default="data/output/enhanced.jpg", help="Path to save filtered image")
    p_enhance.add_argument("--filter", "-f", required=True, choices=list(FILTER_MAP.keys()), help="Filter to apply")

    # Command: report
    p_report = subparsers.add_parser("report", help="Export session reports (JSON/CSV) and analytics chart")
    p_report.add_argument("--session-id", "-s", type=int, help="Session ID to export")
    p_report.add_argument("--output-dir", "-d", default="data/output", help="Directory for exported reports")
    p_report.add_argument("--chart", action="store_true", help="Generate analytics chart across recent sessions")

    # Command: history
    p_hist = subparsers.add_parser("history", help="List recent analysis sessions from SQLite")
    p_hist.add_argument("--limit", "-n", type=int, default=10, help="Maximum sessions to display")

    return parser

def main(args=None) -> int:
    """Dispatches CLI commands."""
    parser = build_parser()
    parsed = parser.parse_args(args)

    if not parsed.command:
        parser.print_help()
        return 0

    try:
        if parsed.command == "faces":
            detector = FaceDetector(scale_factor=parsed.scale_factor, min_neighbors=parsed.min_neighbors)
            res = detector.process_image(parsed.input, parsed.output)
            print(f"[faces] Detected {res['face_count']} face(s). Saved -> {res['output_path']}")
            return 0

        elif parsed.command == "motion":
            detector = MotionDetector(min_area=parsed.min_area)
            res = detector.process_video(parsed.input, parsed.output, max_frames=parsed.max_frames)
            print(f"[motion] Processed {res['total_frames']} frame(s); {res['motion_events']} motion event(s). Saved -> {res['output_path']}")
            return 0

        elif parsed.command == "count":
            counter = ObjectCounter(min_area=parsed.min_area)
            res = counter.process_image(parsed.input, parsed.output)
            print(f"[count] Detected {res['object_count']} object(s), avg area={res['avg_area']}px^2. Saved -> {res['output_path']}")
            return 0

        elif parsed.command == "enhance":
            img = load_image(parsed.input)
            filtered = apply_filter(img, parsed.filter)
            out = save_image(filtered, parsed.output)
            print(f"[enhance] Applied '{parsed.filter}' filter. Saved -> {out}")
            return 0

        elif parsed.command == "report":
            if parsed.chart or not parsed.session_id:
                chart_path = generate_analytics_chart(output_path=f"{parsed.output_dir}/session_analytics.png")
                print(f"[report] Analytics chart generated -> {chart_path}")
            if parsed.session_id:
                rep = generate_full_report(parsed.session_id, output_dir=parsed.output_dir)
                print(f"[report] Full report generated for Session #{parsed.session_id}:")
                print(f"  - JSON: {rep['json_path']}")
                print(f"  - CSV:  {rep['csv_path']}")
                print(f"  - Chart:{rep['chart_path']}")
            return 0

        elif parsed.command == "history":
            sessions = list_sessions(limit=parsed.limit)
            if not sessions:
                print("No sessions recorded yet.")
                return 0
            print(f"{'ID':<4} | {'Module':<16} | {'Status':<10} | {'Detections':<10} | {'Started At':<20} | {'Source'}")
            print("-" * 80)
            for s in sessions:
                print(
                    f"{s['session_id']:<4} | {s['module']:<16} | {s['status']:<10} | "
                    f"{s['detection_count']:<10} | {s['started_at'][:19]:<20} | {Path(s['source_path']).name}"
                )
            return 0

    except Exception as e:
        logger.error("CLI Execution Error: %s", e)
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
