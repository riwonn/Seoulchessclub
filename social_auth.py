"""
소셜 로그인 (Apple, Kakao) 인증 서비스
"""
import httpx
import jwt
from jwt import PyJWKClient
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
import os
from dotenv import load_dotenv

load_dotenv()

# Apple 설정
APPLE_KEY_URL = "https://appleid.apple.com/auth/keys"
APPLE_ISSUER = "https://appleid.apple.com"
APPLE_CLIENT_ID = os.getenv("APPLE_CLIENT_ID", "com.yourcompany.communitycontrol")

# Kakao 설정
KAKAO_USER_INFO_URL = "https://kapi.kakao.com/v2/user/me"


async def verify_apple_token(identity_token: str) -> Dict[str, Any]:
    """
    Apple ID 토큰을 검증하고 사용자 정보를 추출합니다.
    
    Args:
        identity_token: Apple에서 발급받은 ID 토큰
    
    Returns:
        사용자 정보 딕셔너리 (sub, email 등)
    
    Raises:
        HTTPException: 토큰이 유효하지 않은 경우
    """
    try:
        # Apple의 공개 키를 가져와 토큰 검증
        jwks_client = PyJWKClient(APPLE_KEY_URL)
        signing_key = jwks_client.get_signing_key_from_jwt(identity_token)
        
        # 토큰 디코딩 및 검증
        decoded_token = jwt.decode(
            identity_token,
            signing_key.key,
            algorithms=["RS256"],
            audience=APPLE_CLIENT_ID,
            issuer=APPLE_ISSUER,
        )
        
        return decoded_token
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Apple ID token has expired",
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Apple ID token: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error verifying Apple token: {str(e)}",
        )


async def get_kakao_user_info(access_token: str) -> Dict[str, Any]:
    """
    카카오 액세스 토큰으로 사용자 정보를 조회합니다.
    
    Args:
        access_token: 카카오에서 발급받은 액세스 토큰
    
    Returns:
        사용자 정보 딕셔너리
    
    Raises:
        HTTPException: 토큰이 유효하지 않거나 API 호출 실패
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                KAKAO_USER_INFO_URL,
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
                },
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid Kakao access token",
                )
            
            user_data = response.json()
            
            # 카카오 응답 형식:
            # {
            #   "id": 123456789,
            #   "kakao_account": {
            #     "email": "user@example.com",
            #     "profile": {
            #       "nickname": "홍길동"
            #     }
            #   }
            # }
            
            return {
                "id": str(user_data.get("id")),
                "email": user_data.get("kakao_account", {}).get("email"),
                "name": user_data.get("kakao_account", {}).get("profile", {}).get("nickname"),
            }
            
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error connecting to Kakao API: {str(e)}",
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting Kakao user info: {str(e)}",
        )


def extract_apple_user_info(decoded_token: Dict[str, Any], user_info: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Apple 토큰과 사용자 정보에서 필요한 정보를 추출합니다.
    
    Args:
        decoded_token: 검증된 Apple ID 토큰
        user_info: Apple에서 제공하는 사용자 정보 (첫 로그인 시에만)
    
    Returns:
        사용자 정보 딕셔너리
    """
    # Apple ID (sub)는 필수
    apple_id = decoded_token.get("sub")
    email = decoded_token.get("email")
    
    # 첫 로그인 시 제공되는 사용자 정보
    name = None
    if user_info:
        full_name = user_info.get("name", {})
        first_name = full_name.get("firstName", "")
        last_name = full_name.get("lastName", "")
        name = f"{last_name}{first_name}".strip() or "Apple User"
    
    return {
        "id": apple_id,
        "email": email,
        "name": name or "Apple User",
    }

