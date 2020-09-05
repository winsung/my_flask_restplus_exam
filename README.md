### Python 3.7.6 에서 개발
 > virtualenv venv --python=3.7
 > source ./venv/bin/activate

### 필요 라이브러리 설치
 > pip -r install requirements.txt

### 마이그레이션 Alembic 사용
 > vi alembic.ini
38번째 줄 [sqlalchemy.url] 내용을 postgres 환경에 맞게 설정
 > alembic upgrade head

### Application Config 수정
 > vi config.py
안의 HOST, PORT, ID, PW, DB 값을 postgres 환경에 맞게 설정

### 실행
 > python app.py