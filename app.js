// Configurazione API
// Rileva automaticamente se siamo in produzione o sviluppo
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
    ? 'http://localhost:8000' 
    : window.location.origin;

// Debug: log dell'URL API utilizzato
console.log('API Base URL:', API_BASE_URL);
console.log('Current hostname:', window.location.hostname);

// Elementi DOM
const elements = {
    form: document.getElementById('excelForm'),
    fileInput: document.getElementById('excelFile'),
    fileInfo: document.getElementById('fileInfo'),
    fileName: document.getElementById('fileName'),
    sheetSection: document.getElementById('sheetSection'),
    sheetSelect: document.getElementById('sheetSelect'),
    columnSection: document.getElementById('columnSection'),
    quantityColumn: document.getElementById('quantityColumn'),
    priceColumn: document.getElementById('priceColumn'),
    remainingColumn: document.getElementById('remainingColumn'),
    targetSection: document.getElementById('targetSection'),
    targetTotal: document.getElementById('targetTotal'),
    dataRowsSection: document.getElementById('dataRowsSection'),
    dataRows: document.getElementById('dataRows'),
    infoSection: document.getElementById('infoSection'),
    toggleInfo: document.getElementById('toggleInfo'),
    infoToggleText: document.getElementById('infoToggleText'),
    submitBtn: document.getElementById('submitBtn'),
    statusCard: document.getElementById('statusCard'),
    statusMessage: document.getElementById('statusMessage'),
    errorCard: document.getElementById('errorCard'),
    errorMessage: document.getElementById('errorMessage'),
    loadingOverlay: document.getElementById('loadingOverlay'),
    loadingMessage: document.getElementById('loadingMessage'),
    columnAnalysisInfo: document.getElementById('columnAnalysisInfo')
};

// Stato dell'applicazione
let appState = {
    currentFile: null,
    sheetData: null,
    isInfoOpen: false
};

// Inizializzazione
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    hideAllSections();
    testAPIConnection();
});

// Testa la connessione all'API all'avvio
async function testAPIConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/status`);
        if (response.ok) {
            const data = await response.json();
            console.log('✅ Connessione API OK:', data);
        } else {
            console.warn('⚠️ API non raggiungibile:', response.status);
        }
    } catch (error) {
        console.error('❌ Errore connessione API:', error);
        showMessage('error', 'Attenzione: Il server non è raggiungibile. Verifica la connessione.');
    }
}

function initializeEventListeners() {
    // File input change
    elements.fileInput.addEventListener('change', handleFileSelect);
    
    // Sheet selection change
    elements.sheetSelect.addEventListener('change', handleSheetSelect);
    
    // Column selections change
    elements.quantityColumn.addEventListener('change', validateForm);
    elements.priceColumn.addEventListener('change', validateForm);
    elements.remainingColumn.addEventListener('change', validateForm);
    elements.targetTotal.addEventListener('input', validateForm);
    elements.dataRows.addEventListener('input', validateForm);
    
    // Advanced options toggle
    elements.toggleInfo.addEventListener('click', toggleInfoSection);
    
    // Form submission
    elements.form.addEventListener('submit', handleFormSubmit);
    
    // Drag and drop
    const dropZone = document.getElementById('dropZone');
    const uploadArea = document.getElementById('uploadArea');
    const dragOverlay = document.getElementById('dragOverlay');
    const removeFileBtn = document.getElementById('removeFile');
    
    if (dropZone) {
        dropZone.addEventListener('dragover', handleDragOver);
        dropZone.addEventListener('drop', handleDrop);
        dropZone.addEventListener('dragleave', handleDragLeave);
        dropZone.addEventListener('dragenter', handleDragEnter);
    }
    
    if (removeFileBtn) {
        removeFileBtn.addEventListener('click', handleRemoveFile);
    }
}

function hideAllSections() {
    elements.sheetSection.classList.add('hidden');
    elements.columnSection.classList.add('hidden');
    elements.targetSection.classList.add('hidden');
    elements.advancedSection.classList.add('hidden');
    
    // Nascondi anche la card di informazioni del file
    const fileInfo = document.getElementById('fileInfo');
    if (fileInfo) {
        fileInfo.classList.add('hidden');
    }
    
    hideMessages();
}

function hideMessages() {
    elements.statusCard.classList.add('hidden');
    elements.errorCard.classList.add('hidden');
}

function showMessage(type, message) {
    hideMessages();
    if (type === 'status') {
        elements.statusMessage.textContent = message;
        elements.statusCard.classList.remove('hidden');
    } else if (type === 'error') {
        elements.errorMessage.textContent = message;
        elements.errorCard.classList.remove('hidden');
    }
}

function showLoading(message = 'Elaborazione in corso...') {
    elements.loadingMessage.textContent = message;
    elements.loadingOverlay.classList.remove('hidden');
}

function hideLoading() {
    elements.loadingOverlay.classList.add('hidden');
}

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        processFile(file);
    }
}

function handleDragEnter(event) {
    event.preventDefault();
    const dragOverlay = document.getElementById('dragOverlay');
    if (dragOverlay) {
        dragOverlay.style.opacity = '1';
    }
}

function handleDragOver(event) {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'copy';
}

function handleDragLeave(event) {
    event.preventDefault();
    // Solo nascondi l'overlay se stiamo uscendo completamente dalla drop zone
    if (!event.currentTarget.contains(event.relatedTarget)) {
        const dragOverlay = document.getElementById('dragOverlay');
        if (dragOverlay) {
            dragOverlay.style.opacity = '0';
        }
    }
}

function handleDrop(event) {
    event.preventDefault();
    
    // Nascondi l'overlay
    const dragOverlay = document.getElementById('dragOverlay');
    if (dragOverlay) {
        dragOverlay.style.opacity = '0';
    }
    
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        const file = files[0];
        if (file.name.endsWith('.xlsx') || file.name.endsWith('.xls')) {
            elements.fileInput.files = files;
            processFile(file);
        } else {
            showMessage('error', 'Per favore seleziona un file Excel (.xlsx o .xls)');
        }
    }
}

function handleRemoveFile() {
    // Reset del file input
    elements.fileInput.value = '';
    
    // Nascondi le sezioni
    hideAllSections();
    
    // Nascondi le informazioni del file
    const fileInfo = document.getElementById('fileInfo');
    if (fileInfo) {
        fileInfo.classList.add('hidden');
    }
    
    // Reset dello stato
    appState.currentFile = null;
    appState.sheetData = null;
    
    showMessage('status', 'File rimosso. Puoi caricare un nuovo file.');
}

async function processFile(file) {
    // Validazione file
    if (!file.name.endsWith('.xlsx') && !file.name.endsWith('.xls')) {
        showMessage('error', 'Per favore seleziona un file Excel (.xlsx o .xls)');
        return;
    }
    
    if (file.size > 10 * 1024 * 1024) { // 10MB
        showMessage('error', 'Il file è troppo grande. Dimensione massima: 10MB');
        return;
    }
    
    appState.currentFile = file;
    
    // Aggiorna il nome del file nel nuovo design
    const fileNameElement = document.getElementById('fileName');
    if (fileNameElement) {
        fileNameElement.textContent = file.name;
    }
    
    // Mostra la card di informazioni del file
    const fileInfo = document.getElementById('fileInfo');
    if (fileInfo) {
        fileInfo.classList.remove('hidden');
    }
    
    showMessage('status', 'Analisi del file in corso...');
    showLoading('Analisi del file Excel...');
    
    try {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch(`${API_BASE_URL}/introspect`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Errore nell\'analisi del file');
        }
        
        const data = await response.json();
        appState.sheetData = data.sheets;
        
        populateSheetSelect(data.sheets);
        elements.sheetSection.classList.remove('hidden');
        
        const fileExtension = file.name.split('.').pop().toLowerCase();
        let statusMessage = `File analizzato con successo. Trovati ${Object.keys(data.sheets).length} fogli di lavoro.`;
        if (fileExtension === 'xls') {
            statusMessage += ' (File .xls convertito automaticamente in .xlsx)';
        }
        showMessage('status', statusMessage);
        
    } catch (error) {
        console.error('Errore nell\'analisi del file:', error);
        let errorMessage = 'Errore nell\'analisi del file';
        
        if (error.message.includes('Load failed') || error.message.includes('fetch')) {
            errorMessage = 'Errore di connessione. Verifica che il server sia attivo e raggiungibile.';
        } else if (error.message.includes('JSON')) {
            errorMessage = 'Il file contiene dati non validi. Verifica che le colonne numeriche non contengano valori infiniti o non numerici';
        } else if (error.message.includes('network') || error.message.includes('fetch')) {
            errorMessage = 'Errore di connessione al server. Assicurati che il backend sia in esecuzione';
        } else {
            errorMessage = `Errore nell'analisi del file: ${error.message}`;
        }
        
        showMessage('error', errorMessage);
    } finally {
        hideLoading();
    }
}

function populateSheetSelect(sheets) {
    elements.sheetSelect.innerHTML = '<option value="">Seleziona un foglio...</option>';
    
    Object.keys(sheets).forEach(sheetName => {
        const sheet = sheets[sheetName];
        const option = document.createElement('option');
        option.value = sheetName;
        option.textContent = `${sheetName} (${sheet.row_count} righe, ${sheet.columns.length} colonne numeriche)`;
        elements.sheetSelect.appendChild(option);
    });
}

function handleSheetSelect(event) {
    const sheetName = event.target.value;
    if (sheetName && appState.sheetData) {
        const sheet = appState.sheetData[sheetName];
        const suggestedColumns = sheet.suggested_columns || null;
        const excelMapping = sheet.excel_column_mapping || null;
        populateColumnSelects(sheet.columns, suggestedColumns, excelMapping);
        elements.columnSection.classList.remove('hidden');
        
        let statusMessage = `Foglio "${sheetName}" selezionato. ${sheet.columns.length} colonne numeriche disponibili.`;
        if (suggestedColumns && (suggestedColumns.quantity || suggestedColumns.price || suggestedColumns.remaining)) {
            statusMessage += ' Colonne suggerite automaticamente basate sui pattern dei dati.';
            elements.columnAnalysisInfo.classList.remove('hidden');
        } else {
            statusMessage += ' Seleziona le colonne usando le lettere Excel (A, B, C...).';
            elements.columnAnalysisInfo.classList.add('hidden');
        }
        showMessage('status', statusMessage);
    } else {
        elements.columnSection.classList.add('hidden');
        elements.targetSection.classList.add('hidden');
    }
}

function populateColumnSelects(columns, suggestedColumns = null, excelMapping = null) {
    const columnSelects = [
        { select: elements.quantityColumn, type: 'quantity' },
        { select: elements.priceColumn, type: 'price' },
        { select: elements.remainingColumn, type: 'remaining' }
    ];
    
    columnSelects.forEach(({ select, type }) => {
        select.innerHTML = '<option value="">Seleziona colonna...</option>';
        
        // Aggiungi le colonne con lettere Excel se disponibili
        columns.forEach((column, index) => {
            const option = document.createElement('option');
            option.value = column;
            
            // Usa la lettera Excel se disponibile, altrimenti usa il nome della colonna
            let displayText = column;
            if (excelMapping) {
                // Trova la lettera Excel per questa colonna
                const excelLetter = Object.keys(excelMapping).find(letter => excelMapping[letter] === column);
                if (excelLetter) {
                    displayText = `Colonna ${excelLetter} (${column})`;
                }
            }
            
            // Controlla se questa colonna è suggerita per questo tipo
            if (suggestedColumns && suggestedColumns[type] === column) {
                option.textContent = `${displayText} (suggerita)`;
                option.style.fontWeight = 'bold';
                option.style.color = '#059669'; // Verde
            } else {
                option.textContent = displayText;
            }
            
            select.appendChild(option);
        });
        
        // Auto-seleziona la colonna suggerita se disponibile
        if (suggestedColumns && suggestedColumns[type]) {
            select.value = suggestedColumns[type];
        }
    });
    
    // Se non ci sono colonne suggerite, usa l'auto-selezione basata sui nomi
    if (!suggestedColumns || (!suggestedColumns.quantity && !suggestedColumns.price && !suggestedColumns.remaining)) {
        autoSelectColumns(columns);
    }
}

function autoSelectColumns(columns) {
    // Cerca colonne per quantità
    const quantityCandidates = columns.filter(col => 
        col.toLowerCase().includes('quantità') || 
        col.toLowerCase().includes('qty') || 
        col.toLowerCase().includes('quantity') ||
        col.toLowerCase().includes('pezzi')
    );
    
    // Cerca colonne per prezzo
    const priceCandidates = columns.filter(col => 
        col.toLowerCase().includes('prezzo') || 
        col.toLowerCase().includes('price') || 
        col.toLowerCase().includes('costo') ||
        col.toLowerCase().includes('cost')
    );
    
    // Cerca colonne per rimanenze
    const remainingCandidates = columns.filter(col => 
        col.toLowerCase().includes('rimanenze') || 
        col.toLowerCase().includes('remaining') || 
        col.toLowerCase().includes('totale') ||
        col.toLowerCase().includes('total') ||
        col.toLowerCase().includes('valore')
    );
    
    // Auto-seleziona se trova corrispondenze
    if (quantityCandidates.length > 0) {
        elements.quantityColumn.value = quantityCandidates[0];
        console.log(`Auto-selezionata colonna quantità: ${quantityCandidates[0]}`);
    }
    
    if (priceCandidates.length > 0) {
        elements.priceColumn.value = priceCandidates[0];
        console.log(`Auto-selezionata colonna prezzo: ${priceCandidates[0]}`);
    }
    
    if (remainingCandidates.length > 0) {
        elements.remainingColumn.value = remainingCandidates[0];
        console.log(`Auto-selezionata colonna rimanenze: ${remainingCandidates[0]}`);
    }
    
    // Valida il form dopo l'auto-selezione
    validateForm();
}

function validateForm() {
    const hasQuantity = elements.quantityColumn.value !== '';
    const hasPrice = elements.priceColumn.value !== '';
    const hasRemaining = elements.remainingColumn.value !== '';
    const hasTarget = elements.targetTotal.value !== '' && parseFloat(elements.targetTotal.value) > 0;
    const hasDataRows = elements.dataRows.value !== '' && parseInt(elements.dataRows.value) > 0;
    
    console.log('Validazione form:', {
        hasQuantity,
        hasPrice,
        hasRemaining,
        hasTarget,
        hasDataRows,
        quantityValue: elements.quantityColumn.value,
        priceValue: elements.priceColumn.value,
        remainingValue: elements.remainingColumn.value,
        targetValue: elements.targetTotal.value,
        dataRowsValue: elements.dataRows.value
    });
    
    if (hasQuantity && hasPrice && hasRemaining) {
        elements.targetSection.classList.remove('hidden');
        elements.dataRowsSection.classList.remove('hidden');
        
        if (hasTarget && hasDataRows) {
            elements.submitBtn.disabled = false;
            elements.submitBtn.classList.remove('opacity-50', 'cursor-not-allowed');
        } else {
            elements.submitBtn.disabled = true;
            elements.submitBtn.classList.add('opacity-50', 'cursor-not-allowed');
        }
    } else {
        elements.targetSection.classList.add('hidden');
        elements.submitBtn.disabled = true;
        elements.submitBtn.classList.add('opacity-50', 'cursor-not-allowed');
    }
}

function toggleInfoSection() {
    appState.isInfoOpen = !appState.isInfoOpen;
    
    if (appState.isInfoOpen) {
        elements.infoSection.classList.remove('hidden');
        elements.infoToggleText.innerHTML = '<i class="fas fa-chevron-up mr-1"></i>Nascondi come funziona';
    } else {
        elements.infoSection.classList.add('hidden');
        elements.infoToggleText.innerHTML = '<i class="fas fa-chevron-down mr-1"></i>Mostra come funziona';
    }
}


async function handleFormSubmit(event) {
    event.preventDefault();
    
    console.log('=== SUBMISSION STARTED ===');
    console.log('Current file:', appState.currentFile?.name);
    console.log('Form data:', new FormData(event.target));
    
    if (!appState.currentFile) {
        showMessage('error', 'Per favore seleziona un file Excel');
        return;
    }
    
    // Validazione form
    const formData = new FormData(event.target);
    const quantityColumn = formData.get('quantityColumn');
    const priceColumn = formData.get('priceColumn');
    const remainingColumn = formData.get('remainingColumn');
    const targetTotal = parseFloat(formData.get('targetTotal'));
    
    if (!quantityColumn || !priceColumn || !remainingColumn) {
        showMessage('error', 'Per favore seleziona tutte le colonne richieste');
        return;
    }
    
    if (targetTotal <= 0) {
        showMessage('error', 'Il totale target deve essere maggiore di 0');
        return;
    }
    
    // Verifica che le colonne siano diverse
    if (quantityColumn === priceColumn || quantityColumn === remainingColumn || priceColumn === remainingColumn) {
        showMessage('error', 'Le colonne selezionate devono essere diverse tra loro');
        return;
    }
    
    showLoading('Applicazione della correzione ai valori...');
    hideMessages();
    
    // Disabilita il pulsante per evitare doppi click
    elements.submitBtn.disabled = true;
    elements.submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Elaborazione...';
    
    try {
        const submitFormData = new FormData();
        submitFormData.append('file', appState.currentFile);
        submitFormData.append('sheet_name', formData.get('sheetSelect'));
        submitFormData.append('quantity_column', quantityColumn);
        submitFormData.append('price_column', priceColumn);
        submitFormData.append('remaining_column', remainingColumn);
        submitFormData.append('target_total', targetTotal);
        submitFormData.append('data_rows', elements.dataRows.value);
        // Nuova logica intelligente - non servono più parametri di variazione
        
        console.log('Invio richiesta a /adjust...');
        console.log('URL:', `${API_BASE_URL}/adjust`);
        console.log('FormData entries:');
        for (let [key, value] of submitFormData.entries()) {
            console.log(`  ${key}:`, value);
        }
        
        const response = await fetch(`${API_BASE_URL}/adjust`, {
            method: 'POST',
            body: submitFormData
        });
        
        console.log('Risposta ricevuta:', response.status, response.statusText);
        console.log('Headers:', Object.fromEntries(response.headers.entries()));
        
        if (!response.ok) {
            let errorMessage = 'Errore nella correzione del file';
            try {
                const errorData = await response.json();
                errorMessage = errorData.detail || errorMessage;
            } catch (e) {
                errorMessage = `Errore HTTP ${response.status}: ${response.statusText}`;
            }
            throw new Error(errorMessage);
        }
        
        // Verifica che la risposta sia un file
        const contentType = response.headers.get('content-type');
        console.log('Content-Type:', contentType);
        
        if (!contentType || !contentType.includes('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')) {
            throw new Error('La risposta non è un file Excel valido');
        }
        
        // Scarica il file
        console.log('Creazione blob...');
        const blob = await response.blob();
        console.log('Blob creato, dimensione:', blob.size);
        console.log('Blob type:', blob.type);
        
        if (blob.size === 0) {
            throw new Error('Il file scaricato è vuoto');
        }
        
        console.log('Creazione URL per download...');
        const url = window.URL.createObjectURL(blob);
        console.log('URL creato:', url);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = `adjusted_${appState.currentFile.name}`;
        a.style.display = 'none';
        console.log('Nome file download:', a.download);
        
        document.body.appendChild(a);
        console.log('Elemento aggiunto al DOM, avvio download...');
        
        // Prova il download automatico
        try {
            a.click();
            console.log('Download automatico avviato');
        } catch (error) {
            console.error('Errore download automatico:', error);
            // Fallback: apri in nuova finestra
            window.open(url, '_blank');
            console.log('Apertura in nuova finestra come fallback');
        }
        
        // Pulisce dopo un breve delay
        setTimeout(() => {
            window.URL.revokeObjectURL(url);
            if (document.body.contains(a)) {
                document.body.removeChild(a);
            }
            console.log('Cleanup completato');
        }, 1000);
        
        showMessage('status', `File corretto e scaricato con successo!<br>Nome file: adjusted_${appState.currentFile.name}<br>Dimensione: ${(blob.size / 1024).toFixed(1)} KB`);
        
        // Estrae le statistiche dagli header della risposta
        const originalTotal = parseFloat(response.headers.get('X-Original-Total') || '0');
        const finalTotal = parseFloat(response.headers.get('X-Final-Total') || '0');
        const difference = parseFloat(response.headers.get('X-Difference') || '0');
        const rowsProcessed = parseInt(response.headers.get('X-Rows-Processed') || '0');
        
        console.log('Statistiche ricevute:', {
            originalTotal,
            targetTotal,
            finalTotal,
            difference,
            rowsProcessed
        });
        
        // File corretto con successo
        
    } catch (error) {
        console.error('Errore nella correzione:', error);
        showMessage('error', `Errore nella correzione del file: ${error.message}`);
    } finally {
        hideLoading();
        // Riabilita il pulsante
        elements.submitBtn.disabled = false;
        elements.submitBtn.innerHTML = '<i class="fas fa-magic mr-2"></i>Esegui Correzione';
    }
}

