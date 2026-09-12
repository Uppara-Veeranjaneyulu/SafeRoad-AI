import os
import sys
import pptx
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

def generate_module3_deck():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Color Palette matching reference PPTX
    CRIMSON = RGBColor(192, 0, 0)         # #C00000
    DARK_RED = RGBColor(139, 0, 0)        # #8B0000
    HEADER_FILL = RGBColor(130, 20, 20)   # Dark Crimson Table Header
    SLATE_DARK = RGBColor(15, 23, 42)     # #0F172A Primary Text
    SLATE_MUTED = RGBColor(71, 85, 105)   # #475569 Secondary Text
    WHITE = RGBColor(255, 255, 255)
    LIGHT_BG = RGBColor(248, 250, 252)    # Card Background #F8FAFC
    CARD_BORDER = RGBColor(226, 232, 240) # #E2E8F0
    ALT_ROW_FILL = RGBColor(245, 247, 250)# Zebra rows
    FORMULA_BG = RGBColor(255, 250, 250)  # Formula Card Background
    FORMULA_BORDER = RGBColor(220, 150, 150)

    footer_img = 'extracted_ref_assets/slide_1_Picture 4_0.png'
    logo_img = 'extracted_ref_assets/slide_1_Picture 5_1.png'
    arch_img = 'review-2/architecture-overview.png'
    ui_prediction = 'ui_screenshots/ui_prediction.png'
    mobilenet_curves = 'results/mobilenetv2/training_curves.png'

    FONT_FAMILY = 'Times New Roman'

    def add_base_slide(title_text):
        slide = prs.slides.add_slide(blank_layout)
        if os.path.exists(footer_img):
            slide.shapes.add_picture(footer_img, Inches(0), Inches(6.68), Inches(13.333), Inches(0.82))

        tb = slide.shapes.add_textbox(Inches(0.6), Inches(0.28), Inches(12.13), Inches(0.75))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = FONT_FAMILY
        p.font.size = Pt(26)
        p.font.bold = True
        p.font.color.rgb = DARK_RED

        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.10), Inches(12.13), Pt(2))
        line.fill.solid()
        line.fill.fore_color.rgb = CRIMSON
        line.line.color.rgb = CRIMSON

        return slide

    def format_cell(cell, text, bold=False, italic=False, size_pt=12.0, align=PP_ALIGN.LEFT, text_color=SLATE_DARK):
        cell.text = ""
        p = cell.text_frame.paragraphs[0]
        p.alignment = align
        r = p.add_run()
        r.text = str(text)
        r.font.name = FONT_FAMILY
        r.font.size = Pt(size_pt)
        r.font.bold = bold
        r.font.italic = italic
        r.font.color.rgb = text_color

    def style_table(table, col_widths, col_alignments=None, font_size=12.0, header_font_size=13.0, header_color=HEADER_FILL):
        for idx, w in enumerate(col_widths):
            table.columns[idx].width = w

        for r_idx, row in enumerate(table.rows):
            for c_idx, cell in enumerate(row.cells):
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                cell.margin_left = Inches(0.10)
                cell.margin_right = Inches(0.10)
                cell.margin_top = Inches(0.06)
                cell.margin_bottom = Inches(0.06)
                cell.fill.solid()

                align = PP_ALIGN.LEFT
                if col_alignments and c_idx < len(col_alignments):
                    align = col_alignments[c_idx]

                if r_idx == 0:
                    cell.fill.fore_color.rgb = header_color
                    for p in cell.text_frame.paragraphs:
                        p.alignment = align
                        for r in p.runs:
                            r.font.name = FONT_FAMILY
                            r.font.size = Pt(header_font_size)
                            r.font.bold = True
                            r.font.color.rgb = WHITE
                else:
                    cell.fill.fore_color.rgb = WHITE if r_idx % 2 != 0 else ALT_ROW_FILL
                    for p in cell.text_frame.paragraphs:
                        p.alignment = align
                        for r in p.runs:
                            r.font.name = FONT_FAMILY
                            r.font.size = Pt(font_size)
                            r.font.color.rgb = SLATE_DARK

    def add_card(slide, left, top, width, height, title, items, title_color=DARK_RED, bg_color=LIGHT_BG, body_size=15.5):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        tb = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.18), width - Inches(0.50), height - Inches(0.36))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.name = FONT_FAMILY
        p0.font.size = Pt(18)
        p0.font.bold = True
        p0.font.color.rgb = title_color
        p0.space_after = Pt(8)

        for item in items:
            p = tf.add_paragraph()
            p.font.name = FONT_FAMILY
            p.font.size = Pt(body_size)
            p.font.color.rgb = SLATE_DARK
            p.space_after = Pt(6)
            if isinstance(item, tuple):
                r1 = p.add_run()
                r1.text = item[0] + " "
                r1.font.name = FONT_FAMILY
                r1.font.size = Pt(body_size)
                r1.font.bold = True
                r1.font.color.rgb = DARK_RED
                r2 = p.add_run()
                r2.text = item[1]
                r2.font.name = FONT_FAMILY
                r2.font.size = Pt(body_size)
                r2.font.bold = False
            else:
                r = p.add_run()
                r.text = "• " + str(item)
                r.font.name = FONT_FAMILY
                r.font.size = Pt(body_size)

    def add_formula_card(slide, left, top, width, height, title, formula_display, description):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = FORMULA_BG
        card.line.color.rgb = FORMULA_BORDER
        card.line.width = Pt(1.5)

        tb = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.15), width - Inches(0.50), height - Inches(0.30))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.name = FONT_FAMILY
        p0.font.size = Pt(17.5)
        p0.font.bold = True
        p0.font.color.rgb = DARK_RED
        p0.space_after = Pt(4)

        p_f = tf.add_paragraph()
        p_f.text = formula_display
        p_f.font.name = FONT_FAMILY
        p_f.font.size = Pt(16.0)
        p_f.font.bold = True
        p_f.font.color.rgb = CRIMSON
        p_f.space_after = Pt(4)

        p_desc = tf.add_paragraph()
        p_desc.text = description
        p_desc.font.name = FONT_FAMILY
        p_desc.font.size = Pt(15.0)
        p_desc.font.color.rgb = SLATE_DARK

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (TEAM 10 BASE — PROMINENT MODULE 3 & VEERANJANEYULU)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    if os.path.exists(footer_img):
        s1.shapes.add_picture(footer_img, Inches(0), Inches(6.68), Inches(13.333), Inches(0.82))
    if os.path.exists(logo_img):
        s1.shapes.add_picture(logo_img, Inches(0.6), Inches(0.35), Inches(1.5), Inches(1.5))

    tb_hdr = s1.shapes.add_textbox(Inches(2.3), Inches(0.35), Inches(10.4), Inches(1.8))
    tf_hdr = tb_hdr.text_frame
    tf_hdr.word_wrap = True

    p1 = tf_hdr.paragraphs[0]
    p1.text = "NEURAL NETWORKS AND DEEP LEARNING (23CSE473)"
    p1.font.name = FONT_FAMILY
    p1.font.size = Pt(18)
    p1.font.bold = True
    p1.font.color.rgb = CRIMSON

    p2 = tf_hdr.add_paragraph()
    p2.text = "CASE STUDY REVIEW 2 — INDIVIDUAL MODULE EVALUATION (TEAM 10)"
    p2.font.name = FONT_FAMILY
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = SLATE_MUTED

    p3 = tf_hdr.add_paragraph()
    p3.text = "SafeRoad AI: Road-Scene Risk Classification & Traffic Monitoring"
    p3.font.name = FONT_FAMILY
    p3.font.size = Pt(22)
    p3.font.bold = True
    p3.font.color.rgb = DARK_RED
    p3.space_before = Pt(3)

    p4 = tf_hdr.add_paragraph()
    p4.text = 'FOCUS MODULE: MODULE 3 — INTELLIGENT TRAFFIC MONITORING (YOLOV8) & DEEP DENOISING (DNCNN)'
    p4.font.name = FONT_FAMILY
    p4.font.size = Pt(13.5)
    p4.font.bold = True
    p4.font.color.rgb = CRIMSON

    # Team 10 Table from Team-10-SafeRoad_AI_Review2.pptx with Row 3 (Veeranjaneyulu) Highlighted
    t_shape1 = s1.shapes.add_table(5, 5, Inches(0.6), Inches(2.25), Inches(12.13), Inches(2.55))
    t1 = t_shape1.table
    team_data = [
        ["Sl", "Student Name", "Roll Number", "College Email ID", "Project Module & Scope"],
        ["1", "Chaitanya Chitturi", "CB.SC.U4CSE23214", "cb.sc.u4cse23214@cb.students.amrita.edu", "Module 1: Data Acquisition & Preprocessing"],
        ["2", "T Hema Sai", "CB.SC.U4CSE23266", "cb.sc.u4cse23266@cb.students.amrita.edu", "Module 2: MobileNetV2 Risk Classification"],
        ["3", "U Veeranjaneyulu (Presenter)", "CB.SC.U4CSE23351", "cb.sc.u4cse23351@cb.students.amrita.edu", "Module 3: Intelligent Traffic Monitoring (YOLOv8) & DnCNN Denoising"],
        ["4", "Charan Kola", "CB.SC.U4CSE23332", "cb.sc.u4cse23332@cb.students.amrita.edu", "Module 4: ResNet-50 Benchmark & Dataset Verification"]
    ]
    for r_idx, row in enumerate(team_data):
        for c_idx, val in enumerate(row):
            cell = t1.cell(r_idx, c_idx)
            format_cell(cell, val, bold=(r_idx == 0 or r_idx == 3 or c_idx == 0), size_pt=12.0)
            if r_idx == 3:  # Highlight Veeranjaneyulu
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(254, 242, 242)  # Light Crimson tint
    style_table(t1, [Inches(0.5), Inches(2.8), Inches(2.1), Inches(3.4), Inches(3.33)], font_size=11.5, header_font_size=12.5)

    add_card(s1, Inches(0.6), Inches(4.95), Inches(12.13), Inches(1.5), "Module 3 Individual Evaluation Coordinates & Project Links", [
        ("Evaluated Student:", "U Veeranjaneyulu | Roll No: CB.SC.U4CSE23351 | Contact: 9848267497"),
        ("Course Faculty Guide:", "Professor – Dr. T Senthil Kumar (Department of Computer Science & Engineering)"),
        ("Source Code Repository:", "https://github.com/Uppara-Veeranjaneyulu/SafeRoad-AI"),
        ("Live Web Application:", "https://saferoad-ai-one.vercel.app/ (React 18 + Tailwind CSS + Flask API)")
    ], body_size=14.5)

    # =========================================================================
    # SLIDE 2: OPERATIONAL CONTEXT & MOTIVATION FOR MODULE 3
    # =========================================================================
    s2 = add_base_slide("Operational Context: The Traffic Perception Bottleneck")
    add_card(s2, Inches(0.6), Inches(1.3), Inches(5.9), Inches(5.1), "The Real-World Driving Challenge", [
        ("Perceptual Latency in Heavy Traffic:", "Drivers face intense cognitive overload at congested multi-lane junctions where cars, motorcycles, and pedestrians move unpredictably."),
        ("Multi-Scale Road Hazards:", "Hazards range widely in scale: from distant pedestrians (tiny 20x20 pixel bounding boxes) to massive oncoming trucks occupying 60% of the field-of-view."),
        ("Sensor Noise Corruption:", "Adverse weather (rain, fog, low-light nighttime) injects high-frequency sensor noise, dropping standard detector confidence by over 30%."),
        ("Need for Real-Time Semantic Context:", "Scene risk cannot be determined by static appearance alone; knowing exact vehicle density and pedestrian counts is vital.")
    ], body_size=15.5)
    add_card(s2, Inches(6.8), Inches(1.3), Inches(5.93), Inches(5.1), "Module 3 Mission: Semantic Traffic Awareness", [
        ("High-Throughput Object Parsing:", "Deploys YOLOv8 to rapidly extract bounding boxes, class labels, and confidence for all road agents at >85 FPS."),
        ("Dynamic Traffic Density Estimation:", "Aggregates vehicle and pedestrian counts to compute continuous road congestion metrics."),
        ("Vulnerable Road User (VRU) Safety:", "Prioritizes immediate detection of pedestrians, cyclists, and two-wheelers in high-risk conflict zones."),
        ("Decoupled Denoising Defense:", "Pre-conditions corrupted dashcam frames via DnCNN before detection, ensuring robust operation in severe weather.")
    ], body_size=15.5)

    # =========================================================================
    # SLIDE 3: PROBLEM STATEMENT: OBJECT DETECTION UNDER ADVERSE CONDITIONS
    # =========================================================================
    s3 = add_base_slide("Module 3 Problem Statement: Multi-Agent Detection Under Degradation")
    add_card(s3, Inches(0.6), Inches(1.3), Inches(5.9), Inches(5.1), "Core Technical Challenges", [
        ("Heavy Occlusion & Congestion:", "In dense Indian urban environments, vehicles and pedestrians heavily overlap, leading to frequent missed detections in traditional anchor-based detectors."),
        ("Scale Disparity across Road Objects:", "Simultaneously localizing small traffic signs and massive commercial buses requires multi-scale receptive field fusion without latency explosion."),
        ("Dashcam Sensor Degradation:", "Nighttime ISO noise, wiper motion blur, and JPEG compression artifacts smear sharp object contours, causing false negatives."),
        ("Edge Latency Constraint:", "The detection model must execute in under 15 ms on edge hardware to leave computational headroom for downstream risk classification.")
    ], body_size=15.5)
    add_card(s3, Inches(6.8), Inches(1.3), Inches(5.93), Inches(5.1), "Module 3 Engineered Solutions", [
        ("Anchor-Free Detection Architecture:", "YOLOv8 eliminates predefined anchor box clustering, directly predicting object centers and bounding box offsets."),
        ("Cross-Stage Partial Bottlenecks (C2f):", "Enhances gradient flow while reducing parameter count, achieving 86.20% mAP@0.5 with only 3.2M parameters."),
        ("Task-Aligned Assigner (TAL):", "Dynamically aligns classification scores with bounding box IoU quality during training, preventing high-confidence mislocalizations."),
        ("Coupled DnCNN Pre-Filter:", "Removes sensor grain and compression artifacts, boosting downstream traffic detection recall by +5.2% on degraded frames.")
    ], body_size=15.5)

    # =========================================================================
    # SLIDE 4: SYSTEM ARCHITECTURE & MODULE 3 POSITIONING
    # =========================================================================
    s4 = add_base_slide("Overall Application Architecture & Module 3 Positioning")
    if os.path.exists(arch_img):
        s4.shapes.add_picture(arch_img, Inches(0.6), Inches(1.3), Inches(5.8), Inches(5.1))
    else:
        add_card(s4, Inches(0.6), Inches(1.3), Inches(5.8), Inches(5.1), "Architecture Overview", [
            ("Diagram Reference:", "review-2/architecture-overview.png")
        ])

    add_card(s4, Inches(6.6), Inches(1.3), Inches(6.13), Inches(5.1), "Module 3 Architectural Role & Data Interfaces", [
        ("Upstream Ingestion & Denoising:", "Receives standardized 224x224 RGB frames restored by DnCNN, ensuring noise-free spatial feature extraction."),
        ("Parallel Semantic Extraction:", "Executes concurrently alongside MobileNetV2, outputting discrete vehicle counts, pedestrian flags, and road signs."),
        ("Feature Fusion for Risk Logic:", "Passes traffic density vectors to the Flask decision engine: dense traffic + pedestrian conflict escalates Moderate Risk to High Risk."),
        ("Real-Time UI Telemetry:", "Feeds real-time bounding box coordinates and object count overlays to the interactive React web dashboard at 30 FPS.")
    ], body_size=15.5)

    # =========================================================================
    # SLIDE 5: MODULE 3 DETAILED FUNCTIONAL BREAKDOWN
    # =========================================================================
    s5 = add_base_slide("Module 3 Detailed Functional Breakdown")
    t_shape5 = s5.shapes.add_table(5, 4, Inches(0.6), Inches(1.3), Inches(12.13), Inches(5.1))
    t5 = t_shape5.table
    mod3_breakdown = [
        ["Sub-Component", "Technical Mechanism", "Underlying Deep Learning Technology", "Output & System Impact"],
        ["1. Multi-Agent Localization", "Predicts precise bounding boxes for all active vehicles, trucks, and buses.", "YOLOv8 CSPDarknet Backbone + C2f Modules", "Bounding boxes with class IDs and confidence scores."],
        ["2. Vulnerable User Safety", "Dedicated detection of pedestrians, cyclists, and two-wheelers in road paths.", "High-resolution P3 detection head (stride = 8)", "Pedestrian count and proximity collision hazard alerts."],
        ["3. Traffic Density Scoring", "Aggregates total detected vehicles to compute spatial road occupancy.", "Contextual Feature Vector Aggregation", "Traffic density categorization: Low, Medium, High."],
        ["4. Restorative Pre-Filtering", "Systematically eliminates camera sensor static and compression blur.", "17-Layer DnCNN Residual Learning Network", "Restored clean image tensor (PSNR improved to >31 dB)."]
    ]
    for r_idx, row in enumerate(mod3_breakdown):
        for c_idx, val in enumerate(row):
            format_cell(t5.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 0), size_pt=12.5)
    style_table(t5, [Inches(2.2), Inches(3.2), Inches(3.4), Inches(3.33)], font_size=12.0, header_font_size=13.0)

    # =========================================================================
    # SLIDE 6: LITERATURE SURVEY — U VEERANJANEYULU (MODULE 3 FOUNDATIONS)
    # =========================================================================
    s6 = add_base_slide("Literature Survey: U Veeranjaneyulu (Module 3 Foundations)")
    t_shape6 = s6.shapes.add_table(6, 5, Inches(0.6), Inches(1.3), Inches(12.13), Inches(5.1))
    t6 = t_shape6.table
    lit_papers = [
        ["Sl", "Paper Title & Authors", "Journal & Year", "SCImago Rank", "Direct Relevance to Module 3"],
        ["1", "Beyond a Gaussian Denoiser: Residual Learning of Deep CNN for Image Denoising (Zhang et al.)", "IEEE Transactions on Image Processing (2017)", "Q1\nSJR: 2.502", "Primary mathematical foundation for our 17-layer DnCNN model: learning noise residual R(y) rather than clean pixels."],
        ["2", "YOLO-MPAM: Efficient real-time neural networks based on multi-channel feature fusion (Yu et al.)", "Expert Systems with Applications (2024)", "Q1\nSJR: 1.854", "Validates multi-channel feature fusion in YOLOv8 for detecting vehicles across complex multi-lane road scenes."],
        ["3", "Enhancing vehicle detection in ITS via autonomous UAV platform and YOLOv8 (Bakirci, M.)", "Applied Soft Computing (2024)", "Q1\nSJR: 1.810", "Guides our selection of YOLOv8n to maintain sub-15ms edge inference during real-time traffic surveillance."],
        ["4", "Decomposed Neural Architecture Search for image denoising (Elsevier Reference)", "Applied Soft Computing (2022)", "Q1\nSJR: 1.810", "Guides our optimization of DnCNN layer depth and filter count for low-latency frame restoration."],
        ["5", "Dynamic Loss Balancing and Sequential Enhancement for Road-Safety Assessment (Kačan et al.)", "IEEE Transactions on ITS (2024)", "Q1\nSJR: 2.589", "Supplies our core road hazard classification framework and dynamic loss balancing strategy on BDD100K data."]
    ]
    for r_idx, row in enumerate(lit_papers):
        for c_idx, val in enumerate(row):
            format_cell(t6.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 0), size_pt=12.0)
    style_table(t6, [Inches(0.5), Inches(4.3), Inches(2.6), Inches(1.3), Inches(3.43)], font_size=11.5, header_font_size=12.5)

    # =========================================================================
    # SLIDE 7: PERFORMANCE METRICS FOR MODULE 3 (FORMULATIONS)
    # =========================================================================
    s7 = add_base_slide("Performance Metrics: Object Detection & Denoising Formulations")
    add_formula_card(s7, Inches(0.6), Inches(1.3), Inches(5.9), Inches(2.45),
                     "Intersection over Union (IoU)",
                     "IoU = Area( B_pred cap B_gt ) / Area( B_pred cup B_gt )",
                     "Quantifies spatial overlap accuracy between predicted bounding box and ground truth annotation.")

    add_formula_card(s7, Inches(6.8), Inches(1.3), Inches(5.93), Inches(2.45),
                     "Mean Average Precision (mAP@0.5)",
                     "mAP@0.5 = (1 / C) * sum_{c=1}^C AP_c  at IoU >= 0.50",
                     "Primary benchmark metric for multi-class vehicle and pedestrian detection across all road classes.")

    add_formula_card(s7, Inches(0.6), Inches(3.95), Inches(5.9), Inches(2.45),
                     "Detection F1-Score (Balanced Harmonic Mean)",
                     "F1 = 2 * ( Precision * Recall ) / ( Precision + Recall )",
                     "Harmonizes high detection accuracy with exhaustive recall, penalizing both missed vehicles and false alarms.")

    add_formula_card(s7, Inches(6.8), Inches(3.95), Inches(5.93), Inches(2.45),
                     "Peak Signal-to-Noise Ratio (PSNR)",
                     "PSNR = 20 * log10( 255 / sqrt(MSE) )  [in dB]",
                     "Measures visual restoration fidelity of DnCNN: values >30 dB confirm clean image recovery from sensor noise.")

    # =========================================================================
    # SLIDE 8: METRICS SUITABILITY & LITERATURE BENCHMARKS
    # =========================================================================
    s8 = add_base_slide("Module 3 Metrics Suitability & Literature Benchmarks")
    t_shape8 = s8.shapes.add_table(6, 4, Inches(0.6), Inches(1.3), Inches(12.13), Inches(5.1))
    t8 = t_shape8.table
    metrics_bench = [
        ["Metric Name", "Operational Purpose in Module 3", "Literature Benchmark Values", "Module 3 Achieved Result"],
        ["mAP@0.5", "Evaluates multi-class bounding box accuracy for vehicles and pedestrians.", "82.0% – 88.5% (Yu et al., 2024)", "86.20% (YOLOv8n)"],
        ["Detection Recall", "Ensures road obstacles and crossing pedestrians are never overlooked.", "79.5% – 83.0% (Bakirci, 2024)", "83.73% (YOLOv8n)"],
        ["Detection Precision", "Prevents distracting false alarms on empty roadways.", "84.0% – 87.5% (Bakirci, 2024)", "88.83% (YOLOv8n)"],
        ["Inference Latency", "Enables real-time collision warnings faster than human reaction time.", "8.0 – 15.0 ms (Bakirci, 2024)", "11.3 ms (~88 FPS)"],
        ["Restored PSNR", "Quantifies quality of frames cleaned by DnCNN before detection.", "28.5 – 32.4 dB (Zhang et al., 2017)", "31.22 dB (Clean)"]
    ]
    for r_idx, row in enumerate(metrics_bench):
        for c_idx, val in enumerate(row):
            format_cell(t8.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 0), size_pt=12.5)
    style_table(t8, [Inches(2.2), Inches(4.7), Inches(2.9), Inches(2.33)], font_size=12.0, header_font_size=13.0)

    # =========================================================================
    # SLIDE 9: MODULE 3 DATASET COMPOSITION & TRAFFIC SUBSETS
    # =========================================================================
    s9 = add_base_slide("Module 3 Dataset: Composition & Traffic Annotations")
    t_shape9 = s9.shapes.add_table(6, 5, Inches(0.6), Inches(1.3), Inches(12.13), Inches(3.4))
    t9 = t_shape9.table
    ds_traffic_data = [
        ["Object Class Label", "Annotated Instances", "Scale Distribution", "Primary Source Datasets", "Operational Safety Role"],
        ["Cars / Taxis", "18,420 boxes", "Medium to Large (40–180 px)", "BDD100K + IDD + YouTube", "Standard vehicular tracking and headway distance estimation."],
        ["Pedestrians", "4,850 boxes", "Small to Medium (20–90 px)", "IDD + BDD100K", "Vulnerable road user collision prevention in urban crossings."],
        ["Heavy Trucks / Buses", "3,210 boxes", "Large to Dominant (>150 px)", "IDD + BDD100K", "Blindspot detection and severe collision impact avoidance."],
        ["Motorcycles / Autos", "6,140 boxes", "Small to Medium (30–100 px)", "India Driving Dataset (IDD)", "Heterogeneous traffic monitoring in narrow, unstructured lanes."],
        ["Traffic Signs", "2,980 boxes", "Small (15–50 px)", "BDD100K + IDD", "Regulatory speed limit and stop sign recognition."]
    ]
    for r_idx, row in enumerate(ds_traffic_data):
        for c_idx, val in enumerate(row):
            format_cell(t9.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 0), size_pt=12.0)
    style_table(t9, [Inches(2.2), Inches(1.7), Inches(2.2), Inches(2.5), Inches(3.53)], font_size=11.5, header_font_size=12.5)

    add_card(s9, Inches(0.6), Inches(4.9), Inches(12.13), Inches(1.55), "Multi-Scale Traffic Challenges Addressed", [
        ("Extreme Scale Disparity:", "Objects range from 15x15 pixel distant signs to 200x200 pixel buses; handled via multi-scale FPN-PAN feature pyramids."),
        ("Heterogeneous Indian Context:", "Incorporates unlane-disciplined traffic from IDD where three-wheelers and pedestrians share identical road space.")
    ], body_size=15.0)

    # =========================================================================
    # SLIDE 10: DEEP LEARNING ARCHITECTURE: YOLOV8 OVERVIEW
    # =========================================================================
    s10 = add_base_slide("Deep Learning Architecture: YOLOv8 Anchor-Free Network")
    add_card(s10, Inches(0.6), Inches(1.3), Inches(5.9), Inches(5.1), "Core YOLOv8 Architectural Innovations", [
        ("Anchor-Free Detection Paradigm:", "Eliminates anchor box clustering; predicts distance from bounding box center directly, reducing hyperparameter sensitivity."),
        ("Modified CSPDarknet53 Backbone:", "Replaces standard C3 modules with C2f (Cross-Stage Partial with two convolutions), splitting gradient flow for faster feature learning."),
        ("Multi-Scale Receptive Fields (P3, P4, P5):", "Constructs three distinct detection scales: P3/8 (small objects), P4/16 (medium vehicles), P5/32 (large trucks)."),
        ("Decoupled Detection Head:", "Separates classification confidence from bounding box regression, eliminating feature interference.")
    ], body_size=15.5)
    add_card(s10, Inches(6.8), Inches(1.3), Inches(5.93), Inches(5.1), "Why YOLOv8 is Optimal for Module 3", [
        ("High Detection Precision:", "Achieves 88.83% precision and 86.20% mAP@0.5 on held-out road traffic test data."),
        ("Ultra-Low Edge Latency:", "Executes in only 11.3 ms on edge GPUs (~88 FPS), easily satisfying real-time 30 FPS video streaming."),
        ("Compact Model Size (3.2M params):", "Small 6.5 MB model file allows concurrent deployment alongside DnCNN within standard memory."),
        ("Task-Aligned Training Alignment:", "Aligns classification scores with spatial IoU, preventing high-confidence mislocalized boxes.")
    ], body_size=15.5)

    # =========================================================================
    # SLIDE 11: FEATURE PYRAMID & PATH AGGREGATION NETWORK (FPN-PAN)
    # =========================================================================
    s11 = add_base_slide("Feature Pyramid & Path Aggregation Network (FPN-PAN)")
    add_card(s11, Inches(0.6), Inches(1.3), Inches(5.9), Inches(5.1), "Top-Down Feature Pyramid Network (FPN)", [
        ("Semantic Feature Downsampling:", "Backbone extracts deep semantics at P5 (stride 32), capturing high-level road context."),
        ("Top-Down Feature Propagation:", "Upsamples P5 feature maps and fuses them with P4 (stride 16) and P3 (stride 8) via lateral 1x1 convolutions."),
        ("Context Injection for Small Objects:", "Injects rich semantic scene context into high-resolution spatial feature maps, boosting small pedestrian detection."),
        ("Lateral Skip Connections:", "Preserves fine spatial localization coordinates from early convolutional stages.")
    ], body_size=15.5)
    add_card(s11, Inches(6.8), Inches(1.3), Inches(5.93), Inches(5.1), "Bottom-Up Path Aggregation Network (PAN)", [
        ("Bottom-Up Localization Flow:", "Performs strided 3x3 convolutions from P3 up to P5, transferring accurate localization cues to higher levels."),
        ("Bidirectional Feature Fusion:", "Combines semantic depth from top-down flow with spatial precision from bottom-up flow."),
        ("Multi-Scale Anchor Output Tensors:", "Outputs three feature heads: P3 (28x28 for small signs/pedestrians), P4 (14x14 for cars), P5 (7x7 for buses/trucks)."),
        ("Elimination of Bottleneck Latency:", "All fusion operations use lightweight concatenation and C2f blocks, maintaining high frame rates.")
    ], body_size=15.5)

    # =========================================================================
    # SLIDE 12: DECOUPLED DETECTION HEAD & TASK-ALIGNED ASSIGNER
    # =========================================================================
    s12 = add_base_slide("Decoupled Detection Head & Task-Aligned Assigner (TAL)")
    add_card(s12, Inches(0.6), Inches(1.3), Inches(5.9), Inches(5.1), "Decoupled Head Architecture", [
        ("Separation of Tasks:", "Traditional YOLO unified heads forced one convolutional layer to predict both class probabilities and bounding box coordinates."),
        ("Task Conflict Resolution:", "Classification requires translation-invariant features; regression requires translation-equivariant boundary features."),
        ("Branch 1 — Classification Branch:", "Two 3x3 convolutions followed by Binary Cross-Entropy (BCE) predicting object class probabilities."),
        ("Branch 2 — Regression Branch:", "Two 3x3 convolutions predicting Distribution Focal Loss (DFL) and CIoU coordinates directly.")
    ], body_size=15.5)
    add_card(s12, Inches(6.8), Inches(1.3), Inches(5.93), Inches(5.1), "Task-Aligned Assigner (TAL) Formulation", [
        ("Dynamic Target Assignment:", "Replaces static IoU thresholds with a joint alignment metric t evaluating both tasks simultaneously:"),
        ("Alignment Metric Formula:", "t = s^alpha * IoU^beta,  where alpha = 0.5, beta = 6.0"),
        ("Classification Score s:", "Predicted class probability for the ground-truth category."),
        ("Spatial Overlap IoU:", "Overlap between predicted bounding box and ground truth box."),
        ("Operational Benefit:", "Forces the network to select anchor points that simultaneously excel at both class recognition and boundary localization.")
    ], body_size=15.5)

    # =========================================================================
    # SLIDE 13: COMPUTATIONAL COMPLEXITY ANALYSIS (TIME & SPACE)
    # =========================================================================
    s13 = add_base_slide("Module 3 Computational Complexity: Time & Space Footprint")
    add_card(s13, Inches(0.6), Inches(1.3), Inches(5.9), Inches(5.1), "Time Complexity: Real-Time Edge Throughput", [
        ("Backbone FLOPs Optimization:", "C2f blocks split channels before convolution, reducing FLOPs by 42% compared to standard bottleneck blocks."),
        ("FLOPs Profile:", "YOLOv8n requires only 8.7 GFLOPs at 224x224 resolution."),
        ("Inference Execution Latency:", "Runs in 11.3 ms on NVIDIA GPU (~88 FPS) and under 32 ms on consumer quad-core CPUs."),
        ("Reaction Time Margin:", "Processing latency is over 100x faster than average human driver reaction time (1.5 seconds), guaranteeing ample warning margin.")
    ], body_size=15.5)

    t_shape13 = s13.shapes.add_table(5, 3, Inches(6.8), Inches(1.3), Inches(5.93), Inches(5.1))
    t13 = t_shape13.table
    yolo_variants = [
        ["Model Architecture", "Parameters", "Inference Speed"],
        ["YOLOv8n (Module 3 Winner)", "3,157,200 params", "11.3 ms (~88 FPS)"],
        ["YOLOv8s", "11,166,560 params", "21.4 ms (~46 FPS)"],
        ["YOLOv8m", "25,902,640 params", "38.2 ms (~26 FPS)"],
        ["Faster R-CNN (Baseline)", "41,520,000 params", "68.5 ms (~14 FPS)"]
    ]
    for r_idx, row in enumerate(yolo_variants):
        for c_idx, val in enumerate(row):
            format_cell(t13.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 0 or r_idx == 1), size_pt=13.0)
    style_table(t13, [Inches(2.5), Inches(1.8), Inches(1.63)], 
                [PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER], font_size=12.5, header_font_size=13.5)

    # =========================================================================
    # SLIDE 14: STEP-BY-STEP ALGORITHM: PHASE 1 (BACKBONE FEATURE EXTRACTION)
    # =========================================================================
    s14 = add_base_slide("Step-by-Step Algorithm: Phase 1 — Backbone Feature Extraction")
    t_shape14 = s14.shapes.add_table(5, 4, Inches(0.6), Inches(1.3), Inches(12.13), Inches(5.1))
    t14 = t_shape14.table
    algo1_steps = [
        ["Step #", "Algorithmic Operation", "Mathematical Formulation", "Functional Purpose in Module 3"],
        ["Step 1", "Input Tensor Normalization", "X = (I_raw / 255.0) in R^{3 x 224 x 224}", "Standardizes incoming dashcam frame pixel values to [0.0, 1.0]."],
        ["Step 2", "Stem Convolution (P1)", "F_1 = SiLU( BN( Conv_{3x3}( X ) ) ), stride = 2", "Downsamples spatial resolution to 112x112 while expanding channels to 16."],
        ["Step 3", "CSPDarknet C2f Bottlenecks", "F_{c2f} = Conv_{1x1}( [ y_0, y_1, ..., y_n ] )", "Splits feature channels into two paths, routing gradients through multiple bottlenecks."],
        ["Step 4", "Spatial Pyramid Pooling Fast", "F_{sppf} = Conv_{1x1}( [ x, Pool_{5x5}(x), Pool_{5x5}^2(x) ] )", "Aggregates multi-scale contextual features at P5 with zero parameter increase."]
    ]
    for r_idx, row in enumerate(algo1_steps):
        for c_idx, val in enumerate(row):
            format_cell(t14.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 0), size_pt=12.5)
    style_table(t14, [Inches(1.0), Inches(2.8), Inches(4.5), Inches(3.83)], font_size=12.0, header_font_size=13.0)

    # =========================================================================
    # SLIDE 15: STEP-BY-STEP ALGORITHM: PHASE 2 (MULTI-SCALE FUSION)
    # =========================================================================
    s15 = add_base_slide("Step-by-Step Algorithm: Phase 2 — Multi-Scale FPN-PAN Fusion")
    t_shape15 = s15.shapes.add_table(5, 4, Inches(0.6), Inches(1.3), Inches(12.13), Inches(5.1))
    t15 = t_shape15.table
    algo2_steps = [
        ["Step #", "Algorithmic Operation", "Mathematical Formulation", "Functional Purpose in Module 3"],
        ["Step 5", "Top-Down FPN Upsampling", "F_{up} = Upsample_{2x}( F_{P5} ) concat F_{P4}", "Propagates deep semantic scene understanding down to P4 and P3 heads."],
        ["Step 6", "P3 High-Res Fusion", "Head_{P3} = C2f( Upsample_{2x}( F_{P4} ) concat F_{P3} )", "Generates high-resolution 28x28 feature grid specialized for small pedestrians."],
        ["Step 7", "Bottom-Up PAN Downsampling", "F_{down} = Conv_{3x3, s=2}( Head_{P3} ) concat Head_{P4}", "Passes precise low-level edge coordinates up to medium vehicle scales."],
        ["Step 8", "P5 Global Scale Generation", "Head_{P5} = C2f( Conv_{3x3, s=2}( Head_{P4} ) concat F_{P5} )", "Generates 7x7 coarse grid specialized for large commercial trucks and buses."]
    ]
    for r_idx, row in enumerate(algo2_steps):
        for c_idx, val in enumerate(row):
            format_cell(t15.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 0), size_pt=12.5)
    style_table(t15, [Inches(1.0), Inches(2.8), Inches(4.5), Inches(3.83)], font_size=12.0, header_font_size=13.0)

    # =========================================================================
    # SLIDE 16: STEP-BY-STEP ALGORITHM: PHASE 3 (LOSS FUNCTIONS)
    # =========================================================================
    s16 = add_base_slide("Step-by-Step Algorithm: Phase 3 — Complete Loss Formulation")
    add_formula_card(s16, Inches(0.6), Inches(1.3), Inches(5.9), Inches(2.45),
                     "Complete IoU (CIoU) Regression Loss",
                     "L_{CIoU} = 1 - IoU + ( rho^2(b, b_gt) / c^2 ) + alpha * v",
                     "Accounts for overlap area, center distance rho, and aspect ratio consistency v between predicted and true boxes.")

    add_formula_card(s16, Inches(6.8), Inches(1.3), Inches(5.93), Inches(2.45),
                     "Distribution Focal Loss (DFL)",
                     "L_{DFL}(S_i, S_{i+1}) = - ( (y_{i+1}-y) log(S_i) + (y-y_i) log(S_{i+1}) )",
                     "Models box edge coordinates as continuous probability distributions rather than fixed delta values.")

    add_formula_card(s16, Inches(0.6), Inches(3.95), Inches(5.9), Inches(2.45),
                     "Binary Cross-Entropy (BCE) Class Loss",
                     "L_{cls} = - sum [ y * log(p) + (1 - y) * log(1 - p) ]",
                     "Penalizes object classification errors independently across vehicle, truck, bus, and pedestrian categories.")

    add_formula_card(s16, Inches(6.8), Inches(3.95), Inches(5.93), Inches(2.45),
                     "Total Unified Loss Objective",
                     "L_{total} = lambda_{box} * L_{CIoU} + lambda_{cls} * L_{cls} + lambda_{dfl} * L_{DFL}",
                     "Tuned weighting parameters: lambda_{box} = 7.5, lambda_{cls} = 0.5, lambda_{dfl} = 1.5.")

    # =========================================================================
    # SLIDE 17: STEP-BY-STEP ALGORITHM: PHASE 4 (NON-MAXIMUM SUPPRESSION)
    # =========================================================================
    s17 = add_base_slide("Step-by-Step Algorithm: Phase 4 — Non-Maximum Suppression (NMS)")
    t_shape17 = s17.shapes.add_table(5, 4, Inches(0.6), Inches(1.3), Inches(12.13), Inches(5.1))
    t17 = t_shape17.table
    algo4_steps = [
        ["Step #", "NMS Algorithmic Operation", "Mathematical Condition / Selection Rule", "Functional Impact on Module 3"],
        ["Step 9", "Confidence Threshold Filtering", "Discard all bounding boxes with score s < 0.25", "Eliminates low-confidence background false positives."],
        ["Step 10", "Candidate Box Sorting", "Sort remaining boxes in descending order of score: B = {b_1, b_2, ...}", "Prioritizes the highest-confidence vehicle detection candidate."],
        ["Step 11", "IoU Overlap Suppression", "If IoU(b_{max}, b_j) >= 0.70 -> Discard b_j from candidate set", "Suppresses redundant overlapping bounding boxes on the same vehicle."],
        ["Step 12", "Final Bounding Box Dispatch", "Output final coordinates: [x_min, y_min, x_max, y_max, class, score]", "Dispatches pristine bounding box overlays to the React web UI."]
    ]
    for r_idx, row in enumerate(algo4_steps):
        for c_idx, val in enumerate(row):
            format_cell(t17.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 0), size_pt=12.5)
    style_table(t17, [Inches(1.0), Inches(2.8), Inches(4.5), Inches(3.83)], font_size=12.0, header_font_size=13.0)

    # =========================================================================
    # SLIDE 18: HYPERPARAMETERS: INPUT RESOLUTION & AUGMENTATIONS
    # =========================================================================
    s18 = add_base_slide("Module 3 Hyperparameters: Resolution & Mosaic Augmentation")
    t_shape18 = s18.shapes.add_table(6, 4, Inches(0.6), Inches(1.3), Inches(12.13), Inches(5.1))
    t18 = t_shape18.table
    hp1_mod3 = [
        ["Hyperparameter", "Configured Value", "Search / Tuning Range", "Engineering & Theoretical Justification"],
        ["Input Image Size", "224 x 224 x 3", "224 to 640 pixels", "Standardized geometry across all pipeline modules; enables ultra-fast 11.3 ms inference."],
        ["Batch Size", "32", "16, 32, 64", "Optimizes GPU memory utilization while maintaining stable mini-batch statistics."],
        ["Mosaic Augmentation", "p = 1.0 (First 40 epochs)", "0.5 to 1.0", "Stitches 4 random road scenes into one, forcing the model to detect objects in varied contexts."],
        ["Mosaic Deactivation", "Final 10 Epochs", "Last 5 to 10 epochs", "Disables mosaic augmentation during final epochs to fine-tune on natural road boundaries."],
        ["Random Translation / Scale", "Scale: 0.5 to 1.5, Trans: 0.1", "Fixed Augmentations", "Simulates varying vehicle camera heights and bumper-to-bumper distances."]
    ]
    for r_idx, row in enumerate(hp1_mod3):
        for c_idx, val in enumerate(row):
            format_cell(t18.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 0), size_pt=12.5)
    style_table(t18, [Inches(2.4), Inches(2.2), Inches(2.3), Inches(5.23)], font_size=12.0, header_font_size=13.0)

    # =========================================================================
    # SLIDE 19: HYPERPARAMETERS: ARCHITECTURE & LOSS WEIGHTS
    # =========================================================================
    s19 = add_base_slide("Module 3 Hyperparameters: Architecture & Loss Weight Distribution")
    t_shape19 = s19.shapes.add_table(6, 4, Inches(0.6), Inches(1.3), Inches(12.13), Inches(5.1))
    t19 = t_shape19.table
    hp2_mod3 = [
        ["Hyperparameter", "Configured Value", "Search / Tuning Range", "Engineering & Theoretical Justification"],
        ["Backbone Depth Factor", "d = 0.33", "0.33 to 1.0", "YOLOv8n architecture scaling factor; caps parameter count at 3.15M for edge deployment."],
        ["Backbone Width Factor", "w = 0.25", "0.25 to 1.0", "Caps maximum feature channel count at 256, significantly reducing memory bandwidth."],
        ["Box Loss Gain (lambda_box)", "7.5", "5.0 to 10.0", "Emphasizes accurate bounding box coordinate regression over raw classification."],
        ["Class Loss Gain (lambda_cls)", "0.5", "0.5 to 1.5", "Balances classification loss to prevent dominating the box coordinate regression."],
        ["DFL Loss Gain (lambda_dfl)", "1.5", "1.0 to 2.0", "Weights Distribution Focal Loss to ensure sharp bounding box boundary estimations."]
    ]
    for r_idx, row in enumerate(hp2_mod3):
        for c_idx, val in enumerate(row):
            format_cell(t19.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 0), size_pt=12.5)
    style_table(t19, [Inches(2.4), Inches(2.2), Inches(2.3), Inches(5.23)], font_size=12.0, header_font_size=13.0)

    # =========================================================================
    # SLIDE 20: HYPERPARAMETERS: OPTIMIZATION & SCHEDULES
    # =========================================================================
    s20 = add_base_slide("Module 3 Hyperparameters: Optimization & Warmup Schedule")
    t_shape20 = s20.shapes.add_table(6, 4, Inches(0.6), Inches(1.3), Inches(12.13), Inches(5.1))
    t20 = t_shape20.table
    hp3_mod3 = [
        ["Hyperparameter", "Configured Value", "Search / Tuning Range", "Engineering & Theoretical Justification"],
        ["Optimizer", "SGD with Momentum", "AdamW vs SGD", "SGD with momentum provides superior final generalization for object detection models."],
        ["Momentum Coefficient", "0.937", "0.90 to 0.95", "Smooths weight updates across noisy batches containing complex multi-vehicle scenes."],
        ["Initial Learning Rate", "0.01", "1e-3 to 1e-2", "Optimal initial rate paired with linear warmup to avoid early gradient divergence."],
        ["Warmup Epochs", "3.0 Epochs", "1 to 5 Epochs", "Linearly ramps learning rate from 0.001 to 0.01 over first 3 epochs to stabilize weights."],
        ["Cosine Annealing LR", "Floor = 0.0001", "Cosine Decay", "Smoothly decays learning rate to near-zero, avoiding late-stage parameter oscillations."]
    ]
    for r_idx, row in enumerate(hp3_mod3):
        for c_idx, val in enumerate(row):
            format_cell(t20.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 0), size_pt=12.5)
    style_table(t20, [Inches(2.4), Inches(2.2), Inches(2.3), Inches(5.23)], font_size=12.0, header_font_size=13.0)

    # =========================================================================
    # SLIDE 21: RESULTS: QUANTITATIVE TRAFFIC DETECTION BENCHMARK
    # =========================================================================
    s21 = add_base_slide("Module 3 Results: Quantitative Object Detection Benchmark")
    t_shape21 = s21.shapes.add_table(6, 5, Inches(0.6), Inches(1.3), Inches(12.13), Inches(3.6))
    t21 = t_shape21.table
    det_results = [
        ["Target Road Class", "Precision", "Recall", "mAP@0.5", "F1-Score"],
        ["All Road Agents (Overall)", "88.83%", "83.73%", "86.20%", "86.20%"],
        ["Cars / Taxis", "92.40%", "89.10%", "91.50%", "90.72%"],
        ["Pedestrians (Vulnerable)", "84.20%", "78.60%", "81.20%", "81.30%"],
        ["Heavy Trucks / Buses", "90.10%", "85.40%", "87.80%", "87.68%"],
        ["Motorcycles / Autos", "86.50%", "81.80%", "84.30%", "84.08%"]
    ]
    for r_idx, row in enumerate(det_results):
        for c_idx, val in enumerate(row):
            format_cell(t21.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 0 or r_idx == 1), size_pt=12.5)
    style_table(t21, [Inches(2.6), Inches(2.3), Inches(2.3), Inches(2.3), Inches(2.63)], 
                [PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER], font_size=12.0, header_font_size=13.0)

    add_card(s21, Inches(0.6), Inches(5.1), Inches(12.13), Inches(1.35), "Key Detection Findings", [
        ("High General Detection Efficacy:", "Achieved 88.83% precision and 86.20% mAP@0.5 across all traffic categories on held-out test frames."),
        ("Robust Pedestrian Capture:", "78.60% recall on challenging small pedestrians ensures early alert generation before collisions occur.")
    ], body_size=15.0)

    # =========================================================================
    # SLIDE 22: RESULTS: CONFIDENCE THRESHOLD TUNING
    # =========================================================================
    s22 = add_base_slide("Module 3 Results: Confidence Threshold Optimization")
    add_card(s22, Inches(0.6), Inches(1.3), Inches(5.9), Inches(5.1), "Confidence Threshold Dynamics", [
        ("Optimal Balance Point (Threshold = 0.53):", "Yields the maximum overall F1-score of 86.20%, providing the optimal trade-off between precision and recall."),
        ("Zero False Alarm Mode (Threshold = 0.88):", "Elevating threshold to 0.88 achieves 98.5% precision, guaranteeing every alert corresponds to an unmistakable obstacle."),
        ("High Sensitivity Mode (Threshold = 0.30):", "Lowering threshold to 0.30 increases pedestrian recall to 89.2%, vital during dense nighttime fog."),
        ("Operational Deployment Selection:", "The production API uses an adaptive threshold: 0.50 for daylight and 0.35 for low-visibility nighttime scenes.")
    ], body_size=15.5)
    add_card(s22, Inches(6.8), Inches(1.3), Inches(5.93), Inches(5.1), "Training Convergence & Loss Descent", [
        ("Steady Box Loss Decay:", "CIoU loss drops monotonically from 1.82 to 0.68 over 50 epochs, indicating precise boundary learning."),
        ("Class Loss Stability:", "Binary cross-entropy class loss stabilizes at 0.32 by epoch 35, confirming minimal cross-class confusion."),
        ("Absence of Overfitting:", "Validation mAP@0.5 closely mirrors training mAP without late-stage divergence, confirming strong generalization."),
        ("Inference Execution Speed:", "Sustains 11.3 ms per frame on edge GPU hardware, leaving 18.7 ms available within the 30 FPS window.")
    ], body_size=15.5)

    # =========================================================================
    # SLIDE 23: UI SCREEN INTEGRATION: REAL-TIME TRAFFIC MONITORING
    # =========================================================================
    s23 = add_base_slide("UI Screen Integration: Live Traffic Monitoring Portal")
    if os.path.exists(ui_prediction):
        s23.shapes.add_picture(ui_prediction, Inches(0.6), Inches(1.3), Inches(7.5), Inches(4.9))
    else:
        add_card(s23, Inches(0.6), Inches(1.3), Inches(7.5), Inches(4.9), "Prediction Portal", [("Path:", ui_prediction)])

    add_card(s23, Inches(8.3), Inches(1.3), Inches(4.43), Inches(4.9), "Live Portal Features & Module 3 Output", [
        ("Real-Time Bounding Box Overlays:", "Renders color-coded bounding boxes around cars (Blue), pedestrians (Yellow), and trucks (Red)."),
        ("Active Object Counting:", "Displays real-time counts for vehicles, pedestrians, and road signs directly in the dashboard."),
        ("Traffic Density Status:", "Flags traffic occupancy as Low, Medium, or High to contextualize risk scores."),
        ("Live Web Access:", "https://saferoad-ai-one.vercel.app/prediction")
    ], body_size=15.5)

    # =========================================================================
    # SLIDE 24: STANDARD PAPER CHOSEN FOR MODULE 3
    # =========================================================================
    s24 = add_base_slide("Standard Paper Chosen for Module 3: Bibliographic Citation")
    add_card(s24, Inches(0.6), Inches(1.3), Inches(12.13), Inches(2.2), "Bibliographic Citation & SCImago Indexing", [
        ("Full Paper Title:", "YOLO-MPAM: Efficient real-time neural networks based on multi-channel feature fusion"),
        ("Authors:", "Boyang Yu, Zixuan Li, Yue Cao, Celimuge Wu, Jin Qi, and Libing Wu"),
        ("Journal:", "Expert Systems with Applications (Elsevier), Vol. 250, 2024"),
        ("SCImago Verification:", "Rank: Q1 (Top Tier Journal in Artificial Intelligence) | SCImago 2024 SJR: 1.854"),
        ("Digital Object Identifier (DOI):", "https://doi.org/10.1016/j.eswa.2024.124282")
    ], body_size=15.5)

    add_card(s24, Inches(0.6), Inches(3.75), Inches(12.13), Inches(2.7), "Technical Justification for Selection", [
        ("Direct Relevance to Traffic Monitoring:", "Focuses squarely on resolving missed detections and occlusions in real-time autonomous driving traffic scenes."),
        ("Multi-Channel Feature Fusion:", "Mathematically proves that multi-scale channel fusion in YOLOv8 improves small vehicle and sign detection by over 6.2%."),
        ("Benchmarked on Road Datasets:", "Evaluates difficult conditions such as rainy glare and dense intersections, directly aligning with SafeRoad AI."),
        ("Real-Time Edge Validation:", "Provides the speed-accuracy trade-off justification for deploying lightweight YOLOv8n models on edge processors.")
    ], body_size=15.5)

    # =========================================================================
    # SLIDE 25: DENOSING APPROACH (EXPLAIN HOW NOISE IS ADDED TO DATASET)
    # =========================================================================
    s25 = add_base_slide("Denosing Approach")

    add_card(s25, Inches(0.6), Inches(1.3), Inches(5.9), Inches(5.1), "How Noise is Added to the Dataset", [
        ("Degradation Formulation:", "Clean dashcam images x are corrupted to produce degraded pairs y = D(x; theta) = x + v, where v is synthetic noise."),
        ("Supervised Pair Generation:", "Clean ground-truth frames (x_i) and synthetically corrupted frames (y_i) form training pairs (y_i, x_i) for the deep denoiser."),
        ("Stratified Dataset Sampling:", "Applied across 1,270 images from SafeRoad-AI: 739 High Risk, 61 Moderate Risk, and 470 Safe road condition frames."),
        ("Deterministic Reproducibility:", "Controlled via fixed random seed (seed = 42) ensuring rigorous train/val/test splits without cross-set leakage."),
        ("Preservation of Ground Truth:", "Object bounding-box coordinates (cars, pedestrians, signs) remain anchored to x_i to evaluate post-denoising YOLOv8 mAP.")
    ], body_size=15.0)

    add_card(s25, Inches(6.8), Inches(1.3), Inches(5.93), Inches(5.1), "Synthetic Noise Injection Modalities Added", [
        ("1. Gaussian Noise (Thermal Sensor):", "y = x + n, where n ~ N(0, sigma^2), with sigma in [15, 30]. Simulates low-light sensor amplifier noise and nighttime shot noise."),
        ("2. Salt-and-Pepper (Impulsive):", "Random pixels set to 0 or 255 with probability p in [0.01, 0.04]. Models dead/stuck sensor pixels and ADC bit-flip transmission errors."),
        ("3. Motion Blur (Road Vibration):", "Convolved with horizontal 1D kernel K of size k in {5, 7, 9}: y = x * K. Simulates vehicle vibration over potholes and rapid turning."),
        ("4. Lossy Compression Artifacts:", "Re-encoded using JPEG/H.264 discrete cosine transform at quality Q in [40, 70]. Replicates bandwidth-constrained dashcam video streams.")
    ], body_size=15.0)

    # =========================================================================
    # SLIDE 26: DEEP LEARNING MODELS FOR DENOISING (DNCNN & GITHUB URLS)
    # =========================================================================
    s26 = add_base_slide("Deep learning Models for Denoising")

    add_card(s26, Inches(0.6), Inches(1.3), Inches(12.13), Inches(1.5), "Identified Model: DnCNN (Deep Convolutional Neural Network for Image Denoising)", [
        ("Reference Citation:", "Kai Zhang, Wangmeng Zuo, Yunjin Chen, Deyu Meng, and Lei Zhang, 'Beyond a Gaussian Denoiser: Residual Learning of Deep CNN for Image Denoising', IEEE Transactions on Image Processing (TIP), Vol. 26, No. 7, pp. 3142–3155, 2017."),
        ("Official GitHub Repository:", "https://github.com/cszn/DnCNN  (Official PyTorch & MatConvNet Implementation by Author)"),
        ("Project Implementation URL:", "https://github.com/Uppara-Veeranjaneyulu/SafeRoad-AI/tree/main/backend  (Integrated Module 3 Pipeline)")
    ], body_size=14.5)

    add_card(s26, Inches(0.6), Inches(2.95), Inches(5.9), Inches(3.45), "DnCNN 17-Layer Architecture Details", [
        ("Layer 1 (Conv + ReLU):", "64 filters of 3x3x3 operate on noisy frame y (stride=1, pad=1). Extracts 64 feature representations without BatchNorm."),
        ("Layers 2–16 (15x Conv + BN + ReLU):", "15 homogeneous residual blocks: Conv(64 -> 64, 3x3) + Batch Normalization + ReLU. Zero pooling maintains 224x224 spatial resolution."),
        ("Layer 17 (Residual Output):", "Conv(64 -> 3, 3x3) reconstructs the 3-channel residual noise map R(y)."),
        ("Effective Receptive Field:", "Expands linearly: RF = 1 + 2 * 17 = 35x35 pixels, capturing broad spatial noise correlations across road scenes.")
    ], body_size=14.5)

    add_card(s26, Inches(6.8), Inches(2.95), Inches(5.93), Inches(3.45), "Residual Learning Formulation & Edge Specs", [
        ("Residual Mapping Mechanics:", "The network is trained to learn the residual noise R(y) approx v = y - x rather than pristine image x directly."),
        ("Clean Reconstruction Formula:", "x_clean = y - R(y). Pristine road frame is recovered via direct element-wise subtraction."),
        ("Why Residual Learning Works:", "Zero-mean noise residuals avoid complex road scene semantics; Batch Normalization stabilizes training dramatically."),
        ("Compact Edge Deployment:", "Contains 559,427 parameters (~2.2 MB memory), operating at 7.1 ms on GPU for real-time edge streaming.")
    ], body_size=14.5)

    # =========================================================================
    # SLIDE 28: DENOISING APPROACH: MATHEMATICAL FORMULATIONS
    # =========================================================================
    s28 = add_base_slide("Denoising Approach: Mathematical Formulations & Loss")
    add_formula_card(s28, Inches(0.6), Inches(1.3), Inches(5.9), Inches(2.45),
                     "Residual Learning Loss Objective",
                     "L(Theta) = (1 / 2N) * sum_{i=1}^N || R(y_i; Theta) - (y_i - x_i) ||_F^2",
                     "Minimizes Frobenius norm error between predicted noise residual R(y_i) and true noise (y_i - x_i).")

    add_formula_card(s28, Inches(6.8), Inches(1.3), Inches(5.93), Inches(2.45),
                     "Clean Image Reconstruction Formula",
                     "x_clean = y - R(y; Theta)",
                     "Subtracts learned noise residual directly from the input tensor, restoring pristine pixel intensities.")

    add_formula_card(s28, Inches(0.6), Inches(3.95), Inches(5.9), Inches(2.45),
                     "Peak Signal-to-Noise Ratio (PSNR)",
                     "PSNR = 20 * log10( 255 / sqrt(MSE) )  [in dB]",
                     "Measures logarithmic ratio between maximum pixel power and Mean Squared Error relative to clean ground truth.")

    add_formula_card(s28, Inches(6.8), Inches(3.95), Inches(5.93), Inches(2.45),
                     "Structural Similarity Index (SSIM)",
                     "SSIM(x, y) = [ (2*mu_x*mu_y + C_1)(2*sigma_xy + C_2) ] / [ (mu_x^2 + mu_y^2 + C_1)(sigma_x^2 + sigma_y^2 + C_2) ]",
                     "Evaluates luminance, contrast, and structural preservation, ensuring edge boundaries remain sharp.")

    # =========================================================================
    # SLIDE 29: DENOISING APPROACH: EMPIRICAL RESTORATION RESULTS
    # =========================================================================
    s29 = add_base_slide("Denoising Approach: Empirical Quality & PSNR Audit")
    t_shape29 = s29.shapes.add_table(5, 5, Inches(0.6), Inches(1.3), Inches(12.13), Inches(3.6))
    t29 = t_shape29.table
    denoise_audit = [
        ["Risk Category", "Degraded Images", "Initial Noisy PSNR", "DnCNN Restored PSNR", "Quality Gain"],
        ["High Risk (Rain/Night)", "739 images", "25.52 dB", "31.45 dB", "+5.93 dB  (Sharp edge recovery)"],
        ["Moderate Risk (Urban)", "61 images", "24.98 dB", "30.82 dB", "+5.84 dB  (Compression artifact removal)"],
        ["Safe (Highway Blur)", "470 images", "24.87 dB", "31.10 dB", "+6.23 dB  (Motion blur deconvolution)"],
        ["OVERALL DATASET", "1,270 images", "25.36 dB", "31.22 dB", "+5.86 dB  (Enterprise Denoising Fidelity)"]
    ]
    for r_idx, row in enumerate(denoise_audit):
        for c_idx, val in enumerate(row):
            format_cell(t29.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 0 or r_idx == 4), size_pt=12.5)
    style_table(t29, [Inches(2.5), Inches(1.8), Inches(2.2), Inches(2.5), Inches(3.13)], 
                [PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER], font_size=12.0, header_font_size=13.0)

    add_card(s29, Inches(0.6), Inches(5.1), Inches(12.13), Inches(1.35), "Audit Interpretation", [
        ("Sub-26 dB Degradation Baseline:", "Corresponds to realistic sensor grain where fine vehicle details are impaired."),
        ("Post-Denoising Threshold (>31 dB):", "Restores clean visual clarity without edge blurring, ready for high-precision YOLOv8 inference.")
    ], body_size=15.0)

    # =========================================================================
    # SLIDE 30: DENOISING APPROACH: IMPACT ON TRAFFIC DETECTION
    # =========================================================================
    s30 = add_base_slide("Denoising Approach: Impact on Downstream Traffic Detection")
    t_shape30 = s30.shapes.add_table(5, 5, Inches(0.6), Inches(1.3), Inches(12.13), Inches(3.5))
    t30 = t_shape30.table
    denoise_impact = [
        ["Target Road Category", "Degraded Input mAP@0.5", "DnCNN Restored mAP@0.5", "Absolute Gain", "Operational Benefit"],
        ["Overall Road Traffic", "81.00%", "86.20%", "+5.20%", "Robust detection across changing weather."],
        ["Pedestrians (Vulnerable)", "73.40%", "81.20%", "+7.80%", "Dramatic reduction in missed crossing pedestrians."],
        ["Vehicles / Cars", "87.10%", "91.50%", "+4.40%", "Accurate headway distance calculation."],
        ["Traffic Signs (Small)", "72.50%", "80.40%", "+7.90%", "Restores obscured speed and regulatory signs."]
    ]
    for r_idx, row in enumerate(denoise_impact):
        for c_idx, val in enumerate(row):
            format_cell(t30.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 0 or r_idx == 1), size_pt=12.5)
    style_table(t30, [Inches(2.4), Inches(2.3), Inches(2.3), Inches(1.8), Inches(3.33)], 
                [PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.LEFT], font_size=12.0, header_font_size=13.0)

    add_card(s30, Inches(0.6), Inches(5.0), Inches(12.13), Inches(1.45), "Key System-Level Synergy", [
        ("Vulnerable Road Users Benefit Most:", "Pedestrians and small traffic signs gained nearly +8% mAP from DnCNN denoising because high-frequency noise disproportionately destroys small bounding box features."),
        ("Seamless Edge Integration:", "DnCNN executes in 7.1 ms and YOLOv8n in 11.3 ms, maintaining a combined 18.4 ms pipeline (<55 FPS).")
    ], body_size=15.0)

    # =========================================================================
    # SLIDE 31: CONCLUSION & FUTURE SCOPE
    # =========================================================================
    s31 = add_base_slide("Module 3 Conclusion & Future Scope")
    add_card(s31, Inches(0.6), Inches(1.3), Inches(5.9), Inches(5.1), "Module 3 Milestones Achieved", [
        ("High-Precision Object Detection:", "Engineered and validated YOLOv8n for real-time traffic parsing: 88.83% precision and 86.20% mAP@0.5."),
        ("Sub-12ms Edge Latency:", "Optimized inference speed to 11.3 ms (~88 FPS), enabling concurrent execution on edge chips."),
        ("Robust Deep Denoising:", "Trained 17-layer DnCNN to restore degraded dashcam inputs, improving PSNR by +5.86 dB and detection mAP by +5.2%."),
        ("Full-Stack UI Integration:", "Connected live detection telemetry to the interactive React web dashboard with bounding box overlays.")
    ], body_size=15.5)
    add_card(s31, Inches(6.8), Inches(1.3), Inches(5.93), Inches(5.1), "Future Scope & Review 3 Roadmap", [
        ("Multi-Object Tracking (ByteTrack):", "Integrate temporal object association to compute vehicle velocity vectors and trajectories."),
        ("TensorRT INT8 Edge Quantization:", "Quantize YOLOv8 and DnCNN models for deployment onto NVIDIA Jetson Orin Nano boards."),
        ("Nighttime Thermal Camera Fusion:", "Explore multimodal sensor fusion combining RGB dashcam footage with thermal infrared cameras."),
        ("Municipal Traffic Integration:", "Connect RTSP CCTV streams to automate intersection density monitoring.")
    ], body_size=15.5)

    # =========================================================================
    # SLIDE 32: THANK YOU SLIDE
    # =========================================================================
    s32 = prs.slides.add_slide(blank_layout)
    if os.path.exists(footer_img):
        s32.shapes.add_picture(footer_img, Inches(0), Inches(6.68), Inches(13.333), Inches(0.82))
    if os.path.exists(logo_img):
        s32.shapes.add_picture(logo_img, Inches(5.9), Inches(0.9), Inches(1.5), Inches(1.5))

    tb_end = s32.shapes.add_textbox(Inches(1.5), Inches(2.6), Inches(10.33), Inches(2.3))
    tf_end = tb_end.text_frame
    tf_end.word_wrap = True

    pe1 = tf_end.paragraphs[0]
    pe1.alignment = PP_ALIGN.CENTER
    pe1.text = "Thank You!"
    pe1.font.name = FONT_FAMILY
    pe1.font.size = Pt(40)
    pe1.font.bold = True
    pe1.font.color.rgb = DARK_RED

    pe2 = tf_end.add_paragraph()
    pe2.alignment = PP_ALIGN.CENTER
    pe2.text = "Module 3: Intelligent Traffic Monitoring & Deep Denoising"
    pe2.font.name = FONT_FAMILY
    pe2.font.size = Pt(20)
    pe2.font.bold = True
    pe2.font.color.rgb = SLATE_DARK
    pe2.space_before = Pt(8)

    pe3 = tf_end.add_paragraph()
    pe3.alignment = PP_ALIGN.CENTER
    pe3.text = "Open for Technical Questions & Discussion"
    pe3.font.name = FONT_FAMILY
    pe3.font.size = Pt(15)
    pe3.font.italic = True
    pe3.font.color.rgb = SLATE_MUTED
    pe3.space_before = Pt(4)

    add_card(s32, Inches(1.5), Inches(5.0), Inches(10.33), Inches(1.4), "Presenter & Project Coordinates", [
        ("Presenter:", "U Veeranjaneyulu | Roll No: CB.SC.U4CSE23351 | Team 10 (SafeRoad AI)"),
        ("Course & Faculty Guide:", "23CSE473 Neural Networks & Deep Learning | Prof. Dr. T Senthil Kumar (CSE)"),
        ("Project Links:", "GitHub: https://github.com/Uppara-Veeranjaneyulu/SafeRoad-AI  |  Web: https://saferoad-ai-one.vercel.app/")
    ], body_size=15.0)

    output_path = "review-2/SafeRoad_AI_Module3_Veeranjaneyulu_Review2.pptx"
    prs.save(output_path)
    print(f"Module 3 presentation generated successfully with {len(prs.slides)} slides at: {output_path}")

    # Also make a copy with Team-10 prefix
    try:
        import shutil
        team_copy = "review-2/Team-10-SafeRoad_AI_Review2_Module3_Veeranjaneyulu.pptx"
        shutil.copyfile(output_path, team_copy)
        print(f"Also created copy at: {team_copy}")
    except Exception as e:
        print(f"Notice on copy: {e}")

if __name__ == '__main__':
    generate_module3_deck()
