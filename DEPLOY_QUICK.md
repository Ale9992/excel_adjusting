# ⚡ Deploy Rapido su Render

## 🚀 Passaggi Essenziali

### 1. Push su GitHub
```bash
git add .
git commit -m "Preparazione per deploy su Render"
git push origin main
```

### 2. Deploy su Render
1. Vai su [render.com](https://render.com)
2. Registrati e connetti GitHub
3. Clicca "New +" → "Blueprint"
4. Seleziona il repository
5. Render userà automaticamente `render.yaml`
6. Clicca "Apply"

### 3. Attendi il Deploy
- Build: 2-3 minuti
- Deploy: 1-2 minuti
- URL: `https://excel-adjuster.onrender.com`

## ✅ File di Configurazione (Già Pronti)

- `render.yaml` - Configurazione automatica
- `Procfile` - Comando di avvio
- `requirements.txt` - Dipendenze Python
- `runtime.txt` - Versione Python

## 🔧 Configurazione Automatica

Render userà queste impostazioni:
- **Nome**: excel-adjuster
- **Piano**: Free
- **Build**: `pip install -r requirements.txt`
- **Start**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
- **Python**: 3.11.10

## 📚 Documentazione Completa

Per dettagli completi, vedi [DEPLOY_RENDER.md](DEPLOY_RENDER.md)

---

**🎉 In 5 minuti la tua app sarà online!**
