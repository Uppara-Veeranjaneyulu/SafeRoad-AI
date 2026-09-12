# 🚦 SafeRoad AI

### Deep Learning-Based Road Scene Risk Classification and Traffic Monitoring for Proactive Road Safety

> **"Predict Risks. Prevent Accidents."**

---

## 📖 Abstract

SafeRoad AI is an AI-powered intelligent road safety system designed to perform **road scene risk classification** and **traffic monitoring** using deep learning and computer vision. The system aims to assist drivers by analyzing road-scene images and identifying potentially hazardous driving conditions before accidents occur.

The project utilizes the **BDD100K (Berkeley DeepDrive Dataset)** and **IDD (India Driving Dataset)**, which contain diverse road environments, traffic densities, weather conditions, and driving scenarios. Road-scene images are categorized into **Safe**, **Moderate Risk**, and **High Risk** classes to enable supervised learning for accident risk prediction.

SafeRoad AI employs **YOLOv8** for intelligent traffic monitoring and object detection, enabling the detection of vehicles, pedestrians, and other road users while estimating traffic density. For road scene risk classification, the project compares three deep learning models—**CNN**, **MobileNetV2**, and **EfficientNetB0**—to evaluate their performance based on accuracy, precision, recall, F1-score, computational efficiency, and inference time. **Optuna** is used for automated hyperparameter optimization to improve model performance.

The system is developed as a modern web application using **React.js**, **Tailwind CSS**, and **Flask**, providing an intuitive interface for image upload, prediction visualization, model comparison, and analytics. SafeRoad AI demonstrates the practical application of Artificial Intelligence in intelligent transportation systems by combining computer vision, deep learning, and proactive road safety into a unified AI-powered platform.

---

## ✨ Features

- 🚗 Intelligent Traffic Monitoring
- 🧠 AI-Based Road Scene Risk Classification
- 📷 Road Image Upload & Prediction
- 🚦 YOLOv8 Vehicle & Pedestrian Detection
- 📊 Deep Learning Model Comparison
- ⚙️ Hyperparameter Optimization using Optuna
- 📈 Analytics Dashboard
- 🌐 Responsive Web Application

---

## 🏗️ Tech Stack

### Frontend
- React.js
- Tailwind CSS

### Backend
- Flask

### AI & Deep Learning
- Python
- TensorFlow
- Keras
- YOLOv8
- Optuna
- OpenCV

### Data Processing & Visualization
- NumPy
- Pandas
- Matplotlib

### Version Control
- Git
- GitHub

---

## 🤖 Deep Learning Models

| Model | Purpose |
|--------|---------|
| YOLOv8 | Traffic Monitoring & Object Detection |
| CNN | Baseline Road Scene Risk Classification |
| MobileNetV2 | Lightweight Risk Classification |
| EfficientNetB0 | High-Accuracy Risk Classification |

---

## 📂 Dataset

- **BDD100K (Berkeley DeepDrive Dataset)**
- **IDD (India Driving Dataset)**

Both datasets provide diverse driving scenarios including highways, urban roads, varying weather conditions, lighting conditions, and traffic densities for robust model training and evaluation.

---

## 🚦 Risk Categories

The system classifies road scenes into:

- 🟢 Safe
- 🟡 Moderate Risk
- 🔴 High Risk

---

## 🔄 System Workflow

```text
Road Image
      │
      ▼
OpenCV Image Preprocessing
      │
      ▼
YOLOv8 Traffic Monitoring
      │
      ▼
CNN / MobileNetV2 / EfficientNetB0
      │
      ▼
Road Risk Classification
      │
      ▼
Safety Recommendation
      │
      ▼
SafeRoad AI Dashboard
```

---

## 📊 Model Evaluation

The deep learning models are compared using:

- Accuracy
- Precision
- Recall
- F1-Score
- Inference Time
- Computational Efficiency

---

## 🎯 SDG Alignment

- **SDG 3 – Good Health and Well-Being**
- **SDG 11 – Sustainable Cities and Communities**

SafeRoad AI supports safer transportation by enabling proactive road risk analysis and intelligent traffic monitoring.

---

## 🚀 Future Scope

- Live CCTV Integration
- Real-Time Video-Based Risk Prediction
- Smart City Traffic Monitoring
- Advanced Driver Assistance System (ADAS) Integration
- Mobile Application
- Cloud Deployment
- Edge AI Deployment

