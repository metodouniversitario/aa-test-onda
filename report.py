# -*- coding: utf-8 -*-
"""Report di chiamata: riassunto, punti di forza e punti di attenzione.

Serve al team commerciale prima di telefonare a chi ha fatto il test. È tutto
derivato dalle risposte reali, con regole deterministiche: nessun testo
inventato, ogni riga corrisponde a qualcosa che la persona ha davvero risposto.
"""

from contenuti import ARCHETIPI, DOMANDE_PER_ID
from punteggio import bonus_gap

SITUAZIONE = {
    0: "studia",
    1: "studia e lavora",
    2: "lavora come dipendente",
    3: "è libero professionista",
    4: "non lavora e sta cercando",
}


def _scelta(risposte, domanda_id):
    """Indice dell'opzione scelta, o None."""
    valore = risposte.get(domanda_id)
    return int(valore) if valore is not None else None


def _scala(risposte, domanda_id):
    valore = risposte.get(domanda_id)
    return int(valore) if valore is not None else None


def _testo_risposta(risposte, domanda_id):
    domanda = DOMANDE_PER_ID[domanda_id]
    valore = risposte.get(domanda_id)
    if valore is None:
        return ""
    if domanda["tipo"] == "scala":
        return "%s su 10" % valore
    return domanda["opzioni"][int(valore)][0]


# --------------------------------------------------------------------------
# Regole: (condizione, peso, testo). Vince il peso più alto.
# --------------------------------------------------------------------------

def _regole_forza(r):
    d = lambda q: _scelta(r, q)
    d6, d7, d15 = _scala(r, "D6"), _scala(r, "D7"), _scala(r, "D15")
    gap = (d6 - d7) if (d6 is not None and d7 is not None) else 0
    regole = [
        (d("D10") == 0, 10,
         "Ha già investito tempo o denaro in formazione: è abituato a pagare per crescere."),
        (d("D2") == 0, 10,
         "Sa dove vuole arrivare: vuole diventare un professionista più forte e riconosciuto nel suo campo."),
        (gap >= 3, 9,
         "Sente una distanza netta fra quanto conta crescere (%s su 10) e quanto si sente pronto (%s su 10): "
         "è la leva più forte da usare in chiamata." % (d6, d7)),
        (d6 is not None and d6 >= 9, 9,
         "Dà la massima importanza alla propria crescita professionale (%s su 10)." % d6),
        (d("D16") == 0, 9,
         "Se fra 5 anni nulla fosse cambiato lo vivrebbe come un problema serio: c'è urgenza reale."),
        (d("D11") == 0, 8,
         "Cerca un lavoro su di sé più profondo, non solo competenze tecniche: in linea con il percorso."),
        (d("D12") == 0, 8,
         "Si riconosce già nell'idea di mettere il proprio lavoro al servizio di qualcosa di più grande."),
        (d("D5") == 0, 8,
         "Riconosce di dover lavorare prima su di sé: mentalità, sicurezza, determinazione."),
        (d("D9") == 0, 7,
         "È disposto a fare scelte controcorrente rispetto alle proprie abitudini pur di crescere."),
        (d("D8") == 0, 7,
         "Accoglie i cambiamenti importanti anche quando spaventano."),
        (d("D13") in (0, 1), 7,
         "Il suo lavoro è fatto soprattutto di scrittura, comunicazione, analisi, vendita o gestione: "
         "l'intelligenza artificiale lo tocca da vicino."),
        (d("D4") == 0, 7,
         "Teme molto di restare indietro nella professione: pain esplicito e dichiarato."),
        (d("D10") == 1, 6,
         "Si è già informato seriamente sulla formazione: è nella fase giusta per decidere."),
        (d("D3") == 0, 6,
         "Il cambiamento del lavoro legato all'AI lo preoccupa molto e ci pensa spesso."),
        (d("D14") in (0, 1), 6,
         "Ha già visto colleghi del suo settore usare strumenti di intelligenza artificiale."),
        (d("D1") == 3, 5,
         "È libero professionista: decide da solo e può investire su di sé senza chiedere permesso."),
        (d6 is not None and 7 <= d6 <= 8, 5,
         "Tiene molto alla propria crescita professionale (%s su 10)." % d6),
        (d("D10") == 3, 4,
         "Non ha mai fatto nulla per la sua crescita, ma dice di voler iniziare ora."),
        (d15 is not None and d15 <= 3, 4,
         "Si sente impreparato davanti all'AI (%s su 10): sa di avere un vuoto da colmare." % d15),
        (d("D2") in (1, 2), 4,
         "Vuole muoversi ma non sa da dove partire: cerca proprio una direzione."),
    ]
    return regole


def _regole_attenzione(r):
    d = lambda q: _scelta(r, q)
    d6, d7, d15 = _scala(r, "D6"), _scala(r, "D7"), _scala(r, "D15")
    regole = [
        (d("D2") == 4, 10,
         "Dice di essere soddisfatto e di non avere interesse a crescere: manca il motore, va costruito da zero."),
        (d("D16") == 2, 9,
         "Gli sarebbe indifferente se fra 5 anni nulla cambiasse: nessuna urgenza percepita."),
        (d6 is not None and d6 <= 4, 9,
         "La crescita professionale oggi non è una priorità per lui (%s su 10)." % d6),
        (d("D10") == 2, 8,
         "Ci pensa spesso ma non ha mai fatto nulla di concreto: alto rischio che rimandi ancora."),
        (d("D11") == 3, 8,
         "Non crede che il lavoro su di sé lo riguardi: parte del percorso gli suonerà lontana."),
        (d("D5") == 2, 7,
         "Si sente già pronto sul fronte interiore: poca apertura dichiarata a mettersi in discussione."),
        (d("D9") == 3, 7,
         "Tende a restare in ciò che conosce: difficilmente si muove in fretta."),
        (d("D8") == 2, 7,
         "Il cambiamento lo destabilizza, preferisce che le cose restino come sono."),
        (d("D12") == 3, 7,
         "Il tema del lavoro al servizio di qualcosa di più grande non gli interessa."),
        (d("D2") == 3, 7,
         "Guarda solo a concludere quello che sta facendo, senza pensare oltre."),
        (d("D4") == 2, 6,
         "Non teme di restare indietro: l'urgenza va costruita in chiamata, non darla per scontata."),
        (d("D13") == 3, 6,
         "Fa un lavoro soprattutto pratico o manuale: la rilevanza dell'AI va spiegata con esempi concreti."),
        (d7 is not None and d7 >= 9, 6,
         "Si sente già pronto ad affrontare le sfide del suo settore (%s su 10): "
         "vede poco spazio per un percorso." % d7),
        (d15 is not None and d15 >= 9, 6,
         "Dice di essere già pronto sull'intelligenza artificiale (%s su 10)." % d15),
        (d("D1") == 4, 6,
         "Non lavora e sta cercando: valutare tempi e capacità di investimento."),
        (d("D14") == 2, 5,
         "Non ha mai notato l'AI nel suo settore: il tema gli sembra ancora distante."),
        (d("D3") in (2, 3), 5,
         "I cambiamenti del mondo del lavoro non lo preoccupano: leva della paura poco efficace."),
        (d("D11") == 2, 5,
         "Non aveva mai pensato al lavoro su di sé in questi termini: serve spiegarlo con parole semplici."),
        (d("D1") == 0, 4,
         "È studente: valutare capacità e tempi di investimento."),
        (d("D9") == 2, 4,
         "Vuole procedere con gradualità: meglio non spingere troppo nella prima chiamata."),
        (d("D8") == 3, 3,
         "Davanti al cambiamento risponde \"dipende\": posizione poco definita, da approfondire a voce."),
        (d("D12") == 2, 3,
         "Non ha mai riflettuto sul senso più ampio del proprio lavoro."),
    ]
    return regole


def _scegli(regole, quante, riserve):
    attive = sorted(
        [(peso, testo) for condizione, peso, testo in regole if condizione],
        key=lambda x: -x[0],
    )
    scelti = [testo for _, testo in attive[:quante]]
    for riserva in riserve:
        if len(scelti) >= quante:
            break
        if riserva not in scelti:
            scelti.append(riserva)
    return scelti


def _riassunto(risposte, esito, preiscritto):
    d = lambda q: _scelta(risposte, q)
    d6, d7 = _scala(risposte, "D6"), _scala(risposte, "D7")
    gap = bonus_gap(risposte)
    frasi = []

    situazione = SITUAZIONE.get(d("D1"), "non ha indicato la sua situazione")
    archetipo = ARCHETIPI[esito["archetipo"]]["nome"]
    frasi.append("Profilo %s: %s." % (archetipo, situazione))

    if d("D2") == 0:
        frasi.append("Sul futuro professionale ha le idee chiare e vuole diventare più forte nel suo campo.")
    elif d("D2") in (1, 2):
        frasi.append("Vuole cambiare o crescere ma non sa da dove partire.")
    elif d("D2") == 3:
        frasi.append("Per ora pensa solo a concludere quello che ha in mano.")
    elif d("D2") == 4:
        frasi.append("Si dichiara soddisfatto e non interessato a cambiare.")

    if d6 is not None and d7 is not None:
        if gap == 2:
            frasi.append(
                "Mette la crescita a %s su 10 ma si sente pronto solo %s: la distanza fra le due "
                "risposte è il punto su cui far leva." % (d6, d7)
            )
        elif gap == 1:
            frasi.append("Crescita a %s su 10, prontezza a %s: una piccola distanza da colmare." % (d6, d7))
        else:
            frasi.append("Mette crescita (%s) e prontezza (%s) quasi sullo stesso livello." % (d6, d7))

    azione = {
        0: "Ha già investito in formazione.",
        1: "Si sta informando seriamente ma non ha ancora investito.",
        2: "Ci pensa da tempo senza aver mai fatto nulla di concreto.",
        3: "Non ha mai fatto nulla ma dice di voler iniziare ora.",
    }.get(d("D10"))
    if azione:
        frasi.append(azione)

    if d("D13") in (0, 1):
        frasi.append("Il suo lavoro è già esposto all'AI: scrive, comunica, analizza o gestisce.")
    elif d("D13") == 3:
        frasi.append("Fa un lavoro pratico o manuale, quindi il legame con l'AI va costruito.")

    if d("D16") == 0:
        frasi.append("L'idea di restare fermo per 5 anni lo mette molto a disagio.")
    elif d("D16") == 2:
        frasi.append("Restare fermo per 5 anni gli sarebbe indifferente.")

    frasi.append(
        "Ha inviato la pre-iscrizione." if preiscritto
        else "Ha visto il profilo ma non ha ancora inviato la pre-iscrizione."
    )
    return " ".join(frasi)


def genera(risposte, esito, preiscritto=False):
    """Report pronto da leggere prima della chiamata."""
    return {
        "riassunto": _riassunto(risposte, esito, preiscritto),
        "forze": _scegli(
            _regole_forza(risposte), 3,
            [
                "Ha completato tutte e 16 le domande: ha dedicato tempo al test.",
                "Ha lasciato contatti veri per vedere il proprio profilo.",
                "È arrivato in fondo al percorso senza abbandonare.",
            ],
        ),
        "attenzioni": _scegli(
            _regole_attenzione(risposte), 3,
            [
                "Nessun segnale di chiusura evidente: usa la chiamata per capire i tempi.",
                "Verificare a voce quanto tempo può dedicare al percorso.",
                "Approfondire quali aspettative ha rispetto al workshop.",
            ],
        ),
        "risposte_chiave": [
            ("Situazione", _testo_risposta(risposte, "D1")),
            ("Rapporto con la crescita", _testo_risposta(risposte, "D2")),
            ("Cosa ha già fatto", _testo_risposta(risposte, "D10")),
            ("Fra 5 anni tutto uguale", _testo_risposta(risposte, "D16")),
        ],
    }
