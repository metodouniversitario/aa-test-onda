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
            ("Sono libero professionista / ho un'attività mia", 2),
            ("Non lavoro, sto cercando", 1),
        ],
    },
    {
        "id": "D2",
        "blocco": "A",
        "tipo": "scelta",
        "testo": "Quando pensi al tuo futuro professionale, cosa senti? "
                 "Qual è oggi il tuo rapporto con la tua crescita?",
        "opzioni": [
            ("Voglio crescere, migliorare, diventare un professionista più forte e riconosciuto nel mio campo", 4),
            ("Ho un'idea di massima ma non so bene come muovermi", 3),
            ("Vorrei cambiare ma non so da dove partire", 3),
            ("Per ora il mio unico obiettivo è concludere ciò che sto facendo ora, non penso oltre", 1),
            ("Sono soddisfatto di dove sono e non ho interesse a cambiare o crescere professionalmente", 0),
        ],
    },
    {
        "id": "D3",
        "blocco": "A",
        "tipo": "scelta",
        "testo": "C'è qualcosa che oggi ti preoccupa un po' del mondo del lavoro, magari "
                 "pensando anche a come sta cambiando con l'intelligenza artificiale?",
        "opzioni": [
            ("Sì, mi spaventa molto, ci penso spesso", 3),
            ("Un po', ma non ci penso costantemente", 2),
            ("No, non mi preoccupa particolarmente", 1),
            ("Non ci ho mai pensato", 1),
        ],
    },
    {
        "id": "D4",
        "blocco": "A",
        "tipo": "scelta",
        "testo": "Ti capita di temere di restare indietro, o di non riuscire a emergere "
                 "nella tua professione?",
        "opzioni": [
            ("Sì, mi spaventa molto", 3),
            ("Un po'", 2),
            ("No, non mi tocca", 0),
        ],
    },
    {
        "id": "D5",
        "blocco": "A",
        "tipo": "scelta",
        "testo": "C'è una parte di te su cui senti di voler lavorare, come la mentalità, "
                 "la sicurezza in te stesso, la determinazione, per crescere professionalmente?",
        "opzioni": [
            ("Sì, sento di dover lavorare soprattutto su me stesso", 3),
            ("In parte, il mio focus è più su competenze tecniche/pratiche", 2),
            ("No, mi sento già pronto su questo fronte", 0),
        ],
    },
    {
        "id": "D6",
        "blocco": "A",
        "tipo": "scala",
        "testo": "Quanto è importante per te, oggi, crescere professionalmente e diventare "
                 "la versione migliore di te stesso nel tuo lavoro o progetto?",
        "etichetta_min": "Per niente importante",
        "etichetta_max": "Estremamente importante",
        "punteggia": True,
    },
    {
        "id": "D7",
        "blocco": "A",
        "tipo": "scala",
        "testo": "E quanto ti senti pronto, oggi, ad affrontare le sfide e i cambiamenti "
                 "del tuo settore nei prossimi anni?",
        "etichetta_min": "Per niente pronto",
        "etichetta_max": "Completamente pronto",
        "punteggia": False,
    },
    {
        "id": "D8",
        "blocco": "A",
        "tipo": "scelta",
        "testo": "Quando nella vita si presenta un cambiamento importante, "
                 "cosa succede di solito?",
        "opzioni": [
            ("Lo accolgo, anche se spaventa, perché so che aiuta a crescere", 3),
            ("All'inizio resisto, ma poi trovo il modo di adattarmi", 2),
            ("Preferisco che le cose restino come sono, il cambiamento mi destabilizza", 1),
            ("Dipende molto dalla situazione", 0),
        ],
    },
    {
        "id": "D9",
        "blocco": "A",
        "tipo": "scelta",
        "testo": "Quanto sei disposto a fare qualcosa di controcorrente rispetto "
                 "alle tue abitudini, se pensi possa aiutarti a crescere?",
        "opzioni": [
            ("Molto, mi piace mettermi alla prova uscendo dagli schemi", 3),
            ("Abbastanza, se capisco bene il motivo", 2),
            ("Preferisco procedere con gradualità, senza troppi stravolgimenti", 1),
            ("Poco, tendo a restare in ciò che conosco", 0),
        ],
    },
    {
        "id": "D10",
        "blocco": "B",
        "tipo": "scelta",
        "testo": "Cosa hai già fatto, finora, per prenderti cura della tua crescita professionale?",
        "opzioni": [
            ("Ho già investito tempo/denaro in formazione, corsi, percorsi, coaching", 4),
            ("Ho iniziato a informarmi seriamente ma non ho ancora investito concretamente", 3),
            ("Ci penso spesso ma non ho ancora fatto nulla di concreto", 1),
            ("Non ho mai fatto nulla, ma vorrei iniziare ora", 2),
        ],
    },
    {
        "id": "D11",
        "blocco": "B",
        "tipo": "scelta",
        "testo": "Oltre alle competenze tecniche, quanto senti il bisogno di lavorare su te "
                 "stesso a un livello più profondo, per esempio su empatia, ascolto, "
                 "consapevolezza di chi sei davvero?",
        "opzioni": [
            ("Molto, sento che è una parte fondamentale della mia crescita", 4),
            ("Un po', anche se non ci ho mai dedicato tempo vero", 3),
            ("Non ci avevo mai pensato in questi termini", 1),
            ("Non credo mi riguardi", 0),
        ],
    },
    {
        "id": "D12",
        "blocco": "B",
        "tipo": "scelta",
        "testo": "Ti riconosci nell'idea di mettere il tuo lavoro e il tuo talento al servizio "
                 "di qualcosa di più grande di te, non solo del tuo interesse personale?",
        "opzioni": [
            ("Sì, è qualcosa che sento già profondamente mio", 4),
            ("Mi affascina, ma non l'ho ancora esplorato davvero", 2),
            ("Non ci ho mai riflettuto", 0),
            ("Non è un tema che mi interessa", 0),
        ],
    },
    {
        "id": "D13",
        "blocco": "C",
        "tipo": "scelta",
        "testo": "Nella tua attività di tutti i giorni, quanto spazio hanno cose come scrivere, "
                 "comunicare, analizzare, creare contenuti, vendere, gestire persone o progetti?",
        "opzioni": [
            ("Molto, è gran parte di quello che faccio", 4),
            ("Abbastanza, una parte significativa", 3),
            ("Alcune di queste", 2),
            ("Poco, il mio lavoro è soprattutto pratico/manuale", 1),
            ("Non saprei dire", 1),
        ],
    },
    {
        "id": "D14",
        "blocco": "C",
        "tipo": "scelta",
        "testo": "Ti è mai capitato di notare colleghi, altri professionisti del tuo settore, "
                 "usare già strumenti di intelligenza artificiale per lavorare in modo più efficace?",
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
        "testo": "Quanto ti senti pronto, oggi, ad affrontare i cambiamenti che l'intelligenza "
                 "artificiale potrebbe portare nel tuo settore?",
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
            ("Indifferente, non cambierebbe molto per me", 0),
        ],
    },
]

DOMANDE_PER_ID = {d["id"]: d for d in DOMANDE}

# Come i tre assi vengono chiamati nella schermata di risultato: durante il quiz
# i badge restano Crescita, Azione e Cambiamento, nel risultato diventano questi.
MACROAREE = {
    "A": {"icona": "🔥", "nome": "Spinta alla crescita"},
    "B": {"icona": "💪", "nome": "Prontezza ad agire"},
    "C": {"icona": "🤖", "nome": "Consapevolezza del cambiamento"},
}

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
        "preambolo": "workshop",
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
        "preambolo": "workshop",
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
        "preambolo": "workshop",
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
        "preambolo": "workshop",
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
        "preambolo": "pratica",
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
        "preambolo": "pratica",
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
    "titolo": "🌊 Workshop \u201cProfessionista del Futuro\u201d",
    "sottotitolo": "22-25 Ottobre · 20.00-22.00 · Online · Gratuito",
    "paragrafo": (
        "Quattro giorni per imparare a cavalcare l'onda del cambiamento: intelligenza "
        "artificiale, ma anche intelligenza emotiva, elemento umano, e il coraggio di "
        "uscire dalla tua zona di comfort per tornare a chi sei davvero."
    ),
    "teaser_intro": "📌 Questo è solo l'inizio. Al workshop \u201cProfessionista del Futuro\u201d scoprirai:",
    "teaser": [
        "🌍 Perché il mondo del lavoro non sta cambiando: è già cambiato, e conta capire da che parte stare",
        "🤖 Come l'intelligenza artificiale e i nuovi strumenti stanno già ridisegnando ogni professione, inclusa la tua",
        "💪 Perché solo i professionisti eccezionali verranno premiati, e cosa significa esserlo davvero",
        "🌊 Come cavalcare il cambiamento invece di subirlo, lavorando prima \u201cdentro\u201d e poi \u201cfuori\u201d",
    ],
    "nota": (
        "Cliccando qui sotto invii la tua pre-iscrizione: non sei ancora iscritto "
        "automaticamente. Un coach ti contatterà su WhatsApp al più presto per "
        "confermare la tua partecipazione."
    ),
    "cta": "Invia la pre-iscrizione",
}

# Copy della landing, parola per parola come da istruzioni
LANDING = {
    "eyebrow": "QUIZ PROFESSIONISTA DEL FUTURO, GRATUITO",
    "titolo": "Sei pronto a diventare il Professionista del Futuro?",
    "sottotitolo": (
        "L'intelligenza artificiale è come un'onda 🌊\n"
        "Sta arrivando, anzi è già arrivata, anche se non te ne sei ancora accorto.\n"
        "Non è per forza una cosa negativa: puoi scegliere di cavalcarla, oppure "
        "lasciarti travolgere.\n"
        "Con questa rivoluzione non basta più essere sufficienti, quella la garantisce "
        "già l'AI. Serve essere molto bravi per fare la differenza.\n"
        "Rispondi a poche domande e scopri il tuo punto di partenza."
    ),
    "meta": ["🔢 16 domande", "🕒 6 minuti", "📊 profilo personalizzato"],
    "label_nome": "COME TI CHIAMI? (NOME E COGNOME)",
    "placeholder_nome": "es. Mario Rossi",
    "cta": "Inizia il quiz",
}

FOOTER = "© Andrea Acconcia — Il Coach dell'Anima · dal 2015 ⭐⭐⭐"

FIRMA_ANDREA = "ANDREA ACCONCIA · IL COACH DELL'ANIMA"

# Il preambolo del messaggio di Andrea cambia fra i primi quattro profili e
# l'Osservatore, come da istruzioni.
PREAMBOLO_ANDREA = {
    "workshop": (
        "Ciao {nome}, qui sotto ti scrivo un po' di cose che emergono dalle tue "
        "risposte, ma la cosa migliore è viverle direttamente al workshop:"
    ),
    "pratica": (
        "Ciao {nome}, qui sotto ti scrivo un po' di cose che emergono dalle tue "
        "risposte, ma la cosa migliore è passare alla pratica:"
    ),
}
