# 🍎💬🔍 소셜 로그인 설정 가이드

Apple 로그인, 카카오 로그인, Google 로그인 기능이 추가되었습니다!

---

## ✅ 완료된 작업

### 백엔드 (FastAPI)
- ✅ Apple 로그인 API (`POST /auth/apple`)
- ✅ 카카오 로그인 API (`POST /auth/kakao`)
- ✅ Google 로그인 API (`POST /auth/google`)
- ✅ 소셜 로그인용 DB 모델 확장 (`social_provider`, `social_id`)
- ✅ JWT 토큰 발급 및 사용자 자동 생성

### Flutter 앱
- ✅ `sign_in_with_apple` 패키지 통합
- ✅ `kakao_flutter_sdk_user` 패키지 통합
- ✅ 소셜 로그인 서비스 레이어
- ✅ 로그인 화면에 소셜 로그인 버튼 추가
- ✅ 자동 회원가입 및 로그인 처리

---

## 🍎 Apple 로그인 설정

### 1. Apple Developer 계정 설정

#### 1.1 App ID 등록
1. [Apple Developer Console](https://developer.apple.com/account/) 접속
2. **Certificates, Identifiers & Profiles** → **Identifiers** → **+** 버튼
3. **App IDs** 선택 → Bundle ID 입력 (예: `com.yourcompany.communitycontrol`)
4. **Sign in with Apple** 체크 → 저장

#### 1.2 Service ID 등록 (웹/백엔드용)
1. **Identifiers** → **+** 버튼 → **Services IDs** 선택
2. Identifier 입력 (예: `com.yourcompany.communitycontrol.service`)
3. **Sign in with Apple** 활성화
4. **Configure** 클릭:
   - **Primary App ID**: 위에서 만든 App ID 선택
   - **Domains and Subdomains**: 백엔드 도메인 입력 (예: `yourapp.railway.app`)
   - **Return URLs**: 백엔드 콜백 URL (현재는 불필요)

#### 1.3 Key 생성 (백엔드 검증용)
1. **Keys** → **+** 버튼
2. Key 이름 입력 → **Sign in with Apple** 체크
3. **Configure** → App ID 선택
4. **Key** 다운로드 (.p8 파일) ⚠️ 한 번만 다운로드 가능!
5. **Key ID** 기록

### 2. 백엔드 환경 변수 설정

`.env` 파일에 추가:

```env
# Apple Sign In 설정
APPLE_CLIENT_ID=com.yourcompany.communitycontrol  # Service ID 또는 Bundle ID
```

### 3. Flutter iOS 설정

#### 3.1 Xcode 프로젝트 설정
1. `ios/Runner.xcworkspace` 열기
2. **Runner** → **Signing & Capabilities**
3. **+ Capability** 클릭 → **Sign in with Apple** 추가
4. Bundle Identifier 확인 (Apple Developer에서 등록한 것과 일치해야 함)

#### 3.2 Entitlements 확인
`ios/Runner/Runner.entitlements` 파일에 자동 추가됨:

```xml
<key>com.apple.developer.applesignin</key>
<array>
    <string>Default</string>
</array>
```

---

## 💬 카카오 로그인 설정

### 1. 카카오 개발자 콘솔 설정

#### 1.1 애플리케이션 등록
1. [카카오 개발자 콘솔](https://developers.kakao.com/) 접속
2. **내 애플리케이션** → **애플리케이션 추가하기**
3. 앱 이름, 사업자명 입력

#### 1.2 플랫폼 설정 (iOS)
1. 애플리케이션 선택 → **플랫폼** → **iOS 플랫폼 등록**
2. **Bundle ID** 입력 (예: `com.yourcompany.communitycontrol`)
3. **AppStore ID** (선택)

#### 1.3 앱 키 확인
1. **앱 설정** → **앱 키**
2. 다음 키 복사:
   - **네이티브 앱 키** (Native App Key)
   - **JavaScript 키** (JavaScript Key)

#### 1.4 카카오 로그인 활성화
1. **제품 설정** → **카카오 로그인**
2. **활성화 설정** → **ON**
3. **Redirect URI** 설정 (선택, 모바일 앱은 불필요)

### 2. Flutter 앱 설정

#### 2.1 카카오 SDK 초기화

`lib/main.dart`에서 앱 키 설정:

```dart
void main() {
  KakaoSdk.init(
    nativeAppKey: '실제_네이티브_앱_키',
    javaScriptAppKey: '실제_JavaScript_앱_키',
  );
  
  runApp(const CommunityControlApp());
}
```

#### 2.2 iOS 설정

**`ios/Runner/Info.plist`** 파일에 추가:

```xml
<key>CFBundleURLTypes</key>
<array>
    <dict>
        <key>CFBundleTypeRole</key>
        <string>Editor</string>
        <key>CFBundleURLSchemes</key>
        <array>
            <string>kakao네이티브앱키</string>
        </array>
    </dict>
</array>

<key>LSApplicationQueriesSchemes</key>
<array>
    <string>kakaokompassauth</string>
    <string>kakaolink</string>
</array>

<key>KAKAO_APP_KEY</key>
<string>네이티브앱키</string>
```

**예시:**
```xml
<key>CFBundleURLSchemes</key>
<array>
    <string>kakao1234567890abcdef</string>
</array>

<key>KAKAO_APP_KEY</key>
<string>1234567890abcdef</string>
```

---

## 🔍 Google 로그인 설정

### 1. Google Cloud Console 설정

#### 1.1 프로젝트 생성
1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. **새 프로젝트** 생성 또는 기존 프로젝트 선택
3. 프로젝트 이름 입력 (예: `Community Control AI`)

#### 1.2 OAuth 동의 화면 구성
1. **APIs & Services** → **OAuth consent screen**
2. **User Type** 선택:
   - **Internal**: G Suite 조직 내 사용자만 (조직 계정 필요)
   - **External**: 모든 Google 계정 사용자 (추천)
3. 앱 정보 입력:
   - **App name**: Community Control AI
   - **User support email**: 지원 이메일
   - **Developer contact information**: 개발자 이메일
4. **Scopes** 추가:
   - `./auth/userinfo.email`
   - `./auth/userinfo.profile`
   - `openid`
5. **Test users** 추가 (External 모드의 경우, 배포 전 테스트용)

#### 1.3 OAuth 2.0 클라이언트 ID 생성
1. **APIs & Services** → **Credentials**
2. **+ CREATE CREDENTIALS** → **OAuth client ID**
3. **Application type** 선택:
   - **iOS**: iOS 앱용
   - **Android**: Android 앱용
   - **Web application**: 웹/백엔드 테스트용
4. **iOS 설정** (Flutter iOS용):
   - **Name**: iOS Client
   - **Bundle ID**: `com.yourcompany.communitycontrol`
5. **Android 설정** (Flutter Android용):
   - **Name**: Android Client
   - **Package name**: `com.yourcompany.communitycontrol`
   - **SHA-1 certificate fingerprint**: 디버그/릴리즈 서명 키의 SHA-1
6. **Client ID** 복사 (예: `123456789-abcdefg.apps.googleusercontent.com`)

#### 1.4 SHA-1 인증서 지문 얻기 (Android)

**디버그 키:**
```bash
keytool -list -v -keystore ~/.android/debug.keystore -alias androiddebugkey -storepass android -keypass android
```

**릴리즈 키:**
```bash
keytool -list -v -keystore /path/to/your/keystore.jks -alias your-key-alias
```

### 2. 백엔드 환경 변수 설정

`.env` 파일에 추가:

```env
# Google OAuth 설정
GOOGLE_CLIENT_ID=123456789-abcdefg.apps.googleusercontent.com
```

### 3. Flutter 앱 설정

#### 3.1 패키지 추가

`pubspec.yaml`에 추가:

```yaml
dependencies:
  google_sign_in: ^6.1.5
```

설치:
```bash
flutter pub get
```

#### 3.2 iOS 설정

**`ios/Runner/Info.plist`** 파일에 추가:

```xml
<key>CFBundleURLTypes</key>
<array>
    <dict>
        <key>CFBundleTypeRole</key>
        <string>Editor</string>
        <key>CFBundleURLSchemes</key>
        <array>
            <!-- Google Client ID를 역순으로 -->
            <string>com.googleusercontent.apps.123456789-abcdefg</string>
        </array>
    </dict>
</array>
```

**Note**: URL Scheme는 Client ID를 역순으로 변환한 것입니다.
- Client ID: `123456789-abcdefg.apps.googleusercontent.com`
- URL Scheme: `com.googleusercontent.apps.123456789-abcdefg`

#### 3.3 Android 설정

**`android/app/build.gradle`** 확인:

```gradle
android {
    defaultConfig {
        applicationId "com.yourcompany.communitycontrol"
        minSdkVersion 21  // Google Sign-In requires API 21+
    }
}
```

#### 3.4 Google Sign-In 서비스 코드 (Flutter)

```dart
import 'package:google_sign_in/google_sign_in.dart';

class GoogleAuthService {
  final GoogleSignIn _googleSignIn = GoogleSignIn(
    scopes: ['email', 'profile'],
  );

  Future<String?> signInWithGoogle() async {
    try {
      // 1. Google 로그인
      final GoogleSignInAccount? googleUser = await _googleSignIn.signIn();

      if (googleUser == null) {
        return null; // 사용자가 로그인 취소
      }

      // 2. 인증 토큰 가져오기
      final GoogleSignInAuthentication googleAuth =
          await googleUser.authentication;

      // 3. ID 토큰 반환 (백엔드로 전송)
      return googleAuth.idToken;

    } catch (error) {
      print('Google sign in failed: $error');
      return null;
    }
  }

  Future<void> signOut() async {
    await _googleSignIn.signOut();
  }
}
```

#### 3.5 백엔드 API 호출 (Flutter)

```dart
Future<void> loginWithGoogle(String idToken) async {
  final response = await http.post(
    Uri.parse('$baseUrl/auth/google'),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({
      'id_token': idToken,
    }),
  );

  if (response.statusCode == 200) {
    final data = jsonDecode(response.body);
    // JWT 토큰 저장
    await storage.write(key: 'access_token', value: data['access_token']);
    // 사용자 정보 저장
    print('User: ${data['user']['name']}');
  }
}
```

---

## 🚀 테스트 방법

### 1. 백엔드 서버 실행

```bash
cd /Users/riwon/Documents/community_control_ai
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### 2. Flutter 앱 실행

```bash
cd flutter_app
flutter pub get
flutter run
```

### 3. 소셜 로그인 테스트

#### Apple 로그인:
1. iOS 시뮬레이터 또는 실제 디바이스에서 실행
2. 로그인 화면에서 **Apple로 로그인** 버튼 클릭
3. Apple ID와 비밀번호 입력
4. 첫 로그인 시 이름/이메일 공유 동의
5. 자동으로 회원가입 및 로그인 완료

#### 카카오 로그인:
1. iOS 기기에서 실행 (시뮬레이터에서는 카카오톡 앱 필요)
2. 로그인 화면에서 **카카오로 로그인** 버튼 클릭
3. 카카오톡 앱이 실행되어 로그인 동의
4. 자동으로 회원가입 및 로그인 완료

#### Google 로그인:
1. iOS 또는 Android 기기/시뮬레이터에서 실행
2. 로그인 화면에서 **Google로 로그인** 버튼 클릭
3. Google 계정 선택 화면 표시
4. 계정 선택 및 권한 동의
5. 자동으로 회원가입 및 로그인 완료

---

## 📊 API 엔드포인트

### Apple 로그인
```bash
POST /auth/apple
Content-Type: application/json

{
  "identity_token": "eyJraWQiOiI4N...",
  "authorization_code": "c1a2b3c4...",
  "user_info": {
    "name": {
      "firstName": "길동",
      "lastName": "홍"
    }
  }
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
    "email": "user@privaterelay.appleid.com",
    "social_provider": "apple",
    "social_id": "001234.abc..."
  },
  "is_new_user": true
}
```

### 카카오 로그인
```bash
POST /auth/kakao
Content-Type: application/json

{
  "access_token": "rZSJ9pq7..."
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 2,
    "name": "카카오사용자",
    "email": "user@kakao.com",
    "social_provider": "kakao",
    "social_id": "1234567890"
  },
  "is_new_user": true
}
```

### Google 로그인
```bash
POST /auth/google
Content-Type: application/json

{
  "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6..."
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 3,
    "name": "홍길동",
    "email": "user@gmail.com",
    "social_provider": "google",
    "social_id": "110169484474386276334"
  },
  "is_new_user": true
}
```

---

## 🔧 문제 해결

### Apple 로그인 오류

#### "Invalid client"
- Service ID와 Bundle ID 확인
- Apple Developer Console에서 App ID와 Service ID가 제대로 설정되었는지 확인

#### "Invalid grant"
- Identity Token이 만료되었거나 유효하지 않음
- 토큰 검증 URL 확인: `https://appleid.apple.com/auth/keys`

#### iOS에서 Apple 로그인 버튼이 안 보임
- `isAppleSignInAvailable()`가 false를 반환하는 경우
- iOS 13 이상에서만 지원됨
- Xcode에서 Sign in with Apple Capability 추가 확인

### 카카오 로그인 오류

#### "App key not registered"
- `main.dart`에서 앱 키가 올바르게 설정되었는지 확인
- 카카오 개발자 콘솔에서 Bundle ID가 일치하는지 확인

#### "KakaoTalk not installed"
- 카카오톡이 설치되지 않은 경우 자동으로 웹 로그인으로 전환
- `Info.plist`에 LSApplicationQueriesSchemes 추가 확인

#### "Invalid Redirect URI"
- 카카오 개발자 콘솔에서 Redirect URI 설정
- 모바일 앱은 `kakao{APP_KEY}://oauth` 형식 사용

### Google 로그인 오류

#### "Invalid client"
- Google Cloud Console에서 OAuth 클라이언트 ID 확인
- iOS Bundle ID 또는 Android Package Name이 일치하는지 확인

#### "Invalid ID token"
- ID 토큰이 만료되었거나 유효하지 않음
- 토큰 검증 URL 확인: `https://oauth2.googleapis.com/tokeninfo`

#### iOS에서 Google 로그인 실패
- `Info.plist`에 URL Scheme이 올바르게 설정되었는지 확인
- URL Scheme는 Client ID를 역순으로 변환한 것

#### Android에서 Google 로그인 실패
- SHA-1 인증서 지문이 Google Cloud Console에 등록되었는지 확인
- minSdkVersion이 21 이상인지 확인
- Package Name이 일치하는지 확인

---

## 📱 프로덕션 배포 체크리스트

### Apple 로그인
- [ ] Apple Developer 계정 ($99/년)
- [ ] App ID에 Sign in with Apple 활성화
- [ ] Service ID 등록 및 도메인 인증
- [ ] Key 파일(.p8) 안전하게 보관
- [ ] 백엔드 환경 변수 설정
- [ ] Xcode에서 Sign in with Apple Capability 추가

### 카카오 로그인
- [ ] 카카오 개발자 계정 (무료)
- [ ] 애플리케이션 등록 및 검수 완료
- [ ] Bundle ID 등록
- [ ] 앱 키 발급 및 설정
- [ ] Info.plist URL Schemes 설정
- [ ] 비즈 앱으로 전환 (선택, 고급 기능용)

### Google 로그인
- [ ] Google Cloud 계정 (무료)
- [ ] 프로젝트 생성 및 OAuth 동의 화면 설정
- [ ] iOS 및 Android OAuth 클라이언트 ID 생성
- [ ] Bundle ID / Package Name 등록
- [ ] Android SHA-1 인증서 지문 등록
- [ ] iOS Info.plist URL Schemes 설정
- [ ] 백엔드 환경 변수 설정

---

## 🎯 주요 기능

### 자동 회원가입
- 소셜 로그인 시 사용자 정보가 없으면 자동으로 회원 생성
- 기본 정보 (이름, 이메일)만으로 가입 완료
- 추가 정보는 프로필에서 수정 가능

### 통합 로그인
- SMS 인증, Apple, 카카오, Google 네 가지 로그인 방법 지원
- 모두 동일한 JWT 토큰 시스템 사용
- 이메일 기준으로 계정 통합 가능 (추후 구현)

### 보안
- Apple ID 토큰 서버 사이드 검증
- 카카오 액세스 토큰 실시간 검증
- Google ID 토큰 서버 사이드 검증
- JWT 토큰 7일 만료
- 소셜 제공자 ID로 중복 방지

---

## 📚 참고 문서

- [Apple Sign In 문서](https://developer.apple.com/sign-in-with-apple/)
- [카카오 로그인 가이드](https://developers.kakao.com/docs/latest/ko/kakaologin/common)
- [Google Sign In 문서](https://developers.google.com/identity/sign-in/ios)
- [Flutter sign_in_with_apple](https://pub.dev/packages/sign_in_with_apple)
- [kakao_flutter_sdk](https://pub.dev/packages/kakao_flutter_sdk)
- [google_sign_in](https://pub.dev/packages/google_sign_in)

---

**작성일:** 2024-10-27
**최종 업데이트:** 2025-11-29
**버전:** 1.1.0

