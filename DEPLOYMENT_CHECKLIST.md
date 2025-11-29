# ✅ www.seoulchess.club 배포 체크리스트

빠른 배포를 위한 간단한 체크리스트입니다.

---

## 🚀 빠른 시작 (3단계)

### 1️⃣ DNS 설정 (도메인 등록 업체에서)

**가비아 사용 시:**
1. 가비아 로그인 → My가비아 → 서비스 관리
2. seoulchess.club 선택 → DNS 정보 → DNS 관리
3. 레코드 추가:

```
타입: CNAME
호스트: www
값: your-app.railway.app (또는 your-app.onrender.com)

타입: CNAME
호스트: @
값: your-app.railway.app (또는 your-app.onrender.com)
```

**Cloudflare 사용 시:**
1. Cloudflare 로그인 → 도메인 선택 → DNS → Records
2. Add record 클릭:

```
Type: CNAME
Name: www
Target: your-app.railway.app
Proxy status: Proxied (🧡)

Type: CNAME
Name: @
Target: your-app.railway.app
Proxy status: Proxied (🧡)
```

⏰ **대기 시간:** 5분~30분 (DNS 전파)

---

### 2️⃣ SSL 인증서 (자동)

#### Railway 사용 시:
1. https://railway.app → 프로젝트 선택
2. Settings → Domains
3. "Add Custom Domain" 클릭
4. `www.seoulchess.club` 입력 → Enter
5. `seoulchess.club` 입력 → Enter
6. ✅ Railway가 자동으로 SSL 인증서 발급 (1-2분)

#### Render 사용 시:
1. https://render.com → 서비스 선택
2. Settings → Custom Domain
3. "Add Custom Domain" 클릭
4. `www.seoulchess.club` 입력
5. ✅ Render가 자동으로 SSL 인증서 발급 (1-2분)

---

### 3️⃣ 서버 재시작

#### Railway/Render (자동 배포):
```bash
git add .
git commit -m "Update domain to www.seoulchess.club"
git push origin main
```
✅ 자동으로 재배포됨

#### 로컬 서버 (직접 실행):
```bash
cd /Users/riwon/Documents/community_control_ai
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## ✅ 완료 확인

### DNS 확인:
```bash
nslookup www.seoulchess.club
```

### 서비스 확인:
브라우저에서 https://www.seoulchess.club/health 접속

예상 응답:
```json
{
  "status": "ok",
  "service": "Seoul Chess Club API",
  "version": "1.0.0"
}
```

---

## 🔑 환경 변수 설정 (Railway/Render)

배포 플랫폼에서 다음 환경 변수를 설정하세요:

### 필수 변수
```
BASE_DOMAIN=https://www.seoulchess.club
ADMIN_ACCESS_CODE=your-admin-code
ADMIN_EMAIL=admin@seoulchess.club
JWT_SECRET_KEY=your-jwt-secret-key
```

### API 키 (실제 값으로 교체)
```
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_PHONE_NUMBER=your-phone-number
GEMINI_API_KEY=your-gemini-key
GOOGLE_CLIENT_ID=your-google-client-id
KAKAO_PAY_ADMIN_KEY=your-kakao-pay-key
```

---

## 🐛 문제 발생 시

### DNS가 안 됨
- 30분 대기 후 재시도
- DNS 캐시 삭제: `sudo dscacheutil -flushcache` (Mac)

### SSL 인증서 오류
- Railway/Render: 5-10분 대기 후 자동 발급
- 강제 새로고침: Cmd+Shift+R (Mac), Ctrl+Shift+R (Win)

### CORS 오류
- `main.py` 확인: `allow_origins`에 도메인 포함 확인
- 서버 재시작

---

## 📞 지원
- 이메일: contact@seoulchess.club
- 자세한 문서: `DOMAIN_SETUP.md` 참고
