import pickle
import numpy as np
import pandas as pd
import warnings
from typing import Any, Dict, List
warnings.filterwarnings('ignore')

def load_models() -> Dict[str, Any]:
    models: Dict[str, Any] = {}
    with open('models/logistic_regression.pkl', 'rb') as f:
        models['Logistic Regression'] = pickle.load(f)
    with open('models/random_forest.pkl', 'rb') as f:
        models['Random Forest'] = pickle.load(f)
    with open('models/knn.pkl', 'rb') as f:
        models['KNN'] = pickle.load(f)
    with open('models/svm.pkl', 'rb') as f:
        models['SVM'] = pickle.load(f)

    models['XGBoost'] = __import__('xgboost').XGBClassifier()
    models['XGBoost'].load_model('models/xgboost.json')

    return models

def load_scaler() -> Any:
    with open('data/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    return scaler

def predict_disease(features: List[float], model_name: str = 'Random Forest') -> Dict[str, Any]:
    """
    Predict heart disease for a patient.

    Features (13 clinical indicators):
    age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal
    """
    models = load_models()
    scaler = load_scaler()

    models = load_models()
    scaler = load_scaler()

    features_scaled: np.ndarray = scaler.transform([features])
    model = models[model_name]
    prediction: int = int(model.predict(features_scaled)[0])
    probability_all: Any = model.predict_proba(features_scaled)[0]

    result: Dict[str, Any] = {
        'model': model_name,
        'prediction': 'Disease Present' if prediction == 1 else 'No Disease',
        'probability_no_disease': float(probability_all[0]),
        'probability_disease': float(probability_all[1]),
        'confidence': float(max(probability_all) * 100)
    }

    return result

def ensemble_predict(features: List[float]) -> Dict[str, Any]:
    """
    Make predictions using all models and return consensus.
    """
    models = load_models()
    scaler = load_scaler()

    features_scaled: np.ndarray = scaler.transform([features])

    predictions: List[int] = []
    probabilities: List[float] = []

    for name, model in models.items():
        pred: int = int(model.predict(features_scaled)[0])
        prob_array: Any = model.predict_proba(features_scaled)[0]
        prob: float = float(prob_array[1])
        predictions.append(pred)
        probabilities.append(prob)

    consensus: int = 1 if sum(predictions) >= 3 else 0
    avg_probability: float = float(np.mean(probabilities))

    return {
        'consensus_prediction': 'Disease Present' if consensus == 1 else 'No Disease',
        'average_confidence': float(avg_probability * 100),
        'individual_probabilities': {
            name: float(prob * 100) for name, prob in zip(models.keys(), probabilities)
        }
    }

def demo_predictions():
    print("=" * 60)
    print("HEART DISEASE PREDICTION - DEMO")
    print("=" * 60)

    # Example patient data (scaled features)
    example_features = [
        63, 1, 1, 145, 233, 1, 2, 150, 0, 2.3, 3, 0, 6,  # Patient 1: High risk
        37, 1, 3, 130, 250, 0, 1, 187, 0, 3.5, 3, 0, 3   # Patient 2: Low risk
    ]

    patient_1 = example_features[:13]
    patient_2 = example_features[13:]

    scaler = load_scaler()

    print("\nPATIENT 1 - HIGH RISK PROFILE:")
    print(f"Raw features: {patient_1}")

    result = predict_disease(patient_1, 'Random Forest')
    print(f"\nRandom Forest Prediction:")
    print(f"  Result: {result['prediction']}")
    print(f"  Confidence: {result['confidence']:.2f}%")
    print(f"  No Disease Probability: {result['probability_no_disease']:.4f}")
    print(f"  Disease Probability: {result['probability_disease']:.4f}")

    ensemble = ensemble_predict(patient_1)
    print(f"\nEnsemble Prediction (All 5 Models):")
    print(f"  Consensus: {ensemble['consensus_prediction']}")
    print(f"  Average Confidence: {ensemble['average_confidence']:.2f}%")
    print(f"  Individual Model Probabilities:")
    for model, prob in ensemble['individual_probabilities'].items():
        print(f"    {model}: {prob:.2f}%")

    print("\n" + "-" * 60)
    print("\nPATIENT 2 - LOW RISK PROFILE:")
    print(f"Raw features: {patient_2}")

    result = predict_disease(patient_2, 'Random Forest')
    print(f"\nRandom Forest Prediction:")
    print(f"  Result: {result['prediction']}")
    print(f"  Confidence: {result['confidence']:.2f}%")
    print(f"  No Disease Probability: {result['probability_no_disease']:.4f}")
    print(f"  Disease Probability: {result['probability_disease']:.4f}")

    ensemble = ensemble_predict(patient_2)
    print(f"\nEnsemble Prediction (All 5 Models):")
    print(f"  Consensus: {ensemble['consensus_prediction']}")
    print(f"  Average Confidence: {ensemble['average_confidence']:.2f}%")
    print(f"  Individual Model Probabilities:")
    for model, prob in ensemble['individual_probabilities'].items():
        print(f"    {model}: {prob:.2f}%")

if __name__ == "__main__":
    demo_predictions()
