import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

def preprocess_data():
    print("=" * 60)
    print("DATA PREPROCESSING")
    print("=" * 60)

    # Load raw data
    df = pd.read_csv('data/heart_disease_raw.csv')
    print(f"Original shape: {df.shape}")

    # Handle missing values
    df['ca'].fillna(df['ca'].median(), inplace=True)
    df['thal'].fillna(df['thal'].median(), inplace=True)
    print(f"\nMissing values handled")

    # Separate features and target
    X = df.drop('target', axis=1)
    y = df['target']

    # Convert target to binary (0: no disease, 1: disease present)
    y_binary = (y > 0).astype(int)

    print(f"\nTarget distribution (binary):")
    print(f"No disease (0): {(y_binary == 0).sum()}")
    print(f"Disease (1): {(y_binary == 1).sum()}")

    # Train-test split (80-20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_binary, test_size=0.2, random_state=42, stratify=y_binary
    )

    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Save processed data
    np.save('data/X_train.npy', X_train_scaled)
    np.save('data/X_test.npy', X_test_scaled)
    np.save('data/y_train.npy', y_train)
    np.save('data/y_test.npy', y_test)

    # Save scaler and feature names
    import pickle
    with open('data/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)

    print(f"\nTrain set size: {X_train_scaled.shape}")
    print(f"Test set size: {X_test_scaled.shape}")
    print(f"Feature count: {X_train_scaled.shape[1]}")
    print("\nProcessed data saved!")

if __name__ == "__main__":
    preprocess_data()
