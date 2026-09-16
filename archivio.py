# -*- coding: utf-8 -*-
"""Persistenza del Test Onda su SQLite, più la coda WhatsApp su file.

Due tabelle: le sessioni di quiz in corso (per poter tornare indietro senza
perdere le risposte) e le submission complete con contatti e profilo.
"""

import json
import os
import sqlite3
import threading
from datetime import datetime, timezone

CARTELLA_DATI = os.environ.get(
    "TEST_ONDA_DATA_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dati")
)
PERCORSO_DB = os.path.join(CARTELLA_DATI, "test_onda.db")
PERCORSO_CODA = os.path.join(CARTELLA_DATI, "coda_whatsapp.log")

_lock = threading.Lock()


def _ora():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _connessione():
    os.makedirs(CARTELLA_DATI, exist_ok=True)
    conn = sqlite3.connect(PERCORSO_DB, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def inizializza():
    with _lock, _connessione() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS sessioni (
                id TEXT PRIMARY KEY,
                nome_completo TEXT NOT NULL DEFAULT '',
                risposte TEXT NOT NULL DEFAULT '{}',
                creata_il TEXT NOT NULL,
                aggiornata_il TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS submission (
                id TEXT PRIMARY KEY,
                creata_il TEXT NOT NULL,
                nome TEXT NOT NULL,
                cognome TEXT NOT NULL,
                email TEXT NOT NULL,
                telefono TEXT NOT NULL,
                consenso INTEGER NOT NULL DEFAULT 0,
                risposte TEXT NOT NULL,
                punti_a REAL NOT NULL,
                punti_b REAL NOT NULL,
                punti_c REAL NOT NULL,
                livello_a TEXT NOT NULL,
                livello_b TEXT NOT NULL,
                livello_c TEXT NOT NULL,
                etichetta_interna TEXT NOT NULL,
                variante INTEGER NOT NULL,
                archetipo TEXT NOT NULL,
                preiscrizione INTEGER NOT NULL DEFAULT 0,
                preiscrizione_il TEXT
            );
            """
        )


# ---------------------------------------------------------------- sessioni

def crea_sessione(sessione_id, nome_completo):
    with _lock, _connessione() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO sessioni (id, nome_completo, risposte, creata_il, aggiornata_il)"
            " VALUES (?, ?, '{}', ?, ?)",
            (sessione_id, nome_completo, _ora(), _ora()),
        )


def leggi_sessione(sessione_id):
    if not sessione_id:
        return None
    with _lock, _connessione() as conn:
        riga = conn.execute("SELECT * FROM sessioni WHERE id = ?", (sessione_id,)).fetchone()
    if riga is None:
        return None
    return {
        "id": riga["id"],
        "nome_completo": riga["nome_completo"],
        "risposte": json.loads(riga["risposte"]),
    }


def salva_risposte(sessione_id, risposte):
    with _lock, _connessione() as conn:
        conn.execute(
            "UPDATE sessioni SET risposte = ?, aggiornata_il = ? WHERE id = ?",
            (json.dumps(risposte, ensure_ascii=False), _ora(), sessione_id),
        )


def elimina_sessione(sessione_id):
    if not sessione_id:
        return
    with _lock, _connessione() as conn:
        conn.execute("DELETE FROM sessioni WHERE id = ?", (sessione_id,))


# -------------------------------------------------------------- submission

def crea_submission(submission_id, contatti, risposte, esito):
    with _lock, _connessione() as conn:
        conn.execute(
            "INSERT INTO submission (id, creata_il, nome, cognome, email, telefono, consenso,"
            " risposte, punti_a, punti_b, punti_c, livello_a, livello_b, livello_c,"
            " etichetta_interna, variante, archetipo, preiscrizione)"
            " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,0)",
            (
                submission_id,
                _ora(),
                contatti["nome"],
                contatti["cognome"],
                contatti["email"],
                contatti["telefono"],
                1 if contatti.get("consenso") else 0,
                json.dumps(risposte, ensure_ascii=False),
                esito["punti"]["A"],
                esito["punti"]["B"],
                esito["punti"]["C"],
                esito["livelli"]["A"],
                esito["livelli"]["B"],
                esito["livelli"]["C"],
                esito["etichetta_interna"],
                esito["variante"],
                esito["archetipo"],
            ),
        )


def leggi_submission(submission_id):
    if not submission_id:
        return None
    with _lock, _connessione() as conn:
        riga = conn.execute("SELECT * FROM submission WHERE id = ?", (submission_id,)).fetchone()
    return dict(riga) if riga else None


def segna_preiscrizione(submission_id):
    with _lock, _connessione() as conn:
        conn.execute(
            "UPDATE submission SET preiscrizione = 1, preiscrizione_il = ? WHERE id = ?",
            (_ora(), submission_id),
        )


def elenco_submission(limite=500):
    with _lock, _connessione() as conn:
        righe = conn.execute(
            "SELECT * FROM submission ORDER BY creata_il DESC LIMIT ?", (limite,)
        ).fetchall()
    return [dict(r) for r in righe]


# ----------------------------------------------------------- coda WhatsApp

def accoda_whatsapp(nome, cognome, telefono):
    """Nessun provider WhatsApp è collegato: il contatto viene messo in coda su
    file, pronto per essere ripreso da un'integrazione futura."""
    os.makedirs(CARTELLA_DATI, exist_ok=True)
    record = {
        "nome": nome,
        "cognome": cognome,
        "telefono": telefono,
        "accodato_il": _ora(),
        "stato": "da_contattare",
    }
    with _lock, open(PERCORSO_CODA, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record
