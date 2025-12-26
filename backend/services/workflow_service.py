from models.workflow import Workflow, WorkflowNode, WorkflowEdge
from database import db
import json

class WorkflowService:
    """워크플로우 관련 비즈니스 로직"""
    
    def create_workflow(self, data):
        """워크플로우 생성"""
        workflow = Workflow(
            name=data.get('name'),
            description=data.get('description'),
            version=data.get('version', '1.0.0'),
            status=data.get('status', 'draft')
        )
        db.session.add(workflow)
        db.session.flush()
        
        # 노드 생성
        if 'nodes' in data:
            for node_data in data['nodes']:
                node = WorkflowNode(
                    workflow_id=workflow.id,
                    node_id=node_data.get('node_id'),
                    node_type=node_data.get('node_type'),
                    label=node_data.get('label'),
                    position_x=node_data.get('position', {}).get('x', 0),
                    position_y=node_data.get('position', {}).get('y', 0),
                    config=json.dumps(node_data.get('config', {}))
                )
                db.session.add(node)
        
        # 엣지 생성
        if 'edges' in data:
            for edge_data in data['edges']:
                edge = WorkflowEdge(
                    workflow_id=workflow.id,
                    edge_id=edge_data.get('edge_id'),
                    source_node_id=edge_data.get('source'),
                    target_node_id=edge_data.get('target'),
                    source_handle=edge_data.get('sourceHandle'),
                    target_handle=edge_data.get('targetHandle'),
                    label=edge_data.get('label'),
                    condition=edge_data.get('condition')
                )
                db.session.add(edge)
        
        db.session.commit()
        return workflow
    
    def update_workflow(self, workflow_id, data):
        """워크플로우 업데이트"""
        workflow = Workflow.query.get_or_404(workflow_id)
        
        if 'name' in data:
            workflow.name = data['name']
        if 'description' in data:
            workflow.description = data['description']
        if 'version' in data:
            workflow.version = data['version']
        if 'status' in data:
            workflow.status = data['status']
        
        # 기존 노드와 엣지 삭제
        if 'nodes' in data:
            WorkflowNode.query.filter_by(workflow_id=workflow_id).delete()
            for node_data in data['nodes']:
                node = WorkflowNode(
                    workflow_id=workflow.id,
                    node_id=node_data.get('node_id'),
                    node_type=node_data.get('node_type'),
                    label=node_data.get('label'),
                    position_x=node_data.get('position', {}).get('x', 0),
                    position_y=node_data.get('position', {}).get('y', 0),
                    config=json.dumps(node_data.get('config', {}))
                )
                db.session.add(node)
        
        if 'edges' in data:
            WorkflowEdge.query.filter_by(workflow_id=workflow_id).delete()
            for edge_data in data['edges']:
                edge = WorkflowEdge(
                    workflow_id=workflow.id,
                    edge_id=edge_data.get('edge_id'),
                    source_node_id=edge_data.get('source'),
                    target_node_id=edge_data.get('target'),
                    source_handle=edge_data.get('sourceHandle'),
                    target_handle=edge_data.get('targetHandle'),
                    label=edge_data.get('label'),
                    condition=edge_data.get('condition')
                )
                db.session.add(edge)
        
        db.session.commit()
        return workflow
    
    def delete_workflow(self, workflow_id):
        """워크플로우 삭제"""
        workflow = Workflow.query.get_or_404(workflow_id)
        db.session.delete(workflow)
        db.session.commit()
    
    def validate_workflow(self, workflow_id):
        """워크플로우 검증"""
        workflow = Workflow.query.get_or_404(workflow_id)
        errors = []
        warnings = []
        
        # 시작 노드 확인
        start_nodes = [node for node in workflow.nodes if node.node_type == 'start']
        if len(start_nodes) == 0:
            errors.append('시작 노드가 없습니다.')
        elif len(start_nodes) > 1:
            errors.append('시작 노드가 여러 개 있습니다.')
        
        # 종료 노드 확인
        end_nodes = [node for node in workflow.nodes if node.node_type == 'end']
        if len(end_nodes) == 0:
            warnings.append('종료 노드가 없습니다.')
        
        # 고립된 노드 확인
        node_ids = {node.node_id for node in workflow.nodes}
        connected_nodes = set()
        for edge in workflow.edges:
            connected_nodes.add(edge.source_node_id)
            connected_nodes.add(edge.target_node_id)
        
        isolated_nodes = node_ids - connected_nodes - {node.node_id for node in start_nodes}
        if isolated_nodes:
            warnings.append(f'연결되지 않은 노드가 있습니다: {", ".join(isolated_nodes)}')
        
        # 순환 참조 확인 (간단한 체크)
        # 실제로는 더 복잡한 그래프 알고리즘 필요
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
