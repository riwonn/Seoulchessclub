"""
Kakao Pay 결제 통합 모듈
"""
import os
import requests
from datetime import datetime
from typing import Dict, Any


class KakaoPayAPI:
    """카카오페이 API 클라이언트"""

    def __init__(self):
        self.admin_key = os.getenv("KAKAO_PAY_ADMIN_KEY")
        self.cid = os.getenv("KAKAO_PAY_CID", "TC0ONETIME")  # 테스트용 CID
        self.base_url = "https://open-api.kakaopay.com"

        if not self.admin_key:
            print("WARNING: KAKAO_PAY_ADMIN_KEY environment variable is not set.")

    def _get_headers(self) -> Dict[str, str]:
        """카카오페이 API 요청 헤더 생성"""
        return {
            "Authorization": f"DEV_SECRET_KEY {self.admin_key}",
            "Content-Type": "application/json"
        }

    def ready(
        self,
        partner_order_id: str,
        partner_user_id: str,
        item_name: str,
        quantity: int,
        total_amount: int,
        tax_free_amount: int = 0,
        approval_url: str = None,
        cancel_url: str = None,
        fail_url: str = None
    ) -> Dict[str, Any]:
        """
        카카오페이 결제 준비 API

        Args:
            partner_order_id: 가맹점 주문번호 (고유해야 함)
            partner_user_id: 가맹점 회원 ID
            item_name: 상품명
            quantity: 상품 수량
            total_amount: 총 금액
            tax_free_amount: 비과세 금액 (기본값: 0)
            approval_url: 결제 성공 시 리다이렉트 URL
            cancel_url: 결제 취소 시 리다이렉트 URL
            fail_url: 결제 실패 시 리다이렉트 URL

        Returns:
            카카오페이 응답 데이터
        """
        # 기본 URL 설정
        base_domain = os.getenv("BASE_DOMAIN", "http://localhost:8000")
        if not approval_url:
            approval_url = f"{base_domain}/payment/approve"
        if not cancel_url:
            cancel_url = f"{base_domain}/payment/cancel"
        if not fail_url:
            fail_url = f"{base_domain}/payment/fail"

        url = f"{self.base_url}/online/v1/payment/ready"

        payload = {
            "cid": self.cid,
            "partner_order_id": partner_order_id,
            "partner_user_id": partner_user_id,
            "item_name": item_name,
            "quantity": quantity,
            "total_amount": total_amount,
            "tax_free_amount": tax_free_amount,
            "approval_url": approval_url,
            "cancel_url": cancel_url,
            "fail_url": fail_url
        }

        try:
            response = requests.post(url, json=payload, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"카카오페이 결제 준비 실패: {e}")
            if hasattr(e.response, 'text'):
                print(f"응답 내용: {e.response.text}")
            raise

    def approve(
        self,
        tid: str,
        partner_order_id: str,
        partner_user_id: str,
        pg_token: str
    ) -> Dict[str, Any]:
        """
        카카오페이 결제 승인 API

        Args:
            tid: 결제 고유번호 (ready 응답에서 받은 값)
            partner_order_id: 가맹점 주문번호
            partner_user_id: 가맹점 회원 ID
            pg_token: 결제승인 요청 인증 토큰 (카카오페이에서 리다이렉트 시 제공)

        Returns:
            카카오페이 결제 승인 응답 데이터
        """
        url = f"{self.base_url}/online/v1/payment/approve"

        payload = {
            "cid": self.cid,
            "tid": tid,
            "partner_order_id": partner_order_id,
            "partner_user_id": partner_user_id,
            "pg_token": pg_token
        }

        try:
            response = requests.post(url, json=payload, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"카카오페이 결제 승인 실패: {e}")
            if hasattr(e.response, 'text'):
                print(f"응답 내용: {e.response.text}")
            raise

    def cancel(
        self,
        tid: str,
        cancel_amount: int,
        cancel_tax_free_amount: int = 0
    ) -> Dict[str, Any]:
        """
        카카오페이 결제 취소 API

        Args:
            tid: 결제 고유번호
            cancel_amount: 취소 금액
            cancel_tax_free_amount: 취소 비과세 금액 (기본값: 0)

        Returns:
            카카오페이 결제 취소 응답 데이터
        """
        url = f"{self.base_url}/online/v1/payment/cancel"

        payload = {
            "cid": self.cid,
            "tid": tid,
            "cancel_amount": cancel_amount,
            "cancel_tax_free_amount": cancel_tax_free_amount
        }

        try:
            response = requests.post(url, json=payload, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"카카오페이 결제 취소 실패: {e}")
            if hasattr(e.response, 'text'):
                print(f"응답 내용: {e.response.text}")
            raise

    def order_status(self, tid: str, partner_order_id: str, partner_user_id: str) -> Dict[str, Any]:
        """
        카카오페이 주문 조회 API

        Args:
            tid: 결제 고유번호
            partner_order_id: 가맹점 주문번호
            partner_user_id: 가맹점 회원 ID

        Returns:
            카카오페이 주문 조회 응답 데이터
        """
        url = f"{self.base_url}/online/v1/payment/order"

        payload = {
            "cid": self.cid,
            "tid": tid,
            "partner_order_id": partner_order_id,
            "partner_user_id": partner_user_id
        }

        try:
            response = requests.post(url, json=payload, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"카카오페이 주문 조회 실패: {e}")
            if hasattr(e.response, 'text'):
                print(f"응답 내용: {e.response.text}")
            raise


# 싱글톤 인스턴스
kakao_pay_client = KakaoPayAPI()
