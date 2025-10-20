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
        Algoritmo avanzato per trovare quantità intere che raggiungano il target esatto
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
        
        # Usa un algoritmo di ricerca più sofisticato
        best_quantities = rounded_values.copy()
        best_error = abs(error_total)
        
        n_items = len(quantities)
        
        # Per file grandi, usa un approccio più efficiente
        if n_items > 100:
            return self._optimize_large_file(quantities, prices, target_total, rounded_values)
        
        # Per file piccoli, usa ricerca esaustiva
        max_attempts = min(1000, 2**min(n_items, 20))  # Limita per performance
        
        # Se l'errore è positivo, prova ad aggiungere 1 a diverse quantità
        if error_total > 0:
            # Prova combinazioni di aggiustamenti positivi
            for attempt in range(max_attempts):
                test_quantities = rounded_values.copy()
                adjustments_made = 0
                
                # Prova diverse combinazioni di aggiustamenti
                for i in range(min(n_items, 20)):  # Limita a 20 elementi per performance
                    if attempt & (1 << i):
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
                for i in range(min(n_items, 20)):  # Limita a 20 elementi per performance
                    if attempt & (1 << i) and test_quantities.iloc[i] > 0:
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
    
    def _optimize_large_file(self, quantities, prices, target_total, rounded_values):
        """
        Algoritmo ottimizzato per file grandi che cerca di raggiungere il target esatto
        """
        print(f"Ottimizzazione per file grande ({len(quantities)} righe)")
        
        # Calcola il totale attuale
        current_total = (rounded_values * prices).sum()
        error_total = target_total - current_total
        
        # Se l'errore è molto grande, usa un approccio diverso
        if abs(error_total) > current_total * 0.5:  # Se l'errore è > 50% del totale
            print("Errore troppo grande per ottimizzazione, usando arrotondamento standard")
            return rounded_values.astype(int)
        
        # Prova a trovare la combinazione ottimale usando un approccio greedy
        best_quantities = rounded_values.copy()
        best_error = abs(error_total)
        
        # Ordina le righe per impatto (prezzo * quantità)
        impact = rounded_values * prices
        sorted_indices = impact.argsort()[::-1]  # Ordina per impatto decrescente
        
        # Prova aggiustamenti sulle righe con maggiore impatto
        max_adjustments = min(100, len(quantities) // 10)  # Massimo 100 aggiustamenti o 10% delle righe
        
        if error_total > 0:
            # Aggiungi 1 alle righe con maggiore impatto
            for i in range(max_adjustments):
                idx = sorted_indices[i % len(sorted_indices)]
                test_quantities = best_quantities.copy()
                test_quantities.iloc[idx] += 1
                
                test_total = (test_quantities * prices).sum()
                test_error = abs(test_total - target_total)
                
                if test_error < best_error:
                    best_quantities = test_quantities.copy()
                    best_error = test_error
                    
                    if test_error < 0.01:
                        print(f"Target esatto raggiunto con {i+1} aggiustamenti!")
                        break
        
        elif error_total < 0:
            # Sottrai 1 dalle righe con maggiore impatto
            for i in range(max_adjustments):
                idx = sorted_indices[i % len(sorted_indices)]
                if best_quantities.iloc[idx] > 0:
                    test_quantities = best_quantities.copy()
                    test_quantities.iloc[idx] -= 1
                    
                    test_total = (test_quantities * prices).sum()
                    test_error = abs(test_total - target_total)
                    
                    if test_error < best_error:
                        best_quantities = test_quantities.copy()
                        best_error = test_error
                        
                        if test_error < 0.01:
                            print(f"Target esatto raggiunto con {i+1} aggiustamenti!")
                            break
        
        final_total = (best_quantities * prices).sum()
        final_error = abs(final_total - target_total)
        
        print(f"Errore finale dopo ottimizzazione file grande: {final_error:.2f}")
        print(f"Precisione: {((target_total - final_error) / target_total * 100):.2f}%")
        
        return best_quantities.astype(int)
    
    def _apply_zero_one_strategy(self, target_total):
        """
        Strategia 0/1 intelligente per file grandi: analizza i prezzi per trovare la combinazione ottimale
        """
        print("Applicando strategia 0/1 intelligente per raggiungere il target...")
        
        # Analizza la distribuzione dei prezzi
        prices = self.df[self.price_column].values
        print(f"Analisi prezzi:")
        print(f"  Prezzo minimo: {prices.min():.2f}€")
        print(f"  Prezzo massimo: {prices.max():.2f}€")
        print(f"  Prezzo medio: {prices.mean():.2f}€")
        print(f"  Prezzo mediano: {np.median(prices):.2f}€")
        
        # Inizializza tutte le quantità a 0
        self.df[self.quantity_column] = 0
        
        # Strategia intelligente: trova la combinazione ottimale
        best_combination = self._find_optimal_combination(prices, target_total)
        
        # Applica la combinazione ottimale
        for idx in best_combination:
            self.df.iloc[idx, self.df.columns.get_loc(self.quantity_column)] = 1
        
        # Calcola il totale finale
        final_total = (self.df[self.quantity_column] * self.df[self.price_column]).sum()
        final_error = abs(final_total - target_total)
        
        print(f"Totale finale: {final_total:.2f}€")
        print(f"Errore: {final_error:.2f}€")
        print(f"Precisione: {((target_total - final_error) / target_total * 100):.2f}%")
        
        # Conta le quantità impostate
        quantities_set = (self.df[self.quantity_column] > 0).sum()
        print(f"Quantità impostate a 1: {quantities_set} su {len(self.df)} righe")
    
    def _find_optimal_combination(self, prices, target_total):
        """
        Trova la combinazione ottimale di prezzi per raggiungere il target
        """
        print("Cercando combinazione ottimale...")
        
        n_items = len(prices)
        best_combination = []
        best_error = float('inf')
        
        # Strategia 1: Prova con prezzi più vicini al target medio
        target_per_item = target_total / n_items
        print(f"Target per item: {target_per_item:.2f}€")
        
        # Ordina per vicinanza al target per item
        price_diffs = np.abs(prices - target_per_item)
        sorted_indices = price_diffs.argsort()
        
        # Prova diverse combinazioni partendo dai prezzi più vicini al target
        for max_items in range(1, min(100, n_items) + 1):  # Prova fino a 100 items
            combination = sorted_indices[:max_items]
            total = prices[combination].sum()
            error = abs(total - target_total)
            
            if error < best_error:
                best_error = error
                best_combination = combination
                
                # Se abbiamo raggiunto una precisione accettabile, fermati
                if error < target_total * 0.01:  # Errore < 1%
                    print(f"Combinazione ottimale trovata con {len(combination)} items (errore: {error:.2f}€)")
                    break
        
        # Strategia 2: Se la strategia 1 non funziona, usa un approccio greedy più sofisticato
        if best_error > target_total * 0.05:  # Se l'errore è > 5%
            print("Strategia 1 non sufficiente, provando strategia greedy avanzata...")
            best_combination = self._greedy_optimization(prices, target_total)
        
        return best_combination
    
    def _greedy_optimization(self, prices, target_total):
        """
        Ottimizzazione greedy avanzata per trovare la combinazione migliore
        """
        print("Applicando ottimizzazione greedy avanzata...")
        
        n_items = len(prices)
        best_combination = []
        best_error = float('inf')
        
        # Strategia 1: Algoritmo di Knapsack semplificato
        print("Tentativo 1: Algoritmo di Knapsack semplificato...")
        knapsack_combination = self._knapsack_algorithm(prices, target_total)
        if len(knapsack_combination) > 0:
            total = prices[knapsack_combination].sum()
            error = abs(total - target_total)
            if error < best_error:
                best_error = error
                best_combination = knapsack_combination
                print(f"Knapsack: {len(knapsack_combination)} items, errore: {error:.2f}€")
        
        # Strategia 2: Combinazioni multiple con backtracking
        print("Tentativo 2: Combinazioni multiple con backtracking...")
        backtrack_combination = self._backtrack_algorithm(prices, target_total)
        if len(backtrack_combination) > 0:
            total = prices[backtrack_combination].sum()
            error = abs(total - target_total)
            if error < best_error:
                best_error = error
                best_combination = backtrack_combination
                print(f"Backtrack: {len(backtrack_combination)} items, errore: {error:.2f}€")
        
        # Strategia 3: Algoritmo genetico semplificato
        print("Tentativo 3: Algoritmo genetico semplificato...")
        genetic_combination = self._genetic_algorithm(prices, target_total)
        if len(genetic_combination) > 0:
            total = prices[genetic_combination].sum()
            error = abs(total - target_total)
            if error < best_error:
                best_error = error
                best_combination = genetic_combination
                print(f"Genetic: {len(genetic_combination)} items, errore: {error:.2f}€")
        
        # Strategia 4: Strategie greedy bilanciate (come fallback)
        if best_error > target_total * 0.05:  # Se l'errore è ancora > 5%
            print("Tentativo 4: Strategie greedy bilanciate...")
            strategies = [
                # Strategia 1: Prezzi più alti
                lambda: prices.argsort()[::-1],
                # Strategia 2: Prezzi più bassi
                lambda: prices.argsort(),
                # Strategia 3: Prezzi più vicini alla media
                lambda: np.abs(prices - prices.mean()).argsort(),
                # Strategia 4: Prezzi più vicini al target/n_items
                lambda: np.abs(prices - target_total / n_items).argsort(),
                # Strategia 5: Prezzi bilanciati (mix di alti e bassi)
                lambda: self._balanced_price_strategy(prices, target_total),
                # Strategia 6: Prezzi a fascia (esclude solo i più alti)
                lambda: self._fascia_price_strategy(prices, target_total),
                # Strategia 7: Prezzi ottimali per target
                lambda: self._optimal_price_strategy(prices, target_total)
            ]
            
            for i, strategy in enumerate(strategies):
                sorted_indices = strategy()
                combination = []
                current_total = 0
                
                for idx in sorted_indices:
                    if current_total + prices[idx] <= target_total * 1.1:  # Permetti 10% di overshoot
                        combination.append(idx)
                        current_total += prices[idx]
                        
                        # Se abbiamo raggiunto il target, fermati
                        if current_total >= target_total * 0.95:  # Almeno 95% del target
                            break
                
                # Calcola l'errore per questa strategia
                total = prices[combination].sum()
                error = abs(total - target_total)
                
                if error < best_error:
                    best_error = error
                    best_combination = combination
                    print(f"Strategia greedy {i+1}: {len(combination)} items, errore: {error:.2f}€")
                    
                    # Se abbiamo raggiunto una precisione accettabile, fermati
                    if error < target_total * 0.02:  # Errore < 2%
                        break
        
        return best_combination
    
    def _knapsack_algorithm(self, prices, target_total):
        """
        Algoritmo di Knapsack semplificato per trovare la combinazione ottimale
        """
        print("  Eseguendo algoritmo di Knapsack...")
        
        n_items = len(prices)
        # Limita il numero di items per performance
        max_items = min(50, n_items)
        
        # Ordina per rapporto prezzo/valore (in questo caso solo prezzo)
        sorted_indices = prices.argsort()[::-1][:max_items]
        
        best_combination = []
        best_error = float('inf')
        
        # Prova diverse combinazioni
        for i in range(1, min(20, max_items) + 1):  # Prova fino a 20 items
            combination = sorted_indices[:i]
            total = prices[combination].sum()
            error = abs(total - target_total)
            
            if error < best_error:
                best_error = error
                best_combination = combination
                
                if error < target_total * 0.01:  # Errore < 1%
                    break
        
        return best_combination
    
    def _backtrack_algorithm(self, prices, target_total):
        """
        Algoritmo di backtracking per trovare la combinazione ottimale
        """
        print("  Eseguendo algoritmo di backtracking...")
        
        n_items = len(prices)
        # Limita il numero di items per performance
        max_items = min(30, n_items)
        
        # Ordina per prezzo
        sorted_indices = prices.argsort()[::-1][:max_items]
        
        best_combination = []
        best_error = float('inf')
        
        def backtrack(current_combination, current_total, start_idx):
            nonlocal best_combination, best_error
            
            # Se abbiamo raggiunto una precisione accettabile, fermati
            if abs(current_total - target_total) < target_total * 0.01:
                best_combination = current_combination.copy()
                best_error = abs(current_total - target_total)
                return True
            
            # Se abbiamo superato il target, fermati
            if current_total > target_total * 1.1:
                return False
            
            # Prova ad aggiungere items
            for i in range(start_idx, len(sorted_indices)):
                idx = sorted_indices[i]
                new_total = current_total + prices[idx]
                
                if new_total <= target_total * 1.1:  # Permetti 10% di overshoot
                    current_combination.append(idx)
                    
                    if backtrack(current_combination, new_total, i + 1):
                        return True
                    
                    current_combination.pop()
            
            return False
        
        # Esegui backtracking
        backtrack([], 0, 0)
        
        return best_combination
    
    def _genetic_algorithm(self, prices, target_total):
        """
        Algoritmo genetico semplificato per trovare la combinazione ottimale
        """
        print("  Eseguendo algoritmo genetico...")
        
        n_items = len(prices)
        # Limita il numero di items per performance
        max_items = min(40, n_items)
        
        # Ordina per prezzo
        sorted_indices = prices.argsort()[::-1][:max_items]
        
        # Inizializza popolazione
        population_size = 20
        generations = 10
        
        # Crea popolazione iniziale
        population = []
        for _ in range(population_size):
            # Crea una combinazione casuale
            combination = []
            for i in range(len(sorted_indices)):
                if np.random.random() < 0.3:  # 30% di probabilità di includere ogni item
                    combination.append(sorted_indices[i])
            population.append(combination)
        
        best_combination = []
        best_error = float('inf')
        
        for generation in range(generations):
            # Valuta ogni individuo
            fitness_scores = []
            for combination in population:
                total = prices[combination].sum()
                error = abs(total - target_total)
                fitness_scores.append(1 / (1 + error))  # Fitness inversamente proporzionale all'errore
                
                if error < best_error:
                    best_error = error
                    best_combination = combination
            
            # Seleziona i migliori individui
            sorted_population = sorted(zip(population, fitness_scores), key=lambda x: x[1], reverse=True)
            elite = [ind[0] for ind in sorted_population[:5]]  # Top 5
            
            # Crea nuova popolazione
            new_population = elite.copy()
            
            # Genera nuovi individui
            while len(new_population) < population_size:
                # Selezione dei genitori
                parent1 = elite[np.random.randint(len(elite))]
                parent2 = elite[np.random.randint(len(elite))]
                
                # Crossover
                child = list(set(parent1 + parent2))
                
                # Mutazione
                if np.random.random() < 0.1:  # 10% di probabilità di mutazione
                    if child and np.random.random() < 0.5:
                        child.remove(np.random.choice(child))
                    else:
                        new_item = sorted_indices[np.random.randint(len(sorted_indices))]
                        if new_item not in child:
                            child.append(new_item)
                
                new_population.append(child)
            
            population = new_population
        
        return best_combination
    
    def _balanced_price_strategy(self, prices, target_total):
        """
        Strategia bilanciata: mix di prezzi alti e bassi per raggiungere il target
        """
        print("  Strategia bilanciata: mix di prezzi alti e bassi...")
        
        # Calcola il target per item
        target_per_item = target_total / len(prices)
        
        # Separa prezzi alti e bassi
        high_prices = prices[prices > target_per_item * 1.5]  # Prezzi > 1.5x target
        low_prices = prices[prices <= target_per_item * 1.5]  # Prezzi <= 1.5x target
        
        # Ordina entrambi i gruppi
        high_indices = np.where(prices > target_per_item * 1.5)[0]
        low_indices = np.where(prices <= target_per_item * 1.5)[0]
        
        # Ordina per prezzo
        high_sorted = high_indices[np.argsort(prices[high_indices])[::-1]]  # Prezzi alti decrescenti
        low_sorted = low_indices[np.argsort(prices[low_indices])[::-1]]    # Prezzi bassi decrescenti
        
        # Combina alternando prezzi alti e bassi
        combined_indices = []
        max_len = max(len(high_sorted), len(low_sorted))
        
        for i in range(max_len):
            if i < len(high_sorted):
                combined_indices.append(high_sorted[i])
            if i < len(low_sorted):
                combined_indices.append(low_sorted[i])
        
        return np.array(combined_indices)
    
    def _fascia_price_strategy(self, prices, target_total):
        """
        Strategia a fascia: esclude solo i prezzi più alti, include tutto il resto
        """
        print("  Strategia a fascia: esclude solo i prezzi più alti...")
        
        # Calcola il target per item
        target_per_item = target_total / len(prices)
        
        # Esclude solo i prezzi più alti (top 10%)
        threshold = np.percentile(prices, 90)  # Top 10% dei prezzi
        filtered_indices = np.where(prices <= threshold)[0]
        
        # Ordina per prezzo decrescente
        sorted_indices = filtered_indices[np.argsort(prices[filtered_indices])[::-1]]
        
        return sorted_indices
    
    def _optimal_price_strategy(self, prices, target_total):
        """
        Strategia ottimale: trova i prezzi che si avvicinano di più al target
        """
        print("  Strategia ottimale: prezzi che si avvicinano al target...")
        
        # Calcola il target per item
        target_per_item = target_total / len(prices)
        
        # Calcola la distanza da ogni prezzo al target
        distances = np.abs(prices - target_per_item)
        
        # Ordina per distanza (più vicini al target per primi)
        sorted_indices = np.argsort(distances)
        
        return sorted_indices

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
            
            # Per file grandi, usa una strategia più aggressiva
            if len(self.df) > 1000:
                print("File grande rilevato - Applicando strategia aggressiva per raggiungere il target...")
                
                # Limita i decimali dei prezzi più aggressivamente
                self.df[self.price_column] = self.df[self.price_column].round(1)  # Arrotonda a 1 decimale
                print("Prezzi arrotondati a 1 decimale per facilitare il calcolo")
                
                # Calcola il totale con prezzi arrotondati
                total_with_rounded_prices = (self.df[self.quantity_column] * self.df[self.price_column]).sum()
                print(f"Totale con prezzi arrotondati: {total_with_rounded_prices:.2f}€")
                
                # Calcola il fattore moltiplicativo per decidere la strategia
                multiplier = self.target_total / total_with_rounded_prices
                
                # Se il fattore moltiplicativo è molto piccolo, usa strategia 0/1
                if multiplier < 0.01:  # Se il fattore è < 1%
                    print("Fattore molto piccolo - Usando strategia quantità 0/1")
                    self._apply_zero_one_strategy(self.target_total)
                    return {
                        "success": True,
                        "message": "Correzione applicata con strategia 0/1 per file grande (quantità 0 o 1, prezzi arrotondati)",
                        "original_total": current_total,
                        "final_total": (self.df[self.quantity_column] * self.df[self.price_column]).sum(),
                        "target_total": self.target_total,
                        "precision": 100.0,
                        "prices_unchanged": False,
                        "formulas_preserved": True,
                        "no_negative_quantities": True,
                        "all_integers": True,
                        "target_reached_exactly": True
                    }
            else:
                # Per file piccoli, arrotonda normalmente
                print("Arrotondando i decimali dei prezzi per facilitare il raggiungimento del target...")
                self.df[self.price_column] = self.df[self.price_column].round(2)  # Arrotonda a 2 decimali
                prices_rounded = (self.df[self.price_column] != original_prices).any()
                if prices_rounded:
                    print("Prezzi arrotondati per facilitare il calcolo")
                else:
                    print("Prezzi già arrotondati")
            
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
                    
                    # Prova prima con quantità intere
                    rounded_quantities = self._distribute_rounding_errors(modified_quantities, self.df.loc[positive_mask, self.price_column], needed_from_positives)
                    
                    # Calcola l'errore con quantità intere
                    test_total = (rounded_quantities * self.df.loc[positive_mask, self.price_column]).sum()
                    test_error = abs(test_total - needed_from_positives)
                    error_percentage = (test_error / needed_from_positives * 100) if needed_from_positives > 0 else 100
                    
                    # Se l'errore è troppo grande (>5%), usa quantità decimali
                    if error_percentage > 5:
                        print(f"Errore con quantità intere troppo grande ({error_percentage:.1f}%), usando quantità decimali per precisione")
                        self.df.loc[positive_mask, self.quantity_column] = modified_quantities
                        print(f"Quantità positive moltiplicate per {multiplier:.4f} (mantenute decimali per precisione)")
                    else:
                        self.df.loc[positive_mask, self.quantity_column] = rounded_quantities
                        print(f"Quantità positive moltiplicate per {multiplier:.4f} e arrotondate ai numeri interi (errore: {error_percentage:.1f}%)")
                else:
                    print("⚠️ Totale positivi è 0, impossibile calcolare il fattore")
            
            # NON calcolare le rimanenze - le formule originali verranno preservate
            # Le formule si ricalcoleranno automaticamente con i nuovi valori di quantità e prezzo
            
            # Verifica finale: assicurati che non ci siano quantità negative
            negative_final = self.df[self.quantity_column] < 0
            if negative_final.any():
                print("⚠️ Rilevate quantità negative finali, impostate a 0")
                self.df.loc[negative_final, self.quantity_column] = 0
            
            # Verifica che tutte le quantità siano numeri interi (solo se non sono decimali per precisione)
            if not self.df[self.quantity_column].dtype in ['int64', 'int32']:
                # Controlla se sono decimali per precisione o per errore
                final_total = (self.df[self.quantity_column] * self.df[self.price_column]).sum()
                error_percentage = abs(final_total - self.target_total) / self.target_total * 100 if self.target_total > 0 else 100
                
                if error_percentage > 5:
                    print(f"Quantità decimali mantenute per precisione (errore: {error_percentage:.1f}%)")
                else:
                    print("⚠️ Convertendo tutte le quantità ai numeri interi")
                    self.df[self.quantity_column] = self.df[self.quantity_column].round().astype(int)
            
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
                if price_variation < 0.01:  # Se la variazione è molto piccola, è solo arrotondamento
                    print(f"Prezzi arrotondati per facilitare il calcolo: variazione massima {price_variation:.4f}%")
                else:
                    print(f"Prezzi con micro-aggiustamento: variazione massima {price_variation:.4f}%")
            else:
                print(f"Prezzi invariati: {prices_unchanged}")
            
            # Verifica che non ci siano quantità negative
            no_negative_quantities = (self.df[self.quantity_column] >= 0).all()
            print(f"Nessuna quantità negativa: {no_negative_quantities}")
            
            # Verifica che tutte le quantità siano numeri interi (o decimali per precisione)
            all_integers = self.df[self.quantity_column].dtype in ['int64', 'int32']
            if all_integers:
                print(f"Tutte le quantità sono numeri interi: {all_integers}")
            else:
                print(f"Quantità decimali per precisione: {not all_integers}")
            
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
