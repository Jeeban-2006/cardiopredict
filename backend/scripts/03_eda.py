import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

def create_eda():
    print("=" * 60)
    print("EXPLORATORY DATA ANALYSIS")
    print("=" * 60)

    df = pd.read_csv('data/heart_disease_raw.csv')

    # Create figures
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Heart Disease Dataset - EDA', fontsize=16, fontweight='bold')

    # 1. Target distribution
    target_counts = (df['target'] > 0).astype(int).value_counts()
    axes[0, 0].bar(['No Disease', 'Disease'], target_counts.values, color=['green', 'red'])
    axes[0, 0].set_title('Target Distribution')
    axes[0, 0].set_ylabel('Count')

    # 2. Age distribution
    axes[0, 1].hist(df['age'], bins=20, color='skyblue', edgecolor='black')
    axes[0, 1].set_title('Age Distribution')
    axes[0, 1].set_xlabel('Age')
    axes[0, 1].set_ylabel('Frequency')

    # 3. Sex distribution
    sex_counts = df['sex'].value_counts()
    axes[0, 2].bar(['Female', 'Male'], sex_counts.values, color=['pink', 'blue'])
    axes[0, 2].set_title('Sex Distribution')
    axes[0, 2].set_ylabel('Count')

    # 4. Cholesterol distribution
    axes[1, 0].hist(df['chol'], bins=20, color='orange', edgecolor='black')
    axes[1, 0].set_title('Cholesterol Distribution')
    axes[1, 0].set_xlabel('Cholesterol Level')
    axes[1, 0].set_ylabel('Frequency')

    # 5. Blood Pressure distribution
    axes[1, 1].hist(df['trestbps'], bins=20, color='purple', edgecolor='black')
    axes[1, 1].set_title('Resting Blood Pressure Distribution')
    axes[1, 1].set_xlabel('Blood Pressure (mmHg)')
    axes[1, 1].set_ylabel('Frequency')

    # 6. Max Heart Rate
    axes[1, 2].hist(df['thalach'], bins=20, color='cyan', edgecolor='black')
    axes[1, 2].set_title('Max Heart Rate Distribution')
    axes[1, 2].set_xlabel('Max Heart Rate (bpm)')
    axes[1, 2].set_ylabel('Frequency')

    plt.tight_layout()
    plt.savefig('notebooks/01_eda_distribution.png', dpi=100, bbox_inches='tight')
    print("[DONE] Saved: 01_eda_distribution.png")

    # Correlation heatmap
    plt.figure(figsize=(12, 8))
    correlation_matrix = df.drop('target', axis=1).corr()
    sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm',
                square=True, cbar_kws={'label': 'Correlation'})
    plt.title('Feature Correlation Matrix', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('notebooks/02_correlation_matrix.png', dpi=100, bbox_inches='tight')
    print("[DONE] Saved: 02_correlation_matrix.png")

    # Feature statistics by disease status
    disease_status = (df['target'] > 0).astype(int)
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Feature Comparison: Disease vs No Disease', fontsize=14, fontweight='bold')

    axes[0, 0].boxplot([df[df['target'] == 0]['age'], df[df['target'] > 0]['age']],
                       labels=['No Disease', 'Disease'])
    axes[0, 0].set_title('Age')
    axes[0, 0].set_ylabel('Age (years)')

    axes[0, 1].boxplot([df[df['target'] == 0]['chol'], df[df['target'] > 0]['chol']],
                       labels=['No Disease', 'Disease'])
    axes[0, 1].set_title('Cholesterol')
    axes[0, 1].set_ylabel('Cholesterol (mg/dl)')

    axes[1, 0].boxplot([df[df['target'] == 0]['trestbps'], df[df['target'] > 0]['trestbps']],
                       labels=['No Disease', 'Disease'])
    axes[1, 0].set_title('Resting Blood Pressure')
    axes[1, 0].set_ylabel('Blood Pressure (mmHg)')

    axes[1, 1].boxplot([df[df['target'] == 0]['thalach'], df[df['target'] > 0]['thalach']],
                       labels=['No Disease', 'Disease'])
    axes[1, 1].set_title('Max Heart Rate Achieved')
    axes[1, 1].set_ylabel('Heart Rate (bpm)')

    plt.tight_layout()
    plt.savefig('notebooks/03_feature_comparison.png', dpi=100, bbox_inches='tight')
    print("[DONE] Saved: 03_feature_comparison.png")

    print("\nEDA completed! Check notebooks/ folder for visualizations.")

if __name__ == "__main__":
    create_eda()
