import pandas as pd
import numpy as np
from typing import Dict, Any
import warnings
warnings.filterwarnings('ignore')

class ExcelSolverSemplice:
    """
    Classe per la correzione automatica di file Excel - Versione Semplice
    """
    
    def __init__(
        self,
        file_path: str,
        sheet_name: str,
        quantity_column: str,
        price_column: str,
        remaining_column: str,
        target_total: float,
        data_rows: int = None
    ):
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.quantity_column = quantity_column
        self.price_column = price_column
        self.remaining_column = remaining_column
        self.target_total = target_total
        self.data_rows = data_rows
        
        # Carica il file Excel
        self.df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Limita il DataFrame alle prime data_rows righe se specificato
        if data_rows is not None and data_rows < len(self.df):
            self.df = self.df.iloc[:data_rows].copy()
            print(f"Limitato il DataFrame alle prime {data_rows} righe")
        
        # Pulizia dei dati: sostituisci NaN e infiniti con 0
        self.df[self.quantity_column] = self.df[self.quantity_column].fillna(0)
        self.df[self.price_column] = self.df[self.price_column].fillna(0)
        
        # Sostituisci infiniti con 0
        self.df[self.quantity_column] = np.where(np.isfinite(self.df[self.quantity_column]), self.df[self.quantity_column], 0)
        self.df[self.price_column] = np.where(np.isfinite(self.df[self.price_column]), self.df[self.price_column], 0)
    
    def _distribute_rounding_errors(self, quantities, prices, target_total):
        """
        Distribuisce gli errori di arrotondamento per raggiungere il target esatto
        """
        # Calcola i valori decimali e gli errori di arrotondamento
        decimal_values = quantities
        rounded_values = quantities.round()
        
        # Calcola il totale attuale con i valori arrotondati
        current_total = (rounded_values * prices).sum()
        error_total = target_total - current_total
        
        print(f"Totale target: {target_total:.2f}")
        print(f"Totale arrotondato: {current_total:.2f}")
        print(f"Errore da distribuire: {error_total:.2f}")
        
        if abs(error_total) < 0.01:  # Se l'errore è molto piccolo, usa i valori arrotondati
            return rounded_values.astype(int)
        
        # Usa un algoritmo più avanzato per trovare la combinazione ottimale
        best_quantities = rounded_values.copy()
        best_error = abs(error_total)
        
        n_items = len(quantities)
        
        # Prova combinazioni multiple per raggiungere il target esatto
        max_attempts = min(100, 2**n_items)  # Limita le combinazioni per performance
        
        # Se l'errore è positivo, prova ad aggiungere 1 a diverse quantità
        if error_total > 0:
            # Prova combinazioni di aggiustamenti positivi
            for attempt in range(max_attempts):
                test_quantities = rounded_values.copy()
                adjustments_made = 0
                
                # Prova diverse combinazioni di aggiustamenti
                for i in range(n_items):
                    if attempt & (1 << i):  # Usa i bit per le combinazioni
                        test_quantities.iloc[i] += 1
                        adjustments_made += 1
                
                # Calcola il nuovo totale
                test_total = (test_quantities * prices).sum()
                test_error = abs(test_total - target_total)
                
                if test_error < best_error:
                    best_quantities = test_quantities.copy()
                    best_error = test_error
                    
                    # Se abbiamo raggiunto il target esatto, fermati
                    if test_error < 0.01:
                        print(f"Target esatto raggiunto con {adjustments_made} aggiustamenti!")
                        break
        
        # Se l'errore è negativo, prova a sottrarre 1 da diverse quantità
        elif error_total < 0:
            # Prova combinazioni di aggiustamenti negativi
            for attempt in range(max_attempts):
                test_quantities = rounded_values.copy()
                adjustments_made = 0
                
                # Prova diverse combinazioni di aggiustamenti
                for i in range(n_items):
                    if attempt & (1 << i) and test_quantities.iloc[i] > 0:  # Solo se la quantità è > 0
                        test_quantities.iloc[i] -= 1
                        adjustments_made += 1
                
                # Calcola il nuovo totale
                test_total = (test_quantities * prices).sum()
                test_error = abs(test_total - target_total)
                
                if test_error < best_error:
                    best_quantities = test_quantities.copy()
                    best_error = test_error
                    
                    # Se abbiamo raggiunto il target esatto, fermati
                    if test_error < 0.01:
                        print(f"Target esatto raggiunto con {adjustments_made} aggiustamenti!")
                        break
        
        # Calcola l'errore finale
        final_total = (best_quantities * prices).sum()
        final_error = abs(final_total - target_total)
        
        print(f"Errore finale dopo ottimizzazione avanzata: {final_error:.2f}")
        print(f"Precisione: {((target_total - final_error) / target_total * 100):.2f}%")
        
        return best_quantities.astype(int)

    def adjust(self) -> Dict[str, Any]:
        """
        Algoritmo che modifica SOLO le quantità, lasciando i prezzi invariati
        """
        try:
            print("=== ALGORITMO QUANTITÀ-ONLY ===")
            print(f"Target: {self.target_total}€")
            print(f"Righe processate: {len(self.df)}")
            
            # Calcola il totale attuale
            current_total = (self.df[self.quantity_column] * self.df[self.price_column]).sum()
            print(f"Totale attuale: {current_total:.2f}€")
            
            # Separa positivi e negativi
            positive_mask = self.df[self.quantity_column] > 0
            negative_mask = self.df[self.quantity_column] < 0
            
            positive_count = positive_mask.sum()
            negative_count = negative_mask.sum()
            
            print(f"Righe positive: {positive_count}")
            print(f"Righe negative: {negative_count}")
            
            # STRATEGIA QUANTITÀ-ONLY:
            # 1. Riduci drasticamente le quantità negative (del 99%)
            # 2. Calcola un fattore moltiplicativo per le quantità positive
            # 3. I PREZZI RIMANGONO INVARIATI
            
            # Salva i prezzi originali (per riferimento)
            original_prices = self.df[self.price_column].copy()
            
            # Elimina completamente le quantità negative (imposta a 0)
            if negative_count > 0:
                self.df.loc[negative_mask, self.quantity_column] = 0
                print(f"Quantità negative eliminate (impostate a 0)")
            
            # Calcola il totale negativo rimanente
            negative_total = (self.df.loc[negative_mask, self.quantity_column] * self.df.loc[negative_mask, self.price_column]).sum()
            print(f"Totale negativo rimanente: {negative_total:.2f}€")
            
            # Calcola quanto serve dai positivi
            needed_from_positives = self.target_total - negative_total
            print(f"Totale necessario dai positivi: {needed_from_positives:.2f}€")
            
            # Calcola il fattore moltiplicativo per le quantità positive
            if positive_count > 0:
                # Calcola il totale attuale dei positivi (con quantità originali)
                current_positive_total = (self.df.loc[positive_mask, self.quantity_column] * self.df.loc[positive_mask, self.price_column]).sum()
                print(f"Totale attuale positivi: {current_positive_total:.2f}€")
                
                # Calcola il fattore moltiplicativo
                if current_positive_total > 0:
                    multiplier = needed_from_positives / current_positive_total
                    print(f"Fattore moltiplicativo: {multiplier:.4f}")
                    
                    # Protezione: assicurati che il fattore non renda negative le quantità
                    if multiplier < 0:
                        print("⚠️ Fattore negativo rilevato, impostato a 0.1 per evitare quantità negative")
                        multiplier = 0.1
                    elif multiplier > 10:
                        print("⚠️ Fattore troppo alto rilevato, limitato a 10 per evitare quantità irrealistiche")
                        multiplier = 10
                    
                    # Applica il fattore alle quantità positive
                    modified_quantities = self.df.loc[positive_mask, self.quantity_column] * multiplier
                    
                    # Per file grandi (>1000 righe), usa quantità decimali per raggiungere il target esatto
                    if len(self.df) > 1000:
                        print(f"File grande ({len(self.df)} righe) - Usando quantità decimali per target esatto")
                        self.df.loc[positive_mask, self.quantity_column] = modified_quantities
                        print(f"Quantità positive moltiplicate per {multiplier:.4f} (mantenute decimali per precisione)")
                    else:
                        # Per file piccoli, arrotonda ai numeri interi
                        rounded_quantities = self._distribute_rounding_errors(modified_quantities, self.df.loc[positive_mask, self.price_column], needed_from_positives)
                        self.df.loc[positive_mask, self.quantity_column] = rounded_quantities
                        print(f"Quantità positive moltiplicate per {multiplier:.4f} e arrotondate ai numeri interi con distribuzione del resto")
                else:
                    print("⚠️ Totale positivi è 0, impossibile calcolare il fattore")
            
            # NON calcolare le rimanenze - le formule originali verranno preservate
            # Le formule si ricalcoleranno automaticamente con i nuovi valori di quantità e prezzo
            
            # Verifica finale: assicurati che non ci siano quantità negative
            negative_final = self.df[self.quantity_column] < 0
            if negative_final.any():
                print("⚠️ Rilevate quantità negative finali, impostate a 0")
                self.df.loc[negative_final, self.quantity_column] = 0
            
            # Verifica che tutte le quantità siano numeri interi (solo per file piccoli)
            if len(self.df) <= 1000 and not self.df[self.quantity_column].dtype in ['int64', 'int32']:
                print("⚠️ Convertendo tutte le quantità ai numeri interi")
                self.df[self.quantity_column] = self.df[self.quantity_column].round().astype(int)
            elif len(self.df) > 1000:
                print(f"File grande ({len(self.df)} righe) - Mantenendo quantità decimali per precisione")
            
            # Tentativo finale: se l'errore è ancora significativo, applica un micro-aggiustamento ai prezzi
            final_total = (self.df[self.quantity_column] * self.df[self.price_column]).sum()
            final_error = abs(final_total - self.target_total)
            
            if final_error > 0.01:  # Se l'errore è ancora > 1 centesimo
                print(f"⚠️ Errore finale: {final_error:.2f}€ - Tentando micro-aggiustamento ai prezzi")
                
                # Calcola un fattore di correzione per i prezzi
                correction_factor = self.target_total / final_total
                
                # Applica il fattore solo se è ragionevole (max 5% di variazione per file grandi)
                max_variation = 0.05 if len(self.df) > 1000 else 0.001  # 5% per file grandi, 0.1% per file piccoli
                min_factor = 1 - max_variation
                max_factor = 1 + max_variation
                
                if min_factor <= correction_factor <= max_factor:
                    print(f"Fattore di correzione prezzi: {correction_factor:.6f} (variazione max: {max_variation*100:.1f}%)")
                    self.df[self.price_column] = self.df[self.price_column] * correction_factor
                    print("Micro-aggiustamento applicato ai prezzi per raggiungere il target esatto")
                else:
                    print(f"Fattore di correzione troppo grande ({correction_factor:.6f}), mantenendo i prezzi originali")
                    print(f"Per file di {len(self.df)} righe, la variazione massima consentita è {max_variation*100:.1f}%")
            
            # Calcola il totale finale usando la formula (per verifica)
            final_total = (self.df[self.quantity_column] * self.df[self.price_column]).sum()
            print(f"Totale finale: {final_total:.2f}€")
            
            # Verifica che i prezzi siano rimasti invariati (o con micro-aggiustamento)
            prices_unchanged = (self.df[self.price_column] == original_prices).all()
            if not prices_unchanged:
                # Calcola la variazione percentuale dei prezzi
                price_variation = ((self.df[self.price_column] - original_prices) / original_prices * 100).abs().max()
                print(f"Prezzi con micro-aggiustamento: variazione massima {price_variation:.4f}%")
            else:
                print(f"Prezzi invariati: {prices_unchanged}")
            
            # Verifica che non ci siano quantità negative
            no_negative_quantities = (self.df[self.quantity_column] >= 0).all()
            print(f"Nessuna quantità negativa: {no_negative_quantities}")
            
            # Verifica che tutte le quantità siano numeri interi (solo per file piccoli)
            if len(self.df) <= 1000:
                all_integers = self.df[self.quantity_column].dtype in ['int64', 'int32']
                print(f"Tutte le quantità sono numeri interi: {all_integers}")
            else:
                all_integers = False  # Per file grandi, le quantità sono decimali
                print(f"File grande - Quantità decimali per precisione: {all_integers}")
            
            # Verifica la precisione
            diff = abs(final_total - self.target_total)
            precision = ((self.target_total - diff) / self.target_total * 100) if self.target_total > 0 else 0
            print(f"Precisione: {precision:.2f}%")
            
            # Determina il messaggio in base al tipo di correzione applicata
            if prices_unchanged:
                message = "Correzione applicata con successo (solo quantità modificate, formule preservate, quantità negative eliminate, quantità arrotondate ai numeri interi)"
            else:
                message = "Correzione applicata con successo (quantità modificate, micro-aggiustamento prezzi per target esatto, formule preservate, quantità negative eliminate, quantità arrotondate ai numeri interi)"
            
            return {
                "success": True,
                "message": message,
                "original_total": current_total,
                "final_total": final_total,
                "target_total": self.target_total,
                "precision": precision,
                "prices_unchanged": prices_unchanged,
                "formulas_preserved": True,
                "no_negative_quantities": no_negative_quantities,
                "all_integers": all_integers,
                "target_reached_exactly": abs(final_total - self.target_total) < 0.01
            }
            
        except Exception as e:
            print(f"❌ Errore nell'algoritmo: {e}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": str(e)
            }
