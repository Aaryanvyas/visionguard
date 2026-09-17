# VisionGuard — Project Statement

**Student Name**: Aryan Vyas  
**Registration Number**: 24BAI10343  
**Course**: Computer Vision  
**Project Type**: Build Your Own Project (Flipped Course Evaluation)  
**Submission Platform**: VITyarthi  

---

## 1. Problem Statement
Manual visual monitoring — such as watching a continuous CCTV feed for motion, checking whether a person is present in a photograph, or counting items in an inventory image — is repetitive, tiring, and prone to human error. While deep learning models offer high theoretical accuracy, in practice they often demand heavy GPU hardware, large pretrained weight files (often hundreds of megabytes), complex CUDA environments, and non-deterministic cloud latency.

For small teams, students, hobbyists, or edge deployments (such as a Raspberry Pi doorbell or room monitor), there is a practical need for a lightweight, completely offline computer-vision toolkit that handles everyday visual inspection and monitoring tasks using well-understood, classical algorithms with zero setup headache.

## 2. Scope of the Project
VisionGuard addresses this need by packaging four fundamental computer-vision tasks into a modular, offline Command-Line Interface (CLI) application backed by local SQLite logging:

1. **Face Detection**: Fast frontal face detection using OpenCV's Haar Cascade classifier, with contrast equalization for varying room lighting.
2. **Motion Detection**: Background subtraction using Gaussian Mixture Models (MOG2), with shadow elimination and morphological cleanup to log real motion in video files.
3. **Object Counting**: Geometric segmentation using adaptive Gaussian thresholding and contour extraction to detect, number, and measure discrete items.
4. **Image Enhancement**: A filter registry providing spatial and frequency-domain digital enhancements (Canny edges, YCrCb histogram equalization, Gaussian blur, Laplacian sharpening, adaptive binarization).
5. **Audit Logging & Reporting**: Every run is recorded in a local SQLite database (`sessions` and `detections` tables) with automated export to formatted JSON, CSV, and Matplotlib analytics charts.

The scope strictly prioritizes 100% offline executability, deterministic test verification, and clean terminal execution without any GUI dependencies.

## 3. Target Users
- **Students & Evaluators**: Anyone looking for a clean, runnable, well-tested reference implementation of classical CV techniques that works out of the box with zero downloads.
- **Makers & Embedded Developers**: Builders creating lightweight smart camera monitors (e.g. Raspberry Pi) who need fast, low-RAM alerts without paying for cloud AI subscriptions.
- **Small-Scale QC & Inventory**: Operators needing a quick way to count objects or components in top-down photos with area and perimeter statistics.

## 4. High-Level Features
- **Zero Runtime Downloads**: Bundles the Haar cascade XML and sample media directly in the repo; runs completely offline.
- **Clean CLI Interface**: Discoverable argparse commands (`faces`, `motion`, `count`, `enhance`, `report`, `history`) with `--help` documentation on each.
- **Relational Event Persistence**: SQLite records session timestamps, parameters, outcomes, and exact bounding box coordinates with foreign key constraints.
- **Automated Reporting**: One command generates structured JSON, tabular CSV, and clean Matplotlib charts comparing detection counts across recent runs.
- **Automated Test Suite**: 31 comprehensive pytest tests using synthetic mathematical fixtures to verify algorithms and prevent regressions.
- **Resource Friendly**: Streams video frame-by-frame instead of loading full files into memory; uses Matplotlib headless `Agg` backend.
