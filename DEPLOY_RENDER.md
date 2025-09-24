# Guida al Deploy del Progetto "Excel Adjuster" su Render

Questo documento fornisce istruzioni dettagliate per il deploy del progetto full-stack (Frontend HTML/JS + Backend FastAPI Python) su Render.

## Perché Render?

Render è una piattaforma cloud moderna che offre:
- **Deploy automatico** da GitHub
- **Supporto nativo** per Python/FastAPI
- **SSL gratuito** e CDN globale
- **Piano gratuito** generoso per progetti personali
- **Configurazione semplice** con file YAML

## Prerequisiti

1. **Account Render**: Assicurati di avere un account Render. Puoi registrarti gratuitamente su [render.com](https://render.com)
2. **Repository GitHub**: Il tuo progetto deve essere in un repository GitHub pubblico o privato

## Passaggi per il Deploy

### 1. Preparazione del Progetto

Assicurati che il tuo progetto abbia la seguente struttura e file:

#### **File di Configurazione Render**
- **`render.yaml`**: File di configurazione per Render (già creato)
- **`requirements.txt`**: Dipendenze Python (già presente)

#### **File Principali**
- **`app.py`**: Backend FastAPI principale
- **`solver_semplice.py`**: Algoritmo di correzione
- **`index.html`**: Frontend HTML
- **`app.js`**: Frontend JavaScript

### 2. Configurazione del Repository GitHub

1. **Push del codice**:
   ```bash
   git add .
   git commit -m "Preparazione per deploy su Render"
   git push origin main
   ```

2. **Verifica** che tutti i file siano presenti nel repository

### 3. Deploy su Render

#### **Metodo 1: Deploy Automatico con render.yaml**

1. **Accedi a Render**: Vai su [render.com](https://render.com) e accedi al tuo account

2. **Crea nuovo servizio**:
   - Clicca su "New +"
   - Seleziona "Blueprint"
   - Connetti il tuo repository GitHub
   - Render rileverà automaticamente il file `render.yaml`

3. **Configurazione automatica**:
   - Render userà le impostazioni del file `render.yaml`
   - Nome servizio: `excel-adjuster`
   - Piano: `free`
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`

#### **Metodo 2: Deploy Manuale**

1. **Crea nuovo servizio**:
   - Clicca su "New +"
   - Seleziona "Web Service"
   - Connetti il tuo repository GitHub

2. **Configurazione manuale**:
   - **Name**: `excel-adjuster`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Plan**: `Free`

3. **Variabili d'ambiente**:
   - `PYTHON_VERSION`: `3.11.0`

### 4. Configurazione CORS

Il progetto è già configurato per funzionare su Render con CORS abilitato per tutti gli origin (`allow_origins=["*"]`).

### 5. Test del Deploy

1. **Attendi il build**: Render impiegherà alcuni minuti per:
   - Installare le dipendenze
   - Avviare l'applicazione
   - Assegnare un URL pubblico

2. **Verifica il funzionamento**:
   - Vai all'URL fornito da Render
   - Dovresti vedere il frontend dell'applicazione
   - Testa il caricamento di un file Excel
   - Verifica che la correzione funzioni

### 6. URL e Accesso

- **Frontend**: `https://excel-adjuster.onrender.com`
- **API Docs**: `https://excel-adjuster.onrender.com/docs`
- **Health Check**: `https://excel-adjuster.onrender.com/docs`

## Configurazione Avanzata

### **Variabili d'Ambiente (Opzionali)**

Se vuoi personalizzare ulteriormente, puoi aggiungere variabili d'ambiente in Render:

- `DEBUG`: `false` (per produzione)
- `LOG_LEVEL`: `INFO`

### **Dominio Personalizzato (Opzionale)**

1. Vai nelle impostazioni del servizio
2. Sezione "Custom Domains"
3. Aggiungi il tuo dominio
4. Configura i DNS come indicato da Render

## Monitoraggio e Logs

### **Logs in Tempo Reale**
- Vai nella dashboard del servizio
- Sezione "Logs" per vedere i log in tempo reale

### **Metriche**
- Render fornisce metriche di base anche nel piano gratuito
- CPU, memoria, e richieste HTTP

## Limitazioni del Piano Gratuito

- **Sleep dopo inattività**: Il servizio si "addormenta" dopo 15 minuti di inattività
- **Cold start**: Il primo accesso dopo il sleep può richiedere 30-60 secondi
- **Build time**: Limitato a 90 minuti al mese
- **Bandwidth**: 100GB al mese

## Aggiornamenti Futuri

Per deployare nuove modifiche:

1. **Push su GitHub**:
   ```bash
   git add .
   git commit -m "Aggiornamento funzionalità"
   git push origin main
   ```

2. **Deploy automatico**: Render rileverà automaticamente le modifiche e farà il redeploy

## Troubleshooting

### **Build Fallisce**
- Verifica che `requirements.txt` sia corretto
- Controlla i log di build per errori specifici

### **App Non Si Avvia**
- Verifica che il comando di start sia corretto
- Controlla che la porta sia `$PORT` (variabile d'ambiente di Render)

### **CORS Errors**
- Il progetto è già configurato per CORS
- Se hai problemi, verifica che `allow_origins=["*"]` sia presente in `app.py`

### **File Upload Non Funziona**
- Render supporta file temporanei
- I file vengono processati e poi eliminati automaticamente

## Supporto

- **Documentazione Render**: [render.com/docs](https://render.com/docs)
- **Community**: [render.com/community](https://render.com/community)

---

**Congratulazioni! Il tuo "Excel Adjuster" è ora online su Render!** 🚀

Il servizio sarà disponibile all'URL: `https://excel-adjuster.onrender.com`
