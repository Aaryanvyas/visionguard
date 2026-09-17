import os
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
)
from reportlab.pdfgen import canvas

PROJECT_DIR = Path(r"C:\Users\Asus\.gemini\antigravity\scratch\visionguard")
OUTPUT_PDF = PROJECT_DIR / "VisionGuard_Project_Report.pdf"
DIAGRAMS_DIR = PROJECT_DIR / "docs" / "diagrams"
OUTPUT_DIR = PROJECT_DIR / "data" / "output"
SAMPLES_DIR = PROJECT_DIR / "data" / "samples"

class NumberedCanvas(canvas.Canvas):
    """Canvas that computes total page count dynamically for running footers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            # Suppress running footer on cover page
            if self._pageNumber > 1:
                self.setFont("Helvetica", 8.5)
                self.setFillColor(colors.HexColor("#718096"))
                self.drawRightString(letter[0] - 54, 36, f"Page {self._pageNumber} of {num_pages}")
                self.drawString(54, 36, "VisionGuard — Aryan Vyas (24BAI10343) | Computer Vision")
                self.setStrokeColor(colors.HexColor("#CBD5E0"))
                self.setLineWidth(0.5)
                self.line(54, 48, letter[0] - 54, 48)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

def build_pdf():
    doc = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=28,
        leading=34,
        textColor=colors.HexColor("#1A365D"),
        alignment=1
    )
    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=13,
        leading=18,
        textColor=colors.HexColor("#2B6CB0"),
        alignment=1
    )
    section_heading = ParagraphStyle(
        "SectionHeading",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=14.5,
        leading=18.5,
        textColor=colors.HexColor("#1A365D"),
        spaceBefore=10,
        spaceAfter=5
    )
    subheading = ParagraphStyle(
        "SubHeading",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14.5,
        textColor=colors.HexColor("#2B6CB0"),
        spaceBefore=7,
        spaceAfter=3
    )
    body = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.2,
        leading=13.2,
        textColor=colors.HexColor("#2D3748"),
        spaceBefore=2,
        spaceAfter=4
    )
    bullet = ParagraphStyle(
        "Bullet",
        parent=body,
        leftIndent=14,
        firstLineIndent=-10,
        spaceBefore=1,
        spaceAfter=2
    )
    fig_caption = ParagraphStyle(
        "Caption",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#718096"),
        alignment=1,
        spaceBefore=3,
        spaceAfter=5
    )
    code_box = ParagraphStyle(
        "CodeBox",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=7.8,
        leading=11,
        textColor=colors.HexColor("#1A202C")
    )

    story = []

    # ================= PAGE 1: COVER PAGE =================
    story.append(Spacer(1, 110))
    story.append(Paragraph("VisionGuard", title_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Modular Computer Vision Surveillance & Analytics Toolkit", subtitle_style))
    story.append(Spacer(1, 50))
    story.append(Paragraph("<b>Project Report</b>", ParagraphStyle("CoverPR", fontName="Helvetica-Bold", fontSize=13.5, textColor=colors.HexColor("#1A202C"))))
    story.append(Spacer(1, 16))

    cover_meta = [
        [Paragraph("<b>Student Name</b>", body), Paragraph("Aryan Vyas", body)],
        [Paragraph("<b>Registration No.</b>", body), Paragraph("24BAI10343", body)],
        [Paragraph("<b>Course</b>", body), Paragraph("Computer Vision", body)],
        [Paragraph("<b>Project Type</b>", body), Paragraph("Build Your Own Project (Flipped Course Evaluation)", body)],
        [Paragraph("<b>Submission Platform</b>", body), Paragraph("VITyarthi", body)],
        [Paragraph("<b>Report Date</b>", body), Paragraph("September 17, 2026", body)],
    ]
    meta_table = Table(cover_meta, colWidths=[150, 350])
    meta_table.setStyle(TableStyle([
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 5.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5.5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(meta_table)
    story.append(PageBreak())

    # ================= PAGE 2: INTRO, PROBLEM, SCOPE, FRs =================
    story.append(Paragraph("2. Introduction", section_heading))
    story.append(Paragraph(
        "VisionGuard is a modular, fully offline computer-vision toolkit built for the Computer Vision course's flipped "
        "evaluation. Rather than depending on a single fixed dataset or task, the project provides four independent, "
        "CLI-driven modules — face detection, motion detection, object counting and image enhancement — each backed by "
        "a common data-logging and reporting layer built on SQLite.",
        body
    ))
    story.append(Paragraph(
        "The guiding design goal was reproducibility: every module works out of the box on any machine with Python and OpenCV "
        "installed, uses only classical, well-understood computer-vision algorithms (Haar cascades, background subtraction, "
        "contour analysis, spatial filters), and requires no GPU, no external model downloads and no internet connection at run time.",
        body
    ))

    story.append(Spacer(1, 6))
    story.append(Paragraph("3. Problem Statement", section_heading))
    story.append(Paragraph(
        "Manual visual monitoring — watching a video feed for motion, checking whether a person appears in a photo, or counting "
        "items in an image — is repetitive and does not scale. Individuals and small teams often need basic computer-vision "
        "capabilities without the cost and complexity of a full deep-learning / cloud-based pipeline.",
        body
    ))
    story.append(Paragraph(
        "VisionGuard solves this by packaging four common CV tasks into a single, lightweight, offline CLI tool, with every "
        "analysis run persisted to a local database for later review, export, and charting.",
        body
    ))

    story.append(Paragraph("Target Users", subheading))
    story.append(Paragraph("• <b>Students/hobbyists</b> who want a runnable reference implementation of classical CV techniques.", bullet))
    story.append(Paragraph("• <b>Small-scale \"smart camera\" makers</b> (e.g. Raspberry Pi doorbell/shed monitor) needing simple alerts without a cloud subscription.", bullet))
    story.append(Paragraph("• <b>Instructors/evaluators</b> who need a self-contained, reproducible project to review end-to-end.", bullet))

    story.append(Spacer(1, 6))
    story.append(Paragraph("4. Functional Requirements", section_heading))
    story.append(Paragraph("The project implements four major functional modules, each with a clear input/output structure and a logical CLI-driven workflow:", body))
    story.append(Paragraph("• <b>FR-1 Face Detection:</b> Given an input image, detect all faces present and produce an annotated output image with bounding boxes; log each detected face to the database.", bullet))
    story.append(Paragraph("• <b>FR-2 Motion Detection:</b> Given an input video, detect frames/regions containing significant motion using background subtraction; produce an annotated output video and log each motion event.", bullet))
    story.append(Paragraph("• <b>FR-3 Object Counting:</b> Given an input image, count discrete objects via contour analysis and report count plus per-object area/perimeter statistics; produce an annotated output image.", bullet))
    story.append(Paragraph("• <b>FR-4 Image Enhancement:</b> Given an input image and a chosen filter (grayscale, blur, edge-detection, histogram equalisation, adaptive threshold, sharpen), produce the filtered output image.", bullet))
    story.append(Paragraph("• <b>FR-5 Reporting:</b> Given a session ID, export that session's detections to JSON and CSV, and generate a bar chart comparing detection counts across recent sessions.", bullet))
    story.append(Paragraph("• <b>FR-6 Session History:</b> List recent analysis sessions (module, status, source file) from the database.", bullet))
    story.append(PageBreak())

    # ================= PAGE 3: NON-FUNCTIONAL REQUIREMENTS =================
    story.append(Paragraph("5. Non-functional Requirements", section_heading))
    story.append(Spacer(1, 4))

    nfr_data = [
        [Paragraph("<b>NFR</b>", body), Paragraph("<b>Requirement</b>", body), Paragraph("<b>How it is addressed</b>", body)],
        [
            Paragraph("<b>Performance</b>", body),
            Paragraph("Processing should stay responsive on commodity hardware.", body),
            Paragraph("Frames/images are downscaled to a max width before processing; OpenCV's optimised C backends are used throughout.", body)
        ],
        [
            Paragraph("<b>Security</b>", body),
            Paragraph("Reject malformed or unsafe input before processing.", body),
            Paragraph("All file paths/extensions are validated (allow-list) before any file I/O; no shell/eval of user input.", body)
        ],
        [
            Paragraph("<b>Usability</b>", body),
            Paragraph("The tool should be usable without reading source code.", body),
            Paragraph("Discoverable argparse CLI with --help on every sub-command and sensible defaults.", body)
        ],
        [
            Paragraph("<b>Reliability</b>", body),
            Paragraph("A failure in one run should not corrupt state or crash silently.", body),
            Paragraph("Every processing function wraps its logic in try/except, logs the error, and marks the DB session 'failed'.", body)
        ],
        [
            Paragraph("<b>Scalability</b>", body),
            Paragraph("Should handle processing many files without code changes.", body),
            Paragraph("Each module operates on one file per invocation, so batches can be driven by a simple shell loop; DB schema supports unbounded sessions/detections.", body)
        ],
        [
            Paragraph("<b>Maintainability</b>", body),
            Paragraph("Codebase should be easy to extend and reason about.", body),
            Paragraph("Single-responsibility modules, centralised configuration (config.py), docstrings, and a pytest suite guarding against regressions.", body)
        ],
        [
            Paragraph("<b>Logging / Monitoring</b>", body),
            Paragraph("Every operation should leave an audit trail.", body),
            Paragraph("Rotating file handler (logs/visionguard.log) plus console output; every DB session records start/finish time and status.", body)
        ],
        [
            Paragraph("<b>Resource efficiency</b>", body),
            Paragraph("Avoid unnecessary memory/CPU use.", body),
            Paragraph("Video frames are streamed one at a time (never loaded fully into memory); Matplotlib uses the headless Agg backend.", body)
        ],
    ]

    t_nfr = Table(nfr_data, colWidths=[100, 160, 240])
    t_nfr.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1A365D")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0, 0), (-1, -1), 5.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFC")]),
    ]))
    story.append(t_nfr)
    story.append(PageBreak())

    # ================= PAGE 4: ARCHITECTURE & USE CASE =================
    story.append(Paragraph("6. System Architecture", section_heading))
    story.append(Paragraph(
        "VisionGuard follows a simple layered architecture. The <b>Presentation Layer</b> (a single argparse-based CLI) "
        "dispatches to one of four <b>Core Processing Modules</b>. Every core module shares two cross-cutting "
        "<b>Support Services</b> — centralised configuration and logging — and writes its results into a shared "
        "<b>Data & Reporting Layer</b> built on SQLite, which the Report Generator reads back to produce CSV/JSON/chart outputs.",
        body
    ))
    story.append(Spacer(1, 3))
    if (DIAGRAMS_DIR / "architecture.png").exists():
        story.append(Image(str(DIAGRAMS_DIR / "architecture.png"), width=440, height=195))
        story.append(Paragraph("Figure 6.1 — System Architecture Diagram", fig_caption))

    story.append(Spacer(1, 4))
    story.append(Paragraph("7. Design Diagrams", section_heading))
    story.append(Paragraph("7.1 Use Case Diagram", subheading))
    story.append(Paragraph("The system supports one primary actor (the Student/Evaluator running the CLI) and six use cases:", body))
    if (DIAGRAMS_DIR / "use_case.png").exists():
        story.append(Image(str(DIAGRAMS_DIR / "use_case.png"), width=360, height=175))
        story.append(Paragraph("Figure 7.1 — Use Case Diagram", fig_caption))

    story.append(Paragraph("7.2 Workflow / Process Flow Diagram", subheading))
    story.append(PageBreak())

    # ================= PAGE 5: PROCESS WORKFLOW =================
    story.append(Paragraph(
        "Every CLI command follows the same high-level workflow: validate input, open a database session, "
        "process the media, persist detections, annotate and save the output, then finalise the session.",
        body
    ))
    story.append(Spacer(1, 30))
    if (DIAGRAMS_DIR / "workflow.png").exists():
        story.append(Image(str(DIAGRAMS_DIR / "workflow.png"), width=500, height=155))
        story.append(Paragraph("Figure 7.2 — Process Workflow Diagram", fig_caption))
    story.append(PageBreak())

    # ================= PAGE 6: CLASS, SEQUENCE, ER DIAGRAMS =================
    story.append(Paragraph("7.3 Class / Component Diagram", subheading))
    if (DIAGRAMS_DIR / "class_diagram.png").exists():
        story.append(Image(str(DIAGRAMS_DIR / "class_diagram.png"), width=390, height=165))
        story.append(Paragraph("Figure 7.3 — Class / Component Diagram", fig_caption))

    story.append(Spacer(1, 3))
    story.append(Paragraph("7.4 Sequence Diagram", subheading))
    story.append(Paragraph("Sequence for a typical detection run (e.g. <font name='Courier'>python main.py faces ...</font>):", body))
    if (DIAGRAMS_DIR / "sequence_diagram.png").exists():
        story.append(Image(str(DIAGRAMS_DIR / "sequence_diagram.png"), width=390, height=160))
        story.append(Paragraph("Figure 7.4 — Sequence Diagram", fig_caption))

    story.append(Spacer(1, 3))
    story.append(Paragraph("7.5 ER Diagram / Schema Design", subheading))
    story.append(Paragraph(
        "VisionGuard uses two related SQLite tables: <b>sessions</b> (one row per CLI invocation) and <b>detections</b> "
        "(one row per face/motion-event/object found during that session), related 1-to-many via <font name='Courier'>session_id</font>.",
        body
    ))
    if (DIAGRAMS_DIR / "er_diagram.png").exists():
        story.append(Image(str(DIAGRAMS_DIR / "er_diagram.png"), width=390, height=125))
        story.append(Paragraph("Figure 7.5 — Entity-Relationship Diagram", fig_caption))
    story.append(PageBreak())

    # ================= PAGE 7: DESIGN DECISIONS & IMPLEMENTATION =================
    story.append(Paragraph("8. Design Decisions & Rationale", section_heading))
    story.append(Paragraph("• <b>Classical CV over deep learning:</b> Haar cascades, MOG2 background subtraction and contour analysis were chosen over DNN-based detectors so the project runs on any machine with no model downloads, no GPU, and fully deterministic offline behaviour — important for grading reproducibility.", bullet))
    story.append(Paragraph("• <b>SQLite over a full DBMS:</b> SQLite requires no server process, ships with Python's standard library via the sqlite3 module, and is sufficient for the write-then-read reporting pattern this project needs, while still giving a genuine relational schema (sessions/detections) to design around.", bullet))
    story.append(Paragraph("• <b>CLI over GUI:</b> The submission requirements explicitly call for a project that is fully executable via the command line; a CLI also makes automated evaluation and scripting straightforward.", bullet))
    story.append(Paragraph("• <b>Session/Detection separation:</b> Splitting 'one row per run' (sessions) from 'one row per finding' (detections) keeps the schema normalised and allows the Reporting module to aggregate at either granularity.", bullet))
    story.append(Paragraph("• <b>Centralised config.py:</b> All thresholds (contour area cut-offs, Haar cascade parameters, frame-resize width) live in one file so behaviour can be tuned without touching business logic.", bullet))
    story.append(Paragraph("• <b>Fail-safe sessions:</b> Every processing function is wrapped so that an exception still results in a 'failed' session row (with the error message) rather than a silent crash or a dangling 'running' row.", bullet))

    story.append(Spacer(1, 6))
    story.append(Paragraph("9. Implementation Details", section_heading))
    story.append(Paragraph("9.1 Face Detection", subheading))
    story.append(Paragraph(
        "Implemented in <font name='Courier'>src/face_detection.py</font> using OpenCV's bundled "
        "<font name='Courier'>haarcascade_frontalface_default.xml</font> classifier. The image is converted to grayscale, then "
        "<font name='Courier'>detectMultiScale</font> is run with a scale factor of 1.1 and a minimum neighbour count of 5 to balance recall against false positives.",
        body
    ))

    story.append(Paragraph("9.2 Motion Detection", subheading))
    story.append(Paragraph(
        "Implemented in <font name='Courier'>src/motion_detection.py</font> using <font name='Courier'>cv2.createBackgroundSubtractorMOG2</font>. "
        "Each frame's foreground mask is thresholded to remove shadow pixels, cleaned with a morphological opening operation, and external contours above a minimum area are reported as motion events with their bounding boxes.",
        body
    ))

    story.append(Paragraph("9.3 Object Counting", subheading))
    story.append(Paragraph(
        "Implemented in <font name='Courier'>src/object_counter.py</font>. An adaptive Gaussian threshold is applied (robust to uneven lighting), followed by external contour detection. Contours below a configurable minimum area are discarded as noise; the remainder are reported with bounding box, area, and perimeter.",
        body
    ))

    story.append(Paragraph("9.4 Image Enhancement", subheading))
    story.append(Paragraph(
        "Implemented in <font name='Courier'>src/image_utils.py</font> as a small filter registry (grayscale, Gaussian blur, Canny edge detection, YCrCb-channel histogram equalisation, adaptive threshold, and a 3x3 sharpening kernel), selected by name from the CLI.",
        body
    ))

    story.append(Paragraph("9.5 Data Persistence & Reporting", subheading))
    story.append(PageBreak())

    # ================= PAGE 8: DATA PERSISTENCE & FILE COUNT =================
    story.append(Paragraph(
        "<font name='Courier'>src/database.py</font> owns the SQLite schema and exposes simple functions (start_session, log_detection, finish_session) "
        "used by every detection module. <font name='Courier'>src/report_generator.py</font> reads that data back to produce JSON/CSV exports and a Matplotlib bar chart of recent sessions.",
        body
    ))
    story.append(Spacer(1, 10))
    story.append(Paragraph("9.6 Module / File Count", section_heading))
    story.append(Paragraph(
        "The implementation is split across 9 focused source modules plus 5 test modules (14 Python files total), satisfying the 'minimum 5–10 meaningful modules' technical expectation: "
        "<font name='Courier'>config.py, logger_setup.py, database.py, image_utils.py, face_detection.py, motion_detection.py, object_counter.py, report_generator.py, cli.py</font>.",
        body
    ))
    story.append(PageBreak())

    # ================= PAGE 9: SCREENSHOTS (FACES & OBJECT COUNTING) =================
    story.append(Paragraph("10. Screenshots / Results", section_heading))
    story.append(Paragraph("10.1 Face Detection", subheading))
    if (OUTPUT_DIR / "faces_annotated.jpg").exists():
        story.append(Image(str(OUTPUT_DIR / "faces_annotated.jpg"), width=210, height=210))
        story.append(Paragraph("Figure 10.1 — Face detected on a sample portrait (1 face found).", fig_caption))

    story.append(Spacer(1, 8))
    story.append(Paragraph("10.2 Object Counting", subheading))
    if (OUTPUT_DIR / "count_annotated.png").exists():
        story.append(Image(str(OUTPUT_DIR / "count_annotated.png"), width=230, height=195))
        story.append(Paragraph("Figure 10.2 — 7 synthetic shapes correctly counted and numbered.", fig_caption))
    story.append(PageBreak())

    # ================= PAGE 10: SCREENSHOTS (MOTION & ENHANCEMENT) =================
    story.append(Paragraph("10.3 Motion Detection", subheading))
    if (OUTPUT_DIR / "motion_frame.jpg").exists():
        story.append(Image(str(OUTPUT_DIR / "motion_frame.jpg"), width=250, height=185))
        story.append(Paragraph("Figure 10.3 — A frame from the annotated output video; the moving object is boxed in red.", fig_caption))

    story.append(Spacer(1, 8))
    story.append(Paragraph("10.4 Image Enhancement (Canny Edge Detection)", subheading))
    if (OUTPUT_DIR / "enhance_edges.jpg").exists():
        story.append(Image(str(OUTPUT_DIR / "enhance_edges.jpg"), width=210, height=210))
        story.append(Paragraph("Figure 10.4 — Edge-detection filter applied to the sample portrait.", fig_caption))
    story.append(PageBreak())

    # ================= PAGE 11: ANALYTICS & TESTING APPROACH =================
    story.append(Paragraph("10.5 Analytics Report", subheading))
    if (OUTPUT_DIR / "session_analytics.png").exists():
        story.append(Image(str(OUTPUT_DIR / "session_analytics.png"), width=340, height=170))
        story.append(Paragraph("Figure 10.5 — Auto-generated bar chart of detections per recent session, produced by the `report` command.", fig_caption))

    story.append(Spacer(1, 4))
    story.append(Paragraph("Console output summary from an end-to-end run:", body))

    console_snippet = (
        "[faces] Detected 1 face(s). Saved -> data/output/faces_annotated.jpg<br/>"
        "[count] Detected 7 object(s), avg area=4702.9px^2. Saved -> data/output/count_annotated.png<br/>"
        "[motion] Processed 60 frame(s); 50 motion event(s). Saved -> data/output/motion_annotated.mp4<br/>"
        "[enhance] Applied 'edges' filter. Saved -> data/output/enhance_edges.jpg"
    )
    t_cons = Table([[Paragraph(console_snippet, code_box)]], colWidths=[500])
    t_cons.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EDF2F7")),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_cons)

    story.append(Spacer(1, 6))
    story.append(Paragraph("11. Testing Approach", section_heading))
    story.append(Paragraph(
        "The project uses pytest with 31 unit/integration tests spread across five test modules. Rather than relying on external datasets "
        "(which would make tests flaky, slow, or dependent on network access), tests generate deterministic synthetic fixtures at run time:",
        body
    ))
    story.append(Paragraph("• <b>Image filters</b> are tested against a fixed-seed random NumPy array (shape/dtype invariants, binary-output checks for Canny/adaptive-threshold).", bullet))
    story.append(Paragraph("• <b>Face detection</b> is tested both against a blank image (expects zero detections) and the bundled sample portrait (expects ≥1 detection), plus an end-to-end pipeline test.", bullet))
    story.append(Paragraph("• <b>Motion detection</b> is tested against a synthetically generated video containing a moving rectangle on a static background, verifying that motion events are only raised once the background model stabilises.", bullet))
    story.append(Paragraph("• <b>Object counting</b> is tested against a synthetically drawn image with a known number of shapes (4 or 7, depending on the test) so the expected count is exact, not approximate.", bullet))
    story.append(Paragraph("• <b>Database layer</b> is tested against an isolated temporary SQLite file per test (via a pytest fixture with monkeypatching), covering session lifecycle, detection logging, and error handling for unknown session IDs.", bullet))
    story.append(Spacer(1, 3))
    story.append(Paragraph("<b>Result:</b> all 31 tests pass (<font name='Courier'>python -m pytest tests/ -v</font>). This test suite also documents expected behaviour for future maintainers and would catch regressions if detection thresholds in config.py were changed carelessly.", body))
    story.append(PageBreak())

    # ================= PAGE 12: CHALLENGES, LEARNINGS, FUTURE ENHANCEMENTS =================
    story.append(Paragraph("12. Challenges Faced", section_heading))
    story.append(Paragraph(
        "• <b>Tuning motion-detection sensitivity:</b> the MOG2 background subtractor initially reported zero motion events on small synthetic test videos "
        "because the default minimum-contour-area threshold (tuned for realistic frame sizes) was larger than the moving object's foreground pixel count "
        "in a postage-stamp-sized test frame. This was resolved by using a more realistically sized synthetic video in tests and by using an explicit structuring "
        "element for the morphological cleanup step (a bare 'None' kernel was silently ineffective).",
        bullet
    ))
    story.append(Paragraph(
        "• <b>Shadow suppression:</b> MOG2's shadow-detection marks shadow pixels with an intermediate grey value (127) rather than white (255); the threshold "
        "step had to explicitly cut at 200 to exclude shadows from being counted as motion, otherwise moving shadows caused false positives.",
        bullet
    ))
    story.append(Paragraph(
        "• <b>Choosing a face-detection approach that needs no downloads:</b> many modern face detectors require downloading pretrained weights at run time, "
        "which would break offline/reproducible evaluation. Bundling OpenCV's official Haar cascade XML inside the repository avoided this entirely.",
        bullet
    ))
    story.append(Paragraph(
        "• <b>Keeping the SQLite layer test-isolated:</b> because database functions could access the default file, tests needed a fixture that supplies "
        "a temporary path per test so each test runs against a private, throwaway database file rather than the developer's real <font name='Courier'>visionguard.db</font>.",
        bullet
    ))

    story.append(Spacer(1, 6))
    story.append(Paragraph("13. Learnings & Key Takeaways", section_heading))
    story.append(Paragraph("• Classical computer-vision techniques (Haar cascades, background subtraction, contour analysis) remain highly practical for well-scoped problems and are far cheaper to deploy and evaluate than deep-learning pipelines.", bullet))
    story.append(Paragraph("• Designing tests around deterministic, self-generated synthetic data (rather than external datasets) makes a computer-vision test suite fast, offline, and exact — the object-counting tests, for example, can assert an exact expected count.", bullet))
    story.append(Paragraph("• Persisting analysis runs to a small relational schema (even for a CLI tool) makes reporting and later analysis dramatically easier than parsing log files.", bullet))
    story.append(Paragraph("• Centralising configuration and logging early made it much easier to tune thresholds (e.g. the motion-detection minimum contour area) in one place while debugging.", bullet))

    story.append(Spacer(1, 6))
    story.append(Paragraph("14. Future Enhancements", section_heading))
    story.append(Paragraph("• Swap the Haar cascade for a DNN-based face detector (e.g. an ONNX/Caffe SSD model) for higher accuracy in low-light or angled conditions, while keeping the same FaceDetector interface.", bullet))
    story.append(Paragraph("• Add multi-object tracking (e.g. via cv2.Tracker implementations or a Kalman filter) so objects/motion regions are tracked across frames rather than re-detected independently each frame.", bullet))
    story.append(Paragraph("• Expose the same core modules through a lightweight REST API (Flask/FastAPI) for integration into other systems, without changing the underlying processing code.", bullet))
    story.append(PageBreak())

    # ================= PAGE 13: FUTURE ENHANCEMENTS CONT & REFERENCES =================
    story.append(Paragraph("• Replace the hard-coded thresholds in config.py with an external YAML/JSON configuration file that can be edited without touching source code.", bullet))
    story.append(Paragraph("• Add face recognition (identity matching against an enrolled set) as an opt-in extension of the existing face-detection module.", bullet))

    story.append(Spacer(1, 16))
    story.append(Paragraph("15. References", section_heading))
    refs = [
        ("OpenCV Documentation — Cascade Classifier", "https://docs.opencv.org/4.x/db/d28/tutorial_cascade_classifier.html"),
        ("OpenCV Documentation — Background Subtraction (MOG2)", "https://docs.opencv.org/4.x/d1/dc5/tutorial_background_subtraction.html"),
        ("OpenCV Documentation — Contours", "https://docs.opencv.org/4.x/d4/d73/tutorial_py_contours_begin.html"),
        ("OpenCV samples repository (sample test images used for demos)", "https://github.com/opencv/opencv/tree/master/samples/data"),
        ("Python sqlite3 standard library documentation", "https://docs.python.org/3/library/sqlite3.html"),
        ("pytest documentation", "https://docs.pytest.org/"),
        ("Matplotlib documentation", "https://matplotlib.org/stable/"),
    ]
    for title, url in refs:
        story.append(Paragraph(f"• <b>{title}:</b><br/>&nbsp;&nbsp;<font color='#2B6CB0'>{url}</font>", bullet))
        story.append(Spacer(1, 4))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully compiled PDF report to {OUTPUT_PDF}")

if __name__ == "__main__":
    build_pdf()
