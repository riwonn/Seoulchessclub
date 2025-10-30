# 🚀 Flutter iOS 앱 전환 완료 가이드

## ✅ 완료된 작업

### 1. 백엔드 API 리팩토링 ✅

- **JWT 토큰 기반 인증 시스템 추가**
  - `auth.py`: JWT 토큰 생성/검증 함수
  - `get_current_user()`: 인증 미들웨어 의존성
  - 토큰 만료 기간: 7일

- **새로운 API 엔드포인트**
  - `POST /auth/login`: 로그인 및 JWT 토큰 발급
  - `GET /auth/me`: 현재 사용자 정보 조회 (인증 필요)

- **기존 API 개선**
  - `POST /meetings/register`: 토큰 기반 인증으로 변경 (user_id 자동 추출)
  - `POST /meetings/register_interest`: 토큰 기반 인증으로 변경

### 2. Flutter 프로젝트 생성 ✅

완전한 Flutter 앱이 `flutter_app/` 디렉토리에 생성되었습니다:

```
flutter_app/
├── pubspec.yaml              # 패키지 의존성
├── README.md                 # Flutter 앱 문서
├── lib/
│   ├── main.dart            # 앱 진입점
│   ├── models/              # 데이터 모델
│   │   ├── user.dart
│   │   ├── meeting.dart
│   │   └── auth.dart
│   ├── services/            # API 통신
│   │   ├── api_service.dart
│   │   ├── auth_service.dart
│   │   └── meeting_service.dart
│   ├── providers/           # 상태 관리
│   │   ├── auth_provider.dart
│   │   └── meeting_provider.dart
│   └── screens/             # 화면
│       ├── splash_screen.dart
│       ├── auth/
│       │   ├── phone_verification_screen.dart
│       │   └── registration_screen.dart
│       ├── home/
│       │   └── home_screen.dart
│       ├── meetings/
│       │   └── meetings_list_screen.dart
│       └── profile/
│           └── profile_screen.dart
```

### 3. 주요 기능 구현 ✅

- ✅ SMS 인증 화면
- ✅ 회원가입 화면
- ✅ 로그인 (JWT 토큰)
- ✅ 홈 화면 (대시보드)
- ✅ 모임 목록 및 참가 신청
- ✅ 프로필 화면
- ✅ 자동 라우팅 및 인증 체크

---

## 🔧 다음 단계: 앱 실행하기

### 1단계: 백엔드 서버 설정

#### 1.1 환경 변수 설정

```bash
cd /Users/riwon/Documents/community_control_ai
cp .env.example .env
```

`.env` 파일을 열고 실제 값으로 변경:

```env
TWILIO_ACCOUNT_SID=실제_Twilio_SID
TWILIO_AUTH_TOKEN=실제_Twilio_Token
TWILIO_PHONE_NUMBER=실제_Twilio_번호
JWT_SECRET_KEY=매우_강력한_시크릿_키
GEMINI_API_KEY=실제_Gemini_API_키
```

#### 1.2 패키지 설치

```bash
# 가상환경 활성화
source venv/bin/activate

# 새로운 패키지 설치
pip install -r requirements.txt
```

#### 1.3 서버 실행

```bash
python main.py
# 또는
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

서버가 `http://localhost:8000`에서 실행됩니다.

---

### 2단계: Flutter 앱 설정

#### 2.1 Flutter SDK 확인

```bash
flutter --version
```

Flutter가 설치되어 있지 않다면:
- [Flutter 공식 사이트](https://flutter.dev/docs/get-started/install)에서 설치

#### 2.2 프로젝트로 이동

```bash
cd flutter_app
```

#### 2.3 의존성 설치

```bash
flutter pub get
```

#### 2.4 JSON 직렬화 코드 생성

모델 클래스의 JSON 변환 코드를 자동 생성:

```bash
flutter pub run build_runner build --delete-conflicting-outputs
```

이 명령어는 다음 파일들을 생성합니다:
- `lib/models/user.g.dart`
- `lib/models/meeting.g.dart`
- `lib/models/auth.g.dart`

#### 2.5 API 서버 URL 설정

`lib/services/api_service.dart` 파일 열기:

```dart
// 현재 설정 (로컬 개발)
static const String baseUrl = 'http://localhost:8000';

// iOS 시뮬레이터에서는 이렇게 변경:
static const String baseUrl = 'http://127.0.0.1:8000';
```

#### 2.6 iOS 시뮬레이터 실행

```bash
# 사용 가능한 시뮬레이터 확인
flutter emulators

# iOS 시뮬레이터 실행
open -a Simulator

# 앱 실행
flutter run
```

---

## 📱 앱 사용 흐름

### 1. 스플래시 화면
- 앱 로딩
- 자동 인증 체크

### 2. 전화번호 인증
- 전화번호 입력
- "인증 코드 받기" 버튼 클릭
- SMS로 받은 6자리 코드 입력
- "인증 확인" 버튼 클릭

### 3-A. 기존 사용자
- 자동 로그인
- 홈 화면으로 이동

### 3-B. 신규 사용자
- 회원가입 화면으로 이동
- 정보 입력 (이름, 이메일, 성별 등)
- "가입 완료" 버튼 클릭
- 자동 로그인 → 홈 화면

### 4. 홈 화면
- 환영 메시지
- 방문 횟수 표시
- 다가오는 모임 미리보기
- 빠른 메뉴 (모임 목록, 내 프로필)

### 5. 모임 목록
- 모든 예정된 모임 표시
- 정원 현황 표시
- "관심 등록" 또는 "참가 신청" 버튼

### 6. 프로필
- 사용자 정보 표시
- 활동 통계
- 참여한 모임 목록
- 로그아웃

---

## 🐛 문제 해결

### iOS 빌드 오류

```bash
cd ios
pod install
cd ..
flutter clean
flutter pub get
flutter run
```

### JSON 직렬화 오류

```bash
flutter pub run build_runner clean
flutter pub run build_runner build --delete-conflicting-outputs
```

### API 연결 오류

1. 백엔드 서버가 실행 중인지 확인:
   ```bash
   curl http://localhost:8000/health
   ```

2. iOS 시뮬레이터에서는 `localhost` 대신 `127.0.0.1` 사용

3. 방화벽 설정 확인

---

## 🚀 TestFlight 배포 (선택사항)

### 1. Apple Developer 계정 필요
- 연간 $99 USD
- [Apple Developer](https://developer.apple.com/) 가입

### 2. App Store Connect 설정
- 앱 등록
- Bundle Identifier 설정
- 스크린샷 준비

### 3. 빌드 및 업로드

```bash
# iOS 릴리스 빌드
flutter build ios --release

# Xcode에서 업로드
open ios/Runner.xcworkspace
# Product → Archive → Distribute App
```

---

## 📊 프로젝트 현황

### ✅ 완료된 기능

1. **백엔드 API**
   - ✅ JWT 인증 시스템
   - ✅ SMS 인증
   - ✅ 회원가입/로그인
   - ✅ 모임 관리
   - ✅ 사용자 프로필

2. **Flutter 앱**
   - ✅ 프로젝트 구조
   - ✅ 데이터 모델
   - ✅ API 서비스 레이어
   - ✅ 상태 관리 (Provider)
   - ✅ 6개 주요 화면
   - ✅ 라우팅 및 네비게이션

### 🔄 추가 작업 필요

1. **JSON 직렬화 코드 생성** ⚠️
   ```bash
   flutter pub run build_runner build --delete-conflicting-outputs
   ```

2. **앱 아이콘 및 스플래시 스크린** (선택)
   - 디자인 제작
   - `flutter_launcher_icons` 패키지 사용

3. **테스트**
   - 단위 테스트
   - 위젯 테스트
   - 통합 테스트

4. **프로덕션 배포**
   - API URL을 프로덕션 서버로 변경
   - iOS 빌드 및 TestFlight 업로드

---

## 📚 참고 문서

- [Flutter 앱 README](flutter_app/README.md)
- [API 문서](API_DOCUMENTATION.md)
- [백엔드 README](README.md)

---

## 💡 추가 개선 제안

1. **푸시 알림** (Firebase Cloud Messaging)
2. **이미지 업로드** (프로필 사진)
3. **소셜 로그인** (Apple, Google)
4. **다크 모드** 지원
5. **다국어 지원** (i18n)
6. **오프라인 모드** (로컬 캐싱)
7. **앱 내 결제** (모임 참가비)

---

## 🎉 축하합니다!

웹 애플리케이션이 성공적으로 Flutter iOS 앱으로 전환되었습니다!

이제 다음 명령어로 앱을 실행할 수 있습니다:

```bash
# 1. 백엔드 서버 실행
cd /Users/riwon/Documents/community_control_ai
source venv/bin/activate
python main.py

# 2. Flutter 앱 실행 (새 터미널)
cd /Users/riwon/Documents/community_control_ai/flutter_app
flutter pub get
flutter pub run build_runner build --delete-conflicting-outputs
flutter run
```

---

**작성일:** 2024-10-27  
**버전:** 1.0.0

