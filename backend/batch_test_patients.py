#!/usr/bin/env python3
"""
Batch Patient Testing Tool
Test multiple patients and generate summary report
"""

import csv
import pickle
import numpy as np
from datetime import datetime
from typing import List, Dict, Any

def load_models_and_scaler():
    """Load all trained models and scaler"""
    models = {}
    with open('models/logistic_regression.pkl', 'rb') as f:
        models['Logistic Regression'] = pickle.load(f)
    with open('models/random_forest.pkl', 'rb') as f:
        models['Random Forest'] = pickle.load(f)
    with open('models/knn.pkl', 'rb') as f:
        models['KNN'] = pickle.load(f)
    with open('models/svm.pkl', 'rb') as f:
        models['SVM'] = pickle.load(f)

    import xgboost
    xgb = xgboost.XGBClassifier()
    xgb.load_model('models/xgboost.json')
    models['XGBoost'] = xgb

    with open('data/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)

    return models, scaler

def test_patient(patient_data: List[float], models: Dict, scaler) -> Dict[str, Any]:
    """Test single patient"""
    patient_scaled = scaler.transform([patient_data])

    predictions = []
    probabilities = []

    for model in models.values():
        pred = int(model.predict(patient_scaled)[0])
        prob = float(model.predict_proba(patient_scaled)[0][1])
        predictions.append(pred)
        probabilities.append(prob)

    consensus = 1 if sum(predictions) >= 3 else 0
    avg_prob = np.mean(probabilities)

    if avg_prob >= 0.7:
        risk = "HIGH"
    elif avg_prob >= 0.4:
        risk = "MODERATE"
    else:
        risk = "LOW"

    return {
        'consensus': "DISEASE" if consensus == 1 else "NO DISEASE",
        'probability': avg_prob,
        'confidence': avg_prob * 100,
        'risk_level': risk
    }

def test_from_csv(filename: str) -> None:
    """Test patients from CSV file"""
    print(f"\nLoading patients from {filename}...")

    models, scaler = load_models_and_scaler()
    results = []

    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)  # Skip header

            for i, row in enumerate(reader, 1):
                try:
                    patient_data = [float(x) for x in row[1:]]  # Skip patient ID
                    patient_id = row[0]

                    result = test_patient(patient_data, models, scaler)
                    result['patient_id'] = patient_id
                    result['patient_index'] = i
                    results.append(result)

                    print(f"  Patient {i}: {result['consensus']} ({result['confidence']:.1f}%) - {result['risk_level']}")

                except (ValueError, IndexError) as e:
                    print(f"  Error processing patient {i}: {e}")

    except FileNotFoundError:
        print(f"Error: File {filename} not found")
        return

    # Generate report
    generate_batch_report(results)

def generate_batch_report(results: List[Dict]) -> None:
    """Generate batch testing report"""
    print("\n" + "="*70)
    print("BATCH TESTING SUMMARY REPORT")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total Patients: {len(results)}")
    print("="*70)

    # Risk distribution
    high_risk = sum(1 for r in results if r['risk_level'] == 'HIGH')
    moderate_risk = sum(1 for r in results if r['risk_level'] == 'MODERATE')
    low_risk = sum(1 for r in results if r['risk_level'] == 'LOW')

    disease_predicted = sum(1 for r in results if r['consensus'] == 'DISEASE')
    no_disease_predicted = sum(1 for r in results if r['consensus'] == 'NO DISEASE')

    print("\nRISK DISTRIBUTION:")
    print(f"  HIGH RISK:     {high_risk:3d} ({high_risk/len(results)*100:5.1f}%)")
    print(f"  MODERATE RISK: {moderate_risk:3d} ({moderate_risk/len(results)*100:5.1f}%)")
    print(f"  LOW RISK:      {low_risk:3d} ({low_risk/len(results)*100:5.1f}%)")

    print("\nPREDICTION DISTRIBUTION:")
    print(f"  DISEASE PRESENT:  {disease_predicted:3d} ({disease_predicted/len(results)*100:5.1f}%)")
    print(f"  NO DISEASE:       {no_disease_predicted:3d} ({no_disease_predicted/len(results)*100:5.1f}%)")

    # Statistics
    probabilities = [r['probability'] for r in results]
    print("\nPROBABILITY STATISTICS:")
    print(f"  Mean:   {np.mean(probabilities):.4f}")
    print(f"  Median: {np.median(probabilities):.4f}")
    print(f"  Std:    {np.std(probabilities):.4f}")
    print(f"  Min:    {min(probabilities):.4f}")
    print(f"  Max:    {max(probabilities):.4f}")

    # Top high risk patients
    print("\nTOP 5 HIGHEST RISK PATIENTS:")
    sorted_results = sorted(results, key=lambda x: x['probability'], reverse=True)
    for i, r in enumerate(sorted_results[:5], 1):
        print(f"  {i}. Patient {r['patient_id']}: {r['probability']:.4f} ({r['confidence']:.1f}%)")

    # Save detailed report
    report_filename = f"batch_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_filename, 'w') as f:
        f.write("BATCH TESTING SUMMARY REPORT\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Patients: {len(results)}\n\n")

        f.write("RISK DISTRIBUTION:\n")
        f.write(f"  HIGH RISK:     {high_risk:3d} ({high_risk/len(results)*100:5.1f}%)\n")
        f.write(f"  MODERATE RISK: {moderate_risk:3d} ({moderate_risk/len(results)*100:5.1f}%)\n")
        f.write(f"  LOW RISK:      {low_risk:3d} ({low_risk/len(results)*100:5.1f}%)\n\n")

        f.write("DETAILED RESULTS:\n")
        f.write("Patient_ID,Prediction,Probability,Confidence,Risk_Level\n")
        for r in sorted_results:
            f.write(f"{r['patient_id']},{r['consensus']},{r['probability']:.4f},"
                   f"{r['confidence']:.2f}%,{r['risk_level']}\n")

    print(f"\nDetailed report saved: {report_filename}")

def create_sample_csv() -> str:
    """Create sample CSV for testing"""
    filename = "sample_patients.csv"

    sample_data = [
        ["patient_id", "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
         "thalach", "exang", "oldpeak", "slope", "ca", "thal"],
        ["P001", "63", "1", "1", "145", "233", "1", "2", "150", "0", "2.3", "3", "0", "6"],
        ["P002", "57", "1", "0", "130", "236", "0", "2", "174", "0", "0", "1", "1", "3"],
        ["P003", "40", "0", "0", "120", "200", "0", "2", "160", "0", "0", "1", "0", "3"],
        ["P004", "75", "1", "4", "160", "286", "0", "2", "108", "1", "1.5", "2", "3", "7"],
        ["P005", "28", "1", "0", "110", "180", "0", "0", "190", "0", "0", "1", "0", "3"],
        ["P006", "52", "0", "3", "125", "212", "0", "1", "168", "0", "1", "2", "2", "3"],
        ["P007", "65", "1", "1", "130", "254", "0", "0", "147", "0", "1.4", "1", "3", "7"],
        ["P008", "45", "1", "2", "110", "264", "0", "1", "132", "0", "1.2", "1", "0", "3"],
        ["P009", "55", "0", "0", "128", "245", "0", "1", "160", "0", "0.5", "1", "0", "3"],
        ["P010", "70", "1", "3", "145", "270", "1", "2", "120", "1", "2", "2", "2", "3"],
    ]

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(sample_data)

    print(f"Sample CSV created: {filename}")
    return filename

def main():
    """Main function"""
    import os

    if not os.path.exists('models/random_forest.pkl'):
        print("Error: Models not found. Run pipeline first.")
        return

    print("\n" + "="*70)
    print("BATCH PATIENT TESTING TOOL")
    print("="*70)
    print("\n1. Test sample patients (creates demo CSV)")
    print("2. Test from custom CSV file")
    print("3. Exit")

    choice = input("\nSelect option (1-3): ").strip()

    if choice == '1':
        filename = create_sample_csv()
        test_from_csv(filename)

    elif choice == '2':
        filename = input("Enter CSV filename: ").strip()
        test_from_csv(filename)

    elif choice == '3':
        print("Exiting...")

    else:
        print("Invalid option")

if __name__ == "__main__":
    main()
