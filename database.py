from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# 데이터베이스 URL 설정
# Railway나 다른 클라우드 환경: /tmp 디렉토리 사용 (쓰기 가능)
# 로컬 환경: 현재 디렉토리 사용
# Railway 환경 감지: RAILWAY_ENVIRONMENT, RAILWAY_STATIC_URL, PORT 등의 변수 확인
is_production = os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("RAILWAY_STATIC_URL") or (os.getenv("PORT") and not os.path.exists("./venv"))

if is_production:
    # Railway/클라우드 환경에서는 /tmp 디렉토리에 SQLite DB 저장
    SQLALCHEMY_DATABASE_URL = "sqlite:////tmp/community_control.db"
    print(f"🌐 Production environment detected - using /tmp for database")
else:
    # 로컬 개발 환경
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./community_control.db")
    print(f"💻 Local environment detected - using local directory for database")

# DB 엔진 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    # SQLite 사용 시 필수 옵션
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)

# 세션 생성기
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모델 정의를 위한 기본 클래스
Base = declarative_base()

# --------------------
# 1. 사용자 모델 (User Model)
# --------------------
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    
    # Enum이 정의되지 않았으므로 임시로 String 사용
    gender = Column(String, nullable=False) 
    birth_year = Column(Integer, nullable=True)
    chess_experience = Column(String, nullable=False) # 임시 String
    chess_rating = Column(String, nullable=True)     # 임시 String
    
    # 💡 재방문 횟수 트래킹을 위해 추가
    total_visits = Column(Integer, default=1, nullable=False) 
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 관계: User와 Meeting의 다대다 관계
    meetings = relationship("UserMeeting", back_populates="user")

# --------------------
# 2. 인증 코드 모델 (Verification Code Model)
# --------------------
class VerificationCode(Base):
    __tablename__ = "verification_codes"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, index=True, nullable=False)
    code = Column(String, nullable=False)
    # 💡 쿨다운 로직을 위해 추가된 필드: 코드가 생성된 시간 기록
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False) 
    expires_at = Column(DateTime, nullable=False)


# --------------------
# 3. 모임 모델 (Meeting Model)
# --------------------
class Meeting(Base):
    __tablename__ = "meetings"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)  # 모임 제목
    date_time = Column(DateTime, nullable=False)  # 모임 날짜 및 시간
    location = Column(String, nullable=False)  # 모임 장소
    capacity = Column(Integer, nullable=False)  # 정원
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 관계: Meeting과 User의 다대다 관계
    participants = relationship("UserMeeting", back_populates="meeting")


# --------------------
# 4. 사용자-모임 연결 모델 (UserMeeting Model)
# --------------------
class UserMeeting(Base):
    __tablename__ = "user_meetings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # User 테이블 외래키
    meeting_id = Column(Integer, ForeignKey("meetings.id"), nullable=False)  # Meeting 테이블 외래키
    status = Column(String, default="CONFIRMED", nullable=False)  # 참가 상태 (CONFIRMED, CANCELLED)
    registered_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # 관계 정의
    user = relationship("User", back_populates="meetings")
    meeting = relationship("Meeting", back_populates="participants")


# --------------------
# 데이터베이스 초기화 및 유틸리티 함수
# --------------------
def init_db():
    """데이터베이스에 정의된 모든 테이블을 생성합니다."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

# FastAPI의 의존성 주입(Dependency Injection)을 위한 함수 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
