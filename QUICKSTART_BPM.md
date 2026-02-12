# Quick Start Guide - Enterprise BPM System

## Setup (5 minutes)

### 1. Install Dependencies
```bash
cd /home/engine/project
./setup.sh
```

### 2. Start Backend
```bash
cd backend
source ../venv/bin/activate
python app.py
```
Backend will run on **http://localhost:5000**

### 3. Start Frontend (in new terminal)
```bash
cd frontend
npm start
```
Frontend will run on **http://localhost:3000**

## Complete Workflow Example (10 minutes)

### Step 1: Create a Scorecard

**Via UI**:
1. Navigate to **Scorecards** page
2. Click **New Scorecard**
3. Enter:
   - Name: "Personal Credit Scorecard"
   - Base Score: 600
   - PDO: 20
   - Base Odds: 50

**Via API**:
```bash
curl -X POST http://localhost:5000/api/scorecard \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Personal Credit Scorecard",
    "description": "Evaluates personal credit risk",
    "base_score": 600,
    "pdo": 20,
    "base_odds": 50
  }'
```

### Step 2: Add Characteristics

**Add Annual Income characteristic**:
```bash
curl -X POST http://localhost:5000/api/scorecard/1/characteristic \
  -H "Content-Type: application/json" \
  -d '{
    "name": "annual_income",
    "weight": 0.30,
    "order": 1
  }'
```

**Add attributes to characteristic**:
```bash
# Low Income
curl -X POST http://localhost:5000/api/scorecard/characteristic/1/attribute \
  -H "Content-Type: application/json" \
  -d '{
    "attribute": "Low Income",
    "min_value": 0,
    "max_value": 30000000,
    "good_count": 30,
    "bad_count": 70,
    "total_good": 100,
    "total_bad": 100
  }'

# Medium Income
curl -X POST http://localhost:5000/api/scorecard/characteristic/1/attribute \
  -H "Content-Type: application/json" \
  -d '{
    "attribute": "Medium Income",
    "min_value": 30000000,
    "max_value": 50000000,
    "good_count": 60,
    "bad_count": 40,
    "total_good": 100,
    "total_bad": 100
  }'

# High Income
curl -X POST http://localhost:5000/api/scorecard/characteristic/1/attribute \
  -H "Content-Type: application/json" \
  -d '{
    "attribute": "High Income",
    "min_value": 50000000,
    "max_value": 999999999,
    "good_count": 85,
    "bad_count": 15,
    "total_good": 100,
    "total_bad": 100
  }'
```

**Add more characteristics** (Credit History, Debt Ratio, etc.):
```bash
# Credit History
curl -X POST http://localhost:5000/api/scorecard/1/characteristic \
  -H "Content-Type: application/json" \
  -d '{
    "name": "credit_history_months",
    "weight": 0.25,
    "order": 2
  }'

# Debt Ratio
curl -X POST http://localhost:5000/api/scorecard/1/characteristic \
  -H "Content-Type: application/json" \
  -d '{
    "name": "debt_ratio",
    "weight": 0.20,
    "order": 3
  }'
```

### Step 3: Test Scorecard

```bash
curl -X POST http://localhost:5000/api/scorecard/1/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "annual_income": 60000000,
      "credit_history_months": 36,
      "debt_ratio": 0.35
    }
  }'
```

**Expected Response**:
```json
{
  "scorecard_id": 1,
  "scorecard_name": "Personal Credit Scorecard",
  "score": 720.5,
  "probability": 0.8523,
  "breakdown": [
    {
      "characteristic": "annual_income",
      "value": 60000000,
      "attribute": "High Income",
      "points": 65.2,
      "woe": 1.7346
    },
    ...
  ]
}
```

### Step 4: Create Workflow

**Via UI**:
1. Go to **Workflows** page
2. Click **New Workflow**
3. Drag and drop nodes:
   - Start Event
   - Business Rule Task (configure with Scorecard)
   - Exclusive Gateway (condition: `credit_score >= 700`)
   - Two End Events (Approved/Rejected)
4. Connect nodes
5. Save workflow

**Via API**:
```bash
curl -X POST http://localhost:5000/api/workflow \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Credit Evaluation Process",
    "description": "Automated credit evaluation with scorecard",
    "nodes": [
      {
        "node_id": "start-1",
        "type": "start",
        "label": "Application Received",
        "position_x": 100,
        "position_y": 100
      },
      {
        "node_id": "scorecard-1",
        "type": "businessRule",
        "label": "Calculate Credit Score",
        "config": "{\"rule_type\": \"SCORECARD\", \"rule_id\": 1}",
        "position_x": 300,
        "position_y": 100
      },
      {
        "node_id": "gateway-1",
        "type": "gateway",
        "label": "Score >= 700?",
        "config": "{\"condition\": \"credit_score >= 700\"}",
        "position_x": 500,
        "position_y": 100
      },
      {
        "node_id": "end-approved",
        "type": "end",
        "label": "Approved",
        "position_x": 700,
        "position_y": 50
      },
      {
        "node_id": "end-rejected",
        "type": "end",
        "label": "Rejected",
        "position_x": 700,
        "position_y": 150
      }
    ],
    "edges": [
      {
        "edge_id": "edge-1",
        "source": "start-1",
        "target": "scorecard-1"
      },
      {
        "edge_id": "edge-2",
        "source": "scorecard-1",
        "target": "gateway-1"
      },
      {
        "edge_id": "edge-3",
        "source": "gateway-1",
        "target": "end-approved",
        "label": "Yes"
      },
      {
        "edge_id": "edge-4",
        "source": "gateway-1",
        "target": "end-rejected",
        "label": "No"
      }
    ]
  }'
```

### Step 5: Deploy as API

**Via UI**:
1. Go to **Deployments** page
2. Click **Deploy Workflow**
3. Select "Credit Evaluation Process"
4. Click Deploy

**Via API**:
```bash
curl -X POST http://localhost:5000/api/deployment/workflow/1 \
  -H "Content-Type: application/json" \
  -d '{
    "version": "1.0.0"
  }'
```

**Response**:
```json
{
  "success": true,
  "deployment": {
    "id": 1,
    "api_name": "credit-evaluation-process",
    "api_path": "/api/execute/credit-evaluation-process",
    "version": "1.0.0",
    "status": "active"
  },
  "api_path": "/api/execute/credit-evaluation-process",
  "swagger_url": "/api/deployment/1/swagger"
}
```

### Step 6: View Swagger Documentation

```bash
curl http://localhost:5000/api/deployment/1/swagger
```

Or visit in browser: `http://localhost:5000/api/deployment/1/swagger`

### Step 7: Execute Deployed API

**Via UI JSON Test Console**:
1. Go to Deployments
2. Click eye icon on deployment
3. Enter JSON in Request panel
4. Click "Execute API"
5. View response

**Via API**:
```bash
curl -X POST http://localhost:5000/api/execute/credit-evaluation-process \
  -H "Content-Type: application/json" \
  -d '{
    "annual_income": 75000000,
    "credit_history_months": 48,
    "debt_ratio": 0.25,
    "employment_years": 5
  }'
```

**Response**:
```json
{
  "success": true,
  "instance_id": "PI-20240212-143022-a3f5e9",
  "status": "COMPLETED",
  "duration_ms": 245,
  "result": {
    "annual_income": 75000000,
    "credit_history_months": 48,
    "debt_ratio": 0.25,
    "credit_score": 745.8,
    "probability": 0.8932,
    "gateway_result": true,
    "workflow_id": 1,
    "instance_id": "PI-20240212-143022-a3f5e9"
  }
}
```

### Step 8: Monitor Process Instance

```bash
curl http://localhost:5000/api/process-instance/PI-20240212-143022-a3f5e9
```

**Response shows**:
- Process status
- Variables
- Node instances executed
- Execution times
- Complete audit trail

## Testing Features

### Create Test Case

```bash
curl -X POST http://localhost:5000/api/deployment/1/test-case \
  -H "Content-Type: application/json" \
  -d '{
    "name": "High Income Applicant",
    "description": "Should be approved",
    "input_data": {
      "annual_income": 80000000,
      "credit_history_months": 60,
      "debt_ratio": 0.20
    },
    "expected_output": {
      "credit_score": 750,
      "gateway_result": true
    }
  }'
```

### Run Test Case

```bash
curl -X POST http://localhost:5000/api/deployment/1/test-case/1/execute
```

## Decision Tree Example

### Create and Train Decision Tree

```bash
# Create tree
curl -X POST http://localhost:5000/api/decision-tree \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Credit Risk Classifier",
    "target_variable": "default",
    "algorithm": "gini",
    "max_depth": 5,
    "min_samples_split": 10,
    "min_samples_leaf": 5
  }'

# Train tree with data
curl -X POST http://localhost:5000/api/decision-tree/1/train \
  -H "Content-Type: application/json" \
  -d '{
    "features": ["income", "credit_score", "debt_ratio"],
    "training_data": [
      {"income": 50000000, "credit_score": 700, "debt_ratio": 0.3, "default": 0},
      {"income": 30000000, "credit_score": 650, "debt_ratio": 0.5, "default": 1},
      {"income": 70000000, "credit_score": 750, "debt_ratio": 0.2, "default": 0},
      ...
    ]
  }'

# Predict
curl -X POST http://localhost:5000/api/decision-tree/1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "income": 60000000,
      "credit_score": 720,
      "debt_ratio": 0.35
    }
  }'
```

## Human Task Workflow

### Create Workflow with User Task

```json
{
  "nodes": [
    {"type": "start"},
    {"type": "userTask", "config": {
      "name": "Manual Review",
      "assignee": "reviewer1",
      "candidate_users": ["reviewer1", "reviewer2"],
      "form_data": {}
    }},
    {"type": "end"}
  ]
}
```

### Manage Tasks

```bash
# Get my tasks
curl http://localhost:5000/api/task/my-tasks?user_id=reviewer1

# Claim task
curl -X POST http://localhost:5000/api/task/TASK-001/claim \
  -H "Content-Type: application/json" \
  -d '{"user_id": "reviewer1"}'

# Complete task
curl -X POST http://localhost:5000/api/task/TASK-001/complete \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "reviewer1",
    "output": {
      "decision": "APPROVED",
      "comments": "Applicant meets all criteria"
    }
  }'
```

## Advanced Features

### Process Simulation

```bash
curl -X POST http://localhost:5000/api/simulation/run \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_id": 1,
    "num_instances": 1000,
    "input_generator": {
      "annual_income": {"type": "integer", "min": 20000000, "max": 100000000},
      "credit_history_months": {"type": "integer", "min": 0, "max": 120}
    }
  }'
```

### Code Examples

**Python**:
```python
import requests

url = "http://localhost:5000/api/execute/credit-evaluation-process"
data = {
    "annual_income": 60000000,
    "credit_history_months": 36,
    "debt_ratio": 0.35
}

response = requests.post(url, json=data)
result = response.json()

print(f"Credit Score: {result['result']['credit_score']}")
print(f"Decision: {'APPROVED' if result['result']['gateway_result'] else 'REJECTED'}")
```

**JavaScript**:
```javascript
fetch('http://localhost:5000/api/execute/credit-evaluation-process', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    annual_income: 60000000,
    credit_history_months: 36,
    debt_ratio: 0.35
  })
})
  .then(res => res.json())
  .then(data => {
    console.log('Credit Score:', data.result.credit_score);
    console.log('Approved:', data.result.gateway_result);
  });
```

## Troubleshooting

### Backend Won't Start
```bash
# Check if port 5000 is in use
lsof -i :5000

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

### Frontend Won't Start
```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

### Database Issues
```bash
# Delete and recreate database
rm -f database/workflow.db
cd backend
python app.py  # Will auto-create tables
```

## Next Steps

1. **Explore UI**: Navigate through all pages
2. **Create More Scorecards**: Add different risk models
3. **Build Complex Workflows**: Add parallel paths, subprocesses
4. **Test APIs**: Use the JSON console
5. **Monitor Processes**: View real-time execution
6. **Manage Tasks**: Test task lifecycle
7. **Run Simulations**: Identify bottlenecks

## Support

- **API Documentation**: Check Swagger specs for each deployment
- **Code Examples**: See BPM_FEATURES.md
- **Architecture**: See IMPLEMENTATION_SUMMARY.md
- **Health Check**: GET http://localhost:5000/api/health

Happy BPM-ing! 🚀
