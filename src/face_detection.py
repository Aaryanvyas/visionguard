"""Face detection module using classical OpenCV Haar Cascade Classifier."""

import cv2
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional
from src.config import (
    HAAR_CASCADE_PATH, FACE_SCALE_FACTOR, FACE_MIN_NEIGHBORS, FACE_MIN_SIZE
)
from src.image_utils import load_image, save_image, draw_bounding_box
from src.database import start_session, log_detections_batch, finish_session
from src.logger_setup import logger

class FaceDetector:
    """Encapsulates Haar Cascade based frontal face detection."""

    def __init__(
        self,
        cascade_path: Optional[Path] = None,
        scale_factor: float = FACE_SCALE_FACTOR,
        min_neighbors: int = FACE_MIN_NEIGHBORS,
        min_size: tuple = FACE_MIN_SIZE
    ):
        path = cascade_path or HAAR_CASCADE_PATH
        if not Path(path).exists():
            raise FileNotFoundError(f"Haar cascade xml file not found at: {path}")
        self.cascade = cv2.CascadeClassifier(str(path))
        if self.cascade.empty():
            raise RuntimeError(f"Failed to load Haar Cascade from {path}")
        self.scale_factor = scale_factor
        self.min_neighbors = min_neighbors
        self.min_size = min_size

    def detect(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """Detects faces in BGR or Grayscale image and returns list of detection dicts."""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        # Equalize gray histogram for improved contrast invariance
        gray = cv2.equalizeHist(gray)

        raw_faces = self.cascade.detectMultiScale(
            gray,
            scaleFactor=self.scale_factor,
            minNeighbors=self.min_neighbors,
            minSize=self.min_size,
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        detections = []
        for (x, y, w, h) in raw_faces:
            detections.append({
                "label": "face",
                "box": (int(x), int(y), int(w), int(h)),
                "confidence": 1.0,
                "frame_index": 0
            })
        return detections

    def annotate(self, image: np.ndarray, detections: List[Dict[str, Any]]) -> np.ndarray:
        """Annotates detected bounding boxes on copy of the image."""
        annotated = image.copy()
        if len(annotated.shape) == 2:
            annotated = cv2.cvtColor(annotated, cv2.COLOR_GRAY2BGR)

        for d in detections:
            annotated = draw_bounding_box(
                annotated,
                d["box"],
                label="face",
                color=(0, 255, 0),
                thickness=2
            )
        return annotated

    def process_image(
        self,
        input_path: str,
        output_path: Optional[str] = None,
        log_to_db: bool = True,
        db_path: Optional[Path] = None
    ) -> Dict[str, Any]:
        """Runs end-to-end face detection pipeline with SQLite audit logging."""
        session_id = None
        if log_to_db:
            session_id = start_session("face_detection", input_path, db_path=db_path)

        try:
            image = load_image(input_path)
            detections = self.detect(image)
            annotated = self.annotate(image, detections)

            saved_path = None
            if output_path:
                saved_path = str(save_image(annotated, output_path))

            summary = {
                "face_count": len(detections),
                "output_path": saved_path,
                "status": "success"
            }

            if log_to_db and session_id:
                log_detections_batch(session_id, detections, db_path=db_path)
                finish_session(session_id, status="completed", summary=summary, db_path=db_path)

            logger.info("[faces] Detected %d face(s). Saved -> %s", len(detections), saved_path)
            return {
                "session_id": session_id,
                "face_count": len(detections),
                "detections": detections,
                "output_path": saved_path
            }

        except Exception as e:
            logger.error("Face detection failed on %s: %s", input_path, e)
            if log_to_db and session_id:
                finish_session(session_id, status="failed", summary={"error": str(e)}, db_path=db_path)
            raise
