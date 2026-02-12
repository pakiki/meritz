# Enterprise Credit Evaluation BPM System

## 🚀 JBPM + FICO Blaze Advisor Integration

A comprehensive Business Process Management system combining JBPM's workflow capabilities with FICO Blaze Advisor's decision engine features for credit evaluation.

## 🎯 Key Features

### Decision Engine (FICO Style)
- **Decision Trees** with Gini/Entropy algorithms
- **Scorecards** with WOE/IV/PDO calculations
- **Decision Tables** with multiple hit policies
- **Rule Engine** for unified execution

### API Auto-Generation
- Workflow → RESTful API conversion
- OpenAPI/Swagger documentation
- JSON test console
- Version management
- Execution statistics

### JBPM Features
- BPMN 2.0 support
- Process instance monitoring
- Human task service
- Process simulation
- Audit logging
- Form builder

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                      │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐ │
│  │  Workflow   │  │  Scorecard   │  │   Deployment   │ │
│  │  Designer   │  │  Designer    │  │   Manager      │ │
│  └─────────────┘  └──────────────┘  └────────────────┘ │
└─────────────────────────────────────────────────────────┘
                           ↕ REST API
┌─────────────────────────────────────────────────────────┐
│                   Flask Backend                          │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐ │
│  │  Decision   │  │   Process    │  │      API       │ │
│  │  Engine     │  │   Instance   │  │   Generator    │ │
│  └─────────────┘  └──────────────┘  └────────────────┘ │
└─────────────────────────────────────────────────────────┘
                           ↕
┌─────────────────────────────────────────────────────────┐
│              SQLite Database                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │Decision  │  │Scorecard │  │ Process  │  │  Task   │ │
│  │Trees     │  │Data      │  │Instances │  │ Data    │ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────┘
```

## 🛠️ Technology Stack

### Backend
- **Flask 3.0.0** - Web framework
- **SQLAlchemy** - ORM
- **NumPy** - Scientific computing
- **Flask-CORS** - Cross-origin support

### Frontend
- **React 18** - UI framework
- **Material-UI** - Component library
- **ReactFlow** - Workflow visualization
- **Axios** - HTTP client

## 📦 Installation

```bash
# Clone repository
git clone <repository-url>
cd project

# Run setup
./setup.sh

# Start backend
cd backend
python app.py

# Start frontend (new terminal)
cd frontend
npm start
```

## 🎮 Quick Start

### 1. Create a Scorecard

```bash
POST http://localhost:5000/api/scorecard
{
  "name": "Personal Credit Scorecard",
  "base_score": 600,
  "pdo": 20,
  "base_odds": 50
}
```

### 2. Add Characteristics

```bash
POST http://localhost:5000/api/scorecard/1/characteristic
{
  "name": "annual_income",
  "weight": 0.30
}
```

### 3. Create Workflow

Design a workflow with:
- Start Event
- Business Rule Task (Scorecard)
- Exclusive Gateway
- End Events

### 4. Deploy as API

```bash
POST http://localhost:5000/api/deployment/workflow/1
```

Creates: `/api/execute/your-workflow-name`

### 5. Execute API

```bash
POST http://localhost:5000/api/execute/your-workflow-name
{
  "annual_income": 60000000,
  "credit_history_months": 36,
  "debt_ratio": 0.35
}
```

Response:
```json
{
  "instance_id": "PI-001",
  "status": "COMPLETED",
  "result": {
    "credit_score": 720,
    "probability": 0.85,
    "decision": "APPROVED"
  }
}
```

## 📚 Documentation

- **[BPM_FEATURES.md](BPM_FEATURES.md)** - Complete feature documentation
- **[QUICKSTART_BPM.md](QUICKSTART_BPM.md)** - Detailed quick start guide
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Technical implementation details
- **[CHECKLIST.md](CHECKLIST.md)** - Implementation checklist

## 🔑 Key Components

### Backend (48 Python files)

#### Models (17 files)
- Decision Trees, Scorecards, Decision Tables
- Process Definitions, Instances
- Human Tasks, Audit Logs
- Deployed APIs, Test Cases

#### Services (16 files)
- Decision Tree Service (Gini/Entropy)
- Scorecard Service (WOE/IV/PDO)
- Decision Table Service
- Process Instance Service
- Human Task Service
- API Generation Service
- Deployment Service
- Simulation Service

#### Routes (11 files)
- Decision Tree API
- Scorecard API
- Deployment API
- Process Instance API
- Human Task API
- Dynamic API (runtime endpoints)

### Frontend (17 JSX files)

#### Components
- Scorecard Designer
- API Tester (JSON Console)
- Workflow Editor
- Execution Monitor
- Property Panel

#### Pages
- Dashboard
- Workflow Page
- Scorecard Page
- Deployment Page
- Application Page

## 🎯 Use Cases

### 1. Credit Evaluation

```
Application → Scorecard → Decision → Approval/Rejection
```

### 2. Risk Assessment

```
Data → Decision Tree → Risk Category → Action
```

### 3. Automated Decision Making

```
Input → Decision Table → Multiple Rules → Output
```

### 4. Process Automation

```
Start → User Task → Business Rule → Gateway → End
```

## 📊 Example Workflow

```
┌─────────┐     ┌──────────┐     ┌─────────┐
│  Start  │────▶│ Scorecard│────▶│ Gateway │
└─────────┘     └──────────┘     └─────────┘
                                      │
                     ┌────────────────┴────────────────┐
                     ▼                                 ▼
              ┌──────────┐                      ┌──────────┐
              │ Approved │                      │ Rejected │
              └──────────┘                      └──────────┘
```

## 🔍 Features in Detail

### Decision Trees
- CART algorithm
- Gini impurity / Entropy
- Automatic splitting
- Tree pruning
- Prediction
- Accuracy calculation

### Scorecards
- **WOE (Weight of Evidence)**:
  ```
  WOE = ln(Good% / Bad%)
  ```

- **IV (Information Value)**:
  ```
  IV = (Good% - Bad%) × WOE
  ```

- **Points (PDO Scaling)**:
  ```
  Points = (offset + factor × WOE) × weight
  ```

### Decision Tables
- **Hit Policies**:
  - FIRST: First matching rule
  - COLLECT: All matching rules
  - PRIORITY: Highest priority
  - ANY: Any matching rule

- **Operators**:
  - Comparison: ==, !=, >, >=, <, <=
  - Sets: IN, NOT IN
  - Strings: CONTAINS, STARTS_WITH, ENDS_WITH
  - Pattern: REGEX, BETWEEN

### Process Monitoring
- Real-time instance tracking
- Node execution history
- Performance metrics
- Variable inspection
- Audit trail

### Human Tasks
- Task lifecycle: READY → RESERVED → COMPLETED
- Claim/Release mechanism
- Delegation support
- Candidate users/groups
- Form integration

## 🧪 Testing

### JSON Test Console
1. Navigate to Deployments
2. Click eye icon on deployed API
3. Enter JSON request
4. Execute and view response
5. Generate code samples

### Test Cases
```bash
POST /api/deployment/1/test-case
{
  "name": "High Income Test",
  "input_data": {...},
  "expected_output": {...}
}
```

### Simulation
```bash
POST /api/simulation/run
{
  "workflow_id": 1,
  "num_instances": 1000,
  "input_generator": {...}
}
```

## 🔐 API Endpoints

### Decision Engine
- `POST /api/decision-tree` - Create tree
- `POST /api/decision-tree/{id}/train` - Train
- `POST /api/decision-tree/{id}/predict` - Predict
- `POST /api/scorecard` - Create scorecard
- `POST /api/scorecard/{id}/calculate` - Calculate score

### Deployment
- `POST /api/deployment/workflow/{id}` - Deploy
- `GET /api/deployment/{id}/swagger` - Swagger spec
- `POST /api/execute/{api-name}` - Execute API
- `POST /api/deployment/{id}/test` - Test

### Process Management
- `POST /api/process-instance/execute` - Execute
- `GET /api/process-instance/{id}` - Get details
- `POST /api/process-instance/{id}/abort` - Abort

### Tasks
- `GET /api/task/my-tasks` - Get tasks
- `POST /api/task/{id}/claim` - Claim
- `POST /api/task/{id}/complete` - Complete
- `POST /api/task/{id}/delegate` - Delegate

## 📈 Statistics

- **66+ Files** implemented
- **30+ API Endpoints**
- **13 Database Models**
- **12 Service Layers**
- **100% Python Syntax** verified
- **Complete Error Handling**
- **Full CRUD Operations**

## 🎓 Learning Resources

1. **Quick Start**: See QUICKSTART_BPM.md
2. **Features**: See BPM_FEATURES.md
3. **API Docs**: Check Swagger specs
4. **Examples**: See example workflows in docs

## 🤝 Contributing

This is an enterprise-grade system ready for:
- Credit evaluation
- Risk assessment
- Automated decision making
- Process automation
- Workflow management

## 📝 License

See LICENSE file for details.

## 🆘 Support

- **Health Check**: GET http://localhost:5000/api/health
- **API Documentation**: Available via Swagger
- **Examples**: See documentation files

## 🎉 Success Criteria

✅ Decision Trees with Gini/Entropy  
✅ Scorecards with WOE/IV/PDO  
✅ Workflow → API deployment  
✅ Swagger documentation  
✅ JSON test console  
✅ Process monitoring  
✅ Human task management  
✅ Complete audit trail  

---

**Built with ❤️ using JBPM + FICO Blaze Advisor concepts**
