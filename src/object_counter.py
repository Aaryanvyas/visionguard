"""Object counting and geometric morphology analysis module."""

import cv2
import numpy as np
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from src.config import (
    OBJECT_MIN_CONTOUR_AREA, OBJECT_MAX_CONTOUR_AREA,
    OBJECT_ADAPTIVE_BLOCK_SIZE, OBJECT_ADAPTIVE_C
)
from src.image_utils import load_image, save_image, to_grayscale
from src.database import start_session, log_detections_batch, finish_session
from src.logger_setup import logger

class ObjectCounter:
    """Detects and enumerates discrete physical objects via adaptive contour extraction."""

    def __init__(
        self,
        min_area: int = OBJECT_MIN_CONTOUR_AREA,
        max_area: int = OBJECT_MAX_CONTOUR_AREA,
        block_size: int = OBJECT_ADAPTIVE_BLOCK_SIZE,
        c_val: int = OBJECT_ADAPTIVE_C
    ):
        self.min_area = min_area
        self.max_area = max_area
        self.block_size = block_size
        self.c_val = c_val

    def count(self, image: np.ndarray) -> Tuple[List[Dict[str, Any]], np.ndarray]:
        """Segments objects using adaptive Gaussian thresholding and contour hierarchy."""
        gray = to_grayscale(image)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,
            self.block_size, self.c_val
        )

        # Morphological close to bridge internal hollows, then open to remove specks
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
        cleaned = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel, iterations=1)

        contours, hierarchy = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        objects = []
        for i, c in enumerate(contours):
            area = cv2.contourArea(c)
            if self.min_area <= area <= self.max_area:
                perimeter = cv2.arcLength(c, True)
                x, y, w, h = cv2.boundingRect(c)
                M = cv2.moments(c)
                cx = int(M["m10"] / (M["m00"] + 1e-6))
                cy = int(M["m01"] / (M["m00"] + 1e-6))

                objects.append({
                    "id": len(objects) + 1,
                    "label": "object",
                    "box": (int(x), int(y), int(w), int(h)),
                    "area": float(area),
                    "perimeter": float(perimeter),
                    "centroid": (cx, cy),
                    "contour": c,
                    "frame_index": 0,
                    "confidence": 1.0
                })

        # Sort left-to-right, top-to-bottom for consistent deterministic numbering
        objects.sort(key=lambda o: (o["box"][1] // 50, o["box"][0]))
        for idx, obj in enumerate(objects, 1):
            obj["id"] = idx

        return objects, cleaned

    def annotate(self, image: np.ndarray, objects: List[Dict[str, Any]]) -> np.ndarray:
        """Annotates detected shapes with bounding boxes, contour lines, and #ID tags."""
        annotated = image.copy()
        if len(annotated.shape) == 2:
            annotated = cv2.cvtColor(annotated, cv2.COLOR_GRAY2BGR)

        for obj in objects:
            x, y, w, h = obj["box"]
            cv2.drawContours(annotated, [obj["contour"]], -1, (0, 255, 0), 2)
            cv2.rectangle(annotated, (x, y), (x + w, y + h), (255, 128, 0), 2)

            tag = f"#{obj['id']}"
            cv2.putText(
                annotated,
                tag,
                (x, max(15, y - 5)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 165, 255),
                2,
                cv2.LINE_AA
            )

        return annotated

    def process_image(
        self,
        input_path: str,
        output_path: Optional[str] = None,
        log_to_db: bool = True,
        db_path: Optional[Path] = None
    ) -> Dict[str, Any]:
        """Runs end-to-end object counting pipeline with SQLite persistence."""
        session_id = None
        if log_to_db:
            session_id = start_session("object_counting", input_path, db_path=db_path)

        try:
            image = load_image(input_path)
            objects, _ = self.count(image)
            annotated = self.annotate(image, objects)

            saved_path = None
            if output_path:
                saved_path = str(save_image(annotated, output_path))

            total_area = sum(o["area"] for o in objects)
            avg_area = round(total_area / len(objects), 1) if objects else 0.0

            summary = {
                "object_count": len(objects),
                "avg_area_px": avg_area,
                "output_path": saved_path
            }

            if log_to_db and session_id:
                # Strip raw numpy contour array before serialization
                serializable_dets = [
                    {"label": o["label"], "box": o["box"], "confidence": o["confidence"], "frame_index": 0}
                    for o in objects
                ]
                log_detections_batch(session_id, serializable_dets, db_path=db_path)
                finish_session(session_id, status="completed", summary=summary, db_path=db_path)

            logger.info("[count] Detected %d object(s), avg area=%.1fpx^2. Saved -> %s", len(objects), avg_area, saved_path)
            return {
                "session_id": session_id,
                "object_count": len(objects),
                "avg_area": avg_area,
                "objects": objects,
                "output_path": saved_path
            }

        except Exception as e:
            logger.error("Object counting failed on %s: %s", input_path, e)
            if log_to_db and session_id:
                finish_session(session_id, status="failed", summary={"error": str(e)}, db_path=db_path)
            raise
