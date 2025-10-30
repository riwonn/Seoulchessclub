# Community Control API 문서

## 📡 API 베이스 URL

- 개발: `http://localhost:8000`
- 프로덕션: `https://your-app.railway.app`

---

## 🔐 인증 (Authentication)

### 1. SMS 인증 코드 요청

전화번호로 SMS 인증 코드를 요청합니다.

**Endpoint:** `POST /sms/request`

**Request Body:**
```json
{
  "phone_number": "01012345678"
}
```

**Response (200):**
```json
{
  "message": "SMS sent successfully"
}
```

**Error Responses:**
- `429`: 너무 많은 요청 (30초 쿨다운)
- `500`: 서버 오류

---

### 2. SMS 인증 코드 확인

SMS로 받은 인증 코드를 확인합니다.

**Endpoint:** `POST /sms/verify`

**Request Body:**
```json
{
  "phone_number": "01012345678",
  "code": "123456"
}
```

**Response (200):**
```json
{
  "message": "Verification successful."
}
```

**Error Responses:**
- `400`: 잘못된 코드 또는 만료된 코드
- `500`: 서버 오류

---

### 3. 회원가입

새로운 사용자를 등록합니다.

**Endpoint:** `POST /register`

**Request Body:**
```json
{
  "name": "홍길동",
  "phone_number": "01012345678",
  "email": "hong@example.com",
  "gender": "MALE",
  "birth_year": 1990,
  "chess_experience": "OCCASIONALLY_PLAY",
  "chess_rating": "BETWEEN_1000_1500"
}
```

**Response (201):**
```json
{
  "id": 1,
  "name": "홍길동",
  "phone_number": "01012345678",
  "email": "hong@example.com",
  "gender": "MALE",
  "birth_year": 1990,
  "chess_experience": "OCCASIONALLY_PLAY",
  "chess_rating": "BETWEEN_1000_1500",
  "total_visits": 1,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00",
  "attended_meetings": []
}
```

**Error Responses:**
- `403`: 정원 초과 (최대 30명)
- `409`: 중복된 전화번호 또는 이메일
- `500`: 서버 오류

---

### 4. 로그인 (JWT 토큰 발급)

전화번호로 로그인하여 JWT 토큰을 발급받습니다.

**Endpoint:** `POST /auth/login`

**Request Body:**
```json
{
  "phone_number": "01012345678"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "name": "홍길동",
    "phone_number": "01012345678",
    "email": "hong@example.com",
    "gender": "MALE",
    "birth_year": 1990,
    "chess_experience": "OCCASIONALLY_PLAY",
    "chess_rating": "BETWEEN_1000_1500",
    "total_visits": 5,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-05T00:00:00",
    "attended_meetings": []
  }
}
```

**Error Responses:**
- `404`: 등록되지 않은 사용자
- `500`: 서버 오류

---

### 5. 현재 사용자 정보 조회

JWT 토큰으로 인증된 사용자의 정보를 조회합니다.

**Endpoint:** `GET /auth/me`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200):**
```json
{
  "id": 1,
  "name": "홍길동",
  "phone_number": "01012345678",
  "email": "hong@example.com",
  "gender": "MALE",
  "birth_year": 1990,
  "chess_experience": "OCCASIONALLY_PLAY",
  "chess_rating": "BETWEEN_1000_1500",
  "total_visits": 5,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-05T00:00:00",
  "attended_meetings": []
}
```

**Error Responses:**
- `401`: 인증 실패 (토큰 없음 또는 만료)
- `500`: 서버 오류

---

## 👥 사용자 (Users)

### 전화번호로 사용자 조회

재방문 고객 인식을 위해 전화번호로 사용자를 조회합니다.

**Endpoint:** `GET /get_user_by_phone`

**Query Parameters:**
- `phone_number`: 전화번호 (예: `01012345678`)

**Response (200):**
```json
{
  "id": 1,
  "name": "홍길동",
  "phone_number": "01012345678",
  "email": "hong@example.com",
  "gender": "MALE",
  "birth_year": 1990,
  "chess_experience": "OCCASIONALLY_PLAY",
  "chess_rating": "BETWEEN_1000_1500",
  "total_visits": 5,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-05T00:00:00",
  "attended_meetings": []
}
```

**Error Responses:**
- `404`: 사용자를 찾을 수 없음
- `500`: 서버 오류

---

## 📅 모임 (Meetings)

### 1. 모든 모임 목록 조회

활성화된 모든 모임을 조회합니다.

**Endpoint:** `GET /meetings`

**Response (200):**
```json
[
  {
    "id": 1,
    "title": "체스 초보자 모임",
    "date_time": "2024-02-01T19:00:00",
    "location": "서울시 강남구 체스카페",
    "capacity": 10,
    "created_at": "2024-01-01T00:00:00",
    "participants": [
      {
        "id": 1,
        "user_id": 1,
        "meeting_id": 1,
        "status": "CONFIRMED",
        "registered_at": "2024-01-15T10:00:00"
      }
    ]
  }
]
```

---

### 2. 모임 참가 신청 (인증 필요)

지정된 모임에 참가 신청합니다.

**Endpoint:** `POST /meetings/register`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `meeting_id`: 모임 ID (예: `1`)

**Response (201):**
```json
{
  "message": "Meeting registration successful",
  "registration_id": 1,
  "user_id": 1,
  "meeting_id": 1,
  "status": "CONFIRMED"
}
```

**Error Responses:**
- `401`: 인증 필요
- `403`: 정원 초과
- `404`: 모임을 찾을 수 없음
- `409`: 이미 참가 신청함
- `500`: 서버 오류

---

### 3. 모임 관심 등록 (인증 필요)

모임에 관심을 등록합니다 (결제 의사 표시).

**Endpoint:** `POST /meetings/register_interest`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `meeting_id`: 모임 ID (예: `1`)

**Response (201):**
```json
{
  "message": "Meeting interest registered successfully",
  "registration_id": 1,
  "user_id": 1,
  "meeting_id": 1,
  "status": "PENDING"
}
```

**Error Responses:**
- `401`: 인증 필요
- `403`: 정원 초과
- `404`: 모임을 찾을 수 없음
- `409`: 이미 관심 등록함
- `500`: 서버 오류

---

### 4. 모임 생성 (운영자용, 인증 필요)

새로운 모임을 생성합니다.

**Endpoint:** `POST /meetings/create`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "title": "체스 초보자 모임",
  "date_time": "2024-02-01T19:00:00",
  "location": "서울시 강남구 체스카페",
  "capacity": 10
}
```

**Response (201):**
```json
{
  "id": 1,
  "title": "체스 초보자 모임",
  "date_time": "2024-02-01T19:00:00",
  "location": "서울시 강남구 체스카페",
  "capacity": 10,
  "created_at": "2024-01-01T00:00:00",
  "participants": []
}
```

---

## 📝 데이터 모델 (Enums)

### Gender (성별)
- `MALE`: 남성
- `FEMALE`: 여성
- `OTHER`: 기타

### ChessExperience (체스 경험)
- `NO_BUT_WANT_TO_LEARN`: 아니요, 배우고 싶어요
- `KNOW_RULES_ONLY`: 규칙만 알아요
- `OCCASIONALLY_PLAY`: 가끔 둡니다
- `PLAY_WELL`: 잘 둡니다

### ChessRating (체스 레이팅)
- `I_DONT_KNOW`: 모르겠어요
- `UNDER_1000`: 1000 이하
- `BETWEEN_1000_1500`: 1000-1500
- `BETWEEN_1500_2000`: 1500-2000
- `OVER_2000`: 2000 이상

### MeetingStatus (모임 참가 상태)
- `CONFIRMED`: 확정
- `PENDING`: 대기중
- `CANCELLED`: 취소됨

---

## 🔒 JWT 토큰 사용법

1. **로그인** (`POST /auth/login`)으로 토큰 발급
2. 토큰을 로컬 저장소에 저장 (SharedPreferences, localStorage 등)
3. 인증이 필요한 API 요청 시 헤더에 포함:
   ```
   Authorization: Bearer {access_token}
   ```
4. 토큰 만료 시 (`401 Unauthorized`) 다시 로그인

**토큰 만료 기간:** 7일

---

## 🧪 테스트 예시 (cURL)

### SMS 인증 코드 요청
```bash
curl -X POST http://localhost:8000/sms/request \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "01012345678"}'
```

### 로그인
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "01012345678"}'
```

### 모임 목록 조회
```bash
curl -X GET http://localhost:8000/meetings
```

### 모임 참가 신청 (인증 필요)
```bash
curl -X POST "http://localhost:8000/meetings/register?meeting_id=1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 📊 에러 코드 정리

| 상태 코드 | 설명 |
|-----------|------|
| `200` | 성공 |
| `201` | 생성 성공 |
| `400` | 잘못된 요청 |
| `401` | 인증 필요 |
| `403` | 권한 없음 (정원 초과 등) |
| `404` | 리소스를 찾을 수 없음 |
| `409` | 충돌 (중복 데이터) |
| `429` | 너무 많은 요청 |
| `500` | 서버 내부 오류 |

---

## 🚀 프로덕션 배포 시 주의사항

1. **환경 변수 설정**:
   - `JWT_SECRET_KEY`: 강력한 시크릿 키 사용
   - `TWILIO_*`: Twilio 계정 정보
   - `GEMINI_API_KEY`: Google Gemini API 키

2. **HTTPS 사용**: 프로덕션에서는 반드시 HTTPS 사용

3. **CORS 설정**: 필요한 도메인만 허용

4. **Rate Limiting**: API 남용 방지를 위한 제한 설정

5. **로깅**: 모든 API 요청/응답 로깅

---

**문서 버전:** 1.0.0  
**최종 업데이트:** 2024-10-27

