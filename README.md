# CardioPredict - AI-Powered Heart Disease Prediction System

A production-ready web application that predicts heart disease using ensemble machine learning. Built with React, Vite, Tailwind CSS, and Flask.

## 🎯 Overview

CardioPredict uses 5 pre-trained ML models with ensemble voting to deliver accurate, real-time heart disease predictions. The system combines modern web technologies with proven machine learning algorithms for reliable clinical decision support.

**Production Status:** ✅ Ready for Deployment

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Node.js 16+ (development only)

### Installation & Running

```bash
# 1. Install backend dependencies
cd backend
pip install -r requirements.txt

# 2. Start the server
python app.py
```

**Access Application:** http://localhost:5000

## ✨ Features

### Real-time Predictions
- Single model selection from 5 trained algorithms
- 13 clinical features input
- Instant prediction with confidence scores
- Real-time probability visualization

### Ensemble Voting
- All 5 models predict simultaneously
- Majority voting consensus
- Individual model breakdown
- Average confidence calculation

### Performance Analytics
- Compare all model metrics
- Accuracy, Precision, Recall, F1-Score, ROC-AUC
- Interactive dashboard
- Visual performance indicators

## 📊 Model Performance

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|-------|----------|-----------|--------|----------|---------|
| **Random Forest** | **88.52%** | 81.82% | 96.43% | 88.52% | 95.13% |
| Logistic Regression | 86.89% | 81.25% | 92.86% | 86.67% | 95.13% |
| KNN | 88.52% | 80.00% | 100% | 88.89% | 92.32% |
| SVM | 85.25% | 80.65% | 89.29% | 84.75% | 94.37% |
| XGBoost | 85.25% | 78.79% | 92.86% | 85.25% | 91.88% |

**Recommended:** Random Forest (Best accuracy & balanced metrics)

## 🏗️ Architecture

```
backend/           → Flask API + ML Models
├── app.py        → API endpoints
├── models/       → Pre-trained models
├── data/         → Scaler & datasets
└── static/       → Built React app

frontend/         → React App (Pre-built)
└── src/          → Source code
```

## 🔌 API Endpoints

### POST /api/predict
Single model prediction
```json
{
  "features": [64, 1, 3, 145, 212, 0, 0, 157, 0, 0.8, 2, 0, 2],
  "model": "Random Forest"
}
```

### POST /api/predict/ensemble
Ensemble voting
```json
{
  "features": [64, 1, 3, 145, 212, 0, 0, 157, 0, 0.8, 2, 0, 2]
}
```

### GET /api/models/performance
Get all model metrics

## 📋 Clinical Features (13 Variables)

| # | Feature | Range |
|---|---------|-------|
| 1 | Age | Years |
| 2 | Sex | 0=F, 1=M |
| 3 | Chest Pain Type | 0-3 |
| 4 | Resting BP | mmHg |
| 5 | Serum Cholesterol | mg/dl |
| 6 | Fasting Blood Sugar | 0/1 |
| 7 | ECG Results | 0-2 |
| 8 | Max Heart Rate | bpm |
| 9 | Exercise Angina | 0/1 |
| 10 | ST Depression | Value |
| 11 | ST Slope | 0-2 |
| 12 | Major Vessels | 0-3 |
| 13 | Thalassemia | 0-3 |

## 🛠️ Technology Stack

**Frontend:**
- React 18.2
- Vite 5.0
- Tailwind CSS 3.3
- Axios 1.6
- Lucide React

**Backend:**
- Flask
- scikit-learn
- XGBoost
- NumPy & Pandas
- Pickle

## 🚀 Deployment

### Development
```bash
cd backend
python app.py  # http://localhost:5000
```

### Production (Gunicorn)
```bash
cd backend
gunicorn app:app --bind 0.0.0.0:5000
```

Or use: uWSGI, Waitress, Heroku, AWS, Docker, etc.

## 💻 System Requirements

- **CPU:** 2+ cores
- **RAM:** 2GB minimum
- **Storage:** 500MB
- **Network:** Internet connection for dependency downloads

## 📈 Typical Workflow

1. User enters 13 clinical features
2. Frontend sends POST request
3. Backend loads models & scaler
4. Models make predictions
5. Results returned with confidence
6. Frontend displays results with visualization

## ✅ Production Checklist

- [x] All models trained & saved
- [x] Frontend pre-built & optimized
- [x] API endpoints tested
- [x] Error handling implemented
- [x] Security measures in place
- [x] Performance optimized
- [x] UI/UX complete
- [x] Documentation ready

## 🔒 Security Notes

- Input validation on all endpoints
- Model caching for performance
- CORS enabled (configure for production)
- Error handling with user-friendly messages
- No sensitive data logged

## 📝 Configuration

Edit `backend/app.py` for:
- Debug mode (disable for production)
- CORS settings
- Port configuration
- Model loading behavior

## 🎨 UI Features

- Modern gradient dark theme
- Smooth animations & transitions
- Responsive design (desktop & tablet)
- Interactive hover effects
- Real-time result updates
- Confidence visualization
- Model comparison interface

## 📧 Support

Review code comments for implementation details. Check API responses for error messages.

## 📄 License

Ready for educational and commercial use.

---

## Getting Started

```bash
# 1. Install dependencies
cd backend && pip install -r requirements.txt

# 2. Run server
python app.py

# 3. Open browser
# Visit: http://localhost:5000
```

**That's it! Start predicting heart disease in seconds.**

---

**Version:** 1.0.0  
**Status:** Production Ready ✅  
**Last Updated:** 2026-05-11
