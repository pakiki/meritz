import re


class DecisionTableService:
    
    @staticmethod
    def evaluate_condition(condition_value, operator, input_value):
        if operator == '==':
            return str(input_value) == str(condition_value)
        elif operator == '!=':
            return str(input_value) != str(condition_value)
        elif operator == '>':
            try:
                return float(input_value) > float(condition_value)
            except (ValueError, TypeError):
                return False
        elif operator == '>=':
            try:
                return float(input_value) >= float(condition_value)
            except (ValueError, TypeError):
                return False
        elif operator == '<':
            try:
                return float(input_value) < float(condition_value)
            except (ValueError, TypeError):
                return False
        elif operator == '<=':
            try:
                return float(input_value) <= float(condition_value)
            except (ValueError, TypeError):
                return False
        elif operator == 'IN':
            if isinstance(condition_value, list):
                return input_value in condition_value
            return str(input_value) in str(condition_value).split(',')
        elif operator == 'NOT IN':
            if isinstance(condition_value, list):
                return input_value not in condition_value
            return str(input_value) not in str(condition_value).split(',')
        elif operator == 'CONTAINS':
            return str(condition_value) in str(input_value)
        elif operator == 'STARTS_WITH':
            return str(input_value).startswith(str(condition_value))
        elif operator == 'ENDS_WITH':
            return str(input_value).endswith(str(condition_value))
        elif operator == 'REGEX':
            return bool(re.match(str(condition_value), str(input_value)))
        elif operator == 'BETWEEN':
            try:
                if isinstance(condition_value, list) and len(condition_value) == 2:
                    return float(condition_value[0]) <= float(input_value) <= float(condition_value[1])
            except (ValueError, TypeError):
                return False
        elif operator == '-' or operator == 'ANY':
            return True
        
        return False
    
    @staticmethod
    def match_rule(rule, input_data, condition_columns):
        for column in condition_columns:
            column_name = column['name']
            
            if column_name not in rule.conditions:
                continue
            
            condition_spec = rule.conditions[column_name]
            
            if isinstance(condition_spec, dict):
                operator = condition_spec.get('operator', '==')
                value = condition_spec.get('value')
            else:
                operator = '=='
                value = condition_spec
            
            input_value = input_data.get(column_name)
            
            if operator == '-' or operator == 'ANY':
                continue
            
            if input_value is None:
                return False
            
            if not DecisionTableService.evaluate_condition(value, operator, input_value):
                return False
        
        return True
    
    @staticmethod
    def execute_table(decision_table, input_data):
        conditions = decision_table.conditions if isinstance(decision_table.conditions, list) else []
        actions = decision_table.actions if isinstance(decision_table.actions, list) else []
        hit_policy = decision_table.hit_policy or 'FIRST'
        
        matched_rules = []
        
        sorted_rules = sorted(decision_table.rules, key=lambda r: r.priority, reverse=True)
        
        for rule in sorted_rules:
            if not rule.enabled:
                continue
            
            if DecisionTableService.match_rule(rule, input_data, conditions):
                matched_rules.append(rule)
                
                if hit_policy == 'FIRST':
                    break
        
        if not matched_rules:
            return {
                'matched': False,
                'rules': [],
                'output': {},
                'message': 'No matching rules found'
            }
        
        output = {}
        
        if hit_policy == 'FIRST':
            for action_col in actions:
                action_name = action_col['name']
                if action_name in matched_rules[0].actions:
                    output[action_name] = matched_rules[0].actions[action_name]
        
        elif hit_policy == 'COLLECT':
            for action_col in actions:
                action_name = action_col['name']
                output[action_name] = [
                    rule.actions.get(action_name) 
                    for rule in matched_rules 
                    if action_name in rule.actions
                ]
        
        elif hit_policy == 'PRIORITY':
            highest_priority_rule = matched_rules[0]
            for action_col in actions:
                action_name = action_col['name']
                if action_name in highest_priority_rule.actions:
                    output[action_name] = highest_priority_rule.actions[action_name]
        
        elif hit_policy == 'ANY':
            for action_col in actions:
                action_name = action_col['name']
                for rule in matched_rules:
                    if action_name in rule.actions:
                        output[action_name] = rule.actions[action_name]
                        break
        
        return {
            'matched': True,
            'rules': [{'rule_number': rule.rule_number, 'id': rule.id} for rule in matched_rules],
            'output': output,
            'hit_policy': hit_policy
        }
    
    @staticmethod
    def validate_table(decision_table):
        errors = []
        warnings = []
        
        if not decision_table.rules:
            errors.append('Decision table must have at least one rule')
        
        conditions = decision_table.conditions if isinstance(decision_table.conditions, list) else []
        actions = decision_table.actions if isinstance(decision_table.actions, list) else []
        
        if not conditions:
            errors.append('Decision table must have at least one condition column')
        
        if not actions:
            errors.append('Decision table must have at least one action column')
        
        rule_numbers = [rule.rule_number for rule in decision_table.rules]
        if len(rule_numbers) != len(set(rule_numbers)):
            errors.append('Duplicate rule numbers found')
        
        for rule in decision_table.rules:
            if not rule.conditions:
                warnings.append(f'Rule {rule.rule_number} has no conditions')
            if not rule.actions:
                warnings.append(f'Rule {rule.rule_number} has no actions')
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
