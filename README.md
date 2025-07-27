# babilonia

## Descrizione

Il backend è costruito con **FastAPI** e utilizza **SQLAlchemy** per l'interazione con un database **SQLite**. La gestione delle dipendenze e dell'ambiente virtuale è affidata a **Poetry**.

Le funzionalità principali includono:
- Autenticazione degli utenti tramite token JWT.
- Gestione dei progressi dell'utente.
- Generazione di esercizi dinamici tramite l'API di Google Gemini.

## Setup e Installazione

### Prerequisiti
- Python 3.8+
- Poetry installato (`pip install poetry`)

### 1. Clonare il Repository
```bash
git clone <URL_DEL_TUO_REPOSITORY>
cd test-gemini-linguo
```

### 2. Configurare le Variabili d'Ambiente
Crea un file `.env` nella directory principale del progetto. Questo file conterrà le chiavi segrete necessarie per l'applicazione.

```
GEMINI_API_KEY="la_tua_chiave_api_di_gemini"
SECRET_KEY="una_chiave_segreta_forte_e_casuale_per_jwt"

# Opzionale: specifica il modello Gemini da usare. Il default è "gemini-1.5-flash-latest".
# GEMINI_MODEL="gemini-1.5-pro-latest"
```
- `GEMINI_API_KEY`: La tua chiave API per accedere a Google Gemini.
- `SECRET_KEY`: Una stringa casuale e sicura per firmare i token JWT. Puoi generarne una con `openssl rand -hex 32`.

### 3. Installare le Dipendenze
Poetry leggerà il file `pyproject.toml` e installerà tutte le dipendenze necessarie in un ambiente virtuale dedicato.
```bash
poetry install
```

## Avviare l'Applicazione
Per avviare il server di sviluppo, esegui:
```bash
cd src && poetry run uvicorn main:app --reload
```
Il server sarà accessibile all'indirizzo `http://127.0.0.1:8000`.

L'opzione `--reload` fa sì che il server si riavvii automaticamente ogni volta che modifichi un file di codice.

## Documentazione API (Swagger)
Una volta che il server è in esecuzione, puoi accedere alla documentazione interattiva dell'API, generata automaticamente da Swagger UI, al seguente indirizzo:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Da qui potrai testare tutti gli endpoint direttamente dal browser.
