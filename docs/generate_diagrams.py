import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

diagrams_dir = Path(r"C:\Users\Asus\.gemini\antigravity\scratch\visionguard\docs\diagrams")
diagrams_dir.mkdir(parents=True, exist_ok=True)

plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["font.family"] = "sans-serif"

# 1. System Architecture Diagram
def draw_architecture():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Presentation Layer
    p_box = patches.FancyBboxPatch((35, 82), 32, 14, boxstyle="round,pad=0.5", ec="#3182ce", fc="#ebf8ff", lw=1.5)
    ax.add_patch(p_box)
    ax.text(51, 92, "Presentation Layer", ha="center", va="center", fontsize=11, fontweight="bold", color="#2b6cb0")
    ax.text(51, 86, "CLI (main.py / cli.py)\nargparse sub-commands", ha="center", va="center", fontsize=9, color="#2d3748")

    # Core Processing Modules Group
    core_bg = patches.FancyBboxPatch((24, 46), 72, 26, boxstyle="round,pad=0.8", ec="#e53e3e", fc="#fff5f5", lw=1.2, ls="--")
    ax.add_patch(core_bg)
    ax.text(60, 69, "Core Processing Modules", ha="center", va="center", fontsize=11, fontweight="bold", color="#c53030")

    # 4 Modules
    mods = [
        ("Object Counter\n(object_counter.py)", 33),
        ("Face Detection\n(face_detection.py)", 51),
        ("Motion Detection\n(motion_detection.py)", 69),
        ("Image Enhancement\n(image_utils.py)", 87),
    ]
    for title, cx in mods:
        m_box = patches.FancyBboxPatch((cx - 7.5, 49), 15, 16, boxstyle="round,pad=0.4", ec="#e53e3e", fc="#ffffff", lw=1.2)
        ax.add_patch(m_box)
        ax.text(cx, 57, title, ha="center", va="center", fontsize=8, fontweight="bold", color="#742a2a")

    # Support Services
    sup_bg = patches.FancyBboxPatch((50, 20), 45, 18, boxstyle="round,pad=0.6", ec="#805ad5", fc="#faf5ff", lw=1.2, ls=":")
    ax.add_patch(sup_bg)
    ax.text(72.5, 34.5, "Support Services", ha="center", va="center", fontsize=10, fontweight="bold", color="#6b46c1")

    log_box = patches.FancyBboxPatch((52, 23), 18, 8, boxstyle="round,pad=0.3", ec="#805ad5", fc="#ffffff", lw=1)
    ax.add_patch(log_box)
    ax.text(61, 27, "Logging\n(logger_setup.py)", ha="center", va="center", fontsize=8, color="#44337a")

    cfg_box = patches.FancyBboxPatch((74, 23), 19, 8, boxstyle="round,pad=0.3", ec="#805ad5", fc="#ffffff", lw=1)
    ax.add_patch(cfg_box)
    ax.text(83.5, 27, "Configuration\n(config.py)", ha="center", va="center", fontsize=8, color="#44337a")

    # Data & Reporting Layer
    data_bg = patches.FancyBboxPatch((4, 28), 24, 44, boxstyle="round,pad=0.6", ec="#d69e2e", fc="#fffff0", lw=1.2)
    ax.add_patch(data_bg)
    ax.text(16, 68, "Data & Reporting Layer", ha="center", va="center", fontsize=10, fontweight="bold", color="#b7791f")

    rep_box = patches.FancyBboxPatch((6, 51), 20, 13, boxstyle="round,pad=0.4", ec="#d69e2e", fc="#ffffff", lw=1)
    ax.add_patch(rep_box)
    ax.text(16, 57.5, "Report Generator\n(report_generator.py)\nCSV / JSON / Charts", ha="center", va="center", fontsize=7.5, color="#744210")

    db_box = patches.FancyBboxPatch((6, 31), 20, 14, boxstyle="round,pad=0.4", ec="#d69e2e", fc="#ffffff", lw=1)
    ax.add_patch(db_box)
    ax.text(16, 38, "SQLite Database\n(database.py)", ha="center", va="center", fontsize=8.5, fontweight="bold", color="#744210")

    # External dependencies box
    ext_box = patches.FancyBboxPatch((55, 3), 36, 11, boxstyle="round,pad=0.3", ec="#718096", fc="#edf2f7", lw=1)
    ax.add_patch(ext_box)
    ax.text(73, 8.5, "OpenCV / NumPy / Matplotlib\n(External Libraries)", ha="center", va="center", fontsize=8, color="#4a5568")

    # Arrows
    # CLI to Modules
    ax.annotate("", xy=(51, 72), xytext=(51, 82), arrowprops=dict(arrowstyle="->", lw=1.5, color="#3182ce"))
    # Modules to DB
    ax.annotate("", xy=(26, 38), xytext=(33, 49), arrowprops=dict(arrowstyle="->", lw=1.2, color="#4a5568", ls="-"))
    ax.text(28, 45, "log detections", fontsize=8, color="#4a5568", rotation=25)
    # Report generator reads DB
    ax.annotate("", xy=(16, 51), xytext=(16, 45), arrowprops=dict(arrowstyle="<->", lw=1.2, color="#b7791f"))
    ax.text(19, 48, "read/query", fontsize=7.5, color="#744210")
    # Modules to Support Services
    ax.annotate("", xy=(72, 38), xytext=(72, 46), arrowprops=dict(arrowstyle="->", lw=1.2, color="#805ad5", ls=":"))
    # Support Services to External
    ax.annotate("", xy=(73, 14), xytext=(73, 20), arrowprops=dict(arrowstyle="->", lw=1.2, color="#718096"))

    plt.tight_layout()
    out = diagrams_dir / "architecture.png"
    plt.savefig(str(out), bbox_inches="tight")
    plt.close()
    print("Saved architecture.png")

# 2. Use Case Diagram
def draw_usecase():
    fig, ax = plt.subplots(figsize=(9, 6.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Actor: Student / Evaluator
    # Draw stick figure head
    head = patches.Circle((18, 56), 3.5, ec="#2b6cb0", fc="#ebf8ff", lw=2)
    ax.add_patch(head)
    # Body
    ax.plot([18, 18], [52.5, 38], color="#2b6cb0", lw=2.5)
    # Arms
    ax.plot([10, 26], [47, 47], color="#2b6cb0", lw=2.5)
    # Legs
    ax.plot([18, 11], [38, 25], color="#2b6cb0", lw=2.5)
    ax.plot([18, 25], [38, 25], color="#2b6cb0", lw=2.5)
    ax.text(18, 18, "Student /\nEvaluator", ha="center", va="center", fontsize=11, fontweight="bold", color="#1a365d")

    # System boundary box
    sys_box = patches.FancyBboxPatch((36, 6), 60, 88, boxstyle="round,pad=0.8", ec="#4a5568", fc="#f7fafc", lw=1.5)
    ax.add_patch(sys_box)
    ax.text(66, 90, "VisionGuard System Boundary", ha="center", va="center", fontsize=11, fontweight="bold", color="#2d3748")

    use_cases = [
        ("Detect Faces\nin an Image", 79),
        ("Detect Motion\nin a Video", 66),
        ("Count Objects\nin an Image", 53),
        ("Apply Enhancement\nFilter", 40),
        ("Generate Report\n(CSV / JSON / Chart)", 27),
        ("View Past\nSessions", 14),
    ]

    for text, cy in use_cases:
        ellipse = patches.Ellipse((66, cy), 32, 9.5, ec="#3182ce", fc="#ffffff", lw=1.5)
        ax.add_patch(ellipse)
        ax.text(66, cy, text, ha="center", va="center", fontsize=8.5, color="#1a202c", fontweight="bold")
        # Connection line
        ax.plot([25, 50], [47, cy], color="#4a5568", lw=1.2, ls="-")

    plt.tight_layout()
    out = diagrams_dir / "use_case.png"
    plt.savefig(str(out), bbox_inches="tight")
    plt.close()
    print("Saved use_case.png")

# 3. Process Workflow Diagram
def draw_workflow():
    fig, ax = plt.subplots(figsize=(12, 3.8), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 35)
    ax.axis("off")

    steps = [
        ("User runs\nCLI command", 6),
        ("Validate input\n(path / ext)", 17),
        ("Create DB session\n(status: running)", 29),
        ("Load & preprocess\nimage / frame", 41),
        ("Run detector\n(face/motion/object)", 53),
        ("Persist detections\nto SQLite", 65),
        ("Draw annotations\non output", 77),
        ("Save output &\nfinalise session", 89),
    ]

    for text, cx in steps:
        box = patches.FancyBboxPatch((cx - 4.8, 17), 9.6, 12, boxstyle="round,pad=0.3", ec="#3182ce", fc="#ebf8ff", lw=1.2)
        ax.add_patch(box)
        ax.text(cx, 23, text, ha="center", va="center", fontsize=7.2, color="#1a365d", fontweight="bold")

    # Connect forward arrows
    for i in range(len(steps) - 1):
        x1 = steps[i][1] + 4.8
        x2 = steps[i+1][1] - 4.8
        ax.annotate("", xy=(x2, 23), xytext=(x1, 23), arrowprops=dict(arrowstyle="->", lw=1.5, color="#2b6cb0"))

    # Fail branch
    ax.annotate("", xy=(89, 17), xytext=(17, 17),
                arrowprops=dict(arrowstyle="->", lw=1.2, color="#e53e3e", ls="--",
                                connectionstyle="arc3,rad=-0.22"))
    ax.text(53, 6, "invalid input / processing error -> mark session 'failed' & log error",
            ha="center", va="center", fontsize=8, color="#c53030", fontweight="bold")

    plt.tight_layout()
    out = diagrams_dir / "workflow.png"
    plt.savefig(str(out), bbox_inches="tight")
    plt.close()
    print("Saved workflow.png")

# 4. Class / Component Diagram
def draw_class_diagram():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    def draw_uml_box(x, y, w, h, title, attrs, methods, color="#2b6cb0", bg="#f7fafc"):
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0", ec=color, fc=bg, lw=1.5)
        ax.add_patch(box)
        # Header
        ax.plot([x, x + w], [y + h - 5.5, y + h - 5.5], color=color, lw=1)
        ax.text(x + w / 2, y + h - 2.8, title, ha="center", va="center", fontsize=8.5, fontweight="bold", color=color)
        # Attrs / Methods separator
        sep_y = y + h - 5.5 - (len(attrs) * 3.2 + 1)
        if attrs and methods:
            ax.plot([x, x + w], [sep_y, sep_y], color=color, lw=0.8, ls=":")
        # Text
        cur_y = y + h - 7.5
        for a in attrs:
            ax.text(x + 1.5, cur_y, a, ha="left", va="center", fontsize=7, color="#2d3748")
            cur_y -= 3.0
        cur_y = sep_y - 2.5
        for m in methods:
            ax.text(x + 1.5, cur_y, m, ha="left", va="center", fontsize=7, color="#2d3748")
            cur_y -= 3.0

    # CLI
    draw_uml_box(38, 76, 24, 18, "CLI (cli.py)", [],
                 ["+ build_parser(): ArgumentParser", "+ main(args): int"],
                 color="#2b6cb0", bg="#ebf8ff")

    # Detectors
    draw_uml_box(4, 45, 27, 23, "FaceDetector",
                 ["- cascade: CascadeClassifier", "- scale_factor: float"],
                 ["+ detect(image): List[dict]", "+ annotate(image, dets): ndarray", "+ process_image(...): dict"],
                 color="#c53030", bg="#fff5f5")

    draw_uml_box(36, 45, 28, 23, "MotionDetector",
                 ["- subtractor: MOG2", "- min_area: int"],
                 ["+ process_frame(frame): tuple", "+ process_video(...): dict"],
                 color="#c53030", bg="#fff5f5")

    draw_uml_box(68, 45, 28, 23, "ObjectCounter",
                 ["- min_area: int", "- max_area: int"],
                 ["+ count(image): tuple", "+ annotate(image, objs): ndarray", "+ process_image(...): dict"],
                 color="#c53030", bg="#fff5f5")

    # Database
    draw_uml_box(4, 8, 30, 27, "Database (database.py)",
                 ["- schema: SCHEMA_SQL", "- db_path: Path"],
                 ["+ init_db(db_path)", "+ start_session(...): int", "+ log_detections_batch(...)",
                  "+ finish_session(...)", "+ get_session(id): dict", "+ list_sessions(...): list"],
                 color="#b7791f", bg="#fffff0")

    # ImageUtils
    draw_uml_box(40, 8, 28, 27, "ImageUtils (image_utils.py)",
                 ["- FILTER_MAP: dict"],
                 ["+ load_image(path): ndarray", "+ save_image(img, path)",
                  "+ apply_filter(img, name)", "+ draw_bounding_box(...)"],
                 color="#319795", bg="#e6fffa")

    # ReportGenerator
    draw_uml_box(72, 8, 25, 27, "ReportGenerator",
                 [],
                 ["+ export_session_json(...)", "+ export_session_csv(...)",
                  "+ generate_analytics_chart(...)", "+ generate_full_report(...)"],
                 color="#805ad5", bg="#faf5ff")

    # Association lines
    ax.annotate("", xy=(17, 68), xytext=(45, 76), arrowprops=dict(arrowstyle="->", lw=1.2, color="#4a5568"))
    ax.annotate("", xy=(50, 68), xytext=(50, 76), arrowprops=dict(arrowstyle="->", lw=1.2, color="#4a5568"))
    ax.annotate("", xy=(82, 68), xytext=(55, 76), arrowprops=dict(arrowstyle="->", lw=1.2, color="#4a5568"))

    ax.annotate("", xy=(17, 35), xytext=(17, 45), arrowprops=dict(arrowstyle="->", lw=1.2, color="#4a5568"))
    ax.annotate("", xy=(22, 35), xytext=(45, 45), arrowprops=dict(arrowstyle="->", lw=1.2, color="#4a5568"))
    ax.annotate("", xy=(26, 35), xytext=(75, 45), arrowprops=dict(arrowstyle="->", lw=1.2, color="#4a5568"))

    plt.tight_layout()
    out = diagrams_dir / "class_diagram.png"
    plt.savefig(str(out), bbox_inches="tight")
    plt.close()
    print("Saved class_diagram.png")

# 5. Sequence Diagram
def draw_sequence():
    fig, ax = plt.subplots(figsize=(10, 6.2), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    lifelines = [
        ("User", 10),
        ("CLI", 26),
        ("Detector", 44),
        ("ImageUtils", 62),
        ("Database", 78),
        ("FileSystem", 92)
    ]

    for name, x in lifelines:
        box = patches.FancyBboxPatch((x - 6, 88), 12, 7, boxstyle="round,pad=0.3", ec="#2b6cb0", fc="#ebf8ff", lw=1.2)
        ax.add_patch(box)
        ax.text(x, 91.5, name, ha="center", va="center", fontsize=8.5, fontweight="bold", color="#1a365d")
        ax.plot([x, x], [88, 8], color="#a0aec0", lw=1, ls="--")

    calls = [
        (10, 26, 82, "1: run command(args)", "#2b6cb0"),
        (26, 62, 74, "2: load_image(path)", "#2d3748"),
        (62, 92, 67, "3: read binary", "#4a5568"),
        (26, 78, 60, "4: start_session()", "#b7791f"),
        (26, 44, 52, "5: detect(image)", "#c53030"),
        (44, 78, 44, "6: log_detections()", "#b7791f"),
        (44, 62, 36, "7: annotate(image)", "#319795"),
        (62, 92, 28, "8: save_image(out)", "#4a5568"),
        (26, 78, 20, "9: finish_session()", "#b7791f"),
        (26, 10, 12, "10: print summary to console", "#2b6cb0"),
    ]

    for x1, x2, y, msg, color in calls:
        ax.annotate("", xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle="->", lw=1.3, color=color))
        mid_x = (x1 + x2) / 2
        ax.text(mid_x, y + 2.2, msg, ha="center", va="bottom", fontsize=7.5, color=color, fontweight="bold")

    plt.tight_layout()
    out = diagrams_dir / "sequence_diagram.png"
    plt.savefig(str(out), bbox_inches="tight")
    plt.close()
    print("Saved sequence_diagram.png")

# 6. ER Diagram / Schema Design
def draw_er_diagram():
    fig, ax = plt.subplots(figsize=(9.5, 4.8), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 70)
    ax.axis("off")

    def draw_table(x, y, w, title, cols):
        h = 8 + len(cols) * 5.2
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0", ec="#2b6cb0", fc="#ffffff", lw=1.5)
        ax.add_patch(box)
        # Header
        hdr = patches.Rectangle((x, y + h - 8), w, 8, ec="#2b6cb0", fc="#ebf8ff", lw=1.5)
        ax.add_patch(hdr)
        ax.text(x + w / 2, y + h - 4, title, ha="center", va="center", fontsize=9.5, fontweight="bold", color="#1a365d")
        # Rows
        cur_y = y + h - 12
        for col, col_type, is_key in cols:
            prefix = "PK " if is_key == "PK" else ("FK " if is_key == "FK" else "    ")
            key_color = "#c53030" if is_key == "PK" else ("#b7791f" if is_key == "FK" else "#4a5568")
            ax.text(x + 2, cur_y, f"{prefix}{col}", ha="left", va="center", fontsize=8, fontweight="bold" if is_key else "normal", color=key_color)
            ax.text(x + w - 2, cur_y, col_type, ha="right", va="center", fontsize=7.5, color="#718096")
            cur_y -= 5.2

    sessions_cols = [
        ("session_id", "INTEGER", "PK"),
        ("module", "TEXT", ""),
        ("source_path", "TEXT", ""),
        ("started_at", "TEXT", ""),
        ("finished_at", "TEXT", ""),
        ("status", "TEXT", ""),
        ("summary_json", "TEXT", ""),
    ]

    detections_cols = [
        ("detection_id", "INTEGER", "PK"),
        ("session_id", "INTEGER", "FK"),
        ("frame_index", "INTEGER", ""),
        ("label", "TEXT", ""),
        ("x, y, width, height", "INTEGER", ""),
        ("confidence", "REAL", ""),
        ("created_at", "TEXT", ""),
    ]

    draw_table(8, 12, 36, "sessions", sessions_cols)
    draw_table(56, 12, 36, "detections", detections_cols)

    # 1..N Arrow between sessions and detections
    ax.annotate("", xy=(56, 44), xytext=(44, 44),
                arrowprops=dict(arrowstyle="->", lw=2, color="#3182ce"))
    ax.text(50, 47, "1 .. N", ha="center", va="bottom", fontsize=10, fontweight="bold", color="#2b6cb0")
    ax.text(50, 40, "FOREIGN KEY\n(session_id)", ha="center", va="top", fontsize=7, color="#718096")

    plt.tight_layout()
    out = diagrams_dir / "er_diagram.png"
    plt.savefig(str(out), bbox_inches="tight")
    plt.close()
    print("Saved er_diagram.png")

if __name__ == "__main__":
    draw_architecture()
    draw_usecase()
    draw_workflow()
    draw_class_diagram()
    draw_sequence()
    draw_er_diagram()
    print("All 6 diagrams generated successfully.")
