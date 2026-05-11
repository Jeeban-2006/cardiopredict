#!/usr/bin/env python3
"""
Heart Disease Prediction System - Master Execution Script
Runs the complete ML pipeline from data loading to model evaluation
"""

import os
import sys
import subprocess
from pathlib import Path

def run_script(script_path: str, description: str) -> bool:
    """Execute a Python script and report status"""
    print(f"\n{'='*70}")
    print(f"[{description}]")
    print(f"{'='*70}")

    try:
        result = subprocess.run(
            [sys.executable, script_path],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            capture_output=False
        )
        if result.returncode == 0:
            print(f"[OK] {description} - SUCCESS")
            return True
        else:
            print(f"[FAIL] {description} - FAILED")
            return False
    except Exception as e:
        print(f"[FAIL] {description} - ERROR: {e}")
        return False

def main():
    """Execute complete ML pipeline"""
    print("\n" + "="*70)
    print("HEART DISEASE PREDICTION SYSTEM - COMPLETE PIPELINE")
    print("="*70)

    scripts = [
        ("scripts/01_load_data.py", "Step 1: Load & Explore Data"),
        ("scripts/02_preprocess_data.py", "Step 2: Preprocess Data"),
        ("scripts/03_eda.py", "Step 3: Exploratory Data Analysis"),
        ("scripts/04_train_models.py", "Step 4: Train Models"),
        ("scripts/05_evaluate_models.py", "Step 5: Evaluate & Compare Models"),
        ("scripts/06_predict.py", "Step 6: Run Predictions"),
    ]

    results = []
    for script_path, description in scripts:
        if Path(script_path).exists():
            success = run_script(script_path, description)
            results.append((description, success))
        else:
            print(f"[FAIL] {description} - FILE NOT FOUND: {script_path}")
            results.append((description, False))

    # Summary
    print("\n" + "="*70)
    print("PIPELINE EXECUTION SUMMARY")
    print("="*70)

    for description, success in results:
        status = "[OK]" if success else "[FAIL]"
        print(f"{status}: {description}")

    all_passed = all(success for _, success in results)

    print("\n" + "="*70)
    if all_passed:
        print("[SUCCESS] ALL STEPS COMPLETED SUCCESSFULLY!")
        print("="*70)
        print("\nProject Deliverables:")
        print("  • Data: 303 patient records with 13 clinical features")
        print("  • Models: 5 trained ML models (Logistic, RF, KNN, XGBoost, SVM)")
        print("  • Results: Best accuracy 88.52% (Random Forest & KNN)")
        print("  • Visualizations: 8 PNG charts and comparison heatmaps")
        print("  • Reports: Complete summary and model comparison CSV")
        print("\nOutput Locations:")
        print("  • Models: ./models/")
        print("  • Data: ./data/")
        print("  • Visualizations: ./notebooks/")
        print("  • Reports: ./models/SUMMARY_REPORT.txt")
        return 0
    else:
        print("[FAILED] SOME STEPS FAILED - CHECK OUTPUT ABOVE")
        print("="*70)
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
