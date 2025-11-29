# 🚀 GoDaddy + Render 도메인 연결 가이드

www.seoulchess.club을 Render에 연결하는 단계별 가이드입니다.

---

## 📋 전체 과정 (약 10-15분 소요)

1. Render에서 도메인 추가 및 DNS 값 확인
2. GoDaddy에서 DNS 레코드 추가
3. SSL 인증서 자동 발급 대기
4. 테스트 및 확인

---

## 1️⃣ Render에서 커스텀 도메인 추가

### Step 1: Render 대시보드 접속
1. https://render.com 로그인
2. **seoul-chess-club** (또는 해당 서비스) 선택

### Step 2: 커스텀 도메인 추가
1. 왼쪽 메뉴에서 **Settings** 클릭
2. 아래로 스크롤하여 **Custom Domain** 섹션 찾기
3. **Add Custom Domain** 버튼 클릭

### Step 3: 도메인 입력
첫 번째 도메인:
```
www.seoulchess.club
```
→ **Save** 클릭

두 번째 도메인 (선택사항):
```
seoulchess.club
```
→ **Save** 클릭

### Step 4: DNS 정보 확인
Render가 다음과 같은 정보를 표시합니다:

```
Domain: www.seoulchess.club
Status: Waiting for DNS configuration
Type: CNAME
Name: www
Value: [your-service].onrender.com
```

**중요**: `[your-service].onrender.com` 값을 복사하세요!
(예: `seoul-chess-club.onrender.com`)

---

## 2️⃣ GoDaddy에서 DNS 레코드 추가

### Step 1: GoDaddy 도메인 관리 접속
1. https://www.godaddy.com 로그인
2. 상단 메뉴에서 **My Products** 클릭
3. **Domains** 섹션에서 **seoulchess.club** 찾기
4. 도메인 옆의 **DNS** 버튼 클릭 (또는 ⋮ 메뉴 → Manage DNS)

### Step 2: 기존 레코드 확인 및 수정

#### A. www 서브도메인 설정

**기존 레코드가 있다면 삭제:**
- Type이 `A` 또는 `CNAME`이고 Name이 `www`인 레코드 찾기
- 오른쪽 ⋮ 메뉴 → **Delete** 클릭

**새 CNAME 레코드 추가:**
1. **Add** 버튼 (또는 **Add New Record**) 클릭
2. 다음 정보 입력:

```
Type: CNAME
Name: www
Value: your-service.onrender.com (Render에서 복사한 값)
TTL: 1 Hour (또는 기본값)
```

3. **Save** 클릭

#### B. 루트 도메인 설정 (선택사항)

**방법 1: CNAME Flattening 지원 시**
```
Type: CNAME
Name: @
Value: your-service.onrender.com
TTL: 1 Hour
```

**방법 2: CNAME Flattening 미지원 시 (Forwarding 사용)**
1. GoDaddy의 **Forwarding** 섹션으로 이동
2. **Add Forwarding** 클릭
3. 설정:
```
Forward to: https://www.seoulchess.club
Forward type: Permanent (301)
```

### Step 3: 변경사항 저장
- 모든 레코드가 올바르게 입력되었는지 확인
- **Save** 또는 **Save All Changes** 클릭

---

## 3️⃣ DNS 전파 및 SSL 인증서 대기

### DNS 전파 시간
- **일반적으로**: 5-15분
- **최대**: 48시간 (드물게)

### Render에서 상태 확인
1. Render 대시보드 → Settings → Custom Domain
2. 도메인 상태 확인:
   - ⏳ **Waiting for DNS**: DNS 전파 대기 중
   - ✅ **Active**: DNS 연결 완료, SSL 발급 중
   - 🔒 **Active with SSL**: 완료!

### SSL 인증서 자동 발급
- Render가 Let's Encrypt SSL 인증서를 자동으로 발급
- 보통 1-2분 내 완료
- 별도 작업 불필요

---

## 4️⃣ 배포 및 환경 변수 확인

### 환경 변수 설정 확인
1. Render 대시보드 → **Environment** 탭
2. 다음 변수가 설정되어 있는지 확인:

```
BASE_DOMAIN=https://www.seoulchess.club
ADMIN_ACCESS_CODE=your-admin-code
ADMIN_EMAIL=admin@seoulchess.club
JWT_SECRET_KEY=your-jwt-secret-key-change-this
```

### API 키 추가 (아직 안 했다면)
```
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=your-twilio-phone-number
GEMINI_API_KEY=your-gemini-api-key
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
KAKAO_PAY_ADMIN_KEY=your-kakao-pay-admin-key
KAKAO_PAY_CID=TC0ONETIME
```

### 재배포 (환경 변수 변경 시)
환경 변수를 변경했다면:
1. **Manual Deploy** → **Deploy latest commit** 클릭
2. 또는 코드 변경 후 Git Push:
```bash
git add .
git commit -m "Update environment variables"
git push origin main
```

---

## 5️⃣ 테스트 및 확인

### Step 1: DNS 전파 확인

**터미널에서 확인:**
```bash
# www 서브도메인
nslookup www.seoulchess.club

# 예상 결과:
# Name:    your-service.onrender.com
# Address: [IP 주소]
```

**온라인 도구 사용:**
- https://www.whatsmydns.net/
- Domain에 `www.seoulchess.club` 입력
- Type: `CNAME` 선택
- 전 세계적으로 전파되었는지 확인

### Step 2: HTTPS 접속 테스트

**브라우저에서 접속:**
1. https://www.seoulchess.club/health
2. 예상 응답:
```json
{
  "status": "ok",
  "service": "Seoul Chess Club API",
  "version": "1.0.0",
  "timestamp": "2025-11-29T..."
}
```

**SSL 인증서 확인:**
- 주소창의 자물쇠 🔒 아이콘 클릭
- 인증서 정보 확인
- "Let's Encrypt" 발급 확인

### Step 3: 주요 엔드포인트 테스트

**메인 페이지:**
```
https://www.seoulchess.club/
```

**API 문서:**
```
https://www.seoulchess.club/docs
```

**건강 체크:**
```bash
curl https://www.seoulchess.club/health
```

---

## 🐛 문제 해결

### 1. "This site can't be reached" 오류

**원인:** DNS 전파가 아직 완료되지 않음

**해결:**
- 15-30분 대기
- DNS 캐시 삭제:
```bash
# Mac
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder

# Windows
ipconfig /flushdns

# Linux
sudo systemd-resolve --flush-caches
```

### 2. SSL 인증서 오류 (NET::ERR_CERT_COMMON_NAME_INVALID)

**원인:** SSL 인증서가 아직 발급되지 않음

**해결:**
1. Render 대시보드에서 상태 확인
2. 5-10분 대기
3. 강제 새로고침: Cmd+Shift+R (Mac), Ctrl+Shift+R (Win)

### 3. CORS 오류

**원인:** CORS 설정에 도메인이 없음

**확인:**
`main.py` 파일 확인:
```python
allow_origins=[
    "https://www.seoulchess.club",  # ✅ 있어야 함
    "https://seoulchess.club",
    ...
]
```

**해결:** 이미 설정되어 있으므로 서버 재시작만 하면 됨

### 4. GoDaddy DNS 레코드가 저장 안 됨

**원인:** GoDaddy 프록시 또는 충돌하는 레코드

**해결:**
- 기존 `www` 레코드 완전 삭제 후 재추가
- GoDaddy 프리미엄 DNS를 사용 중이라면 설정 확인

---

## 📊 배포 상태 모니터링

### Render 로그 확인
1. Render 대시보드 → **Logs** 탭
2. 실시간 로그 확인
3. 에러 메시지 확인

### 서비스 상태 확인
```bash
# 반복 테스트 (10초마다)
watch -n 10 'curl -s https://www.seoulchess.club/health | jq'
```

---

## ✅ 완료 체크리스트

- [ ] Render에 www.seoulchess.club 도메인 추가
- [ ] GoDaddy에 CNAME 레코드 추가 (www → your-service.onrender.com)
- [ ] DNS 전파 완료 확인 (nslookup)
- [ ] SSL 인증서 자동 발급 확인 (🔒 아이콘)
- [ ] https://www.seoulchess.club/health 접속 성공
- [ ] Render 환경 변수 설정 확인
- [ ] 메인 페이지 접속 테스트

---

## 📸 GoDaddy DNS 설정 예시

최종 DNS 레코드는 다음과 같아야 합니다:

```
Type     | Name | Value                          | TTL
---------|------|--------------------------------|--------
CNAME    | www  | your-service.onrender.com      | 1 Hour
CNAME*   | @    | your-service.onrender.com      | 1 Hour

* @ (루트 도메인)은 선택사항
```

---

## 🎉 성공 시 다음 단계

1. **소셜 로그인 리다이렉트 URL 업데이트**
   - Google Cloud Console: https://www.seoulchess.club
   - Apple Developer: https://www.seoulchess.club
   - Kakao Developers: https://www.seoulchess.club

2. **Kakao Pay 리다이렉트 URL 업데이트**
   - 결제 성공 URL: https://www.seoulchess.club/payment/success
   - 결제 실패 URL: https://www.seoulchess.club/payment/fail

3. **데이터베이스 백업 설정**
   - Render 대시보드 → Disk 백업 설정

---

## 📞 지원

문제가 계속되면:
- Render 지원: https://render.com/docs
- GoDaddy 지원: https://www.godaddy.com/help
- Email: contact@seoulchess.club

---

**작성일:** 2025-11-29
**소요 시간:** 약 10-15분
**난이도:** ⭐⭐☆☆☆ (쉬움)
