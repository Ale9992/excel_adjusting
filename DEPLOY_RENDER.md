# 🚀 Guida al Deploy su Render - Excel Adjuster

Questa guida ti accompagna passo dopo passo nel deploy dell'applicazione Excel Adjuster su Render, una piattaforma cloud moderna e gratuita.

## 📋 Prerequisiti

1. **Account Render**: Registrati gratuitamente su [render.com](https://render.com)
2. **Repository GitHub**: Il progetto deve essere su GitHub (pubblico o privato)
3. **Git configurato**: Per pushare le modifiche

## 🛠️ Preparazione del Progetto

### File di Configurazione (Già Creati)

Il progetto è già configurato con tutti i file necessari:

- ✅ `render.yaml` - Configurazione automatica per Render
- ✅ `Procfile` - Comando di avvio
- ✅ `requirements.txt` - Dipendenze Python
- ✅ `app.py` - Backend FastAPI configurato per Render

### Struttura del Progetto

```
PuffStore-tool-web/
├── app.py              # Backend FastAPI
├── solver_semplice.py  # Algoritmo di correzione
├── index.html          # Frontend HTML
├── app.js              # Frontend JavaScript
├── requirements.txt    # Dipendenze Python
├── render.yaml         # Configurazione Render
├── Procfile            # Comando di avvio
└── README.md           # Documentazione
```

## 🚀 Deploy su Render

### Metodo 1: Deploy Automatico (Raccomandato)

1. **Push del codice su GitHub**:
   ```bash
   git add .
   git commit -m "Preparazione per deploy su Render"
   git push origin main
   ```

2. **Accedi a Render**:
   - Vai su [render.com](https://render.com)
   - Clicca su "Sign Up" e registrati
   - Connetti il tuo account GitHub

3. **Crea nuovo servizio**:
   - Clicca su "New +"
   - Seleziona "Blueprint"
   - Connetti il tuo repository GitHub
   - Render rileverà automaticamente il file `render.yaml`

4. **Configurazione automatica**:
   - Render userà le impostazioni del file `render.yaml`
   - Nome servizio: `excel-adjuster`
   - Piano: `Free`
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`

### Metodo 2: Deploy Manuale

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
   - `PYTHON_VERSION`: `3.11.10`

## ⏱️ Processo di Deploy

1. **Build Phase** (2-3 minuti):
   - Render installa Python 3.11.10
   - Installa le dipendenze da `requirements.txt`
   - Prepara l'ambiente di runtime

2. **Deploy Phase** (1-2 minuti):
   - Avvia l'applicazione FastAPI
   - Assegna un URL pubblico
   - Configura SSL automaticamente

3. **Health Check**:
   - Render verifica che l'app risponda su `/docs`
   - Se tutto è OK, il servizio diventa attivo

## 🌐 Accesso all'Applicazione

Dopo il deploy, l'applicazione sarà disponibile su:

- **URL Pubblico**: `https://excel-adjuster.onrender.com`
- **API Documentation**: `https://excel-adjuster.onrender.com/docs`
- **Health Check**: `https://excel-adjuster.onrender.com/`

## 🔧 Configurazione Avanzata

### Variabili d'Ambiente (Opzionali)

Puoi aggiungere variabili d'ambiente in Render per personalizzare l'app:

- `DEBUG`: `false` (per produzione)
- `LOG_LEVEL`: `INFO`
- `MAX_FILE_SIZE`: `10485760` (10MB)

### Dominio Personalizzato

1. Vai nelle impostazioni del servizio
2. Sezione "Custom Domains"
3. Aggiungi il tuo dominio
4. Configura i DNS come indicato da Render

## 📊 Monitoraggio

### Logs in Tempo Reale
- Dashboard del servizio → Sezione "Logs"
- Visualizza errori e output dell'applicazione

### Metriche
- CPU e memoria utilizzate
- Richieste HTTP per minuto
- Tempo di risposta

## ⚠️ Limitazioni del Piano Gratuito

- **Sleep dopo inattività**: Il servizio si "addormenta" dopo 15 minuti di inattività
- **Cold start**: Il primo accesso dopo il sleep può richiedere 30-60 secondi
- **Build time**: Limitato a 90 minuti al mese
- **Bandwidth**: 100GB al mese

## 🔄 Aggiornamenti Futuri

Per deployare nuove modifiche:

1. **Modifica il codice localmente**
2. **Push su GitHub**:
   ```bash
   git add .
   git commit -m "Aggiornamento funzionalità"
   git push origin main
   ```
3. **Deploy automatico**: Render rileverà le modifiche e farà il redeploy

## 🐛 Troubleshooting

### Build Fallisce
- Verifica che `requirements.txt` sia corretto
- Controlla i log di build per errori specifici
- Assicurati che tutte le dipendenze siano compatibili

### App Non Si Avvia
- Verifica che il comando di start sia corretto
- Controlla che la porta sia `$PORT` (variabile d'ambiente di Render)
- Verifica i log per errori di runtime

### CORS Errors
- Il progetto è già configurato per CORS
- Se hai problemi, verifica che `allow_origins=["*"]` sia presente in `app.py`

### File Upload Non Funziona
- Render supporta file temporanei
- I file vengono processati e poi eliminati automaticamente
- Verifica che il frontend punti all'URL corretto di Render

### Cold Start Lento
- È normale per il piano gratuito
- Considera l'upgrade al piano Starter per eliminare il cold start

## 💡 Consigli per l'Ottimizzazione

1. **Riduci le dipendenze**: Rimuovi pacchetti non necessari da `requirements.txt`
2. **Ottimizza le immagini**: Comprimi le icone in `assets/`
3. **Cache**: Implementa cache per file Excel processati di recente
4. **Monitoraggio**: Usa i log per identificare problemi di performance

## 🆘 Supporto

- **Documentazione Render**: [render.com/docs](https://render.com/docs)
- **Community**: [render.com/community](https://render.com/community)
- **Status Page**: [status.render.com](https://status.render.com)

---

## 🎉 Congratulazioni!

Il tuo Excel Adjuster è ora online e accessibile da tutto il mondo!

**URL dell'applicazione**: `https://excel-adjuster.onrender.com`

L'applicazione è pronta per essere utilizzata da chiunque abbia bisogno di correggere file Excel automaticamente. 🚀
