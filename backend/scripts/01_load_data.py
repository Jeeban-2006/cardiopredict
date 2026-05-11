import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# Load Heart Disease Dataset from UCI
def load_heart_disease_data():
    url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data'
    column_names = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
                    'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target']

    df = pd.read_csv(url, names=column_names, na_values='?')
    return df

def explore_data(df):
    print("=" * 60)
    print("DATASET OVERVIEW")
    print("=" * 60)
    print(f"Dataset Shape: {df.shape}")
    print(f"\nFirst 5 rows:\n{df.head()}")
    print(f"\nData Types:\n{df.dtypes}")
    print(f"\nMissing Values:\n{df.isnull().sum()}")
    print(f"\nStatistical Summary:\n{df.describe()}")
    print(f"\nTarget Distribution:\n{df['target'].value_counts()}")

    # Save processed data
    df.to_csv('data/heart_disease_raw.csv', index=False)
    return df

if __name__ == "__main__":
    print("Loading Heart Disease Dataset...")
    df = load_heart_disease_data()
    print("Data loaded successfully!")
    explore_data(df)
