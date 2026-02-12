import numpy as np
from collections import Counter
import json


class DecisionTreeService:
    
    @staticmethod
    def calculate_gini(y):
        counter = Counter(y)
        impurity = 1.0
        total = len(y)
        for count in counter.values():
            prob = count / total
            impurity -= prob ** 2
        return impurity
    
    @staticmethod
    def calculate_entropy(y):
        counter = Counter(y)
        entropy = 0.0
        total = len(y)
        for count in counter.values():
            prob = count / total
            if prob > 0:
                entropy -= prob * np.log2(prob)
        return entropy
    
    @staticmethod
    def calculate_information_gain(parent, left, right, algorithm='gini'):
        weight_left = len(left) / len(parent)
        weight_right = len(right) / len(parent)
        
        if algorithm == 'gini':
            parent_impurity = DecisionTreeService.calculate_gini(parent)
            gain = parent_impurity - (
                weight_left * DecisionTreeService.calculate_gini(left) +
                weight_right * DecisionTreeService.calculate_gini(right)
            )
        else:
            parent_impurity = DecisionTreeService.calculate_entropy(parent)
            gain = parent_impurity - (
                weight_left * DecisionTreeService.calculate_entropy(left) +
                weight_right * DecisionTreeService.calculate_entropy(right)
            )
        
        return gain
    
    @staticmethod
    def find_best_split(X, y, feature_idx, algorithm='gini'):
        best_gain = -1
        best_threshold = None
        
        values = sorted(set(X[:, feature_idx]))
        
        for i in range(len(values) - 1):
            threshold = (values[i] + values[i + 1]) / 2
            
            left_mask = X[:, feature_idx] <= threshold
            right_mask = ~left_mask
            
            if np.sum(left_mask) == 0 or np.sum(right_mask) == 0:
                continue
            
            gain = DecisionTreeService.calculate_information_gain(
                y, y[left_mask], y[right_mask], algorithm
            )
            
            if gain > best_gain:
                best_gain = gain
                best_threshold = threshold
        
        return best_threshold, best_gain
    
    @staticmethod
    def build_tree(X, y, features, depth=0, max_depth=5, min_samples_split=2, 
                   min_samples_leaf=1, algorithm='gini', node_id='0'):
        
        n_samples = len(y)
        
        if depth >= max_depth or n_samples < min_samples_split or len(set(y)) == 1:
            counter = Counter(y)
            return {
                'node_id': node_id,
                'is_leaf': True,
                'class_label': counter.most_common(1)[0][0],
                'samples': n_samples,
                'value': dict(counter),
                'gini': DecisionTreeService.calculate_gini(y) if algorithm == 'gini' else None,
                'entropy': DecisionTreeService.calculate_entropy(y) if algorithm == 'entropy' else None
            }
        
        best_feature = None
        best_threshold = None
        best_gain = -1
        
        for feature_idx in range(X.shape[1]):
            threshold, gain = DecisionTreeService.find_best_split(X, y, feature_idx, algorithm)
            
            if gain > best_gain:
                best_gain = gain
                best_feature = feature_idx
                best_threshold = threshold
        
        if best_feature is None:
            counter = Counter(y)
            return {
                'node_id': node_id,
                'is_leaf': True,
                'class_label': counter.most_common(1)[0][0],
                'samples': n_samples,
                'value': dict(counter),
                'gini': DecisionTreeService.calculate_gini(y) if algorithm == 'gini' else None,
                'entropy': DecisionTreeService.calculate_entropy(y) if algorithm == 'entropy' else None
            }
        
        left_mask = X[:, best_feature] <= best_threshold
        right_mask = ~left_mask
        
        if np.sum(left_mask) < min_samples_leaf or np.sum(right_mask) < min_samples_leaf:
            counter = Counter(y)
            return {
                'node_id': node_id,
                'is_leaf': True,
                'class_label': counter.most_common(1)[0][0],
                'samples': n_samples,
                'value': dict(counter),
                'gini': DecisionTreeService.calculate_gini(y) if algorithm == 'gini' else None,
                'entropy': DecisionTreeService.calculate_entropy(y) if algorithm == 'entropy' else None
            }
        
        counter = Counter(y)
        node = {
            'node_id': node_id,
            'is_leaf': False,
            'feature': features[best_feature],
            'threshold': float(best_threshold),
            'operator': '<=',
            'samples': n_samples,
            'value': dict(counter),
            'gini': DecisionTreeService.calculate_gini(y) if algorithm == 'gini' else None,
            'entropy': DecisionTreeService.calculate_entropy(y) if algorithm == 'entropy' else None
        }
        
        node['left'] = DecisionTreeService.build_tree(
            X[left_mask], y[left_mask], features, depth + 1, max_depth,
            min_samples_split, min_samples_leaf, algorithm, f"{node_id}-L"
        )
        node['right'] = DecisionTreeService.build_tree(
            X[right_mask], y[right_mask], features, depth + 1, max_depth,
            min_samples_split, min_samples_leaf, algorithm, f"{node_id}-R"
        )
        
        return node
    
    @staticmethod
    def predict(tree_dict, sample):
        if tree_dict['is_leaf']:
            return tree_dict['class_label']
        
        feature_value = sample.get(tree_dict['feature'])
        
        if feature_value is None:
            return tree_dict.get('class_label', 'UNKNOWN')
        
        if feature_value <= tree_dict['threshold']:
            return DecisionTreeService.predict(tree_dict['left'], sample)
        else:
            return DecisionTreeService.predict(tree_dict['right'], sample)
    
    @staticmethod
    def calculate_accuracy(tree_dict, X_test, y_test, features):
        predictions = []
        for i in range(len(X_test)):
            sample = {features[j]: X_test[i][j] for j in range(len(features))}
            predictions.append(DecisionTreeService.predict(tree_dict, sample))
        
        correct = sum(1 for pred, actual in zip(predictions, y_test) if pred == actual)
        return correct / len(y_test) if len(y_test) > 0 else 0.0
    
    @staticmethod
    def prune_tree(tree_dict, validation_X, validation_y, features):
        if tree_dict['is_leaf']:
            return tree_dict
        
        original_accuracy = DecisionTreeService.calculate_accuracy(
            tree_dict, validation_X, validation_y, features
        )
        
        pruned_tree = {
            'node_id': tree_dict['node_id'],
            'is_leaf': True,
            'class_label': max(tree_dict['value'], key=tree_dict['value'].get),
            'samples': tree_dict['samples'],
            'value': tree_dict['value'],
            'gini': tree_dict.get('gini'),
            'entropy': tree_dict.get('entropy')
        }
        
        pruned_accuracy = DecisionTreeService.calculate_accuracy(
            pruned_tree, validation_X, validation_y, features
        )
        
        if pruned_accuracy >= original_accuracy:
            return pruned_tree
        
        tree_dict['left'] = DecisionTreeService.prune_tree(
            tree_dict['left'], validation_X, validation_y, features
        )
        tree_dict['right'] = DecisionTreeService.prune_tree(
            tree_dict['right'], validation_X, validation_y, features
        )
        
        return tree_dict
