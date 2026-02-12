import xml.etree.ElementTree as ET
import json


class BPMNService:
    
    BPMN_NS = {'bpmn': 'http://www.omg.org/spec/BPMN/20100524/MODEL'}
    
    @staticmethod
    def parse_bpmn_xml(xml_content):
        try:
            root = ET.fromstring(xml_content)
            
            process_elements = root.findall('.//bpmn:process', BPMNService.BPMN_NS)
            
            if not process_elements:
                return {'success': False, 'error': 'No process found in BPMN'}
            
            process_elem = process_elements[0]
            process_id = process_elem.get('id')
            process_name = process_elem.get('name', process_id)
            
            nodes = []
            edges = []
            
            for elem in process_elem:
                tag = elem.tag.replace(f'{{{BPMNService.BPMN_NS["bpmn"]}}}', '')
                
                if tag == 'startEvent':
                    nodes.append({
                        'node_id': elem.get('id'),
                        'label': elem.get('name', 'Start'),
                        'type': 'start',
                        'config': {}
                    })
                
                elif tag == 'endEvent':
                    nodes.append({
                        'node_id': elem.get('id'),
                        'label': elem.get('name', 'End'),
                        'type': 'end',
                        'config': {}
                    })
                
                elif tag == 'userTask':
                    nodes.append({
                        'node_id': elem.get('id'),
                        'label': elem.get('name', 'User Task'),
                        'type': 'userTask',
                        'config': {
                            'assignee': elem.get('assignee'),
                            'candidate_users': elem.get('candidateUsers', '').split(','),
                            'candidate_groups': elem.get('candidateGroups', '').split(',')
                        }
                    })
                
                elif tag == 'serviceTask':
                    nodes.append({
                        'node_id': elem.get('id'),
                        'label': elem.get('name', 'Service Task'),
                        'type': 'serviceTask',
                        'config': {
                            'implementation': elem.get('implementation')
                        }
                    })
                
                elif tag == 'businessRuleTask':
                    nodes.append({
                        'node_id': elem.get('id'),
                        'label': elem.get('name', 'Business Rule'),
                        'type': 'businessRule',
                        'config': {}
                    })
                
                elif tag == 'exclusiveGateway':
                    nodes.append({
                        'node_id': elem.get('id'),
                        'label': elem.get('name', 'Gateway'),
                        'type': 'gateway',
                        'config': {}
                    })
                
                elif tag == 'sequenceFlow':
                    edges.append({
                        'edge_id': elem.get('id'),
                        'source': elem.get('sourceRef'),
                        'target': elem.get('targetRef'),
                        'label': elem.get('name', '')
                    })
            
            return {
                'success': True,
                'process_id': process_id,
                'process_name': process_name,
                'nodes': nodes,
                'edges': edges
            }
            
        except Exception as e:
            return {'success': False, 'error': f'Failed to parse BPMN: {str(e)}'}
    
    @staticmethod
    def generate_bpmn_xml(process_id, process_name, nodes, edges):
        root = ET.Element('definitions', {
            'xmlns': 'http://www.omg.org/spec/BPMN/20100524/MODEL',
            'xmlns:bpmndi': 'http://www.omg.org/spec/BPMN/20100524/DI',
            'xmlns:dc': 'http://www.omg.org/spec/DD/20100524/DC',
            'xmlns:di': 'http://www.omg.org/spec/DD/20100524/DI',
            'targetNamespace': 'http://bpmn.io/schema/bpmn',
            'id': f'Definitions_{process_id}'
        })
        
        process = ET.SubElement(root, 'process', {
            'id': process_id,
            'name': process_name,
            'isExecutable': 'true'
        })
        
        for node in nodes:
            node_type = node.get('type')
            node_id = node.get('node_id')
            label = node.get('label', '')
            config = node.get('config', {})
            
            if node_type == 'start':
                ET.SubElement(process, 'startEvent', {'id': node_id, 'name': label})
            
            elif node_type == 'end':
                ET.SubElement(process, 'endEvent', {'id': node_id, 'name': label})
            
            elif node_type == 'userTask':
                attrs = {'id': node_id, 'name': label}
                if config.get('assignee'):
                    attrs['assignee'] = config['assignee']
                ET.SubElement(process, 'userTask', attrs)
            
            elif node_type == 'serviceTask':
                ET.SubElement(process, 'serviceTask', {'id': node_id, 'name': label})
            
            elif node_type == 'businessRule':
                ET.SubElement(process, 'businessRuleTask', {'id': node_id, 'name': label})
            
            elif node_type == 'gateway':
                ET.SubElement(process, 'exclusiveGateway', {'id': node_id, 'name': label})
        
        for edge in edges:
            ET.SubElement(process, 'sequenceFlow', {
                'id': edge.get('edge_id'),
                'sourceRef': edge.get('source'),
                'targetRef': edge.get('target'),
                'name': edge.get('label', '')
            })
        
        return ET.tostring(root, encoding='unicode')
    
    @staticmethod
    def validate_bpmn(nodes, edges):
        errors = []
        warnings = []
        
        start_nodes = [n for n in nodes if n.get('type') == 'start']
        end_nodes = [n for n in nodes if n.get('type') == 'end']
        
        if len(start_nodes) == 0:
            errors.append('Process must have at least one start event')
        
        if len(end_nodes) == 0:
            errors.append('Process must have at least one end event')
        
        if len(start_nodes) > 1:
            warnings.append('Process has multiple start events')
        
        node_ids = set(n.get('node_id') for n in nodes)
        for edge in edges:
            if edge.get('source') not in node_ids:
                errors.append(f'Edge source not found: {edge.get("source")}')
            if edge.get('target') not in node_ids:
                errors.append(f'Edge target not found: {edge.get("target")}')
        
        for node in nodes:
            node_id = node.get('node_id')
            incoming = [e for e in edges if e.get('target') == node_id]
            outgoing = [e for e in edges if e.get('source') == node_id]
            
            if node.get('type') == 'start' and len(incoming) > 0:
                warnings.append(f'Start event {node_id} has incoming edges')
            
            if node.get('type') == 'end' and len(outgoing) > 0:
                warnings.append(f'End event {node_id} has outgoing edges')
            
            if node.get('type') not in ['start', 'end'] and len(incoming) == 0:
                warnings.append(f'Node {node_id} has no incoming edges')
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
