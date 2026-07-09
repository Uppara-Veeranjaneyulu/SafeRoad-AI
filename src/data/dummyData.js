// ─── Dashboard Stats ───
export const dashboardStats = {
  totalImages: 3247,
  totalPredictions: 1842,
  avgConfidence: 94.7,
  bestModel: 'EfficientNetB0',
  latestPrediction: {
    risk: 'High Risk',
    confidence: 96.2,
    timestamp: '2 min ago',
  },
};

// ─── Risk Distribution Chart ───
export const riskDistributionData = {
  labels: ['Low Risk', 'Moderate Risk', 'High Risk'],
  datasets: [{
    data: [45, 32, 23],
    backgroundColor: [
      'rgba(0, 200, 83, 0.8)',
      'rgba(255, 193, 7, 0.8)',
      'rgba(244, 67, 54, 0.8)',
    ],
    borderColor: [
      '#00C853',
      '#FFC107',
      '#F44336',
    ],
    borderWidth: 2,
    hoverOffset: 8,
  }],
};

// ─── Traffic Density Chart ───
export const trafficDensityData = {
  labels: ['Light', 'Moderate', 'Heavy', 'Very Heavy', 'Congested'],
  datasets: [{
    label: 'Traffic Density',
    data: [28, 35, 22, 10, 5],
    backgroundColor: [
      'rgba(0, 200, 83, 0.7)',
      'rgba(26, 188, 156, 0.7)',
      'rgba(255, 193, 7, 0.7)',
      'rgba(255, 87, 34, 0.7)',
      'rgba(244, 67, 54, 0.7)',
    ],
    borderRadius: 8,
    borderSkipped: false,
  }],
};

// ─── Model Comparison Chart ───
export const modelComparisonData = {
  labels: ['Accuracy', 'Precision', 'Recall', 'F1 Score'],
  datasets: [
    {
      label: 'CNN',
      data: [88.4, 87.1, 86.5, 86.8],
      backgroundColor: 'rgba(41, 182, 246, 0.7)',
      borderColor: '#29B6F6',
      borderWidth: 2,
      borderRadius: 6,
    },
    {
      label: 'MobileNetV2',
      data: [91.2, 90.8, 89.6, 90.2],
      backgroundColor: 'rgba(171, 71, 188, 0.7)',
      borderColor: '#AB47BC',
      borderWidth: 2,
      borderRadius: 6,
    },
    {
      label: 'EfficientNetB0',
      data: [95.3, 94.9, 94.1, 94.5],
      backgroundColor: 'rgba(0, 200, 83, 0.7)',
      borderColor: '#00C853',
      borderWidth: 2,
      borderRadius: 6,
    },
  ],
};

// ─── Prediction Trend Chart ───
export const predictionTrendData = {
  labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
  datasets: [
    {
      label: 'Total Predictions',
      data: [45, 62, 58, 80, 74, 95, 88],
      borderColor: '#00C853',
      backgroundColor: 'rgba(0, 200, 83, 0.1)',
      fill: true,
      tension: 0.4,
      pointBackgroundColor: '#00C853',
      pointRadius: 4,
    },
    {
      label: 'High Risk Events',
      data: [8, 14, 10, 18, 12, 22, 16],
      borderColor: '#F44336',
      backgroundColor: 'rgba(244, 67, 54, 0.05)',
      fill: true,
      tension: 0.4,
      pointBackgroundColor: '#F44336',
      pointRadius: 4,
    },
  ],
};

// ─── Accuracy / Loss Curves ───
export const accuracyCurveData = {
  labels: Array.from({ length: 50 }, (_, i) => i + 1),
  datasets: [
    {
      label: 'CNN Train',
      data: Array.from({ length: 50 }, (_, i) => 60 + 28 * (1 - Math.exp(-i / 15)) + (Math.random() - 0.5) * 2),
      borderColor: '#29B6F6',
      borderWidth: 2,
      pointRadius: 0,
      tension: 0.4,
    },
    {
      label: 'MobileNetV2 Train',
      data: Array.from({ length: 50 }, (_, i) => 64 + 28 * (1 - Math.exp(-i / 12)) + (Math.random() - 0.5) * 2),
      borderColor: '#AB47BC',
      borderWidth: 2,
      pointRadius: 0,
      tension: 0.4,
    },
    {
      label: 'EfficientNetB0 Train',
      data: Array.from({ length: 50 }, (_, i) => 68 + 28 * (1 - Math.exp(-i / 10)) + (Math.random() - 0.5) * 2),
      borderColor: '#00C853',
      borderWidth: 2,
      pointRadius: 0,
      tension: 0.4,
    },
  ],
};

export const lossCurveData = {
  labels: Array.from({ length: 50 }, (_, i) => i + 1),
  datasets: [
    {
      label: 'CNN Loss',
      data: Array.from({ length: 50 }, (_, i) => 1.5 * Math.exp(-i / 12) + 0.12 + (Math.random() - 0.5) * 0.05),
      borderColor: '#29B6F6',
      borderWidth: 2,
      pointRadius: 0,
      tension: 0.4,
    },
    {
      label: 'MobileNetV2 Loss',
      data: Array.from({ length: 50 }, (_, i) => 1.4 * Math.exp(-i / 10) + 0.09 + (Math.random() - 0.5) * 0.04),
      borderColor: '#AB47BC',
      borderWidth: 2,
      pointRadius: 0,
      tension: 0.4,
    },
    {
      label: 'EfficientNetB0 Loss',
      data: Array.from({ length: 50 }, (_, i) => 1.3 * Math.exp(-i / 9) + 0.05 + (Math.random() - 0.5) * 0.03),
      borderColor: '#00C853',
      borderWidth: 2,
      pointRadius: 0,
      tension: 0.4,
    },
  ],
};

// ─── Prediction History ───
export const predictionHistory = [
  { id: 'PR-001', image: 'highway_001.jpg', model: 'EfficientNetB0', risk: 'High Risk', confidence: 96.2, traffic: 'Heavy', weather: 'Rain', time: '2 min ago', duration: '145ms' },
  { id: 'PR-002', image: 'urban_crossroad.jpg', model: 'MobileNetV2', risk: 'Moderate Risk', confidence: 91.8, traffic: 'Moderate', weather: 'Clear', time: '15 min ago', duration: '89ms' },
  { id: 'PR-003', image: 'rural_road_dusk.jpg', model: 'EfficientNetB0', risk: 'Low Risk', confidence: 94.5, traffic: 'Light', weather: 'Foggy', time: '32 min ago', duration: '152ms' },
  { id: 'PR-004', image: 'expressway_night.jpg', model: 'CNN', risk: 'High Risk', confidence: 87.3, traffic: 'Very Heavy', weather: 'Night', time: '1 hr ago', duration: '210ms' },
  { id: 'PR-005', image: 'intersection_peak.jpg', model: 'MobileNetV2', risk: 'Moderate Risk', confidence: 89.1, traffic: 'Heavy', weather: 'Clear', time: '2 hr ago', duration: '95ms' },
  { id: 'PR-006', image: 'mountain_curve.jpg', model: 'EfficientNetB0', risk: 'High Risk', confidence: 97.8, traffic: 'Light', weather: 'Snow', time: '3 hr ago', duration: '148ms' },
  { id: 'PR-007', image: 'city_freeway.jpg', model: 'CNN', risk: 'Low Risk', confidence: 85.6, traffic: 'Moderate', weather: 'Clear', time: '5 hr ago', duration: '205ms' },
  { id: 'PR-008', image: 'school_zone.jpg', model: 'MobileNetV2', risk: 'Moderate Risk', confidence: 92.4, traffic: 'Moderate', weather: 'Cloudy', time: '6 hr ago', duration: '91ms' },
];

// ─── Model Metrics ───
export const modelMetrics = {
  CNN: {
    accuracy: 88.4,
    precision: 87.1,
    recall: 86.5,
    f1Score: 86.8,
    inferenceTime: '210ms',
    loss: 0.28,
    epochs: 50,
    params: '2.3M',
    color: '#29B6F6',
    description: 'Custom Convolutional Neural Network baseline model trained from scratch for road risk classification.',
  },
  MobileNetV2: {
    accuracy: 91.2,
    precision: 90.8,
    recall: 89.6,
    f1Score: 90.2,
    inferenceTime: '89ms',
    loss: 0.19,
    epochs: 50,
    params: '3.4M',
    color: '#AB47BC',
    description: 'Lightweight MobileNetV2 with transfer learning, optimized for real-time inference on edge devices.',
  },
  EfficientNetB0: {
    accuracy: 95.3,
    precision: 94.9,
    recall: 94.1,
    f1Score: 94.5,
    inferenceTime: '145ms',
    loss: 0.08,
    epochs: 50,
    params: '5.3M',
    color: '#00C853',
    description: 'State-of-the-art EfficientNetB0 with compound scaling, achieving best performance across all metrics.',
  },
};

// ─── Features ───
export const features = [
  {
    id: 1,
    icon: 'MdOutlineVideoCamera',
    title: 'Road Scene Analysis',
    description: 'Deep analysis of road environments using advanced computer vision to understand scene context, road conditions, and environmental factors in real-time.',
    color: '#00C853',
  },
  {
    id: 2,
    icon: 'MdOutlineTraffic',
    title: 'Traffic Monitoring',
    description: 'Continuous monitoring of traffic density patterns, vehicle flow analysis, and congestion detection across urban and highway environments.',
    color: '#29B6F6',
  },
  {
    id: 3,
    icon: 'MdOutlineSearch',
    title: 'YOLO Vehicle Detection',
    description: 'YOLOv8-powered real-time object detection identifying vehicles, pedestrians, cyclists, and road obstacles with sub-second inference.',
    color: '#AB47BC',
  },
  {
    id: 4,
    icon: 'MdOutlineShield',
    title: 'Risk Classification',
    description: 'Three-tier risk classification system (Low / Moderate / High) powered by ensemble deep learning models with confidence scoring.',
    color: '#FFC107',
  },
  {
    id: 5,
    icon: 'MdOutlineBolt',
    title: 'Real-Time Prediction',
    description: 'Sub-200ms inference pipeline enabling real-time road safety assessments suitable for deployment in live traffic management systems.',
    color: '#FF7043',
  },
  {
    id: 6,
    icon: 'MdOutlineLightbulb',
    title: 'Safety Recommendations',
    description: 'AI-generated actionable safety recommendations based on detected risk factors, helping drivers and traffic operators make better decisions.',
    color: '#26C6DA',
  },
];

// ─── Dummy Prediction Result ───
export const dummyPrediction = {
  risk: 'High Risk',
  riskLevel: 'high',
  confidence: 96.2,
  inferenceTime: '145ms',
  model: 'EfficientNetB0',
  yoloObjects: [
    { label: 'Car', count: 8 },
    { label: 'Truck', count: 3 },
    { label: 'Motorcycle', count: 2 },
    { label: 'Person', count: 1 },
  ],
  trafficDensity: 'Very Heavy',
  weather: 'Rainy',
  roadType: 'Highway',
  possibleCauses: [
    'Excessive vehicle density on a wet highway',
    'Reduced visibility due to rain',
    'Presence of heavy vehicles increasing stopping distance',
    'Low-light conditions reducing driver reaction time',
  ],
  recommendations: [
    'Reduce speed to below 60 km/h immediately',
    'Increase following distance by at least 3x',
    'Activate hazard lights if stopped',
    'Avoid overtaking in wet conditions',
    'Alert traffic management center',
  ],
};

// ─── Workflow Steps ───
export const workflowSteps = [
  { id: 1, label: 'Road Image Input', icon: '🖼️', desc: 'Upload or capture road scene image' },
  { id: 2, label: 'Image Preprocessing', icon: '⚙️', desc: 'Resize, normalize, augment with OpenCV' },
  { id: 3, label: 'YOLOv8 Detection', icon: '🔍', desc: 'Real-time object detection & tracking' },
  { id: 4, label: 'Vehicle Detection', icon: '🚗', desc: 'Classify vehicles, pedestrians, obstacles' },
  { id: 5, label: 'Traffic Density Analysis', icon: '📊', desc: 'Compute density and flow metrics' },
  { id: 6, label: 'CNN / MobileNetV2 / EfficientNetB0', icon: '🧠', desc: 'Deep learning risk feature extraction' },
  { id: 7, label: 'Risk Classification', icon: '⚠️', desc: 'Low / Moderate / High risk scoring' },
  { id: 8, label: 'Safety Recommendation', icon: '💡', desc: 'AI-generated actionable safety advice' },
  { id: 9, label: 'Dashboard Output', icon: '📱', desc: 'Real-time visualization & alerts' },
];
