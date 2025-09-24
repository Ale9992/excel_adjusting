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
        Algoritmo semplice: Riduci drasticamente le quantità negative e imposta prezzo fisso per i positivi
        """
        try:
            print("=== ALGORITMO SEMPLICE ===")
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
            
            # STRATEGIA SEMPLICE:
            # 1. Riduci drasticamente le quantità negative (del 99%)
            # 2. Imposta quantità fissa di 1 per tutti i positivi
            # 3. Calcola il prezzo fisso per raggiungere esattamente il target
            
            # Riduci le quantità negative del 99%
            if negative_count > 0:
                self.df.loc[negative_mask, self.quantity_column] = self.df.loc[negative_mask, self.quantity_column] * 0.01
            
            # Imposta quantità fissa di 1 per tutti i positivi
            if positive_count > 0:
                self.df.loc[positive_mask, self.quantity_column] = 1
            
            # Calcola il totale negativo rimanente
            negative_total = (self.df.loc[negative_mask, self.quantity_column] * self.df.loc[negative_mask, self.price_column]).sum()
            print(f"Totale negativo rimanente: {negative_total:.2f}€")
            
            # Calcola quanto serve dai positivi
            needed_from_positives = self.target_total - negative_total
            print(f"Totale necessario dai positivi: {needed_from_positives:.2f}€")
            
            # Calcola il prezzo fisso per i positivi
            if positive_count > 0:
                fixed_price = needed_from_positives / positive_count
                print(f"Prezzo fisso per positivi: €{fixed_price:.2f}")
                
                # Imposta il prezzo fisso per tutti i positivi
                self.df.loc[positive_mask, self.price_column] = fixed_price
            
            # Calcola le nuove rimanenze
            self.df[self.remaining_column] = self.df[self.quantity_column] * self.df[self.price_column]
            
            # Calcola il totale finale
            final_total = self.df[self.remaining_column].sum()
            print(f"Totale finale: {final_total:.2f}€")
            
            # Verifica la precisione
            diff = abs(final_total - self.target_total)
            precision = ((self.target_total - diff) / self.target_total * 100) if self.target_total > 0 else 0
            print(f"Precisione: {precision:.2f}%")
            
            return {
                "success": True,
                "message": "Correzione applicata con successo",
                "original_total": current_total,
                "final_total": final_total,
                "target_total": self.target_total,
                "precision": precision
            }
            
        except Exception as e:
            print(f"❌ Errore nell'algoritmo: {e}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": str(e)
            }
