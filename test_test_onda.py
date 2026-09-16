# -*- coding: utf-8 -*-
"""Test del flusso completo del Test Onda e della logica di punteggio.

Si avvia con: python3 -m unittest test_test_onda
"""

import html
import itertools
import json
import os
import re
import tempfile
import threading
import unittest
import urllib.error
import urllib.parse
import urllib.request
from http.cookiejar import CookieJar
from http.server import ThreadingHTTPServer

CARTELLA_TEMP = tempfile.mkdtemp(prefix="test_onda_")
os.environ["TEST_ONDA_DATA_DIR"] = CARTELLA_TEMP

import archivio  # noqa: E402
import contenuti  # noqa: E402
import punteggio  # noqa: E402
import report  # noqa: E402
import server  # noqa: E402

# parole che non devono mai comparire nel sorgente HTML servito alla persona
PAROLE_VIETATE = [
    "semaforo", "idoneo", "escluso", "priorit", "etichetta_interna",
    "ALTO", "MEDIO", "BASSO", "punti_a", "bonus",
]


class ServerDiProva:
    def __init__(self):
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
        self.porta = self.httpd.server_address[1]
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)

    def __enter__(self):
        archivio.inizializza()
        self.thread.start()
        return "http://127.0.0.1:%d" % self.porta

    def __exit__(self, *args):
        self.httpd.shutdown()
        self.httpd.server_close()


class Cliente:
    def __init__(self, base):
        self.base = base
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(CookieJar())
        )

    def get(self, percorso):
        with self.opener.open(self.base + percorso) as r:
            return r.geturl(), r.read().decode("utf-8")

    def get_admin(self, percorso, password="onda"):
        import base64
        richiesta = urllib.request.Request(self.base + percorso)
        chiave = base64.b64encode(("team:%s" % password).encode()).decode()
        richiesta.add_header("Authorization", "Basic " + chiave)
        with self.opener.open(richiesta) as r:
            return r.geturl(), r.read().decode("utf-8")

    def post(self, percorso, dati):
        corpo = urllib.parse.urlencode(dati).encode("utf-8")
        with self.opener.open(self.base + percorso, data=corpo) as r:
            return r.geturl(), r.read().decode("utf-8")


def indice_domanda(html_pagina):
    trovato = re.search(r"DOMANDA (\d+) DI (\d+)", html_pagina, re.IGNORECASE)
    return int(trovato.group(1)) - 1 if trovato else None


class TestPunteggio(unittest.TestCase):
    def test_massimi_di_blocco(self):
        massimi = {"A": 0.0, "B": 0.0, "C": 0.0}
        for d in contenuti.DOMANDE:
            if d["tipo"] == "scala":
                massimi[d["blocco"]] += 5 if d.get("punteggia") else 0
            else:
                massimi[d["blocco"]] += max(p for _, p in d["opzioni"])
        self.assertEqual(massimi["A"], 26)  # 26 + 2 di bonus gap = 28
        self.assertEqual(massimi["B"], 12)
        self.assertEqual(massimi["C"], 15)

    def test_bonus_gap(self):
        self.assertEqual(punteggio.bonus_gap({"D6": 9, "D7": 3}), 2)
        self.assertEqual(punteggio.bonus_gap({"D6": 7, "D7": 5}), 1)
        self.assertEqual(punteggio.bonus_gap({"D6": 5, "D7": 5}), 0)
        self.assertEqual(punteggio.bonus_gap({"D6": 3, "D7": 9}), 0)

    def test_etichetta_interna(self):
        self.assertEqual(punteggio.etichetta_interna("BASSO", "ALTO", "ALTO"), "rosso")
        self.assertEqual(punteggio.etichetta_interna("ALTO", "BASSO", "ALTO"), "rosso")
        self.assertEqual(punteggio.etichetta_interna("ALTO", "ALTO", "MEDIO"), "verde")
        self.assertEqual(punteggio.etichetta_interna("ALTO", "ALTO", "BASSO"), "giallo")
        self.assertEqual(punteggio.etichetta_interna("MEDIO", "MEDIO", "MEDIO"), "giallo")

    def test_tutte_le_varianti_sono_raggiungibili(self):
        viste = set()
        for combinazione in itertools.product(("ALTO", "MEDIO", "BASSO"), repeat=3):
            a, b, c = combinazione
            etichetta = punteggio.etichetta_interna(a, b, c)
            viste.add(punteggio.scegli_variante(etichetta, a, c))
        self.assertEqual(viste, {1, 2, 3, 4, 5, 6})

    def test_ogni_combinazione_produce_un_profilo(self):
        """Il quiz non esclude nessuno: qualunque set di risposte dà un profilo."""
        for indici in itertools.product((0, 1), repeat=len(contenuti.DOMANDE)):
            risposte = {}
            for scelta, d in zip(indici, contenuti.DOMANDE):
                if d["tipo"] == "scala":
                    risposte[d["id"]] = 1 if scelta == 0 else 10
                else:
                    risposte[d["id"]] = min(scelta, len(d["opzioni"]) - 1)
            esito = punteggio.calcola(risposte)
            self.assertIn(esito["variante"], contenuti.VARIANTI)
            self.assertIn(esito["archetipo"], contenuti.ARCHETIPI)


class TestFlusso(unittest.TestCase):
    def test_percorso_completo(self):
        with ServerDiProva() as base:
            cliente = Cliente(base)
            pagine = []

            _, landing = cliente.get("/")
            pagine.append(landing)
            self.assertIn("Sei pronto a diventare il Professionista del Futuro?", landing)

            url, html_pagina = cliente.post("/inizia", {"nome": "Marco Rossi"})
            self.assertTrue(url.endswith("/quiz"))

            # risponde a tutte e 16 le domande scegliendo sempre la prima opzione
            for atteso in range(len(contenuti.DOMANDE)):
                self.assertEqual(indice_domanda(html_pagina), atteso)
                pagine.append(html_pagina)
                domanda = contenuti.DOMANDE[atteso]
                valore = 9 if domanda["tipo"] == "scala" else 0
                url, html_pagina = cliente.post(
                    "/quiz", {"d": str(atteso), "risposta": str(valore)}
                )

            self.assertTrue(url.endswith("/contatti"), url)
            self.assertIn("Ci siamo quasi!", html_pagina)
            pagine.append(html_pagina)

            # email non valida: resta sulla pagina contatti
            _, html_errore = cliente.post("/contatti", {
                "nome": "Marco Rossi", "email": "non-valida",
                "telefono": "3331234567", "consenso": "1",
            })
            self.assertIn("Controlla l&#x27;indirizzo email", html_errore)

            # consenso mancante: non prosegue
            _, html_errore = cliente.post("/contatti", {
                "nome": "Marco Rossi", "email": "marco@example.com",
                "telefono": "3331234567",
            })
            self.assertIn("consenso", html_errore)

            url, risultato = cliente.post("/contatti", {
                "nome": "Marco Rossi", "email": "marco@example.com",
                "telefono": "333 1234567", "consenso": "1",
            })
            self.assertTrue(url.endswith("/risultato"), url)
            self.assertIn("IL TUO PROFILO", risultato)
            self.assertIn("Marco", risultato)
            self.assertIn("/10", risultato)
            self.assertIn("Spinta alla crescita", risultato)
            self.assertIn("Ti ritrovi in questo?", risultato)
            self.assertIn("22-25 Ottobre", risultato)
            self.assertIn("Invia la pre-iscrizione", risultato)  # CTA sempre attiva
            pagine.append(risultato)

            # tutto in una schermata, ma il workshop resta dopo profilo e punteggi
            self.assertLess(risultato.index("IL TUO PROFILO"),
                            risultato.index("Ti ritrovi in questo?"))
            self.assertLess(risultato.index("Ti ritrovi in questo?"),
                            risultato.index("IL PROSSIMO PASSO"))

            url, conferma = cliente.post("/preiscrizione", {})
            self.assertTrue(url.endswith("/conferma"), url)
            self.assertIn("pre-iscrizione", conferma.lower())
            pagine.append(conferma)

            # il contatto finisce nella coda WhatsApp
            with open(archivio.PERCORSO_CODA, encoding="utf-8") as f:
                righe = [json.loads(r) for r in f if r.strip()]
            self.assertTrue(any(r["nome"] == "Marco" for r in righe))

            for html_pagina in pagine:
                for parola in PAROLE_VIETATE:
                    self.assertNotIn(parola, html_pagina,
                                     "parola vietata nel sorgente: %s" % parola)

    def test_bottone_indietro_conserva_la_risposta(self):
        with ServerDiProva() as base:
            cliente = Cliente(base)
            cliente.post("/inizia", {"nome": "Giulia Bianchi"})

            cliente.post("/quiz", {"d": "0", "risposta": "1"})   # D1, seconda opzione
            _, html_pagina = cliente.post("/quiz", {"d": "1", "risposta": "2"})  # D2, terza
            self.assertEqual(indice_domanda(html_pagina), 2)

            # indietro dalla domanda 3 alla domanda 2
            _, html_pagina = cliente.post("/quiz", {"d": "2", "azione": "indietro"})
            self.assertEqual(indice_domanda(html_pagina), 1)
            self.assertIn('value="2" class="opzione scelta"', html_pagina)

            # il bottone Indietro non è mai disabilitato
            self.assertNotIn("disabled", html_pagina)

            # ancora indietro: prima domanda, con la sua risposta conservata
            _, html_pagina = cliente.post("/quiz", {"d": "1", "azione": "indietro"})
            self.assertEqual(indice_domanda(html_pagina), 0)
            self.assertIn('value="1" class="opzione scelta"', html_pagina)

            # dalla prima domanda si torna alla landing
            url, _ = cliente.post("/quiz", {"d": "0", "azione": "indietro"})
            self.assertEqual(url.rstrip("/"), base)

    def test_vecchia_rotta_del_workshop_porta_al_risultato(self):
        with ServerDiProva() as base:
            cliente = Cliente(base)
            url, _ = cliente.get("/risultato/prossimo-passo")
            self.assertEqual(url.rstrip("/"), base)

    def test_non_si_salta_avanti(self):
        with ServerDiProva() as base:
            cliente = Cliente(base)
            cliente.post("/inizia", {"nome": "Luca Verdi"})
            _, html_pagina = cliente.get("/quiz?d=12")
            self.assertEqual(indice_domanda(html_pagina), 0)

    def test_risultato_non_accessibile_senza_contatti(self):
        with ServerDiProva() as base:
            cliente = Cliente(base)
            url, _ = cliente.get("/risultato")
            self.assertEqual(url.rstrip("/"), base)

    def test_dashboard_mostra_i_test_completati(self):
        with ServerDiProva() as base:
            cliente = Cliente(base)
            cliente.post("/inizia", {"nome": "Sara Neri"})
            for indice, domanda in enumerate(contenuti.DOMANDE):
                cliente.post("/quiz", {
                    "d": str(indice),
                    "risposta": "7" if domanda["tipo"] == "scala" else "0",
                })
            cliente.post("/contatti", {
                "nome": "Sara Neri", "email": "sara@example.com",
                "telefono": "3339998877", "consenso": "1",
            })
            cliente.post("/preiscrizione", {})

            _, dashboard = cliente.get_admin("/admin")
            self.assertIn("Dashboard Test Onda", dashboard)
            self.assertIn("sara@example.com", dashboard)
            self.assertIn("Test completati", dashboard)

            # dal riepilogo si apre il dettaglio con tutte le risposte
            id_submission = re.search(r'/admin/dettaglio\?id=([^"]+)', dashboard).group(1)
            _, dettaglio = cliente.get_admin("/admin/dettaglio?id=" + id_submission)
            self.assertIn("Sara", dettaglio)
            self.assertIn("Tutte le risposte", dettaglio)
            for domanda in contenuti.DOMANDE:
                self.assertIn(html.escape(domanda["testo"], quote=True), dettaglio)

            self.assertIn("PRIMA DI CHIAMARE", dettaglio)
            self.assertIn("Punti di forza", dettaglio)
            self.assertIn("Punti di attenzione", dettaglio)

            _, csv_testo = cliente.get_admin("/admin/export.csv")
            self.assertIn("sara@example.com", csv_testo)

    def test_report_sempre_tre_e_tre(self):
        """Il venditore deve trovare sempre 3 forze e 3 attenzioni, qualunque
        siano le risposte."""
        import itertools
        for indici in itertools.product((0, 1, 2), repeat=4):
            risposte = {}
            for posizione, d in enumerate(contenuti.DOMANDE):
                if d["tipo"] == "scala":
                    risposte[d["id"]] = (1, 5, 10)[indici[posizione % 4]]
                else:
                    risposte[d["id"]] = min(indici[posizione % 4], len(d["opzioni"]) - 1)
            esito = punteggio.calcola(risposte)
            scheda = report.genera(risposte, esito, False)
            self.assertEqual(len(scheda["forze"]), 3)
            self.assertEqual(len(scheda["attenzioni"]), 3)
            self.assertEqual(len(set(scheda["forze"])), 3)
            self.assertEqual(len(set(scheda["attenzioni"])), 3)
            self.assertTrue(scheda["riassunto"].strip())

    def test_area_team_protetta(self):
        with ServerDiProva() as base:
            cliente = Cliente(base)
            with self.assertRaises(urllib.error.HTTPError) as ctx:
                cliente.get("/admin")
            self.assertEqual(ctx.exception.code, 401)


if __name__ == "__main__":
    unittest.main()
