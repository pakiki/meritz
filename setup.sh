#!/bin/bash

# Meritz 워크플로우 시스템 설정 스크립트

echo "==================================="
echo "Meritz 워크플로우 시스템 설정"
echo "==================================="
echo ""

# 1. Python 가상환경 생성
echo "1. Python 가상환경 생성 중..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ 가상환경이 생성되었습니다."
else
    echo "✓ 가상환경이 이미 존재합니다."
fi

# 2. 가상환경 활성화
echo ""
echo "2. 가상환경 활성화 중..."
source venv/bin/activate

# 3. Python 의존성 설치
echo ""
echo "3. Python 의존성 설치 중..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✓ Python 패키지가 설치되었습니다."

# 4. 데이터베이스 디렉토리 확인
echo ""
echo "4. 데이터베이스 디렉토리 확인 중..."
mkdir -p database
echo "✓ 데이터베이스 디렉토리가 준비되었습니다."

# 5. Frontend 의존성 설치
echo ""
echo "5. Frontend 의존성 설치 중..."
cd frontend
if [ ! -d "node_modules" ]; then
    npm install
    echo "✓ Node.js 패키지가 설치되었습니다."
else
    echo "✓ Node.js 패키지가 이미 설치되어 있습니다."
fi
cd ..

echo ""
echo "==================================="
echo "설정 완료!"
echo "==================================="
echo ""
echo "실행 방법:"
echo ""
echo "1. 백엔드 서버 실행:"
echo "   source venv/bin/activate"
echo "   cd backend"
echo "   python app.py"
echo ""
echo "2. 프론트엔드 서버 실행 (새 터미널):"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "3. 브라우저에서 접속:"
echo "   http://localhost:3000"
echo ""
