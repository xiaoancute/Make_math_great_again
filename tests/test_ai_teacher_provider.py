from math_learning_graph.models import ChatTurn, TopicMemoryInput
from math_learning_graph.openai_teacher import (
    OpenAITeacherClient,
    OpenAITeacherConfig,
    openai_teacher_from_env,
)
from math_learning_graph.service import MathLearningService
from math_learning_graph.teacher import (
    SECTION_CHECK,
    SECTION_EXAMPLE,
    SECTION_FORMAL,
    SECTION_TERMS,
    SECTION_WHAT,
    SECTION_WHY,
    answer_respects_term_first,
)

VALID_AI_ANSWER = "\n".join(
    [
        SECTION_TERMS,
        "等号：表示两边一样多。",
        SECTION_WHAT,
        "在讲两边保持相等。",
        SECTION_WHY,
        "为了在不知道某个量时继续推理。",
        SECTION_EXAMPLE,
        "像天平两边同时减去同样重量。",
        SECTION_FORMAL,
        "等式两边同时做相同运算，等式仍成立。",
        SECTION_CHECK,
        "你能说出为什么两边要做同样的事吗？",
    ]
)


class FakeTeacher:
    def __init__(self, answer: str = VALID_AI_ANSWER) -> None:
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

    assert response.answer == VALID_AI_ANSWER
    assert teacher.prompts
    assert "不要假设学生已经知道" in teacher.prompts[0]
    assert "【先弄懂这些词】" in teacher.prompts[0]
    assert "等式：掌握等级 3" in teacher.prompts[0]
    assert "移项：掌握等级 1" in teacher.prompts[0]


def test_service_falls_back_to_local_teacher_when_ai_provider_fails():
    service = MathLearningService.create_default(ai_teacher=BrokenTeacher())

    response = service.teacher_answer(
        "function_intro",
        student_age=12,
        question="函数为什么要存在？",
    )

    assert "【先弄懂这些词】" in response.answer
    assert response.answer.index("【先弄懂这些词】") < response.answer.index("【课本会怎么说】")
    assert "函数" in response.answer


def test_service_falls_back_when_ai_answer_breaks_term_first_order():
    service = MathLearningService.create_default(ai_teacher=FakeTeacher("这是 AI 生成的讲解"))

    response = service.teacher_answer(
        "function_intro",
        student_age=12,
        question="函数为什么要存在？",
    )

    assert response.answer != "这是 AI 生成的讲解"
    assert response.answer.index(SECTION_TERMS) < response.answer.index(SECTION_FORMAL)


def test_service_keeps_good_ai_answer_even_with_extra_intro_line():
    # A model answer with an intro line and no rigid six-header template is still
    # accepted as long as terms come before the formal definition.
    flexible_answer = "\n".join(
        [
            "好问题！我们一步步来。",
            SECTION_TERMS,
            "函数：一个量跟着另一个量变，一个输入只对一个输出。",
            SECTION_EXAMPLE,
            "打车费用跟着公里数变。",
            SECTION_FORMAL,
            "设 x、y 是两个变量，若对每个 x 都有唯一的 y 与之对应，则 y 是 x 的函数。",
        ]
    )
    service = MathLearningService.create_default(ai_teacher=FakeTeacher(flexible_answer))

    response = service.teacher_answer(
        "function_intro",
        student_age=35,
        question="函数为什么要存在？",
    )

    assert response.answer == flexible_answer


def test_answer_respects_term_first_gate():
    assert answer_respects_term_first(f"{SECTION_TERMS}\n词。\n{SECTION_FORMAL}\n定义。")
    assert answer_respects_term_first(f"{SECTION_TERMS}\n只有拆词也行。")
    assert not answer_respects_term_first("直接给定义，没有拆词。")
    formal_first = f"{SECTION_FORMAL}\n定义先出。\n{SECTION_TERMS}\n词后补。"
    assert not answer_respects_term_first(formal_first)


def test_followup_turn_accepts_free_dialogue_and_carries_history():
    free_reply = "对，你说的第二种理解是对的。那你试试：把 3 换成 5，等式还平衡吗？"
    teacher = FakeTeacher(free_reply)
    service = MathLearningService.create_default(ai_teacher=teacher)
    history = [
        ChatTurn(question="等式是啥？", answer="等式就是两边一样多，像天平。你觉得 5+3=8 平衡吗？"),
    ]

    response = service.teacher_answer(
        "equality",
        student_age=12,
        question="平衡，因为两边都是 8",
        history=history,
    )

    assert response.answer == free_reply
    assert response.source == "ai"
    prompt = teacher.prompts[0]
    assert "【之前的对话】" in prompt
    assert "等式就是两边一样多" in prompt
    assert "继续对话" in prompt
    assert "输出硬顺序" not in prompt
    assert "仍然必须先用人话拆词" in prompt


def test_opening_turn_still_requires_term_first_sections():
    teacher = FakeTeacher("直接聊天，没有任何拆词块。")
    service = MathLearningService.create_default(ai_teacher=teacher)

    response = service.teacher_answer(
        "equality",
        student_age=12,
        question="等式是啥？",
    )

    assert response.source == "local"
    assert SECTION_TERMS in response.answer
    assert "输出硬顺序" in teacher.prompts[0]


def test_followup_fallback_is_honest_not_a_lesson_redump():
    class FailingTeacher:
        def generate_answer(self, prompt: str) -> str:
            raise RuntimeError("provider down")

    service = MathLearningService.create_default(ai_teacher=FailingTeacher())
    history = [ChatTurn(question="等式是啥？", answer="像天平。")]

    response = service.teacher_answer(
        "equality",
        student_age=12,
        question="那移项呢？",
        history=history,
    )

    assert response.source == "local"
    assert "联系不上" in response.answer
    assert SECTION_FORMAL not in response.answer


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
            "instructions": (
                "你是一名耐心的中文数学老师。"
                "永远不要假设学生已经知道数学术语的意思；"
                "必须先用人话拆词，再讲到底在说什么关系，最后才给课本说法；"
                "不要用一个未解释的新术语解释另一个新术语。"
            ),
            "input": "请解释函数",
        }
    ]


def test_openai_teacher_from_env_requires_model_name(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.delenv("OPENAI_MODEL", raising=False)

    assert openai_teacher_from_env() is None
