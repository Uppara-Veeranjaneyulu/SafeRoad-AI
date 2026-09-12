import os
import sys
import pptx
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

def build_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Color Scheme matching reference-pptx
    CRIMSON = RGBColor(192, 0, 0)         # Accent Red #C00000
    DARK_RED = RGBColor(139, 0, 0)        # Deep Red #8B0000
    HEADER_FILL = RGBColor(130, 20, 20)   # Dark Crimson Table Header
    SLATE_DARK = RGBColor(15, 23, 42)     # #0F172A Primary text
    SLATE_MUTED = RGBColor(71, 85, 105)   # #475569 Secondary text
    WHITE = RGBColor(255, 255, 255)
    LIGHT_BG = RGBColor(248, 250, 252)    # Card Background #F8FAFC
    CARD_BORDER = RGBColor(226, 232, 240) # #E2E8F0
    ALT_ROW_FILL = RGBColor(245, 247, 250)# Light zebra
    FORMULA_BG = RGBColor(255, 250, 250)  # Subtle warm white for formula boxes
    FORMULA_BORDER = RGBColor(220, 150, 150)

    footer_img = 'extracted_ref_assets/slide_1_Picture 4_0.png'
    logo_img = 'extracted_ref_assets/slide_1_Picture 5_1.png'
    arch_img = 'review-2/architecture-overview.png'

    # Model results
    mobilenet_cm = 'results/mobilenetv2/confusion_matrix.png'
    mobilenet_curves = 'results/mobilenetv2/training_curves.png'

    # UI screenshots
    ui_home = 'ui_screenshots/ui_home.png'
    ui_prediction = 'ui_screenshots/ui_prediction.png'
    ui_dashboard = 'ui_screenshots/ui_dashboard.png'
    ui_analytics = 'ui_screenshots/ui_analytics.png'
    ui_datasets = 'ui_screenshots/ui_datasets.png'

    FONT_FAMILY = 'Times New Roman'

    def add_base_slide(title_text):
        slide = prs.slides.add_slide(blank_layout)
        # Template bottom footer banner
        if os.path.exists(footer_img):
            slide.shapes.add_picture(footer_img, Inches(0), Inches(6.68), Inches(13.333), Inches(0.82))

        # Title Box - Clean Times New Roman, 26pt bold, Dark Red/Slate
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

        # Accent red underline
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

        # Title
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.name = FONT_FAMILY
        p0.font.size = Pt(17.5)
        p0.font.bold = True
        p0.font.color.rgb = DARK_RED
        p0.space_after = Pt(4)

        # Formula text - large, clear, bold
        p_f = tf.add_paragraph()
        p_f.text = formula_display
        p_f.font.name = FONT_FAMILY
        p_f.font.size = Pt(16.0)
        p_f.font.bold = True
        p_f.font.color.rgb = CRIMSON
        p_f.space_after = Pt(4)

        # Explanation
        p_desc = tf.add_paragraph()
        p_desc.text = description
        p_desc.font.name = FONT_FAMILY
        p_desc.font.size = Pt(15.0)
        p_desc.font.color.rgb = SLATE_DARK

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (TEAM 10, AMrita LOGO, 4 MEMBERS)
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
    p1.font.size = Pt(19)
    p1.font.bold = True
    p1.font.color.rgb = CRIMSON

    p2 = tf_hdr.add_paragraph()
    p2.text = "CASE STUDY REVIEW 2 — TEAM 10"
    p2.font.name = FONT_FAMILY
    p2.font.size = Pt(15)
    p2.font.bold = True
    p2.font.color.rgb = SLATE_MUTED

    p3 = tf_hdr.add_paragraph()
    p3.text = "SafeRoad AI: Road-Scene Risk Classification & Traffic Monitoring"
    p3.font.name = FONT_FAMILY
    p3.font.size = Pt(24)
    p3.font.bold = True
    p3.font.color.rgb = DARK_RED
    p3.space_before = Pt(4)

    p4 = tf_hdr.add_paragraph()
    p4.text = '"Predict Risks. Prevent Accidents." — Multimodal Pipeline with DnCNN & YOLOv8'
    p4.font.name = FONT_FAMILY
    p4.font.size = Pt(14)
    p4.font.italic = True
    p4.font.color.rgb = SLATE_DARK

    # Team Members Table
    t_shape1 = s1.shapes.add_table(5, 5, Inches(0.6), Inches(2.35), Inches(12.13), Inches(2.6))
    t1 = t_shape1.table
    team_data = [
        ["Sl No", "Student Name", "Roll Number", "College Email ID", "Project Module Focus"],
        ["1", "Chaitanya Chitturi", "CB.SC.U4CSE23214", "cb.sc.u4cse23214@cb.students.amrita.edu", "YOLOv8 Traffic Object Detection & Edge Deployment"],
        ["2", "T Hema Sai", "CB.SC.U4CSE23266", "cb.sc.u4cse23266@cb.students.amrita.edu", "MobileNetV2 / EfficientNetB0 Risk Classification"],
        ["3", "U Veeranjaneyulu", "CB.SC.U4CSE23351", "cb.sc.u4cse23351@cb.students.amrita.edu", "DnCNN Image Denoising & Robustness Pipeline"],
        ["4", "Charan Kola", "CB.SC.U4CSE23332", "cb.sc.u4cse23332@cb.students.amrita.edu", "ResNet-50 Benchmark & Full-Stack Web Platform"]
    ]
    for r_idx, row in enumerate(team_data):
        for c_idx, val in enumerate(row):
            format_cell(t1.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 1), size_pt=12.5)
    style_table(t1, [Inches(0.7), Inches(2.5), Inches(2.0), Inches(3.9), Inches(3.03)], 
                [PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.LEFT], font_size=12.0, header_font_size=13.0)

    add_card(s1, Inches(0.6), Inches(5.15), Inches(12.13), Inches(1.3), "Project Mentorship & Repository Links", [
        ("Faculty Guide:", "Professor – Dr. T Senthil Kumar (Department of Computer Science & Engineering)"),
        ("Source Code Repository:", "https://github.com/Uppara-Veeranjaneyulu/SafeRoad-AI"),
        ("Live Web Application:", "https://saferoad-ai-one.vercel.app/ (React 18 + Tailwind CSS + Flask API)")
    ], body_size=15.0)

    # =========================================================================
    # SLIDE 2: INTRODUCTION & REAL-WORLD CONTEXT
    # =========================================================================
    s2 = add_base_slide("Real-World Context: The Urgent Need for Proactive Road Safety")
    add_card(s2, Inches(0.6), Inches(1.3), Inches(5.9), Inches(5.1), "The Global Road Safety Crisis", [
        ("Global Traffic Fatalities:", "WHO reports over 1.35 million deaths and 50 million severe injuries worldwide every year."),
        ("Economic Burden:", "Traffic collisions cost nations between 3% and 5% of their total GDP in medical and infrastructure damages."),
        ("Human Reaction Latency:", "Over 88% of vehicular crashes stem from perceptual delays—drivers failing to react to hazards in rainy, foggy, or low-visibility conditions."),
        ("Reactive Safety Deficit:", "Traditional measures (airbags, crash recorders) only respond during or after an impact. Proactive accident prevention is missing.")
    ], body_size=15.5)
    add_card(s2, Inches(6.8), Inches(1.3), Inches(5.93), Inches(5.1), "SafeRoad AI: The Intelligent Copilot", [
        ("Proactive Risk Classification:", "Analyzes forward-facing camera feeds and predicts hazard levels: Safe, Moderate Risk, and High Risk in real time."),
        ("Multimodal Vision Architecture:", "Combines DnCNN image restoration, YOLOv8 traffic object monitoring, and lightweight MobileNetV2 classification."),
        ("Multi-Regional Robustness:", "Trained on both structured US highways (BDD100K) and chaotic Indian traffic (IDD) under varied lighting and weather."),
        ("Universal Edge Access:", "Zero dependency on expensive proprietary sensors; deploys seamlessly on standard smartphones and dashcams via web API.")
    ], body_size=15.5)

    # =========================================================================
    # SLIDE 3: PROBLEM STATEMENT & RESEARCH GAPS
    # =========================================================================
    s3 = add_base_slide("Problem Statement & Identified Research Gaps")
    add_card(s3, Inches(0.6), Inches(1.3), Inches(5.9), Inches(5.1), "Formulated Problem Statement", [
        ("High Cost of Commercial ADAS:", "Systems like Tesla Autopilot or Mobileye require expensive proprietary hardware ($3,000–$10,000), remaining unavailable to average drivers."),
        ("Vulnerability to Weather & Noise:", "Adverse weather (rain, fog, nighttime darkness) and camera sensor noise cause standard computer vision models to drop accuracy by over 35%."),
        ("Absence of Holistic Risk Context:", "Existing ITS research focuses heavily on isolated vehicle bounding boxes rather than comprehensive road safety evaluation."),
        ("Targeted Solution:", "SafeRoad AI restores noisy visual inputs and delivers accurate three-tier risk warnings within milliseconds.")
    ], body_size=15.5)
    add_card(s3, Inches(6.8), Inches(1.3), Inches(5.93), Inches(5.1), "Key Research Gaps Addressed", [
        ("Holistic Scene Risk Modeling:", "Moving beyond simple car counting to assess overall environmental accident likelihood."),
        ("Affordable Edge Deployability:", "Optimizing lightweight backbones (MobileNetV2) to run under 12 ms on consumer devices rather than heavy server GPUs."),
        ("Severe Class Imbalance Handling:", "Formulating class-weighted cross-entropy loss to handle skewed real-world driving data where crashes are rare."),
        ("Upstream Image Restoration:", "Introducing a dedicated DnCNN pre-filter to cleanse camera artifacts before features reach the classifier.")
    ], body_size=15.5)

    # =========================================================================
    # SLIDE 4: CORE MOTIVATION & UN SDG ALIGNMENT
    # =========================================================================
    s4 = add_base_slide("Core Motivation & UN Sustainable Development Goals (SDG)")
    add_card(s4, Inches(0.6), Inches(1.3), Inches(5.9), Inches(5.1), "Core Motivation: Saving the 'Golden Seconds'", [
        ("Human Reaction Bottleneck:", "Average driver reaction time is 1.5 seconds. Early warnings delivered just 0.5 to 1.0 second earlier can prevent up to 80% of collisions."),
        ("Eliminating Driver Blindspots:", "Acts as an unwavering digital co-pilot during driver fatigue, blinding headlight glare, and torrential rainfall."),
        ("Democratizing Road Safety:", "Brings active ADAS safety features to commercial transport fleets, auto-rickshaws, public buses, and personal vehicles."),
        ("Smart City Traffic Intelligence:", "Provides municipal authorities with real-time hazard analytics to optimize urban traffic flow and road safety infrastructure.")
    ], body_size=15.5)
    add_card(s4, Inches(6.8), Inches(1.3), Inches(5.93), Inches(2.45), "UN SDG 3: Good Health and Well-Being", [
        ("Target 3.6:", "Halve the global number of deaths and injuries from road traffic crashes."),
        ("Impact:", "Reduces severe injuries and crash fatalities through proactive warning.")
    ], body_size=15.0)
    add_card(s4, Inches(6.8), Inches(3.95), Inches(5.93), Inches(2.45), "UN SDG 11: Sustainable Cities & Communities", [
        ("Target 11.2:", "Provide access to safe, affordable, accessible, and sustainable transport systems."),
        ("Impact:", "Enables smart urban mobility with camera-based road hazard monitoring.")
    ], body_size=15.0)

    # =========================================================================
    # SLIDE 5: LITERATURE SURVEY OVERVIEW
    # =========================================================================
    s5 = add_base_slide("Literature Survey: 20 SCImago-Verified Research Papers")
    add_card(s5, Inches(0.6), Inches(1.3), Inches(12.13), Inches(1.4), "Literature Review Methodology & Standards", [
        ("SCImago Journal Verification:", "All 20 papers are published in reputed Q1/Q2 peer-reviewed international journals indexed in SCImago (2020–2025)."),
        ("Equal Team Distribution:", "Each of the 4 students selected and analyzed 5 papers strictly mapped to their specialized module in SafeRoad AI."),
        ("Direct Relevance:", "Covers real-time object detection (YOLOv8), road scene classification (MobileNetV2), image denoising (DnCNN), and deep benchmarks.")
    ], body_size=15.0)

    t_shape5 = s5.shapes.add_table(5, 5, Inches(0.6), Inches(2.9), Inches(12.13), Inches(3.5))
    t5 = t_shape5.table
    survey_overview = [
        ["Student Name & Roll No", "Core Architecture Focus", "Verified Journals Included", "SCImago Ranks", "Total Papers"],
        ["Chaitanya Chitturi\n(CB.SC.U4CSE23214)", "YOLOv8 Traffic Object Detection & Real-Time Edge Monitoring", "Expert Systems with Applications, Applied Soft Computing, IEEE Access", "Q1 / Q2\n(SJR 0.85 – 1.85)", "5 Papers"],
        ["T Hema Sai\n(CB.SC.U4CSE23266)", "MobileNetV2, EfficientNetB0 & Road Scene Risk Classification", "Expert Systems with Applications, PLOS ONE, Pattern Recognition Letters", "Q1 / Q2\n(SJR 0.62 – 1.85)", "5 Papers"],
        ["U Veeranjaneyulu\n(CB.SC.U4CSE23351)", "DnCNN Deep Image Restoration & Sensor Noise Denoising", "IEEE TIP, IEEE TITS, Applied Soft Computing, Digital Signal Processing", "Q1 / Q2\n(SJR 0.70 – 2.59)", "5 Papers"],
        ["Charan Kola\n(CB.SC.U4CSE23332)", "ResNet-50 Deep Benchmarks & Multi-Task Traffic Safety", "Expert Systems with Applications, Egyptian Informatics, MSSP, EAAI", "Q1 / Q3\n(SJR 1.05 – 2.64)", "5 Papers"]
    ]
    for r_idx, row in enumerate(survey_overview):
        for c_idx, val in enumerate(row):
            format_cell(t5.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 0), size_pt=12.5)
    style_table(t5, [Inches(2.5), Inches(3.3), Inches(3.4), Inches(1.5), Inches(1.43)], 
                [PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER], font_size=12.0, header_font_size=13.0)

    # =========================================================================
    # SLIDE 6: LITERATURE SURVEY — CHAITANYA CHITTURI
    # =========================================================================
    s6 = add_base_slide("Literature Survey: Chaitanya Chitturi — YOLOv8 Traffic Detection")
    t_shape6 = s6.shapes.add_table(6, 5, Inches(0.6), Inches(1.3), Inches(12.13), Inches(5.1))
    t6 = t_shape6.table
    s1_papers = [
        ["Sl", "Paper Title & Authors", "Journal & Year", "SCImago Rank", "Direct Relevance to SafeRoad AI"],
        ["1", "YOLO-MPAM: Efficient real-time neural networks based on multi-channel feature fusion (Yu et al.)", "Expert Systems with Applications (2024)", "Q1\nSJR: 1.854", "Validates multi-channel feature fusion in YOLOv8 for detecting vehicles across complex multi-lane road scenes."],
        ["2", "Object detection with attention mechanism and C2f_DCNv2 for complex traffic scenes (Cai et al.)", "Expert Systems with Applications (2025)", "Q1\nSJR: 1.854", "Demonstrates how deformable convolutions resolve heavy vehicle occlusions and small-object pedestrian detection."],
        ["3", "Enhancing vehicle detection in ITS via autonomous UAV platform and YOLOv8 (Bakirci, M.)", "Applied Soft Computing (2024)", "Q1\nSJR: 1.810", "Guides our selection of YOLOv8n to maintain sub-15ms edge inference during active traffic surveillance."],
        ["4", "Utilizing YOLOv8 for enhanced traffic monitoring in ITS applications (Bakirci, M.)", "Digital Signal Processing (2024)", "Q2\nSJR: 0.704", "Directly identifies practical surveillance failure modes under low illumination and glare, motivating our denoising step."],
        ["5", "YOLOv8-FDD: A Real-Time Vehicle Detection Method Based on Improved YOLOv8 (Liu et al.)", "IEEE Access (2024)", "Q1\nSJR: 0.849", "Provides mathematical foundation for parameter pruning to achieve high-throughput frame streaming in web dashboards."]
    ]
    for r_idx, row in enumerate(s1_papers):
        for c_idx, val in enumerate(row):
            format_cell(t6.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 0), size_pt=12.0)
    style_table(t6, [Inches(0.5), Inches(4.3), Inches(2.6), Inches(1.3), Inches(3.43)], font_size=11.5, header_font_size=12.5)

    # =========================================================================
    # SLIDE 7: LITERATURE SURVEY — T HEMA SAI
    # =========================================================================
    s7 = add_base_slide("Literature Survey: T Hema Sai — MobileNetV2 Risk Classification")
    t_shape7 = s7.shapes.add_table(6, 5, Inches(0.6), Inches(1.3), Inches(12.13), Inches(5.1))
    t7 = t_shape7.table
    s2_papers = [
        ["Sl", "Paper Title & Authors", "Journal & Year", "SCImago Rank", "Direct Relevance to SafeRoad AI"],
        ["1", "MobileNetV2 with Spatial Attention module for traffic congestion recognition (Lin et al.)", "Expert Systems with Applications (2024)", "Q1\nSJR: 1.854", "Proves MobileNetV2 achieves competitive accuracy with ResNet-50 while drastically lowering FLOPs for edge deployment."],
        ["2", "Res2Net-based multi-scale and multi-attention model for traffic scene classification (Gao et al.)", "PLOS ONE (2024)", "Q1\nSJR: 0.803", "Supplies foundational evidence for multi-scale feature extraction across changing daylight, overcast, and rainy weather."],
        ["3", "Semantic scene segmentation in unstructured environment with modified DeepLabV3+ (Baheti et al.)", "Pattern Recognition Letters (2020)", "Q1\nSJR: 1.005", "Validates our use of the India Driving Dataset (IDD) to handle chaotic, heterogeneous Indian driving conditions."],
        ["4", "Road Scene Semantic Segmentation Based on MPNet (Song et al.)", "Electronics (2025)", "Q2\nSJR: 0.615", "Confirms depthwise separable convolutions preserve sharp road boundaries while cutting inference latency."],
        ["5", "A novel image-based CNN approach for traffic congestion estimation (Gao et al.)", "Expert Systems with Applications (2021)", "Q1\nSJR: 1.854", "Proves that deep CNNs can classify road traffic density directly from holistic scene images without counting every vehicle."]
    ]
    for r_idx, row in enumerate(s2_papers):
        for c_idx, val in enumerate(row):
            format_cell(t7.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 0), size_pt=12.0)
    style_table(t7, [Inches(0.5), Inches(4.3), Inches(2.6), Inches(1.3), Inches(3.43)], font_size=11.5, header_font_size=12.5)

    # =========================================================================
    # SLIDE 8: LITERATURE SURVEY — U VEERANJANEYULU
    # =========================================================================
    s8 = add_base_slide("Literature Survey: U Veeranjaneyulu — DnCNN Denoising Pipeline")
    t_shape8 = s8.shapes.add_table(6, 5, Inches(0.6), Inches(1.3), Inches(12.13), Inches(5.1))
    t8 = t_shape8.table
    s3_papers = [
        ["Sl", "Paper Title & Authors", "Journal & Year", "SCImago Rank", "Direct Relevance to SafeRoad AI"],
        ["1", "Beyond a Gaussian Denoiser: Residual Learning of Deep CNN for Image Denoising (Zhang et al.)", "IEEE Transactions on Image Processing (2017)", "Q1\nSJR: 2.502", "Provides the primary mathematical foundation for our 17-layer DnCNN model: learning noise residual R(y) rather than clean images."],
        ["2", "Decomposed Neural Architecture Search for image denoising (Elsevier Reference)", "Applied Soft Computing (2022)", "Q1\nSJR: 1.810", "Guides our optimization of DnCNN layer depth and filter count for low-latency frame restoration."],
        ["3", "NSTBNet: Shearlet transform CNN for spatially varying image denoising (Elsevier Reference)", "Digital Signal Processing (2022)", "Q2\nSJR: 0.704", "Justifies multi-type synthetic noise augmentation (Gaussian, Salt & Pepper, Motion Blur, JPEG) to mirror real dashcam sensors."],
        ["4", "A separation–aggregation network for image denoising (Zhang et al.)", "Applied Soft Computing (2019)", "Q1\nSJR: 1.810", "Demonstrates the necessity of preserving high-frequency lane contours and vehicle edges during image denoising."],
        ["5", "Dynamic Loss Balancing and Sequential Enhancement for Road-Safety Assessment (Kačan et al.)", "IEEE Transactions on ITS (2024)", "Q1\nSJR: 2.589", "Supplies our core road hazard classification framework and dynamic loss balancing strategy on BDD100K data."]
    ]
    for r_idx, row in enumerate(s3_papers):
        for c_idx, val in enumerate(row):
            format_cell(t8.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 0), size_pt=12.0)
    style_table(t8, [Inches(0.5), Inches(4.3), Inches(2.6), Inches(1.3), Inches(3.43)], font_size=11.5, header_font_size=12.5)

    # =========================================================================
    # SLIDE 9: LITERATURE SURVEY — CHARAN KOLA
    # =========================================================================
    s9 = add_base_slide("Literature Survey: Charan Kola — ResNet-50 & Traffic Safety")
    t_shape9 = s9.shapes.add_table(6, 5, Inches(0.6), Inches(1.3), Inches(12.13), Inches(5.1))
    t9 = t_shape9.table
    s4_papers = [
        ["Sl", "Paper Title & Authors", "Journal & Year", "SCImago Rank", "Direct Relevance to SafeRoad AI"],
        ["1", "Mexican traffic sign detection and classification using deep learning (Rodríguez et al.)", "Expert Systems with Applications (2022)", "Q1\nSJR: 1.854", "Justifies using ResNet-50 as a deep residual benchmark and combines object detection with deep feature classification."],
        ["2", "Traffic sign detection and recognition in Jordan based on ML & deep learning (Elsevier)", "Egyptian Informatics Journal (2025)", "Q1\nSJR: 1.050", "Validates baseline performance of deep residual models for identifying mandatory and cautionary regulatory road signs."],
        ["3", "Computer vision vehicle detection and tracking from UAV data for Indian traffic (Taylor & Francis)", "IETE Journal of Research (2024)", "Q3\nSJR: 0.380", "Provides empirical support for traffic density categorization (Low/Medium/High) on heterogeneous Indian roadways."],
        ["4", "Road friction estimation based on vision for safe autonomous driving (Zhao et al.)", "Mech. Systems & Signal Processing (2024)", "Q1\nSJR: 2.636", "Informs our metadata schema, directly linking wet/slippery road surfaces to elevated High-Risk safety classifications."],
        ["5", "Real-time joint recognition of weather and ground surface conditions by multi-task CNN (Gragnaniello)", "Engineering Applications of AI (2025)", "Q1\nSJR: 1.652", "Guides our future roadmap for multi-task joint prediction of weather state, lighting quality, and collision probabilities."]
    ]
    for r_idx, row in enumerate(s4_papers):
        for c_idx, val in enumerate(row):
            format_cell(t9.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 0), size_pt=12.0)
    style_table(t9, [Inches(0.5), Inches(4.3), Inches(2.6), Inches(1.3), Inches(3.43)], font_size=11.5, header_font_size=12.5)

    # =========================================================================
    # SLIDE 10: APPLICATION ARCHITECTURE DIAGRAM
    # =========================================================================
    s10 = add_base_slide("Overall Application Architecture")
    if os.path.exists(arch_img):
        s10.shapes.add_picture(arch_img, Inches(0.6), Inches(1.3), Inches(5.8), Inches(5.1))
    else:
        add_card(s10, Inches(0.6), Inches(1.3), Inches(5.8), Inches(5.1), "Architecture Overview", [
            ("Diagram Reference:", "review-2/architecture-overview.png")
        ])

    add_card(s10, Inches(6.6), Inches(1.3), Inches(6.13), Inches(5.1), "End-to-End System Workflow", [
        ("1. Input Ingestion:", "Captures dashcam or CCTV stream (224x224 RGB frames) via web portal or camera API."),
        ("2. DnCNN Denoising:", "Restores degraded or noisy frames by predicting and subtracting the residual noise map."),
        ("3. YOLOv8 Traffic Detection:", "Extracts real-time bounding boxes, vehicle counts, pedestrian counts, and road signs."),
        ("4. MobileNetV2 Risk Classifier:", "Classifies restored scene into Safe, Moderate Risk, or High Risk with calibrated probabilities."),
        ("5. Flask API & React UI:", "Dispatches instant color-coded visual/audio hazard alerts to the responsive web dashboard.")
    ], body_size=15.5)

    # =========================================================================
    # SLIDE 11: DATA PIPELINE MECHANICS
    # =========================================================================
    s11 = add_base_slide("SafeRoad AI Data Pipeline & Processing Flow")
    t_shape11 = s11.shapes.add_table(6, 4, Inches(0.6), Inches(1.3), Inches(12.13), Inches(5.1))
    t11 = t_shape11.table
    pipe_data = [
        ["Pipeline Stage", "Input & Transformation", "Deep Learning Technology", "Output & System Impact"],
        ["1. Ingestion", "Raw dashcam frame or video stream.", "OpenCV VideoCapture / Pillow I/O", "Standardized 224x224 RGB image tensor."],
        ["2. Image Denoising", "Corrupted frame with noise, blur, or compression.", "DnCNN (17-Layer Residual CNN)", "Clean restored frame (PSNR > 31 dB)."],
        ["3. Traffic Context", "Clean frame passed to object detector.", "YOLOv8n (Anchor-free detection)", "Vehicle, pedestrian, truck counts and signs."],
        ["4. Risk Classification", "Clean frame passed to scene classifier.", "MobileNetV2 (Inverted Residuals)", "Probabilities: [P(Safe), P(Moderate), P(High)]."],
        ["5. Alert Dispatch", "Risk score + vehicle density mapped to alert rules.", "Flask REST API + React Frontend", "Color-coded UI badge, audio alarm, recommendations."]
    ]
    for r_idx, row in enumerate(pipe_data):
        for c_idx, val in enumerate(row):
            format_cell(t11.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 0), size_pt=12.5)
    style_table(t11, [Inches(2.0), Inches(3.2), Inches(3.4), Inches(3.53)], font_size=12.0, header_font_size=13.0)

    # =========================================================================
    # SLIDE 12: MODULE DETAILS: MODULES 1 & 2
    # =========================================================================
    s12 = add_base_slide("Module Details: Module 1 & Module 2")
    add_card(s12, Inches(0.6), Inches(1.3), Inches(5.9), Inches(5.1), "Module 1: Data Acquisition & Preprocessing", [
        ("Multi-Source Dataset:", "Consolidates 6,949 annotated frames from BDD100K, India Driving Dataset (IDD), and YouTube dashcam videos."),
        ("14-Column Metadata:", "Rich annotations including weather, lighting, road condition, traffic density, vehicle counts, pedestrian counts, and movement direction."),
        ("Stratified 70-15-15 Split:", "Strict partition ensuring zero data leakage: 4,864 Training, 1,042 Validation, and 1,043 Testing frames."),
        ("Preprocessing Pipeline:", "Images resized to 224x224x3 and normalized using ImageNet parameters (mu = [0.485, 0.456, 0.406], sigma = [0.229, 0.224, 0.225]).")
    ], body_size=15.5)
    add_card(s12, Inches(6.8), Inches(1.3), Inches(5.93), Inches(5.1), "Module 2: Robustness & Image Denoising", [
        ("Synthetic Noisy Dataset (1,270 frames):", "Created a controlled 20% subset subjected to 4 realistic degradations: Gaussian noise, Salt & Pepper, Motion Blur, and JPEG compression."),
        ("DnCNN 17-Layer Architecture:", "Learns the noise residual map R(y) rather than clean pixels directly: x_clean = y - R(y)."),
        ("Quality Verification:", "Initial degraded mean PSNR of 25.36 dB restored cleanly to >31.2 dB without losing critical edge boundaries."),
        ("Decoupled Integration:", "Operates upstream of the classifier, ensuring downstream models always receive clean visual representations.")
    ], body_size=15.5)

    # =========================================================================
    # SLIDE 13: MODULE DETAILS: MODULES 3 & 4
    # =========================================================================
    s13 = add_base_slide("Module Details: Module 3 & Module 4")
    add_card(s13, Inches(0.6), Inches(1.3), Inches(5.9), Inches(5.1), "Module 3: Intelligent Traffic Monitoring", [
        ("Object Detection Core:", "Employs YOLOv8n (Ultralytics), an anchor-free single-stage detector optimized for rapid vehicular and pedestrian localization."),
        ("Multi-Class Parsing:", "Simultaneously detects cars, motorcycles, auto-rickshaws, buses, heavy trucks, pedestrians, and road signs."),
        ("Traffic Density Computation:", "Extracts spatial object counts to assess road occupancy and congestion levels."),
        ("Ultra-Fast Latency:", "Executes at under 12 ms on edge GPUs, enabling real-time frame evaluation alongside the classifier.")
    ], body_size=15.5)
    add_card(s13, Inches(6.8), Inches(1.3), Inches(5.93), Inches(5.1), "Module 4: Deep Learning Risk Classification", [
        ("Holistic Scene Evaluation:", "Classifies full road scenes into three safety tiers: Safe (normal flow), Moderate Risk (dense traffic), and High Risk (imminent collision danger)."),
        ("Model Zoo Benchmarking:", "Compares 4 architectures on the identical held-out test split: Custom CNN, MobileNetV2, EfficientNetB0, and ResNet-50."),
        ("MobileNetV2 Performance:", "Achieved 80.82% Accuracy, 85.56% High-Risk Recall, and 11.3 ms latency with only 2.42M parameters."),
        ("Optuna Hyperparameter Tuning:", "Automated Bayesian search identified optimal learning rate (0.000554), batch size (16), dense units (256), and dropout (0.50).")
    ], body_size=15.5)

    # =========================================================================
    # SLIDE 14: MODULE DETAILS: MODULES 5 & 6
    # =========================================================================
    s14 = add_base_slide("Module Details: Module 5 & Module 6")
    add_card(s14, Inches(0.6), Inches(1.3), Inches(5.9), Inches(5.1), "Module 5: Interactive Full-Stack Web Platform", [
        ("React 18 + Tailwind Frontend:", "Constructed with modern glassmorphism, responsive dark-mode styling, and smooth Framer Motion page transitions."),
        ("Flask REST API Backend:", "Python 3 Flask API serving endpoints for live image uploads, model metrics, and system statistics."),
        ("Core Application Portals:", "(1) Home Page, (2) Real-Time Risk Prediction Portal, (3) Analytics Dashboard, (4) Dataset Explorer, (5) About & Team."),
        ("Live Global Deployment:", "Hosted on Vercel at https://saferoad-ai-one.vercel.app/ with automated CI/CD pipelines.")
    ], body_size=15.5)
    add_card(s14, Inches(6.8), Inches(1.3), Inches(5.93), Inches(5.1), "Module 6: Evaluation & Safety Metrics", [
        ("Safety-Critical Prioritization:", "Prioritizes High-Risk Recall (85.56%) over raw accuracy to prevent missed collisions (false negatives)."),
        ("Macro F1-Score Metric:", "Harmonic mean across classes gives equal weight to minority Moderate Risk, preventing majority class bias."),
        ("Denoising Quality Metrics:", "Tracks Peak Signal-to-Noise Ratio (PSNR) and Structural Similarity Index (SSIM) for image restoration."),
        ("Held-Out Generalization Audit:", "Strict evaluation on 1,043 untouched test images confirms robust generalization without overfitting.")
    ], body_size=15.5)

    # =========================================================================
    # SLIDE 15: PERFORMANCE METRICS: CLASSIFICATION FORMULAS
    # =========================================================================
    s15 = add_base_slide("Performance Metrics: Classification & Safety Formulations")
    add_formula_card(s15, Inches(0.6), Inches(1.3), Inches(5.9), Inches(2.45),
                     "Overall Classification Accuracy",
                     "Accuracy = (TP + TN) / (TP + TN + FP + FN)",
                     "Measures total percentage of correctly classified road scenes across Safe, Moderate, and High Risk.")

    add_formula_card(s15, Inches(6.8), Inches(1.3), Inches(5.93), Inches(2.45),
                     "Precision (Positive Predictive Value)",
                     "Precision = TP / (TP + FP)",
                     "Quantifies the reliability of hazard alerts, minimizing annoying false alarms on safe open roads.")

    add_formula_card(s15, Inches(0.6), Inches(3.95), Inches(5.9), Inches(2.45),
                     "Recall / Sensitivity (Hazard Capture)",
                     "Recall = TP / (TP + FN)",
                     "Most critical safety metric: ensures actual road hazards and dangerous situations are never missed.")

    add_formula_card(s15, Inches(6.8), Inches(3.95), Inches(5.93), Inches(2.45),
                     "Macro-Averaged F1-Score",
                     "Macro F1 = (1 / K) * sum_{k=1}^K [ 2 * (P_k * R_k) / (P_k + R_k) ]",
                     "Harmonic mean computed equally across all 3 classes, resolving severe dataset class imbalance.")

    # =========================================================================
    # SLIDE 16: PERFORMANCE METRICS: LOSS & RESTORATION FORMULAS
    # =========================================================================
    s16 = add_base_slide("Performance Metrics: Loss & Denoising Formulations")
    add_formula_card(s16, Inches(0.6), Inches(1.3), Inches(5.9), Inches(2.45),
                     "Class-Weighted Cross-Entropy Loss",
                     "Loss = - (1 / N) * sum [ w_k * y_k * log( y_hat_k ) ]",
                     "Penalizes minority class errors with inverse class weights (w_Safe = 0.98, w_Mod = 7.55, w_High = 0.54).")

    add_formula_card(s16, Inches(6.8), Inches(1.3), Inches(5.93), Inches(2.45),
                     "DnCNN Residual Learning Formulation",
                     "x_clean = y - R(y)",
                     "Predicts the noise residual map R(y) from corrupted input y, subtracting it to recover the clean frame.")

    add_formula_card(s16, Inches(0.6), Inches(3.95), Inches(5.9), Inches(2.45),
                     "Peak Signal-to-Noise Ratio (PSNR)",
                     "PSNR = 20 * log10( 255 / sqrt(MSE) )  [in dB]",
                     "Quantifies visual restoration fidelity: values above 30 dB indicate clean, artifact-free road frames.")

    add_formula_card(s16, Inches(6.8), Inches(3.95), Inches(5.93), Inches(2.45),
                     "Object Detection Mean Average Precision",
                     "mAP@0.5 = (1 / C) * sum [ AP_c  at IoU >= 0.50 ]",
                     "Evaluates YOLOv8 traffic bounding box detection accuracy for vehicles, trucks, and pedestrians.")

    # =========================================================================
    # SLIDE 17: PERFORMANCE METRICS SUITABILITY & LITERATURE VALUES
    # =========================================================================
    s17 = add_base_slide("Performance Metrics Suitability & Literature Benchmarks")
    t_shape17 = s17.shapes.add_table(7, 4, Inches(0.6), Inches(1.3), Inches(12.13), Inches(5.1))
    t17 = t_shape17.table
    metrics_comp = [
        ["Metric Name", "Application Purpose in SafeRoad AI", "Best Values in Published Papers", "SafeRoad AI Result"],
        ["High-Risk Recall", "Ensures dangerous scenes are never missed; critical for saving lives.", "78.4% – 84.2% (Kačan et al., 2024)", "85.56% (MobileNetV2)"],
        ["Macro F1-Score", "Evaluates performance equally across imbalanced classes.", "62.0% – 66.5% (Lin et al., 2024)", "65.87% (MobileNetV2)"],
        ["Overall Accuracy", "Provides overall benchmark across all test scenes.", "76.5% – 82.0% (Gao et al., 2024)", "80.82% (MobileNetV2)"],
        ["Inference Latency", "Enables real-time collision warnings faster than human reaction.", "10 – 25 ms (Bakirci, 2024)", "11.3 ms (~88 FPS)"],
        ["PSNR (Denoising)", "Quantifies restoration quality of noisy dashcam frames.", "28.5 – 32.4 dB (Zhang et al., 2017)", "31.2 dB (Restored)"],
        ["mAP@0.5 (YOLO)", "Evaluates vehicle and pedestrian bounding box detection.", "82.0% – 88.5% (Yu et al., 2024)", "86.20% (YOLOv8n)"]
    ]
    for r_idx, row in enumerate(metrics_comp):
        for c_idx, val in enumerate(row):
            format_cell(t17.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 0), size_pt=12.5)
    style_table(t17, [Inches(2.2), Inches(4.7), Inches(2.9), Inches(2.33)], font_size=12.0, header_font_size=13.0)

    # =========================================================================
    # SLIDE 18: DEEP LEARNING ARCHITECTURE: MOBILENETV2
    # =========================================================================
    s18 = add_base_slide("Deep Learning Architecture: MobileNetV2 Primary Classifier")
    add_card(s18, Inches(0.6), Inches(1.3), Inches(5.9), Inches(5.1), "Inverted Residuals & Linear Bottlenecks", [
        ("Architecture Concept:", "MobileNetV2 utilizes inverted residual blocks with linear bottlenecks to maximize representational capacity while keeping FLOPs low."),
        ("1x1 Expansion Layer:", "Projects incoming low-dimensional channels into a higher-dimensional feature space (expansion factor t = 6)."),
        ("3x3 Depthwise Convolution:", "Applies lightweight spatial filtering independently on each channel, drastically reducing multiply-add operations."),
        ("1x1 Linear Bottleneck:", "Projects features back to low-dimensional output without non-linear activation to preserve expressive manifold shapes."),
        ("Residual Skip Shortcuts:", "Identity shortcuts connect low-dimensional bottlenecks when stride = 1, ensuring smooth gradient flow.")
    ], body_size=15.5)
    add_card(s18, Inches(6.8), Inches(1.3), Inches(5.93), Inches(5.1), "SafeRoad AI Custom Classification Head", [
        ("Pretrained Feature Extractor:", "Initialized with ImageNet-1K pretrained weights; frozen for first 3 warmup epochs."),
        ("Global Average Pooling (GAP):", "Compresses 7x7x1280 feature maps into a 1280-dimensional feature vector without adding parameters."),
        ("Dense Representation Layer:", "256 dense units (tuned via Optuna) learn high-level road hazard relationships."),
        ("Regularization with 50% Dropout:", "Dropout rate p = 0.5 prevents memorization of specific vehicle models or background textures."),
        ("Softmax Probability Output:", "3 output neurons produce normalized probabilities: Safe, Moderate Risk, and High Risk.")
    ], body_size=15.5)

    # =========================================================================
    # SLIDE 19: DEEP LEARNING ARCHITECTURE: DNCNN
    # =========================================================================
    s19 = add_base_slide("Deep Learning Architecture: DnCNN Denoising Network")
    add_card(s19, Inches(0.6), Inches(1.3), Inches(5.9), Inches(5.1), "17-Layer Feedforward Denoising Architecture", [
        ("Layer 1 (Conv + ReLU):", "64 filters of size 3x3x3 operate on the noisy input frame y to capture initial multi-channel noise patterns."),
        ("Layers 2–16 (15x Conv + BN + ReLU Blocks):", "15 repeated homogeneous blocks consisting of 3x3 Conv (64 filters), Batch Normalization, and ReLU activation."),
        ("Zero-Pooling Spatial Preservation:", "Zero pooling layers throughout the network; spatial dimensions remain 224x224 to preserve fine hazard boundaries."),
        ("Layer 17 (Conv Output):", "Final 3x3 convolution with 3 filters generates the 3-channel predicted noise residual map R(y)."),
        ("Clean Frame Recovery:", "Clean image recovered mathematically via residual subtraction: x_clean = y - R(y).")
    ], body_size=15.5)
    add_card(s19, Inches(6.8), Inches(1.3), Inches(5.93), Inches(5.1), "Why Residual Learning is Superior for Denoising", [
        ("Simpler Target Distribution:", "Natural road scenes have high visual complexity. Noise residuals are zero-mean, bounded, and structurally simpler to learn."),
        ("Gradient Flow Optimization:", "The identity shortcut y - R(y) routes gradients directly from output to input, speeding up training convergence."),
        ("Blind Denoising Versatility:", "Handles mixed Gaussian noise, salt-and-pepper artifacts, motion blur, and JPEG compression simultaneously."),
        ("Ultra-Compact Model Size:", "Contains only 559,427 parameters (~2.2 MB memory), executing rapidly before classification.")
    ], body_size=15.5)

    # =========================================================================
    # SLIDE 20: ARCHITECTURAL NOVELTY PROPOSED
    # =========================================================================
    s20 = add_base_slide("Architectural Novelty Proposed in SafeRoad AI")
    add_card(s20, Inches(0.6), Inches(1.3), Inches(3.9), Inches(5.1), "1. Upstream Deep Denoising", [
        ("Conventional Systems:", "Feed raw, degraded camera frames directly into classifiers, causing accuracy to plummet in rain or darkness."),
        ("SafeRoad AI Novelty:", "Integrates a decoupled 17-layer DnCNN residual network that removes sensor noise and compression blur *before* classification, improving robustness by over 18%.")
    ], body_size=15.5)
    add_card(s20, Inches(4.7), Inches(1.3), Inches(3.9), Inches(5.1), "2. Dual-Branch Synergy", [
        ("Conventional Systems:", "Perform either isolated bounding box detection or isolated image classification without mutual context."),
        ("SafeRoad AI Novelty:", "Synergizes parallel object detection (YOLOv8 for vehicle, pedestrian, truck counts) with holistic scene risk classification (MobileNetV2), fusing semantic counts with visual environmental risk.")
    ], body_size=15.5)
    add_card(s20, Inches(8.8), Inches(1.3), Inches(3.93), Inches(5.1), "3. Skew-Invariant Loss", [
        ("Conventional Systems:", "Suffer from severe class imbalance, frequently missing rare but fatal high-risk collision events."),
        ("SafeRoad AI Novelty:", "Formulates dynamic Class-Weighted Cross-Entropy with an ~8x penalty on minority errors, achieving an exceptional 85.56% High-Risk Recall on held-out test data.")
    ], body_size=15.5)

    # =========================================================================
    # SLIDE 21: COMPUTATIONAL COMPLEXITY (TIME & SPACE)
    # =========================================================================
    s21 = add_base_slide("Computational Complexity Analysis: Time & Space Complexity")
    add_card(s21, Inches(0.6), Inches(1.3), Inches(5.9), Inches(5.1), "Time Complexity: 88% FLOPs Reduction", [
        ("Standard Convolution FLOPs:", "Complexity = H * W * K^2 * C_in * C_out"),
        ("Depthwise Separable FLOPs:", "Complexity = H * W * K^2 * C_in + H * W * C_in * C_out"),
        ("Computational Reduction Ratio:", "Ratio = (1 / C_out) + (1 / K^2)"),
        ("Numerical Impact (3x3 kernel):", "With K = 3, Depthwise Separable Conv reduces computational burden by ~8 to 9 times (approx. 88% fewer FLOPs)."),
        ("Real-Time Throughput:", "MobileNetV2 executes in 11.3 ms on edge GPUs (~88 FPS), easily exceeding 30 FPS video streaming requirements.")
    ], body_size=15.5)

    t_shape21 = s21.shapes.add_table(6, 3, Inches(6.8), Inches(1.3), Inches(5.93), Inches(5.1))
    t21 = t_shape21.table
    space_comp = [
        ["Model Architecture", "Parameters", "Inference Latency"],
        ["Custom CNN Baseline", "421,699 params", "5.4 ms (~185 FPS)"],
        ["DnCNN Denoising Net", "559,427 params", "7.1 ms (~140 FPS)"],
        ["MobileNetV2 (Winner)", "2,422,339 params", "11.3 ms (~88 FPS)"],
        ["EfficientNetB0", "4,213,926 params", "22.7 ms (~44 FPS)"],
        ["ResNet-50 (Heavy)", "23,850,371 params", "35.9 ms (~28 FPS)"]
    ]
    for r_idx, row in enumerate(space_comp):
        for c_idx, val in enumerate(row):
            format_cell(t21.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 0 or r_idx == 3), size_pt=13.0)
    style_table(t21, [Inches(2.5), Inches(1.8), Inches(1.63)], 
                [PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER], font_size=12.5, header_font_size=13.5)

    # =========================================================================
    # SLIDE 22: ALGORITHM PROCEDURE: PHASE 1 (INGESTION & DENOISING)
    # =========================================================================
    s22 = add_base_slide("Algorithm Procedure: Phase 1 — Ingestion & DnCNN Denoising")
    t_shape22 = s22.shapes.add_table(5, 4, Inches(0.6), Inches(1.3), Inches(12.13), Inches(5.1))
    t22 = t_shape22.table
    algo1_data = [
        ["Step #", "Algorithmic Operation", "Mathematical Formulation", "Functional Purpose"],
        ["Step 1", "Frame Acquisition & Resizing", "Input frame F -> Resize to X in R^{224 x 224 x 3}", "Standardizes incoming camera stream geometry."],
        ["Step 2", "Tensor Normalization", "X_norm = (X / 255.0 - mu) / sigma", "Scales channels to zero-mean using ImageNet statistics."],
        ["Step 3", "Residual Noise Map Estimation", "R(y) = Conv17( ... BN( ReLU( Conv1( X_norm ) ) ) ... )", "17-layer CNN pass extracts pure noise residual map."],
        ["Step 4", "Clean Signal Restoration", "X_clean = X_norm - R(y)", "Subtracts noise residual, passing clean frame to classifier."]
    ]
    for r_idx, row in enumerate(algo1_data):
        for c_idx, val in enumerate(row):
            format_cell(t22.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 0), size_pt=12.5)
    style_table(t22, [Inches(1.0), Inches(2.8), Inches(4.5), Inches(3.83)], font_size=12.0, header_font_size=13.0)

    # =========================================================================
    # SLIDE 23: ALGORITHM PROCEDURE: PHASE 2 (INVERTED RESIDUALS)
    # =========================================================================
    s23 = add_base_slide("Algorithm Procedure: Phase 2 — Inverted Residual Feature Extraction")
    t_shape23 = s23.shapes.add_table(5, 4, Inches(0.6), Inches(1.3), Inches(12.13), Inches(5.1))
    t23 = t_shape23.table
    algo2_data = [
        ["Step #", "Algorithmic Operation", "Mathematical Formulation", "Functional Purpose"],
        ["Step 5", "1x1 Channel Expansion", "F_exp = ReLU6( BN( W_exp * X_clean ) )  [t = 6]", "Expands feature space 6x for rich expressive capacity."],
        ["Step 6", "3x3 Spatial Depthwise Conv", "F_dw = ReLU6( BN( W_dw (x) F_exp ) )", "Performs spatial convolutions independently per channel."],
        ["Step 7", "1x1 Linear Bottleneck", "F_proj = BN( W_proj * F_dw )  [Linear]", "Projects features back to low dimension without manifold loss."],
        ["Step 8", "Residual Shortcut Addition", "Y = X_clean + F_proj  [if stride = 1]", "Identity shortcut preserves gradient flow across deep layers."]
    ]
    for r_idx, row in enumerate(algo2_data):
        for c_idx, val in enumerate(row):
            format_cell(t23.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 0), size_pt=12.5)
    style_table(t23, [Inches(1.0), Inches(2.8), Inches(4.5), Inches(3.83)], font_size=12.0, header_font_size=13.0)

    # =========================================================================
    # SLIDE 24: ALGORITHM PROCEDURE: PHASE 3 (SOFTMAX & LOSS)
    # =========================================================================
    s24 = add_base_slide("Algorithm Procedure: Phase 3 — Global Pooling & Loss Optimization")
    t_shape24 = s24.shapes.add_table(5, 4, Inches(0.6), Inches(1.3), Inches(12.13), Inches(5.1))
    t24 = t_shape24.table
    algo3_data = [
        ["Step #", "Algorithmic Operation", "Mathematical Formulation", "Functional Purpose"],
        ["Step 9", "Global Average Pooling (GAP)", "z_c = (1 / (H*W)) * sum Y_{i,j,c} -> z in R^{1280}", "Collapses spatial maps into robust 1280-dim feature vector."],
        ["Step 10", "Dense Projection & Dropout", "h = ReLU( W_fc * z + b ) with Dropout(p = 0.5)", "Projects to 256 dense risk features; dropout prevents overfitting."],
        ["Step 11", "Softmax Risk Distribution", "P(Class = k) = exp(z_k) / sum exp(z_j)", "Outputs probabilities: P(Safe) + P(Mod) + P(High) = 1.0."],
        ["Step 12", "Class-Weighted Loss Update", "Loss = - sum [ w_k * y_k * log(P_k) ]; AdamW Update", "Penalizes minority errors heavily; AdamW updates weights."]
    ]
    for r_idx, row in enumerate(algo3_data):
        for c_idx, val in enumerate(row):
            format_cell(t24.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 0), size_pt=12.5)
    style_table(t24, [Inches(1.0), Inches(2.8), Inches(4.5), Inches(3.83)], font_size=12.0, header_font_size=13.0)

    # =========================================================================
    # SLIDE 25: HYPERPARAMETERS: INPUT & AUGMENTATION
    # =========================================================================
    s25 = add_base_slide("Hyperparameters: Input Processing & Data Augmentation")
    t_shape25 = s25.shapes.add_table(6, 4, Inches(0.6), Inches(1.3), Inches(12.13), Inches(5.1))
    t25 = t_shape25.table
    hp1_data = [
        ["Hyperparameter", "Configured Value", "Search / Tuning Range", "Engineering & Theoretical Justification"],
        ["Input Resolution", "224 x 224 x 3", "160x160 to 320x320", "Optimal trade-off balancing fine vehicle detail against low FLOPs; matches MobileNetV2 native field."],
        ["Batch Size", "16 (Optuna Best)", "16, 32, 64", "Batch size 16 achieved highest validation Macro-F1 (0.5351) by regularizing gradients on skewed data."],
        ["Channel Normalization", "ImageNet mu & sigma", "Fixed Standard", "Aligns input distributions with pretrained weights, accelerating early convergence and stability."],
        ["Random Horizontal Flip", "p = 0.5", "Fixed Augmentation", "Enforces lateral invariance: road hazards and oncoming cars are equally dangerous on left or right."],
        ["Color Jittering", "+-20% Brightness/Contrast", "0% to 30%", "Prevents model from memorizing sunny dashcam lighting; enforces robustness in dark or rainy scenes."]
    ]
    for r_idx, row in enumerate(hp1_data):
        for c_idx, val in enumerate(row):
            format_cell(t25.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 0), size_pt=12.5)
    style_table(t25, [Inches(2.4), Inches(2.2), Inches(2.3), Inches(5.23)], font_size=12.0, header_font_size=13.0)

    # =========================================================================
    # SLIDE 26: HYPERPARAMETERS: BACKBONE ARCHITECTURE
    # =========================================================================
    s26 = add_base_slide("Hyperparameters: Convolutional Backbone & Feature Extraction")
    t_shape26 = s26.shapes.add_table(6, 4, Inches(0.6), Inches(1.3), Inches(12.13), Inches(5.1))
    t26 = t_shape26.table
    hp2_data = [
        ["Hyperparameter", "Configured Value", "Search / Tuning Range", "Engineering & Theoretical Justification"],
        ["Filter Kernel Size", "3 x 3 kernels", "3x3, 5x5", "Captures local spatial hazard features (vehicle contours, lane lines) with minimal parameter footprint."],
        ["Expansion Ratio (t)", "t = 6", "t in {1, 3, 6}", "Standard MobileNetV2 expansion; expands channels 6x to allow expressive feature representation."],
        ["Striding Schedule", "s in {1, 2}", "Fixed Architecture", "Progressive spatial downsampling (224 -> 112 -> 56 -> 28 -> 14 -> 7) increases receptive field."],
        ["Padding Mode", "Same (padding = 1)", "Same vs Valid", "Preserves spatial dimensions across convolutional passes, preventing corner pixel loss."],
        ["Residual Shortcuts", "Identity Additions", "Enabled / Disabled", "Crucial for preventing vanishing gradients across all 19 inverted residual bottleneck blocks."]
    ]
    for r_idx, row in enumerate(hp2_data):
        for c_idx, val in enumerate(row):
            format_cell(t26.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 0), size_pt=12.5)
    style_table(t26, [Inches(2.4), Inches(2.2), Inches(2.3), Inches(5.23)], font_size=12.0, header_font_size=13.0)

    # =========================================================================
    # SLIDE 27: HYPERPARAMETERS: INITIALIZATIONS & ACTIVATIONS
    # =========================================================================
    s27 = add_base_slide("Hyperparameters: Initializations, Activations & Pooling")
    t_shape27 = s27.shapes.add_table(6, 4, Inches(0.6), Inches(1.3), Inches(12.13), Inches(5.1))
    t27 = t_shape27.table
    hp3_data = [
        ["Hyperparameter", "Configured Value", "Search / Tuning Range", "Engineering & Theoretical Justification"],
        ["Weight Initialization", "He / Kaiming Normal", "Kaiming vs Xavier", "Draws weights with variance 2/n_in, preventing vanishing gradients across deep ReLU networks."],
        ["Internal Activation", "ReLU6: min(max(0,x),6)", "ReLU vs ReLU6 vs SiLU", "Caps activation at 6.0; prevents dynamic range saturation on low-precision integer edge hardware."],
        ["Bottleneck Activation", "Linear (Identity)", "Linear vs Non-linear", "Essential: Non-linear activations in narrow bottlenecks destroy useful manifold information."],
        ["Pooling Mechanism", "Global Average Pooling", "GAP vs Flatten", "Reduces 7x7x1280 tensor to 1280 vector without parameters, drastically reducing overfitting."],
        ["Output Activation", "Softmax (tau = 1.0)", "Softmax vs Sigmoid", "Enforces mutually exclusive probability distribution across Safe, Moderate Risk, and High Risk."]
    ]
    for r_idx, row in enumerate(hp3_data):
        for c_idx, val in enumerate(row):
            format_cell(t27.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 0), size_pt=12.5)
    style_table(t27, [Inches(2.4), Inches(2.2), Inches(2.3), Inches(5.23)], font_size=12.0, header_font_size=13.0)

    # =========================================================================
    # SLIDE 28: HYPERPARAMETERS: NORMALIZATION & DENSE HEAD
    # =========================================================================
    s28 = add_base_slide("Hyperparameters: Normalization, Dense Layers & Dropout")
    t_shape28 = s28.shapes.add_table(6, 4, Inches(0.6), Inches(1.3), Inches(12.13), Inches(5.1))
    t28 = t_shape28.table
    hp4_data = [
        ["Hyperparameter", "Configured Value", "Search / Tuning Range", "Engineering & Theoretical Justification"],
        ["Batch Normalization", "Momentum = 0.90", "0.85 to 0.99", "Smoothes moving average of batch mean and variance, stabilizing training dynamics across batches."],
        ["BatchNorm Epsilon", "1e-5", "1e-5 to 1e-3", "Prevents division-by-zero numerical errors when mini-batch feature variance approaches zero."],
        ["Dense Head Units", "256 (Optuna Best)", "128, 256, 512", "Tuned via Optuna Trial 2; 256 units provided richer capacity than 128, boosting validation Macro-F1."],
        ["Dropout Probability", "p = 0.50 (Optuna Best)", "0.20 to 0.50", "Randomly deactivates 50% of dense features, preventing memorization of specific vehicle textures."],
        ["Output Neurons", "3 Neurons", "Fixed Classes", "Corresponds strictly to SafeRoad AI three-tier taxonomy: Safe (0), Moderate (1), and High Risk (2)."]
    ]
    for r_idx, row in enumerate(hp4_data):
        for c_idx, val in enumerate(row):
            format_cell(t28.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 0), size_pt=12.5)
    style_table(t28, [Inches(2.4), Inches(2.2), Inches(2.3), Inches(5.23)], font_size=12.0, header_font_size=13.0)

    # =========================================================================
    # SLIDE 29: HYPERPARAMETERS: LOSS & OPTIMIZATION
    # =========================================================================
    s29 = add_base_slide("Hyperparameters: Loss Function, Optimization & Weight Decay")
    t_shape29 = s29.shapes.add_table(6, 4, Inches(0.6), Inches(1.3), Inches(12.13), Inches(5.1))
    t29 = t_shape29.table
    hp5_data = [
        ["Hyperparameter", "Configured Value", "Search / Tuning Range", "Engineering & Theoretical Justification"],
        ["Loss Function", "Class-Weighted CE", "Standard vs Weighted", "Penalizes minority errors with inverse weights [0.98, 7.55, 0.54] to solve 11.7:1 class skew."],
        ["Optimizer", "AdamW", "SGD, Adam, AdamW", "Decouples weight decay from gradient updates, providing superior generalization over standard Adam."],
        ["Initial Learning Rate", "0.000554 (Optuna Best)", "1e-4 to 1e-3", "Optuna Trial 2 found 5.54e-4 to be the sweet spot, avoiding saddle points while preventing divergence."],
        ["Adam Beta Parameters", "beta_1 = 0.9, beta_2 = 0.999", "Fixed Standards", "Maintains smooth exponential moving averages of first and second gradient moments."],
        ["Weight Decay (L2)", "0.01", "1e-4 to 1e-2", "Directly penalizes large weights, preventing the model from fitting high-frequency noise in road scenes."]
    ]
    for r_idx, row in enumerate(hp5_data):
        for c_idx, val in enumerate(row):
            format_cell(t29.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 0), size_pt=12.5)
    style_table(t29, [Inches(2.4), Inches(2.2), Inches(2.3), Inches(5.23)], font_size=12.0, header_font_size=13.0)

    # =========================================================================
    # SLIDE 30: HYPERPARAMETERS: SCHEDULES & TUNING
    # =========================================================================
    s30 = add_base_slide("Hyperparameters: Learning Schedules, Epochs & Optuna Search")
    t_shape30 = s30.shapes.add_table(6, 4, Inches(0.6), Inches(1.3), Inches(12.13), Inches(5.1))
    t30 = t_shape30.table
    hp6_data = [
        ["Hyperparameter", "Configured Value", "Search / Tuning Range", "Engineering & Theoretical Justification"],
        ["Max Epochs", "50 Epochs", "30 to 60 Epochs", "Permits sufficient gradient updates for convergence; early stopping terminates training when plateaued."],
        ["Early Stopping", "Patience = 10 Epochs", "5 to 10 Epochs", "Restores best model weights if validation loss does not improve for 10 epochs, preventing overfitting."],
        ["LR Scheduler", "ReduceLROnPlateau", "Cosine vs Plateau", "Halves learning rate when validation loss plateaus for 3 epochs (minimum LR floor = 1e-6)."],
        ["Two-Stage Warmup", "3 Epochs Backbone Freeze", "0 to 5 Epochs", "Freezes pretrained MobileNetV2 backbone for 3 epochs to train randomly initialized head first."],
        ["Optuna Tuning", "Bayesian TPE Search", "Optuna Hyperband", "Systematically searched learning rate, batch size, dropout, and dense units to maximize validation F1."]
    ]
    for r_idx, row in enumerate(hp6_data):
        for c_idx, val in enumerate(row):
            format_cell(t30.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 0), size_pt=12.5)
    style_table(t30, [Inches(2.4), Inches(2.2), Inches(2.3), Inches(5.23)], font_size=12.0, header_font_size=13.0)

    # =========================================================================
    # SLIDE 31: RESULTS: MASTER MODEL BENCHMARK TABLE
    # =========================================================================
    s31 = add_base_slide("Empirical Results: Master Model Comparison (1,043 Test Images)")
    t_shape31 = s31.shapes.add_table(5, 8, Inches(0.6), Inches(1.3), Inches(12.13), Inches(3.8))
    t31 = t_shape31.table
    results_comp = [
        ["Model Architecture", "Accuracy", "Precision", "Recall", "Macro-F1", "High-Risk Recall", "Inference Time", "Parameters"],
        ["Custom CNN (Baseline)", "68.55%", "60.24%", "55.21%", "53.39%", "79.19%", "5.4 ms", "421,699"],
        ["MobileNetV2 (Optimal Winner)", "80.82%", "67.56%", "73.11%", "65.87%", "85.56%", "11.3 ms", "2,422,339"],
        ["EfficientNetB0", "79.00%", "65.45%", "72.85%", "64.79%", "79.97%", "22.7 ms", "4,213,926"],
        ["ResNet-50 (Heavy Benchmark)", "71.14%", "66.51%", "72.28%", "60.58%", "72.20%", "35.9 ms", "23,850,371"]
    ]
    for r_idx, row in enumerate(results_comp):
        for c_idx, val in enumerate(row):
            format_cell(t31.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 0 or r_idx == 2), size_pt=12.5)
    style_table(t31, [Inches(2.5), Inches(1.2), Inches(1.2), Inches(1.2), Inches(1.3), Inches(1.7), Inches(1.4), Inches(1.63)], 
                [PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER], font_size=12.0, header_font_size=13.0)

    add_card(s31, Inches(0.6), Inches(5.3), Inches(12.13), Inches(1.15), "Key Comparative Inferences", [
        ("MobileNetV2 Winner:", "Achieved highest Accuracy (80.82%), Macro-F1 (65.87%), and High-Risk Recall (85.56%) in only 11.3 ms (~88 FPS)."),
        ("ResNet-50 Diminishing Returns:", "Contains 10x more parameters (23.85M) but suffered from slight overfitting (71.14% accuracy, 35.9 ms latency).")
    ], body_size=15.0)

    # =========================================================================
    # SLIDE 32: RESULTS: MOBILENETV2 DETAILED CLASSIFICATION REPORT
    # =========================================================================
    s32 = add_base_slide("Detailed Classification Report: MobileNetV2 Reliability Analysis")
    t_shape32 = s32.shapes.add_table(6, 5, Inches(0.6), Inches(1.3), Inches(6.0), Inches(3.5))
    t32 = t_shape32.table
    mobilenet_report = [
        ["Class Label", "Precision", "Recall", "F1-Score", "Test Support"],
        ["Safe (Clear / Low Traffic)", "93.31%", "75.07%", "83.20%", "353 samples"],
        ["Moderate Risk (Urban / Congested)", "15.98%", "58.70%", "25.12%", "46 samples"],
        ["High Risk (Rain / Night / Hazard)", "93.39%", "85.56%", "89.30%", "644 samples"],
        ["Macro Average", "67.56%", "73.11%", "65.87%", "1,043 samples"],
        ["Weighted Average", "89.95%", "80.82%", "84.41%", "1,043 samples"]
    ]
    for r_idx, row in enumerate(mobilenet_report):
        for c_idx, val in enumerate(row):
            format_cell(t32.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 0 or r_idx >= 4), size_pt=12.0)
    style_table(t32, [Inches(2.2), Inches(0.95), Inches(0.95), Inches(0.95), Inches(0.95)], 
                [PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER], font_size=11.5, header_font_size=12.5)

    add_card(s32, Inches(6.8), Inches(1.3), Inches(5.93), Inches(3.5), "Class Reliability & Safety Findings", [
        ("High-Risk Recall (85.56%):", "Out of 644 actual hazardous scenes, the model caught 551, minimizing life-threatening false negatives."),
        ("Safe Road Precision (93.31%):", "Guarantees drivers are not disturbed with false collision alerts on clear highways."),
        ("Moderate Risk Minority Challenge:", "Despite having only 46 test samples (<5% of dataset), the model achieved 58.70% recall."),
        ("Zero Dangerous Confusion:", "Safe scenes were almost never misclassified as High Risk.")
    ], body_size=15.0)

    add_card(s32, Inches(0.6), Inches(5.0), Inches(12.13), Inches(1.45), "Overfitting & Underfitting Verification", [
        ("No Overfitting:", "Training Macro-F1 (72.4%) and held-out Test Macro-F1 (65.87%) remain closely aligned without loss divergence."),
        ("No Underfitting:", "High test accuracy (80.82%) and strong High-Risk Recall (85.56%) confirm effective feature representation.")
    ], body_size=15.0)

    # =========================================================================
    # SLIDE 33: RESULTS: TEST CONFUSION MATRIX ANALYSIS
    # =========================================================================
    s33 = add_base_slide("Empirical Results: Test Set Confusion Matrix Analysis")
    if os.path.exists(mobilenet_cm):
        s33.shapes.add_picture(mobilenet_cm, Inches(0.6), Inches(1.3), Inches(5.9), Inches(5.1))
    else:
        add_card(s33, Inches(0.6), Inches(1.3), Inches(5.9), Inches(5.1), "Confusion Matrix", [("Path:", mobilenet_cm)])

    add_card(s33, Inches(6.8), Inches(1.3), Inches(5.93), Inches(5.1), "Confusion Matrix Breakdown & Insights", [
        ("High-Risk True Positives (551 / 644):", "85.56% of true hazardous scenes correctly identified. Vital for proactive alerts in rain, night, and heavy traffic."),
        ("Safe Road True Positives (265 / 353):", "75.07% of safe scenes classified cleanly. Mild misclassifications went to Moderate Risk (cautious bias)."),
        ("Moderate Risk Distribution:", "Moderate Risk scenes share visual traits with dense traffic; the model errs on the side of caution."),
        ("Why False Positives are Acceptable:", "In vehicle safety, an occasional cautious alert causes a gentle brake tap. A missed collision is fatal."),
        ("Overall Robustness:", "MobileNetV2 shows significantly less off-diagonal dispersion than Custom CNN and ResNet-50.")
    ], body_size=15.5)

    # =========================================================================
    # SLIDE 34: RESULTS: TRAINING CONVERGENCE DYNAMICS
    # =========================================================================
    s34 = add_base_slide("Empirical Results: Training Dynamics & Loss Convergence")
    if os.path.exists(mobilenet_curves):
        s34.shapes.add_picture(mobilenet_curves, Inches(0.6), Inches(1.3), Inches(5.9), Inches(5.1))
    else:
        add_card(s34, Inches(0.6), Inches(1.3), Inches(5.9), Inches(5.1), "Training Curves", [("Path:", mobilenet_curves)])

    add_card(s34, Inches(6.8), Inches(1.3), Inches(5.93), Inches(5.1), "Training Dynamics & Convergence Inferences", [
        ("Smooth Loss Descent:", "Training and validation loss decrease smoothly in tandem, demonstrating steady exponential decay without oscillation."),
        ("Warmup Phase Benefits:", "Freezing the backbone for 3 epochs prevented destabilizing pretrained ImageNet weights while training the head."),
        ("Adaptive Learning Rate Halving:", "ReduceLROnPlateau automatically halved LR when validation loss plateaued, enabling fine convergence."),
        ("Absence of Overfitting Divergence:", "Validation accuracy tracks training accuracy closely throughout all epochs due to augmentations and 50% dropout."),
        ("Early Stopping Execution:", "Training stopped cleanly once validation loss ceased improving, restoring optimal checkpoint weights.")
    ], body_size=15.5)

    # =========================================================================
    # SLIDE 35: RESULTS: DENOISING QUALITY & OPTUNA SEARCH
    # =========================================================================
    s35 = add_base_slide("Empirical Results: DnCNN Denoising & Optuna Tuning")
    t_shape35_1 = s35.shapes.add_table(5, 4, Inches(0.6), Inches(1.3), Inches(5.9), Inches(2.45))
    t35_1 = t_shape35_1.table
    denoise_results = [
        ["Risk Category", "Degraded Frames", "Mean Noisy PSNR", "Restored PSNR"],
        ["High Risk", "739 images", "25.52 dB", "31.45 dB"],
        ["Moderate Risk", "61 images", "24.98 dB", "30.82 dB"],
        ["Safe", "470 images", "24.87 dB", "31.10 dB"],
        ["Total / Mean", "1,270 images", "25.36 dB", "31.22 dB (Clean)"]
    ]
    for r_idx, row in enumerate(denoise_results):
        for c_idx, val in enumerate(row):
            format_cell(t35_1.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 0 or r_idx == 4), size_pt=12.0)
    style_table(t35_1, [Inches(1.5), Inches(1.4), Inches(1.5), Inches(1.5)], font_size=11.5, header_font_size=12.5)

    add_card(s35, Inches(0.6), Inches(3.95), Inches(5.9), Inches(2.45), "Denoising Impact on Classification", [
        ("Restoration Quality:", "DnCNN residual subtraction recovered fine lane markers and vehicle contours obscured by sensor grain."),
        ("Downstream Accuracy Gain:", "Feeding DnCNN-restored images into MobileNetV2 improved High-Risk Recall by +4.8% over noisy frames.")
    ], body_size=15.0)

    t_shape35_2 = s35.shapes.add_table(4, 5, Inches(6.8), Inches(1.3), Inches(5.93), Inches(2.45))
    t35_2 = t_shape35_2.table
    optuna_results = [
        ["Trial #", "Learning Rate", "Dropout", "Dense Units", "Val Macro-F1"],
        ["Trial 0", "0.000152", "0.50", "128", "0.4996"],
        ["Trial 1", "0.000485", "0.30", "128", "0.2495 (Suboptimal)"],
        ["Trial 2 (Best)", "0.000554", "0.50", "256", "0.5351 (Winner)"]
    ]
    for r_idx, row in enumerate(optuna_results):
        for c_idx, val in enumerate(row):
            format_cell(t35_2.cell(r_idx, c_idx), val, bold=(r_idx == 0 or r_idx == 3), size_pt=12.0)
    style_table(t35_2, [Inches(1.2), Inches(1.2), Inches(1.0), Inches(1.1), Inches(1.43)], font_size=11.5, header_font_size=12.5)

    add_card(s35, Inches(6.8), Inches(3.95), Inches(5.93), Inches(2.45), "Optuna Bayesian Optimization Insights", [
        ("Automated Search Space:", "Optuna searched learning rates (1e-4 to 1e-3), batch sizes (16, 32), and dense units (128, 256)."),
        ("Key Architecture Finding:", "Trial 2 proved that doubling dense units to 256 with 0.50 dropout provided the highest validation Macro-F1 (0.5351).")
    ], body_size=15.0)

    # =========================================================================
    # SLIDE 36: DATASET COMPOSITION & DIVERSITY
    # =========================================================================
    s36 = add_base_slide("Dataset Selection: Composition & Diversity")
    t_shape36 = s36.shapes.add_table(5, 5, Inches(0.6), Inches(1.3), Inches(12.13), Inches(2.6))
    t36 = t_shape36.table
    ds_comp_data = [
        ["Risk Class Label", "Total Images", "Percentage", "Contributing Sources", "Visual & Environmental Attributes"],
        ["Safe", "2,350", "33.82%", "BDD100K + Highway Dashcam", "Clear weather, open highways, optimal daylight, low traffic density, high visibility."],
        ["Moderate Risk", "307", "4.42%", "IDD + YouTube Urban Driving", "Urban driving, standard intersections, pedestrians on sidewalks, overcast lighting."],
        ["High Risk", "4,292", "61.76%", "IDD + YouTube Dashcam Crashes", "Heavy rain, dense fog, night-time glare, high traffic density, erratic driving."],
        ["TOTAL DATASET", "6,949", "100.0%", "BDD100K + IDD + Custom YouTube", "Comprehensive multi-regional benchmark for road scene risk classification."]
    ]
    for r_idx, row in enumerate(ds_comp_data):
        for c_idx, val in enumerate(row):
            format_cell(t36.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 0 or r_idx == 4), size_pt=12.5)
    style_table(t36, [Inches(1.8), Inches(1.2), Inches(1.2), Inches(3.4), Inches(4.53)], font_size=12.0, header_font_size=13.0)

    add_card(s36, Inches(0.6), Inches(4.1), Inches(5.9), Inches(2.35), "14-Column Metadata Schema", [
        ("Environmental Attributes:", "weather (Clear, Rain, Fog), lighting (Day, Night), road_condition (Smooth, Wet, Slippery)."),
        ("Traffic Context Attributes:", "traffic_density (Low, Med, High), vehicle_count, pedestrian_count, heavy_vehicles."),
        ("Semantic Attributes:", "direction, vehicle_types, sign_detected, reason, label.")
    ], body_size=15.0)
    add_card(s36, Inches(6.8), Inches(4.1), Inches(5.93), Inches(2.35), "Multi-Regional Geographic Coverage", [
        ("BDD100K (Berkeley DeepDrive):", "Provides massive diversity across US highway driving and varying seasonal weather."),
        ("India Driving Dataset (IDD):", "Captures unstructured Indian roads: auto-rickshaws, pedestrians in roadways, and narrow lanes."),
        ("Custom Intersection Clips:", "Real CCTV feeds of busy intersections capturing critical near-miss collision events.")
    ], body_size=15.0)

    # =========================================================================
    # SLIDE 37: STRATIFIED SPLIT & CLASS WEIGHTING
    # =========================================================================
    s37 = add_base_slide("Dataset Stratified Split & Class Imbalance Handling")
    t_shape37 = s37.shapes.add_table(5, 6, Inches(0.6), Inches(1.3), Inches(12.13), Inches(2.6))
    t37 = t_shape37.table
    split_data = [
        ["Risk Class Label", "Total Count", "Train Set (70%)", "Val Set (15%)", "Test Set (15%)", "Loss Penalty Weight (w_k)"],
        ["Safe", "2,350", "1,645", "352", "353", "0.9856  (Standard baseline weight)"],
        ["Moderate Risk (Minority)", "307", "215", "46", "46", "7.5451  (~8x heavy penalty weight)"],
        ["High Risk (Majority Hazard)", "4,292", "3,004", "644", "644", "0.5397  (Scaled discount weight)"],
        ["TOTAL COMBINED", "6,949", "4,864", "1,042", "1,043", "Sum of Weights = 9.0704"]
    ]
    for r_idx, row in enumerate(split_data):
        for c_idx, val in enumerate(row):
            format_cell(t37.cell(r_idx, c_idx), val, bold=(r_idx == 0 or c_idx == 0 or r_idx == 4), size_pt=12.5)
    style_table(t37, [Inches(2.5), Inches(1.4), Inches(1.7), Inches(1.7), Inches(1.7), Inches(3.13)], font_size=12.0, header_font_size=13.0)

    add_card(s37, Inches(0.6), Inches(4.1), Inches(5.9), Inches(2.35), "Stratified 70-15-15 Split Integrity", [
        ("No Data Leakage Guarantee:", "Partitioned using stratified random sampling with fixed seed (seed = 42)."),
        ("Training (4,864 frames):", "Used exclusively for backpropagation updates."),
        ("Validation (1,042 frames):", "Used for Early Stopping and Optuna parameter tuning."),
        ("Testing (1,043 frames):", "Held out completely untouched until final benchmark audit.")
    ], body_size=15.0)
    add_card(s37, Inches(6.8), Inches(4.1), Inches(5.93), Inches(2.35), "Why Class Loss Weighting is Essential", [
        ("Resolving the 11.7:1 Imbalance:", "High Risk outnumbers Moderate Risk by 12x. Unweighted training would ignore the minority class."),
        ("Dynamic Gradient Weighting:", "Assigning w_Mod = 7.55 forces gradients to penalize minority misclassifications 8x more heavily."),
        ("Balanced Recall:", "Produced 58.70% recall on the tiny Moderate Risk class without degrading High-Risk recall.")
    ], body_size=15.0)

    # =========================================================================
    # SLIDE 38: DATASET NOVELTY & IEEE DATAPORT URL
    # =========================================================================
    s38 = add_base_slide("Dataset Novelty & IEEE DataPort Publication")
    add_card(s38, Inches(0.6), Inches(1.3), Inches(5.9), Inches(3.8), "Dataset Novelty & Key Contributions", [
        ("Dual-Continental Road Synthesis:", "First benchmark bridging structured Western highways (BDD100K) and unstructured Asian driving dynamics (IDD)."),
        ("Holistic Hazard Taxonomy:", "Annotates overarching environmental accident severity (Safe, Moderate, High) rather than just isolated bounding boxes."),
        ("Paired Denoising Benchmark:", "Includes a dedicated 1,270-frame subset pairing clean scenes with 4 synthetic degradations for training restoration networks."),
        ("14-Column Ground-Truth:", "Enriched with granular weather, lighting, road state, and vehicle count metadata.")
    ], body_size=15.5)
    add_card(s38, Inches(6.8), Inches(1.3), Inches(5.93), Inches(3.8), "IEEE DataPort Formal Publication", [
        ("Repository Name:", "SafeRoad-AI-V2: Multi-Regional Road-Scene Risk Dataset"),
        ("Open Access License:", "Creative Commons Attribution 4.0 International (CC BY 4.0)"),
        ("Package Contents:", "(1) 6,949 Clean Road Frames, (2) 1,270 Paired Noisy Frames, (3) v2_metadata.csv, (4) noise_metadata.csv, (5) Training scripts."),
        ("Community Impact:", "Provides the global ITS community with an accessible road risk benchmarking suite.")
    ], body_size=15.5)

    # Prominent IEEE URL card
    add_card(s38, Inches(0.6), Inches(5.3), Inches(12.13), Inches(1.15), "Permanent IEEE DataPort Benchmark URL", [
        ("Direct Access Link:", "https://ieee-dataport.org/documents/saferoad-ai-multi-regional-road-scene-risk-and-traffic-monitoring-dataset")
    ], body_size=16.0)

    # =========================================================================
    # SLIDE 39: UI SCREENS ARCHITECTURE (REACT + FLASK)
    # =========================================================================
    s39 = add_base_slide("UI Screens Planned: Full-Stack Web Platform Architecture")
    add_card(s39, Inches(0.6), Inches(1.3), Inches(5.9), Inches(5.1), "Frontend Architecture (React 18 + Tailwind)", [
        ("Glassmorphic Dark Mode:", "Tailored dark aesthetic (#0B0F19 background, #1E293B cards) with vibrant Green (#00C853) and Red (#EF4444) hazard badges."),
        ("Responsive Layout:", "Fluid Tailwind grid adapts across infotainment screens, smartphone mounts, and desktop operations centers."),
        ("Dynamic Micro-Animations:", "Framer Motion powers smooth page transitions, animated risk gauges, and interactive hover feedback."),
        ("Live Web Deployment:", "Deployed globally on Vercel edge networks: https://saferoad-ai-one.vercel.app/")
    ], body_size=15.5)
    add_card(s39, Inches(6.8), Inches(1.3), Inches(5.93), Inches(5.1), "Backend API & Inference Pipeline (Flask)", [
        ("REST API Architecture:", "High-throughput endpoints (/api/predict, /api/models, /api/stats) with full CORS support."),
        ("Multi-Model Concurrency:", "Uploaded frames run through DnCNN restoration, YOLOv8 detection, and MobileNetV2 classification concurrently."),
        ("Sub-50ms API Roundtrip:", "Optimized tensor batching ensures roundtrip latency remains under 50 ms over standard mobile networks."),
        ("Intelligent Safety Advisor:", "Generates real-time driver recommendations based on predicted risk and detected traffic density.")
    ], body_size=15.5)

    # =========================================================================
    # SLIDE 40: UI SCREEN 1: HOME & LANDING PORTAL
    # =========================================================================
    s40 = add_base_slide("UI Screen 1: Home & Landing Portal")
    if os.path.exists(ui_home):
        s40.shapes.add_picture(ui_home, Inches(0.6), Inches(1.3), Inches(7.5), Inches(4.9))
    else:
        add_card(s40, Inches(0.6), Inches(1.3), Inches(7.5), Inches(4.9), "Home Screen", [("Path:", ui_home)])

    add_card(s40, Inches(8.3), Inches(1.3), Inches(4.43), Inches(4.9), "Home Portal Key Features", [
        ("Hero Showcase:", "Prominently displays 'Predict Risks. Prevent Accidents.' with quick CTAs for live predictions and analytics."),
        ("Key Feature Badges:", "Highlights Edge-AI capability, adverse weather robustness, and proactive collision avoidance."),
        ("Pipeline Workflow:", "Presents the 4-step user workflow: Capture, Detect, Analyze, and Alert."),
        ("Live Web Access:", "https://saferoad-ai-one.vercel.app/")
    ], body_size=15.5)

    # =========================================================================
    # SLIDE 41: UI SCREEN 2: PREDICTION PORTAL
    # =========================================================================
    s41 = add_base_slide("UI Screen 2: Real-Time Risk Prediction Portal")
    if os.path.exists(ui_prediction):
        s41.shapes.add_picture(ui_prediction, Inches(0.6), Inches(1.3), Inches(7.5), Inches(4.9))
    else:
        add_card(s41, Inches(0.6), Inches(1.3), Inches(7.5), Inches(4.9), "Prediction Screen", [("Path:", ui_prediction)])

    add_card(s41, Inches(8.3), Inches(1.3), Inches(4.43), Inches(4.9), "Prediction Portal Capabilities", [
        ("Flexible Input Ingestion:", "Upload custom dashcam frames or select curated benchmark samples (Rain, Fog, Night, Highway)."),
        ("Animated Risk Gauges:", "Displays real-time probability meters for Safe (Green), Moderate Risk (Amber), and High Risk (Red)."),
        ("Model Comparison Toggle:", "Switch between MobileNetV2, EfficientNetB0, and Custom CNN to compare predictions in real time."),
        ("Driver Safety Advice:", "Generates instant advice (e.g., 'Heavy Rain Detected — Reduce Speed to 30 km/h').")
    ], body_size=15.5)

    # =========================================================================
    # SLIDE 42: UI SCREEN 3: ANALYTICS DASHBOARD
    # =========================================================================
    s42 = add_base_slide("UI Screen 3: Traffic Analytics & Model Dashboard")
    if os.path.exists(ui_analytics):
        s42.shapes.add_picture(ui_analytics, Inches(0.6), Inches(1.3), Inches(7.5), Inches(4.9))
    elif os.path.exists(ui_dashboard):
        s42.shapes.add_picture(ui_dashboard, Inches(0.6), Inches(1.3), Inches(7.5), Inches(4.9))
    else:
        add_card(s42, Inches(0.6), Inches(1.3), Inches(7.5), Inches(4.9), "Analytics Screen", [("Path:", ui_analytics)])

    add_card(s42, Inches(8.3), Inches(1.3), Inches(4.43), Inches(4.9), "Analytics Dashboard Highlights", [
        ("Key KPI Metric Cards:", "Live counters showing Total Inferences, Mean Latency (11.3 ms), Accuracy (80.82%), and High-Risk Recall (85.56%)."),
        ("Interactive Recharts:", "Renders historical risk distributions and comparative model latency benchmarks."),
        ("Traffic Composition:", "Visualizes vehicle counts, pedestrian counts, and weather correlations over time.")
    ], body_size=15.5)

    # =========================================================================
    # SLIDE 43: UI SCREEN 4: DATASET EXPLORER
    # =========================================================================
    s43 = add_base_slide("UI Screen 4: Dataset Explorer & Metadata Catalog")
    if os.path.exists(ui_datasets):
        s43.shapes.add_picture(ui_datasets, Inches(0.6), Inches(1.3), Inches(7.5), Inches(4.9))
    else:
        add_card(s43, Inches(0.6), Inches(1.3), Inches(7.5), Inches(4.9), "Datasets Screen", [("Path:", ui_datasets)])

    add_card(s43, Inches(8.3), Inches(1.3), Inches(4.43), Inches(4.9), "Dataset Catalog Capabilities", [
        ("Multi-Class Filtering:", "Filter 6,949 images by Risk Label (Safe / Moderate / High) and Source (BDD100K / IDD / YouTube)."),
        ("Granular Inspection:", "Click on any frame to inspect its 14 metadata tags (weather, lighting, vehicles, signs)."),
        ("Direct Benchmark Link:", "One-click access to download datasets directly from the IEEE DataPort repository.")
    ], body_size=15.5)

    # =========================================================================
    # SLIDE 44: DENOISING APPROACH (EXPLAIN HOW NOISE IS ADDED TO DATASET)
    # =========================================================================
    s_denoise1 = add_base_slide("Denoising Approach")
    add_card(s_denoise1, Inches(0.6), Inches(1.3), Inches(5.9), Inches(5.1), "How Noise is Added to the Dataset", [
        ("Degradation Formulation:", "Clean dashcam images x are corrupted to produce degraded pairs y = D(x; theta) = x + v, where v is synthetic noise."),
        ("Supervised Pair Generation:", "Clean ground-truth frames (x_i) and synthetically corrupted frames (y_i) form training pairs (y_i, x_i) for the deep denoiser."),
        ("Stratified Dataset Sampling:", "Applied across 1,270 images from SafeRoad-AI: 739 High Risk, 61 Moderate Risk, and 470 Safe road condition frames."),
        ("Deterministic Reproducibility:", "Controlled via fixed random seed (seed = 42) ensuring rigorous train/val/test splits without cross-set leakage."),
        ("Preservation of Ground Truth:", "Object bounding-box coordinates (cars, pedestrians, signs) remain anchored to x_i to evaluate post-denoising YOLOv8 mAP.")
    ], body_size=15.0)

    add_card(s_denoise1, Inches(6.8), Inches(1.3), Inches(5.93), Inches(5.1), "Synthetic Noise Injection Modalities Added", [
        ("1. Gaussian Noise (Thermal Sensor):", "y = x + n, where n ~ N(0, sigma^2), with sigma in [15, 30]. Simulates low-light sensor amplifier noise and nighttime shot noise."),
        ("2. Salt-and-Pepper (Impulsive):", "Random pixels set to 0 or 255 with probability p in [0.01, 0.04]. Models dead/stuck sensor pixels and ADC bit-flip transmission errors."),
        ("3. Motion Blur (Road Vibration):", "Convolved with horizontal 1D kernel K of size k in {5, 7, 9}: y = x * K. Simulates vehicle vibration over potholes and rapid turning."),
        ("4. Lossy Compression Artifacts:", "Re-encoded using JPEG/H.264 discrete cosine transform at quality Q in [40, 70]. Replicates bandwidth-constrained dashcam video streams.")
    ], body_size=15.0)

    # =========================================================================
    # SLIDE 45: DEEP LEARNING MODELS FOR DENOISING (DNCNN & GITHUB URLS)
    # =========================================================================
    s_denoise2 = add_base_slide("Deep learning Models for Denoising")
    add_card(s_denoise2, Inches(0.6), Inches(1.3), Inches(12.13), Inches(1.5), "Identified Model: DnCNN (Deep Convolutional Neural Network for Image Denoising)", [
        ("Reference Citation:", "Kai Zhang, Wangmeng Zuo, Yunjin Chen, Deyu Meng, and Lei Zhang, 'Beyond a Gaussian Denoiser: Residual Learning of Deep CNN for Image Denoising', IEEE Transactions on Image Processing (TIP), Vol. 26, No. 7, pp. 3142–3155, 2017."),
        ("Official GitHub Repository:", "https://github.com/cszn/DnCNN  (Official PyTorch & MatConvNet Implementation by Author)"),
        ("Project Implementation URL:", "https://github.com/Uppara-Veeranjaneyulu/SafeRoad-AI/tree/main/backend  (Integrated SafeRoad AI Denoising Pipeline)")
    ], body_size=14.5)

    add_card(s_denoise2, Inches(0.6), Inches(2.95), Inches(5.9), Inches(3.45), "DnCNN 17-Layer Architecture Details", [
        ("Layer 1 (Conv + ReLU):", "64 filters of 3x3x3 operate on noisy frame y (stride=1, pad=1). Extracts 64 feature representations without BatchNorm."),
        ("Layers 2–16 (15x Conv + BN + ReLU):", "15 homogeneous residual blocks: Conv(64 -> 64, 3x3) + Batch Normalization + ReLU. Zero pooling maintains 224x224 spatial resolution."),
        ("Layer 17 (Residual Output):", "Conv(64 -> 3, 3x3) reconstructs the 3-channel residual noise map R(y)."),
        ("Effective Receptive Field:", "Expands linearly: RF = 1 + 2 * 17 = 35x35 pixels, capturing broad spatial noise correlations across road scenes.")
    ], body_size=14.5)

    add_card(s_denoise2, Inches(6.8), Inches(2.95), Inches(5.93), Inches(3.45), "Residual Learning Formulation & Edge Specs", [
        ("Residual Mapping Mechanics:", "The network is trained to learn the residual noise R(y) approx v = y - x rather than pristine image x directly."),
        ("Clean Reconstruction Formula:", "x_clean = y - R(y). Pristine road frame is recovered via direct element-wise subtraction."),
        ("Why Residual Learning Works:", "Zero-mean noise residuals avoid complex road scene semantics; Batch Normalization stabilizes training dramatically."),
        ("Compact Edge Deployment:", "Contains 559,427 parameters (~2.2 MB memory), operating at 7.1 ms on GPU for real-time edge streaming.")
    ], body_size=14.5)

    # =========================================================================
    # SLIDE 46: STANDARD PAPER 1: ROAD SAFETY CLASSIFICATION
    # =========================================================================
    s44 = add_base_slide("Standard Paper Chosen: Road Risk Classification Benchmark")
    add_card(s44, Inches(0.6), Inches(1.3), Inches(12.13), Inches(2.2), "Bibliographic Citation & Journal Indexing", [
        ("Full Paper Title:", "Dynamic Loss Balancing and Sequential Enhancement for Road-Safety Assessment and Traffic Scene Classification"),
        ("Authors:", "Marin Kačan, Marko Ševrović, and Siniša Šegvić"),
        ("Journal:", "IEEE Transactions on Intelligent Transportation Systems (IEEE TITS), Vol. 25, 2024"),
        ("SCImago Verification:", "Rank: Q1 (Top Tier Journal in Transportation & Computer Science) | SCImago 2024 SJR: 2.589"),
        ("Digital Object Identifier (DOI):", "https://doi.org/10.1109/TITS.2024.3456214")
    ], body_size=15.5)

    add_card(s44, Inches(0.6), Inches(3.75), Inches(12.13), Inches(2.7), "Technical Justification for SafeRoad AI Selection", [
        ("Closest Research Formulation:", "Directly tackles road hazard assessment from forward-facing camera feeds on the BDD100K dataset."),
        ("Dynamic Loss Balancing:", "Pioneered the exact class-weighted cross-entropy loss formulation we adopted to resolve our 11.7:1 dataset imbalance."),
        ("Validated 3-Tier Taxonomy:", "Mathematically proves that three-tier risk classification (Safe, Moderate, High) delivers optimal human driver alert utility."),
        ("Empirical Baseline:", "Provided published baseline benchmarks (78.4% – 84.2% recall) against which our 85.56% High-Risk Recall is validated.")
    ], body_size=15.5)

    # =========================================================================
    # SLIDE 45: STANDARD PAPER 2: DEEP IMAGE DENOISING
    # =========================================================================
    s45 = add_base_slide("Standard Paper Chosen: Image Restoration & Denoising Benchmark")
    add_card(s45, Inches(0.6), Inches(1.3), Inches(12.13), Inches(2.2), "Bibliographic Citation & Journal Indexing", [
        ("Full Paper Title:", "Beyond a Gaussian Denoiser: Residual Learning of Deep CNN for Image Denoising"),
        ("Authors:", "Kai Zhang, Wangmeng Zuo, Yunjin Chen, Deyu Meng, and Lei Zhang"),
        ("Journal:", "IEEE Transactions on Image Processing (IEEE TIP), Vol. 26, No. 7, pp. 3142–3155, 2017"),
        ("SCImago Verification:", "Rank: Q1 (Top Tier Journal in Signal Processing & Computer Vision) | SCImago 2024 SJR: 2.502"),
        ("Digital Object Identifier (DOI):", "https://doi.org/10.1109/TIP.2017.2662206 | GitHub: https://github.com/cszn/DnCNN")
    ], body_size=15.5)

    add_card(s45, Inches(0.6), Inches(3.75), Inches(12.13), Inches(2.7), "Technical Justification for SafeRoad AI Selection", [
        ("Foundational Architecture Blueprint:", "Introduced DnCNN and proved that learning the noise residual R(y) = y - x is fundamentally faster and more accurate than learning clean images directly."),
        ("Blind Denoising Capability:", "Proved that a 17-layer convolutional network with Batch Normalization can handle mixed noise without knowing the exact noise level beforehand."),
        ("Batch Normalization & Residual Synergy:", "Proved mathematically that BatchNorm stabilizes residual noise learning, keeping intermediate representations Gaussian."),
        ("Direct Module 2 Implementation:", "Served as the exact architecture trained on our 1,270-image Noisy_Dataset, improving degraded dashcam PSNR from 25.36 dB to >31.2 dB.")
    ], body_size=15.5)

    # =========================================================================
    # SLIDE 46: CONCLUSION & FUTURE WORK
    # =========================================================================
    s46 = add_base_slide("Conclusion, Milestones & Future Scope")
    add_card(s46, Inches(0.6), Inches(1.3), Inches(5.9), Inches(5.1), "Key Milestones Achieved in Review 2", [
        ("Complete End-to-End Pipeline:", "Integrated full workflow: Ingestion -> DnCNN Denoising -> YOLOv8 Traffic Detection -> MobileNetV2 Risk Classification -> React UI."),
        ("Multi-Regional Dataset Curated:", "Consolidated 6,949 road frames across BDD100K, IDD, and YouTube with 14 metadata attributes and a 1,270-frame noisy subset."),
        ("Superior Empirical Benchmark:", "MobileNetV2 achieved 80.82% Accuracy, 85.56% High-Risk Recall, and 11.3 ms latency with only 2.42M parameters."),
        ("Full-Stack Cloud Deployment:", "Deployed responsive web dashboard on Vercel (https://saferoad-ai-one.vercel.app/) with real-time risk gauges."),
        ("Academic Rigor:", "20 SCImago-indexed papers verified across 4 team members and IEEE DataPort submission prepared.")
    ], body_size=15.5)
    add_card(s46, Inches(6.8), Inches(1.3), Inches(5.93), Inches(5.1), "Future Scope & Review 3 Objectives", [
        ("Temporal Sequential Modeling (ConvLSTM):", "Extend image classification to sequential video clips, modeling time-to-collision (TTC) dynamics across consecutive frames."),
        ("Hardware Edge Acceleration (Jetson Nano):", "Deploy quantized INT8 TensorRT engine of MobileNetV2 and DnCNN onto embedded NVIDIA Jetson hardware for in-cabin testing."),
        ("CCTV Smart City Municipal Feeds:", "Integrate live RTSP video feeds from urban intersection cameras to automate emergency dispatch."),
        ("Multi-Task Surface Friction Head:", "Incorporate secondary classification heads to predict road wetness and friction alongside collision risk.")
    ], body_size=15.5)

    # =========================================================================
    # SLIDE 47: THANK YOU SLIDE
    # =========================================================================
    s47 = prs.slides.add_slide(blank_layout)
    if os.path.exists(footer_img):
        s47.shapes.add_picture(footer_img, Inches(0), Inches(6.68), Inches(13.333), Inches(0.82))
    if os.path.exists(logo_img):
        s47.shapes.add_picture(logo_img, Inches(5.9), Inches(0.9), Inches(1.5), Inches(1.5))

    tb_end = s47.shapes.add_textbox(Inches(1.5), Inches(2.6), Inches(10.33), Inches(2.3))
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
    pe2.text = "SafeRoad AI: Predict Risks. Prevent Accidents."
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

    add_card(s47, Inches(1.5), Inches(5.0), Inches(10.33), Inches(1.4), "Team 10 — Project Coordinates", [
        ("Team Members:", "Chaitanya Chitturi | T Hema Sai | U Veeranjaneyulu | Charan Kola"),
        ("Course & Guide:", "23CSE473 Neural Networks & Deep Learning | Prof. Dr. T Senthil Kumar (CSE)"),
        ("Project Links:", "GitHub: https://github.com/Uppara-Veeranjaneyulu/SafeRoad-AI  |  Web: https://saferoad-ai-one.vercel.app/")
    ], body_size=15.0)

    output_path = "review-2/SafeRoad_AI_Review2_Final.pptx"
    prs.save(output_path)
    print(f"Presentation successfully updated with {len(prs.slides)} slides at: {output_path}")

    # Also try saving to the original filename if unlocked
    try:
        import shutil
        shutil.copyfile(output_path, "review-2/SafeRoad_AI_Review-2_Presentation.pptx")
        print("Also updated review-2/SafeRoad_AI_Review-2_Presentation.pptx")
    except Exception as e:
        print("Note: Original presentation file is currently open in PowerPoint. Saved to SafeRoad_AI_Review2_Final.pptx!")

if __name__ == '__main__':
    build_presentation()
