"""Motion detection module using MOG2 background subtraction and morphology."""

from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import cv2
import numpy as np
from src.config import (
    MOTION_HISTORY, MOTION_VAR_THRESHOLD, MOTION_DETECT_SHADOWS,
    MOTION_SHADOW_THRESHOLD, MOTION_MIN_CONTOUR_AREA, MOTION_KERNEL_SIZE,
    MAX_FRAME_WIDTH
)
from src.database import start_session, log_detections_batch, finish_session
from src.logger_setup import logger

class MotionDetector:
    """Tracks moving foreground objects across sequential video frames using MOG2."""

    def __init__(
        self,
        history: int = MOTION_HISTORY,
        var_threshold: float = MOTION_VAR_THRESHOLD,
        detect_shadows: bool = MOTION_DETECT_SHADOWS,
        min_area: int = MOTION_MIN_CONTOUR_AREA,
        shadow_thresh: int = MOTION_SHADOW_THRESHOLD
    ):
        self.subtractor = cv2.createBackgroundSubtractorMOG2(
            history=history,
            varThreshold=var_threshold,
            detectShadows=detect_shadows
        )
        self.min_area = min_area
        self.shadow_thresh = shadow_thresh
        self.kernel = cv2.getStructuringElement(cv2.MORPH_RECT, MOTION_KERNEL_SIZE)

    def process_frame(self, frame: np.ndarray, frame_index: int = 0) -> Tuple[List[Dict[str, Any]], np.ndarray]:
        """Applies MOG2 foreground subtraction, removes shadows, and detects moving contours."""
        fg_mask = self.subtractor.apply(frame)

        # Remove shadow pixels (OpenCV MOG2 sets shadows to ~127; foreground is 255)
        _, clean_mask = cv2.threshold(fg_mask, self.shadow_thresh, 255, cv2.THRESH_BINARY)

        # Morphological opening to filter salt-and-pepper noise
        clean_mask = cv2.morphologyEx(clean_mask, cv2.MORPH_OPEN, self.kernel, iterations=1)
        # Morphological dilation to bridge small gaps within moving bodies
        clean_mask = cv2.dilate(clean_mask, self.kernel, iterations=2)

        contours, _ = cv2.findContours(clean_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        detections = []
        for c in contours:
            area = cv2.contourArea(c)
            if area >= self.min_area:
                x, y, w, h = cv2.boundingRect(c)
                detections.append({
                    "label": "motion",
                    "box": (int(x), int(y), int(w), int(h)),
                    "area": float(area),
                    "confidence": 1.0,
                    "frame_index": frame_index
                })

        return detections, clean_mask

    def process_video(
        self,
        input_path: str,
        output_path: Optional[str] = None,
        max_frames: Optional[int] = None,
        log_to_db: bool = True,
        db_path: Optional[Path] = None
    ) -> Dict[str, Any]:
        """Streams and processes a video file, saving an annotated motion tracking output video."""
        in_path = Path(input_path)
        if not in_path.exists():
            raise FileNotFoundError(f"Video file not found: {input_path}")

        session_id = None
        if log_to_db:
            session_id = start_session("motion_detection", str(in_path), db_path=db_path)

        cap = cv2.VideoCapture(str(in_path))
        if not cap.isOpened():
            if log_to_db and session_id:
                finish_session(session_id, status="failed", summary={"error": "Cannot open video"}, db_path=db_path)
            raise IOError(f"Failed to open video source: {input_path}")

        fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
        orig_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        orig_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Downscale if wider than MAX_FRAME_WIDTH
        if orig_w > MAX_FRAME_WIDTH:
            scale = MAX_FRAME_WIDTH / float(orig_w)
            target_w = MAX_FRAME_WIDTH
            target_h = int(orig_h * scale)
        else:
            target_w = orig_w
            target_h = orig_h

        writer = None
        if output_path:
            out_p = Path(output_path)
            out_p.parent.mkdir(parents=True, exist_ok=True)
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            writer = cv2.VideoWriter(str(out_p), fourcc, fps, (target_w, target_h))
            if not writer.isOpened():
                # Fallback to XVID
                fourcc = cv2.VideoWriter_fourcc(*"XVID")
                writer = cv2.VideoWriter(str(out_p), fourcc, fps, (target_w, target_h))

        frame_idx = 0
        all_detections: List[Dict[str, Any]] = []

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                if (frame.shape[1], frame.shape[0]) != (target_w, target_h):
                    frame = cv2.resize(frame, (target_w, target_h), interpolation=cv2.INTER_AREA)

                dets, _ = self.process_frame(frame, frame_index=frame_idx)
                all_detections.extend(dets)

                # Annotate moving regions
                for d in dets:
                    x, y, w, h = d["box"]
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.putText(
                        frame,
                        "motion",
                        (x, max(15, y - 5)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 0, 255),
                        1,
                        cv2.LINE_AA
                    )

                if writer:
                    writer.write(frame)

                frame_idx += 1
                if max_frames and frame_idx >= max_frames:
                    break

            cap.release()
            if writer:
                writer.release()

            summary = {
                "total_frames": frame_idx,
                "motion_events": len(all_detections),
                "output_path": output_path
            }

            if log_to_db and session_id:
                log_detections_batch(session_id, all_detections, db_path=db_path)
                finish_session(session_id, status="completed", summary=summary, db_path=db_path)

            logger.info(
                "[motion] Processed %d frame(s); %d motion event(s). Saved -> %s",
                frame_idx, len(all_detections), output_path
            )

            return {
                "session_id": session_id,
                "total_frames": frame_idx,
                "motion_events": len(all_detections),
                "output_path": output_path
            }

        except Exception as e:
            cap.release()
            if writer:
                writer.release()
            logger.error("Motion detection failed on %s: %s", input_path, e)
            if log_to_db and session_id:
                finish_session(session_id, status="failed", summary={"error": str(e)}, db_path=db_path)
            raise
