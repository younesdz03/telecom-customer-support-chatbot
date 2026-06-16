import random
from pathlib import Path

import pandas as pd

# Aligné avec intents.md et eval_questions.csv
ROOT = Path(__file__).resolve().parents[1]

intents = {
    "OFFRE_INFO": [
        "quelle est la différence entre ADSL et fibre",
        "quelle offre internet choisir pour la maison",
        "c’est quoi une box 4G",
        "la fibre est-elle plus stable que l’ADSL",
        "je veux comparer les offres internet",
    ],
    "ELIGIBILITE_INFO": [
        "comment savoir si je suis éligible à la fibre",
        "la fibre est disponible dans ma zone",
        "je peux avoir la fibre dans ma ville",
        "comment vérifier l’éligibilité sans me déplacer",
        "quelles infos pour vérifier l’éligibilité fibre",
    ],
    "PANNE_NO_INTERNET": [
        "je n’ai plus internet",
        "la connexion internet ne fonctionne pas",
        "internet est coupé chez moi",
        "la fibre ne marche plus",
        "je suis connecté au wifi mais aucun site ne s’ouvre",
    ],
    "DEBIT_LENT": [
        "internet est très lent",
        "le débit est faible",
        "ça rame pour regarder des vidéos",
        "ping élevé dans les jeux",
        "la navigation est lente même proche du modem",
    ],
    "PROBLEME_WIFI": [
        "le wifi ne s’affiche plus",
        "mon téléphone ne se connecte pas au wifi",
        "wifi faible dans ma chambre",
        "mot de passe wifi refusé",
        "le wifi se déconnecte tout le temps",
    ],
    "MODEM_ONT_VOYANTS": [
        "le voyant LOS est rouge",
        "le voyant PON clignote",
        "voyant internet éteint sur la box",
        "le voyant WLAN est éteint",
        "les voyants du modem sont bizarres",
    ],
    "OUVRIR_TICKET": [
        "je veux ouvrir une réclamation",
        "créez un ticket svp",
        "envoyez un technicien",
        "je veux signaler une panne",
        "ouvrir un ticket pour mon problème internet",
    ],
    "CONTACT_SUPPORT": [
        "quel numéro appeler pour le support",
        "comment contacter Algérie Télécom",
        "je peux aller en agence",
        "c’est quoi les moyens de contact",
        "je veux parler à un agent",
    ],
}

prefixes = [
    "",
    "bonjour",
    "s'il vous plaît",
    "je rencontre un problème",
    "pouvez-vous m'aider",
    "j'ai un souci",
    "merci de vérifier",
]

suffixes = [
    "",
    "depuis ce matin",
    "depuis hier",
    "depuis plusieurs jours",
    "à mon domicile",
    "dans mon quartier",
]

VARIATIONS_PER_PHRASE = 80

dataset = []

for intent, phrases in intents.items():
    for phrase in phrases:
        for _ in range(VARIATIONS_PER_PHRASE):
            p = random.choice(prefixes)
            s = random.choice(suffixes)
            text = f"{p} {phrase} {s}".strip()
            dataset.append({"texte_client": text, "intent": intent})

df = pd.DataFrame(dataset)
out = ROOT / "data" / "dataset.csv"
out.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(out, index=False, encoding="utf-8")

print("Dataset généré :", len(df), "->", out)
