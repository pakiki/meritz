# Meritz 워크플로우 시스템 - 빠른 시작 가이드

## 📋 사전 요구사항

시스템에 다음 소프트웨어가 설치되어 있어야 합니다:

- **Python 3.8 이상**
- **Node.js 16 이상**
- **npm** (Node.js와 함께 설치됨)

설치 확인:
```bash
python3 --version
node --version
npm --version
```

## 🚀 빠른 시작

### 방법 1: 자동 설정 스크립트 사용 (권장)

```bash
# 1. 설정 스크립트 실행
./setup.sh

# 2. 백엔드 실행
source venv/bin/activate
cd backend
python app.py

# 3. 새 터미널에서 프론트엔드 실행
cd frontend
npm start
```

### 방법 2: 수동 설정

#### 백엔드 설정

```bash
# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate  # Windows

# 의존성 설치
pip install -r requirements.txt

# Flask 서버 실행
cd backend
python app.py
```

백엔드가 http://localhost:5000 에서 실행됩니다.

#### 프론트엔드 설정

```bash
# 새 터미널 열기
cd frontend

# 의존성 설치
npm install

# React 개발 서버 실행
npm start
```

프론트엔드가 http://localhost:3000 에서 실행되며, 자동으로 브라우저가 열립니다.

## 🎯 첫 워크플로우 생성하기

1. 브라우저에서 http://localhost:3000 접속
2. **"새 워크플로우"** 버튼 클릭
3. 워크플로우 이름과 설명 입력
4. 왼쪽 팔레트에서 노드를 드래그하여 캔버스에 추가:
   - **시작 노드** (초록색)
   - **점수 계산 노드** (파란색)
   - **의사결정 노드** (주황색)
   - **종료 노드** (빨간색)
5. 노드를 클릭하고 드래그하여 연결
6. **저장** 버튼 클릭

## 📝 첫 신청서 생성 및 실행하기

1. 대시보드로 돌아가기
2. **"새 신청서"** 버튼 클릭
3. 워크플로우 선택
4. 신청자 정보 입력:
   - 이름
   - 식별번호
   - 연소득
   - 신용 이력
   - 부채 비율
   - 재직 기간
5. **"신청서 생성"** 버튼 클릭
6. 생성된 신청서 페이지에서 **"실행"** 버튼 클릭
7. 오른쪽 패널에서 실행 로그 확인

## 🔧 문제 해결

### 백엔드가 시작되지 않음

```bash
# 가상환경이 활성화되었는지 확인
which python  # /path/to/meritz/venv/bin/python 이어야 함

# 의존성 재설치
pip install -r requirements.txt

# 포트가 이미 사용 중인지 확인
lsof -i :5000  # Mac/Linux
# 사용 중이면 프로세스 종료 또는 .env 파일에서 포트 변경
```

### 프론트엔드가 시작되지 않음

```bash
# node_modules 삭제 후 재설치
rm -rf node_modules
npm install

# 캐시 정리
npm cache clean --force
```

### CORS 오류

`.env` 파일에서 CORS 설정 확인:
```
REACT_APP_API_URL=http://localhost:5000/api
```

### 데이터베이스 오류

```bash
# 데이터베이스 재생성
rm database/meritz.db
cd backend
python app.py  # 자동으로 새 DB 생성
```

## 📚 추가 리소스

- **프로젝트 구조**: `PROJECT_STRUCTURE.md` 참조
- **상세 README**: `README.md` 참조
- **API 문서**: 백엔드 실행 후 http://localhost:5000/api/health 확인

## 🐳 Docker를 사용한 실행 (선택사항)

```bash
# Docker Compose로 전체 스택 실행
docker-compose up

# 백그라운드 실행
docker-compose up -d

# 종료
docker-compose down
```

## 💡 개발 팁

### 백엔드 디버깅
- Flask는 기본적으로 디버그 모드로 실행됩니다
- 코드 변경 시 자동으로 재시작됩니다
- 에러 발생 시 터미널에 상세한 스택 트레이스가 표시됩니다

### 프론트엔드 디버깅
- 브라우저 개발자 도구 (F12) 사용
- React DevTools 확장 프로그램 설치 권장
- 코드 변경 시 핫 리로드 지원

### API 테스트
```bash
# curl로 API 테스트
curl http://localhost:5000/api/health

# 워크플로우 목록 조회
curl http://localhost:5000/api/workflow/
```

## 🎉 완료!

이제 Meritz 워크플로우 시스템을 사용할 준비가 되었습니다!

문제가 발생하면 GitHub Issues를 통해 문의해주세요.
