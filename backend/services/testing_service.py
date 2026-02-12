from backend.models.test_case import TestCase, TestResult
from backend.models.deployed_api import DeployedAPI
import json
import time


class TestingService:
    
    @staticmethod
    def create_test_case(deployed_api_id, name, description, input_data, expected_output, db):
        test_case = TestCase(
            deployed_api_id=deployed_api_id,
            name=name,
            description=description,
            input_data=json.dumps(input_data),
            expected_output=json.dumps(expected_output) if expected_output else None
        )
        
        db.session.add(test_case)
        db.session.commit()
        
        return test_case.to_dict()
    
    @staticmethod
    def execute_test_case(test_case_id, workflow_execution_func, db):
        test_case = db.session.query(TestCase).get(test_case_id)
        if not test_case:
            return {'success': False, 'error': 'Test case not found'}
        
        deployed_api = db.session.query(DeployedAPI).get(test_case.deployed_api_id)
        if not deployed_api:
            return {'success': False, 'error': 'Deployed API not found'}
        
        input_data = json.loads(test_case.input_data)
        expected_output = json.loads(test_case.expected_output) if test_case.expected_output else None
        
        start_time = time.time()
        
        try:
            result = workflow_execution_func(deployed_api.workflow_id, input_data)
            execution_time_ms = int((time.time() - start_time) * 1000)
            
            status = 'PASS'
            error_message = None
            
            if not result.get('success'):
                status = 'FAIL'
                error_message = result.get('error', 'Execution failed')
            elif expected_output:
                if not TestingService.compare_outputs(result, expected_output):
                    status = 'FAIL'
                    error_message = 'Output does not match expected result'
            
            test_result = TestResult(
                test_case_id=test_case_id,
                status=status,
                actual_output=json.dumps(result),
                error_message=error_message,
                execution_time_ms=execution_time_ms
            )
            
            db.session.add(test_result)
            db.session.commit()
            
            return {
                'success': True,
                'test_result': test_result.to_dict(),
                'test_case': test_case.to_dict()
            }
            
        except Exception as e:
            execution_time_ms = int((time.time() - start_time) * 1000)
            
            test_result = TestResult(
                test_case_id=test_case_id,
                status='ERROR',
                actual_output=None,
                error_message=str(e),
                execution_time_ms=execution_time_ms
            )
            
            db.session.add(test_result)
            db.session.commit()
            
            return {
                'success': False,
                'test_result': test_result.to_dict(),
                'error': str(e)
            }
    
    @staticmethod
    def execute_all_test_cases(deployed_api_id, workflow_execution_func, db):
        deployed_api = db.session.query(DeployedAPI).get(deployed_api_id)
        if not deployed_api:
            return {'success': False, 'error': 'Deployed API not found'}
        
        test_cases = db.session.query(TestCase).filter_by(deployed_api_id=deployed_api_id).all()
        
        results = []
        pass_count = 0
        fail_count = 0
        error_count = 0
        
        for test_case in test_cases:
            result = TestingService.execute_test_case(test_case.id, workflow_execution_func, db)
            results.append(result)
            
            if result.get('success'):
                test_status = result['test_result']['status']
                if test_status == 'PASS':
                    pass_count += 1
                elif test_status == 'FAIL':
                    fail_count += 1
                else:
                    error_count += 1
            else:
                error_count += 1
        
        return {
            'success': True,
            'total': len(test_cases),
            'passed': pass_count,
            'failed': fail_count,
            'errors': error_count,
            'results': results
        }
    
    @staticmethod
    def compare_outputs(actual, expected):
        if isinstance(expected, dict):
            for key, value in expected.items():
                if key not in actual:
                    return False
                if not TestingService.compare_outputs(actual[key], value):
                    return False
            return True
        elif isinstance(expected, list):
            if len(actual) != len(expected):
                return False
            for a, e in zip(actual, expected):
                if not TestingService.compare_outputs(a, e):
                    return False
            return True
        else:
            return actual == expected
    
    @staticmethod
    def get_test_results(test_case_id, db, limit=10):
        results = db.session.query(TestResult)\
            .filter_by(test_case_id=test_case_id)\
            .order_by(TestResult.executed_at.desc())\
            .limit(limit)\
            .all()
        
        return [r.to_dict() for r in results]
