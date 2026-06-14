from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import warnings
import os
import logging

# Configure robust centralized logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger("cardiopredict-backend")

warnings.filterwarnings('ignore')

app = Flask(__name__)

# Configure production-grade CORS configuration
allowed_origins_env = os.environ.get('ALLOWED_ORIGINS')
if allowed_origins_env:
    allowed_origins = [origin.strip() for origin in allowed_origins_env.split(',') if origin.strip()]
else:
    allowed_origins = [
        'http://localhost:5173', 'http://127.0.0.1:5173',
        'http://localhost:5174', 'http://127.0.0.1:5174',
        'http://localhost:5000', 'http://127.0.0.1:5000'
    ]

CORS(app, resources={
    r"/api/*": {
        "origins": allowed_origins,
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

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

def validate_startup():
    """Fail immediately if model files or required resources are missing on startup"""
    logger.info("Initializing startup checks...")
    
    # 1. Environment Variable Logging
    logger.info(f"CORS Allowed Origins: {allowed_origins}")
    
    # 2. Check for Scaler file
    scaler_path = os.path.join(DATA_DIR, 'scaler.pkl')
    if not os.path.exists(scaler_path):
        scaler_path = os.path.join(MODELS_DIR, 'scaler.pkl')
    if not os.path.exists(scaler_path):
        raise FileNotFoundError(f"CRITICAL: Scaler file missing at {scaler_path}")
        
    # 3. Check for Model files
    required_files = [
        ('logistic_regression.pkl', 'Logistic Regression'),
        ('random_forest.pkl', 'Random Forest'),
        ('knn.pkl', 'KNN'),
        ('svm.pkl', 'SVM'),
        ('xgboost.json', 'XGBoost')
    ]
    for filename, model_name in required_files:
        path = os.path.join(MODELS_DIR, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"CRITICAL: Model file '{filename}' missing for '{model_name}' at {path}")
            
    logger.info("Startup validation successful. All model files and scalers verified.")

@app.route('/')
def home():
    return jsonify({
        "status": "API Running",
        "service": "CardioPredict Backend"
    })

@app.route('/health')
def health():
    """Health check endpoint for Render monitoring"""
    return jsonify({"status": "ok"}), 200

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No request body provided'}), 400
            
        features = data.get('features', [])
        model_name = data.get('model', 'Random Forest')
        
        logger.info(f"Received prediction request for model='{model_name}' with features={features}")

        if len(features) != 13:
            logger.warning(f"Rejected request: got {len(features)} features, exactly 13 required")
            return jsonify({'error': 'Exactly 13 features are required'}), 400

        models = load_models()
        scaler = load_scaler()

        features_array = np.array(features, dtype=float).reshape(1, -1)
        features_scaled = scaler.transform(features_array)

        if model_name not in models:
            logger.warning(f"Requested model '{model_name}' is not supported")
            return jsonify({'error': f"Model '{model_name}' not supported"}), 400

        model = models[model_name]
        prediction = int(model.predict(features_scaled)[0])
        prob_all = model.predict_proba(features_scaled)[0]

        logger.info(f"Successful prediction. Result={prediction}, Confidence={max(prob_all)*100:.2f}%")

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
        logger.exception("Error processing single prediction")
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict/ensemble', methods=['POST'])
def predict_ensemble():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No request body provided'}), 400
            
        features = data.get('features', [])
        logger.info(f"Received ensemble prediction request with features={features}")

        if len(features) != 13:
            logger.warning(f"Rejected ensemble request: got {len(features)} features, exactly 13 required")
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

        logger.info(f"Successful ensemble prediction. Consensus={consensus}, Votes Present={votes_disease}")

        return jsonify({
            'consensus_prediction': consensus,
            'consensus_label': 'Disease Present' if consensus == 1 else 'No Disease',
            'average_confidence': avg_prob * 100,
            'votes_disease': votes_disease,
            'votes_no_disease': 5 - votes_disease,
            'individual_results': results
        })
    except Exception as e:
        logger.exception("Error processing ensemble prediction")
        return jsonify({'error': str(e)}), 500

@app.route('/api/models/performance', methods=['GET'])
def model_performance():
    return jsonify(MODEL_PERFORMANCE)

# Global Flask Error Handler to return structured JSON errors instead of HTML crashes
@app.errorhandler(Exception)
def handle_global_exception(e):
    logger.exception("Global exception handler caught unhandled crash")
    return jsonify({
        'error': 'Internal server error occurred',
        'message': str(e)
    }), 500

if __name__ == '__main__':
    try:
        validate_startup()
        load_models()
        load_scaler()
        logger.info("Pre-loaded models and scaler successfully.")
    except Exception as e:
        logger.critical(f"Flask failed to initialize: {e}")
        os._exit(1)
        
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting API server on port {port}...")
    app.run(host="0.0.0.0", port=port)
