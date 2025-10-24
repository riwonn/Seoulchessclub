from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request
import uvicorn
from twilio.rest import Client
import os
from datetime import datetime, timedelta
import random
from dotenv import load_dotenv
from sqlalchemy.orm import Session, joinedload
from database import VerificationCode, SessionLocal, User, Meeting, UserMeeting, get_db, init_db
from schemas import SMSRequest, SMSVerify, UserCreate, UserOut, CSParseRequest, CSParseResponse, MeetingCreate, MeetingOut, UserMeetingInterest
from sqlalchemy.exc import IntegrityError # 데이터베이스 무결성 오류 처리용
import json
import google.generativeai as genai

# .env 파일 로드
load_dotenv()

# Twilio 클라이언트 초기화
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# FastAPI 앱 인스턴스 생성
app = FastAPI(title="Community Control AI", version="1.0.0")

# 클라이언트 초기화 시 환경 변수 누락 확인
if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN or not TWILIO_PHONE_NUMBER:
    print("WARNING: Twilio environment variables are not fully set.")
    # 실제 운영 환경에서는 앱이 시작되지 않도록 처리하는 것이 좋지만, 여기서는 경고만 표시
    twilio_client = None 
else:
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Gemini API 설정
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY environment variable is not set.")
    genai_client = None
else:
    genai.configure(api_key=GEMINI_API_KEY)
    genai_client = genai.GenerativeModel('gemini-2.0-flash-exp')

# FastAPI 앱 인스턴스 생성
app = FastAPI(title="Community Control AI", version="1.0.0")

# 앱 시작 시 데이터베이스 초기화
@app.on_event("startup")
async def startup_event():
    """앱 시작 시 데이터베이스 테이블 생성"""
    try:
        print("=" * 60)
        print("🚀 Starting Community Control AI Application...")
        print(f"📁 Current working directory: {os.getcwd()}")
        print(f"📂 Directory contents: {os.listdir('.')}")
        print(f"🌍 Environment Variables:")
        print(f"  - RAILWAY_ENVIRONMENT: {os.getenv('RAILWAY_ENVIRONMENT', 'Not set')}")
        print(f"  - RAILWAY_STATIC_URL: {os.getenv('RAILWAY_STATIC_URL', 'Not set')}")
        print(f"  - PORT: {os.getenv('PORT', 'Not set')}")
        print(f"  - Static dir exists: {os.path.exists('static')}")
        print(f"  - Templates dir exists: {os.path.exists('templates')}")
        print("=" * 60)
        init_db()
        print("✅ Database initialized successfully!")
        print("=" * 60)
    except Exception as e:
        print(f"❌ Error during startup: {str(e)}")
        import traceback
        traceback.print_exc()
        raise

# Static 파일 서빙 (디렉토리 존재 확인)
try:
    if os.path.exists("static"):
        app.mount("/static", StaticFiles(directory="static"), name="static")
        print("✅ Static files mounted successfully")
    else:
        print("⚠️  Warning: 'static' directory not found")
except Exception as e:
    print(f"⚠️  Warning: Could not mount static files: {str(e)}")

# Jinja2 템플릿 설정
try:
    templates = Jinja2Templates(directory="templates")
    print("✅ Templates configured successfully")
except Exception as e:
    print(f"❌ Error configuring templates: {str(e)}")
    templates = None

@app.get("/health")
async def health_check():
    """Health check endpoint for Railway"""
    return {"status": "healthy", "service": "Community Control AI"}

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Root endpoint - landing page"""
    if templates is None:
        return HTMLResponse(content="<h1>Community Control AI</h1><p>Templates not configured. Check deployment logs.</p>")
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    """운영자 대시보드 페이지"""
    # 모든 사용자 조회
    users = db.query(User).all()
    return templates.TemplateResponse("dashboard.html", {"request": request, "users": users})

@app.get("/register_form", response_class=HTMLResponse)
async def register_form(request: Request):
    """사용자 등록 폼 페이지"""
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/meetings_list", response_class=HTMLResponse)
async def meetings_list(request: Request, db: Session = Depends(get_db)):
    """모임 목록 페이지 - 모든 활성화된 모임을 표시"""
    # 모든 활성화된 모임 조회
    meetings = db.query(Meeting).all()
    return templates.TemplateResponse("meetings_list.html", {"request": request, "meetings": meetings})

@app.get("/get_user_by_phone", response_model=UserOut)
async def get_user_by_phone(phone_number: str, db: Session = Depends(get_db)):
    """
    전화번호로 사용자 조회 API - 재방문 고객 인식용
    쿼리 파라미터로 phone_number를 받아 사용자를 조회합니다.
    사용자가 없으면 404 에러를 반환합니다.
    attended_meetings 리스트도 함께 반환합니다.
    """
    # 전화번호로 사용자 검색 (attended_meetings 관계 포함)
    user = db.query(User).options(joinedload(User.meetings)).filter(User.phone_number == phone_number).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

@app.post("/sms/request")
async def send_sms(request: SMSRequest, db: Session = Depends(get_db)):
    """SMS verification code request API: generates, saves, and sends the code."""
    
    # 1. Generate 6-digit random verification code
    verification_code = str(random.randint(100000, 999999))
    
    try:
        # --- DB TRANSACTION START: CHECK COOL-DOWN AND SAVE NEW CODE ---
        
        # 1.1. Check Cool-down period and clean up existing records
        existing_records = db.query(VerificationCode).filter(
            VerificationCode.phone_number == request.phone_number
        ).all()

        if existing_records:
            # Check if any existing record is within cooldown period
            for record in existing_records:
                time_since_creation = datetime.utcnow() - record.created_at
                
                # If requested too soon (within 30 seconds)
                if time_since_creation < timedelta(seconds=30):
                    remaining_time = 30 - int(time_since_creation.total_seconds())
                    raise HTTPException(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail=f"Please wait {remaining_time} seconds before requesting a new code."
                    )
            
            # Delete all existing records for this phone number
            for record in existing_records:
                db.delete(record)
            
        # 1.2. Save new verification code record (5 minutes expiry)
        verification_record = VerificationCode(
            phone_number=request.phone_number,
            code=verification_code,
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(minutes=5)
        )
        db.add(verification_record)
        db.commit()
        db.refresh(verification_record)
        
    except HTTPException:
        # Re-raise explicit HTTP exceptions (e.g., 429)
        raise
    except Exception as e:
        # Handle DB/Internal errors
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal database error during code request: {str(e)}"
        )
        
    # 2. SEND SMS (ONLY after successful DB save)
    # 국가코드 자동 추가 (한국: +82)
    phone_number = request.phone_number.strip()
    
    # 이미 +로 시작하는 경우 그대로 사용
    if phone_number.startswith('+'):
        formatted_number = phone_number
    # 010으로 시작하는 경우 +82로 변환
    elif phone_number.startswith('010'):
        formatted_number = f"+82{phone_number[1:]}"
    # 82로 시작하는 경우 + 추가
    elif phone_number.startswith('82'):
        formatted_number = f"+{phone_number}"
    # 그 외의 경우 +82 추가
    else:
        formatted_number = f"+82{phone_number}"
    
    # 개발 환경에서는 Twilio 없이도 테스트 가능하도록 모킹
    print(f"[개발 모드] SMS 모킹: {formatted_number}로 인증 코드 {verification_code} 전송됨")
    
    # 3. Return success response
    return {"message": "SMS sent successfully"}

@app.post("/sms/verify")
async def verify_sms(request: SMSVerify, db: Session = Depends(get_db)):
    """SMS verification code verification API"""
    try:
        # 1. Find matching VerificationCode record in DB
        verification_record = db.query(VerificationCode).filter(
            VerificationCode.phone_number == request.phone_number,
            VerificationCode.code == request.code
        ).first()
        
        # 2. If code is not found or is invalid
        if not verification_record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Verification code is invalid or does not exist."
            )
        
        # 3. Check if code has expired (5 minutes)
        if datetime.utcnow() > verification_record.expires_at:
            # Delete expired code
            db.delete(verification_record)
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Verification code has expired."
            )
        
        # 4. Delete VerificationCode record after successful verification
        # 이 시점에서 인증이 성공했고, verification_record가 삭제됩니다.
        db.delete(verification_record)
        db.commit()
        
        return {"message": "Verification successful."}
            
    except HTTPException:
        # Re-raise explicit HTTP exceptions
        raise
    except Exception as e:
        # Handle DB/Internal errors
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error during verification: {str(e)}"
        )


# =========================================================================
# 💡 3. 사용자 등록 엔드포인트 (/register)
# =========================================================================
@app.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    사용자 등록 API (순수 회원 가입 기능만 수행).
    모임 신청은 별도의 /meetings/register 엔드포인트를 사용합니다.
    """
    # 1. 자동 마감 로직 - 최대 30명 제한
    MAX_CAPACITY = 30
    current_count = db.query(User).count()
    if current_count >= MAX_CAPACITY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Registration is closed. Maximum capacity of {MAX_CAPACITY} users reached."
        )

    # 2. 전화번호로 기존 사용자 조회
    existing_user = db.query(User).filter(User.phone_number == user_data.phone_number).first()

    # 4. 트랜잭션으로 사용자 등록/업데이트 처리
    try:
        if existing_user:
            # 기존 사용자: 필드 업데이트 및 total_visits 1 증가
            existing_user.name = user_data.name
            existing_user.email = user_data.email
            existing_user.gender = user_data.gender
            existing_user.birth_year = user_data.birth_year
            existing_user.chess_experience = user_data.chess_experience
            existing_user.chess_rating = user_data.chess_rating
            existing_user.total_visits += 1
            existing_user.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(existing_user)
            return existing_user
        else:
            # 신규 사용자: total_visits를 1로 설정하여 새 레코드 생성
            new_user = User(
                name=user_data.name,
                phone_number=user_data.phone_number,
                email=user_data.email,
                gender=user_data.gender,
                birth_year=user_data.birth_year,
                chess_experience=user_data.chess_experience,
                chess_rating=user_data.chess_rating,
                total_visits=1
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
            
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Registration failed due to a database integrity constraint (phone or email duplication)."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during registration: {str(e)}"
        )

@app.post("/parse_cs", response_model=CSParseResponse)
async def parse_cs_text(request: CSParseRequest):
    """
    CS 텍스트를 구조화된 JSON 형태로 파싱하는 API
    Gemini API를 사용하여 고객 문의의 의도와 엔티티를 분석합니다.
    """
    # API 키 확인
    if not genai_client:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Gemini API key is not configured. Please set GEMINI_API_KEY environment variable."
        )
    
    try:
        # 간단한 프롬프트로 시작
        prompt = f"""
        다음 고객 서비스 텍스트를 분석해주세요: "{request.text}"
        
        다음 JSON 형식으로 응답해주세요:
        {{
            "intent": "GREETING",
            "entities": [],
            "confidence": 0.9,
            "original_text": "{request.text}",
            "processed_at": "{datetime.utcnow().isoformat()}"
        }}
        
        intent는 다음 중 하나여야 합니다: GREETING, QUESTION, COMPLAINT, REQUEST, COMPLIMENT, APOLOGY, THANK_YOU, GOODBYE, OTHER
        """
        
        # Gemini API 호출
        response = genai_client.generate_content(prompt)
        
        # 응답 텍스트에서 JSON 추출
        response_text = response.text.strip()
        
        # JSON 부분만 추출 (```json ... ``` 형태일 수 있음)
        if "```json" in response_text:
            json_start = response_text.find("```json") + 7
            json_end = response_text.find("```", json_start)
            response_text = response_text[json_start:json_end].strip()
        elif "```" in response_text:
            json_start = response_text.find("```") + 3
            json_end = response_text.find("```", json_start)
            response_text = response_text[json_start:json_end].strip()
        
        # JSON 파싱
        response_data = json.loads(response_text)
        
        # CSParseResponse 객체 생성
        parse_response = CSParseResponse(
            intent=response_data.get("intent", "OTHER"),
            entities=response_data.get("entities", []),
            confidence=response_data.get("confidence", 0.5),
            original_text=response_data.get("original_text", request.text),
            processed_at=response_data.get("processed_at", datetime.utcnow().isoformat())
        )
        
        return parse_response
        
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to parse Gemini API response as JSON: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing CS text: {str(e)}"
        )


# =========================================================================
# 💡 4. 모임 관련 엔드포인트
# =========================================================================

@app.post("/meetings/create", response_model=MeetingOut, status_code=status.HTTP_201_CREATED)
async def create_meeting(meeting_data: MeetingCreate, db: Session = Depends(get_db)):
    """
    새 모임 생성 API (운영자용).
    모임 제목, 날짜/시간, 장소, 정원을 받아 새 모임을 생성합니다.
    """
    try:
        new_meeting = Meeting(
            title=meeting_data.title,
            date_time=meeting_data.date_time,
            location=meeting_data.location,
            capacity=meeting_data.capacity
        )
        
        db.add(new_meeting)
        db.commit()
        db.refresh(new_meeting)
        
        return new_meeting
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating meeting: {str(e)}"
        )


@app.get("/meetings", response_model=list[MeetingOut])
async def get_all_meetings(db: Session = Depends(get_db)):
    """
    모든 활성화된 모임 리스트를 반환하는 API.
    participants 관계를 포함하여 각 모임의 참가자 정보도 함께 반환합니다.
    """
    try:
        meetings = db.query(Meeting).options(joinedload(Meeting.participants)).all()
        return meetings
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching meetings: {str(e)}"
        )


@app.post("/meetings/register", status_code=status.HTTP_201_CREATED)
async def register_for_meeting(user_id: int, meeting_id: int, db: Session = Depends(get_db)):
    """
    모임 참가 신청 API.
    user_id와 meeting_id를 받아 UserMeeting 테이블에 참가 기록을 생성합니다.
    """
    try:
        # 1. 사용자 존재 확인
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        
        # 2. 모임 존재 확인
        meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
        if not meeting:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Meeting with id {meeting_id} not found"
            )
        
        # 3. 이미 참가 신청했는지 확인
        existing_registration = db.query(UserMeeting).filter(
            UserMeeting.user_id == user_id,
            UserMeeting.meeting_id == meeting_id
        ).first()
        
        if existing_registration:
            # 이미 참가 신청한 경우, 상태가 CANCELLED면 CONFIRMED로 변경
            if existing_registration.status == "CANCELLED":
                existing_registration.status = "CONFIRMED"
                existing_registration.registered_at = datetime.utcnow()
                db.commit()
                return {
                    "message": "Meeting registration reactivated successfully",
                    "registration_id": existing_registration.id
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User is already registered for this meeting"
                )
        
        # 4. 모임 정원 확인
        current_participants = db.query(UserMeeting).filter(
            UserMeeting.meeting_id == meeting_id,
            UserMeeting.status == "CONFIRMED"
        ).count()
        
        if current_participants >= meeting.capacity:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Meeting is full. Capacity: {meeting.capacity}"
            )
        
        # 5. 새로운 참가 기록 생성
        new_registration = UserMeeting(
            user_id=user_id,
            meeting_id=meeting_id,
            status="CONFIRMED",
            registered_at=datetime.utcnow()
        )
        
        db.add(new_registration)
        db.commit()
        db.refresh(new_registration)
        
        return {
            "message": "Meeting registration successful",
            "registration_id": new_registration.id,
            "user_id": user_id,
            "meeting_id": meeting_id,
            "status": new_registration.status
        }
        
    except HTTPException:
        # Re-raise explicit HTTP exceptions
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error registering for meeting: {str(e)}"
        )


@app.post("/meetings/register_interest", status_code=status.HTTP_201_CREATED)
async def register_interest_for_meeting(interest_data: UserMeetingInterest, db: Session = Depends(get_db)):
    """
    모임 관심 등록 API (결제 의사 표시).
    user_id와 meeting_id를 받아 UserMeeting 테이블에 status='PENDING'으로 기록을 생성합니다.
    최종 확인 전 '신청 중' 상태로 등록하는 역할을 합니다.
    """
    try:
        # 1. 사용자 존재 확인
        user = db.query(User).filter(User.id == interest_data.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {interest_data.user_id} not found"
            )
        
        # 2. 모임 존재 확인
        meeting = db.query(Meeting).filter(Meeting.id == interest_data.meeting_id).first()
        if not meeting:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Meeting with id {interest_data.meeting_id} not found"
            )
        
        # 3. 이미 관심 등록 또는 참가 신청했는지 확인
        existing_interest = db.query(UserMeeting).filter(
            UserMeeting.user_id == interest_data.user_id,
            UserMeeting.meeting_id == interest_data.meeting_id
        ).first()
        
        if existing_interest:
            # 이미 등록된 경우, 상태에 따라 다른 메시지 반환
            if existing_interest.status == "CONFIRMED":
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User is already confirmed for this meeting"
                )
            elif existing_interest.status == "PENDING":
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User has already expressed interest in this meeting"
                )
            elif existing_interest.status == "CANCELLED":
                # 취소된 경우 PENDING으로 재활성화
                existing_interest.status = "PENDING"
                existing_interest.registered_at = datetime.utcnow()
                db.commit()
                return {
                    "message": "Meeting interest reactivated successfully",
                    "registration_id": existing_interest.id,
                    "user_id": interest_data.user_id,
                    "meeting_id": interest_data.meeting_id,
                    "status": "PENDING"
                }
        
        # 4. 모임 정원 확인 (CONFIRMED + PENDING 상태 합산)
        current_participants = db.query(UserMeeting).filter(
            UserMeeting.meeting_id == interest_data.meeting_id,
            UserMeeting.status.in_(["CONFIRMED", "PENDING"])
        ).count()
        
        if current_participants >= meeting.capacity:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Meeting is full. Capacity: {meeting.capacity}"
            )
        
        # 5. 새로운 관심 등록 기록 생성 (status='PENDING')
        new_interest = UserMeeting(
            user_id=interest_data.user_id,
            meeting_id=interest_data.meeting_id,
            status="PENDING",
            registered_at=datetime.utcnow()
        )
        
        db.add(new_interest)
        db.commit()
        db.refresh(new_interest)
        
        return {
            "message": "Meeting interest registered successfully",
            "registration_id": new_interest.id,
            "user_id": interest_data.user_id,
            "meeting_id": interest_data.meeting_id,
            "status": new_interest.status
        }
        
    except HTTPException:
        # Re-raise explicit HTTP exceptions
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error registering interest for meeting: {str(e)}"
        )
