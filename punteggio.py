# -*- coding: utf-8 -*-
"""Logica di calcolo del Test Onda.

Vive solo lato server: il browser non riceve mai punteggi grezzi, soglie o
etichette interne. Il quiz non esclude nessuno, qualunque sia il risultato:
l'etichetta interna serve unicamente al team per organizzare il follow-up.
"""

from contenuti import DOMANDE_PER_ID, VARIANTI

ALTO, MEDIO, BASSO = "ALTO", "MEDIO", "BASSO"

# soglie per blocco: (minimo per ALTO, minimo per MEDIO, massimo teorico)
SOGLIE = {
    "A": {"alto": 19, "medio": 10, "max": 28},
    "B": {"alto": 8, "medio": 4, "max": 12},
    "C": {"alto": 10, "medio": 5, "max": 15},
}

# traduzione per la persona: valore su 10 e etichetta discorsiva
ETICHETTE = {
    "A": {ALTO: (9, "Molto forte"), MEDIO: (6, "In movimento"), BASSO: (3, "Agli inizi")},
    "B": {ALTO: (9, "Concreta"), MEDIO: (6, "Presente"), BASSO: (3, "Da risvegliare")},
    "C": {ALTO: (9, "Già chiara"), MEDIO: (6, "In costruzione"), BASSO: (3, "Da esplorare")},
}


def punti_risposta(domanda_id, risposta):
    """Punti di una singola risposta. `risposta` è l'indice dell'opzione
    scelta per le domande a scelta, il valore 1-10 per le scale."""
    domanda = DOMANDE_PER_ID[domanda_id]
    if risposta is None:
        return 0
    if domanda["tipo"] == "scala":
        if not domanda.get("punteggia"):
            return 0
        return int(risposta) / 2
    opzioni = domanda["opzioni"]
    indice = int(risposta)
    if 0 <= indice < len(opzioni):
        return opzioni[indice][1]
    return 0


def bonus_gap(risposte):
    """Distanza fra quanto conta crescere (D6) e quanto la persona si sente
    già pronta (D7): è il segnale di pain più forte del test."""
    d6, d7 = risposte.get("D6"), risposte.get("D7")
    if d6 is None or d7 is None:
        return 0
    differenza = int(d6) - int(d7)
    if differenza >= 3:
        return 2
    if differenza >= 1:
        return 1
    return 0


def livello(blocco, punti):
    soglie = SOGLIE[blocco]
    if punti >= soglie["alto"]:
        return ALTO
    if punti >= soglie["medio"]:
        return MEDIO
    return BASSO


def etichetta_interna(livello_a, livello_b, livello_c):
    """Etichetta a uso esclusivo del team, mai mostrata alla persona."""
    if livello_a == BASSO:
        return "rosso"
    if livello_b == BASSO:
        return "rosso"
    if livello_a == ALTO and livello_b == ALTO and livello_c != BASSO:
        return "verde"
    return "giallo"


def scegli_variante(etichetta, livello_a, livello_c):
    if etichetta == "verde":
        return 1 if livello_c == ALTO else 2
    if etichetta == "giallo":
        return 3 if livello_a == ALTO else 4
    return 5 if livello_a == BASSO else 6


def calcola(risposte):
    """Dalle risposte grezze al profilo completo da mostrare."""
    punti = {"A": 0.0, "B": 0.0, "C": 0.0}
    for domanda_id, risposta in risposte.items():
        domanda = DOMANDE_PER_ID.get(domanda_id)
        if domanda is None:
            continue
        punti[domanda["blocco"]] += punti_risposta(domanda_id, risposta)

    bonus = bonus_gap(risposte)
    punti["A"] += bonus
    for blocco in punti:
        punti[blocco] = min(punti[blocco], SOGLIE[blocco]["max"])

    livelli = {b: livello(b, punti[b]) for b in ("A", "B", "C")}
    etichetta = etichetta_interna(livelli["A"], livelli["B"], livelli["C"])
    variante = scegli_variante(etichetta, livelli["A"], livelli["C"])

    return {
        "punti": punti,
        "bonus_gap": bonus,
        "livelli": livelli,
        "etichetta_interna": etichetta,
        "variante": variante,
        "archetipo": VARIANTI[variante]["archetipo"],
        "mostrati": {b: ETICHETTE[b][livelli[b]] for b in ("A", "B", "C")},
    }
