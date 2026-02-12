import json


class FormService:
    
    @staticmethod
    def generate_form_from_schema(schema):
        form_fields = []
        
        properties = schema.get('properties', {})
        required_fields = schema.get('required', [])
        
        for field_name, field_spec in properties.items():
            field_type = field_spec.get('type', 'string')
            
            form_field = {
                'name': field_name,
                'label': field_spec.get('title', field_name.replace('_', ' ').title()),
                'type': FormService.map_schema_type_to_form_type(field_type),
                'required': field_name in required_fields,
                'description': field_spec.get('description', ''),
                'placeholder': field_spec.get('placeholder', ''),
                'default': field_spec.get('default')
            }
            
            if field_type == 'string' and field_spec.get('enum'):
                form_field['type'] = 'select'
                form_field['options'] = field_spec['enum']
            
            if field_type in ['number', 'integer']:
                form_field['min'] = field_spec.get('minimum')
                form_field['max'] = field_spec.get('maximum')
            
            if field_type == 'string':
                form_field['minLength'] = field_spec.get('minLength')
                form_field['maxLength'] = field_spec.get('maxLength')
                form_field['pattern'] = field_spec.get('pattern')
            
            form_fields.append(form_field)
        
        return {
            'fields': form_fields,
            'layout': 'vertical',
            'submit_button_text': 'Submit'
        }
    
    @staticmethod
    def map_schema_type_to_form_type(schema_type):
        mapping = {
            'string': 'text',
            'integer': 'number',
            'number': 'number',
            'boolean': 'checkbox',
            'array': 'multiselect',
            'object': 'json'
        }
        return mapping.get(schema_type, 'text')
    
    @staticmethod
    def validate_form_data(form_definition, form_data):
        errors = {}
        
        for field in form_definition.get('fields', []):
            field_name = field['name']
            field_type = field['type']
            required = field.get('required', False)
            
            value = form_data.get(field_name)
            
            if required and (value is None or value == ''):
                errors[field_name] = f'{field["label"]} is required'
                continue
            
            if value is not None and value != '':
                if field_type == 'number':
                    try:
                        numeric_value = float(value)
                        
                        if field.get('min') is not None and numeric_value < field['min']:
                            errors[field_name] = f'{field["label"]} must be at least {field["min"]}'
                        
                        if field.get('max') is not None and numeric_value > field['max']:
                            errors[field_name] = f'{field["label"]} must be at most {field["max"]}'
                    except (ValueError, TypeError):
                        errors[field_name] = f'{field["label"]} must be a number'
                
                elif field_type == 'email':
                    if '@' not in str(value):
                        errors[field_name] = f'{field["label"]} must be a valid email'
                
                elif field_type == 'text':
                    value_str = str(value)
                    
                    if field.get('minLength') and len(value_str) < field['minLength']:
                        errors[field_name] = f'{field["label"]} must be at least {field["minLength"]} characters'
                    
                    if field.get('maxLength') and len(value_str) > field['maxLength']:
                        errors[field_name] = f'{field["label"]} must be at most {field["maxLength"]} characters'
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    @staticmethod
    def render_form_html(form_definition):
        html = '<form class="auto-generated-form">\n'
        
        for field in form_definition.get('fields', []):
            field_name = field['name']
            field_label = field.get('label', field_name)
            field_type = field['type']
            required = field.get('required', False)
            
            html += f'  <div class="form-group">\n'
            html += f'    <label for="{field_name}">{field_label}'
            
            if required:
                html += ' <span class="required">*</span>'
            
            html += '</label>\n'
            
            if field_type == 'text' or field_type == 'email' or field_type == 'number':
                html += f'    <input type="{field_type}" id="{field_name}" name="{field_name}" '
                
                if field.get('placeholder'):
                    html += f'placeholder="{field["placeholder"]}" '
                
                if required:
                    html += 'required '
                
                html += '/>\n'
            
            elif field_type == 'textarea':
                html += f'    <textarea id="{field_name}" name="{field_name}" '
                
                if field.get('placeholder'):
                    html += f'placeholder="{field["placeholder"]}" '
                
                if required:
                    html += 'required '
                
                html += '></textarea>\n'
            
            elif field_type == 'select':
                html += f'    <select id="{field_name}" name="{field_name}" '
                
                if required:
                    html += 'required '
                
                html += '>\n'
                
                if not required:
                    html += '      <option value="">-- Select --</option>\n'
                
                for option in field.get('options', []):
                    html += f'      <option value="{option}">{option}</option>\n'
                
                html += '    </select>\n'
            
            elif field_type == 'checkbox':
                html += f'    <input type="checkbox" id="{field_name}" name="{field_name}" />\n'
            
            if field.get('description'):
                html += f'    <small class="form-text">{field["description"]}</small>\n'
            
            html += '  </div>\n'
        
        submit_text = form_definition.get('submit_button_text', 'Submit')
        html += f'  <button type="submit" class="btn btn-primary">{submit_text}</button>\n'
        html += '</form>'
        
        return html
