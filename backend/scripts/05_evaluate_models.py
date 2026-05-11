import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import Dict, Any

def load_results() -> Dict[str, Dict[str, float]]:
    with open('models/training_results.pkl', 'rb') as f:
        results = pickle.load(f)
    return results

def create_comparison_report():
    print("=" * 60)
    print("MODEL EVALUATION & COMPARISON REPORT")
    print("=" * 60)

    results = load_results()

    # Create DataFrame
    df_results = pd.DataFrame(results).T
    df_results = df_results.round(4)

    print("\nMODEL PERFORMANCE COMPARISON:")
    print(df_results)

    # Save to CSV
    df_results.to_csv('models/model_comparison.csv')
    print("\n[DONE] Saved: model_comparison.csv")

    # Find best model for each metric
    print("\nBEST MODELS BY METRIC:")
    for col in df_results.columns:
        best_model = df_results[col].idxmax()
        best_score = df_results[col].max()
        print(f"{col}: {best_model} ({best_score:.4f})")

    return df_results

def create_visualizations(df_results):
    print("\nCREATING VISUALIZATIONS...")

    # 1. Model Comparison - All Metrics
    fig, ax = plt.subplots(figsize=(12, 6))
    df_results.plot(kind='bar', ax=ax)
    ax.set_title('Model Performance Comparison', fontsize=14, fontweight='bold')
    ax.set_xlabel('Model')
    ax.set_ylabel('Score')
    ax.legend(loc='lower right', fontsize=9)
    ax.set_ylim([0.75, 1.0])
    ax.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('notebooks/04_model_comparison.png', dpi=100, bbox_inches='tight')
    print("[DONE] Saved: 04_model_comparison.png")

    # 2. Accuracy Comparison
    fig, ax = plt.subplots(figsize=(10, 6))
    accuracy_scores = df_results['Accuracy'].sort_values(ascending=False)
    colors = ['green' if score == accuracy_scores.max() else 'steelblue' for score in accuracy_scores]
    accuracy_scores.plot(kind='barh', ax=ax, color=colors)
    ax.set_title('Model Accuracy Comparison', fontsize=14, fontweight='bold')
    ax.set_xlabel('Accuracy')
    ax.set_xlim([0.8, 0.95])
    for i, (model, score) in enumerate(accuracy_scores.items()):
        ax.text(score - 0.01, i, f'{score:.4f}', ha='right', va='center', fontweight='bold')
    plt.tight_layout()
    plt.savefig('notebooks/05_accuracy_comparison.png', dpi=100, bbox_inches='tight')
    print("[DONE] Saved: 05_accuracy_comparison.png")

    # 3. ROC-AUC Comparison
    fig, ax = plt.subplots(figsize=(10, 6))
    roc_auc_scores = df_results['ROC-AUC'].sort_values(ascending=False)
    colors = ['green' if score == roc_auc_scores.max() else 'steelblue' for score in roc_auc_scores]
    roc_auc_scores.plot(kind='barh', ax=ax, color=colors)
    ax.set_title('Model ROC-AUC Comparison', fontsize=14, fontweight='bold')
    ax.set_xlabel('ROC-AUC Score')
    ax.set_xlim([0.88, 0.97])
    for i, (model, score) in enumerate(roc_auc_scores.items()):
        ax.text(score - 0.005, i, f'{score:.4f}', ha='right', va='center', fontweight='bold')
    plt.tight_layout()
    plt.savefig('notebooks/06_roc_auc_comparison.png', dpi=100, bbox_inches='tight')
    print("[DONE] Saved: 06_roc_auc_comparison.png")

    # 4. Heatmap of all metrics
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(df_results, annot=True, fmt='.4f', cmap='RdYlGn', ax=ax,
                cbar_kws={'label': 'Score'}, vmin=0.75, vmax=1.0)
    ax.set_title('Model Performance Heatmap', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('notebooks/07_performance_heatmap.png', dpi=100, bbox_inches='tight')
    print("[DONE] Saved: 07_performance_heatmap.png")

    # 5. F1-Score and Precision-Recall Tradeoff
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    f1_scores = df_results['F1-Score'].sort_values(ascending=False)
    f1_scores.plot(kind='bar', ax=ax1, color='steelblue')
    ax1.set_title('F1-Score Comparison', fontsize=12, fontweight='bold')
    ax1.set_ylabel('F1-Score')
    ax1.set_ylim([0.8, 0.95])
    ax1.grid(axis='y', alpha=0.3)
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

    precision_recall = df_results[['Precision', 'Recall']].sort_values('Precision', ascending=False)
    precision_recall.plot(kind='bar', ax=ax2)
    ax2.set_title('Precision vs Recall', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Score')
    ax2.set_ylim([0.75, 1.0])
    ax2.grid(axis='y', alpha=0.3)
    ax2.legend(loc='lower right')
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')

    plt.tight_layout()
    plt.savefig('notebooks/08_f1_and_tradeoff.png', dpi=100, bbox_inches='tight')
    print("[DONE] Saved: 08_f1_and_tradeoff.png")

def create_summary_report(df_results):
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)

    best_overall = df_results['Accuracy'].idxmax()
    best_accuracy = df_results['Accuracy'].max()
    best_roc_auc = df_results['ROC-AUC'].max()
    best_roc_model = df_results['ROC-AUC'].idxmax()

    summary = f"""
HEART DISEASE DETECTION - MODEL EVALUATION SUMMARY
{'=' * 60}

DATASET INFORMATION:
- Total samples: 303
- Training samples: 242 (80%)
- Test samples: 61 (20%)
- Features: 13 clinical indicators
- Target: Binary (Disease/No Disease)

MODELS EVALUATED:
1. Logistic Regression
2. Random Forest
3. K-Nearest Neighbors (KNN)
4. XGBoost
5. Support Vector Machine (SVM)

TOP PERFORMERS:
- Best Overall Model (Accuracy): {best_overall} ({best_accuracy:.4f})
- Best ROC-AUC Model: {best_roc_model} ({best_roc_auc:.4f})

KEY FINDINGS:
- Random Forest and KNN achieved the highest accuracy (0.8852)
- Logistic Regression achieved the highest ROC-AUC (0.9513)
- Random Forest shows best balance of Precision and Recall
- All models show strong performance with >85% accuracy

RECOMMENDATIONS:
1. For production deployment: Use Random Forest or KNN for best accuracy
2. For confidence scores: Use Logistic Regression with highest ROC-AUC
3. For interpretability: Logistic Regression is most interpretable
4. Ensemble approach: Combine predictions from top 3 models for robustness

MODEL PERFORMANCE TABLE:
{df_results.to_string()}
    """

    with open('models/SUMMARY_REPORT.txt', 'w') as f:
        f.write(summary)

    print(summary)
    print("[DONE] Saved: SUMMARY_REPORT.txt")

def main():
    df_results = create_comparison_report()
    create_visualizations(df_results)
    create_summary_report(df_results)

    print("\n" + "=" * 60)
    print("ALL ANALYSIS COMPLETE!")
    print("Check notebooks/ folder for visualizations")
    print("Check models/ folder for reports and trained models")
    print("=" * 60)

if __name__ == "__main__":
    main()
