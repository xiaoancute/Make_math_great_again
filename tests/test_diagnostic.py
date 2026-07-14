import pytest
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


def test_acing_everything_places_at_senior_level():
    items = load_diagnostic_items()
    answers = [
        DiagnosticAnswer(item_id=item.id, choice_index=item.correct_index) for item in items
    ]

    result = score_diagnostic(answers)

    assert result.level_rank >= 5
    assert "高中" in result.level_label


def test_failed_senior_probes_do_not_pollute_a_beginner():
    items = load_diagnostic_items()
    # A primary kid: solid on ranks 1-2, lost above that.
    answers = [
        DiagnosticAnswer(
            item_id=item.id,
            choice_index=item.correct_index
            if item.level_rank <= 2
            else (item.correct_index + 1) % len(item.choices),
        )
        for item in items
    ]

    result = score_diagnostic(answers)

    assert result.level_rank <= 3
    assert "derivative_intro" not in result.weak_topic_ids
    assert "set_concept" not in result.weak_topic_ids
    assert "导数" not in result.summary
    assert result.starter_topic_id == "linear_equation_one_variable"


def test_junior_only_client_submission_stays_version_tolerant():
    # An older app build only shows the six junior items; the senior bank must
    # be treated as unprobed, not weak.
    junior = [item for item in load_diagnostic_items() if item.level_rank <= 4]
    answers = [
        DiagnosticAnswer(item_id=item.id, choice_index=item.correct_index) for item in junior
    ]

    result = score_diagnostic(answers)

    assert result.total_count == len(junior)
    assert not any(t in result.weak_topic_ids for t in ("set_concept", "derivative_intro"))
    assert result.level_rank == 4


def test_acing_high_ranks_without_basics_stays_low():
    items = load_diagnostic_items()
    # Misreads the equals sign but answers the function probe correctly.
    answers = [
        DiagnosticAnswer(
            item_id=item.id,
            choice_index=item.correct_index
            if item.level_rank >= 4
            else (item.correct_index + 1) % len(item.choices),
        )
        for item in items
    ]

    result = score_diagnostic(answers)

    assert result.level_rank == 1
    assert result.starter_topic_id == "equality"


def test_summary_uses_chinese_names_not_topic_ids():
    items = load_diagnostic_items()
    wrong_first = [
        DiagnosticAnswer(
            item_id=items[0].id,
            choice_index=(items[0].correct_index + 1) % len(items[0].choices),
        )
    ]

    result = score_diagnostic(wrong_first, topic_names={"equality": "等式"})

    assert "等式" in result.summary
    assert "equality" not in result.summary


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


@pytest.mark.parametrize(
    "answers",
    [
        [
            DiagnosticAnswer(item_id="d_equality", choice_index=1),
            DiagnosticAnswer(item_id="d_equality", choice_index=1),
        ],
        [DiagnosticAnswer(item_id="missing", choice_index=0)],
        [DiagnosticAnswer(item_id="d_equality", choice_index=99)],
    ],
)
def test_score_rejects_invalid_answer_sets(answers):
    with pytest.raises(ValueError):
        score_diagnostic(answers)


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


def test_diagnostic_submit_api_rejects_duplicate_answers():
    client = TestClient(create_app())
    payload = {
        "answers": [
            {"item_id": "d_equality", "choice_index": 1},
            {"item_id": "d_equality", "choice_index": 1},
        ]
    }

    response = client.post("/diagnostic/submit", json=payload)

    assert response.status_code == 422


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
