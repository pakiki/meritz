# Meritz 개인신용평가 워크플로우 시스템

React + Python Flask 기반의 데스크톱 웹 애플리케이션으로, 개인신용평가를 위한 워크플로우를 시각적으로 설계하고 실행할 수 있는 시스템입니다.

## 기술 스택

### Backend
- **Python 3.x**
- **Flask 3.0.0** - 웹 프레임워크
- **Flask-SQLAlchemy** - ORM
- **SQLite** - 데이터베이스
- **Flask-CORS** - CORS 지원

### Frontend
- **React 18.2.0** - UI 프레임워크
- **Material-UI (MUI)** - UI 컴포넌트 라이브러리
- **ReactFlow** - 워크플로우 시각화 및 에디터
- **Axios** - HTTP 클라이언트
- **React Router** - 라우팅

## 프로젝트 구조

```
meritz/
├── backend/                 # Python Flask 백엔드
│   ├── app.py              # Flask 메인 애플리케이션
│   ├── config.py           # 설정 파일
│   ├── database.py         # 데이터베이스 설정
│   ├── requirements.txt    # Python 의존성
│   ├── routes/             # API 라우트
│   │   ├── workflow.py     # 워크플로우 API
│   │   ├── application.py  # 신청서 API
│   │   └── engine.py       # 엔진 API
│   ├── models/             # 데이터 모델
│   │   ├── workflow.py     # 워크플로우 모델
│   │   ├── application.py  # 신청서 모델
│   │   └── rule.py         # 규칙 모델
│   ├── services/           # 비즈니스 로직
│   │   ├── workflow_service.py
│   │   ├── engine_service.py
│   │   └── scoring_service.py
│   └── utils/              # 유틸리티
│       └── validators.py
│
├── frontend/               # React 프론트엔드
│   ├── public/
│   ├── src/
│   │   ├── components/     # React 컴포넌트
│   │   ├── pages/          # 페이지 컴포넌트
│   │   ├── services/       # API 서비스
│   │   ├── styles/         # 스타일시트
│   │   └── utils/          # 유틸리티
│   └── package.json
│
├── database/               # 데이터베이스
│   ├── schema.sql         # SQLite 스키마
│   └── meritz.db          # SQLite 데이터베이스 파일 (생성됨)
│
├── .env                    # 환경 변수
├── requirements.txt        # 전체 Python 의존성
└── docker-compose.yml      # Docker 설정
```

## 설치 및 실행

### 사전 요구사항
- Python 3.8 이상
- Node.js 16 이상
- npm 또는 yarn

### 1. 프로젝트 클론

```bash
git clone <repository-url>
cd meritz
```

### 2. 백엔드 설정 및 실행

```bash
# 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# Flask 서버 실행
cd backend
python app.py
```

백엔드 서버는 `http://localhost:5000`에서 실행됩니다.

### 3. 프론트엔드 설정 및 실행

```bash
# 새 터미널에서
cd frontend

# 의존성 설치
npm install

# React 개발 서버 실행
npm start
```

프론트엔드 애플리케이션은 `http://localhost:3000`에서 실행됩니다.

### Docker를 사용한 실행 (선택사항)

```bash
docker-compose up
```

## 주요 기능

### 1. 워크플로우 에디터
- 드래그 앤 드롭 방식의 시각적 워크플로우 설계
- 다양한 노드 타입 지원:
  - **시작 노드**: 워크플로우 시작점
  - **종료 노드**: 워크플로우 종료점
  - **의사결정 노드**: 조건부 분기
  - **점수 계산 노드**: 신용 점수 계산
  - **API 호출 노드**: 외부 API 연동

### 2. 신청서 관리
- 개인 신용평가 신청서 생성
- 신청 정보 입력:
  - 신청자 정보
  - 연소득
  - 신용 이력
  - 부채 비율
  - 재직 기간

### 3. 워크플로우 실행 엔진
- 설계된 워크플로우에 따라 신청서 자동 처리
- 실시간 실행 로그 모니터링
- 노드별 실행 결과 추적

### 4. 신용 점수 계산
- 다양한 요소를 고려한 신용 점수 산출
- 1-10등급의 신용 등급 평가

### 5. 대시보드
- 전체 워크플로우 및 신청서 현황
- 최근 활동 내역
- 통계 정보

## API 엔드포인트

### Workflow API
- `GET /api/workflow/` - 모든 워크플로우 조회
- `GET /api/workflow/<id>` - 특정 워크플로우 조회
- `POST /api/workflow/` - 워크플로우 생성
- `PUT /api/workflow/<id>` - 워크플로우 업데이트
- `DELETE /api/workflow/<id>` - 워크플로우 삭제
- `POST /api/workflow/<id>/validate` - 워크플로우 검증

### Application API
- `GET /api/application/` - 모든 신청서 조회
- `GET /api/application/<id>` - 특정 신청서 조회
- `POST /api/application/` - 신청서 생성
- `POST /api/application/<id>/execute` - 신청서 실행
- `GET /api/application/<id>/logs` - 실행 로그 조회

### Engine API
- `GET /api/engine/rules` - 모든 규칙 조회
- `POST /api/engine/rules` - 규칙 생성
- `PUT /api/engine/rules/<id>` - 규칙 업데이트
- `DELETE /api/engine/rules/<id>` - 규칙 삭제
- `POST /api/engine/score` - 신용 점수 계산

## 데이터베이스 스키마

### workflows
워크플로우 정의 정보

### workflow_nodes
워크플로우 내 노드 정보

### workflow_edges
노드 간 연결 정보

### rules
평가 규칙 정보

### applications
신청서 정보

### application_logs
신청서 실행 로그

## 개발

### 코드 스타일
- Backend: PEP 8 가이드라인 준수
- Frontend: ESLint + React 표준

### 테스트
```bash
# Backend 테스트
pytest

# Frontend 테스트
npm test
```

## 라이선스

MIT License

## 기여

이슈와 풀 리퀘스트를 환영합니다.

## 연락처

프로젝트 관련 문의사항은 이슈 트래커를 이용해주세요.
