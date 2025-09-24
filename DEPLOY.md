# 🚀 Guida al Deploy del Progetto Excel Adjuster

## Opzioni di Hosting

### 1. Vercel (Raccomandato) ✅

**Vantaggi:**
- Supporta Python e FastAPI
- Deploy automatico da GitHub
- Hosting gratuito
- CDN globale

**Passaggi:**
1. Installa Vercel CLI: `npm i -g vercel`
2. Login: `vercel login`
3. Deploy: `vercel`
4. Segui le istruzioni

**File necessari:**
- `vercel.json` ✅ (già creato)
- `app_vercel.py` ✅ (già creato)
- `requirements.txt` ✅ (già presente)

### 2. Railway 🚂

**Vantaggi:**
- Supporta Python
- Deploy da GitHub
- Database incluso

**Passaggi:**
1. Vai su [railway.app](https://railway.app)
2. Connetti il repository GitHub
3. Railway rileverà automaticamente Python
4. Deploy automatico

### 3. Render 🎨

**Vantaggi:**
- Hosting gratuito per Python
- Deploy automatico
- SSL incluso

**Passaggi:**
1. Vai su [render.com](https://render.com)
2. Crea un nuovo Web Service
3. Connetti il repository GitHub
4. Configura:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`

### 4. Netlify + Backend Separato 🔄

**Per il Frontend (Netlify):**
1. Modifica `app.js` per puntare al backend remoto
2. Deploy su Netlify

**Per il Backend:**
- Usa una delle opzioni sopra (Vercel, Railway, Render)

## Modifiche Necessarie per il Deploy

### 1. Aggiorna app.js per il Backend Remoto

```javascript
// Cambia questa riga in app.js:
const API_BASE_URL = 'https://your-backend-url.vercel.app';

// Invece di:
const API_BASE_URL = 'http://localhost:8000';
```

### 2. Configura CORS

Il backend è già configurato per accettare richieste da qualsiasi origine (`allow_origins=["*"]`).

### 3. Variabili d'Ambiente (se necessario)

Per Vercel, puoi aggiungere variabili d'ambiente nel dashboard.

## Test del Deploy

Dopo il deploy, testa:
1. `GET /` - Dovrebbe restituire `{"message": "Excel Adjuster API", "status": "running"}`
2. `POST /introspect` - Testa l'upload di un file Excel
3. `POST /adjust` - Testa la correzione

## Domini di Esempio

- **Vercel**: `https://your-project.vercel.app`
- **Railway**: `https://your-project.railway.app`
- **Render**: `https://your-project.onrender.com`

## Note Importanti

⚠️ **Limitazioni del Piano Gratuito:**
- Vercel: 100GB bandwidth/mese
- Railway: 500 ore/mese
- Render: 750 ore/mese

💡 **Raccomandazione:**
Usa **Vercel** per il deploy completo (frontend + backend) o **Railway** per il backend + **Netlify** per il frontend.
