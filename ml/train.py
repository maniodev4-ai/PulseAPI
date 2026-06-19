"""
Train a classifier on the Wine dataset and save it to disk.

This script loads the wine dataset, splits it into train/test sets,
trains a RandomForestClassifier, evaluates its accuracy, and saves
the trained model to ml/saved_model.pkl for later use by the API.
"""

import pickle
from pathlib import Path

from sklearn.datasets import load_wine
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


def load_data():
    """Load the wine dataset and return features (X) and labels (y)."""
    data = load_wine()
    return data.data, data.target, data.feature_names, data.target_names


def train_model(X_train, y_train) -> RandomForestClassifier:
    """Train a RandomForestClassifier on the given training data."""
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model


def evaluate_model(model: RandomForestClassifier, X_test, y_test) -> float:
    """Evaluate the model on test data and print a report. Returns accuracy."""
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    print(f"Accuracy: {accuracy:.4f}\n")
    print("Classification Report:")
    print(classification_report(y_test, predictions))

    return accuracy


def save_model(model: RandomForestClassifier, path: str) -> None:
    """Save the trained model to disk using pickle."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(model, f)
    print(f"Model saved to {path}")


def main():
    print("Loading data...")
    X, y, feature_names, target_names = load_data()

    print(f"Dataset shape: {X.shape}")
    print(f"Features: {list(feature_names)}")
    print(f"Classes: {list(target_names)}\n")

    print("Splitting into train/test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("Training model...\n")
    model = train_model(X_train, y_train)

    print("Evaluating model...\n")
    evaluate_model(model, X_test, y_test)

    save_model(model, "ml/saved_model.pkl")


if __name__ == "__main__":
    main()