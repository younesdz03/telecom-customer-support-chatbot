from pathlib import Path
from typing import Optional

import joblib

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "data" / "classifier.joblib"

_model = None


def load_classifier():
    global _model
    if _model is not None:
        return _model
    if not MODEL_PATH.exists():
        return None
    _model = joblib.load(MODEL_PATH)
    return _model


def predict_intent(text: str) -> Optional[str]:
    clf = load_classifier()
    if clf is None:
        return None
    return str(clf.predict([text])[0])


# Aide la recherche sémantique (même embedding) en français
INTENT_HINTS_FR = {
    "OFFRE_INFO": "offres internet ADSL fibre 4G box abonnement",
    "ELIGIBILITE_INFO": "éligibilité fibre zone disponibilité vérification",
    "PANNE_NO_INTERNET": "panne pas de connexion internet coupé diagnostic",
    "DEBIT_LENT": "débit lent lenteur ping navigation streaming",
    "PROBLEME_WIFI": "wifi sans fil mot de passe SSID portée déconnexion",
    "MODEM_ONT_VOYANTS": "voyants modem ONT LOS PON WLAN diagnostic box",
    "OUVRIR_TICKET": "réclamation ticket support technique assistance",
    "CONTACT_SUPPORT": "contact numéro agence support client hotline",
}


def augment_query_for_retrieval(question: str) -> str:
    intent = predict_intent(question)
    if not intent:
        return question
    hint = INTENT_HINTS_FR.get(intent, "")
    if not hint:
        return question
    return f"{question}\n{hint}"
