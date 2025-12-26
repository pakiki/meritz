# Meritz 워크플로우 시스템 - 프로젝트 구조

## 개요
이 문서는 Meritz 개인신용평가 워크플로우 시스템의 프로젝트 구조와 각 파일의 역할을 설명합니다.

## 디렉토리 구조

```
meritz/
├── backend/                          # Flask 백엔드 애플리케이션
│   ├── app.py                       # Flask 메인 애플리케이션 진입점
│   ├── config.py                    # 설정 클래스 (개발/프로덕션/테스트)
│   ├── database.py                  # SQLAlchemy 데이터베이스 초기화
│   ├── requirements.txt             # Python 의존성 패키지
│   │
│   ├── routes/                      # API 라우트 (Blueprint)
│   │   ├── __init__.py             # 라우트 모듈 초기화
│   │   ├── workflow.py             # 워크플로우 CRUD API
│   │   ├── application.py          # 신청서 CRUD 및 실행 API
│   │   └── engine.py               # 규칙 관리 및 점수 계산 API
│   │
│   ├── models/                      # SQLAlchemy 데이터 모델
│   │   ├── __init__.py             # 모델 모듈 초기화
│   │   ├── workflow.py             # Workflow, WorkflowNode, WorkflowEdge 모델
│   │   ├── application.py          # Application, ApplicationLog 모델
│   │   └── rule.py                 # Rule 모델
│   │
│   ├── services/                    # 비즈니스 로직 계층
│   │   ├── __init__.py             # 서비스 모듈 초기화
│   │   ├── workflow_service.py     # 워크플로우 생성/수정/검증 로직
│   │   ├── engine_service.py       # 워크플로우 실행 엔진
│   │   └── scoring_service.py      # 신용 점수 계산 로직
│   │
│   └── utils/                       # 유틸리티 함수
│       ├── __init__.py             # 유틸리티 모듈 초기화
│       └── validators.py           # 데이터 검증 함수
│
├── frontend/                         # React 프론트엔드 애플리케이션
│   ├── package.json                 # Node.js 의존성 및 스크립트
│   │
│   ├── public/                      # 정적 파일
│   │   └── index.html              # HTML 템플릿
│   │
│   └── src/                         # React 소스 코드
│       ├── index.js                # React 앱 진입점
│       ├── App.jsx                 # 메인 앱 컴포넌트 (라우팅 설정)
│       │
│       ├── components/              # 재사용 가능한 React 컴포넌트
│       │   ├── WorkflowEditor.jsx  # 워크플로우 비주얼 에디터
│       │   ├── NodePalette.jsx     # 드래그 가능한 노드 팔레트
│       │   ├── Canvas.jsx          # 워크플로우 캔버스
│       │   ├── PropertyPanel.jsx   # 노드 속성 편집 패널
│       │   └── ExecutionMonitor.jsx # 실행 로그 모니터
│       │
│       ├── pages/                   # 페이지 컴포넌트
│       │   ├── Dashboard.jsx       # 대시보드 (통계 및 목록)
│       │   ├── WorkflowPage.jsx    # 워크플로우 생성/편집 페이지
│       │   └── ApplicationPage.jsx # 신청서 생성/조회 페이지
│       │
│       ├── services/                # API 클라이언트 및 비즈니스 로직
│       │   ├── api.js              # Axios 기반 API 호출 함수
│       │   └── workflowService.js  # 워크플로우 유틸리티 함수
│       │
│       ├── styles/                  # 스타일시트
│       │   └── index.css           # 전역 CSS 및 React Flow 커스터마이징
│       │
│       └── utils/                   # 유틸리티 및 상수
│           └── constants.js        # 애플리케이션 상수
│
├── database/                         # 데이터베이스 파일
│   ├── schema.sql                   # SQLite 스키마 정의
│   └── meritz.db                    # SQLite 데이터베이스 (생성됨)
│
├── .env                             # 환경 변수 설정
├── .gitignore                       # Git 무시 파일 목록
├── README.md                        # 프로젝트 README
├── PROJECT_STRUCTURE.md             # 이 파일
├── requirements.txt                 # 전체 Python 의존성
├── docker-compose.yml               # Docker Compose 설정
└── setup.sh                         # 프로젝트 설정 스크립트
```

## 파일 설명

### 백엔드 (Backend)

#### 메인 파일
- **app.py**: Flask 애플리케이션 팩토리, CORS 설정, 라우트 등록
- **config.py**: 환경별 설정 클래스 (개발/프로덕션/테스트)
- **database.py**: SQLAlchemy 데이터베이스 초기화 및 테이블 생성

#### API 라우트 (routes/)
각 라우트 파일은 Flask Blueprint를 정의하고 RESTful API 엔드포인트를 제공합니다.

- **workflow.py**
  - GET /api/workflow/ - 워크플로우 목록
  - GET /api/workflow/<id> - 워크플로우 상세
  - POST /api/workflow/ - 워크플로우 생성
  - PUT /api/workflow/<id> - 워크플로우 수정
  - DELETE /api/workflow/<id> - 워크플로우 삭제
  - POST /api/workflow/<id>/validate - 워크플로우 검증

- **application.py**
  - GET /api/application/ - 신청서 목록 (페이지네이션)
  - GET /api/application/<id> - 신청서 상세
  - POST /api/application/ - 신청서 생성
  - POST /api/application/<id>/execute - 신청서 실행
  - GET /api/application/<id>/logs - 실행 로그 조회

- **engine.py**
  - GET /api/engine/rules - 규칙 목록
  - POST /api/engine/rules - 규칙 생성
  - PUT /api/engine/rules/<id> - 규칙 수정
  - DELETE /api/engine/rules/<id> - 규칙 삭제
  - POST /api/engine/score - 신용 점수 계산

#### 데이터 모델 (models/)
SQLAlchemy ORM 모델 정의

- **workflow.py**
  - Workflow: 워크플로우 정의
  - WorkflowNode: 워크플로우 노드 (시작, 종료, 의사결정, 점수, API)
  - WorkflowEdge: 노드 간 연결 및 조건

- **application.py**
  - Application: 신청서 정보 및 평가 결과
  - ApplicationLog: 워크플로우 실행 로그

- **rule.py**
  - Rule: 평가 규칙 정의

#### 비즈니스 로직 (services/)
- **workflow_service.py**: 워크플로우 생성, 수정, 삭제, 검증 로직
- **engine_service.py**: 워크플로우 실행 엔진 (노드 순회 및 실행)
- **scoring_service.py**: 신용 점수 계산 알고리즘

#### 유틸리티 (utils/)
- **validators.py**: 워크플로우 및 신청서 데이터 검증 함수

### 프론트엔드 (Frontend)

#### 메인 파일
- **index.js**: React 앱 진입점, ReactDOM 렌더링
- **App.jsx**: 메인 앱 컴포넌트, 라우팅 설정, MUI 테마

#### 컴포넌트 (components/)
- **WorkflowEditor.jsx**: ReactFlow 기반 워크플로우 시각적 에디터
- **NodePalette.jsx**: 드래그 가능한 노드 팔레트 (시작, 종료, 의사결정 등)
- **Canvas.jsx**: 워크플로우 캔버스 래퍼 컴포넌트
- **PropertyPanel.jsx**: 선택된 노드의 속성 편집 패널
- **ExecutionMonitor.jsx**: 워크플로우 실행 로그 실시간 모니터링

#### 페이지 (pages/)
- **Dashboard.jsx**: 메인 대시보드 (통계, 최근 워크플로우/신청서)
- **WorkflowPage.jsx**: 워크플로우 생성 및 편집 페이지
- **ApplicationPage.jsx**: 신청서 생성 및 조회 페이지

#### 서비스 (services/)
- **api.js**: Axios 기반 API 클라이언트 (모든 백엔드 API 호출 함수)
- **workflowService.js**: 워크플로우 검증, 데이터 변환 유틸리티

#### 스타일 (styles/)
- **index.css**: 전역 CSS, React Flow 노드 커스터마이징

#### 유틸리티 (utils/)
- **constants.js**: 애플리케이션 상수 (상태, 노드 타입 등)

### 데이터베이스 (database/)
- **schema.sql**: SQLite 스키마 정의 (테이블, 인덱스)
- **meritz.db**: SQLite 데이터베이스 파일 (자동 생성)

### 설정 파일
- **.env**: 환경 변수 (Flask 포트, 데이터베이스 경로 등)
- **.gitignore**: Git 무시 파일 목록
- **requirements.txt**: Python 의존성 패키지
- **docker-compose.yml**: Docker Compose 설정
- **setup.sh**: 프로젝트 자동 설정 스크립트

## 데이터 흐름

### 워크플로우 생성
1. 사용자가 WorkflowEditor에서 노드를 추가하고 연결
2. 저장 시 workflowService.js가 데이터를 API 형식으로 변환
3. api.js의 createWorkflow()가 POST /api/workflow/ 호출
4. workflow.py의 create_workflow()가 요청 수신
5. workflow_service.py의 create_workflow()가 비즈니스 로직 실행
6. Workflow, WorkflowNode, WorkflowEdge 모델을 데이터베이스에 저장

### 신청서 실행
1. 사용자가 ApplicationPage에서 신청서 생성 및 실행
2. api.js의 executeApplication()가 POST /api/application/<id>/execute 호출
3. application.py의 execute_application()이 요청 수신
4. engine_service.py의 execute_workflow()가 워크플로우 실행
5. 각 노드를 순회하며 _execute_node() 호출
6. ApplicationLog에 실행 로그 저장
7. Application 모델에 결과 및 점수 업데이트

## 기술 스택 요약

### 백엔드
- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- Flask-CORS 4.0.0
- SQLite

### 프론트엔드
- React 18.2.0
- Material-UI 5.14.20
- ReactFlow 11.10.1
- Axios 1.6.2
- React Router 6.20.1

## 다음 단계

프로젝트를 실행하려면:

```bash
# 1. 설정 스크립트 실행
./setup.sh

# 2. 백엔드 실행
source venv/bin/activate
cd backend
python app.py

# 3. 프론트엔드 실행 (새 터미널)
cd frontend
npm start
```

이제 http://localhost:3000에서 애플리케이션에 접근할 수 있습니다.
