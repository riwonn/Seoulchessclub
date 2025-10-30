"""
JWT 토큰 기반 인증 시스템
"""
from datetime import datetime, timedelta
from typing import Optional
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import User, get_db
import os
from dotenv import load_dotenv

load_dotenv()

# JWT 설정
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7일

# HTTPBearer 스키마 (헤더에서 토큰 추출)
security = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    JWT 액세스 토큰 생성
    
    Args:
        data: 토큰에 포함할 데이터 (보통 user_id, phone_number 등)
        expires_delta: 토큰 만료 시간 (기본값: 7일)
    
    Returns:
        JWT 토큰 문자열
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def verify_token(token: str) -> dict:
    """
    JWT 토큰 검증 및 디코딩
    
    Args:
        token: JWT 토큰 문자열
    
    Returns:
        토큰에 포함된 페이로드 (user_id 등)
    
    Raises:
        HTTPException: 토큰이 유효하지 않거나 만료된 경우
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    현재 인증된 사용자 가져오기 (의존성 주입용)
    
    Authorization 헤더에서 Bearer 토큰을 추출하고 검증한 후,
    해당 사용자를 데이터베이스에서 조회하여 반환합니다.
    
    Args:
        credentials: HTTP Authorization 헤더 (Bearer 토큰)
        db: 데이터베이스 세션
    
    Returns:
        인증된 User 객체
    
    Raises:
        HTTPException: 토큰이 유효하지 않거나 사용자가 존재하지 않는 경우
    """
    token = credentials.credentials
    payload = verify_token(token)
    
    user_id: int = payload.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 데이터베이스에서 사용자 조회
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    선택적 인증 (토큰이 있으면 사용자 반환, 없으면 None 반환)
    
    공개 API에서 토큰이 있으면 추가 정보를 제공하고,
    없으면 기본 정보만 제공할 때 사용합니다.
    
    Args:
        credentials: HTTP Authorization 헤더 (Bearer 토큰, 선택)
        db: 데이터베이스 세션
    
    Returns:
        인증된 User 객체 또는 None
    """
    if credentials is None:
        return None
    
    try:
        token = credentials.credentials
        payload = verify_token(token)
        user_id: int = payload.get("user_id")
        
        if user_id is None:
            return None
        
        user = db.query(User).filter(User.id == user_id).first()
        return user
    except HTTPException:
        return None

