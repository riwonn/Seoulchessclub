# Community Control Flutter App

체스 커뮤니티 관리 iOS 앱

## 📱 기능

- **SMS 인증**: 전화번호 기반 인증 시스템
- **회원가입/로그인**: JWT 토큰 기반 인증
- **모임 관리**: 모임 목록 조회, 참가 신청, 관심 등록
- **프로필 관리**: 사용자 프로필 및 활동 내역 조회

## 🏗️ 프로젝트 구조

```
lib/
├── main.dart                    # 앱 진입점
├── models/                      # 데이터 모델
│   ├── user.dart
│   ├── meeting.dart
│   └── auth.dart
├── services/                    # API 통신 서비스
│   ├── api_service.dart
│   ├── auth_service.dart
│   └── meeting_service.dart
├── providers/                   # 상태 관리 (Provider)
│   ├── auth_provider.dart
│   └── meeting_provider.dart
├── screens/                     # 화면
│   ├── splash_screen.dart
│   ├── auth/
│   │   ├── phone_verification_screen.dart
│   │   └── registration_screen.dart
│   ├── home/
│   │   └── home_screen.dart
│   ├── meetings/
│   │   └── meetings_list_screen.dart
│   └── profile/
│       └── profile_screen.dart
└── widgets/                     # 재사용 위젯 (추후 추가)
```

## 🚀 시작하기

### 1. 의존성 설치

```bash
cd flutter_app
flutter pub get
```

### 2. JSON 직렬화 코드 생성

모델 클래스에서 사용하는 JSON 직렬화 코드를 생성합니다:

```bash
flutter pub run build_runner build --delete-conflicting-outputs
```

### 3. API 서버 URL 설정

`lib/services/api_service.dart` 파일에서 API 베이스 URL을 설정하세요:

```dart
// 개발 환경
static const String baseUrl = 'http://localhost:8000';

// 프로덕션 환경 (Railway 등)
static const String baseUrl = 'https://your-api-url.railway.app';
```

### 4. 앱 실행

```bash
flutter run
```

## 📦 주요 패키지

- **provider**: 상태 관리
- **dio**: HTTP 클라이언트
- **shared_preferences**: 로컬 저장소 (토큰 저장)
- **go_router**: 라우팅 및 네비게이션
- **json_annotation**: JSON 직렬화
- **intl**: 날짜/시간 포맷팅

## 🔐 인증 흐름

1. **전화번호 입력** → SMS 인증 코드 요청
2. **인증 코드 확인** → SMS 인증
3. **사용자 존재 확인**:
   - 기존 사용자: 자동 로그인 → 홈 화면
   - 신규 사용자: 회원가입 페이지 → 가입 후 로그인 → 홈 화면
4. **JWT 토큰 저장** → 이후 API 요청 시 자동으로 헤더에 포함

## 🛠️ 백엔드 API 엔드포인트

### 인증 관련
- `POST /sms/request` - SMS 인증 코드 요청
- `POST /sms/verify` - SMS 인증 코드 확인
- `POST /register` - 회원가입
- `POST /auth/login` - 로그인 (JWT 토큰 발급)
- `GET /auth/me` - 현재 사용자 정보 조회 (인증 필요)

### 모임 관련
- `GET /meetings` - 모든 모임 목록 조회
- `POST /meetings/register` - 모임 참가 신청 (인증 필요)
- `POST /meetings/register_interest` - 모임 관심 등록 (인증 필요)

## 📱 iOS 배포 준비

### 1. 앱 아이콘 설정

`ios/Runner/Assets.xcassets/AppIcon.appiconset/` 디렉토리에 앱 아이콘 추가

### 2. Bundle Identifier 설정

`ios/Runner.xcodeproj/project.pbxproj`에서 Bundle Identifier 변경:
```
PRODUCT_BUNDLE_IDENTIFIER = com.yourcompany.communitycontrol
```

### 3. iOS 최소 버전 설정

`ios/Podfile`:
```ruby
platform :ios, '12.0'
```

### 4. 권한 설정

`ios/Runner/Info.plist`에 필요한 권한 추가:
```xml
<key>NSPhotoLibraryUsageDescription</key>
<string>프로필 사진 업로드를 위해 사진 라이브러리 접근이 필요합니다</string>
```

### 5. 빌드 및 배포

```bash
# iOS 빌드
flutter build ios --release

# TestFlight 업로드 (Xcode에서 진행)
# 1. Xcode에서 ios/Runner.xcworkspace 열기
# 2. Product → Archive
# 3. Distribute App → App Store Connect
```

## 🐛 트러블슈팅

### JSON 직렬화 오류

```bash
flutter pub run build_runner clean
flutter pub run build_runner build --delete-conflicting-outputs
```

### iOS 빌드 오류

```bash
cd ios
pod install
cd ..
flutter clean
flutter pub get
```

### API 연결 오류

- API 서버가 실행 중인지 확인
- `api_service.dart`의 baseUrl이 올바른지 확인
- iOS 시뮬레이터에서는 `localhost` 대신 `127.0.0.1` 사용

## 📝 환경 변수

백엔드 서버 `.env` 파일 설정:

```env
# Twilio SMS 인증
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=your_twilio_phone

# JWT 인증
JWT_SECRET_KEY=your_secret_key_here

# Gemini API (CS 파싱용)
GEMINI_API_KEY=your_gemini_key
```

## 🎯 다음 단계

1. ✅ 백엔드 API JWT 인증 추가
2. ✅ Flutter 프로젝트 기본 구조 생성
3. ✅ 데이터 모델 및 서비스 레이어 구현
4. ✅ 주요 화면 구현 (인증, 홈, 모임, 프로필)
5. 🔄 JSON 직렬화 코드 생성 필요
6. 📱 iOS 앱 아이콘 및 스플래시 스크린 디자인
7. 🧪 테스트 및 버그 수정
8. 🚀 TestFlight 베타 테스트
9. 📦 App Store 출시

## 📄 라이선스

Copyright © 2024 Community Control

