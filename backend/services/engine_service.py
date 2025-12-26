from models.application import Application, ApplicationLog
from models.workflow import Workflow, WorkflowNode, WorkflowEdge
from database import db
from datetime import datetime
import json
import time

class EngineService:
    """워크플로우 실행 엔진"""
    
    def execute_workflow(self, application_id):
        """워크플로우 실행"""
        application = Application.query.get_or_404(application_id)
        workflow = Workflow.query.get_or_404(application.workflow_id)
        
        # 상태 업데이트
        application.status = 'processing'
        db.session.commit()
        
        try:
            # 시작 노드 찾기
            start_node = next(
                (node for node in workflow.nodes if node.node_type == 'start'),
                None
            )
            
            if not start_node:
                raise Exception('시작 노드를 찾을 수 없습니다.')
            
            # 워크플로우 실행
            context = {
                'application_data': json.loads(application.application_data),
                'score': 0,
                'results': {}
            }
            
            self._execute_node(application, workflow, start_node, context)
            
            # 결과 저장
            application.status = 'completed'
            application.score = context.get('score')
            application.result = json.dumps(context.get('results'))
            application.completed_at = datetime.utcnow()
            db.session.commit()
            
            return {
                'status': 'completed',
                'score': context.get('score'),
                'results': context.get('results')
            }
            
        except Exception as e:
            application.status = 'error'
            db.session.commit()
            
            # 에러 로그 생성
            log = ApplicationLog(
                application_id=application.id,
                action='workflow_execution',
                status='error',
                error_message=str(e)
            )
            db.session.add(log)
            db.session.commit()
            
            raise e
    
    def _execute_node(self, application, workflow, node, context):
        """노드 실행"""
        start_time = time.time()
        
        try:
            # 노드 타입별 처리
            if node.node_type == 'start':
                output = {'message': '워크플로우 시작'}
            elif node.node_type == 'end':
                output = {'message': '워크플로우 종료'}
            elif node.node_type == 'score':
                output = self._execute_score_node(node, context)
            elif node.node_type == 'decision':
                output = self._execute_decision_node(node, context)
            elif node.node_type == 'api':
                output = self._execute_api_node(node, context)
            else:
                output = {'message': f'알 수 없는 노드 타입: {node.node_type}'}
            
            execution_time = time.time() - start_time
            
            # 로그 생성
            log = ApplicationLog(
                application_id=application.id,
                node_id=node.node_id,
                node_type=node.node_type,
                action='execute',
                input_data=json.dumps(context.get('application_data', {})),
                output_data=json.dumps(output),
                status='success',
                execution_time=execution_time
            )
            db.session.add(log)
            db.session.commit()
            
            # 다음 노드로 이동
            if node.node_type != 'end':
                next_nodes = self._get_next_nodes(workflow, node, context)
                for next_node in next_nodes:
                    self._execute_node(application, workflow, next_node, context)
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            # 에러 로그 생성
            log = ApplicationLog(
                application_id=application.id,
                node_id=node.node_id,
                node_type=node.node_type,
                action='execute',
                status='error',
                error_message=str(e),
                execution_time=execution_time
            )
            db.session.add(log)
            db.session.commit()
            
            raise e
    
    def _execute_score_node(self, node, context):
        """점수 계산 노드 실행"""
        config = json.loads(node.config) if node.config else {}
        score_value = config.get('score', 0)
        
        context['score'] = context.get('score', 0) + score_value
        
        return {
            'score_added': score_value,
            'total_score': context['score']
        }
    
    def _execute_decision_node(self, node, context):
        """의사결정 노드 실행"""
        config = json.loads(node.config) if node.config else {}
        condition = config.get('condition', '')
        
        # 간단한 조건 평가 (실제로는 더 복잡한 평가 엔진 필요)
        result = self._evaluate_condition(condition, context)
        
        return {
            'condition': condition,
            'result': result
        }
    
    def _execute_api_node(self, node, context):
        """API 호출 노드 실행"""
        config = json.loads(node.config) if node.config else {}
        
        # 실제 API 호출은 여기서 구현
        return {
            'message': 'API 호출 실행',
            'config': config
        }
    
    def _get_next_nodes(self, workflow, current_node, context):
        """다음 노드 찾기"""
        next_edges = [
            edge for edge in workflow.edges
            if edge.source_node_id == current_node.node_id
        ]
        
        next_nodes = []
        for edge in next_edges:
            # 조건 확인
            if edge.condition:
                if self._evaluate_condition(edge.condition, context):
                    next_node = next(
                        (node for node in workflow.nodes if node.node_id == edge.target_node_id),
                        None
                    )
                    if next_node:
                        next_nodes.append(next_node)
            else:
                next_node = next(
                    (node for node in workflow.nodes if node.node_id == edge.target_node_id),
                    None
                )
                if next_node:
                    next_nodes.append(next_node)
        
        return next_nodes
    
    def _evaluate_condition(self, condition, context):
        """조건 평가"""
        # 간단한 조건 평가
        # 실제로는 더 안전하고 복잡한 평가 엔진 필요
        try:
            return eval(condition, {"__builtins__": {}}, context)
        except:
            return False
