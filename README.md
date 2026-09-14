# Test Onda

Quiz di prequalifica per il workshop gratuito "Professionista del Futuro" di Andrea Acconcia
(Il Coach dell'Anima). Implementazione a partire dalla specifica in
[`risorsa_progetto/test_onda_logica_e_contenuti_CORRETTO.md`](risorsa_progetto/test_onda_logica_e_contenuti_CORRETTO.md).

Funnel: landing, 16 domande, raccolta contatti, risultato con profilo, presentazione del
workshop, pre-iscrizione, contatto su WhatsApp a cura del team.

## Avvio

Serve solo Python 3.8 o successivo, nessuna dipendenza esterna.

```bash
python3 server.py
# http://localhost:8000
```

Variabili di ambiente:

| Variabile | Default | A cosa serve |
|---|---|---|
| `TEST_ONDA_PORT` | `8000` | porta di ascolto |
| `TEST_ONDA_HOST` | `0.0.0.0` | indirizzo di ascolto |
| `TEST_ONDA_ADMIN_PASSWORD` | `onda` | password dell'area team (da cambiare prima del lancio) |
| `TEST_ONDA_DATA_DIR` | `./dati` | cartella di database e coda WhatsApp |

Test:

```bash
python3 -m unittest test_test_onda
```

## File

| File | Contenuto |
|---|---|
| `server.py` | rotte, rendering delle pagine, sessioni, area team, export CSV |
| `contenuti.py` | testi: 16 domande con opzioni e punti, 3 archetipi, 6 varianti, blocco workshop |
| `punteggio.py` | soglie, bonus gap, etichetta interna, scelta della variante |
| `archivio.py` | SQLite (sessioni e submission) e coda WhatsApp su file |
| `statico/stile.css` | linguaggio grafico del brand |
| `test_test_onda.py` | test del flusso completo e della logica di punteggio |
| `risorsa_progetto/` | documenti di riferimento su logica e contenuti |

## Regole di prodotto rispettate dal codice

1. **Il quiz non esclude nessuno.** Qualunque sia il risultato, la persona arriva in fondo,
   vede il proprio profilo e trova sempre il bottone di pre-iscrizione attivo. L'etichetta
   interna serve solo al team per organizzare il follow-up. Il test
   `test_ogni_combinazione_produce_un_profilo` verifica che non esista un percorso di risposte
   che porti a un vicolo cieco.
2. **Il workshop non viene mai nominato prima del risultato.** Landing, 16 domande e pagina
   contatti non lo citano. Compare solo nella seconda schermata di risultato, e nel messaggio
   di Andrea delle varianti 5 e 6 che la introduce.
3. **Niente punteggi nel browser.** Calcolo, soglie, etichetta interna e scelta della variante
   vivono solo lato server: il browser riceve i testi delle domande e, alla fine, il contenuto
   già tradotto. Il test del flusso completo controlla che nel sorgente HTML di tutte le pagine
   non compaiano mai punteggi grezzi, livelli interni o parole come "escluso" o "idoneo".
4. **Il punteggio viene calcolato solo dopo la raccolta contatti**, e il risultato non è
   raggiungibile senza aver lasciato i contatti.

## Logica in breve

Tre blocchi: Crescita (D1-D9, massimo 26 più 2 di bonus gap), Azione (D10-D12, massimo 12),
Cambiamento (D13-D16, massimo 15). Il bonus gap nasce dalla distanza fra D6 (quanto conta
crescere) e D7 (quanto la persona si sente già pronta): differenza di 3 o più vale 2 punti,
di 1 o 2 vale 1 punto.

Ogni blocco diventa un livello (alto, medio, basso), i tre livelli diventano una etichetta
interna, e da questa esce una delle 6 varianti di testo, raggruppate in 3 archetipi:
Surfista, Nuotatore, Osservatore. Alla persona vengono mostrati solo il nome dell'archetipo,
tre valori su 10 con etichetta discorsiva, il punto di partenza e il messaggio di Andrea.

## Area team

`/admin`, protetta da password (autenticazione HTTP di base, password in
`TEST_ONDA_ADMIN_PASSWORD`): tabella delle submission con contatti, punteggi per blocco,
etichetta interna, variante e stato della pre-iscrizione. Export completo, risposta per
risposta, su `/admin/export.csv`.

## Punti aperti e scelte di implementazione

- **WhatsApp non è collegato a nessun provider.** Alla pre-iscrizione il contatto viene
  accodato in `dati/coda_whatsapp.log`, una riga JSON per persona, pronto per essere ripreso
  da una integrazione futura (Twilio, 360dialog, WhatsApp Business API o una automazione tipo
  Make e Zapier). Resta una decisione da prendere con il team per il lancio.
- **Valori mostrati nel risultato.** La specifica elenca, per ogni variante, una terna di
  valori fissa, ma in un paio di casi quella terna non coincide con i livelli che la variante
  può davvero avere (per esempio la variante 2 appartiene al Surfista, dove Cambiamento non
  può essere basso). I tre valori mostrati sono quindi calcolati dai livelli reali della
  persona, seguendo la tabella di traduzione della specifica, mentre i testi delle varianti
  restano esatti. Così ogni profilo resta coerente con le risposte date.
- **Bottone "Indietro".** Conserva le risposte già date ed è sempre attivo: dalla prima
  domanda riporta alla landing. L'attributo `disabled` non viene mai scritto vuoto, che era la
  causa del bug storico: l'helper `attributo()` in `server.py` omette del tutto gli attributi
  senza valore. Il comportamento è coperto dal test `test_bottone_indietro_conserva_la_risposta`.
- **Nessun CRM collegato.** L'area team è pensata per la fase di test.
