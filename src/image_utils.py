"""Image processing utilities, input validation, and filter registry."""

import os
from pathlib import Path
from typing import Tuple, List, Optional
import cv2
import numpy as np
from src.config import ALLOWED_IMAGE_EXTENSIONS, MAX_FRAME_WIDTH
from src.logger_setup import logger

def validate_image_path(image_path: str) -> Path:
    """Validates existence and extension of an input image file."""
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Input image does not exist: {image_path}")
    if path.suffix.lower() not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValueError(
            f"Unsupported image format '{path.suffix}'. Supported formats: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}"
        )
    return path

def load_image(image_path: str, max_width: int = MAX_FRAME_WIDTH) -> np.ndarray:
    """Loads an image from disk and optionally resizes if wider than max_width."""
    path = validate_image_path(image_path)
    image = cv2.imread(str(path))
    if image is None:
        raise ValueError(f"OpenCV failed to decode image: {image_path}")

    h, w = image.shape[:2]
    if max_width and w > max_width:
        ratio = max_width / float(w)
        new_height = int(h * ratio)
        image = cv2.resize(image, (max_width, new_height), interpolation=cv2.INTER_AREA)
        logger.debug("Downscaled image %s from (%d, %d) to (%d, %d)", path.name, w, h, max_width, new_height)

    return image

def save_image(image: np.ndarray, output_path: str) -> Path:
    """Saves an image to disk, ensuring directory existence."""
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    success = cv2.imwrite(str(out), image)
    if not success:
        raise IOError(f"Failed to write image to {output_path}")
    logger.info("Saved image -> %s", out)
    return out

# --- Filter Registry ---

def to_grayscale(img: np.ndarray) -> np.ndarray:
    """Converts image to grayscale (single-channel or 3-channel duplicate for saving)."""
    if len(img.shape) == 2:
        return img
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def apply_gaussian_blur(img: np.ndarray, ksize: Tuple[int, int] = (5, 5), sigma: float = 0.0) -> np.ndarray:
    """Applies Gaussian spatial smoothing filter."""
    return cv2.GaussianBlur(img, ksize, sigma)

def apply_canny_edges(img: np.ndarray, threshold1: int = 50, threshold2: int = 150) -> np.ndarray:
    """Extracts edges using the Canny edge detection algorithm."""
    gray = to_grayscale(img)
    edges = cv2.Canny(gray, threshold1, threshold2)
    return edges

def apply_histogram_equalization(img: np.ndarray) -> np.ndarray:
    """Enhances contrast using histogram equalization across intensity/luminance."""
    if len(img.shape) == 2:
        return cv2.equalizeHist(img)
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
    return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)

def apply_adaptive_threshold(img: np.ndarray, block_size: int = 11, c: int = 2) -> np.ndarray:
    """Applies adaptive Gaussian thresholding to handle illumination variations."""
    gray = to_grayscale(img)
    return cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, c
    )

def apply_sharpen(img: np.ndarray) -> np.ndarray:
    """Sharpens high-frequency edge details using a 3x3 Laplacian-derived kernel."""
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]], dtype=np.float32)
    return cv2.filter2D(img, -1, kernel)

FILTER_MAP = {
    "grayscale": to_grayscale,
    "blur": apply_gaussian_blur,
    "edges": apply_canny_edges,
    "hist_eq": apply_histogram_equalization,
    "adaptive_thresh": apply_adaptive_threshold,
    "sharpen": apply_sharpen,
}

def apply_filter(img: np.ndarray, filter_name: str) -> np.ndarray:
    """Applies a named filter from the filter registry."""
    key = filter_name.lower().strip()
    if key not in FILTER_MAP:
        available = ", ".join(FILTER_MAP.keys())
        raise ValueError(f"Unknown filter '{filter_name}'. Available filters: {available}")
    return FILTER_MAP[key](img)

def draw_bounding_box(
    img: np.ndarray,
    box: Tuple[int, int, int, int],
    label: Optional[str] = None,
    color: Tuple[int, int, int] = (0, 255, 0),
    thickness: int = 2
) -> np.ndarray:
    """Draws a styled bounding box with optional text badge on an image."""
    annotated = img.copy()
    if len(annotated.shape) == 2:
        annotated = cv2.cvtColor(annotated, cv2.COLOR_GRAY2BGR)

    x, y, w, h = box
    cv2.rectangle(annotated, (x, y), (x + w, y + h), color, thickness)
    if label:
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        font_thickness = 1
        (text_w, text_h), baseline = cv2.getTextSize(label, font, font_scale, font_thickness)
        badge_y1 = max(0, y - text_h - 6)
        badge_y2 = y
        cv2.rectangle(annotated, (x, badge_y1), (x + text_w + 4, badge_y2), color, -1)
        cv2.putText(
            annotated,
            label,
            (x + 2, y - 4),
            font,
            font_scale,
            (255, 255, 255) if sum(color) < 400 else (0, 0, 0),
            font_thickness,
            cv2.LINE_AA
        )
    return annotated
