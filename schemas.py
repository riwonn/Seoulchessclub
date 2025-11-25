from __future__ import annotations
from enum import Enum
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class GenderEnum(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"

class ChessExperienceEnum(str, Enum):
    NO_BUT_WANT_TO_LEARN = "NO_BUT_WANT_TO_LEARN"
    KNOW_RULES_ONLY = "KNOW_RULES_ONLY"
    OCCASIONALLY_PLAY = "OCCASIONALLY_PLAY"
    PLAY_WELL = "PLAY_WELL"

class ChessRatingEnum(str, Enum):
    I_DONT_KNOW = "I_DONT_KNOW"
    UNDER_1000 = "UNDER_1000"
    BETWEEN_1000_1500 = "BETWEEN_1000_1500"
    BETWEEN_1500_2000 = "BETWEEN_1500_2000"
    OVER_2000 = "OVER_2000"

class SMSRequest(BaseModel):
    phone_number: str

class SMSVerify(BaseModel):
    phone_number: str
    code: str

class UserRegistration(BaseModel):
    name: str
    phone_number: str
    email: str
    gender: GenderEnum
    birth_year: Optional[int] = None
    chess_experience: ChessExperienceEnum
    chess_rating: Optional[ChessRatingEnum] = None

class IntentEnum(str, Enum):
    GREETING = "GREETING"
    QUESTION = "QUESTION"
    COMPLAINT = "COMPLAINT"
    REQUEST = "REQUEST"
    COMPLIMENT = "COMPLIMENT"
    APOLOGY = "APOLOGY"
    THANK_YOU = "THANK_YOU"
    GOODBYE = "GOODBYE"
    OTHER = "OTHER"

class EntityEnum(str, Enum):
    PERSON = "PERSON"
    PRODUCT = "PRODUCT"
    SERVICE = "SERVICE"
    LOCATION = "LOCATION"
    TIME = "TIME"
    DATE = "DATE"
    NUMBER = "NUMBER"
    EMAIL = "EMAIL"
    PHONE = "PHONE"
    URL = "URL"
    OTHER = "OTHER"

class CSParseRequest(BaseModel):
    text: str

class CSParseResponse(BaseModel):
    intent: IntentEnum
    entities: List[dict] = []
    confidence: float
    original_text: str
    processed_at: str

class UserCreate(BaseModel):
    name: str
    phone_number: str
    email: str
    gender: GenderEnum
    birth_year: Optional[int] = None
    chess_experience: ChessExperienceEnum
    chess_rating: Optional[ChessRatingEnum] = None

class UserOut(BaseModel):
    id: int
    name: str
    phone_number: Optional[str] = None
    email: str
    gender: str
    birth_year: Optional[int] = None
    chess_experience: str
    chess_rating: Optional[str] = None
    total_visits: int
    social_provider: Optional[str] = None
    social_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    attended_meetings: List[UserMeetingOut] = []  # 사용자가 참여한 모임 목록
    
    class Config:
        from_attributes = True


# --------------------
# Meeting 관련 스키마
# --------------------
class MeetingBase(BaseModel):
    """모임 기본 스키마"""
    title: str
    date_time: datetime
    location: str
    capacity: int
    price: float = 10000.0  # 모임 참가비 (기본값: 10,000원)


class MeetingCreate(MeetingBase):
    """모임 생성 스키마"""
    pass


class MeetingOut(MeetingBase):
    """모임 출력 스키마 (참가자 목록 포함)"""
    id: int
    created_at: datetime
    participants: List[UserMeetingOut] = []  # 모임에 참여한 사용자 목록

    class Config:
        from_attributes = True


# --------------------
# UserMeeting 관련 스키마
# --------------------
class UserMeetingInterest(BaseModel):
    """모임 관심 등록 입력 스키마 (결제 의사 표시)"""
    user_id: int
    meeting_id: int


class UserMeetingOut(BaseModel):
    """사용자-모임 연결 출력 스키마"""
    id: int
    user_id: int
    meeting_id: int
    status: str
    registered_at: datetime
    
    class Config:
        from_attributes = True


# --------------------
# 인증 관련 스키마
# --------------------
class LoginRequest(BaseModel):
    """로그인 요청 스키마 (전화번호 + SMS 인증 후 로그인)"""
    phone_number: str


class LoginResponse(BaseModel):
    """로그인 응답 스키마"""
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class TokenData(BaseModel):
    """JWT 토큰 페이로드 스키마"""
    user_id: Optional[int] = None
    phone_number: Optional[str] = None


# --------------------
# 소셜 로그인 관련 스키마
# --------------------
class AdminLoginRequest(BaseModel):
    """관리자 코드 기반 로그인 요청 스키마"""
    code: str

class AppleLoginRequest(BaseModel):
    """Apple 로그인 요청 스키마"""
    identity_token: str  # Apple에서 받은 ID 토큰
    authorization_code: str  # Apple에서 받은 인증 코드
    user_info: Optional[dict] = None  # 첫 로그인 시 제공되는 사용자 정보


class KakaoLoginRequest(BaseModel):
    """카카오 로그인 요청 스키마"""
    access_token: str  # 카카오에서 받은 액세스 토큰


class SocialLoginResponse(BaseModel):
    """소셜 로그인 응답 스키마"""
    access_token: str
    token_type: str = "bearer"
    user: UserOut
    is_new_user: bool  # 신규 가입 여부


# --------------------
# 챗봇 관련 스키마
# --------------------
class ChatMessage(BaseModel):
    """챗봇 메시지 스키마"""
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    """챗봇 요청 스키마"""
    message: str
    conversation_history: List[ChatMessage] = []


class ChatResponse(BaseModel):
    """챗봇 응답 스키마"""
    response: str
    timestamp: datetime


# --------------------
# 결제 관련 스키마 (Payment Schemas)
# --------------------
class PaymentTypeEnum(str, Enum):
    MEETING = "meeting"
    MEMBERSHIP = "membership"


class PaymentStatusEnum(str, Enum):
    READY = "ready"
    APPROVED = "approved"
    CANCELLED = "cancelled"
    FAILED = "failed"
    REFUNDED = "refunded"


class MembershipTypeEnum(str, Enum):
    MONTHLY = "monthly"
    ANNUAL = "annual"


class PaymentCreateRequest(BaseModel):
    """결제 생성 요청 스키마"""
    payment_type: PaymentTypeEnum
    meeting_id: Optional[int] = None  # 모임 결제 시 필수
    membership_type: Optional[MembershipTypeEnum] = None  # 멤버십 결제 시 필수
    amount: float


class KakaoPayReadyResponse(BaseModel):
    """카카오페이 결제 준비 응답 스키마"""
    tid: str  # 결제 고유번호
    next_redirect_pc_url: str  # PC 웹 결제 URL
    next_redirect_mobile_url: str  # 모바일 웹 결제 URL
    next_redirect_app_url: str  # 앱 결제 URL
    partner_order_id: str
    created_at: datetime


class KakaoPayApproveRequest(BaseModel):
    """카카오페이 결제 승인 요청 스키마"""
    pg_token: str  # 카카오페이에서 리다이렉트 시 전달되는 토큰
    partner_order_id: str


class KakaoPayApproveResponse(BaseModel):
    """카카오페이 결제 승인 응답 스키마"""
    aid: str  # 요청 고유번호
    tid: str  # 결제 고유번호
    partner_order_id: str
    partner_user_id: str
    payment_method_type: str  # 결제 수단 (CARD, MONEY 등)
    amount: dict  # 결제 금액 정보
    item_name: str
    approved_at: datetime
    status: str


class PaymentCancelRequest(BaseModel):
    """결제 취소 요청 스키마"""
    payment_id: int
    cancel_reason: str


class PaymentRefundRequest(BaseModel):
    """환불 요청 스키마"""
    payment_id: int
    refund_amount: float
    refund_reason: str


class PaymentOut(BaseModel):
    """결제 출력 스키마"""
    id: int
    user_id: int
    payment_type: str
    meeting_id: Optional[int] = None
    membership_id: Optional[int] = None
    amount: float
    status: str
    partner_order_id: str
    tid: Optional[str] = None
    created_at: datetime
    approved_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MembershipOut(BaseModel):
    """멤버십 출력 스키마"""
    id: int
    user_id: int
    membership_type: str
    status: str
    start_date: datetime
    end_date: datetime
    auto_renew: bool
    price: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MembershipCreateRequest(BaseModel):
    """멤버십 생성 요청 스키마"""
    membership_type: MembershipTypeEnum
