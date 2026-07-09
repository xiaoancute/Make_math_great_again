from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Protocol

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


def _create_openai_client(config: OpenAITeacherConfig) -> Any:
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("openai package is not installed") from exc
    return OpenAI(api_key=config.api_key)
