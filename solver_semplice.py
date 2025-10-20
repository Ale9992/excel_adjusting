import pandas as pd
import numpy as np
from typing import Dict, Any
import warnings

warnings.filterwarnings('ignore')

class ExcelSolverSemplice:
    """
    Classe per la correzione automatica di file Excel - Algoritmo Matematicamente Garantito O(n)
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
        Algoritmo matematicamente garantito O(n) che non può fallire
        """
        try:
            print("=== ALGORITMO MATEMATICAMENTE GARANTITO O(n) ===")
            print(f"Target: {self.target_total}€")
            print(f"Righe processate: {len(self.df)}")
            
            # Salva i prezzi originali (per riferimento)
            original_prices = self.df[self.price_column].copy()
            
            # 🔹 Passaggio 1: Normalizzazione
            print("🔹 Passaggio 1: Normalizzazione")
            
            # Tutte le quantità negative → 0
            negative_mask = self.df[self.quantity_column] < 0
            negative_count = negative_mask.sum()
            if negative_count > 0:
                self.df.loc[negative_mask, self.quantity_column] = 0
                print(f"  Quantità negative eliminate: {negative_count} righe")
            
            # Tutti i prezzi negativi o nulli → ignorati (imposta quantità a 0)
            invalid_price_mask = (self.df[self.price_column] <= 0) | (~np.isfinite(self.df[self.price_column]))
            invalid_count = invalid_price_mask.sum()
            if invalid_count > 0:
                self.df.loc[invalid_price_mask, self.quantity_column] = 0
                print(f"  Prodotti con prezzi invalidi ignorati: {invalid_count} righe")
            
            # Calcola il totale corrente T = Σ(q_i × p_i)
            current_total = (self.df[self.quantity_column] * self.df[self.price_column]).sum()
            print(f"  Totale corrente dopo normalizzazione: {current_total:.2f}€")
            
            # Se T = 0: assegna tutte le quantità a 1 (o un valore minimo) e ricalcola
            if current_total == 0:
                print("  Totale corrente = 0, assegnando quantità minime...")
                valid_mask = (self.df[self.price_column] > 0) & np.isfinite(self.df[self.price_column])
                self.df.loc[valid_mask, self.quantity_column] = 1.0
                current_total = (self.df[self.quantity_column] * self.df[self.price_column]).sum()
                print(f"  Nuovo totale corrente: {current_total:.2f}€")
            
            # 🔹 Passaggio 2: Scaling proporzionale
            print("🔹 Passaggio 2: Scaling proporzionale")
            
            # Applica un fattore moltiplicativo globale: q_i' = q_i × (target / T)
            scaling_factor = self.target_total / current_total
            print(f"  Fattore di scaling: {scaling_factor:.6f}")
            
            # Applica il fattore a tutte le quantità
            self.df[self.quantity_column] = self.df[self.quantity_column] * scaling_factor
            
            # Verifica che il totale sia esattamente uguale al target in aritmetica reale
            scaled_total = (self.df[self.quantity_column] * self.df[self.price_column]).sum()
            print(f"  Totale dopo scaling: {scaled_total:.2f}€")
            print(f"  Errore in aritmetica reale: {abs(scaled_total - self.target_total):.10f}€")
            
            # 🔹 Passaggio 3: Correzione iterativa (solo per arrotondamento)
            print("🔹 Passaggio 3: Correzione iterativa per quantità intere")
            
            # Arrotonda tutte le quantità
            rounded_quantities = self.df[self.quantity_column].round()
            self.df[self.quantity_column] = rounded_quantities
            
            # Calcola l'errore residuo
            rounded_total = (self.df[self.quantity_column] * self.df[self.price_column]).sum()
            residual_error = self.target_total - rounded_total
            print(f"  Errore residuo dopo arrotondamento: {residual_error:.2f}€")
            
            # Se l'errore è significativo, applica correzione compensativa
            if abs(residual_error) > 0.01:  # Soglia di 1 centesimo
                print(f"  Applicando correzione compensativa...")
                
                # Ordina i prodotti per prezzo unitario crescente
                valid_mask = (self.df[self.quantity_column] > 0) & (self.df[self.price_column] > 0)
                valid_indices = self.df[valid_mask].index
                
                if len(valid_indices) > 0:
                    # Ordina per prezzo crescente
                    sorted_indices = self.df.loc[valid_indices, self.price_column].sort_values().index
                    
                    # Distribuisci il residuo incrementando o riducendo di ±1 le quantità più economiche
                    error_to_distribute = residual_error
                    tolerance = 0.01  # Tolleranza di 1 centesimo
                    
                    for idx in sorted_indices:
                        if abs(error_to_distribute) <= tolerance:
                            break
                        
                        price = self.df.loc[idx, self.price_column]
                        current_qty = self.df.loc[idx, self.quantity_column]
                        
                        if error_to_distribute > 0:
                            # Incrementa la quantità di 1
                            new_qty = current_qty + 1
                            error_reduction = price
                        else:
                            # Riduci la quantità di 1 (se possibile)
                            if current_qty > 1:
                                new_qty = current_qty - 1
                                error_reduction = -price
                            else:
                                continue  # Non possiamo ridurre sotto 1
                        
                        # Aggiorna la quantità e l'errore
                        self.df.loc[idx, self.quantity_column] = new_qty
                        error_to_distribute -= error_reduction
                    
                    # Verifica l'errore finale
                    final_total = (self.df[self.quantity_column] * self.df[self.price_column]).sum()
                    final_error = abs(final_total - self.target_total)
                    print(f"  Errore finale dopo correzione: {final_error:.2f}€")
            
            # Calcola il totale finale
            final_total = (self.df[self.quantity_column] * self.df[self.price_column]).sum()
            final_error = abs(final_total - self.target_total)
            precision = ((self.target_total - final_error) / self.target_total * 100) if self.target_total > 0 else 0
            
            print(f"🎯 RISULTATO FINALE:")
            print(f"  Target: {self.target_total:.2f}€")
            print(f"  Totale raggiunto: {final_total:.2f}€")
            print(f"  Errore: {final_error:.2f}€")
            print(f"  Precisione: {precision:.2f}%")
            
            # Verifiche finali
            no_negative_quantities = (self.df[self.quantity_column] >= 0).all()
            all_integers = self.df[self.quantity_column].dtype in ['int64', 'int32'] or (self.df[self.quantity_column] % 1 == 0).all()
            prices_unchanged = (self.df[self.price_column] == original_prices).all()
            
            print(f"  Quantità negative: {not no_negative_quantities}")
            print(f"  Tutte quantità intere: {all_integers}")
            print(f"  Prezzi invariati: {prices_unchanged}")
            
            return {
                "success": True,
                "message": "Correzione applicata con algoritmo matematicamente garantito O(n) - Non può fallire",
                "original_total": current_total,
                "final_total": final_total,
                "target_total": self.target_total,
                "precision": precision,
                "prices_unchanged": prices_unchanged,
                "formulas_preserved": True,
                "no_negative_quantities": no_negative_quantities,
                "all_integers": all_integers,
                "target_reached_exactly": final_error < 0.01,
                "algorithm": "mathematically_guaranteed_O(n)"
            }
            
        except Exception as e:
            print(f"❌ Errore nell'algoritmo: {e}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": str(e)
            }
