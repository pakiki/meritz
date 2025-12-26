def validate_workflow_data(data):
    """워크플로우 데이터 검증"""
    errors = []
    
    if not data.get('name'):
        errors.append('워크플로우 이름은 필수입니다.')
    
    if 'nodes' in data:
        if not isinstance(data['nodes'], list):
            errors.append('노드는 리스트 형태여야 합니다.')
        else:
            for i, node in enumerate(data['nodes']):
                if not node.get('node_id'):
                    errors.append(f'노드 {i}: node_id는 필수입니다.')
                if not node.get('node_type'):
                    errors.append(f'노드 {i}: node_type은 필수입니다.')
    
    if 'edges' in data:
        if not isinstance(data['edges'], list):
            errors.append('엣지는 리스트 형태여야 합니다.')
        else:
            for i, edge in enumerate(data['edges']):
                if not edge.get('source'):
                    errors.append(f'엣지 {i}: source는 필수입니다.')
                if not edge.get('target'):
                    errors.append(f'엣지 {i}: target는 필수입니다.')
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }

def validate_application_data(data):
    """신청서 데이터 검증"""
    errors = []
    
    if not data.get('workflow_id'):
        errors.append('workflow_id는 필수입니다.')
    
    application_data = data.get('application_data', {})
    
    if not application_data.get('applicant_name'):
        errors.append('신청자 이름은 필수입니다.')
    
    if not application_data.get('applicant_id'):
        errors.append('신청자 식별번호는 필수입니다.')
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }
