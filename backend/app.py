from flask import Flask, request, jsonify, send_from_directory, render_template_string
from flask_cors import CORS
import pickle
import numpy as np
import warnings
import os
import json

warnings.filterwarnings('ignore')

app = Flask(__name__)

#Configure CORS using ALLOWED_ORIGINS environment variable
allowed_origins_env = os.environ.get('ALLOWED_ORIGINS')
if allowed_origins_env:
    allowed_origins = [origin.strip() for origin in allowed_origins_env.split(',') if origin.strip()]
else:
    allowed_origins = ['http://localhost:5173', 'http://127.0.0.1:5173']

CORS(app, resources={r"/api/*": {"origins": allowed_origins}})

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, 'models')
DATA_DIR = os.path.join(BASE_DIR, 'data')

models_cache = {}
scaler_cache = None

MODEL_PERFORMANCE = {
    "Logistic Regression": {"accuracy": 0.8689, "precision": 0.8125, "recall": 0.9286, "f1": 0.8667, "roc_auc": 0.9513},
    "Random Forest":       {"accuracy": 0.8852, "precision": 0.8182, "recall": 0.9643, "f1": 0.8852, "roc_auc": 0.9513},
    "KNN":                 {"accuracy": 0.8852, "precision": 0.8000, "recall": 1.0000, "f1": 0.8889, "roc_auc": 0.9232},
    "XGBoost":             {"accuracy": 0.8525, "precision": 0.7879, "recall": 0.9286, "f1": 0.8525, "roc_auc": 0.9188},
    "SVM":                 {"accuracy": 0.8525, "precision": 0.8065, "recall": 0.8929, "f1": 0.8475, "roc_auc": 0.9437},
}

def load_scaler():
    global scaler_cache
    if scaler_cache is None:
        scaler_path = os.path.join(DATA_DIR, 'scaler.pkl')
        if not os.path.exists(scaler_path):
            scaler_path = os.path.join(MODELS_DIR, 'scaler.pkl')
        with open(scaler_path, 'rb') as f:
            scaler_cache = pickle.load(f)
    return scaler_cache

def load_models():
    global models_cache
    if not models_cache:
        with open(os.path.join(MODELS_DIR, 'logistic_regression.pkl'), 'rb') as f:
            models_cache['Logistic Regression'] = pickle.load(f)
        with open(os.path.join(MODELS_DIR, 'random_forest.pkl'), 'rb') as f:
            models_cache['Random Forest'] = pickle.load(f)
        with open(os.path.join(MODELS_DIR, 'knn.pkl'), 'rb') as f:
            models_cache['KNN'] = pickle.load(f)
        with open(os.path.join(MODELS_DIR, 'svm.pkl'), 'rb') as f:
            models_cache['SVM'] = pickle.load(f)
        import xgboost as xgb
        xgb_model = xgb.XGBClassifier()
        xgb_model.load_model(os.path.join(MODELS_DIR, 'xgboost.json'))
        models_cache['XGBoost'] = xgb_model
    return models_cache

@app.route('/')
def home():
    return jsonify({
        "status": "API Running"
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        features = data.get('features', [])
        model_name = data.get('model', 'Random Forest')

        if len(features) != 13:
            return jsonify({'error': 'Exactly 13 features are required'}), 400

        models = load_models()
        scaler = load_scaler()

        features_array = np.array(features, dtype=float).reshape(1, -1)
        features_scaled = scaler.transform(features_array)

        model = models[model_name]
        prediction = int(model.predict(features_scaled)[0])
        prob_all = model.predict_proba(features_scaled)[0]

        return jsonify({
            'model': model_name,
            'prediction': prediction,
            'label': 'Disease Present' if prediction == 1 else 'No Disease',
            'probability_no_disease': float(prob_all[0]),
            'probability_disease': float(prob_all[1]),
            'confidence': float(max(prob_all) * 100),
            'performance': MODEL_PERFORMANCE.get(model_name, {})
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict/ensemble', methods=['POST'])
def predict_ensemble():
    try:
        data = request.get_json()
        features = data.get('features', [])

        if len(features) != 13:
            return jsonify({'error': 'Exactly 13 features are required'}), 400

        models = load_models()
        scaler = load_scaler()

        features_array = np.array(features, dtype=float).reshape(1, -1)
        features_scaled = scaler.transform(features_array)

        results = {}
        predictions = []
        probabilities = []

        for name, model in models.items():
            pred = int(model.predict(features_scaled)[0])
            prob_all = model.predict_proba(features_scaled)[0]
            prob_disease = float(prob_all[1])
            predictions.append(pred)
            probabilities.append(prob_disease)
            results[name] = {
                'prediction': pred,
                'probability_disease': prob_disease,
                'probability_no_disease': float(prob_all[0]),
                'confidence': float(max(prob_all) * 100)
            }

        votes_disease = sum(predictions)
        consensus = 1 if votes_disease >= 3 else 0
        avg_prob = float(np.mean(probabilities))

        return jsonify({
            'consensus_prediction': consensus,
            'consensus_label': 'Disease Present' if consensus == 1 else 'No Disease',
            'average_confidence': avg_prob * 100,
            'votes_disease': votes_disease,
            'votes_no_disease': 5 - votes_disease,
            'individual_results': results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/models/performance', methods=['GET'])
def model_performance():
    return jsonify(MODEL_PERFORMANCE)

# @app.errorhandler(404)
# def not_found(e):
#     return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    print("Starting Heart Disease Prediction API...")
    print("Loading models...")
    try:
        load_models()
        load_scaler()
        print("Models loaded successfully!")
    except Exception as e:
        print(f"Warning: Could not pre-load models: {e}")
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT", 10000)))
