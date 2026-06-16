import requests
import unicodedata
import json
from pathlib import Path
import random

from app.rag.retriever import retrieve, build_context


OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "phi3"

BASE_DIR = Path(__file__).resolve().parents[1]
OFFRES_PATH = BASE_DIR / "data" / "kb" / "kb_offres.json"


def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return text



def get_smalltalk_response(question: str):
    q = normalize_text(question)

    greetings = {
        "bonjour", "salut", "bonsoir", "hello", "salam", "cc", "coucou",
        "hey", "hi", "bjr", "bsr", "slt", "salam alikom", "wa alikom salam",
        "ahlan", "marhba", "good morning", "good evening", "yo", "wesh",
        "bonjour bonjour", "salut salut", "coucou coucou", "allo", "allô"
    }

    thanks = {
        "merci", "merci beaucoup", "thanks", "non merci", "merci bien",
        "je vous remercie", "je te remercie", "thank you", "thx", "mrc",
        "merci infiniment", "merci pour votre aide", "merci pour l aide",
        "c est tres utile", "tres utile", "utile", "ca m a aide",
        "vous m avez aide", "parfait merci", "super merci", "ok merci",
        "d accord merci", "nickel merci", "impeccable merci"
    }

    goodbye = {
        "au revoir", "bye", "a bientot", "bonne nuit", "non au revoir",
        "bonne journee", "bonne soiree", "bonne fin de journee",
        "a plus", "a plus tard", "a tout a l heure", "a toute",
        "ciao", "tchao", "bye bye", "goodbye", "on se revoit",
        "je vous dis au revoir", "je pars", "je dois y aller",
        "merci au revoir", "ok au revoir", "c est bon au revoir"
    }

    how_are_you = {
        "ca va", "comment ca va", "comment vous allez", "comment tu vas",
        "ca va ?", "cv", "tu vas bien", "vous allez bien",
        "comment allez vous", "quoi de neuf", "la forme", "t es en forme",
        "ca roule", "comment vas tu", "tout va bien"
    }

    who_are_you = {
        "qui es tu", "qui etes vous", "tu es qui", "vous etes qui",
        "c est quoi ce chatbot", "c est quoi ce bot", "tu es un robot",
        "tu es une ia", "vous etes une ia", "t es un humain",
        "tu es humain", "tu es une machine", "presentez vous",
        "presente toi", "dis moi qui tu es", "c est quoi ce service",
        "comment tu t appelles", "comment vous appelez vous",
        "quel est ton nom", "ton nom"
    }

    what_can_you_do = {
        "que peux tu faire", "tu peux faire quoi", "vous pouvez faire quoi",
        "aide moi", "aide", "help", "comment tu peux m aider",
        "comment vous pouvez m aider", "c est quoi tes fonctionnalites",
        "a quoi tu sers", "a quoi vous servez", "tu sers a quoi",
        "tu peux m aider", "vous pouvez m aider", "je ne sais pas quoi demander",
        "par ou commencer", "que faire", "explique toi", "explique vous"
    }

    yes = {
        "oui", "oui merci", "yes", "ouais", "yep", "bien sur",
        "exactement", "tout a fait", "effectivement", "affirmatif",
        "ok", "d accord", "c est ca", "voila", "correct", "juste"
    }

    no = {
        "non", "no", "nope", "pas vraiment", "pas du tout",
        "absolument pas", "nenni", "nan"
    }

    insults = {
        "idiot", "nul", "inutile", "stupide", "bete", "mauvais",
        "horrible", "catastrophique", "deplorable", "zero", "naze"
    }

    compliments = {
        "bravo", "excellent", "super", "genial", "top", "bien",
        "parfait", "impressionnant", "incroyable", "magnifique",
        "bien joue", "chapeau", "tres bien"
    }

    greetings_responses = [
        "Bonjour 👋 Je suis l'assistant Algérie Télécom. Comment puis-je vous aider ?",
        "Salut 😊 Bienvenue chez Algérie Télécom ! Quelle est votre question ?",
        "Bonjour ! Ravi de vous retrouver 👋 En quoi puis-je vous être utile ?",
        "Bonsoir 🌙 Je suis là pour vous aider. Que puis-je faire pour vous ?",
        "Bonjour ! Comment puis-je vous assister aujourd'hui ? 😊",
    ]

    thanks_responses = [
        "Avec plaisir 😊 Avez-vous une autre question ?",
        "Je suis là pour ça ! N'hésitez pas si vous avez d'autres questions 👍",
        "Ravi d'avoir pu vous aider 😊 Y a-t-il autre chose ?",
        "C'est avec plaisir ! N'hésitez pas à revenir si besoin 🙏",
        "Merci à vous ! Une autre question peut-être ? 😊",
    ]

    goodbye_responses = [
        "Au revoir 👋 N'hésitez pas à revenir si vous avez besoin d'aide.",
        "Bonne journée ! À bientôt 😊",
        "Au revoir ! Je reste disponible quand vous avez besoin 👋",
        "Bonne continuation ! Revenez quand vous voulez 😊",
        "À bientôt 👋 Algérie Télécom reste à votre service !",
    ]

    how_are_you_responses = [
        "Je suis un assistant, donc toujours en pleine forme ! 😄 Et vous ? En quoi puis-je vous aider ?",
        "Très bien merci ! Prêt à vous aider 💪 Quelle est votre question ?",
        "Opérationnel à 100% ! 😄 Comment puis-je vous aider ?",
        "Toujours disponible pour vous aider ! Quelle est votre demande ? 😊",
    ]

    who_are_you_responses = [
        "Je suis l'assistant virtuel d'Algérie Télécom 🤖 Je suis là pour répondre à vos questions sur les pannes, la fibre, le paiement, et plus encore !",
        "Je suis un chatbot intelligent au service d'Algérie Télécom 💬 Posez-moi vos questions sur internet, le modem, les factures ou les services.",
        "Je suis votre assistant Algérie Télécom 🤖 Je peux vous aider sur les problèmes techniques, les factures, la résiliation, et bien d'autres sujets !",
    ]

    what_can_you_do_responses = [
        "Je peux vous aider sur :\n• 🔧 Pannes internet ou modem\n• 💡 Fibre optique et ADSL\n• 💳 Paiement de factures\n• 📋 Résiliation de contrat\n• 📞 Contacter le support\n\nQue souhaitez-vous savoir ?",
        "Voici ce que je sais faire :\n• Diagnostiquer une panne internet\n• Expliquer comment payer une facture\n• Informer sur les offres et services\n• Guider pour contacter le support\n\nQuelle est votre question ? 😊",
        "Je suis spécialisé dans les services Algérie Télécom ! Posez-moi vos questions sur les pannes, la fibre, le modem, les factures ou la résiliation 💬",
    ]

    yes_responses = [
        "Parfait ! Que puis-je faire pour vous ? 😊",
        "Super ! Posez votre question, je suis là 👍",
        "Très bien ! Comment puis-je vous aider ? 😊",
    ]

    no_responses = [
        "D'accord ! N'hésitez pas à revenir si vous avez besoin 😊",
        "Pas de problème ! Je reste disponible si vous avez une question 👍",
        "Très bien ! À votre disposition si besoin 😊",
    ]

    insults_responses = [
        "Je comprends votre frustration 😔 Je fais de mon mieux pour vous aider. Quelle est votre question ?",
        "Désolé si je n'ai pas pu répondre à vos attentes 🙏 Essayons de nouveau, quelle est votre demande ?",
        "Je suis là pour vous aider du mieux possible 😊 Reformulez votre question et je ferai de mon mieux !",
    ]

    compliments_responses = [
        "Merci beaucoup ! 😊 C'est très gentil. Y a-t-il autre chose que je peux faire pour vous ?",
        "Oh merci ! 🙏 Ravi d'avoir pu vous aider. Une autre question ?",
        "Merci pour ce retour positif 😊 Je reste disponible pour vous !",
    ]

    if q in greetings:
        return random.choice(greetings_responses)

    if q in thanks:
        return random.choice(thanks_responses)

    if q in goodbye:
        return random.choice(goodbye_responses)

    if q in how_are_you:
        return random.choice(how_are_you_responses)

    if q in who_are_you:
        return random.choice(who_are_you_responses)

    if q in what_can_you_do:
        return random.choice(what_can_you_do_responses)

    if q in yes:
        return random.choice(yes_responses)

    if q in no:
        return random.choice(no_responses)

    if q in insults:
        return random.choice(insults_responses)

    if q in compliments:
        return random.choice(compliments_responses)

    return None



def professional_fallback_response() -> str:
    return (
        "Je suis désolé, cette demande ne relève pas du périmètre de l’assistant Algérie Télécom. "
        "Je peux vous accompagner concernant les offres Internet, l’ADSL, le VDSL, la fibre, la 4G LTE, "
        "le Wi-Fi, le modem, les pannes de connexion, le débit lent ou les moyens de contact du support."
    )


def is_general_offer_question(question: str) -> bool:
    q = normalize_text(question)

    offer_patterns = [
        "quelles sont les offres",
        "quels sont les offres",
        "liste des offres",
        "les offres disponibles",
        "offres internet disponibles",
        "offres internet",
        "offres algerie telecom",
        "donne moi les offres",
        "donner moi les offres",
        "affiche les offres",
        "propose moi les offres",
        "liste des offres fibre",
        "liste des offres adsl",
        "liste des offres vdsl",
        "liste des offres 4g",
        "offres fibre",
        "offres adsl",
        "offres vdsl",
        "offres 4g"
    ]

    return any(pattern in q for pattern in offer_patterns)


def detect_offer_filter(question: str):
    q = normalize_text(question)

    if "fibre gamers" in q or "gamers" in q:
        return "fibre_gamers"

    if "fibre" in q or "ftth" in q or "fttx" in q:
        return "fibre"

    if "adsl" in q:
        return "adsl"

    if "vdsl" in q:
        return "vdsl"

    if "4g" in q or "lte" in q:
        return "4g"

    return None


def offer_matches_filter(offre: dict, offer_filter: str | None) -> bool:
    if offer_filter is None:
        return True

    nom = normalize_text(offre.get("nom", ""))
    technologie = normalize_text(offre.get("technologie", ""))

    if offer_filter == "fibre_gamers":
        return "gamers" in nom

    if offer_filter == "fibre":
        return ("fibre" in nom or "fttx" in technologie) and "gamers" not in nom

    if offer_filter == "adsl":
        return "adsl" in nom or "adsl" in technologie

    if offer_filter == "vdsl":
        return "vdsl" in nom or "vdsl" in technologie

    if offer_filter == "4g":
        return "4g" in nom or "4g" in technologie or "lte" in nom or "lte" in technologie

    return True


def get_offers_response(question: str = ""):
    if not OFFRES_PATH.exists():
        return (
            "Je ne trouve pas le fichier des offres. "
            "Veuillez vérifier que le fichier kb_offres.json existe dans data/kb/."
        ), [], ""

    with open(OFFRES_PATH, "r", encoding="utf-8") as f:
        offres = json.load(f)

    offer_filter = detect_offer_filter(question)
    selected_offres = []

    for offre in offres:
        if not offer_matches_filter(offre, offer_filter):
            continue

        selected_offres.append({
            "score": 1.0,
            "source": offre.get("source", "kb_offres"),
            "doc_type": "offre",
            "record_id": offre.get("id", ""),
            "title": offre.get("nom", ""),
            "chunk_index": 0,
            "text": offre.get("usage_recommande", ""),

            "id": offre.get("id", ""),
            "nom": offre.get("nom", ""),
            "technologie": offre.get("technologie", ""),
            "debit_descendant": offre.get("debit_descendant", ""),
            "prix_mensuel": offre.get("prix_mensuel", ""),
            "usage_recommande": offre.get("usage_recommande", "")
        })

    if not selected_offres:
        return "Je n’ai trouvé aucune offre correspondant à cette demande.", [], ""

    if offer_filter == "fibre":
        titre = "Voici la liste des offres IDOOM Fibre disponibles :"
    elif offer_filter == "fibre_gamers":
        titre = "Voici la liste des offres IDOOM Fibre Gamers disponibles :"
    elif offer_filter == "adsl":
        titre = "Voici la liste des offres IDOOM ADSL disponibles :"
    elif offer_filter == "vdsl":
        titre = "Voici la liste des offres IDOOM VDSL disponibles :"
    elif offer_filter == "4g":
        titre = "Voici la liste des offres IDOOM 4G LTE disponibles :"
    else:
        titre = "Voici la liste des offres Algérie Télécom disponibles :"

    lignes = [titre]

    for i, offre in enumerate(selected_offres, start=1):
        bloc = (
            f"{i}. **{offre.get('nom', 'Offre sans nom')}**\n"
            f"   - ID : {offre.get('id', '')}\n"
            f"   - Source : {offre.get('source', '')}\n"
            f"   - Technologie : {offre.get('technologie', '')}\n"
            f"   - Débit / volume : {offre.get('debit_descendant', '')}\n"
            f"   - Prix : {offre.get('prix_mensuel', '')}\n"
            f"   - Usage recommandé : {offre.get('usage_recommande', '')}"
        )

        lignes.append(bloc)

    lignes.append(
        "Les tarifs et la disponibilité doivent être confirmés auprès du service commercial "
        "ou d’une agence Algérie Télécom."
    )

    answer = "\n\n".join(lignes)
    context = "\n\n".join([
        f"{offre.get('nom', '')} - {offre.get('debit_descendant', '')} - "
        f"{offre.get('prix_mensuel', '')} - {offre.get('usage_recommande', '')}"
        for offre in selected_offres
    ])

    return answer, selected_offres, context


def build_prompt(context: str, question: str) -> str:
    return f"""
Tu es un assistant pour Algérie Télécom.

Règles importantes :
- Utilise uniquement les informations pertinentes du contexte
- Ignore les parties du contexte qui ne correspondent pas à la question
- Si aucune information pertinente n’est trouvée, dis seulement : Je ne sais pas
- Ne jamais inventer
- Réponds en français simple et clair
- Ne mentionne pas les champs internes comme id, source, statut, mots_cles ou note_interne
- Si la question concerne les offres, présente les offres disponibles sous forme de liste claire
- Pour les offres, indique le nom de l’offre, la technologie, le débit ou volume, le prix et l’usage recommandé

Contexte :
{context}

Question :
{question}
"""


def call_ollama(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 250
        }
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=300)
        response.raise_for_status()

        data = response.json()
        return data.get("response", "").strip()

    except requests.exceptions.ConnectionError:
        return (
            "Le modèle local n’est pas disponible actuellement. "
            "Veuillez vérifier que le serveur Ollama est lancé."
        )

    except requests.exceptions.Timeout:
        return (
            "Le modèle local prend trop de temps à répondre. "
            "Veuillez réessayer dans quelques instants."
        )

    except requests.exceptions.RequestException:
        return (
            "Une erreur est survenue lors de la communication avec le modèle local."
        )
    
def is_los_question(question: str) -> bool:
    q = normalize_text(question)

    los_keywords = [
        "los",
        "voyant los",
        "voyant rouge",
        "los rouge",
        "signal fibre",
        "pas de signal",
        "voyant fibre rouge"
    ]

    return any(keyword in q for keyword in los_keywords)

def los_response():
    answer = (
        "Le voyant LOS rouge indique généralement une perte de signal fibre. "
        "Veuillez vérifier que le câble fibre est correctement branché, sans être plié ou endommagé. "
        "Redémarrez ensuite l'équipement fibre, comme l'ONT ou le modem, puis attendez quelques minutes. "
        "Si le voyant LOS reste rouge, il peut s'agir d'un problème de raccordement ou d'un incident réseau. "
        "Dans ce cas, il est recommandé de contacter le support technique d'Algérie Télécom pour ouvrir un ticket d'intervention."
    )

    results = [{
        "score": 1.0,
        "source": "réponse_prédéfinie",
        "doc_type": "diagnostic_fibre",
        "record_id": "los_rouge",
        "title": "Voyant LOS rouge",
        "chunk_index": 0,
        "text": answer
    }]

    return answer, results, answer

def ask(question: str):
    question = question.strip()

    if not question:
        return "Veuillez poser une question.", [], ""

    smalltalk_answer = get_smalltalk_response(question)
    if smalltalk_answer:
        return smalltalk_answer, [], ""
    if is_los_question(question):
        print("[DEBUG] question LOS détectée")
        return los_response()

    if is_general_offer_question(question):
        print("[DEBUG] question générale sur les offres")
        return get_offers_response(question)

    print("[DEBUG] début ask()")

    q_lower = question.lower()

    is_offer_question = any(word in q_lower for word in [
        "offre", "offres", "adsl", "fibre", "vdsl", "4g", "lte",
        "internet disponible", "abonnement", "prix", "tarif", "forfait"
    ])

    if is_offer_question:
        results = retrieve(question, top_k=10)
        score_threshold = 0.15
    else:
        results = retrieve(question, top_k=4)
        score_threshold = 0.3

    print("[DEBUG] retrieve OK")

    results = [r for r in results if r["score"] > score_threshold]

    if not results:
        print("[DEBUG] aucun résultat pertinent")
        return professional_fallback_response(), [], ""

    context = build_context(results)
    prompt = build_prompt(context, question)

    print("[DEBUG] appel API Ollama...")

    answer = call_ollama(prompt)
    print("[DEBUG] réponse Ollama OK")

    answer_lower = answer.strip().lower()

    fallback_triggers = [
        "je ne sais pas",
        "je n'ai pas d'informations",
        "je n’ai pas d’informations",
        "pas d'informations",
        "pas d’informations",
        "dans ce contexte fourni",
        "ce contexte fourni",
        "reformuler votre question",
        "je serais heureux",
        "question :"
    ]

    if any(trigger in answer_lower for trigger in fallback_triggers):
        answer = professional_fallback_response()

    return answer, results, context
if __name__ == "__main__":
    question = input("Pose ta question : ")
    answer, _, _ = ask(question)
    print("\n===== RÉPONSE =====\n")
    print(answer)