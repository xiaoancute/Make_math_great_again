from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Protocol

from math_learning_graph.models import AIStatusResponse

TEACHER_INSTRUCTIONS = "你是一名耐心、严格、循序渐进的中文数学老师。"


class TeacherClient(Protocol):
    def generate_answer(self, prompt: str) -> str: ...


@dataclass(frozen=True)
class OpenAITeacherConfig:
    api_key: str
    model: str


class OpenAITeacherClient:
    def __init__(
        self,
        config: OpenAITeacherConfig,
        client_factory: Callable[[OpenAITeacherConfig], Any] | None = None,
    ) -> None:
        self._config = config
        self._client = client_factory(config) if client_factory else _create_openai_client(config)

    def generate_answer(self, prompt: str) -> str:
        response = self._client.responses.create(
            model=self._config.model,
            instructions=TEACHER_INSTRUCTIONS,
            input=prompt,
        )
        return str(getattr(response, "output_text", "")).strip()


def openai_teacher_from_env(model: str | None = None) -> OpenAITeacherClient | None:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None
    selected_model = (model or os.getenv("OPENAI_MODEL", "")).strip()
    if not selected_model:
        return None
    return OpenAITeacherClient(OpenAITeacherConfig(api_key=api_key, model=selected_model))


def ai_status_from_env(model: str | None = None) -> AIStatusResponse:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    request_model = (model or "").strip()
    env_model = os.getenv("OPENAI_MODEL", "").strip()
    selected_model = request_model or env_model
    source = "request" if request_model else "environment" if env_model else "missing"
    return AIStatusResponse(
        backend="ok",
        openai_key_configured=bool(api_key),
        model_configured=bool(selected_model),
        model=selected_model,
        model_source=source,
        ready=bool(api_key and selected_model),
    )


def _create_openai_client(config: OpenAITeacherConfig) -> Any:
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("openai package is not installed") from exc
    return OpenAI(api_key=config.api_key)
