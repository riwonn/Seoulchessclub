# 🌐 www.seoulchess.club 도메인 설정 가이드

이 문서는 Seoul Chess Club 서비스를 www.seoulchess.club 도메인으로 배포하는 방법을 안내합니다.

---

## 📋 목차

1. [DNS 설정](#1-dns-설정)
2. [호스팅 플랫폼별 도메인 연결](#2-호스팅-플랫폼별-도메인-연결)
3. [SSL 인증서 설정](#3-ssl-인증서-설정)
4. [환경 변수 확인](#4-환경-변수-확인)
5. [배포 및 테스트](#5-배포-및-테스트)

---

## 1. DNS 설정

### 도메인 등록 업체에서 DNS 레코드 추가

도메인을 구매한 곳(가비아, Cloudflare, GoDaddy 등)에서 다음 설정을 추가합니다:

#### Option A: CNAME 레코드 (Railway/Render 사용 시 권장)

| 타입 | 호스트명 | 값 | TTL |
|------|----------|-----|-----|
| CNAME | www | `your-app.railway.app` 또는 `your-app.onrender.com` | 3600 |
| CNAME | @ | `your-app.railway.app` 또는 `your-app.onrender.com` | 3600 |

#### Option B: A 레코드 (직접 서버 운영 시)

| 타입 | 호스트명 | 값 | TTL |
|------|----------|-----|-----|
| A | www | `서버 IP 주소` | 3600 |
| A | @ | `서버 IP 주소` | 3600 |

**참고**: `@`는 루트 도메인(seoulchess.club)을 의미하고, `www`는 서브도메인(www.seoulchess.club)을 의미합니다.

---

## 2. 호스팅 플랫폼별 도메인 연결

### Railway 사용 시

1. **Railway 대시보드 접속**
   - https://railway.app 로그인
   - 프로젝트 선택

2. **커스텀 도메인 추가**
   - Settings → Domains 탭
   - "Add Custom Domain" 클릭
   - `www.seoulchess.club` 입력
   - `seoulchess.club` 입력 (루트 도메인)

3. **DNS 확인 대기**
   - Railway가 자동으로 DNS 레코드를 확인
   - 보통 5-30분 소요 (DNS 전파 시간)

4. **SSL 인증서**
   - Railway가 자동으로 Let's Encrypt SSL 인증서 발급
   - HTTPS 자동 활성화

### Render 사용 시

1. **Render 대시보드 접속**
   - https://render.com 로그인
   - 서비스 선택

2. **커스텀 도메인 추가**
   - Settings → Custom Domain 섹션
   - "Add Custom Domain" 클릭
   - `www.seoulchess.club` 입력
   - `seoulchess.club` 입력 (선택사항)

3. **DNS 레코드 확인**
   - Render가 제공하는 CNAME 값 복사
   - 도메인 등록 업체 DNS 설정에서 CNAME 레코드 추가

4. **SSL 인증서**
   - Render가 자동으로 SSL 인증서 발급
   - 보통 1-2분 내 완료

### 직접 서버 운영 시 (VPS, AWS EC2 등)

1. **Nginx 설정**

`/etc/nginx/sites-available/seoulchess.club`:

```nginx
server {
    listen 80;
    server_name www.seoulchess.club seoulchess.club;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

활성화:
```bash
sudo ln -s /etc/nginx/sites-available/seoulchess.club /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

2. **Certbot으로 SSL 인증서 발급**

```bash
# Certbot 설치
sudo apt update
sudo apt install certbot python3-certbot-nginx

# SSL 인증서 발급
sudo certbot --nginx -d www.seoulchess.club -d seoulchess.club

# 자동 갱신 테스트
sudo certbot renew --dry-run
```

3. **방화벽 설정**

```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

---

## 3. SSL 인증서 설정

### Railway/Render (자동)
- 도메인 연결 후 자동으로 SSL 인증서 발급
- Let's Encrypt 사용
- 자동 갱신

### 직접 서버 (Certbot)
```bash
# 인증서 발급 (위 섹션 참고)
sudo certbot --nginx -d www.seoulchess.club -d seoulchess.club

# 인증서 확인
sudo certbot certificates

# 수동 갱신 (자동 갱신 실패 시)
sudo certbot renew
```

---

## 4. 환경 변수 확인

배포 전 다음 환경 변수들이 올바르게 설정되어 있는지 확인:

### 필수 환경 변수

```env
# 도메인 설정
BASE_DOMAIN=https://www.seoulchess.club

# 관리자 설정
ADMIN_ACCESS_CODE=your-secure-admin-code
ADMIN_EMAIL=admin@seoulchess.club

# JWT 설정
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production

# Twilio (SMS 인증)
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=your-twilio-phone-number

# Gemini API (챗봇)
GEMINI_API_KEY=your-gemini-api-key

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com

# Kakao Pay
KAKAO_PAY_ADMIN_KEY=your-kakao-pay-admin-key
KAKAO_PAY_CID=your-kakao-pay-cid
```

### Railway 환경 변수 설정

1. Railway 대시보드 → 프로젝트 선택
2. Variables 탭
3. 위 환경 변수들을 하나씩 추가

### Render 환경 변수 설정

1. Render 대시보드 → 서비스 선택
2. Environment → Environment Variables
3. 위 환경 변수들을 하나씩 추가

---

## 5. 배포 및 테스트

### Git Push로 자동 배포 (Railway/Render)

```bash
# 변경사항 커밋
git add .
git commit -m "Configure domain www.seoulchess.club"

# Railway 또는 Render에 푸시
git push origin main
```

Railway와 Render는 자동으로 배포를 시작합니다.

### 로컬 서버 재시작 (직접 운영 시)

```bash
# 현재 실행 중인 프로세스 종료
pkill -f "uvicorn main:app"

# 가상환경 활성화
source venv/bin/activate

# 서버 재시작
uvicorn main:app --host 0.0.0.0 --port 8000

# 또는 백그라운드로 실행
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &
```

### systemd로 서비스 등록 (권장)

`/etc/systemd/system/seoulchess.service`:

```ini
[Unit]
Description=Seoul Chess Club API
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/path/to/community_control_ai
Environment="PATH=/path/to/community_control_ai/venv/bin"
ExecStart=/path/to/community_control_ai/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

활성화:
```bash
sudo systemctl daemon-reload
sudo systemctl enable seoulchess
sudo systemctl start seoulchess
sudo systemctl status seoulchess
```

---

## 6. 배포 확인 및 테스트

### DNS 전파 확인

```bash
# DNS 조회
nslookup www.seoulchess.club
nslookup seoulchess.club

# 또는
dig www.seoulchess.club
dig seoulchess.club
```

### SSL 인증서 확인

브라우저에서 https://www.seoulchess.club 접속 후:
- 주소창의 자물쇠 아이콘 클릭
- 인증서 정보 확인
- "Let's Encrypt" 또는 유효한 CA 확인

### API 테스트

```bash
# Health check
curl https://www.seoulchess.club/health

# 예상 응답:
# {"status":"ok","service":"Seoul Chess Club API","version":"1.0.0","timestamp":"..."}

# CORS 테스트
curl -H "Origin: https://www.seoulchess.club" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS https://www.seoulchess.club/auth/login
```

---

## 7. 문제 해결

### DNS가 업데이트되지 않음

```bash
# DNS 캐시 플러시 (macOS)
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder

# DNS 캐시 플러시 (Windows)
ipconfig /flushdns

# DNS 캐시 플러시 (Linux)
sudo systemd-resolve --flush-caches
```

### SSL 인증서 오류

```bash
# Certbot 로그 확인
sudo tail -f /var/log/letsencrypt/letsencrypt.log

# Nginx 로그 확인
sudo tail -f /var/log/nginx/error.log
```

### CORS 오류

CORS 설정이 올바른지 확인:
- `main.py`의 `allow_origins` 리스트에 도메인 추가 확인
- 서버 재시작 후 테스트

---

## 8. 보안 체크리스트

배포 전 반드시 확인:

- [ ] `.env` 파일이 `.gitignore`에 포함되어 있음
- [ ] 프로덕션 환경에서 강력한 JWT 시크릿 키 사용
- [ ] 관리자 액세스 코드 변경
- [ ] Twilio, Gemini, Google, Kakao API 키가 실제 프로덕션 키로 설정됨
- [ ] HTTPS만 허용 (HTTP는 HTTPS로 리다이렉트)
- [ ] CORS 설정에서 특정 도메인만 허용 (`"*"` 사용 안 함)
- [ ] 데이터베이스 백업 설정
- [ ] 로그 모니터링 설정

---

## 9. 유지보수

### 로그 확인

```bash
# Railway
railway logs

# Render
# 대시보드에서 Logs 탭 확인

# 직접 서버
sudo journalctl -u seoulchess -f
```

### 데이터베이스 백업

```bash
# SQLite 백업
cp community_control.db community_control.db.backup.$(date +%Y%m%d)

# 자동 백업 스크립트 (cron)
# crontab -e
# 0 2 * * * /path/to/backup-script.sh
```

---

## 📞 지원

문제가 발생하면:
- Email: contact@seoulchess.club
- Website: https://www.seoulchess.club

---

**작성일:** 2025-11-29
**버전:** 1.0.0
