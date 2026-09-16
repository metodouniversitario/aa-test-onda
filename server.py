# -*- coding: utf-8 -*-
"""Test Onda: server del quiz di prequalifica per il workshop
"Professionista del Futuro" di Andrea Acconcia.

Solo libreria standard: si avvia con `python3 server.py`.

Regola di prodotto: il quiz non esclude nessuno. Chiunque arriva in fondo, vede
il proprio profilo e può inviare la pre-iscrizione. Punteggi, soglie, etichetta
interna e scelta della variante restano solo lato server: il browser riceve i
testi delle domande e, alla fine, il contenuto già tradotto da mostrare.
"""

import base64
import csv
import hmac
import html
import io
import json
import os
import secrets
import urllib.parse
from http import HTTPStatus
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import archivio
import contenuti
import punteggio
import report

# Railway (e la maggior parte degli hosting) passa la porta in PORT
PORTA = int(os.environ.get("PORT") or os.environ.get("TEST_ONDA_PORT") or 8000)
INDIRIZZO = os.environ.get("TEST_ONDA_HOST", "0.0.0.0")
IN_PRODUZIONE = bool(os.environ.get("RAILWAY_ENVIRONMENT") or os.environ.get("TEST_ONDA_PRODUZIONE"))


def _password_admin():
    """La dashboard contiene dati personali: online non deve mai restare
    protetta da una password di default. Se la variabile di ambiente manca,
    ne viene generata una casuale e stampata nei log di avvio."""
    scelta = os.environ.get("TEST_ONDA_ADMIN_PASSWORD")
    if scelta:
        return scelta, False
    if IN_PRODUZIONE:
        return secrets.token_urlsafe(12), True
    return "onda", False


PASSWORD_ADMIN, PASSWORD_GENERATA = _password_admin()
CARTELLA = os.path.dirname(os.path.abspath(__file__))
TOTALE_DOMANDE = len(contenuti.DOMANDE)


# --------------------------------------------------------------------------
# Helper di rendering
# --------------------------------------------------------------------------

def e(testo):
    return html.escape(str(testo), quote=True)


def attributo(nome, valore):
    """Scrive un attributo solo se ha davvero un valore.

    Gli attributi booleani dell'HTML (`disabled`, `checked`, `selected`) sono
    attivi per il solo fatto di essere presenti, anche con valore vuoto: per
    questo un attributo vuoto non va scritto affatto, invece che scritto vuoto.
    È la classe di bug che bloccava il bottone "Indietro".
    """
    if valore is None or valore is False or valore == "":
        return ""
    if valore is True:
        return " " + nome
    return ' %s="%s"' % (nome, e(valore))


HEADER = """
<header class="header">
  <div class="logo">★</div>
  <div class="logo-testo"><b>ANDREA</b> ACCONCIA<span>IL COACH DELL'ANIMA</span></div>
  <div class="pillola-test">TEST ONDA</div>
</header>
"""

FOOTER = """
<footer class="footer">%s</footer>
""" % contenuti.FOOTER


def pagina(titolo, corpo, progresso=None):
    barra = ""
    if progresso is not None:
        barra = '<div class="progresso"><div style="width:%d%%"></div></div>' % progresso
    return """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>%s</title>
<link rel="stylesheet" href="/statico/stile.css">
</head>
<body>
<div class="pagina">
%s%s
%s
%s
</div>
</body>
</html>""" % (e(titolo), HEADER, barra, corpo, FOOTER)


# --------------------------------------------------------------------------
# Pagine
# --------------------------------------------------------------------------

def pagina_landing(errore=None, nome=""):
    blocco_errore = '<div class="errore">%s</div>' % e(errore) if errore else ""
    L = contenuti.LANDING
    meta = "".join("<span>%s</span>" % e(v) for v in L["meta"])
    corpo = """
<section class="hero">
  <span class="eyebrow">%s</span>
  <h1>%s</h1>
  <p class="sottotitolo-hero">%s</p>
  <div class="meta">%s</div>
</section>
<div class="contenuto stretto">
  <div class="card sollevata">
    %s
    <form method="post" action="/inizia">
      <div class="campo">
        <label for="nome">%s</label>
        <input type="text" id="nome" name="nome" value="%s" placeholder="%s"
               required autocomplete="name">
      </div>
      <button type="submit" class="bottone largo">%s <span>&rarr;</span></button>
    </form>
    <div class="box-autore">
      <div class="avatar">AA</div>
      <div>
        <div class="autore-nome">Andrea Acconcia</div>
        <div class="autore-ruolo">IL COACH DELL'ANIMA · DAL 2015</div>
      </div>
    </div>
  </div>
</div>
""" % (
        e(L["eyebrow"]), e(L["titolo"]), e(L["sottotitolo"]), meta, blocco_errore,
        e(L["label_nome"]), e(nome), e(L["placeholder_nome"]), e(L["cta"]),
    )
    return pagina("Test Onda", corpo)


def pagina_domanda(indice, risposta_salvata):
    domanda = contenuti.DOMANDE[indice]
    blocco = contenuti.BLOCCHI[domanda["blocco"]]
    numero = indice + 1
    percentuale = int(round(numero / TOTALE_DOMANDE * 100))

    if domanda["tipo"] == "scala":
        pulsanti = []
        for valore in range(1, 11):
            classe = "scelta" if risposta_salvata == valore else ""
            pulsanti.append(
                '<button type="submit" name="risposta" value="%d"%s>%d</button>'
                % (valore, attributo("class", classe), valore)
            )
        risposte_html = (
            '<div class="scala-legenda"><span>%s</span><span>%s</span></div>'
            '<div class="scala">%s</div>'
            % (e(domanda["etichetta_min"]), e(domanda["etichetta_max"]), "".join(pulsanti))
        )
    else:
        opzioni = []
        for i, (testo, _punti) in enumerate(domanda["opzioni"]):
            classe = "opzione scelta" if risposta_salvata == i else "opzione"
            opzioni.append(
                '<button type="submit" name="risposta" value="%d" class="%s">%s</button>'
                % (i, classe, e(testo))
            )
        risposte_html = '<div class="opzioni">%s</div>' % "".join(opzioni)

    corpo = """
<div class="contenuto">
  <form method="post" action="/quiz">
    <input type="hidden" name="d" value="%d">
    <div class="riga-progresso">
      <span>DOMANDA %d DI %d</span><span>%d%%</span>
    </div>
    <div class="progresso"><div style="width:%d%%"></div></div>
    <div class="card">
      <div class="riga-alta">
        <button type="submit" name="azione" value="indietro" class="bottone fantasma">&larr; Indietro</button>
        <span class="badge %s">%s %s</span>
      </div>
      <h2>%s</h2>
      %s
    </div>
  </form>
</div>
""" % (
        indice, numero, TOTALE_DOMANDE, percentuale, percentuale,
        e(blocco["classe"]), e(blocco["icona"]), e(blocco["nome"].upper()),
        e(domanda["testo"]), risposte_html,
    )
    return pagina("Test Onda, domanda %d" % numero, corpo)


def pagina_contatti(sessione, errore=None, valori=None):
    valori = valori or {}
    blocco_errore = '<div class="errore">%s</div>' % e(errore) if errore else ""
    corpo = """
<div class="contenuto stretto">
  <div class="card">
    %s
    <h2>Ci siamo quasi!</h2>
    <p class="sottotitolo-card">Inserisci i tuoi dati per conoscere la tua situazione attuale.</p>
    <form method="post" action="/contatti">
      <div class="campo">
        <label for="nome">NOME E COGNOME *</label>
        <input type="text" id="nome" name="nome" value="%s" required autocomplete="name">
      </div>
      <div class="campo">
        <label for="email">EMAIL *</label>
        <input type="email" id="email" name="email" value="%s" placeholder="Es. mario@email.it"
               required autocomplete="email">
      </div>
      <div class="campo">
        <label for="telefono">NUMERO DI TELEFONO *</label>
        <input type="tel" id="telefono" name="telefono" value="%s" placeholder="Es. 333 1234567"
               required autocomplete="tel">
      </div>
      <label class="consenso">
        <input type="checkbox" name="consenso" value="1"%s>
        <span>Do il consenso al trattamento dei miei dati personali secondo i Termini di
        Utilizzo e la Privacy Policy.</span>
      </label>
      <button type="submit" class="bottone largo">Scopri il mio profilo <span>&rarr;</span></button>
    </form>
    <p class="nota centrata">I tuoi dati sono al sicuro e non li condivideremo mai con terzi.</p>
  </div>
</div>
""" % (
        blocco_errore,
        e(valori.get("nome", sessione["nome_completo"])),
        e(valori.get("email", "")),
        e(valori.get("telefono", "")),
        attributo("checked", bool(valori.get("consenso"))),
    )
    return pagina("Test Onda, i tuoi contatti", corpo, 100)


def _blocco_punteggi(esito):
    righe = []
    for chiave in ("A", "B", "C"):
        macroarea = contenuti.MACROAREE[chiave]
        valore, etichetta = esito["mostrati"][chiave]
        righe.append(
            """
      <div class="punteggio">
        <span class="icona">%s</span>
        <span class="nome">%s</span>
        <span class="valore">%d/10<span class="etichetta">%s</span></span>
      </div>"""
            % (e(macroarea["icona"]), e(macroarea["nome"]), valore, e(etichetta))
        )
    return '<div class="punteggi">%s</div>' % "".join(righe)


def pagina_risultato(submission, esito):
    """Profilo, punteggi, messaggio di Andrea e workshop: tutto in una schermata."""
    variante = contenuti.VARIANTI[esito["variante"]]
    archetipo = contenuti.ARCHETIPI[variante["archetipo"]]
    nome = submission["nome"]
    w = contenuti.WORKSHOP

    preambolo = contenuti.PREAMBOLO_ANDREA[variante["preambolo"]].format(nome=nome)
    teaser = "".join("<li>%s</li>" % e(riga) for riga in w["teaser"])

    corpo = """
<section class="hero">
  <span class="eyebrow">IL TUO PROFILO È PRONTO</span>
  <div class="profilo-icona">%s</div>
  <h1>Sei un %s</h1>
  <p>%s, ecco cosa emerge dalle tue risposte:</p>
</section>
<div class="contenuto">
  <div class="card sollevata">
    %s
    <p>%s</p>
    <p>%s</p>
  </div>

  <div class="card">
    <div class="messaggio-andrea">
      <div class="andrea-intestazione">
        <span class="avatar">AA</span>
        <span class="andrea-nome">%s</span>
      </div>
      <p>%s</p>
      <p>%s</p>
      <p><strong>Ti ritrovi in questo?</strong></p>
    </div>
  </div>

  <div class="card">
    <span class="eyebrow scuro">%s</span>
    <h2>%s</h2>
    <div class="data-workshop">%s</div>
    <p>%s</p>
    <div class="teaser">
      <strong>%s</strong>
      <ul>%s</ul>
    </div>
    <p class="nota">%s</p>
    <form method="post" action="/preiscrizione">
      <button type="submit" class="bottone largo">%s <span>&rarr;</span></button>
    </form>
    <a class="link-secondario" href="/rifai">Rifai il quiz</a>
  </div>
</div>
""" % (
        e(archetipo["icona"]),
        e(archetipo["nome"]),
        e(nome),
        _blocco_punteggi(esito),
        e(archetipo["descrizione"]),
        e(variante["punto_a"]),
        e(contenuti.FIRMA_ANDREA),
        e(preambolo),
        e(variante["messaggio"]),
        e(w["eyebrow"]),
        e(w["titolo"]),
        e(w["sottotitolo"]),
        e(w["paragrafo"]),
        e(w["teaser_intro"]),
        teaser,
        e(w["nota"]),
        e(w["cta"]),
    )
    return pagina("Test Onda, il tuo profilo", corpo)


def pagina_conferma(submission):
    corpo = """
<section class="hero">
  <div class="profilo-icona">✅</div>
  <h1>Ci siamo, %s</h1>
  <p>La tua pre-iscrizione al workshop è arrivata.</p>
</section>
<div class="contenuto stretto">
  <div class="card sollevata">
    <h2>Cosa succede adesso</h2>
    <p>Un coach del team ti scrive su WhatsApp al numero che hai lasciato, entro 48 ore,
    per completare l'iscrizione e rispondere alle tue domande.</p>
    <p>Nel frattempo salva le date: <strong>22-25 Ottobre, online</strong>.</p>
    <div class="box-autore">
      <div class="avatar">AA</div>
      <div>
        <div class="autore-nome">Andrea Acconcia</div>
        <div class="autore-ruolo">IL COACH DELL'ANIMA · DAL 2015</div>
      </div>
    </div>
  </div>
</div>
""" % e(submission["nome"])
    return pagina("Test Onda, pre-iscrizione inviata", corpo)


def _riepilogo(righe):
    totale = len(righe)
    preiscritti = sum(1 for r in righe if r["preiscrizione"])
    per_archetipo = {}
    for r in righe:
        per_archetipo[r["archetipo"]] = per_archetipo.get(r["archetipo"], 0) + 1
    tessere = [
        ("Test completati", totale),
        ("Pre-iscrizioni", preiscritti),
    ]
    for chiave in ("surfista", "nuotatore", "osservatore"):
        archetipo = contenuti.ARCHETIPI[chiave]
        tessere.append(
            ("%s %s" % (archetipo["icona"], archetipo["nome"]), per_archetipo.get(chiave, 0))
        )
    return "".join(
        '<div class="statistica"><span class="numero">%s</span><span class="voce">%s</span></div>'
        % (e(valore), e(nome))
        for nome, valore in tessere
    )


def pagina_admin(righe):
    intestazioni = [
        "Data", "Nome", "Email", "Telefono", "Profilo", "Crescita", "Azione",
        "Cambiamento", "Segmento", "Pre-iscrizione", "",
    ]
    celle = "".join("<th>%s</th>" % e(t) for t in intestazioni)
    corpi = []
    for r in righe:
        archetipo = contenuti.ARCHETIPI[r["archetipo"]]
        corpi.append(
            "<tr>" + "".join(
                "<td>%s</td>" % v
                for v in (
                    e(r["creata_il"].replace("T", " ")[:16]),
                    e("%s %s" % (r["nome"], r["cognome"])),
                    e(r["email"]),
                    e(r["telefono"]),
                    "%s %s" % (e(archetipo["icona"]), e(archetipo["nome"])),
                    "%g (%s)" % (r["punti_a"], e(r["livello_a"].lower())),
                    "%g (%s)" % (r["punti_b"], e(r["livello_b"].lower())),
                    "%g (%s)" % (r["punti_c"], e(r["livello_c"].lower())),
                    e(r["etichetta_interna"]),
                    "sì" if r["preiscrizione"] else "no",
                    '<a href="/admin/dettaglio?id=%s">Apri</a>' % e(r["id"]),
                )
            ) + "</tr>"
        )
    if not righe:
        corpi.append('<tr><td colspan="11">Ancora nessun test completato.</td></tr>')
    corpo = """
<div class="contenuto" style="max-width:1200px">
  <div class="card">
    <h2>Dashboard Test Onda</h2>
    <div class="statistiche">%s</div>
    <p style="margin-top:18px"><a class="bottone fantasma" href="/admin/export.csv">Scarica tutto in CSV</a></p>
  </div>
  <div class="card">
    <h2>Chi ha fatto il test</h2>
    <div class="tabella-wrapper">
      <table class="admin"><thead><tr>%s</tr></thead><tbody>%s</tbody></table>
    </div>
  </div>
</div>
""" % (_riepilogo(righe), celle, "".join(corpi))
    return pagina("Test Onda, dashboard", corpo)


def pagina_dettaglio(submission):
    risposte = json.loads(submission["risposte"])
    esito = punteggio.calcola(risposte)
    archetipo = contenuti.ARCHETIPI[submission["archetipo"]]
    scheda = report.genera(risposte, esito, bool(submission["preiscrizione"]))

    elenco = []
    for indice, domanda in enumerate(contenuti.DOMANDE):
        valore = risposte.get(domanda["id"])
        if valore is None:
            testo = "(nessuna risposta)"
        elif domanda["tipo"] == "scala":
            testo = "%s su 10" % valore
        else:
            testo = domanda["opzioni"][valore][0]
        elenco.append(
            "<tr><td>%d</td><td>%s</td><td>%s</td><td><strong>%s</strong></td></tr>"
            % (indice + 1, e(contenuti.BLOCCHI[domanda["blocco"]]["nome"]),
               e(domanda["testo"]), e(testo))
        )

    forze = "".join("<li>%s</li>" % e(t) for t in scheda["forze"])
    attenzioni = "".join("<li>%s</li>" % e(t) for t in scheda["attenzioni"])
    chiave = "".join(
        "<div><span>%s</span>%s</div>" % (e(etichetta), e(valore or "—"))
        for etichetta, valore in scheda["risposte_chiave"]
    )

    corpo = """
<div class="contenuto" style="max-width:900px">
  <div class="card">
    <p><a href="/admin">&larr; Torna alla dashboard</a></p>
    <h2>%s %s</h2>
    <p class="sottotitolo-card">%s · %s<br>Test completato il %s</p>
  </div>

  <div class="card">
    <span class="eyebrow scuro">PRIMA DI CHIAMARE</span>
    <h2>%s %s</h2>
    <p>%s</p>
    <div class="due-colonne">
      <div class="colonna forze">
        <h3>Punti di forza</h3>
        <ul>%s</ul>
      </div>
      <div class="colonna attenzioni">
        <h3>Punti di attenzione</h3>
        <ul>%s</ul>
      </div>
    </div>
    <div class="risposte-chiave">%s</div>
  </div>

  <div class="card">
    <h2>Dati interni</h2>
    <p>Variante %d, segmento %s<br>
    Crescita %g (%s), Azione %g (%s), Cambiamento %g (%s), bonus gap %g<br>
    Pre-iscrizione: <strong>%s</strong></p>
  </div>

  <div class="card">
    <h2>Tutte le risposte</h2>
    <div class="tabella-wrapper">
      <table class="admin">
        <thead><tr><th>#</th><th>Blocco</th><th>Domanda</th><th>Risposta</th></tr></thead>
        <tbody>%s</tbody>
      </table>
    </div>
  </div>
</div>
""" % (
        e(submission["nome"]), e(submission["cognome"]),
        e(submission["email"]), e(submission["telefono"]),
        e(submission["creata_il"].replace("T", " ")[:16]),
        e(archetipo["icona"]), e(archetipo["nome"]),
        e(scheda["riassunto"]),
        forze, attenzioni, chiave,
        submission["variante"], e(submission["etichetta_interna"]),
        submission["punti_a"], e(submission["livello_a"].lower()),
        submission["punti_b"], e(submission["livello_b"].lower()),
        submission["punti_c"], e(submission["livello_c"].lower()),
        esito["bonus_gap"],
        "sì, il %s" % e((submission["preiscrizione_il"] or "").replace("T", " ")[:16])
        if submission["preiscrizione"] else "no",
        "".join(elenco),
    )
    return pagina("Test Onda, %s %s" % (submission["nome"], submission["cognome"]), corpo)


# --------------------------------------------------------------------------
# Handler HTTP
# --------------------------------------------------------------------------

class Handler(BaseHTTPRequestHandler):
    server_version = "TestOnda/1.0"

    # ------------------------------------------------------------ utilità

    def _cookie(self, nome):
        intestazione = self.headers.get("Cookie")
        if not intestazione:
            return None
        biscotti = SimpleCookie()
        biscotti.load(intestazione)
        morso = biscotti.get(nome)
        return morso.value if morso else None

    def _rispondi(self, corpo, stato=HTTPStatus.OK, tipo="text/html; charset=utf-8", cookie=None):
        dati = corpo.encode("utf-8") if isinstance(corpo, str) else corpo
        self.send_response(stato)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(dati)))
        self.send_header("Cache-Control", "no-store")
        for nome, valore in (cookie or []):
            self.send_header(
                "Set-Cookie",
                "%s=%s; Path=/; HttpOnly; SameSite=Lax; Max-Age=%d" % (nome, valore, 60 * 60 * 12),
            )
        self.end_headers()
        self.wfile.write(dati)

    def _redirect(self, percorso, cookie=None):
        self.send_response(HTTPStatus.SEE_OTHER)
        self.send_header("Location", percorso)
        self.send_header("Cache-Control", "no-store")
        for nome, valore in (cookie or []):
            self.send_header(
                "Set-Cookie",
                "%s=%s; Path=/; HttpOnly; SameSite=Lax; Max-Age=%d" % (nome, valore, 60 * 60 * 12),
            )
        self.end_headers()

    def _corpo_form(self):
        lunghezza = int(self.headers.get("Content-Length") or 0)
        grezzo = self.rfile.read(lunghezza).decode("utf-8") if lunghezza else ""
        return {k: v[0] for k, v in urllib.parse.parse_qs(grezzo, keep_blank_values=True).items()}

    def _sessione(self):
        return archivio.leggi_sessione(self._cookie("onda_sid"))

    def _submission(self):
        return archivio.leggi_submission(self._cookie("onda_rid"))

    def _prima_senza_risposta(self, risposte):
        for indice, domanda in enumerate(contenuti.DOMANDE):
            if domanda["id"] not in risposte:
                return indice
        return TOTALE_DOMANDE

    def _autorizzato_admin(self):
        intestazione = self.headers.get("Authorization", "")
        if not intestazione.startswith("Basic "):
            return False
        try:
            decodificato = base64.b64decode(intestazione[6:]).decode("utf-8")
        except Exception:
            return False
        _, _, password = decodificato.partition(":")
        return hmac.compare_digest(password, PASSWORD_ADMIN)

    def _chiedi_password(self):
        self.send_response(HTTPStatus.UNAUTHORIZED)
        self.send_header("WWW-Authenticate", 'Basic realm="Test Onda"')
        self.send_header("Content-Length", "0")
        self.end_headers()

    def log_message(self, formato, *args):
        print("%s %s" % (self.address_string(), formato % args))

    # ---------------------------------------------------------------- GET

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        percorso = parsed.path.rstrip("/") or "/"
        query = urllib.parse.parse_qs(parsed.query)

        if percorso == "/":
            return self._rispondi(pagina_landing())

        if percorso == "/risultato/prossimo-passo":
            # il risultato ora sta tutto in una schermata sola
            return self._redirect("/risultato")

        if percorso == "/statico/stile.css":
            return self._file_statico("stile.css", "text/css; charset=utf-8")

        if percorso == "/quiz":
            sessione = self._sessione()
            if sessione is None:
                return self._redirect("/")
            prima = self._prima_senza_risposta(sessione["risposte"])
            if prima >= TOTALE_DOMANDE and "d" not in query:
                return self._redirect("/contatti")
            try:
                richiesto = int(query.get("d", [prima])[0])
            except ValueError:
                richiesto = prima
            # non si salta avanti: al massimo la prima domanda ancora senza risposta
            richiesto = max(0, min(richiesto, min(prima, TOTALE_DOMANDE - 1)))
            domanda = contenuti.DOMANDE[richiesto]
            return self._rispondi(
                pagina_domanda(richiesto, sessione["risposte"].get(domanda["id"]))
            )

        if percorso == "/contatti":
            sessione = self._sessione()
            if sessione is None:
                return self._redirect("/")
            if self._prima_senza_risposta(sessione["risposte"]) < TOTALE_DOMANDE:
                return self._redirect("/quiz")
            return self._rispondi(pagina_contatti(sessione))

        if percorso == "/risultato":
            submission = self._submission()
            if submission is None:
                return self._redirect("/")
            esito = punteggio.calcola(self._risposte_submission(submission))
            return self._rispondi(pagina_risultato(submission, esito))

        if percorso == "/conferma":
            submission = self._submission()
            if submission is None:
                return self._redirect("/")
            return self._rispondi(pagina_conferma(submission))

        if percorso == "/rifai":
            archivio.elimina_sessione(self._cookie("onda_sid"))
            return self._redirect("/")

        if percorso == "/admin":
            if not self._autorizzato_admin():
                return self._chiedi_password()
            return self._rispondi(pagina_admin(archivio.elenco_submission()))

        if percorso == "/admin/dettaglio":
            if not self._autorizzato_admin():
                return self._chiedi_password()
            submission = archivio.leggi_submission(query.get("id", [""])[0])
            if submission is None:
                return self._redirect("/admin")
            return self._rispondi(pagina_dettaglio(submission))

        if percorso == "/admin/export.csv":
            if not self._autorizzato_admin():
                return self._chiedi_password()
            return self._esporta_csv()

        return self._rispondi(pagina("Test Onda", '<div class="contenuto"><div class="card">'
                                     "<h2>Pagina non trovata</h2>"
                                     '<p><a href="/">Torna all\'inizio</a></p></div></div>'),
                              HTTPStatus.NOT_FOUND)

    # --------------------------------------------------------------- POST

    def do_POST(self):
        percorso = urllib.parse.urlparse(self.path).path.rstrip("/") or "/"
        dati = self._corpo_form()

        if percorso == "/inizia":
            nome_completo = " ".join(dati.get("nome", "").split())
            if not nome_completo:
                return self._rispondi(
                    pagina_landing("Scrivi nome e cognome per iniziare.", nome_completo)
                )
            sessione_id = secrets.token_urlsafe(16)
            archivio.crea_sessione(sessione_id, nome_completo)
            return self._redirect("/quiz", cookie=[("onda_sid", sessione_id)])

        if percorso == "/quiz":
            sessione = self._sessione()
            if sessione is None:
                return self._redirect("/")
            indice = max(0, min(int(dati.get("d", "0") or 0), TOTALE_DOMANDE - 1))

            if dati.get("azione") == "indietro":
                if indice == 0:
                    return self._redirect("/")
                return self._redirect("/quiz?d=%d" % (indice - 1))

            grezza = dati.get("risposta")
            if grezza is None or grezza == "":
                return self._redirect("/quiz?d=%d" % indice)

            domanda = contenuti.DOMANDE[indice]
            valore = int(grezza)
            if domanda["tipo"] == "scala":
                valore = max(1, min(10, valore))
            else:
                valore = max(0, min(len(domanda["opzioni"]) - 1, valore))
            risposte = dict(sessione["risposte"])
            risposte[domanda["id"]] = valore
            archivio.salva_risposte(sessione["id"], risposte)

            if indice + 1 >= TOTALE_DOMANDE:
                return self._redirect("/contatti")
            return self._redirect("/quiz?d=%d" % (indice + 1))

        if percorso == "/contatti":
            sessione = self._sessione()
            if sessione is None:
                return self._redirect("/")
            nome_completo = " ".join(dati.get("nome", "").split())
            nome, _, cognome = nome_completo.partition(" ")
            valori = {
                "nome": nome,
                "cognome": cognome,
                "nome_completo": nome_completo,
                "email": dati.get("email", "").strip(),
                "telefono": dati.get("telefono", "").strip(),
                "consenso": dati.get("consenso") == "1",
            }
            errore = _valida_contatti(valori)
            if errore:
                valori["nome"] = nome_completo
                return self._rispondi(pagina_contatti(sessione, errore, valori))

            esito = punteggio.calcola(sessione["risposte"])
            submission_id = secrets.token_urlsafe(16)
            archivio.crea_submission(submission_id, valori, sessione["risposte"], esito)
            archivio.elimina_sessione(sessione["id"])
            return self._redirect("/risultato", cookie=[("onda_rid", submission_id)])

        if percorso == "/preiscrizione":
            submission = self._submission()
            if submission is None:
                return self._redirect("/")
            if not submission["preiscrizione"]:
                archivio.segna_preiscrizione(submission["id"])
                archivio.accoda_whatsapp(
                    submission["nome"], submission["cognome"], submission["telefono"]
                )
            return self._redirect("/conferma")

        return self._redirect("/")

    # ------------------------------------------------------------- helper

    def _risposte_submission(self, submission):
        return json.loads(submission["risposte"])

    def _file_statico(self, nome_file, tipo):
        percorso = os.path.join(CARTELLA, "statico", nome_file)
        try:
            with open(percorso, "rb") as f:
                contenuto = f.read()
        except OSError:
            return self._rispondi("not found", HTTPStatus.NOT_FOUND, "text/plain")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(contenuto)))
        self.end_headers()
        self.wfile.write(contenuto)

    def _esporta_csv(self):
        buffer = io.StringIO()
        scrittore = csv.writer(buffer)
        colonne = [
            "id", "creata_il", "nome", "cognome", "email", "telefono", "consenso",
            "punti_crescita", "livello_crescita", "punti_azione", "livello_azione",
            "punti_cambiamento", "livello_cambiamento", "etichetta_interna",
            "variante", "archetipo", "preiscrizione", "preiscrizione_il",
        ] + [d["id"] for d in contenuti.DOMANDE]
        scrittore.writerow(colonne)
        for r in archivio.elenco_submission(limite=100000):
            risposte = json.loads(r["risposte"])
            riga = [
                r["id"], r["creata_il"], r["nome"], r["cognome"], r["email"], r["telefono"],
                r["consenso"], r["punti_a"], r["livello_a"], r["punti_b"], r["livello_b"],
                r["punti_c"], r["livello_c"], r["etichetta_interna"], r["variante"],
                r["archetipo"], r["preiscrizione"], r["preiscrizione_il"] or "",
            ]
            for domanda in contenuti.DOMANDE:
                valore = risposte.get(domanda["id"])
                if valore is None:
                    riga.append("")
                elif domanda["tipo"] == "scala":
                    riga.append(valore)
                else:
                    riga.append(domanda["opzioni"][valore][0])
            scrittore.writerow(riga)
        dati = buffer.getvalue().encode("utf-8-sig")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/csv; charset=utf-8")
        self.send_header("Content-Disposition", 'attachment; filename="test_onda.csv"')
        self.send_header("Content-Length", str(len(dati)))
        self.end_headers()
        self.wfile.write(dati)


def _valida_contatti(valori):
    if not valori["nome"] or not valori["cognome"]:
        return "Scrivi nome e cognome."
    email = valori["email"]
    if "@" not in email or "." not in email.split("@")[-1]:
        return "Controlla l'indirizzo email."
    cifre = [c for c in valori["telefono"] if c.isdigit()]
    if len(cifre) < 8:
        return "Controlla il numero di telefono."
    if not valori["consenso"]:
        return "Serve il consenso al trattamento dei dati per proseguire."
    return None


def main():
    archivio.inizializza()
    server = ThreadingHTTPServer((INDIRIZZO, PORTA), Handler)
    print("Test Onda in ascolto su http://%s:%d" % (INDIRIZZO, PORTA))
    print("Dati in %s" % archivio.CARTELLA_DATI)
    if PASSWORD_GENERATA:
        print("ATTENZIONE: TEST_ONDA_ADMIN_PASSWORD non impostata.")
        print("Password temporanea della dashboard: %s" % PASSWORD_ADMIN)
        print("Impostala fra le variabili del servizio per averne una stabile.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
