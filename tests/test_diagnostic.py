from fastapi.testclient import TestClient

from math_learning_graph.api import create_app
from math_learning_graph.diagnostic import load_diagnostic_items, score_diagnostic
from math_learning_graph.models import DiagnosticAnswer
from math_learning_graph.seed import load_seed_knowledge_points
from math_learning_graph.teacher import build_teacher_prompt


def test_diagnostic_items_probe_real_topics():
    items = load_diagnostic_items()
    topic_ids = {point.id for point in load_seed_knowledge_points()}

    assert len(items) >= 5
    assert all(item.topic_id in topic_ids for item in items)
    assert all(0 <= item.correct_index < len(item.choices) for item in items)


def test_score_all_correct_reaches_function_band():
    items = load_diagnostic_items()
    answers = [
        DiagnosticAnswer(item_id=item.id, choice_index=item.correct_index) for item in items
    ]

    result = score_diagnostic(answers)

    assert result.correct_count == len(items)
    assert result.level_rank >= 3
    assert "function_intro" in result.known_topic_ids
    assert result.starter_topic_id


def test_score_all_wrong_starts_at_equality():
    items = load_diagnostic_items()
    answers = [
        DiagnosticAnswer(item_id=item.id, choice_index=(item.correct_index + 1) % len(item.choices))
        for item in items
    ]

    result = score_diagnostic(answers)

    assert result.correct_count == 0
    assert result.starter_topic_id == "equality"
    assert "equality" in result.weak_topic_ids
    assert "不默认" in result.summary or "术语" in result.summary


def test_diagnostic_api_hides_answer_key():
    client = TestClient(create_app())

    response = client.get("/diagnostic")

    assert response.status_code == 200
    data = response.json()
    assert data["title"]
    assert data["items"]
    assert "correct_index" not in data["items"][0]
    assert data["items"][0]["choices"]


def test_diagnostic_submit_api_returns_placement():
    client = TestClient(create_app())
    items = load_diagnostic_items()
    payload = {
        "answers": [
            {"item_id": items[0].id, "choice_index": items[0].correct_index},
            {
                "item_id": items[1].id,
                "choice_index": (items[1].correct_index + 1) % len(items[1].choices),
            },
        ]
    }

    response = client.post("/diagnostic/submit", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["level_label"]
    assert data["starter_topic_id"]
    assert "equality" in data["known_topic_ids"] or items[0].topic_id in data["known_topic_ids"]
    assert items[1].topic_id in data["weak_topic_ids"]


def test_teacher_prompt_includes_placement_or_zero_assumption():
    point = next(item for item in load_seed_knowledge_points() if item.id == "function_intro")

    bare = build_teacher_prompt(point, student_age=12, question="函数是啥？")
    placed = build_teacher_prompt(
        point,
        student_age=12,
        question="函数是啥？",
        placement_level="小学中段",
        placement_summary="建议先补分数与数量关系。",
    )

    assert "尚未摸底" in bare or "零基础术语" in bare
    assert "小学中段" in placed
    assert "建议先补分数" in placed
