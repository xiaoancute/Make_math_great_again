from math_learning_graph.models import TopicMemoryInput
from math_learning_graph.openai_teacher import (
    OpenAITeacherClient,
    OpenAITeacherConfig,
    openai_teacher_from_env,
)
from math_learning_graph.service import MathLearningService


class FakeTeacher:
    def __init__(self, answer: str = "这是 AI 生成的讲解") -> None:
        self.answer = answer
        self.prompts: list[str] = []

    def generate_answer(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return self.answer


class BrokenTeacher:
    def generate_answer(self, prompt: str) -> str:
        raise RuntimeError("provider down")


def test_service_uses_configured_ai_teacher_with_learning_memory():
    teacher = FakeTeacher()
    service = MathLearningService.create_default(ai_teacher=teacher)

    response = service.teacher_answer(
        "linear_equation_one_variable",
        student_age=12,
        question="为什么移项要变号？",
        mastered_topic_ids={"equality"},
        memory_records=[
            TopicMemoryInput(
                topic_id="equality",
                mastery_level=3,
                review_count=2,
                lapse_count=0,
            ),
            TopicMemoryInput(
                topic_id="transposition",
                mastery_level=1,
                review_count=0,
                lapse_count=2,
            ),
        ],
    )

    assert response.answer == "这是 AI 生成的讲解"
    assert teacher.prompts
    assert "不要假设学生理解术语" in teacher.prompts[0]
    assert "等式：掌握等级 3" in teacher.prompts[0]
    assert "移项：掌握等级 1" in teacher.prompts[0]


def test_service_falls_back_to_local_teacher_when_ai_provider_fails():
    service = MathLearningService.create_default(ai_teacher=BrokenTeacher())

    response = service.teacher_answer(
        "function_intro",
        student_age=12,
        question="函数为什么要存在？",
    )

    assert "可以先这样理解" in response.answer
    assert "函数" in response.answer


def test_openai_teacher_client_uses_responses_api_and_output_text():
    calls = []

    class FakeResponses:
        def create(self, **kwargs):
            calls.append(kwargs)
            return type("Response", (), {"output_text": "真实模型回答"})()

    class FakeOpenAIClient:
        responses = FakeResponses()

    client = OpenAITeacherClient(
        OpenAITeacherConfig(api_key="test-key", model="test-model"),
        client_factory=lambda config: FakeOpenAIClient(),
    )

    assert client.generate_answer("请解释函数") == "真实模型回答"
    assert calls == [
        {
            "model": "test-model",
            "instructions": "你是一名耐心、严格、循序渐进的中文数学老师。",
            "input": "请解释函数",
        }
    ]


def test_openai_teacher_from_env_requires_model_name(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.delenv("OPENAI_MODEL", raising=False)

    assert openai_teacher_from_env() is None
