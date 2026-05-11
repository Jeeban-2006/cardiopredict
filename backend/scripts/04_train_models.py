import numpy as np
import pandas as pd
import warnings
from typing import Dict, Tuple, Any
warnings.filterwarnings('ignore')

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import pickle

def load_data() -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    X_train = np.load('data/X_train.npy')
    X_test = np.load('data/X_test.npy')
    y_train = np.load('data/y_train.npy')
    y_test = np.load('data/y_test.npy')
    return X_train, X_test, y_train, y_test

def evaluate_model(y_true: np.ndarray, y_pred: np.ndarray, y_pred_proba: Any = None) -> Dict[str, Any]:
    metrics: Dict[str, Any] = {
        'Accuracy': float(accuracy_score(y_true, y_pred)),
        'Precision': float(precision_score(y_true, y_pred)),
        'Recall': float(recall_score(y_true, y_pred)),
        'F1-Score': float(f1_score(y_true, y_pred))
    }
    if y_pred_proba is not None:
        metrics['ROC-AUC'] = float(roc_auc_score(y_true, y_pred_proba))
    return metrics

def train_logistic_regression(X_train: np.ndarray, X_test: np.ndarray, y_train: np.ndarray, y_test: np.ndarray) -> Dict[str, Any]:
    print("\n" + "=" * 60)
    print("1. LOGISTIC REGRESSION")
    print("=" * 60)

    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train, y_train)

    y_pred: np.ndarray = model.predict(X_test)
    y_pred_proba: np.ndarray = model.predict_proba(X_test)
    prob_disease: np.ndarray = y_pred_proba[:, 1]

    metrics = evaluate_model(y_test, y_pred, prob_disease)
    for key, val in metrics.items():
        print(f"{key}: {val:.4f}")

    with open('models/logistic_regression.pkl', 'wb') as f:
        pickle.dump(model, f)

    return metrics

def train_random_forest(X_train: np.ndarray, X_test: np.ndarray, y_train: np.ndarray, y_test: np.ndarray) -> Dict[str, Any]:
    print("\n" + "=" * 60)
    print("2. RANDOM FOREST")
    print("=" * 60)

    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    y_pred: np.ndarray = model.predict(X_test)
    y_pred_proba_all: Any = model.predict_proba(X_test)
    y_pred_proba: np.ndarray = y_pred_proba_all[:, 1]

    metrics = evaluate_model(y_test, y_pred, y_pred_proba)
    for key, val in metrics.items():
        print(f"{key}: {val:.4f}")

    with open('models/random_forest.pkl', 'wb') as f:
        pickle.dump(model, f)

    return metrics

def train_knn(X_train: np.ndarray, X_test: np.ndarray, y_train: np.ndarray, y_test: np.ndarray) -> Dict[str, Any]:
    print("\n" + "=" * 60)
    print("3. K-NEAREST NEIGHBORS (KNN)")
    print("=" * 60)

    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(X_train, y_train)

    y_pred: np.ndarray = model.predict(X_test)
    y_pred_proba_all: Any = model.predict_proba(X_test)
    y_pred_proba: np.ndarray = y_pred_proba_all[:, 1]

    metrics = evaluate_model(y_test, y_pred, y_pred_proba)
    for key, val in metrics.items():
        print(f"{key}: {val:.4f}")

    with open('models/knn.pkl', 'wb') as f:
        pickle.dump(model, f)

    return metrics

def train_xgboost(X_train: np.ndarray, X_test: np.ndarray, y_train: np.ndarray, y_test: np.ndarray) -> Dict[str, Any]:
    print("\n" + "=" * 60)
    print("4. XGBOOST")
    print("=" * 60)

    model = XGBClassifier(n_estimators=100, random_state=42, verbosity=0, use_label_encoder=False)
    model.fit(X_train, y_train)

    y_pred: np.ndarray = model.predict(X_test)
    y_pred_proba_all: Any = model.predict_proba(X_test)
    y_pred_proba: np.ndarray = y_pred_proba_all[:, 1]

    metrics = evaluate_model(y_test, y_pred, y_pred_proba)
    for key, val in metrics.items():
        print(f"{key}: {val:.4f}")

    model.save_model('models/xgboost.json')

    return metrics

def train_support_vector_machine(X_train: np.ndarray, X_test: np.ndarray, y_train: np.ndarray, y_test: np.ndarray) -> Dict[str, Any]:
    print("\n" + "=" * 60)
    print("5. SUPPORT VECTOR MACHINE (SVM)")
    print("=" * 60)

    from sklearn.svm import SVC

    model = SVC(kernel='rbf', probability=True, random_state=42)
    model.fit(X_train, y_train)

    y_pred: np.ndarray = model.predict(X_test)
    y_pred_proba_all: Any = model.predict_proba(X_test)
    y_pred_proba: np.ndarray = y_pred_proba_all[:, 1]

    metrics = evaluate_model(y_test, y_pred, y_pred_proba)
    for key, val in metrics.items():
        print(f"{key}: {val:.4f}")

    with open('models/svm.pkl', 'wb') as f:
        pickle.dump(model, f)

    return metrics

def main() -> None:
    print("=" * 60)
    print("MODEL TRAINING & EVALUATION")
    print("=" * 60)

    X_train, X_test, y_train, y_test = load_data()
    print(f"Training set size: {X_train.shape}")
    print(f"Test set size: {X_test.shape}")

    results: Dict[str, Dict[str, Any]] = {}

    results['Logistic Regression'] = train_logistic_regression(X_train, X_test, y_train, y_test)
    results['Random Forest'] = train_random_forest(X_train, X_test, y_train, y_test)
    results['KNN'] = train_knn(X_train, X_test, y_train, y_test)
    results['XGBoost'] = train_xgboost(X_train, X_test, y_train, y_test)
    results['Support Vector Machine'] = train_support_vector_machine(X_train, X_test, y_train, y_test)

    # Save results
    with open('models/training_results.pkl', 'wb') as f:
        pickle.dump(results, f)

    print("\n" + "=" * 60)
    print("All models trained and saved!")
    print("=" * 60)

if __name__ == "__main__":
    main()
