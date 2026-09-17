"""Central configuration and hyperparameter constants for VisionGuard.

Developer: Aryan Vyas (Reg: 24BAI10343)
Course: Computer Vision — Flipped Course Project
"""

import os
from pathlib import Path
import cv2

# Base directory paths
SRC_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SRC_DIR.parent
DATA_DIR = PROJECT_DIR / "data"
SAMPLES_DIR = DATA_DIR / "samples"
OUTPUT_DIR = DATA_DIR / "output"
LOGS_DIR = PROJECT_DIR / "logs"
DOCS_DIR = PROJECT_DIR / "docs"
DIAGRAMS_DIR = DOCS_DIR / "diagrams"

# Database configuration
# Stored locally inside data/ so no external database server is needed
DEFAULT_DB_PATH = DATA_DIR / "visionguard.db"

# Logging configuration (keeps up to 3 backup logs, 2MB each)
DEFAULT_LOG_FILE = LOGS_DIR / "visionguard.log"
LOG_MAX_BYTES = 2 * 1024 * 1024
LOG_BACKUP_COUNT = 3

# Constraints on image/frame dimensions for responsive processing
MAX_FRAME_WIDTH = 1280
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv"}

# Face Detection Parameters (Haar Cascade)
# First check local repo bundle in data/models/, then fall back to OpenCV system path if available
MODELS_DIR = DATA_DIR / "models"
LOCAL_CASCADE_PATH = MODELS_DIR / "haarcascade_frontalface_default.xml"
SYSTEM_CASCADE_PATH = Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml" if hasattr(cv2, "data") and hasattr(cv2.data, "haarcascades") else None
HAAR_CASCADE_PATH = LOCAL_CASCADE_PATH if LOCAL_CASCADE_PATH.exists() else SYSTEM_CASCADE_PATH

FACE_SCALE_FACTOR = 1.1
FACE_MIN_NEIGHBORS = 5
FACE_MIN_SIZE = (30, 30)

# Motion Detection Parameters (MOG2)
MOTION_HISTORY = 500
MOTION_VAR_THRESHOLD = 16
MOTION_DETECT_SHADOWS = True
# Cutoff at 200 because MOG2 marks shadows as ~127; cutting at 200 keeps only true foreground (255)
MOTION_SHADOW_THRESHOLD = 200
# Contours with area less than 800px are treated as noise (e.g., small camera jitter)
MOTION_MIN_CONTOUR_AREA = 800
MOTION_KERNEL_SIZE = (3, 3)

# Object Counter Parameters
# Filter out small specks (< 300px) and whole-frame boundaries (> 250000px)
OBJECT_MIN_CONTOUR_AREA = 300
OBJECT_MAX_CONTOUR_AREA = 250000
OBJECT_ADAPTIVE_BLOCK_SIZE = 11
OBJECT_ADAPTIVE_C = 2
