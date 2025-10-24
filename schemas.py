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
    phone_number: str
    email: str
    gender: str
    birth_year: Optional[int] = None
    chess_experience: str
    chess_rating: Optional[str] = None
    total_visits: int
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
