# Test Onda: logica, contenuti e stato del progetto

Questo documento riassume tutto quello che serve per parlare del quiz "Test Onda" in una chat
normale, senza bisogno di leggere codice: come funziona, cosa dice all'utente, cosa è cambiato nel
tempo e cosa resta da sistemare. È scritto per essere caricato come risorsa in un progetto Claude e
discusso lì (contenuti, logica, decisioni), non per sviluppare tecnicamente: per quello c'è la
cartella `claude_code` con i file sorgente e le istruzioni tecniche originali.

**Nota su questa versione del documento:** è la revisione corretta e completa, verificata riga per
riga contro il codice sorgente reale (`server.py`) del progetto. In fondo (sezione 10) trovi il
confronto puntuale con una bozza di riepilogo precedente che conteneva alcune imprecisioni.

---

## 1. Cos'è il Test Onda

È un quiz di prequalifica per il workshop gratuito "Professionista del Futuro" di Andrea Acconcia
(Il Coach dell'Anima). Si inserisce in questo funnel:

```
Post sui social -> CTA "Fai il test" -> quiz di 16 domande (nessun riferimento al workshop)
-> raccolta contatti -> risultato personalizzato (profilo + punteggi)
-> SOLO ORA si presenta il workshop -> bottone "pre-iscriviti" -> contatto su WhatsApp
```

Il quiz si presenta all'utente come un test di autoconoscenza professionale legato alla metafora
dell'onda (l'intelligenza artificiale come onda che arriva: si può scegliere di cavalcarla o
esserne travolti). Il workshop non viene mai nominato durante le domande: compare solo nella
schermata di risultato finale, dopo che la persona ha già visto il proprio profilo.

**C'è una sola versione in uso: 16 domande.** Non esistono una "versione A" e una "versione B"
separate: il quiz è passato da 14 a 16 domande nel corso dello sviluppo (aggiungendo 4 domande
nuove e riformulandone alcune), ma si tratta di un'unica linea di evoluzione, non di due prodotti
alternativi. I documenti storici a 14 domande restano nella cartella `risorsa_progetto` solo come
riferimento del percorso fatto, non come alternativa valida.

## 2. Il "perché" dietro la scelta più importante: il quiz non esclude più nessuno

Questo è il punto che è cambiato di più durante lo sviluppo, ed è importante capirlo perché guida
tutta la logica sotto.

**Versione iniziale:** il quiz nasceva come strumento di selezione. I blocchi Crescita e Azione
erano pensati come "eliminatori": chi otteneva un punteggio basso su questi due assi non veniva più
fatto proseguire verso l'iscrizione, con l'obiettivo dichiarato di evitare gli "scappati di casa"
(persone poco in target, curiose, o in cerca solo di contenuto gratuito).

**Versione attuale (quella in uso):** questa logica è stata esplicitamente ribaltata. Ora il quiz
non seleziona ed esclude nessuno. Qualsiasi cosa risponda, la persona arriva sempre alla fine, vede
sempre il proprio profilo personalizzato, e può sempre cliccare il bottone di pre-iscrizione: non
esistono varianti "senza CTA" o "con CTA disabilitata". Il punteggio interno (verde/giallo/rosso)
non è più un cancello: è diventato solo un'etichetta a uso del team, per dare priorità al follow-up
(a chi ricontattare per primo su WhatsApp, con quale tono). La logica di calcolo interna (le
formule, le soglie) è rimasta sostanzialmente la stessa della prima versione: è cambiato il
significato che le viene attribuito, non i numeri.

Perché questo cambiamento ha senso: se il quiz esclude qualcuno silenziosamente (senza dirglielo,
come da requisito di design), quella persona non riceve comunque nessun feedback e il quiz perde
valore per lei. Trasformando il punteggio da filtro a segmentazione interna, ogni persona riceve
comunque il proprio "Punto A" (il profilo), e il team può comunque dare priorità di follow-up a chi
ha il pain più alto, senza dover scartare nessuno a livello di prodotto.

## 3. Le 16 domande, domanda per domanda, con i punti di ciascuna risposta

Le domande sono divise in 3 blocchi, ciascuno con un'etichetta e un colore mostrati come badge
durante il quiz. Nessuna delle 16 domande nomina mai il workshop o "Professionista del Futuro": due
domande del blocco Azione lo nominavano esplicitamente in una fase precedente e sono state
riscritte apposta (dettaglio in D11 e D12 sotto).

I punteggi che seguono sono presi direttamente dal codice del server: sono quelli realmente
applicati, non un'approssimazione.

### 🎯 Blocco A, Crescita (9 domande, D1-D9): massimo 26 punti + fino a 2 di bonus, totale 28

Misura quanta voglia reale la persona ha di crescere professionalmente. Le domande D8 e D9 sono
state aggiunte in un secondo momento (la prima versione ne aveva 7) per aggiungere una componente
più emotiva.

- **D1**, "Raccontami un po' di te: qual è la tua situazione oggi?": Studente = 1, Studio e lavoro
  = 2, Lavoro come dipendente = 2, Libero professionista/attività propria = 2, Non lavoro/sto
  cercando = 1. (Domanda di contesto, il punteggio non premia una situazione più di un'altra.)
- **D2**, "Quando pensi al tuo futuro professionale, cosa senti?": Voglio crescere e diventare più
  forte nel mio campo = 4, Ho un'idea di massima ma non so come muovermi = 3, Vorrei cambiare ma non
  so da dove partire = 3, Il mio unico obiettivo è concludere quello che sto facendo ora = 1, Sono
  soddisfatto e non ho interesse a cambiare = 0.
- **D3**, "C'è qualcosa che oggi ti preoccupa del mondo del lavoro, magari pensando all'AI?": Sì mi
  spaventa molto = 3, Un po' ma non costantemente = 2, No non mi preoccupa = 1, Non ci ho mai
  pensato = 1.
- **D4**, "Ti capita di temere di restare indietro professionalmente?": Sì molto = 3, Un po' = 2,
  No non mi tocca = 0.
- **D5**, "C'è una parte di te su cui vuoi lavorare (mentalità, sicurezza, determinazione)?": Sì
  soprattutto su me stesso = 3, In parte, più su competenze tecniche = 2, No mi sento già pronto =
  0.
- **D6** (scala 1-10), "Quanto è importante per te crescere professionalmente oggi?": punti = valore
  scelto diviso 2, quindi da 0,5 a 5 punti.
- **D7** (scala 1-10), "Quanto ti senti già pronto ad affrontare le sfide del tuo settore?": non
  assegna punti diretti, serve solo a calcolare la distanza (il "gap") con D6.
- **D8**, "Quando nella vita si presenta un cambiamento importante, cosa succede di solito?": Lo
  accolgo anche se spaventa = 3, All'inizio resisto ma poi mi adatto = 2, Preferisco che le cose
  restino come sono = 1, Dipende dalla situazione = 0.
- **D9**, "Quanto sei disposto a fare qualcosa di controcorrente rispetto alle tue abitudini, se
  pensi possa aiutarti a crescere?": Molto, mi piace mettermi alla prova = 3, Abbastanza se capisco
  il motivo = 2, Preferisco procedere con gradualità = 1, Poco, tendo a restare in ciò che conosco =
  0.

**Il bonus "gap" (D6 meno D7):** se la persona dice che crescere è molto importante (es. 9 su D6) ma
si sente poco pronta (es. 3 su D7), quella distanza è un segnale forte di pain reale. Differenza di
3 o più: +2 punti bonus. Differenza di 1 o 2: +1 punto bonus. Nessuna differenza, o D7 maggiore di
D6: nessun bonus.

Soglie sul totale (max 28 con bonus): 19 o più = ALTO, tra 10 e 18 = MEDIO, 9 o meno = BASSO.

### 💪 Blocco B, Azione (3 domande, D10-D12): massimo 12 punti

Misura quanto la persona è concreta, non solo interessata a parole. **D11 e D12 in origine
nominavano il workshop esplicitamente** ("Se durante il workshop... come ti sentiresti?", "Cosa
vorresti trovare in Professionista del Futuro?") e sono state riscritte per non farlo mai, spostando
il focus su temi più profondi e trasferibili.

- **D10**, "Cosa hai già fatto finora per la tua crescita professionale?": Ho già investito
  tempo/denaro in formazione = 4, Ho iniziato a informarmi seriamente = 3, Ci penso spesso ma non
  ho ancora fatto nulla = 1, Non ho mai fatto nulla ma vorrei iniziare = 2.
- **D11**, "Quanto senti il bisogno di lavorare su te stesso a un livello più profondo (empatia,
  ascolto, consapevolezza di chi sei)?": Molto, è fondamentale per la mia crescita = 4, Un po', ma
  non ci ho mai dedicato tempo = 3, Non ci avevo mai pensato in questi termini = 1, Non credo mi
  riguardi = 0.
- **D12**, "Ti riconosci nell'idea di mettere il tuo lavoro al servizio di qualcosa di più grande di
  te?": Sì è già profondamente mio = 4, Mi affascina ma non l'ho esplorato = 2, Non ci ho mai
  riflettuto = 0, Non è un tema che mi interessa = 0.

Soglie (max 12): 8 o più = ALTO, tra 4 e 7 = MEDIO, 3 o meno = BASSO.

### 🤖 Blocco C, Cambiamento (4 domande, D13-D16): massimo 15 punti

Misura quanto l'intelligenza artificiale è già, o potrebbe diventare, rilevante per il lavoro della
persona. Le domande sono scritte per far ragionare chi non ci ha mai pensato, non per scartarlo su
una prima risposta negativa (per esempio "non ci ho fatto caso, ma potrebbe essere" vale più di un
secco "no").

- **D13**, "Quanto spazio ha nel tuo lavoro quotidiano scrivere, comunicare, analizzare, vendere,
  gestire persone o progetti?": Molto = 4, Abbastanza = 3, Alcune di queste = 2, Poco, lavoro
  pratico/manuale = 1, Non saprei dire = 1.
- **D14**, "Hai notato colleghi del tuo settore usare già strumenti di intelligenza artificiale?":
  Sì capita spesso = 3, Qualche volta = 2, No mai = 0, Non ci ho fatto caso ma potrebbe essere = 1.
- **D15** (scala 1-10), "Quanto ti senti pronto ad affrontare i cambiamenti che l'AI potrebbe
  portare nel tuo settore?": punti = valore scelto diviso 2, da 0,5 a 5 punti.
- **D16**, "Se tra 5 anni nulla fosse cambiato nel tuo modo di lavorare, mentre tutto intorno a te
  si trasforma, come ti sentiresti?": Molto a disagio, sarebbe un problema serio = 3, Un po' di
  preoccupazione ma gestibile = 2, Indifferente, non cambierebbe molto = 0. Questa domanda ha
  sostituito una versione precedente più neutra ("pensando ai prossimi 3-5 anni, ritieni possibile
  che il tuo lavoro cambi"), riscritta per chiudere il quiz su una nota più intensa.

Soglie (max 15): 10 o più = ALTO, tra 5 e 9 = MEDIO, 4 o meno = BASSO.

## 4. Dall'etichetta interna al profilo mostrato

I tre punteggi (A, B, C) vengono prima tradotti in tre livelli (ALTO/MEDIO/BASSO secondo le soglie
sopra), poi combinati in un'unica etichetta interna a semaforo:

1. Se A è BASSO: 🔴 Rosso, a prescindere dal resto.
2. Se A non è basso ma B è BASSO: 🔴 Rosso comunque.
3. Se A e B sono entrambi ALTI e C non è basso: 🟢 Verde.
4. Tutte le altre combinazioni che superano lo sbarramento iniziale: 🟡 Giallo.

Questa etichetta non compare mai all'utente (né la parola "semaforo", né "idoneo/escluso", né i
numeri grezzi): serve solo al team per dare priorità al follow-up. In parallelo, ogni punteggio
viene tradotto in un valore 1-10 con un'etichetta discorsiva da mostrare in chiaro all'utente (mai
il numero grezzo):

| Blocco | 0 fino a soglia bassa | fascia media | fascia alta |
|---|---|---|---|
| Crescita (max 28) | 3/10, "Agli inizi" (0-9) | 6/10, "In movimento" (10-18) | 9/10, "Molto forte" (19-28) |
| Azione (max 12) | 3/10, "Da risvegliare" (0-3) | 6/10, "Presente" (4-7) | 9/10, "Concreta" (8-12) |
| Cambiamento (max 15) | 3/10, "Da esplorare" (0-4) | 6/10, "In costruzione" (5-9) | 9/10, "Già chiara" (10-15) |

## 5. I 3 archetipi e le 6 varianti di risultato, testo esatto

L'etichetta interna e i tre livelli determinano quale delle 6 varianti di testo mostrare, raggruppate
in 3 archetipi narrativi (mai chiamati "verde/giallo/rosso" davanti all'utente). Sostituire `[Nome]`
con il nome della persona. Ogni variante mostra: i 3 punteggi (icona, valore 1-10, etichetta), la
descrizione del profilo (identica per le due varianti dello stesso archetipo), il "Punto A"
personalizzato, e un messaggio firmato da Andrea che chiude sempre con "Ti ritrovi in questo?".

### 🏄 Il Surfista (corrisponde internamente al Verde)

**Descrizione del profilo, uguale per entrambe le varianti:**
"Sei salito sulla tavola, e questo già ti distingue da molti. Ma non sei ancora un surfista
esperto: ti muovi, provi, a volte perdi l'equilibrio. Hai la spinta e il coraggio di stare sull'onda
invece di scappare, ora ti manca solo la tecnica per restarci stabile e portarla dove vuoi tu."

**Variante 1** (Cambiamento alto): punteggi 9/10, 9/10, 9/10, "Molto forte", "Concreta", "Già
chiara".
Punto A: "Dalle tue risposte emerge un quadro molto chiaro: hai una vera spinta a crescere
professionalmente e non ti accontenti di restare dove sei oggi. Hai già iniziato a muoverti in
questa direzione, e questo dice molto sulla tua determinazione. In più, il tuo lavoro è già toccato
dai cambiamenti che l'intelligenza artificiale sta portando: significa che il momento per
prepararti è adesso, non tra qualche anno."
Messaggio di Andrea: "Dal test emerge che tu la direzione ce l'hai già chiara: vuoi crescere, e non
ti stai limitando a pensarlo, ti stai già muovendo. Quello che mi colpisce è che il tuo settore è
già dentro al cambiamento che l'intelligenza artificiale sta portando, anche se magari fino ad oggi
non ci avevi ancora messo a fuoco fino in fondo. Non è un problema, è un'opportunità: chi se ne
accorge prima, parte in vantaggio su tutti gli altri."

**Variante 2** (Cambiamento basso): punteggi 9/10, 9/10, 3/10, "Molto forte", "Concreta", "Da
esplorare".
Punto A: "Dalle tue risposte emerge una spinta forte verso la tua crescita professionale, e la
voglia concreta di lavorarci su, non solo di pensarci. C'è un aspetto su cui vale la pena riflettere
ancora: potresti non aver ancora notato quanto l'intelligenza artificiale stia già cambiando anche
settori che sembrano lontani da questi temi. Spesso è proprio chi si sente più 'al sicuro' da certi
cambiamenti a scoprire, approfondendo, che in realtà lo riguardano più di quanto pensasse."
Messaggio di Andrea: "Dal test emerge che la tua spinta a crescere è forte, e soprattutto concreta:
non ti limiti a pensarci, ti stai già muovendo. C'è un aspetto su cui vale la pena aprire gli occhi:
l'intelligenza artificiale potrebbe riguardare il tuo lavoro più di quanto pensi oggi. Spesso è
proprio chi si sente più al sicuro a scoprire, guardando più da vicino, che il cambiamento lo tocca
comunque."

### 🏊 Il Nuotatore (corrisponde internamente al Giallo)

**Descrizione del profilo, uguale per entrambe le varianti:**
"Non stai fermo, questo è già molto. Sei in acqua, nuoti, provi a restare dentro l'onda invece di
uscirne. Ma nuotare non è cavalcare: fai fatica, consumi energie, e senza la tavola giusta rischi di
restare a lungo nello stesso punto, senza portarti davvero avanti."

**Variante 3** (Crescita alta, Azione media): punteggi 9/10, 6/10, 6/10, "Molto forte", "Presente",
"In costruzione".
Punto A: "Dalle tue risposte emerge chiaramente che il tema della tua crescita professionale ti sta
a cuore, e non poco. Quello che noto è che finora questa spinta non si è ancora trasformata in
azioni concrete: è normale, spesso manca solo l'occasione o il contesto giusto per iniziare
davvero."
Messaggio di Andrea: "Dal test emerge che il tema della tua crescita professionale ti sta davvero a
cuore. Quello che noto è che questa spinta, finora, non si è ancora trasformata in azioni concrete.
Non è un difetto, è semplicemente la fase in cui sei: a volte basta il contesto giusto, il momento
giusto, per iniziare a muoversi davvero."

**Variante 4** (Crescita media, Azione alta): punteggi 6/10, 9/10, 6/10, "In movimento", "Concreta",
"In costruzione".
Punto A: "Dalle tue risposte emerge una grande apertura a metterti in gioco e lavorare su di te,
questo è un punto di forza importante. Allo stesso tempo, il tuo rapporto con il futuro
professionale sembra ancora un po' un punto di domanda: non hai completamente chiaro cosa vuoi
diventare o dove vuoi arrivare, ed è una sensazione più comune di quanto sembri."
Messaggio di Andrea: "Dal test emerge che sei una persona aperta a mettersi in gioco, e questo è già
un punto di forza importante. Allo stesso tempo, il tuo rapporto con il futuro professionale è
ancora un po' un punto di domanda: non hai del tutto chiaro cosa vuoi diventare o dove vuoi
arrivare. È una sensazione più comune di quanto sembri, e va bene attraversarla senza fretta."

### 🏖️ L'Osservatore (corrisponde internamente al Rosso)

**Descrizione del profilo, uguale per entrambe le varianti:**
"Oggi guardi l'onda da fuori, e va bene così: non è il momento sbagliato in assoluto, è solo un
momento diverso. Ma chi osserva senza entrare in acqua, prima o poi viene raggiunto e travolto
comunque, anche restando fermo sulla riva."

**Variante 5** (Crescita bassa): punteggi 3/10, 6/10, 6/10, "Agli inizi", "Presente", "In
costruzione".
Punto A: "Dalle tue risposte emerge che, oggi, il tema della crescita professionale non è la tua
priorità, e va benissimo così: ognuno ha i propri tempi e i propri obiettivi del momento."
Messaggio di Andrea: "Dal test emerge che oggi le tue priorità sono altre, e va benissimo così. Non
tutti i momenti sono quelli giusti per pensare al proprio futuro professionale, ognuno ha le sue
priorità del momento. Se vuoi scendere in acqua, il workshop 'Professionista del Futuro' è pensato
anche per chi vuole muovere il primo passo."

**Variante 6** (Crescita ok ma Azione bassa): punteggi 6/10, 3/10, 6/10, "In movimento", "Da
risvegliare", "In costruzione".
Punto A: "Dalle tue risposte emerge che stai attraversando un momento in cui cerchi qualcosa, ma
forse non ancora uno spazio in cui metterti attivamente in gioco, e va bene anche questo: non tutti
i momenti sono quelli giusti per un percorso impegnativo."
Messaggio di Andrea: "Dal test emerge che stai attraversando un momento in cui cerchi qualcosa, ma
probabilmente non ancora uno spazio in cui metterti attivamente in gioco. È del tutto normale, non
tutti i momenti sono quelli giusti per un percorso impegnativo. Se vuoi scendere in acqua, il
workshop 'Professionista del Futuro' è pensato anche per chi vuole muovere il primo passo."

**Nota:** nelle varianti 5 e 6 (Osservatore) l'ultima riga del messaggio di Andrea nomina il
workshop per la prima volta. Nelle varianti 1-4 il messaggio di Andrea non lo nomina, perché ne
parla già il blocco che segue subito dopo nella stessa schermata.

## 6. Come si passa dall'etichetta interna alla variante

- Verde con Cambiamento ALTO: Variante 1. Verde con Cambiamento MEDIO: Variante 2. (Il Verde con
  Cambiamento BASSO non può capitare per come è costruita la tabella al punto 4, quindi non serve
  una variante per quel caso.)
- Giallo con Crescita ALTO: Variante 3. Giallo con Crescita MEDIO: Variante 4.
- Rosso con Crescita BASSO: Variante 5. Rosso con Crescita non bassa ma Azione BASSA: Variante 6.

## 7. Il funnel pagina per pagina

1. **Landing**: eyebrow "QUIZ PROFESSIONISTA DEL FUTURO, GRATUITO", titolo "Sei pronto a diventare
   il Professionista del Futuro?", sottotitolo con la metafora dell'onda, meta info (16 domande, 6
   minuti, profilo personalizzato), campo nome e cognome, bottone "Inizia il quiz", firma di Andrea
   in fondo. Anche qui il workshop non viene mai nominato come evento con date e formato.
2. **Le 16 domande**, una per schermata, con barra di progresso, badge di categoria colorato,
   bottone "Indietro" (funzionante, vedi sezione 8), opzioni cliccabili o scala numerica 1-10.
3. **Raccolta contatti** (dopo l'ultima domanda, prima del risultato): titolo "Ci siamo quasi!",
   campi nome/cognome (pre-compilato), email, telefono, checkbox di consenso privacy, bottone
   "Scopri il mio profilo". Ancora nessuna menzione di workshop o WhatsApp qui: il punteggio viene
   calcolato solo a questo punto, dopo aver raccolto i contatti (serve per la lead generation, il
   risultato non è visibile senza aver lasciato i contatti).
4. **Risultato, schermata 1**: eyebrow "IL TUO PROFILO È PRONTO", titolo "Sei un Surfista/
   Nuotatore/Osservatore", i 3 punteggi, descrizione del profilo, Punto A. Ancora nessun workshop.
5. **Risultato, schermata 2**: qui e solo qui compare il workshop per la prima volta. Contiene il
   messaggio personale di Andrea (box con bordo verde, chiuso da "Ti ritrovi in questo?"), seguito
   da un blocco unico e compatto che presenta il workshop, identico per tutti e 3 gli archetipi:
   - Eyebrow "IL PROSSIMO PASSO"
   - Titolo "Workshop 'Professionista del Futuro'", sottotitolo "22-25 Ottobre, Online, Gratuito"
   - Un breve paragrafo ("Quattro giorni per imparare a cavalcare l'onda del cambiamento...")
   - Un box teaser con 5 righe a icone che anticipano i contenuti del workshop (il mondo del lavoro
     è già cambiato, come l'AI sta ridisegnando ogni professione, perché solo i professionisti
     eccezionali verranno premiati, come cavalcare il cambiamento lavorando prima "dentro" e poi
     "fuori")
   - Una nota piccola grigia che chiarisce che cliccare il bottone è solo una pre-iscrizione, non
     una conferma automatica, e che un coach ricontatterà su WhatsApp entro 48 ore
   - Il bottone "Invia la pre-iscrizione", sempre attivo per tutti i profili, e sotto il link
     secondario "Rifai il quiz"

   Nota storica: questa schermata 2 ha sostituito, in due passaggi successivi, una versione
   precedente più lunga e divisa in tre schermate separate (checklist "cosa scoprirai" più banner
   nero "alza la mano" più schermata di conferma finale a parte). È stata compattata in un'unica
   schermata per rendere il funnel più snello. Una revisione intermedia del blocco workshop aveva
   anche una semplice checklist a 3 righe con spunta (date/online/gratuito) al posto del box teaser
   a 5 righe attuale.

## 8. Bug noti e TODO aperti

- **Bug del bottone "Indietro": risolto, confermato nella versione attualmente in uso.** Nella
  prima implementazione, cliccando "Indietro" il bottone non riportava mai alla domanda precedente
  dopo la prima domanda. La causa reale era un dettaglio tecnico banale ma insidioso: il codice
  scriveva l'attributo HTML `disabled` anche quando doveva essere assente, passandogli il valore
  vuoto (`null`), ma il browser interpreta comunque quell'attributo come presente (quindi il
  bottone risultava disabilitato) qualunque cosa gli venga scritta dentro, anche il "vuoto" stesso.
  Il fix è stato: non scrivere affatto l'attributo quando il suo valore è vuoto, invece di scriverci
  dentro un valore vuoto. Verificato dal vivo che ora il bottone funziona e conserva la risposta
  data in precedenza. Se in fase di migrazione il codice viene riscritto da zero in un altro stack,
  vale la pena verificare che questa classe di bug (attributi booleani impostati a un valore vuoto
  invece che omessi del tutto) non si ripresenti.
- **Nessun altro TODO tecnico aperto noto**, al momento dell'ultima verifica manuale (flusso
  completo testato dall'inizio alla fine: landing, 16 domande con avanti e indietro, contatti,
  risultato in 2 schermate, conferma pre-iscrizione, per varie combinazioni di punteggio/variante).
- **Integrazione WhatsApp**: non è mai stata collegata a un provider reale (nessuna credenziale
  disponibile durante lo sviluppo). Il sistema attuale si limita a mettere in coda un record (nome,
  telefono, data e ora) in un file di log, pronto per essere ripreso da un'integrazione futura
  (Twilio, 360dialog, WhatsApp Business API, o un'automazione tipo Make/Zapier). Questo è un punto
  aperto da decidere con il team per il lancio reale, non un bug.
- **Dashboard/export team**: esiste una pagina admin protetta da password con tabella e export CSV
  di tutte le submission (contatti, tutte le risposte, punteggi per blocco, etichetta interna,
  variante assegnata). Non risulta collegata a nessun CRM esterno: è un accesso minimale pensato
  per la fase di test.

## 9. Riferimenti di design e regole trasversali

Il quiz replica il linguaggio grafico di un altro quiz dello stesso brand ("Test DSV", di cui è
allegato un PDF di riferimento nella stessa cartella): header nero fisso con logo tondo e stella
verde, badge pillola col nome del test, palette verde su sfondo verde scuro sfumato per le sezioni
hero, giallo usato con parsimonia, card molto arrotondate, bottoni a pillola con freccia, barra di
progresso sottile, badge di categoria colorati, footer fisso identico in ogni pagina.

In nessun punto del codice HTML o del testo visibile all'utente devono comparire: punteggi grezzi,
la parola "semaforo", "idoneo/non idoneo", "escluso", "priorità" (riferito al lead). Questo vale sia
per il testo visibile sia per il codice sorgente della pagina (un utente tecnicamente curioso non
deve poter dedurre nulla nemmeno guardando "visualizza sorgente"): per questo tutta la logica di
punteggio, soglie e scelta della variante vive solo lato server, e il browser riceve solo i testi
delle domande e, a fine quiz, il contenuto già tradotto da mostrare.

Regole di stile del progetto, valide anche per questo documento: niente doppie desinenze di genere
(niente "o/a", si usa il maschile o formule impersonali).

## 10. Correzioni rispetto a una bozza di riepilogo precedente

Mi hai passato una bozza di riepilogo con alcune parti segnalate come incerte o da recuperare.
Confrontandola col codice reale del progetto, ecco cosa correggo:

- **Non esistono una "Versione A" e una "Versione B" separate.** C'è un solo quiz, passato da 14 a
  16 domande nel corso dello sviluppo. I documenti a 14 domande (`Test_Onda_Documento_Completo` e
  `Test_Onda_Schema_Logico`) restano solo come materiale storico.
- **Non esiste nessun file `build_pdf.py`** da nessuna parte nel progetto: cercato esplicitamente,
  non trovato. Non risulta nemmeno una "sessione del 17 agosto" distinta da quella in cui è stata
  scritta la versione a 16 domande: potrebbe essere una confusione con un'altra conversazione o un
  altro progetto.
- **Le domande D9/D10 riscritte per non nominare il workshop, nella versione a 14 domande, non
  corrispondono esattamente al testo indicato nella bozza precedente.** Il testo realmente
  implementato era ancora quello che nominava il workshop (non risultano mai state riscritte nella
  versione a 14 domande): la correzione è arrivata solo con il passaggio alla versione a 16 domande,
  dove le due domande equivalenti (D11 e D12 del blocco Azione) sono state riscritte da zero con un
  contenuto diverso (vedi sezione 3).
- **Il bug del bottone "Indietro" è risolto**, non più aperto: vedi sezione 8 per il dettaglio
  tecnico e la conferma del test.
- **Il testo esatto delle 6 varianti e il dettaglio domanda per domanda della versione a 16
  domande**, segnalati come mancanti, sono ora completi nelle sezioni 3 e 5 di questo documento,
  presi parola per parola dal codice sorgente.
