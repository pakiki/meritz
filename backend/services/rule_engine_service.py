from backend.models.decision_tree import DecisionTree, DecisionTreeNode
from backend.models.scorecard import Scorecard
from backend.models.decision_table import DecisionTable
from backend.models.rule_set import RuleSet
from backend.services.decision_tree_service import DecisionTreeService
from backend.services.scorecard_service import ScorecardService
from backend.services.decision_table_service import DecisionTableService
import json


class RuleEngineService:
    
    @staticmethod
    def execute_rule(rule_type, rule_id, input_data, db):
        if rule_type == 'DECISION_TREE':
            return RuleEngineService.execute_decision_tree(rule_id, input_data, db)
        elif rule_type == 'SCORECARD':
            return RuleEngineService.execute_scorecard(rule_id, input_data, db)
        elif rule_type == 'DECISION_TABLE':
            return RuleEngineService.execute_decision_table(rule_id, input_data, db)
        elif rule_type == 'RULE_SET':
            return RuleEngineService.execute_rule_set(rule_id, input_data, db)
        else:
            return {
                'success': False,
                'error': f'Unknown rule type: {rule_type}'
            }
    
    @staticmethod
    def execute_decision_tree(tree_id, input_data, db):
        tree = db.session.query(DecisionTree).get(tree_id)
        if not tree:
            return {'success': False, 'error': 'Decision tree not found'}
        
        tree_dict = RuleEngineService.build_tree_dict_from_nodes(tree.nodes)
        
        prediction = DecisionTreeService.predict(tree_dict, input_data)
        
        return {
            'success': True,
            'rule_type': 'DECISION_TREE',
            'tree_id': tree_id,
            'tree_name': tree.name,
            'prediction': prediction,
            'input': input_data
        }
    
    @staticmethod
    def execute_scorecard(scorecard_id, input_data, db):
        scorecard = db.session.query(Scorecard).get(scorecard_id)
        if not scorecard:
            return {'success': False, 'error': 'Scorecard not found'}
        
        result = ScorecardService.calculate_score(scorecard, input_data)
        
        probability = ScorecardService.calculate_probability(
            result['total_score'],
            scorecard.base_score,
            scorecard.pdo,
            scorecard.base_odds
        )
        
        return {
            'success': True,
            'rule_type': 'SCORECARD',
            'scorecard_id': scorecard_id,
            'scorecard_name': scorecard.name,
            'score': result['total_score'],
            'breakdown': result['breakdown'],
            'probability': round(probability, 4),
            'input': input_data
        }
    
    @staticmethod
    def execute_decision_table(table_id, input_data, db):
        table = db.session.query(DecisionTable).get(table_id)
        if not table:
            return {'success': False, 'error': 'Decision table not found'}
        
        result = DecisionTableService.execute_table(table, input_data)
        
        return {
            'success': True,
            'rule_type': 'DECISION_TABLE',
            'table_id': table_id,
            'table_name': table.name,
            'matched': result['matched'],
            'output': result['output'],
            'matched_rules': result.get('rules', []),
            'input': input_data
        }
    
    @staticmethod
    def execute_rule_set(rule_set_id, input_data, db):
        rule_set = db.session.query(RuleSet).get(rule_set_id)
        if not rule_set:
            return {'success': False, 'error': 'Rule set not found'}
        
        results = []
        context = input_data.copy()
        
        sorted_rules = sorted(rule_set.rules, key=lambda r: r.priority, reverse=True)
        
        for rule in sorted_rules:
            if not rule.enabled:
                continue
            
            condition_result = RuleEngineService.evaluate_expression(rule.condition, context)
            
            if condition_result:
                action_result = RuleEngineService.execute_action(rule.action, context)
                results.append({
                    'rule_id': rule.id,
                    'rule_name': rule.name,
                    'condition': rule.condition,
                    'action': rule.action,
                    'result': action_result
                })
                
                if isinstance(action_result, dict):
                    context.update(action_result)
        
        return {
            'success': True,
            'rule_type': 'RULE_SET',
            'rule_set_id': rule_set_id,
            'rule_set_name': rule_set.name,
            'fired_rules': results,
            'final_context': context,
            'input': input_data
        }
    
    @staticmethod
    def evaluate_expression(expression, context):
        try:
            safe_context = {k: v for k, v in context.items()}
            result = eval(expression, {"__builtins__": {}}, safe_context)
            return result
        except Exception as e:
            return False
    
    @staticmethod
    def execute_action(action, context):
        try:
            safe_context = {k: v for k, v in context.items()}
            exec(action, {"__builtins__": {}}, safe_context)
            return {k: v for k, v in safe_context.items() if k not in context or context[k] != v}
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def build_tree_dict_from_nodes(nodes):
        if not nodes:
            return None
        
        root_node = next((n for n in nodes if n.parent_id is None or n.node_id == '0'), nodes[0])
        
        def build_node(node):
            node_dict = {
                'node_id': node.node_id,
                'is_leaf': node.is_leaf,
                'samples': node.samples,
                'gini': node.gini,
                'entropy': node.entropy,
                'value': json.loads(node.value) if node.value else {}
            }
            
            if node.is_leaf:
                node_dict['class_label'] = node.class_label
            else:
                node_dict['feature'] = node.feature
                node_dict['threshold'] = node.threshold
                node_dict['operator'] = node.operator
                
                left_child = next((n for n in nodes if n.node_id == f"{node.node_id}-L"), None)
                right_child = next((n for n in nodes if n.node_id == f"{node.node_id}-R"), None)
                
                if left_child:
                    node_dict['left'] = build_node(left_child)
                if right_child:
                    node_dict['right'] = build_node(right_child)
            
            return node_dict
        
        return build_node(root_node)
