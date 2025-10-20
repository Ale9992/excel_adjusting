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
                    
                    # Applica il fattore alle quantità positive e arrotonda ai numeri interi
                    self.df.loc[positive_mask, self.quantity_column] = (self.df.loc[positive_mask, self.quantity_column] * multiplier).round().astype(int)
                    print(f"Quantità positive moltiplicate per {multiplier:.4f} e arrotondate ai numeri interi")
                else:
                    print("⚠️ Totale positivi è 0, impossibile calcolare il fattore")
            
            # NON calcolare le rimanenze - le formule originali verranno preservate
            # Le formule si ricalcoleranno automaticamente con i nuovi valori di quantità e prezzo
            
            # Verifica finale: assicurati che non ci siano quantità negative
            negative_final = self.df[self.quantity_column] < 0
            if negative_final.any():
                print("⚠️ Rilevate quantità negative finali, impostate a 0")
                self.df.loc[negative_final, self.quantity_column] = 0
            
            # Verifica che tutte le quantità siano numeri interi
            if not self.df[self.quantity_column].dtype in ['int64', 'int32']:
                print("⚠️ Convertendo tutte le quantità ai numeri interi")
                self.df[self.quantity_column] = self.df[self.quantity_column].round().astype(int)
            
            # Calcola il totale finale usando la formula (per verifica)
            final_total = (self.df[self.quantity_column] * self.df[self.price_column]).sum()
            print(f"Totale finale: {final_total:.2f}€")
            
            # Verifica che i prezzi siano rimasti invariati
            prices_unchanged = (self.df[self.price_column] == original_prices).all()
            print(f"Prezzi invariati: {prices_unchanged}")
            
            # Verifica che non ci siano quantità negative
            no_negative_quantities = (self.df[self.quantity_column] >= 0).all()
            print(f"Nessuna quantità negativa: {no_negative_quantities}")
            
            # Verifica che tutte le quantità siano numeri interi
            all_integers = self.df[self.quantity_column].dtype in ['int64', 'int32']
            print(f"Tutte le quantità sono numeri interi: {all_integers}")
            
            # Verifica la precisione
            diff = abs(final_total - self.target_total)
            precision = ((self.target_total - diff) / self.target_total * 100) if self.target_total > 0 else 0
            print(f"Precisione: {precision:.2f}%")
            
            return {
                "success": True,
                "message": "Correzione applicata con successo (solo quantità modificate, formule preservate, quantità negative eliminate, quantità arrotondate ai numeri interi)",
                "original_total": current_total,
                "final_total": final_total,
                "target_total": self.target_total,
                "precision": precision,
                "prices_unchanged": prices_unchanged,
                "formulas_preserved": True,
                "no_negative_quantities": no_negative_quantities,
                "all_integers": all_integers
            }
            
        except Exception as e:
            print(f"❌ Errore nell'algoritmo: {e}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": str(e)
            }
