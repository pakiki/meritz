# Enterprise BPM System - JBPM + FICO Blaze Advisor Features

## Overview

This system combines the power of JBPM (Business Process Management) with FICO Blaze Advisor's decision engine capabilities to create a comprehensive credit evaluation platform.

## Core Features

### 1. Decision Engine (FICO Blaze Advisor Style)

#### Decision Trees
- **Algorithm Support**: Gini impurity and Entropy (Information Gain)
- **Features**:
  - Automatic tree building from training data
  - Configurable max depth, min samples split, min samples leaf
  - Tree pruning for better generalization
  - Real-time prediction
  - Accuracy calculation

**API Endpoints**:
- `POST /api/decision-tree` - Create new decision tree
- `POST /api/decision-tree/{id}/train` - Train tree with data
- `POST /api/decision-tree/{id}/predict` - Make predictions
- `GET /api/decision-tree/{id}` - Get tree details

#### Scorecards
- **WOE (Weight of Evidence)** calculation
- **IV (Information Value)** calculation
- **PDO (Points to Double Odds)** scaling
- **Features**:
  - Multiple characteristics with weights
  - Attribute binning (equal width, equal frequency)
  - Auto WOE/IV calculation
  - Score decomposition and breakdown
  - Probability of default calculation

**API Endpoints**:
- `POST /api/scorecard` - Create scorecard
- `POST /api/scorecard/{id}/characteristic` - Add characteristic
- `POST /api/scorecard/characteristic/{id}/attribute` - Add attribute
- `POST /api/scorecard/{id}/calculate` - Calculate credit score

**Example Scorecard**:
```json
{
  "name": "Personal Credit Scorecard",
  "base_score": 600,
  "pdo": 20,
  "base_odds": 50,
  "characteristics": [
    {
      "name": "annual_income",
      "weight": 0.30,
      "attributes": [
        {"min_value": 0, "max_value": 30000000, "woe": -0.5, "points": 20},
        {"min_value": 30000000, "max_value": 50000000, "woe": 0.2, "points": 45},
        {"min_value": 50000000, "max_value": 100000000, "woe": 0.8, "points": 65}
      ]
    },
    {
      "name": "credit_history_months",
      "weight": 0.25,
      "attributes": [...]
    }
  ]
}
```

#### Decision Tables
- **Hit Policies**: FIRST, COLLECT, PRIORITY, ANY
- **Operators**: ==, !=, >, >=, <, <=, IN, NOT IN, CONTAINS, REGEX, BETWEEN
- **Features**:
  - Condition-action matrix
  - Multiple rule evaluation
  - Priority-based execution
  - Rule validation

**API Endpoints**:
- `POST /api/decision-table` - Create decision table
- `POST /api/decision-table/{id}/rule` - Add rule
- `POST /api/decision-table/{id}/execute` - Execute table

### 2. API Auto-Generation & Deployment

#### Workflow → API Conversion
When you deploy a workflow, the system automatically:
1. Generates a RESTful API endpoint
2. Creates OpenAPI/Swagger documentation
3. Provides JSON test console
4. Manages API versioning

**Deployment Process**:
```
Workflow → Deploy → API Generated
/api/execute/credit-evaluation
```

**Features**:
- Automatic input/output schema extraction
- API path generation from workflow name
- Version management (1.0.0, 2.0.0, etc.)
- Execution statistics tracking
- Swagger UI integration

**API Endpoints**:
- `POST /api/deployment/workflow/{workflow_id}` - Deploy workflow as API
- `GET /api/deployment/{id}/swagger` - Get Swagger spec
- `POST /api/execute/{api_name}` - Execute deployed API
- `POST /api/deployment/{id}/test` - Test deployment

#### OpenAPI/Swagger Documentation
Auto-generated Swagger spec includes:
- API endpoints and methods
- Request/response schemas
- Example requests and responses
- Authentication requirements
- API metadata (version, description)

**Example Swagger Output**:
```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "Credit Evaluation API",
    "version": "1.0.0"
  },
  "paths": {
    "/api/execute/credit-evaluation": {
      "post": {
        "summary": "Execute Credit Evaluation",
        "requestBody": {...},
        "responses": {...}
      }
    }
  }
}
```

#### JSON Test Console
- Interactive API testing
- Request/response visualization
- Sample code generation (cURL, Python, JavaScript)
- Response validation
- Error handling

### 3. JBPM Features

#### Process Instance Management
- **Real-time Monitoring**: Track process execution
- **Node Instance Tracking**: Monitor individual node executions
- **Process Variables**: Manage process context
- **Audit Logs**: Complete execution history

**API Endpoints**:
- `POST /api/process-instance/execute` - Start process instance
- `GET /api/process-instance/{id}` - Get instance details
- `POST /api/process-instance/{id}/abort` - Abort process

**Process Instance Data**:
```json
{
  "instance_id": "PI-20240101-001",
  "status": "RUNNING",
  "variables": {...},
  "start_time": "2024-01-01T10:00:00",
  "node_instances": [
    {
      "node_id": "node-1",
      "node_type": "businessRule",
      "status": "COMPLETED",
      "duration_ms": 150
    }
  ]
}
```

#### Human Task Service
- **Task Assignment**: Assign tasks to users/groups
- **Task Claiming**: Users claim tasks from pool
- **Task Completion**: Complete tasks with output data
- **Task Delegation**: Delegate tasks to other users
- **Task History**: Track all task actions

**API Endpoints**:
- `GET /api/task/my-tasks` - Get user's tasks
- `POST /api/task/{id}/claim` - Claim task
- `POST /api/task/{id}/complete` - Complete task
- `POST /api/task/{id}/delegate` - Delegate task
- `POST /api/task/{id}/release` - Release task

**Task Workflow**:
```
READY → RESERVED (claimed) → IN_PROGRESS → COMPLETED
       ↓
    RELEASED (back to pool)
```

#### BPMN 2.0 Support
- **Start Event**: Process entry point
- **End Event**: Process completion
- **User Task**: Human interaction required
- **Service Task**: Automated service call
- **Business Rule Task**: Decision engine integration
- **Exclusive Gateway**: Conditional branching
- **Sequence Flow**: Node connections

**BPMN XML Import/Export**:
```xml
<process id="credit-evaluation" name="Credit Evaluation">
  <startEvent id="start"/>
  <userTask id="application" name="Submit Application"/>
  <businessRuleTask id="scorecard" name="Calculate Score"/>
  <exclusiveGateway id="gateway"/>
  <endEvent id="approved"/>
  <endEvent id="rejected"/>
  <sequenceFlow sourceRef="start" targetRef="application"/>
  <sequenceFlow sourceRef="application" targetRef="scorecard"/>
  <sequenceFlow sourceRef="scorecard" targetRef="gateway"/>
  <sequenceFlow sourceRef="gateway" targetRef="approved">
    <conditionExpression>credit_score >= 700</conditionExpression>
  </sequenceFlow>
  <sequenceFlow sourceRef="gateway" targetRef="rejected">
    <conditionExpression>credit_score < 700</conditionExpression>
  </sequenceFlow>
</process>
```

#### Process Simulation
- **Monte Carlo Simulation**: Run multiple instances
- **Performance Analysis**: Identify bottlenecks
- **Duration Statistics**: Min, max, avg, percentiles
- **Node Statistics**: Execution counts and times
- **Success Rate**: Track completion vs failures

**Simulation Config**:
```json
{
  "num_instances": 1000,
  "input_generator": {
    "annual_income": {"type": "integer", "min": 20000000, "max": 100000000},
    "credit_history_months": {"type": "integer", "min": 0, "max": 120},
    "debt_ratio": {"type": "number", "min": 0, "max": 1}
  },
  "node_durations": {
    "businessRule": {"min": 50, "max": 200},
    "userTask": {"min": 1000, "max": 5000}
  }
}
```

**Simulation Results**:
```json
{
  "total_instances": 1000,
  "successful": 850,
  "failed": 150,
  "success_rate": 0.85,
  "avg_duration_ms": 2450,
  "p50_duration_ms": 2200,
  "p95_duration_ms": 4100,
  "p99_duration_ms": 4800,
  "node_statistics": {
    "scorecard": {
      "executions": 1000,
      "avg_duration_ms": 120
    }
  }
}
```

## Complete Workflow Example

### Step 1: Create Scorecard
```bash
POST /api/scorecard
{
  "name": "Personal Credit Scorecard",
  "base_score": 600,
  "pdo": 20,
  "base_odds": 50
}
```

### Step 2: Add Characteristics
```bash
POST /api/scorecard/1/characteristic
{
  "name": "annual_income",
  "weight": 0.30
}

POST /api/scorecard/characteristic/1/attribute
{
  "attribute": "High Income",
  "min_value": 50000000,
  "max_value": 999999999,
  "good_count": 80,
  "bad_count": 20
}
```

### Step 3: Create Workflow
```bash
POST /api/workflow
{
  "name": "Credit Evaluation",
  "nodes": [
    {"type": "start", "label": "Start"},
    {"type": "businessRule", "label": "Scorecard", "config": {"rule_type": "SCORECARD", "rule_id": 1}},
    {"type": "gateway", "label": "Score >= 700?", "config": {"condition": "credit_score >= 700"}},
    {"type": "end", "label": "Approved"},
    {"type": "end", "label": "Rejected"}
  ],
  "edges": [...]
}
```

### Step 4: Deploy as API
```bash
POST /api/deployment/workflow/1
→ Creates: /api/execute/credit-evaluation
```

### Step 5: Execute API
```bash
POST /api/execute/credit-evaluation
{
  "annual_income": 60000000,
  "credit_history_months": 36,
  "debt_ratio": 0.35
}

Response:
{
  "instance_id": "PI-20240101-001",
  "status": "COMPLETED",
  "result": {
    "credit_score": 720,
    "probability": 0.8523,
    "decision": "APPROVED"
  }
}
```

### Step 6: View Swagger Docs
```bash
GET /api/deployment/1/swagger
→ Returns OpenAPI 3.0 specification
```

### Step 7: Test in Console
Use the web UI JSON Test Console to:
- Edit request JSON
- Execute API
- View formatted response
- Generate code samples

## Database Models (13 Total)

1. **DecisionTree** - Tree structure and config
2. **DecisionTreeNode** - Individual tree nodes
3. **Scorecard** - Scorecard definition
4. **ScorecardCharacteristic** - Scorecard features
5. **ScorecardAttribute** - Binned attributes with WOE/IV
6. **DecisionTable** - Decision table definition
7. **DecisionTableRule** - Individual rules
8. **RuleSet** - Rule set container
9. **DeployedAPI** - Deployed API metadata
10. **TestCase** - API test cases
11. **TestResult** - Test execution results
12. **ProcessInstance** - Process execution instance
13. **HumanTask** - User tasks
14. **NodeInstance** - Node execution tracking
15. **AuditLog** - Complete audit trail

## Services (12 Total)

1. **DecisionTreeService** - Tree building, prediction
2. **ScorecardService** - WOE/IV/PDO calculations
3. **DecisionTableService** - Rule matching
4. **RuleEngineService** - Unified rule execution
5. **APIGenerationService** - Auto API creation
6. **DeploymentService** - Deployment management
7. **TestingService** - API testing
8. **ProcessInstanceService** - Process execution
9. **HumanTaskService** - Task management
10. **BPMNService** - BPMN parsing/generation
11. **SimulationService** - Process simulation
12. **FormService** - Dynamic form generation

## Frontend Components (10+ Total)

1. **ScorecardDesigner** - Visual scorecard builder
2. **APITester** - JSON test console
3. **DeploymentPage** - Deployment management
4. **ProcessInstanceViewer** - Process monitoring
5. **TaskList** - User task management
6. **SwaggerViewer** - API documentation
7. **Canvas** - Workflow designer (existing)
8. **ExecutionMonitor** - Real-time monitoring

## Technology Stack

### Backend
- **Flask 3.0.0** - Web framework
- **SQLAlchemy** - ORM
- **SQLite** - Database
- **NumPy** - Scientific computing
- **Flask-CORS** - Cross-origin support

### Frontend
- **React 18.2.0** - UI framework
- **Material-UI** - Component library
- **ReactFlow** - Workflow visualization
- **Axios** - HTTP client

## Key Metrics

- **66+ Files** implemented
- **13 Database Models** with full relationships
- **12 Services** with comprehensive logic
- **11 API Routes** with RESTful design
- **10+ React Components** for rich UI
- **3 Decision Engines** (Tree, Scorecard, Table)
- **Full BPMN 2.0** support
- **OpenAPI 3.0** auto-generation

## Acceptance Criteria ✅

✅ Decision Tree creation and evaluation  
✅ Scorecard WOE/IV/PDO calculation  
✅ Workflow deployment → API generation  
✅ Swagger documentation auto-creation  
✅ JSON Test Console  
✅ Process Instance monitoring  
✅ Human Task management  
✅ BAM Dashboard (process analytics)  
✅ All models have to_dict() methods  
✅ Comprehensive error handling  
✅ RESTful API design  

## Getting Started

### 1. Setup
```bash
./setup.sh
```

### 2. Start Backend
```bash
cd backend
python app.py
```

### 3. Start Frontend
```bash
cd frontend
npm start
```

### 4. Access Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Swagger Docs**: http://localhost:5000/api/deployment/{id}/swagger

## Next Steps

1. Create your first scorecard
2. Build a credit evaluation workflow
3. Deploy as API
4. Test with JSON console
5. Monitor process instances
6. Manage human tasks
7. Run simulations
8. View analytics

## Support

For issues or questions, check the API documentation at `/api/health` endpoint.
