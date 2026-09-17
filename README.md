# VisionGuard
### Modular Computer Vision Surveillance & Analytics Toolkit

[![Tests](https://img.shields.io/badge/pytest-31%20passed-brightgreen.svg)](#instructions-for-testing)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](#license)
[![OpenCV](https://img.shields.io/badge/OpenCV-Classical%20CV-orange.svg)](https://opencv.org/)

VisionGuard is a modular, fully offline computer-vision toolkit built for the **Computer Vision** flipped course evaluation. It provides four classical CV modules — face detection, motion tracking, object counting, and image enhancement — with an embedded SQLite persistence layer and automated analytical reporting.

Designed to be completely reproducible, self-contained, and executable from the terminal with zero external model downloads or cloud dependencies.

---

## Student Information
- **Author**: Aryan Vyas
- **Registration Number**: 24BAI10343
- **Course**: Computer Vision
- **Evaluation**: Build Your Own Project (Flipped Course Evaluation)
- **Platform**: VITyarthi
- **Date**: September 17, 2026

---

## Table of Contents
- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Technologies & Tools Used](#technologiestools-used)
- [Installation & Environment Setup](#installation--environment-setup)
- [Command-Line Usage Guide](#command-line-usage-guide)
  - [1. Face Detection](#1-face-detection)
  - [2. Object Counting](#2-object-counting)
  - [3. Motion Detection in Video](#3-motion-detection-in-video)
  - [4. Image Enhancement Filters](#4-image-enhancement-filters)
  - [5. Session History](#5-session-history)
  - [6. Audit Reporting & Analytics](#6-audit-reporting--analytics)
- [Instructions for Testing](#instructions-for-testing)
- [Screenshots & Visual Results](#screenshots--visual-results)
- [Design Diagrams](#design-diagrams)
- [Project Structure](#project-structure)
- [Design Decisions & Implementation Notes](#design-decisions--implementation-notes)
- [License](#license)

---

## Project Overview
Manual visual surveillance and manual counting of objects are time-consuming and error-prone. While modern deep learning has its merits, it often requires heavy GPU hardware, large pretrained weight files (hundreds of MBs), complex CUDA setups, and non-deterministic cloud delays.

VisionGuard provides a clean, practical CLI alternative using classical computer-vision algorithms implemented in OpenCV and Python:
1. **Zero External Downloads at Run Time**: The required Haar cascade XML and sample media are bundled directly in the repository.
2. **Deterministic & Reproducible**: Automated test suite with synthetic fixtures asserting exact mathematical counts and invariants.
3. **Pure Terminal Executability**: Clean argparse sub-commands with sensible defaults, standard exit codes, and no required GUI.
4. **Relational Audit Trail**: Built-in SQLite database tracking every execution session and individual entity detection with strict foreign key integrity.

---

## Key Features
- **Face Detection (`faces`)**: Uses OpenCV's Haar Cascade classifier with histogram-equalization preprocessing so detections are stable under varied lighting.
- **Motion Detection (`motion`)**: Uses MOG2 background subtraction with shadow suppression (cutting at threshold 200 to ignore gray shadow pixels) and morphological opening/dilation.
- **Object Counting (`count`)**: Uses adaptive Gaussian thresholding (robust to uneven lighting) and contour hierarchy analysis to detect, measure, and number discrete objects.
- **Image Enhancement (`enhance`)**: A filter registry providing Canny edge detection, YCrCb histogram equalization, Gaussian blur, Laplacian sharpening, and adaptive thresholding.
- **Session Audit (`history`)**: Tabular CLI inspection of recent execution sessions, detection counts, and error states.
- **Analytical Reporting (`report`)**: Exports session findings to JSON and CSV, and generates an automated detection comparison chart across recent runs.

---

## System Architecture

```
                       +-----------------------------------+
                       |        Presentation Layer         |
                       |        (main.py / cli.py)         |
                       +-----------------+-----------------+
                                         |
     +-------------------+---------------+-------------------+--------------------+
     |                   |                                   |                    |
     v                   v                                   v                    v
+----+-------------+ +---+-----------------+       +---------+--------+ +---------+---------+
|   FaceDetector   | |   MotionDetector    |       |  ObjectCounter   | |   ImageUtils      |
| (Haar Cascades)  | |  (MOG2 Subtractor)  |       | (Contour Morph)  | | (Filter Registry) |
+----+-------------+ +---+-----------------+       +---------+--------+ +---------+---------+
     |                   |                                   |                    |
     +-------------------+---------------+-------------------+--------------------+
                                         |
                                         v
                         +---------------+---------------+
                         |   SQLite Persistence Layer    |
                         |   (sessions & detections)     |
                         +---------------+---------------+
                                         |
                                         v
                         +---------------+---------------+
                         |       Report Generator        |
                         |   (JSON, CSV, Analytics Bar)  |
                         +-------------------------------+
```

---

## Technologies & Tools Used
- **Language**: Python 3.10+ (tested on Python 3.12)
- **Computer Vision**: OpenCV (`opencv-python` >= 4.8.0)
- **Numerical Computing**: NumPy (`numpy` >= 1.24.0)
- **Data Visualization**: Matplotlib (`matplotlib` >= 3.7.0, headless `Agg` backend)
- **Database**: SQLite3 (Python standard library, relational schema with foreign keys)
- **Testing**: Pytest (`pytest` >= 7.4.0, isolated temporary DB fixtures & synthetic media)
- **PDF Report Generation**: ReportLab (`reportlab` >= 4.0.0)

---

## Installation & Environment Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Aaryanvyas/visionguard.git
cd visionguard
```

### 2. Create and Activate a Virtual Environment
**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```

---

## Command-Line Usage Guide

VisionGuard provides a unified CLI with subcommands. View help for any subcommand using `--help`:
```bash
python main.py --help
python main.py faces --help
python main.py motion --help
python main.py count --help
python main.py enhance --help
python main.py report --help
python main.py history --help
```

### 1. Face Detection
Detects human faces in an image, draws green bounding boxes, and records detections to SQLite.
```bash
python main.py faces --input data/samples/portrait.jpg --output data/output/faces_annotated.jpg
```
*Console Output:*
```
[faces] Detected 1 face(s). Saved -> data/output/faces_annotated.jpg
```

### 2. Object Counting
Detects and numbers discrete physical objects using adaptive thresholding and contour analysis.
```bash
python main.py count --input data/samples/shapes.png --output data/output/count_annotated.png
```
*Console Output:*
```
[count] Detected 7 object(s), avg area=4702.9px^2. Saved -> data/output/count_annotated.png
```

### 3. Motion Detection in Video
Processes video frames, subtracts background using MOG2, highlights moving objects in red, and saves an annotated video.
```bash
python main.py motion --input data/samples/motion_sample.mp4 --output data/output/motion_annotated.mp4
```
*Console Output:*
```
[motion] Processed 60 frame(s); 50 motion event(s). Saved -> data/output/motion_annotated.mp4
```

### 4. Image Enhancement Filters
Applies spatial and frequency-domain digital filters (`grayscale`, `blur`, `edges`, `hist_eq`, `adaptive_thresh`, `sharpen`).
```bash
python main.py enhance --input data/samples/portrait.jpg --output data/output/enhance_edges.jpg --filter edges
```
*Console Output:*
```
[enhance] Applied 'edges' filter. Saved -> data/output/enhance_edges.jpg
```

### 5. Session History
Displays a formatted tabular summary of previous analysis sessions stored in SQLite.
```bash
python main.py history --limit 5
```
*Console Output:*
```
ID   | Module           | Status     | Detections | Started At           | Source
--------------------------------------------------------------------------------
3    | motion_detection | completed  | 50         | 2026-09-17T10:20:57  | motion_sample.mp4
2    | object_counting  | completed  | 7          | 2026-09-17T10:20:48  | shapes.png
1    | face_detection   | completed  | 1          | 2026-09-17T10:20:29  | portrait.jpg
```

### 6. Audit Reporting & Analytics
Exports session findings to JSON and CSV, and generates a detection comparison chart across recent runs.
```bash
python main.py report --session-id 2 --chart
```
*Console Output:*
```
[report] Analytics chart generated -> data/output/session_analytics.png
[report] Full report generated for Session #2:
  - JSON: data/output/session_2_report.json
  - CSV:  data/output/session_2_detections.csv
  - Chart:data/output/analytics_chart.png
```

---

## Instructions for Testing

VisionGuard includes an automated test suite implemented in `pytest` containing **31 passing tests**. Tests use isolated temporary databases and synthetic mathematical media generators so they run fast, completely offline, and without flaky environmental dependencies.

Run the entire test suite:
```bash
python -m pytest tests/ -v
```

Expected Output:
```
============================= test session starts =============================
platform win32 -- Python 3.12.6, pytest-9.1.1
collected 31 items

tests/test_database.py::test_init_db_creates_tables PASSED               [  3%]
tests/test_database.py::test_start_and_finish_session PASSED             [  6%]
tests/test_database.py::test_log_single_detection PASSED                 [  9%]
tests/test_database.py::test_log_detections_batch PASSED                 [ 12%]
tests/test_database.py::test_list_sessions_returns_correct_counts PASSED [ 16%]
tests/test_database.py::test_failed_session_status_logging PASSED        [ 19%]
tests/test_face_detection.py::test_face_detection_blank_image_finds_zero PASSED [ 22%]
tests/test_face_detection.py::test_face_detection_sample_portrait_finds_face PASSED [ 25%]
tests/test_face_detection.py::test_face_detection_annotation_modifies_image PASSED [ 29%]
tests/test_face_detection.py::test_face_detection_invalid_path_raises PASSED [ 32%]
tests/test_face_detection.py::test_face_detection_end_to_end_with_db PASSED [ 35%]
tests/test_image_utils.py::test_validate_image_path_valid PASSED         [ 38%]
tests/test_image_utils.py::test_validate_image_path_nonexistent PASSED   [ 41%]
tests/test_image_utils.py::test_validate_image_path_invalid_extension PASSED [ 45%]
tests/test_image_utils.py::test_grayscale_filter_shape PASSED            [ 48%]
tests/test_image_utils.py::test_gaussian_blur_dtype_and_shape PASSED     [ 51%]
tests/test_image_utils.py::test_canny_edges_binary_output PASSED         [ 54%]
tests/test_image_utils.py::test_histogram_equalization_bgr PASSED        [ 58%]
tests/test_image_utils.py::test_adaptive_threshold_binary PASSED         [ 61%]
tests/test_image_utils.py::test_sharpen_filter PASSED                    [ 64%]
tests/test_image_utils.py::test_invalid_filter_name_raises PASSED        [ 67%]
tests/test_image_utils.py::test_draw_bounding_box PASSED                 [ 70%]
tests/test_motion_detection.py::test_motion_detector_initialization PASSED [ 74%]
tests/test_motion_detection.py::test_motion_detector_static_frame_no_motion PASSED [ 77%]
tests/test_motion_detection.py::test_motion_detector_moving_object_detected PASSED [ 80%]
tests/test_motion_detection.py::test_motion_detector_video_processing_pipeline PASSED [ 83%]
tests/test_object_counter.py::test_object_counter_initialization PASSED  [ 87%]
tests/test_object_counter.py::test_object_counter_blank_image_finds_zero PASSED [ 90%]
tests/test_object_counter.py::test_object_counter_exact_count_synthetic_4_shapes PASSED [ 93%]
tests/test_object_counter.py::test_object_counter_exact_count_sample_7_shapes PASSED [ 96%]
tests/test_object_counter.py::test_object_counter_end_to_end_with_db PASSED [100%]

============================= 31 passed in 1.89s ==============================
```

---

## Screenshots & Visual Results

| Module | Result Preview | Description |
| :--- | :---: | :--- |
| **Face Detection** | `data/output/faces_annotated.jpg` | Bounding box detected on portrait (1 face found). |
| **Object Counting** | `data/output/count_annotated.png` | 7 discrete geometric shapes segmented and numbered. |
| **Motion Detection** | `data/output/motion_frame.jpg` | Moving object localized in red box during video stream. |
| **Canny Edge Filter** | `data/output/enhance_edges.jpg` | High-frequency gradient edge map of input image. |
| **Session Analytics** | `data/output/session_analytics.png` | Automated bar chart of detections per session. |

---

## Design Diagrams
All high-resolution system design diagrams are located in `docs/diagrams/`:
- **System Architecture**: `docs/diagrams/architecture.png`
- **Use Case Diagram**: `docs/diagrams/use_case.png`
- **Process Workflow**: `docs/diagrams/workflow.png`
- **Class / Component Diagram**: `docs/diagrams/class_diagram.png`
- **Sequence Diagram**: `docs/diagrams/sequence_diagram.png`
- **Entity-Relationship Diagram**: `docs/diagrams/er_diagram.png`

---

## Project Structure
```
visionguard/
├── .gitignore
├── requirements.txt
├── README.md                      # Complete project documentation
├── statement.md                   # Problem statement, scope, target users
├── main.py                        # Top-level CLI entry point
├── generate_report.py             # Script to compile academic PDF report
├── VisionGuard_Project_Report.pdf # 13-page academic report (under 1MB)
├── src/
│   ├── __init__.py                # Package metadata (Aryan Vyas, 24BAI10343)
│   ├── config.py                  # Hyperparameters, paths, and thresholds
│   ├── logger_setup.py            # Dual console & rotating file logging
│   ├── database.py                # SQLite schema & persistence layer
│   ├── image_utils.py             # Validation, resizing, and 6 enhancement filters
│   ├── face_detection.py          # Haar cascade face detection pipeline
│   ├── motion_detection.py        # MOG2 background subtractor & morphology
│   ├── object_counter.py          # Adaptive thresholding & contour hierarchy
│   ├── report_generator.py        # JSON/CSV exporter & Matplotlib analytics
│   └── cli.py                     # Argparse command dispatcher
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Pytest fixtures (temporary DB, mock media)
│   ├── test_image_utils.py        # Image validation & filter invariants (9 tests)
│   ├── test_face_detection.py     # Face detector behavior & edge cases (5 tests)
│   ├── test_motion_detection.py   # Motion detector video processing (4 tests)
│   ├── test_object_counter.py     # Contour counting accuracy (5 tests)
│   └── test_database.py           # Database CRUD & session lifecycle (7 tests)
├── data/
│   ├── models/                    # Bundled offline Haar cascade XML
│   ├── samples/                   # Bundled sample images & synthetic video
│   └── output/                    # Annotated images, videos, reports & charts
├── docs/
│   ├── generate_diagrams.py       # Diagram rendering script
│   └── diagrams/                  # 6 architecture and UML diagrams
└── logs/                          # Rotating execution audit logs
```

---

## Design Decisions & Implementation Notes
- **Why Classical CV?** Deep learning models are impressive, but they introduce heavy weight files, CUDA version mismatches, and hardware barriers. For focused tasks like face detection and object counting, classical techniques (Haar Cascades, MOG2, and contour analysis) run fast on CPU with zero setup hurdles.
- **MOG2 Shadow Suppression**: OpenCV's MOG2 background subtractor marks shadow pixels with gray (~127). We apply a threshold cut at 200 so moving shadows are not falsely logged as motion events.
- **Adaptive vs. Global Thresholding**: For object counting, lighting is rarely uniform across the entire image. Adaptive Gaussian thresholding calculates local thresholds for small pixel neighborhoods, yielding clean shape contours even if one corner is darker than another.
- **Deterministic Testing**: Rather than relying on external web datasets that might disappear or fail to download, the test suite generates synthetic geometric images and small videos programmatically. This ensures tests run in under 3 seconds on any machine.

---

## License
This project is open source and available under the [MIT License](LICENSE).
