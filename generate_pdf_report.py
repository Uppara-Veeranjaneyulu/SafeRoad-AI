import os
import json
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "SafeRoad AI — Technical Project Report & Benchmark Analysis")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)

        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)
        
        self.drawString(54, 32, "SafeRoad AI System | Confidential & Technical Documentation")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_str)
        self.restoreState()

def build_pdf_report():
    pdf_filename = "SafeRoad_AI_Comprehensive_Project_Report.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    primary_color = colors.HexColor("#0F172A")
    accent_blue = colors.HexColor("#2563EB")
    dark_gray = colors.HexColor("#334155")
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary_color,
        spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=accent_blue,
        spaceAfter=14
    )
    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#64748B"),
        spaceAfter=15
    )
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=primary_color,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=accent_blue,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=dark_gray,
        spaceAfter=6
    )
    body_bold = ParagraphStyle(
        'BodyBold_Custom',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    callout_style = ParagraphStyle(
        'Callout_Text',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1E3A8A")
    )
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=dark_gray
    )
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell,
        fontName='Helvetica-Bold',
        textColor=primary_color
    )
    table_header = ParagraphStyle(
        'TableHeader',
        parent=table_cell,
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    story = []

    # Title Banner
    story.append(Paragraph("SafeRoad AI — Technical Project Report", title_style))
    story.append(Paragraph("Deep Learning Road Scene Risk Classification, Traffic Monitoring & Full-Stack Integration", subtitle_style))
    story.append(Paragraph("<b>Version:</b> 1.0.0 &nbsp;|&nbsp; <b>Date:</b> September 2026 &nbsp;|&nbsp; <b>Frameworks:</b> TensorFlow 2.18 / Keras 3, Ultralytics YOLOv8, Flask, React & Vite", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=accent_blue, spaceBefore=0, spaceAfter=12))

    # Executive Summary
    story.append(Paragraph("Executive Summary", h1_style))
    story.append(Paragraph(
        "<b>SafeRoad AI</b> is an intelligent, real-time road safety and hazard mitigation platform designed to monitor traffic scenes, "
        "detect objects, evaluate environmental hazard factors, and predict accident risk severity. In this project, a complete deep learning "
        "machine learning pipeline was designed and executed from scratch without altering the existing frontend UI. Four distinct deep learning "
        "classification models (<b>Custom CNN Baseline</b>, <b>MobileNetV2</b>, <b>EfficientNetB0</b>, and <b>ResNet50</b>) were trained on the real "
        "SafeRoad multi-source dataset, tuned using Optuna Bayesian optimization, and rigorously evaluated on an identical, strictly isolated 15% unseen test set. "
        "Ultralytics YOLOv8 was integrated for real-time contextual vehicle/pedestrian detection and traffic density estimation. "
        "A high-performance Flask REST API was deployed to connect the React/Tailwind frontend, enabling live interactive predictions, 4-model benchmarking, "
        "and persistent historical analytics.",
        body_style
    ))

    # Highlight box for Best Model
    best_model_box = [
        [
            Paragraph(
                "<b>KEY HIGHLIGHT: BEST PERFORMING MODEL DETERMINED</b><br/>"
                "<b>MobileNetV2</b> achieved the top benchmark ranking with <b>80.82% Test Accuracy</b>, "
                "<b>65.87% Macro-F1</b>, <b>85.56% High-Risk Recall</b>, and ultra-fast <b>11.3 ms/image inference latency</b>. "
                "It serves as the default production model powering live predictions on the SafeRoad AI website.",
                callout_style
            )
        ]
    ]
    t_highlight = Table(best_model_box, colWidths=[504])
    t_highlight.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EFF6FF")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#3B82F6")),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(t_highlight)
    story.append(Spacer(1, 10))

    # Section 1: Dataset & Leakage Prevention
    story.append(Paragraph("1. Dataset Architecture & Leakage-Free Splitting", h1_style))
    story.append(Paragraph(
        "The SafeRoad AI dataset aggregates real-world road scenes across multiple challenging driving contexts: "
        "<b>BDD100K</b> (diverse highway and urban scenes under varied daylight and weather), "
        "<b>India Driving Dataset (IDD)</b> (complex unstructured traffic environments), and "
        "<b>Custom Intersection Video Captures</b>. A programmatic audit confirmed <b>6,949 valid, uncorrupted RGB images</b> across three risk categories.",
        body_style
    ))

    # Dataset table
    ds_data = [
        [Paragraph("Risk Class", table_header), Paragraph("Total Count", table_header), Paragraph("Proportion", table_header), Paragraph("Train (70%)", table_header), Paragraph("Val (15%)", table_header), Paragraph("Test (15%)", table_header), Paragraph("Train Weight", table_header)],
        [Paragraph("Safe", table_cell_bold), Paragraph("2,350", table_cell), Paragraph("33.82%", table_cell), Paragraph("1,645", table_cell), Paragraph("353", table_cell), Paragraph("352", table_cell), Paragraph("0.9856", table_cell)],
        [Paragraph("Moderate Risk", table_cell_bold), Paragraph("307", table_cell), Paragraph("4.42%", table_cell), Paragraph("215", table_cell), Paragraph("46", table_cell), Paragraph("46", table_cell), Paragraph("7.5411", table_cell)],
        [Paragraph("High Risk", table_cell_bold), Paragraph("4,292", table_cell), Paragraph("61.76%", table_cell), Paragraph("3,004", table_cell), Paragraph("643", table_cell), Paragraph("645", table_cell), Paragraph("0.5397", table_cell)],
        [Paragraph("Total / Summary", table_cell_bold), Paragraph("6,949", table_cell_bold), Paragraph("100.0%", table_cell_bold), Paragraph("4,864", table_cell_bold), Paragraph("1,042", table_cell_bold), Paragraph("1,043", table_cell_bold), Paragraph("Fixed Seed=42", table_cell_bold)],
    ]
    t_ds = Table(ds_data, colWidths=[80, 60, 60, 68, 64, 64, 108])
    t_ds.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E293B")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor("#F8FAFC")]),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor("#E2E8F0")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_ds)
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "<b>Data Leakage Prevention Protocol:</b> The 1,043 test images were strictly partitioned prior to any modeling and saved to <code>ml/split_data.json</code>. "
        "The test set remained completely unseen during training, validation checkpointing, and hyperparameter tuning. "
        "Class weights were calculated <i>strictly</i> on the 4,864 training samples using inverse-frequency balancing to penalize minority misclassifications.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # Section 2: Model Architectures
    story.append(Paragraph("2. Deep Learning Model Architectures & Methodologies", h1_style))
    story.append(Paragraph(
        "All four classification models share the standardized input dimensions (224 × 224 × 3 RGB) and output space (3 classes: Safe, Moderate Risk, High Risk). "
        "Data augmentation (random horizontal flip, small rotation ±10°, random zoom ±10%, brightness shift ±10%) was applied <b>only</b> during training.",
        body_style
    ))

    arch_data = [
        [Paragraph("Model", table_header), Paragraph("Backbone Type", table_header), Paragraph("Classification Head Architecture", table_header), Paragraph("Param Count", table_header), Paragraph("Training Protocol", table_header)],
        [
            Paragraph("Custom CNN", table_cell_bold),
            Paragraph("4-Stage Conv2D Stack (32→64→128→256 filters, 3x3, ReLU, MaxPool 2x2)", table_cell),
            Paragraph("GlobalAveragePooling2D → Dense(128, ReLU) → Dropout(0.3) → Dense(3, Softmax)", table_cell),
            Paragraph("421,699", table_cell),
            Paragraph("Trained from scratch; Adam lr=0.001, ReduceLROnPlateau, EarlyStopping", table_cell)
        ],
        [
            Paragraph("MobileNetV2", table_cell_bold),
            Paragraph("Depthwise-Separable Convolutions, Inverted Residuals (ImageNet pre-trained)", table_cell),
            Paragraph("GAP → Dense(128, ReLU) → Dropout(0.3) → Dense(3, Softmax)", table_cell),
            Paragraph("2,422,339", table_cell),
            Paragraph("Two-phase: Head training (frozen backbone, lr=0.001), fine-tuning top blocks (lr=0.0001)", table_cell)
        ],
        [
            Paragraph("EfficientNetB0", table_cell_bold),
            Paragraph("Compound scaling MBConv with Squeeze-and-Excitation (ImageNet pre-trained)", table_cell),
            Paragraph("GAP → Dense(128, ReLU) → Dropout(0.3) → Dense(3, Softmax)", table_cell),
            Paragraph("4,213,926", table_cell),
            Paragraph("Feature transfer + fine-tuning upper MBConv stages with Adam lr=0.0001", table_cell)
        ],
        [
            Paragraph("ResNet50", table_cell_bold),
            Paragraph("50-layer Residual Network with Skip Connections (ImageNet pre-trained)", table_cell),
            Paragraph("GAP → Dense(128, ReLU) → Dropout(0.3) → Dense(3, Softmax)", table_cell),
            Paragraph("23,850,371", table_cell),
            Paragraph("Rescaling internal layer (-120 mean shifted) + feature extraction fine-tuning", table_cell)
        ],
        [
            Paragraph("Ultralytics YOLOv8", table_cell_bold),
            Paragraph("YOLOv8 Nano (yolov8n.pt) object detector", table_cell),
            Paragraph("Decoupled detection head: vehicle & pedestrian localization", table_cell),
            Paragraph("3,157,200", table_cell),
            Paragraph("Pretrained COCO weights; decoupled from risk classification; density estimation only", table_cell)
        ]
    ]
    t_arch = Table(arch_data, colWidths=[70, 110, 140, 60, 124])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E293B")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 10))

    # Page Break to start Section 3 cleanly
    story.append(PageBreak())

    # Section 3: Optuna Tuning
    story.append(Paragraph("3. Optuna Hyperparameter Optimization Study", h1_style))
    story.append(Paragraph(
        "To objectively select optimal training hyperparameters under severe class imbalance, an <b>Optuna Bayesian optimization study</b> was executed. "
        "The objective was set to maximize <b>Validation Macro-F1</b> rather than simple validation accuracy to ensure strong generalization on minority risk cases.",
        body_style
    ))

    optuna_data = [
        [Paragraph("Trial #", table_header), Paragraph("Learning Rate", table_header), Paragraph("Dropout", table_header), Paragraph("Dense Units", table_header), Paragraph("Batch Size", table_header), Paragraph("Val Macro-F1", table_header), Paragraph("Training Time", table_header)],
        [Paragraph("Trial 0", table_cell), Paragraph("0.000152", table_cell), Paragraph("0.50", table_cell), Paragraph("128", table_cell), Paragraph("16", table_cell), Paragraph("49.96%", table_cell), Paragraph("214.3s", table_cell)],
        [Paragraph("Trial 1", table_cell), Paragraph("0.000485", table_cell), Paragraph("0.30", table_cell), Paragraph("128", table_cell), Paragraph("16", table_cell), Paragraph("24.95%", table_cell), Paragraph("259.5s", table_cell)],
        [Paragraph("Trial 2 (Best)", table_cell_bold), Paragraph("0.000554", table_cell_bold), Paragraph("0.50", table_cell_bold), Paragraph("256", table_cell_bold), Paragraph("16", table_cell_bold), Paragraph("53.51%", table_cell_bold), Paragraph("248.7s", table_cell_bold)],
    ]
    t_optuna = Table(optuna_data, colWidths=[65, 75, 55, 70, 65, 85, 89])
    t_optuna.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E293B")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor("#F8FAFC")]),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor("#DCFCE7")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_optuna)
    story.append(Spacer(1, 10))

    # Section 4: Final Comparison
    story.append(Paragraph("4. Benchmark Performance & Comparative Model Evaluation", h1_style))
    story.append(Paragraph(
        "Each trained model was evaluated on the <b>same 1,043 unseen test images</b>. "
        "Standard statistical formulas were utilized: <i>Accuracy = (TP+TN)/(TP+TN+FP+FN)</i>, <i>Precision = TP/(TP+FP)</i>, "
        "<i>Recall = TP/(TP+FN)</i>, <i>Macro-F1 = (F1_Safe + F1_Mod + F1_High) / 3</i>. "
        "In road scene safety, <b>High-Risk Recall</b> and <b>Macro-F1</b> are prioritized over raw accuracy to prevent dangerous false negatives.",
        body_style
    ))

    comp_data = [
        [Paragraph("Model", table_header), Paragraph("Test Acc", table_header), Paragraph("Precision", table_header), Paragraph("Recall", table_header), Paragraph("F1-Score", table_header), Paragraph("Macro-F1", table_header), Paragraph("High-Risk Recall", table_header), Paragraph("Latency", table_header), Paragraph("Params", table_header)],
        [
            Paragraph("<b>MobileNetV2 (Best)</b>", table_cell_bold),
            Paragraph("<b>80.82%</b>", table_cell_bold),
            Paragraph("67.56%", table_cell),
            Paragraph("73.11%", table_cell),
            Paragraph("65.87%", table_cell),
            Paragraph("<b>65.87%</b>", table_cell_bold),
            Paragraph("<b>85.56%</b>", table_cell_bold),
            Paragraph("11.3 ms", table_cell),
            Paragraph("2.42M", table_cell)
        ],
        [
            Paragraph("EfficientNetB0", table_cell_bold),
            Paragraph("79.00%", table_cell),
            Paragraph("65.45%", table_cell),
            Paragraph("72.85%", table_cell),
            Paragraph("64.79%", table_cell),
            Paragraph("64.79%", table_cell),
            Paragraph("79.97%", table_cell),
            Paragraph("22.7 ms", table_cell),
            Paragraph("4.21M", table_cell)
        ],
        [
            Paragraph("ResNet50", table_cell_bold),
            Paragraph("71.14%", table_cell),
            Paragraph("66.51%", table_cell),
            Paragraph("72.28%", table_cell),
            Paragraph("60.58%", table_cell),
            Paragraph("60.58%", table_cell),
            Paragraph("72.20%", table_cell),
            Paragraph("35.9 ms", table_cell),
            Paragraph("23.85M", table_cell)
        ],
        [
            Paragraph("Custom CNN Baseline", table_cell_bold),
            Paragraph("68.55%", table_cell),
            Paragraph("60.24%", table_cell),
            Paragraph("55.21%", table_cell),
            Paragraph("53.39%", table_cell),
            Paragraph("53.39%", table_cell),
            Paragraph("79.19%", table_cell),
            Paragraph("5.4 ms", table_cell),
            Paragraph("0.42M", table_cell)
        ],
    ]
    t_comp = Table(comp_data, colWidths=[95, 52, 50, 48, 50, 52, 80, 45, 42])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E293B")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#EFF6FF"), colors.white, colors.HexColor("#F8FAFC"), colors.white]),
        ('LINEBELOW', (0, 1), (-1, 1), 1.5, colors.HexColor("#2563EB")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Model Selection Rationale:</b>", h2_style))
    story.append(Paragraph(
        "1. <b>Macro-F1 (65.87%)</b>: MobileNetV2 demonstrated the highest balanced metric across all three risk classes, successfully navigating the severe under-representation of Moderate Risk scenes.<br/>"
        "2. <b>High-Risk Recall (85.56%)</b>: Correctly flagged <b>552 out of 645</b> unseen test high-risk road scenes. In accident prevention, missing a high-risk situation has catastrophic real-world consequences.<br/>"
        "3. <b>Latency Efficiency (11.3 ms)</b>: Fast enough to sustain ~88 FPS on edge inference, outperforming EfficientNetB0 (22.7 ms) and ResNet50 (35.9 ms) while requiring only 2.42 million parameters.",
        body_style
    ))
    story.append(Spacer(1, 10))

    # Section 5: Visual Charts
    story.append(PageBreak())
    story.append(Paragraph("5. Empirical Training Curves & Confusion Matrices", h1_style))
    story.append(Paragraph(
        "Below are the actual measured training histories and test set confusion matrices generated during evaluation.",
        body_style
    ))

    # Best Model Visuals
    story.append(Paragraph("A. MobileNetV2 (Selected Best Model)", h2_style))
    mob_curves = "results/mobilenetv2/training_curves.png"
    mob_cm = "results/mobilenetv2/confusion_matrix.png"
    if os.path.exists(mob_curves) and os.path.exists(mob_cm):
        img_table = [
            [
                Image(mob_curves, width=3.3*inch, height=1.7*inch),
                Image(mob_cm, width=2.4*inch, height=1.7*inch)
            ],
            [
                Paragraph("<b>Figure 1a:</b> MobileNetV2 Accuracy & Loss Curves", table_cell),
                Paragraph("<b>Figure 1b:</b> MobileNetV2 Test Confusion Matrix", table_cell)
            ]
        ]
        t_img = Table(img_table, colWidths=[280, 224])
        t_img.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        story.append(t_img)
        story.append(Spacer(1, 10))

    # EfficientNetB0 Visuals
    story.append(Paragraph("B. EfficientNetB0 (Runner-Up)", h2_style))
    eff_curves = "results/efficientnetb0/training_curves.png"
    eff_cm = "results/efficientnetb0/confusion_matrix.png"
    if os.path.exists(eff_curves) and os.path.exists(eff_cm):
        img_table_eff = [
            [
                Image(eff_curves, width=3.3*inch, height=1.7*inch),
                Image(eff_cm, width=2.4*inch, height=1.7*inch)
            ],
            [
                Paragraph("<b>Figure 2a:</b> EfficientNetB0 Accuracy & Loss Curves", table_cell),
                Paragraph("<b>Figure 2b:</b> EfficientNetB0 Test Confusion Matrix", table_cell)
            ]
        ]
        t_img_eff = Table(img_table_eff, colWidths=[280, 224])
        t_img_eff.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        story.append(t_img_eff)
        story.append(Spacer(1, 10))

    # ResNet50 & CNN Visuals on next page
    story.append(PageBreak())
    story.append(Paragraph("C. ResNet50 & Custom CNN Baseline Benchmarks", h2_style))
    res_curves = "results/resnet50/training_curves.png"
    res_cm = "results/resnet50/confusion_matrix.png"
    if os.path.exists(res_curves) and os.path.exists(res_cm):
        img_table_res = [
            [
                Image(res_curves, width=3.3*inch, height=1.6*inch),
                Image(res_cm, width=2.4*inch, height=1.6*inch)
            ],
            [
                Paragraph("<b>Figure 3a:</b> ResNet50 Accuracy & Loss Curves", table_cell),
                Paragraph("<b>Figure 3b:</b> ResNet50 Confusion Matrix", table_cell)
            ]
        ]
        t_img_res = Table(img_table_res, colWidths=[280, 224])
        t_img_res.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        story.append(t_img_res)
        story.append(Spacer(1, 8))

    cnn_curves = "results/cnn/training_curves.png"
    cnn_cm = "results/cnn/confusion_matrix.png"
    if os.path.exists(cnn_curves) and os.path.exists(cnn_cm):
        img_table_cnn = [
            [
                Image(cnn_curves, width=3.3*inch, height=1.6*inch),
                Image(cnn_cm, width=2.4*inch, height=1.6*inch)
            ],
            [
                Paragraph("<b>Figure 4a:</b> Custom CNN Accuracy & Loss Curves", table_cell),
                Paragraph("<b>Figure 4b:</b> Custom CNN Confusion Matrix", table_cell)
            ]
        ]
        t_img_cnn = Table(img_table_cnn, colWidths=[280, 224])
        t_img_cnn.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        story.append(t_img_cnn)
        story.append(Spacer(1, 10))

    # Section 6: System Architecture & Full-Stack Integration
    story.append(Paragraph("6. Full-Stack System Architecture & API Endpoints", h1_style))
    story.append(Paragraph(
        "The web application integrates the trained deep learning pipeline without modifying the frontend's visual design. "
        "The React UI communicates seamlessly with the Flask REST server running on port 5000.",
        body_style
    ))

    api_data = [
        [Paragraph("HTTP Method & Route", table_header), Paragraph("Purpose / Functionality", table_header), Paragraph("Key Parameters / Payload", table_header), Paragraph("Return Data", table_header)],
        [
            Paragraph("<code>POST /api/predict</code>", table_cell_bold),
            Paragraph("Main inference endpoint for risk classification + YOLOv8 traffic analysis", table_cell),
            Paragraph("Multipart form image + query <code>?model=best/cnn/mobilenetv2/...</code>", table_cell),
            Paragraph("Risk, confidence, counts, density, safety recommendations, latency", table_cell)
        ],
        [
            Paragraph("<code>GET /api/models/list</code>", table_cell_bold),
            Paragraph("Supplies model dropdown in Prediction UI", table_cell),
            Paragraph("None", table_cell),
            Paragraph("List of models, training status, and active best model", table_cell)
        ],
        [
            Paragraph("<code>GET /api/models/comparison</code>", table_cell_bold),
            Paragraph("Supplies benchmark table in Analytics page", table_cell),
            Paragraph("None", table_cell),
            Paragraph("Measured metrics for all 4 models on unseen test set", table_cell)
        ],
        [
            Paragraph("<code>GET /api/models/metrics</code>", table_cell_bold),
            Paragraph("Supplies accuracy/loss curves and confusion matrix data", table_cell),
            Paragraph("None", table_cell),
            Paragraph("Historical epoch metrics and confusion matrix arrays", table_cell)
        ],
        [
            Paragraph("<code>GET /api/predictions/stats</code>", table_cell_bold),
            Paragraph("Feeds real-time dashboard cards", table_cell),
            Paragraph("None", table_cell),
            Paragraph("Total predictions, risk counts, traffic density breakdown", table_cell)
        ],
        [
            Paragraph("<code>GET /api/health</code>", table_cell_bold),
            Paragraph("Live backend connection status monitoring", table_cell),
            Paragraph("None", table_cell),
            Paragraph("<code>{ status: 'online', version: '1.0.0' }</code>", table_cell)
        ]
    ]
    t_api = Table(api_data, colWidths=[120, 150, 120, 114])
    t_api.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E293B")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_api)
    story.append(Spacer(1, 10))

    # Section 7: Deployment & Operations
    story.append(PageBreak())
    story.append(Paragraph("7. Operations & Execution Guide", h1_style))
    story.append(Paragraph(
        "The complete SafeRoad AI platform is fully automated and modular. To run or reproduce the system:",
        body_style
    ))

    ops_steps = [
        "<b>1. Launch Backend Server:</b> Run <code>npm run backend</code> or <code>py backend/app.py</code> (starts Flask API on port 5000).",
        "<b>2. Launch Frontend UI:</b> Run <code>npm run dev</code> (starts Vite development server on port 5173).",
        "<b>3. Access Interactive Prediction:</b> Navigate to <code>http://localhost:5173/prediction</code>. Upload any road scene image, choose a model from the dropdown (or use Best Model), and receive real-time classification, YOLOv8 detections, and hazard advisories.",
        "<b>4. Inspect Live Analytics:</b> Navigate to <code>http://localhost:5173/analytics</code> to compare all 4 models, inspect training curves, and analyze confusion matrices.",
        "<b>5. Retrain Models (Optional):</b> Run <code>py ml/train_cnn.py</code>, <code>py ml/train_mobilenet.py</code>, <code>py ml/train_efficientnet.py</code>, or <code>py ml/train_resnet.py</code> to execute standalone training pipelines.",
        "<b>6. Run Optuna Optimization:</b> Run <code>py ml/tune_models.py</code> to run Bayesian hyperparameter optimization on Validation Macro-F1."
    ]
    for step in ops_steps:
        story.append(Paragraph(step, body_style))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 8))
    story.append(Paragraph("8. Project Deliverables & Artifact Inventory", h1_style))
    
    deliv_data = [
        [Paragraph("Directory / File", table_header), Paragraph("Description & Contents", table_header)],
        [Paragraph("<code>trained_models/mobilenetv2_best.keras</code>", table_cell_bold), Paragraph("Trained weights for Best Model (MobileNetV2, 80.82% acc, 23.8 MB)", table_cell)],
        [Paragraph("<code>trained_models/efficientnetb0_best.keras</code>", table_cell_bold), Paragraph("Trained weights for EfficientNetB0 (79.00% acc, 30.7 MB)", table_cell)],
        [Paragraph("<code>trained_models/resnet50_best.keras</code>", table_cell_bold), Paragraph("Trained weights for ResNet50 (71.14% acc, 98.2 MB)", table_cell)],
        [Paragraph("<code>trained_models/cnn_best.keras</code>", table_cell_bold), Paragraph("Trained weights for Custom CNN Baseline (68.55% acc, 5.1 MB)", table_cell)],
        [Paragraph("<code>results/model_comparison.csv & .json</code>", table_cell_bold), Paragraph("Comprehensive benchmark comparison across all 4 models on unseen test set", table_cell)],
        [Paragraph("<code>results/optuna_tuning.json</code>", table_cell_bold), Paragraph("Optuna hyperparameter study records, trial trials, and optimal parameters", table_cell)],
        [Paragraph("<code>results/{model}/confusion_matrix.png</code>", table_cell_bold), Paragraph("High-resolution test set confusion matrix heatmaps for each model", table_cell)],
        [Paragraph("<code>results/{model}/training_curves.png</code>", table_cell_bold), Paragraph("Accuracy and loss trajectory plots across training and validation epochs", table_cell)],
        [Paragraph("<code>backend/app.py & routes/ & services/</code>", table_cell_bold), Paragraph("Flask REST API backend with YOLOv8 and multi-model inference pipelines", table_cell)],
        [Paragraph("<code>src/pages/Prediction.jsx, Analytics.jsx</code>", table_cell_bold), Paragraph("Integrated React UI components connected to live backend endpoints", table_cell)],
    ]
    t_deliv = Table(deliv_data, colWidths=[180, 324])
    t_deliv.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E293B")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_deliv)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[PDF Generator] Successfully generated: {pdf_filename}")
    return pdf_filename

if __name__ == '__main__':
    build_pdf_report()
