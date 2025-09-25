# Excel Adjuster - Correzione Automatica File Excel

Un'applicazione web completa per la correzione automatica di file Excel con algoritmo intelligente che modifica quantità e prezzi per raggiungere un totale target specifico.

## 🚀 Caratteristiche

- **Backend FastAPI** robusto e scalabile
- **Frontend moderno** con Tailwind CSS
- **Algoritmo intelligente** con vincoli di non-negatività
- **Interfaccia drag & drop** per caricamento file
- **Validazione completa** dei dati
- **Download automatico** del file corretto

## 📋 Requisiti

- Python 3.8 o superiore
- pip (gestore pacchetti Python)

## 🛠️ Installazione

### 1. Clona o scarica il progetto
```bash
# Se hai git
git clone <repository-url>
cd PuffStore-tool

# Oppure scarica e estrai i file in una cartella
```

### 2. Crea un ambiente virtuale (raccomandato)
```bash
# Crea l'ambiente virtuale
python -m venv venv

# Attiva l'ambiente virtuale
# Su Windows:
venv\Scripts\activate
# Su macOS/Linux:
source venv/bin/activate
```

### 3. Installa le dipendenze
```bash
pip install -r requirements.txt
```

## 🚀 Avvio dell'Applicazione

### Opzione 1: Esecuzione Locale

#### 1. Avvia il Backend FastAPI
```bash
# Metodo 1: Comando diretto
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Metodo 2: Usando Python
python app.py
```

Il backend sarà disponibile su: `http://localhost:8000`

#### 2. Apri il Frontend
Apri il file `index.html` nel tuo browser preferito:
- **Chrome/Edge**: Doppio click su `index.html`
- **Firefox**: Doppio click su `index.html`
- **Safari**: Doppio click su `index.html`

Oppure apri direttamente: `file:///percorso/completo/a/PuffStore-tool/index.html`

### Opzione 2: Deploy su Render (Raccomandato)

Per rendere l'applicazione accessibile online, segui la guida completa in [DEPLOY_RENDER.md](DEPLOY_RENDER.md).

**Passaggi rapidi:**
1. Pusha il codice su GitHub
2. Connetti il repository a Render
3. Deploy automatico con il file `render.yaml`
4. L'app sarà disponibile su `https://excel-adjuster.onrender.com`

## 📖 Come Usare l'Applicazione

### 1. Carica un File Excel
- Trascina un file `.xlsx` o `.xls` nell'area di upload
- Oppure clicca "Carica un file" e seleziona il file
- Il sistema analizzerà automaticamente il file

### 2. Seleziona il Foglio di Lavoro
- Scegli il foglio di lavoro dal menu a tendina
- Il sistema mostrerà le colonne numeriche disponibili

### 3. Configura le Colonne
- **Colonna Quantità**: Seleziona la colonna con le quantità
- **Colonna Prezzo**: Seleziona la colonna con i prezzi
- **Colonna Rimanenze**: Seleziona la colonna che calcola Quantità × Prezzo

### 4. Imposta il Totale Target
- Inserisci il valore totale che vuoi raggiungere
- Il sistema modificherà i valori per raggiungere questo totale

### 5. Opzioni Avanzate (opzionale)
- **Variazione Quantità**: Percentuale di variazione per le quantità (default: ±15%)
- **Variazione Prezzo**: Percentuale di variazione per i prezzi (default: ±20%)
- **Seed Casuale**: Numero per risultati riproducibili (opzionale)

### 6. Esegui la Correzione
- Clicca "Esegui Correzione"
- Il sistema elaborerà il file e lo scaricherà automaticamente

## 🔧 API Endpoints

### POST `/introspect`
Analizza un file Excel e restituisce informazioni sui fogli e colonne.

**Parametri:**
- `file`: File Excel (.xlsx o .xls)

**Risposta:**
```json
{
  "success": true,
  "sheets": {
    "Foglio1": {
      "columns": ["Quantità", "Prezzo", "Totale"],
      "row_count": 100,
      "sample_data": [...]
    }
  },
  "filename": "esempio.xlsx"
}
```

### POST `/adjust`
Applica l'algoritmo di correzione al file Excel.

**Parametri:**
- `file`: File Excel
- `sheet_name`: Nome del foglio di lavoro
- `quantity_column`: Nome colonna quantità
- `price_column`: Nome colonna prezzo
- `remaining_column`: Nome colonna rimanenze
- `target_total`: Totale target (float)
- `quantity_variation`: Variazione quantità (default: 0.15)
- `price_variation`: Variazione prezzo (default: 0.20)
- `random_seed`: Seed casuale (opzionale)

**Risposta:** File Excel modificato per download

## 🧮 Algoritmo di Correzione

L'algoritmo implementa una strategia a più fasi:

1. **Variazione Casuale**: Applica variazioni casuali a quantità e prezzi entro i limiti specificati
2. **Correzione Fattore**: Calcola un fattore moltiplicativo per raggiungere il totale target
3. **Regolazione Fine**: Corregge l'ultima riga per eliminare residui di arrotondamento
4. **Vincoli di Sicurezza**: Garantisce che quantità ≥ 0 e prezzi ≥ 0.01

### Caratteristiche dell'Algoritmo:
- ✅ **Nessun valore negativo**: Quantità e prezzi non possono diventare negativi
- ✅ **Precisione**: Corregge automaticamente i residui di arrotondamento
- ✅ **Riproducibilità**: Seed casuale per risultati consistenti
- ✅ **Flessibilità**: Variazioni personalizzabili per quantità e prezzi

## 🐛 Risoluzione Problemi

### Errore "Connection refused"
- Assicurati che il backend sia in esecuzione su `http://localhost:8000`
- Verifica che non ci siano altri servizi sulla porta 8000

### Errore "File non valido"
- Verifica che il file sia un Excel (.xlsx o .xls)
- Controlla che il file non sia corrotto
- Assicurati che le colonne selezionate contengano dati numerici

### Errore "Colonne non trovate"
- Verifica che le colonne selezionate esistano nel foglio
- Controlla che le colonne contengano dati numerici
- Assicurati di aver selezionato il foglio corretto

### Problemi di Performance
- Per file molto grandi (>10MB), considera di dividere i dati
- Usa un seed casuale per risultati più prevedibili

## 📁 Struttura del Progetto

```
PuffStore-tool/
├── app.py              # Backend FastAPI principale
├── solver.py           # Algoritmo di correzione Excel
├── index.html          # Frontend HTML con Tailwind CSS
├── app.js              # Logica JavaScript frontend
├── requirements.txt    # Dipendenze Python
└── README.md          # Questa documentazione
```

## 🔒 Sicurezza

- Il sistema non salva i file caricati permanentemente
- I file temporanei vengono eliminati automaticamente
- Validazione completa di tutti gli input
- CORS configurato per sicurezza

## 📝 Note di Sviluppo

- **Backend**: FastAPI con validazione Pydantic
- **Frontend**: HTML5, CSS3 (Tailwind), JavaScript ES6+
- **Gestione File**: pandas + openpyxl per Excel
- **Calcoli**: NumPy per operazioni numeriche
- **UI/UX**: Design responsive con Tailwind CSS

## 🤝 Contributi

Per contribuire al progetto:
1. Fork del repository
2. Crea un branch per la feature
3. Implementa le modifiche
4. Testa accuratamente
5. Crea una Pull Request

## 📄 Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi il file LICENSE per i dettagli.

---

**Sviluppato con ❤️ per la gestione intelligente di file Excel**
