from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Float, Boolean, Text
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
    phone_number = Column(String, nullable=True, unique=True)  # 소셜 로그인 시 null 가능
    email = Column(String, nullable=False, unique=True)
    
    # Enum이 정의되지 않았으므로 임시로 String 사용
    gender = Column(String, nullable=False) 
    birth_year = Column(Integer, nullable=True)
    chess_experience = Column(String, nullable=False) # 임시 String
    chess_rating = Column(String, nullable=True)     # 임시 String
    
    # 💡 재방문 횟수 트래킹을 위해 추가
    total_visits = Column(Integer, default=1, nullable=False) 
    
    # 💡 소셜 로그인 정보
    social_provider = Column(String, nullable=True)  # 'apple', 'kakao', null (일반 로그인)
    social_id = Column(String, nullable=True, unique=True)  # 소셜 제공자의 고유 ID
    
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
    price = Column(Float, nullable=False, default=10000.0)  # 모임 참가비 (기본값: 10,000원)
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
# 5. 결제 모델 (Payment Model)
# --------------------
class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # 결제한 사용자

    # 결제 유형: 'meeting' (모임 등록비) 또는 'membership' (멤버십 구독)
    payment_type = Column(String, nullable=False)

    # 결제 대상 (모임 ID 또는 멤버십 ID)
    meeting_id = Column(Integer, ForeignKey("meetings.id"), nullable=True)  # 모임 결제 시
    membership_id = Column(Integer, ForeignKey("memberships.id"), nullable=True)  # 멤버십 결제 시

    # 결제 금액
    amount = Column(Float, nullable=False)

    # 카카오페이 결제 정보
    tid = Column(String, nullable=True, unique=True)  # 카카오페이 거래 고유번호
    partner_order_id = Column(String, nullable=False, unique=True)  # 가맹점 주문번호
    partner_user_id = Column(String, nullable=False)  # 가맹점 회원 ID

    # 결제 상태: 'ready', 'approved', 'cancelled', 'failed', 'refunded'
    status = Column(String, default="ready", nullable=False)

    # 결제 승인 정보
    aid = Column(String, nullable=True)  # 요청 고유번호 (승인 후)
    payment_method_type = Column(String, nullable=True)  # 결제 수단 (CARD, MONEY 등)

    # 결제 시간
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    approved_at = Column(DateTime, nullable=True)  # 결제 승인 시간
    cancelled_at = Column(DateTime, nullable=True)  # 결제 취소 시간

    # 환불 정보
    refund_reason = Column(Text, nullable=True)
    refund_amount = Column(Float, nullable=True, default=0.0)

    # 관계
    user = relationship("User")
    meeting = relationship("Meeting", foreign_keys=[meeting_id])
    membership = relationship("Membership", foreign_keys=[membership_id])


# --------------------
# 6. 멤버십 구독 모델 (Membership Model)
# --------------------
class Membership(Base):
    __tablename__ = "memberships"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)  # 한 사용자당 하나의 활성 멤버십

    # 멤버십 유형: 'monthly' (월간) 또는 'annual' (연간)
    membership_type = Column(String, nullable=False)

    # 멤버십 상태: 'active', 'cancelled', 'expired'
    status = Column(String, default="active", nullable=False)

    # 멤버십 기간
    start_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_date = Column(DateTime, nullable=False)  # 멤버십 만료일

    # 자동 갱신 여부
    auto_renew = Column(Boolean, default=True, nullable=False)

    # 가격 정보
    price = Column(Float, nullable=False)

    # 생성 및 업데이트 시간
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 관계
    user = relationship("User")
    payments = relationship("Payment", back_populates="membership")


# Payment 모델에 membership relationship 추가
Payment.membership = relationship("Membership", back_populates="payments")


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
