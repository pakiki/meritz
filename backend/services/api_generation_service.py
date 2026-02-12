import json
from datetime import datetime


class APIGenerationService:
    
    @staticmethod
    def generate_api_name(workflow):
        api_name = workflow.name.lower().replace(' ', '-')
        api_name = ''.join(c for c in api_name if c.isalnum() or c == '-')
        return api_name
    
    @staticmethod
    def generate_api_path(api_name, version='1.0.0'):
        return f"/api/execute/{api_name}"
    
    @staticmethod
    def extract_input_schema(workflow):
        input_fields = []
        
        for node in workflow.nodes:
            if node.type == 'start':
                config = json.loads(node.config) if node.config else {}
                form_fields = config.get('form_fields', [])
                input_fields.extend(form_fields)
        
        schema = {
            "type": "object",
            "properties": {},
            "required": []
        }
        
        for field in input_fields:
            field_name = field.get('name')
            field_type = field.get('type', 'string')
            required = field.get('required', False)
            
            if field_name:
                schema['properties'][field_name] = {
                    "type": field_type,
                    "description": field.get('description', '')
                }
                
                if required:
                    schema['required'].append(field_name)
        
        if not schema['properties']:
            schema['properties']['data'] = {
                "type": "object",
                "description": "Input data for the workflow"
            }
        
        return schema
    
    @staticmethod
    def extract_output_schema(workflow):
        output_fields = []
        
        for node in workflow.nodes:
            if node.type == 'end':
                config = json.loads(node.config) if node.config else {}
                output_fields = config.get('output_fields', [])
                break
        
        schema = {
            "type": "object",
            "properties": {
                "process_instance_id": {
                    "type": "string",
                    "description": "Process instance identifier"
                },
                "status": {
                    "type": "string",
                    "description": "Process execution status"
                },
                "result": {
                    "type": "object",
                    "description": "Process execution result"
                }
            }
        }
        
        if output_fields:
            for field in output_fields:
                field_name = field.get('name')
                field_type = field.get('type', 'string')
                
                if field_name:
                    schema['properties'][field_name] = {
                        "type": field_type,
                        "description": field.get('description', '')
                    }
        
        return schema
    
    @staticmethod
    def generate_swagger_spec(deployed_api, workflow):
        input_schema = json.loads(deployed_api.input_schema) if deployed_api.input_schema else {}
        output_schema = json.loads(deployed_api.output_schema) if deployed_api.output_schema else {}
        
        swagger = {
            "openapi": "3.0.0",
            "info": {
                "title": f"{workflow.name} API",
                "description": deployed_api.description or workflow.description or "Auto-generated API from workflow",
                "version": deployed_api.version,
                "contact": {
                    "name": "API Support"
                }
            },
            "servers": [
                {
                    "url": "http://localhost:5000",
                    "description": "Development server"
                }
            ],
            "paths": {
                deployed_api.api_path: {
                    "post": {
                        "summary": f"Execute {workflow.name}",
                        "description": f"Execute the {workflow.name} workflow with provided input data",
                        "operationId": f"execute_{deployed_api.api_name}",
                        "tags": ["Workflow Execution"],
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": input_schema,
                                    "example": APIGenerationService.generate_example_input(input_schema)
                                }
                            }
                        },
                        "responses": {
                            "200": {
                                "description": "Successful execution",
                                "content": {
                                    "application/json": {
                                        "schema": output_schema,
                                        "example": APIGenerationService.generate_example_output(output_schema)
                                    }
                                }
                            },
                            "400": {
                                "description": "Invalid input",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "error": {"type": "string"}
                                            }
                                        }
                                    }
                                }
                            },
                            "500": {
                                "description": "Server error",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "error": {"type": "string"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "get": {
                        "summary": f"Get {workflow.name} API information",
                        "description": "Get information about the API endpoint",
                        "operationId": f"info_{deployed_api.api_name}",
                        "tags": ["API Information"],
                        "responses": {
                            "200": {
                                "description": "API information",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "api_name": {"type": "string"},
                                                "version": {"type": "string"},
                                                "status": {"type": "string"},
                                                "description": {"type": "string"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "components": {
                "schemas": {}
            }
        }
        
        return swagger
    
    @staticmethod
    def generate_example_input(schema):
        example = {}
        properties = schema.get('properties', {})
        
        for field_name, field_spec in properties.items():
            field_type = field_spec.get('type', 'string')
            
            if field_type == 'string':
                example[field_name] = "example_value"
            elif field_type == 'integer':
                example[field_name] = 100
            elif field_type == 'number':
                example[field_name] = 100.0
            elif field_type == 'boolean':
                example[field_name] = True
            elif field_type == 'array':
                example[field_name] = []
            elif field_type == 'object':
                example[field_name] = {}
        
        return example
    
    @staticmethod
    def generate_example_output(schema):
        example = {
            "process_instance_id": "PI-20240101-001",
            "status": "COMPLETED",
            "result": {}
        }
        
        properties = schema.get('properties', {})
        
        for field_name, field_spec in properties.items():
            if field_name in ['process_instance_id', 'status']:
                continue
            
            field_type = field_spec.get('type', 'string')
            
            if field_type == 'string':
                example[field_name] = "example_value"
            elif field_type == 'integer':
                example[field_name] = 100
            elif field_type == 'number':
                example[field_name] = 100.0
            elif field_type == 'boolean':
                example[field_name] = True
            elif field_type == 'array':
                example[field_name] = []
            elif field_type == 'object':
                example[field_name] = {}
        
        return example
