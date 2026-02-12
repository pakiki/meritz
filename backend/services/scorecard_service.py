import math
import numpy as np


class ScorecardService:
    
    @staticmethod
    def calculate_woe(good_count, bad_count, total_good, total_bad):
        good_rate = (good_count / total_good) if total_good > 0 else 0.0001
        bad_rate = (bad_count / total_bad) if total_bad > 0 else 0.0001
        
        if good_rate == 0:
            good_rate = 0.0001
        if bad_rate == 0:
            bad_rate = 0.0001
        
        woe = math.log(good_rate / bad_rate)
        return woe
    
    @staticmethod
    def calculate_iv(good_count, bad_count, total_good, total_bad):
        good_rate = (good_count / total_good) if total_good > 0 else 0.0001
        bad_rate = (bad_count / total_bad) if total_bad > 0 else 0.0001
        
        if good_rate == 0:
            good_rate = 0.0001
        if bad_rate == 0:
            bad_rate = 0.0001
        
        woe = math.log(good_rate / bad_rate)
        iv = (good_rate - bad_rate) * woe
        return iv
    
    @staticmethod
    def calculate_scorecard_points(woe, weight, base_score, pdo, base_odds):
        factor = pdo / math.log(2)
        offset = base_score - factor * math.log(base_odds)
        points = (offset + factor * woe) * weight
        return points
    
    @staticmethod
    def calculate_score(scorecard, input_data):
        total_score = scorecard.base_score
        breakdown = []
        
        for characteristic in scorecard.characteristics:
            char_name = characteristic.name
            char_value = input_data.get(char_name)
            
            if char_value is None:
                continue
            
            matched_attribute = None
            for attribute in characteristic.attributes:
                if ScorecardService.match_attribute(attribute, char_value):
                    matched_attribute = attribute
                    break
            
            if matched_attribute and matched_attribute.points:
                total_score += matched_attribute.points
                breakdown.append({
                    'characteristic': char_name,
                    'value': char_value,
                    'attribute': matched_attribute.attribute,
                    'points': matched_attribute.points,
                    'woe': matched_attribute.woe
                })
        
        return {
            'total_score': round(total_score, 2),
            'breakdown': breakdown
        }
    
    @staticmethod
    def match_attribute(attribute, value):
        if attribute.category:
            return str(value) == str(attribute.category)
        
        if attribute.min_value is not None and attribute.max_value is not None:
            try:
                numeric_value = float(value)
                return attribute.min_value <= numeric_value < attribute.max_value
            except (ValueError, TypeError):
                return False
        
        return False
    
    @staticmethod
    def calculate_binning(data, column, n_bins=10, method='equal_width'):
        values = [row[column] for row in data if row.get(column) is not None]
        
        if not values:
            return []
        
        if method == 'equal_width':
            min_val = min(values)
            max_val = max(values)
            bin_width = (max_val - min_val) / n_bins
            
            bins = []
            for i in range(n_bins):
                bins.append({
                    'min_value': min_val + i * bin_width,
                    'max_value': min_val + (i + 1) * bin_width,
                    'attribute': f"Bin {i+1}"
                })
            return bins
        
        elif method == 'equal_frequency':
            sorted_values = sorted(values)
            bin_size = len(sorted_values) // n_bins
            
            bins = []
            for i in range(n_bins):
                start_idx = i * bin_size
                end_idx = (i + 1) * bin_size if i < n_bins - 1 else len(sorted_values)
                
                bins.append({
                    'min_value': sorted_values[start_idx],
                    'max_value': sorted_values[end_idx - 1],
                    'attribute': f"Bin {i+1}"
                })
            return bins
        
        return []
    
    @staticmethod
    def auto_binning_woe(data, feature_column, target_column, max_bins=10):
        bins = ScorecardService.calculate_binning(data, feature_column, max_bins, 'equal_frequency')
        
        total_good = sum(1 for row in data if row.get(target_column) == 1)
        total_bad = sum(1 for row in data if row.get(target_column) == 0)
        
        for bin_info in bins:
            good_count = 0
            bad_count = 0
            
            for row in data:
                value = row.get(feature_column)
                target = row.get(target_column)
                
                if value is None or target is None:
                    continue
                
                if bin_info['min_value'] <= value < bin_info['max_value']:
                    if target == 1:
                        good_count += 1
                    else:
                        bad_count += 1
            
            bin_info['good_count'] = good_count
            bin_info['bad_count'] = bad_count
            bin_info['woe'] = ScorecardService.calculate_woe(good_count, bad_count, total_good, total_bad)
            bin_info['iv'] = ScorecardService.calculate_iv(good_count, bad_count, total_good, total_bad)
        
        return bins
    
    @staticmethod
    def calculate_odds(score, base_score, pdo, base_odds):
        factor = pdo / math.log(2)
        odds = base_odds * math.exp((score - base_score) / factor)
        return odds
    
    @staticmethod
    def calculate_probability(score, base_score, pdo, base_odds):
        odds = ScorecardService.calculate_odds(score, base_score, pdo, base_odds)
        probability = odds / (1 + odds)
        return probability
