"""
vLLM LLM 구현 (외부 서버 호출)
BaseLLM을 상속받아 HTTP로 vLLM 서버를 호출합니다.
"""
import os
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning
from .base_llm import BaseLLM


class VLLMLLM(BaseLLM):
    """
    vLLM LLM 구현 클래스
    
    SOLID 원칙:
    - 단일 책임 원칙(SRP): vLLM LLM 호출만 담당
    - 개방/폐쇄 원칙(OCP): BaseLLM 확장으로 구현
    - 리스코프 치환 원칙(LSP): BaseLLM으로 완전히 치환 가능
    """
    
    def _initialize(self) -> None:
        """서버 URL/검증/타임아웃 설정 초기화"""
        self.server_url = self.config.get('server_url') or os.getenv('VLLM_SERVER_URL')
        if not self.server_url:
            raise ValueError("vLLM 서버 URL이 필요합니다. (server_url 인자 또는 VLLM_SERVER_URL 환경변수)")
        self.verify = self.config.get('verify', True)
        self.timeout = self.config.get('timeout', 30)
        if not self.verify:
            urllib3.disable_warnings(InsecureRequestWarning)

    def __call__(self, prompt: str, *args, **kwargs):
        """vLLM 서버에 프롬프트를 전송하고 결과를 반환"""
        payload = {"prompt": prompt}
        payload.update(kwargs.pop('payload', {}))
        response = requests.post(
            f"{self.server_url}/generate",
            json=payload,
            timeout=self.timeout,
            verify=self.verify,
        )
        response.raise_for_status()
        return response.json()
