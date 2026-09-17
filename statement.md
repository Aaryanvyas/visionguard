# VisionGuard — Project Statement

## 1. Problem Statement
Manual visual surveillance and optical inspection — such as monitoring continuous security video feeds for intrusion, detecting human presence in photographs, or manually counting physical items on assembly lines and in inventory images — is labor-intensive, error-prone, and fails to scale. While deep learning offers high theoretical accuracy, modern neural network frameworks often impose heavy GPU dependencies, massive pre-trained model downloads (hundreds of megabytes or gigabytes), complex runtime configurations, and non-deterministic cloud latency.

Organizations, hobbyists, smart camera developers, and academic evaluators require a lightweight, deterministic, completely offline Computer Vision toolkit that solves core surveillance and inspection tasks using robust classical algorithms without external network calls or specialized hardware.

## 2. Scope of the Project
VisionGuard addresses this problem by packaging four foundational Computer Vision tasks into a modular, production-grade Command-Line Interface (CLI) application backed by local SQLite persistence and automated reporting:

1. **Face Detection**: Fast Haar Cascade detection of frontal human faces with bounding box annotations.
2. **Motion Detection**: Robust background subtraction using Gaussian Mixture Models (MOG2) with shadow suppression and morphological noise filtration to identify moving entities in video streams.
3. **Object Counting**: Geometric contour hierarchy analysis and adaptive Gaussian thresholding to identify, count, measure, and enumerate discrete physical objects.
4. **Image Enhancement**: Spatial and frequency-domain digital image processing filters (Canny edge detection, histogram equalization across YCrCb luminance, Gaussian smoothing, sharpening, and adaptive binarization).
5. **Data Logging & Reporting**: Relational SQLite event logging (`sessions` and `detections` tables) with automated export to structured JSON, tabular CSV, and graphical Matplotlib summary charts.

The scope strictly prioritizes reproducibility, zero runtime network dependencies, deterministic execution, and complete terminal executability.

## 3. Target Users
- **Students and Academic Evaluators**: Seeking an end-to-end, reproducible reference implementation of classical computer vision techniques with comprehensive automated test coverage and zero setup friction.
- **Edge / Embedded Developers**: Building offline smart cameras (e.g., Raspberry Pi doorbell or perimeter monitor) requiring low memory footprint and no subscription-based cloud AI.
- **Quality Control & Warehouse Operators**: Requiring rapid, deterministic counting of components or items from standard top-down image captures.
- **Security & Facility Technicians**: Requiring lightweight motion logging and audit history without streaming raw video over external networks.

## 4. High-Level Features
- **Deterministic & Offline**: Bundles all necessary cascade classifiers and sample datasets. No internet connection or model downloads needed.
- **Unified Modular CLI**: Clean, intuitive argparse interface with `--help` documentation on all subcommands (`faces`, `motion`, `count`, `enhance`, `report`, `history`).
- **Relational Persistence (SQLite)**: Automatically audits every processing invocation, tracking timestamps, parameters, outcomes, and bounding box coordinates.
- **Multi-Format Export**: One-command generation of audit reports in JSON, CSV, and high-resolution graphical bar charts.
- **Comprehensive Pytest Suite**: 31 automated unit and integration tests verifying invariants, edge cases, and end-to-end pipelines.
- **Resource Efficient**: Streams video frame-by-frame without loading full media into RAM; utilizes headless Matplotlib rendering (`Agg`).
