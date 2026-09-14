# -*- coding: utf-8 -*-
"""Contenuti testuali del Test Onda: domande, opzioni e varianti di risultato.

Tutto quello che riguarda punteggi, soglie e scelta della variante vive lato
server: il browser riceve solo i testi delle domande e, a fine quiz, il
contenuto già tradotto da mostrare.
"""

# --------------------------------------------------------------------------
# Blocchi
# --------------------------------------------------------------------------

BLOCCHI = {
    "A": {"nome": "Crescita", "icona": "🎯", "classe": "badge-a"},
    "B": {"nome": "Azione", "icona": "💪", "classe": "badge-b"},
    "C": {"nome": "Cambiamento", "icona": "🤖", "classe": "badge-c"},
}

# --------------------------------------------------------------------------
# Le 16 domande
#
# tipo "scelta": lista di opzioni (testo, punti)
# tipo "scala":  scala 1-10; se "punteggia" i punti sono il valore diviso 2,
#                altrimenti la risposta serve solo al calcolo del gap
#
# Nessuna domanda nomina il workshop: il workshop compare solo nella seconda
# schermata di risultato, dopo che la persona ha già visto il proprio profilo.
# --------------------------------------------------------------------------

DOMANDE = [
    {
        "id": "D1",
        "blocco": "A",
        "tipo": "scelta",
        "testo": "Raccontami un po' di te: qual è la tua situazione oggi?",
        "opzioni": [
            ("Studente", 1),
            ("Studio e lavoro", 2),
            ("Lavoro come dipendente", 2),
            ("Libero professionista o attività propria", 2),
            ("Non lavoro e sto cercando", 1),
        ],
    },
    {
        "id": "D2",
        "blocco": "A",
        "tipo": "scelta",
        "testo": "Quando pensi al tuo futuro professionale, cosa senti?",
        "opzioni": [
            ("Voglio crescere e diventare più forte nel mio campo", 4),
            ("Ho un'idea di massima ma non so come muovermi", 3),
            ("Vorrei cambiare ma non so da dove partire", 3),
            ("Il mio unico obiettivo è concludere quello che sto facendo ora", 1),
            ("Sono soddisfatto e non ho interesse a cambiare", 0),
        ],
    },
    {
        "id": "D3",
        "blocco": "A",
        "tipo": "scelta",
        "testo": "C'è qualcosa che oggi ti preoccupa del mondo del lavoro, "
                 "magari pensando all'intelligenza artificiale?",
        "opzioni": [
            ("Sì, mi spaventa molto", 3),
            ("Un po', ma non costantemente", 2),
            ("No, non mi preoccupa", 1),
            ("Non ci ho mai pensato", 1),
        ],
    },
    {
        "id": "D4",
        "blocco": "A",
        "tipo": "scelta",
        "testo": "Ti capita di temere di restare indietro professionalmente?",
        "opzioni": [
            ("Sì, molto", 3),
            ("Un po'", 2),
            ("No, non mi tocca", 0),
        ],
    },
    {
        "id": "D5",
        "blocco": "A",
        "tipo": "scelta",
        "testo": "C'è una parte di te su cui vuoi lavorare "
                 "(mentalità, sicurezza, determinazione)?",
        "opzioni": [
            ("Sì, soprattutto su me stesso", 3),
            ("In parte, più su competenze tecniche", 2),
            ("No, mi sento già pronto", 0),
        ],
    },
    {
        "id": "D6",
        "blocco": "A",
        "tipo": "scala",
        "testo": "Quanto è importante per te crescere professionalmente oggi?",
        "etichetta_min": "Per niente",
        "etichetta_max": "Moltissimo",
        "punteggia": True,
    },
    {
        "id": "D7",
        "blocco": "A",
        "tipo": "scala",
        "testo": "Quanto ti senti già pronto ad affrontare le sfide del tuo settore?",
        "etichetta_min": "Per niente",
        "etichetta_max": "Del tutto",
        "punteggia": False,
    },
    {
        "id": "D8",
        "blocco": "A",
        "tipo": "scelta",
        "testo": "Quando nella vita si presenta un cambiamento importante, "
                 "cosa succede di solito?",
        "opzioni": [
            ("Lo accolgo, anche se spaventa", 3),
            ("All'inizio resisto, ma poi mi adatto", 2),
            ("Preferisco che le cose restino come sono", 1),
            ("Dipende dalla situazione", 0),
        ],
    },
    {
        "id": "D9",
        "blocco": "A",
        "tipo": "scelta",
        "testo": "Quanto sei disposto a fare qualcosa di controcorrente rispetto "
                 "alle tue abitudini, se pensi possa aiutarti a crescere?",
        "opzioni": [
            ("Molto, mi piace mettermi alla prova", 3),
            ("Abbastanza, se capisco il motivo", 2),
            ("Preferisco procedere con gradualità", 1),
            ("Poco, tendo a restare in ciò che conosco", 0),
        ],
    },
    {
        "id": "D10",
        "blocco": "B",
        "tipo": "scelta",
        "testo": "Cosa hai già fatto finora per la tua crescita professionale?",
        "opzioni": [
            ("Ho già investito tempo o denaro in formazione", 4),
            ("Ho iniziato a informarmi seriamente", 3),
            ("Ci penso spesso ma non ho ancora fatto nulla", 1),
            ("Non ho mai fatto nulla ma vorrei iniziare", 2),
        ],
    },
    {
        "id": "D11",
        "blocco": "B",
        "tipo": "scelta",
        "testo": "Quanto senti il bisogno di lavorare su te stesso a un livello "
                 "più profondo (empatia, ascolto, consapevolezza di chi sei)?",
        "opzioni": [
            ("Molto, è fondamentale per la mia crescita", 4),
            ("Un po', ma non ci ho mai dedicato tempo", 3),
            ("Non ci avevo mai pensato in questi termini", 1),
            ("Non credo mi riguardi", 0),
        ],
    },
    {
        "id": "D12",
        "blocco": "B",
        "tipo": "scelta",
        "testo": "Ti riconosci nell'idea di mettere il tuo lavoro al servizio "
                 "di qualcosa di più grande di te?",
        "opzioni": [
            ("Sì, è già profondamente mio", 4),
            ("Mi affascina ma non l'ho esplorato", 2),
            ("Non ci ho mai riflettuto", 0),
            ("Non è un tema che mi interessa", 0),
        ],
    },
    {
        "id": "D13",
        "blocco": "C",
        "tipo": "scelta",
        "testo": "Quanto spazio ha nel tuo lavoro quotidiano scrivere, comunicare, "
                 "analizzare, vendere, gestire persone o progetti?",
        "opzioni": [
            ("Molto", 4),
            ("Abbastanza", 3),
            ("Alcune di queste", 2),
            ("Poco, faccio un lavoro pratico o manuale", 1),
            ("Non saprei dire", 1),
        ],
    },
    {
        "id": "D14",
        "blocco": "C",
        "tipo": "scelta",
        "testo": "Hai notato colleghi del tuo settore usare già strumenti "
                 "di intelligenza artificiale?",
        "opzioni": [
            ("Sì, capita spesso", 3),
            ("Qualche volta", 2),
            ("No, mai", 0),
            ("Non ci ho fatto caso, ma potrebbe essere", 1),
        ],
    },
    {
        "id": "D15",
        "blocco": "C",
        "tipo": "scala",
        "testo": "Quanto ti senti pronto ad affrontare i cambiamenti che "
                 "l'intelligenza artificiale potrebbe portare nel tuo settore?",
        "etichetta_min": "Per niente",
        "etichetta_max": "Del tutto",
        "punteggia": True,
    },
    {
        "id": "D16",
        "blocco": "C",
        "tipo": "scelta",
        "testo": "Se tra 5 anni nulla fosse cambiato nel tuo modo di lavorare, "
                 "mentre tutto intorno a te si trasforma, come ti sentiresti?",
        "opzioni": [
            ("Molto a disagio, sarebbe un problema serio", 3),
            ("Un po' di preoccupazione, ma gestibile", 2),
            ("Indifferente, non cambierebbe molto", 0),
        ],
    },
]

DOMANDE_PER_ID = {d["id"]: d for d in DOMANDE}

# --------------------------------------------------------------------------
# I 3 archetipi e le 6 varianti di risultato
#
# Gli archetipi sono i soli nomi mostrati alla persona: l'etichetta interna
# non compare mai, né in pagina né nel sorgente HTML.
# --------------------------------------------------------------------------

ARCHETIPI = {
    "surfista": {
        "nome": "Surfista",
        "icona": "🏄",
        "descrizione": (
            "Sei salito sulla tavola, e questo già ti distingue da molti. Ma non sei "
            "ancora un surfista esperto: ti muovi, provi, a volte perdi l'equilibrio. "
            "Hai la spinta e il coraggio di stare sull'onda invece di scappare, ora ti "
            "manca solo la tecnica per restarci stabile e portarla dove vuoi tu."
        ),
    },
    "nuotatore": {
        "nome": "Nuotatore",
        "icona": "🏊",
        "descrizione": (
            "Non stai fermo, questo è già molto. Sei in acqua, nuoti, provi a restare "
            "dentro l'onda invece di uscirne. Ma nuotare non è cavalcare: fai fatica, "
            "consumi energie, e senza la tavola giusta rischi di restare a lungo nello "
            "stesso punto, senza portarti davvero avanti."
        ),
    },
    "osservatore": {
        "nome": "Osservatore",
        "icona": "🏖️",
        "descrizione": (
            "Oggi guardi l'onda da fuori, e va bene così: non è il momento sbagliato in "
            "assoluto, è solo un momento diverso. Ma chi osserva senza entrare in acqua, "
            "prima o poi viene raggiunto e travolto comunque, anche restando fermo "
            "sulla riva."
        ),
    },
}

VARIANTI = {
    1: {
        "archetipo": "surfista",
        "punto_a": (
            "Dalle tue risposte emerge un quadro molto chiaro: hai una vera spinta a "
            "crescere professionalmente e non ti accontenti di restare dove sei oggi. "
            "Hai già iniziato a muoverti in questa direzione, e questo dice molto sulla "
            "tua determinazione. In più, il tuo lavoro è già toccato dai cambiamenti che "
            "l'intelligenza artificiale sta portando: significa che il momento per "
            "prepararti è adesso, non tra qualche anno."
        ),
        "messaggio": (
            "Dal test emerge che tu la direzione ce l'hai già chiara: vuoi crescere, e "
            "non ti stai limitando a pensarlo, ti stai già muovendo. Quello che mi "
            "colpisce è che il tuo settore è già dentro al cambiamento che "
            "l'intelligenza artificiale sta portando, anche se magari fino ad oggi non "
            "ci avevi ancora messo a fuoco fino in fondo. Non è un problema, è "
            "un'opportunità: chi se ne accorge prima, parte in vantaggio su tutti "
            "gli altri."
        ),
    },
    2: {
        "archetipo": "surfista",
        "punto_a": (
            "Dalle tue risposte emerge una spinta forte verso la tua crescita "
            "professionale, e la voglia concreta di lavorarci su, non solo di pensarci. "
            "C'è un aspetto su cui vale la pena riflettere ancora: potresti non aver "
            "ancora notato quanto l'intelligenza artificiale stia già cambiando anche "
            "settori che sembrano lontani da questi temi. Spesso è proprio chi si sente "
            "più 'al sicuro' da certi cambiamenti a scoprire, approfondendo, che in "
            "realtà lo riguardano più di quanto pensasse."
        ),
        "messaggio": (
            "Dal test emerge che la tua spinta a crescere è forte, e soprattutto "
            "concreta: non ti limiti a pensarci, ti stai già muovendo. C'è un aspetto su "
            "cui vale la pena aprire gli occhi: l'intelligenza artificiale potrebbe "
            "riguardare il tuo lavoro più di quanto pensi oggi. Spesso è proprio chi si "
            "sente più al sicuro a scoprire, guardando più da vicino, che il cambiamento "
            "lo tocca comunque."
        ),
    },
    3: {
        "archetipo": "nuotatore",
        "punto_a": (
            "Dalle tue risposte emerge chiaramente che il tema della tua crescita "
            "professionale ti sta a cuore, e non poco. Quello che noto è che finora "
            "questa spinta non si è ancora trasformata in azioni concrete: è normale, "
            "spesso manca solo l'occasione o il contesto giusto per iniziare davvero."
        ),
        "messaggio": (
            "Dal test emerge che il tema della tua crescita professionale ti sta davvero "
            "a cuore. Quello che noto è che questa spinta, finora, non si è ancora "
            "trasformata in azioni concrete. Non è un difetto, è semplicemente la fase "
            "in cui sei: a volte basta il contesto giusto, il momento giusto, per "
            "iniziare a muoversi davvero."
        ),
    },
    4: {
        "archetipo": "nuotatore",
        "punto_a": (
            "Dalle tue risposte emerge una grande apertura a metterti in gioco e "
            "lavorare su di te, questo è un punto di forza importante. Allo stesso "
            "tempo, il tuo rapporto con il futuro professionale sembra ancora un po' un "
            "punto di domanda: non hai completamente chiaro cosa vuoi diventare o dove "
            "vuoi arrivare, ed è una sensazione più comune di quanto sembri."
        ),
        "messaggio": (
            "Dal test emerge che sei una persona aperta a mettersi in gioco, e questo è "
            "già un punto di forza importante. Allo stesso tempo, il tuo rapporto con il "
            "futuro professionale è ancora un po' un punto di domanda: non hai del tutto "
            "chiaro cosa vuoi diventare o dove vuoi arrivare. È una sensazione più "
            "comune di quanto sembri, e va bene attraversarla senza fretta."
        ),
    },
    5: {
        "archetipo": "osservatore",
        "punto_a": (
            "Dalle tue risposte emerge che, oggi, il tema della crescita professionale "
            "non è la tua priorità, e va benissimo così: ognuno ha i propri tempi e i "
            "propri obiettivi del momento."
        ),
        "messaggio": (
            "Dal test emerge che oggi le tue priorità sono altre, e va benissimo così. "
            "Non tutti i momenti sono quelli giusti per pensare al proprio futuro "
            "professionale, ognuno ha le sue priorità del momento. Se vuoi scendere in "
            "acqua, il workshop 'Professionista del Futuro' è pensato anche per chi "
            "vuole muovere il primo passo."
        ),
    },
    6: {
        "archetipo": "osservatore",
        "punto_a": (
            "Dalle tue risposte emerge che stai attraversando un momento in cui cerchi "
            "qualcosa, ma forse non ancora uno spazio in cui metterti attivamente in "
            "gioco, e va bene anche questo: non tutti i momenti sono quelli giusti per "
            "un percorso impegnativo."
        ),
        "messaggio": (
            "Dal test emerge che stai attraversando un momento in cui cerchi qualcosa, "
            "ma probabilmente non ancora uno spazio in cui metterti attivamente in "
            "gioco. È del tutto normale, non tutti i momenti sono quelli giusti per un "
            "percorso impegnativo. Se vuoi scendere in acqua, il workshop "
            "'Professionista del Futuro' è pensato anche per chi vuole muovere il "
            "primo passo."
        ),
    },
}

# --------------------------------------------------------------------------
# Blocco workshop, identico per tutti e tre gli archetipi
# --------------------------------------------------------------------------

WORKSHOP = {
    "eyebrow": "IL PROSSIMO PASSO",
    "titolo": "Workshop 'Professionista del Futuro'",
    "sottotitolo": "22-25 Ottobre, Online, Gratuito",
    "paragrafo": (
        "Quattro giorni per imparare a cavalcare l'onda del cambiamento invece di "
        "subirla, partendo da chi sei e da dove vuoi arrivare."
    ),
    "teaser": [
        ("🌍", "Il mondo del lavoro è già cambiato, anche se non sempre si vede"),
        ("🤖", "Come l'intelligenza artificiale sta ridisegnando ogni professione"),
        ("⭐", "Perché da qui in avanti verranno premiati solo i professionisti eccezionali"),
        ("🧭", "Come si lavora prima dentro di sé, sulla mentalità e sulla direzione"),
        ("🏄", "Come si porta quel lavoro fuori, nella professione di tutti i giorni"),
    ],
    "nota": (
        "Cliccando invii una pre-iscrizione, non una conferma automatica: un coach del "
        "team ti ricontatta su WhatsApp entro 48 ore per completare l'iscrizione."
    ),
    "cta": "Invia la pre-iscrizione",
}
