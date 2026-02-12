import random
import numpy as np
from datetime import datetime, timedelta
import json


class SimulationService:
    
    @staticmethod
    def simulate_process(workflow, simulation_config):
        num_instances = simulation_config.get('num_instances', 100)
        input_generator = simulation_config.get('input_generator', {})
        
        results = []
        node_statistics = {}
        edge_statistics = {}
        
        for i in range(num_instances):
            input_data = SimulationService.generate_input_data(input_generator)
            
            instance_result = SimulationService.simulate_instance(workflow, input_data, simulation_config)
            results.append(instance_result)
            
            for node_stat in instance_result.get('node_stats', []):
                node_id = node_stat['node_id']
                if node_id not in node_statistics:
                    node_statistics[node_id] = {
                        'executions': 0,
                        'total_duration_ms': 0,
                        'min_duration_ms': float('inf'),
                        'max_duration_ms': 0
                    }
                
                stats = node_statistics[node_id]
                stats['executions'] += 1
                stats['total_duration_ms'] += node_stat['duration_ms']
                stats['min_duration_ms'] = min(stats['min_duration_ms'], node_stat['duration_ms'])
                stats['max_duration_ms'] = max(stats['max_duration_ms'], node_stat['duration_ms'])
        
        for node_id, stats in node_statistics.items():
            if stats['executions'] > 0:
                stats['avg_duration_ms'] = stats['total_duration_ms'] / stats['executions']
        
        successful = sum(1 for r in results if r.get('status') == 'COMPLETED')
        failed = sum(1 for r in results if r.get('status') == 'FAILED')
        
        durations = [r['duration_ms'] for r in results if 'duration_ms' in r]
        
        return {
            'total_instances': num_instances,
            'successful': successful,
            'failed': failed,
            'success_rate': successful / num_instances if num_instances > 0 else 0,
            'avg_duration_ms': np.mean(durations) if durations else 0,
            'min_duration_ms': min(durations) if durations else 0,
            'max_duration_ms': max(durations) if durations else 0,
            'p50_duration_ms': np.percentile(durations, 50) if durations else 0,
            'p95_duration_ms': np.percentile(durations, 95) if durations else 0,
            'p99_duration_ms': np.percentile(durations, 99) if durations else 0,
            'node_statistics': node_statistics,
            'edge_statistics': edge_statistics,
            'instances': results[:10]
        }
    
    @staticmethod
    def simulate_instance(workflow, input_data, simulation_config):
        context = input_data.copy()
        node_stats = []
        visited_nodes = set()
        
        start_time = datetime.utcnow()
        
        start_node = next((n for n in workflow.nodes if n.type == 'start'), None)
        if not start_node:
            return {'status': 'FAILED', 'error': 'No start node'}
        
        current_node = start_node
        
        while current_node and len(visited_nodes) < 100:
            if current_node.node_id in visited_nodes:
                break
            
            visited_nodes.add(current_node.node_id)
            
            node_duration = SimulationService.get_node_duration(
                current_node,
                simulation_config.get('node_durations', {})
            )
            
            node_stats.append({
                'node_id': current_node.node_id,
                'node_type': current_node.type,
                'duration_ms': node_duration
            })
            
            if current_node.type == 'businessRule':
                config = json.loads(current_node.config) if current_node.config else {}
                rule_type = config.get('rule_type')
                
                if rule_type == 'SCORECARD':
                    context['credit_score'] = random.randint(300, 850)
                elif rule_type == 'DECISION_TABLE':
                    context['decision'] = random.choice(['APPROVED', 'REJECTED', 'MANUAL_REVIEW'])
            
            elif current_node.type == 'gateway':
                config = json.loads(current_node.config) if current_node.config else {}
                condition = config.get('condition')
                
                try:
                    result = eval(condition, {"__builtins__": {}}, context)
                    context['gateway_result'] = result
                except:
                    context['gateway_result'] = random.choice([True, False])
            
            if current_node.type == 'end':
                break
            
            outgoing_edges = [e for e in workflow.edges if e.source == current_node.node_id]
            
            if not outgoing_edges:
                break
            
            if len(outgoing_edges) == 1:
                next_edge = outgoing_edges[0]
            else:
                next_edge = random.choice(outgoing_edges)
            
            current_node = next((n for n in workflow.nodes if n.node_id == next_edge.target), None)
        
        end_time = datetime.utcnow()
        total_duration = sum(ns['duration_ms'] for ns in node_stats)
        
        return {
            'status': 'COMPLETED',
            'duration_ms': total_duration,
            'node_stats': node_stats,
            'output': context
        }
    
    @staticmethod
    def generate_input_data(input_generator):
        input_data = {}
        
        for field_name, field_config in input_generator.items():
            field_type = field_config.get('type', 'number')
            
            if field_type == 'number':
                min_val = field_config.get('min', 0)
                max_val = field_config.get('max', 100)
                input_data[field_name] = random.uniform(min_val, max_val)
            
            elif field_type == 'integer':
                min_val = field_config.get('min', 0)
                max_val = field_config.get('max', 100)
                input_data[field_name] = random.randint(min_val, max_val)
            
            elif field_type == 'string':
                options = field_config.get('options', ['value1', 'value2'])
                input_data[field_name] = random.choice(options)
            
            elif field_type == 'boolean':
                input_data[field_name] = random.choice([True, False])
        
        return input_data
    
    @staticmethod
    def get_node_duration(node, node_durations):
        node_id = node.node_id
        node_type = node.type
        
        if node_id in node_durations:
            duration_config = node_durations[node_id]
        elif node_type in node_durations:
            duration_config = node_durations[node_type]
        else:
            duration_config = {'min': 10, 'max': 100}
        
        min_duration = duration_config.get('min', 10)
        max_duration = duration_config.get('max', 100)
        
        return random.randint(min_duration, max_duration)
    
    @staticmethod
    def analyze_bottlenecks(node_statistics):
        bottlenecks = []
        
        sorted_nodes = sorted(
            node_statistics.items(),
            key=lambda x: x[1].get('avg_duration_ms', 0),
            reverse=True
        )
        
        for node_id, stats in sorted_nodes[:5]:
            bottlenecks.append({
                'node_id': node_id,
                'avg_duration_ms': stats.get('avg_duration_ms', 0),
                'executions': stats.get('executions', 0),
                'total_time_ms': stats.get('total_duration_ms', 0)
            })
        
        return bottlenecks
