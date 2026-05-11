#!/usr/bin/env python3
"""
Interactive Heart Disease Prediction Test Tool
Test the trained models with real patient data
"""

import pickle
import numpy as np
from typing import List, Dict, Any
import sys

def load_models() -> Dict[str, Any]:
    """Load all trained models"""
    models = {}
    try:
        with open('models/logistic_regression.pkl', 'rb') as f:
            models['Logistic Regression'] = pickle.load(f)
        with open('models/random_forest.pkl', 'rb') as f:
            models['Random Forest'] = pickle.load(f)
        with open('models/knn.pkl', 'rb') as f:
            models['KNN'] = pickle.load(f)
        with open('models/svm.pkl', 'rb') as f:
            models['SVM'] = pickle.load(f)

        import xgboost
        models['XGBoost'] = xgboost.XGBClassifier()
        models['XGBoost'].load_model('models/xgboost.json')

        return models
    except Exception as e:
        print(f"Error loading models: {e}")
        sys.exit(1)

def load_scaler():
    """Load feature scaler"""
    with open('data/scaler.pkl', 'rb') as f:
        return pickle.load(f)

def get_patient_data() -> List[float]:
    """Get patient data from user input"""
    print("\n" + "="*70)
    print("ENTER PATIENT DATA (13 CLINICAL INDICATORS)")
    print("="*70)

    features = []
    feature_names = [
        'Age (years)',
        'Sex (0=Female, 1=Male)',
        'Chest Pain Type (1-4)',
        'Resting Blood Pressure (mmHg)',
        'Serum Cholesterol (mg/dl)',
        'Fasting Blood Sugar >120 (0=No, 1=Yes)',
        'Resting ECG (0-2)',
        'Max Heart Rate Achieved (bpm)',
        'Exercise Induced Angina (0=No, 1=Yes)',
        'ST Depression (0-6.2)',
        'ST Slope (1-3)',
        'Number of Major Vessels (0-3)',
        'Thalassemia (3-7)'
    ]

    for i, name in enumerate(feature_names, 1):
        while True:
            try:
                value = float(input(f"{i}. {name}: "))
                features.append(value)
                break
            except ValueError:
                print("   Please enter a valid number")

    return features

def predict_with_patient_data(patient_data: List[float]) -> Dict[str, Any]:
    """Make predictions for patient data"""
    models = load_models()
    scaler = load_scaler()

    # Scale features
    patient_scaled = scaler.transform([patient_data])

    results = {
        'patient_data': patient_data,
        'individual_predictions': {},
        'consensus': None,
        'risk_level': None
    }

    predictions = []
    probabilities = []

    print("\n" + "="*70)
    print("MODEL PREDICTIONS")
    print("="*70)

    for model_name, model in models.items():
        pred = int(model.predict(patient_scaled)[0])
        prob_array = model.predict_proba(patient_scaled)[0]
        prob_disease = float(prob_array[1])

        predictions.append(pred)
        probabilities.append(prob_disease)

        result_text = "DISEASE PRESENT" if pred == 1 else "NO DISEASE"
        confidence = prob_disease * 100

        results['individual_predictions'][model_name] = {
            'prediction': result_text,
            'disease_probability': prob_disease,
            'confidence': confidence
        }

        print(f"\n{model_name}:")
        print(f"  Prediction: {result_text}")
        print(f"  Disease Probability: {prob_disease:.4f}")
        print(f"  Confidence: {confidence:.2f}%")

    # Consensus prediction
    consensus = 1 if sum(predictions) >= 3 else 0
    avg_probability = np.mean(probabilities)

    results['consensus'] = "DISEASE PRESENT" if consensus == 1 else "NO DISEASE"
    results['consensus_probability'] = avg_probability
    results['consensus_confidence'] = avg_probability * 100

    # Risk level
    if avg_probability >= 0.7:
        results['risk_level'] = "HIGH RISK"
    elif avg_probability >= 0.4:
        results['risk_level'] = "MODERATE RISK"
    else:
        results['risk_level'] = "LOW RISK"

    return results

def print_detailed_report(results: Dict[str, Any]) -> None:
    """Print detailed patient report"""
    print("\n" + "="*70)
    print("PATIENT REPORT - CONSENSUS PREDICTION")
    print("="*70)

    print(f"\nConsensus Prediction: {results['consensus']}")
    print(f"Disease Probability: {results['consensus_probability']:.4f}")
    print(f"Confidence Level: {results['consensus_confidence']:.2f}%")
    print(f"Risk Level: {results['risk_level']}")

    print("\n" + "="*70)
    print("INDIVIDUAL MODEL BREAKDOWN")
    print("="*70)

    for model_name, pred in results['individual_predictions'].items():
        print(f"\n{model_name}:")
        print(f"  Result: {pred['prediction']}")
        print(f"  Probability: {pred['disease_probability']:.4f}")
        print(f"  Confidence: {pred['confidence']:.2f}%")

    print("\n" + "="*70)
    print("CLINICAL RECOMMENDATIONS")
    print("="*70)

    if results['risk_level'] == "HIGH RISK":
        print("""
RECOMMENDATION: IMMEDIATE MEDICAL CONSULTATION REQUIRED
- Urgent cardiology evaluation recommended
- Consider advanced testing (ECG, stress test, angiography)
- Hospital admission may be necessary
- Monitor vital signs continuously
        """)
    elif results['risk_level'] == "MODERATE RISK":
        print("""
RECOMMENDATION: MEDICAL CONSULTATION WITHIN 1-2 WEEKS
- Schedule cardiology appointment
- Perform non-invasive tests (ECG, echocardiogram)
- Lifestyle modifications recommended
- Regular monitoring advised
        """)
    else:
        print("""
RECOMMENDATION: ROUTINE CHECK-UP RECOMMENDED
- Annual cardiac screening
- Maintain healthy lifestyle
- Continue regular exercise
- Monitor risk factors periodically
        """)

def save_patient_record(results: Dict[str, Any]) -> None:
    """Save patient record to file"""
    from datetime import datetime

    filename = f"patient_records_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    with open(filename, 'w') as f:
        f.write("="*70 + "\n")
        f.write("HEART DISEASE PREDICTION - PATIENT RECORD\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*70 + "\n\n")

        feature_names = [
            'Age', 'Sex', 'Chest Pain Type', 'Resting BP', 'Cholesterol',
            'Fasting BS', 'Resting ECG', 'Max Heart Rate', 'Exercise Angina',
            'ST Depression', 'ST Slope', 'Major Vessels', 'Thalassemia'
        ]

        f.write("PATIENT DATA:\n")
        for name, value in zip(feature_names, results['patient_data']):
            f.write(f"  {name}: {value}\n")

        f.write(f"\nCONSENSUS PREDICTION: {results['consensus']}\n")
        f.write(f"Disease Probability: {results['consensus_probability']:.4f}\n")
        f.write(f"Confidence: {results['consensus_confidence']:.2f}%\n")
        f.write(f"Risk Level: {results['risk_level']}\n")

        f.write("\nINDIVIDUAL PREDICTIONS:\n")
        for model_name, pred in results['individual_predictions'].items():
            f.write(f"  {model_name}: {pred['prediction']} ")
            f.write(f"({pred['confidence']:.2f}%)\n")

    print(f"\nPatient record saved: {filename}")

def test_with_examples() -> None:
    """Test with realistic example patients"""
    print("\n" + "="*70)
    print("TESTING WITH EXAMPLE PATIENTS")
    print("="*70)

    # Example patients
    examples = {
        "Patient 1 - HIGH RISK (63-year-old male)": [63, 1, 1, 145, 233, 1, 2, 150, 0, 2.3, 3, 0, 6],
        "Patient 2 - MODERATE RISK (57-year-old male)": [57, 1, 0, 130, 236, 0, 2, 174, 0, 0, 1, 1, 3],
        "Patient 3 - LOW RISK (40-year-old female)": [40, 0, 0, 120, 200, 0, 2, 160, 0, 0, 1, 0, 3],
        "Patient 4 - MODERATE RISK (45-year-old male)": [45, 1, 1, 110, 264, 0, 1, 132, 0, 1.2, 1, 0, 3],
        "Patient 5 - HIGH RISK (70-year-old male)": [70, 1, 4, 160, 286, 0, 2, 108, 1, 1.5, 2, 3, 3],
    }

    for patient_name, patient_data in examples.items():
        print(f"\n{'='*70}")
        print(f"Testing: {patient_name}")
        print(f"{'='*70}")

        results = predict_with_patient_data(patient_data)
        print_detailed_report(results)

def interactive_mode() -> None:
    """Interactive mode for testing"""
    while True:
        print("\n" + "="*70)
        print("HEART DISEASE PREDICTION - INTERACTIVE TEST")
        print("="*70)
        print("\n1. Test with manual patient data")
        print("2. Test with example patients")
        print("3. View feature descriptions")
        print("4. Exit")

        choice = input("\nSelect option (1-4): ").strip()

        if choice == '1':
            patient_data = get_patient_data()
            results = predict_with_patient_data(patient_data)
            print_detailed_report(results)

            save = input("\nSave patient record? (y/n): ").strip().lower()
            if save == 'y':
                save_patient_record(results)

        elif choice == '2':
            test_with_examples()

        elif choice == '3':
            print_feature_descriptions()

        elif choice == '4':
            print("\nExiting...")
            break

        else:
            print("Invalid option. Please try again.")

def print_feature_descriptions() -> None:
    """Print detailed feature descriptions"""
    print("\n" + "="*70)
    print("FEATURE DESCRIPTIONS & NORMAL RANGES")
    print("="*70)

    descriptions = {
        "Age": "Patient age in years | Normal: 20-80",
        "Sex": "Gender (0=Female, 1=Male)",
        "Chest Pain Type": "1=Typical, 2=Atypical, 3=Non-anginal, 4=Asymptomatic",
        "Resting BP": "Blood pressure at rest in mmHg | Normal: 90-120",
        "Cholesterol": "Serum cholesterol in mg/dl | Desirable: <200",
        "Fasting BS": "Fasting blood sugar >120 mg/dl | 0=No, 1=Yes",
        "Resting ECG": "0=Normal, 1=ST-T abnormality, 2=LV hypertrophy",
        "Max Heart Rate": "Maximum heart rate achieved during exercise | Normal: 60-100 at rest",
        "Exercise Angina": "Angina induced by exercise | 0=No, 1=Yes",
        "ST Depression": "ST segment depression induced by exercise | Normal: 0-1",
        "ST Slope": "1=Upsloping, 2=Flat, 3=Downsloping",
        "Major Vessels": "Number of major vessels colored by fluoroscopy | Normal: 0",
        "Thalassemia": "Blood disorder | 3=Normal, 4=Fixed, 5=Reversible, 6-7=Other",
    }

    for feature, description in descriptions.items():
        print(f"\n{feature}:")
        print(f"  {description}")

def main():
    """Main function"""
    import os

    # Check if models exist
    if not os.path.exists('models/random_forest.pkl'):
        print("Error: Models not found. Please run the full pipeline first.")
        print("Run: python run_pipeline.py")
        sys.exit(1)

    interactive_mode()

if __name__ == "__main__":
    main()
