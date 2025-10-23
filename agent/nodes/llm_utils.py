import os
from typing import Any
from dotenv import load_dotenv
from llm import LLMFactory


def _get_env(key: str, default: str | None = None) -> str | None:
    value = os.getenv(key)
    if value is None:
        return default
    return value


def create_langchain_llm_from_env(prefix: str) -> Any:
    """
    환경변수에서 제공자/모델/옵션을 읽어 LangChain 호환 LLM을 생성한다.
    prefix가 있는 경우 `{PREFIX}_PROVIDER`, `{PREFIX}_MODEL`, `{PREFIX}_TEMPERATURE`를 우선 사용하며,
    없으면 전역 `LLM_PROVIDER`, `LLM_MODEL` 값을 사용한다.
    """
    load_dotenv()

    provider = _get_env(f"{prefix}_PROVIDER", _get_env("LLM_PROVIDER", "ollama"))
    model = _get_env(f"{prefix}_MODEL", _get_env("LLM_MODEL", "gemma3n:e4b"))

    # 선택적 파라미터들
    temperature_str = _get_env(f"{prefix}_TEMPERATURE", _get_env("LLM_TEMPERATURE", "0.0"))
    max_tokens_str = _get_env(f"{prefix}_MAX_TOKENS", _get_env("LLM_MAX_TOKENS", None))

    kwargs: dict[str, Any] = {}
    if temperature_str is not None:
        try:
            kwargs["temperature"] = float(temperature_str)
        except ValueError:
            pass
    if max_tokens_str is not None:
        try:
            kwargs["max_tokens"] = int(max_tokens_str)
        except ValueError:
            pass

    llm = LLMFactory.create(provider=provider, model=model, **kwargs)
    return llm.as_langchain_model()


