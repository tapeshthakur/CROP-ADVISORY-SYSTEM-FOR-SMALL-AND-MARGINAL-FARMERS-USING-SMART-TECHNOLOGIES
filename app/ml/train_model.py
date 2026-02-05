import pathlib

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

BASE_DIR = pathlib.Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "crop_recommendation_sample.csv"
MODEL_PATH = BASE_DIR / "ml" / "model.pkl"


def evaluate_model(model, x_train, x_test, y_train, y_test):
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    report = classification_report(y_test, predictions, output_dict=True, zero_division=0)
    return report["accuracy"], report


def main():
    data = pd.read_csv(DATA_PATH)
    features = data[["N", "P", "K", "ph", "rainfall", "temperature", "humidity"]]
    labels = data["label"]

    # For small academic sample datasets, stratify can fail if classes are many and rows are few.
    stratify_labels = labels if labels.value_counts().min() > 1 and len(data) >= 50 else None

    X_train, X_test, y_train, y_test = train_test_split(
        features,
        labels,
        test_size=0.3,
        random_state=42,
        stratify=stratify_labels,
    )

    candidates = {
        "DecisionTree": DecisionTreeClassifier(random_state=42),
        "RandomForest": RandomForestClassifier(n_estimators=120, random_state=42),
    }

    best_name = None
    best_model = None
    best_accuracy = -1

    for name, model in candidates.items():
        accuracy, report = evaluate_model(model, X_train, X_test, y_train, y_test)
        print(f"\n{name} Accuracy: {accuracy:.4f}")
        print(classification_report(y_test, model.predict(X_test), zero_division=0))
        if accuracy > best_accuracy:
            best_name, best_model, best_accuracy = name, model, accuracy

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(best_model, MODEL_PATH)
    print(f"\nSelected model: {best_name} (accuracy={best_accuracy:.4f})")
    print(f"Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    main()
