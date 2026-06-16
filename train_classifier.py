from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parents[1]
DATA_CSV = ROOT / "data" / "dataset.csv"
MODEL_PATH = ROOT / "data" / "classifier.joblib"


def main():
    if not DATA_CSV.exists():
        raise FileNotFoundError(
            f"Dataset introuvable : {DATA_CSV}. Lance d'abord : python app/generate_dataset.py"
        )

    data = pd.read_csv(DATA_CSV)
    if "intent" not in data.columns:
        raise ValueError("Colonne 'intent' absente du dataset (attendu après generate_dataset).")

    X = data["texte_client"]
    y = data["intent"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = Pipeline(
        [
            ("tfidf", TfidfVectorizer(max_features=20_000, ngram_range=(1, 2))),
            ("clf", LogisticRegression(max_iter=500)),
        ]
    )

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print("Modèle sauvegardé :", MODEL_PATH)


if __name__ == "__main__":
    main()
