from fastapi.testclient import TestClient

from math_learning_graph.api import create_app
from math_learning_graph.seed import load_knowledge_points
from math_learning_graph.service import MathLearningService


def test_service_exposes_complete_domain_framework():
    service = MathLearningService.create_default()

    domains = service.list_domains()

    assert [domain.id for domain in domains] == [
        "number_operations",
        "algebra_equations",
        "geometry",
        "functions",
        "statistics_probability",
        "mathematical_thinking",
        "modeling_applications",
    ]
    assert domains[0].primary_scope
    assert domains[0].junior_scope
    assert domains[0].common_breaks


def test_service_exposes_primary_to_junior_roadmap():
    service = MathLearningService.create_default()

    roadmap = service.list_roadmap()

    assert roadmap[0].id == "quantity_sense"
    assert roadmap[0].is_foundational
    assert any(item.id == "function_intro_path" for item in roadmap)
    assert any("fraction" in item.core_topic_ids for item in roadmap)


def test_service_includes_first_batch_textbook_detail_nodes():
    service = MathLearningService.create_default()

    topics = service.list_topics()
    topic_ids = {topic.id for topic in topics}

    assert len(topics) >= 75
    assert "number_comparison" in topic_ids
    assert "linear_equation_applications" in topic_ids
    assert "function_graph_reading" in topic_ids


def test_service_includes_high_school_textbook_nodes():
    service = MathLearningService.create_default()

    topics = service.list_topics()
    topic_ids = {topic.id for topic in topics}
    high_school_topics = [topic for topic in topics if topic.grade_band == "senior"]

    assert len(high_school_topics) >= 30
    assert {
        "set_concept",
        "function_properties_high_school",
        "trigonometric_functions",
        "sequence_arithmetic",
        "solid_geometry_spatial_relations",
        "conic_sections",
        "derivative_intro",
        "counting_principle",
        "normal_distribution",
    }.issubset(topic_ids)
    assert any(
        position.grade == "高中必修第一册"
        for topic in topics
        for position in topic.textbook_positions
    )
    assert any(
        position.grade == "高中选择性必修第三册"
        for topic in topics
        for position in topic.textbook_positions
    )


def test_high_school_topics_do_not_assume_new_terms_are_known():
    service = MathLearningService.create_default()

    high_school_topics = [topic for topic in service.list_topics() if topic.grade_band == "senior"]

    assert high_school_topics
    assert all(topic.term_explanations for topic in high_school_topics)
    assert all(len(topic.term_explanations) >= 3 for topic in high_school_topics)
    assert all("先把词说清楚" in topic.conceptual_layers[0] for topic in high_school_topics)
    assert all(
        any(
            "这个符号" in step or "这个词" in step
            for example in topic.worked_examples
            for step in example.steps
        )
        for topic in high_school_topics
    )


def test_all_topics_include_deep_learning_scaffold():
    service = MathLearningService.create_default()

    topics = service.list_topics()

    assert all(topic.conceptual_layers for topic in topics)
    assert all(topic.worked_examples for topic in topics)
    assert all(topic.practice_ladder for topic in topics)
    assert all(topic.reflection_questions for topic in topics)


def test_domain_and_roadmap_endpoints_return_framework():
    client = TestClient(create_app())

    domains_response = client.get("/domains")
    roadmap_response = client.get("/roadmap")

    assert domains_response.status_code == 200
    assert roadmap_response.status_code == 200
    assert domains_response.json()[0]["id"] == "number_operations"
    assert roadmap_response.json()[0]["id"] == "quantity_sense"


def test_teacher_prompt_endpoint_uses_topic_context():
    client = TestClient(create_app())

    response = client.get(
        "/topics/function_intro/teacher-prompt",
        params={"age": 12, "question": "函数为什么要存在？"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["topic_id"] == "function_intro"
    assert "12岁" in data["prompt"]
    assert "函数为什么要存在？" in data["prompt"]


def test_teacher_answer_endpoint_returns_student_facing_answer():
    client = TestClient(create_app())

    response = client.get(
        "/topics/function_intro/teacher-answer",
        params={"age": 12, "question": "函数为什么要存在？"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["topic_id"] == "function_intro"
    assert "【先弄懂这些词】" in data["answer"]
    assert data["answer"].index("【先弄懂这些词】") < data["answer"].index("【课本会怎么说】")
    assert "输入" in data["answer"]


def test_teacher_answer_endpoint_uses_mastered_learning_memory():
    client = TestClient(create_app())

    response = client.get(
        "/topics/linear_equation_one_variable/teacher-answer",
        params={
            "age": 12,
            "question": "一元一次方程为什么要这样解？",
            "mastered": "equality,arithmetic_operations",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["learning_profile"]["mastered"] == ["arithmetic_operations", "equality"]
    assert "transposition" in data["learning_profile"]["weak"]
    assert "等式" in data["answer"]
    assert "四则运算" in data["answer"]
    assert "可能要先补" in data["answer"]


def test_teacher_answer_post_endpoint_accepts_local_memory_records():
    client = TestClient(create_app())

    response = client.post(
        "/topics/linear_equation_one_variable/teacher-answer",
        json={
            "age": 12,
            "question": "为什么移项要变号？",
            "model": "test-model",
            "mastered": ["equality"],
            "memories": [
                {
                    "topic_id": "equality",
                    "mastery_level": 3,
                    "review_count": 2,
                    "lapse_count": 0,
                },
                {
                    "topic_id": "transposition",
                    "mastery_level": 1,
                    "review_count": 0,
                    "lapse_count": 2,
                },
            ],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["topic_id"] == "linear_equation_one_variable"
    assert "本机复习记录" in data["answer"]
    assert "移项" in data["answer"]
    assert "遗忘 2 次" in data["answer"]


def test_ai_status_endpoint_reports_missing_model_and_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    client = TestClient(create_app())

    response = client.post("/ai/status", json={"model": ""})

    assert response.status_code == 200
    data = response.json()
    assert data["backend"] == "ok"
    assert data["openai_key_configured"] is False
    assert data["model_configured"] is False
    assert data["ready"] is False


def test_ai_status_endpoint_accepts_request_model(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    client = TestClient(create_app())

    response = client.post("/ai/status", json={"model": "user-model"})

    assert response.status_code == 200
    data = response.json()
    assert data["openai_key_configured"] is True
    assert data["model"] == "user-model"
    assert data["model_source"] == "request"
    assert data["ready"] is True


def test_load_bearing_and_diagnostic_topics_have_real_content():
    # Ratchet: these topics are either top载重 prerequisites or diagnostic starters.
    # They must carry hand-written content, never depth.py template scaffolding.
    from math_learning_graph.depth import scaffolded_fields

    protected = {
        "number_recognition",
        "place_value_decimal_system",
        "integer_addition_subtraction",
        "multiplication_meaning",
        "arithmetic_operations",
        "division_meaning",
        "quantity_relationship",
        "decimal",
        "negative_number_intro",
        "rational_numbers",
        "measurement_units",
        "line_angle_basic",
        "distributive_property",
        "power_scientific_notation",
        "equality",
        "fraction",
        "linear_equation_one_variable",
        "transposition",
        "function_intro",
        "set_concept",
        "function_properties_high_school",
        "trigonometric_functions",
        "derivative_intro",
    }
    points = {p.id: p for p in load_knowledge_points()}
    still_templated = {
        topic_id: scaffolded_fields(points[topic_id])
        for topic_id in sorted(protected)
        if scaffolded_fields(points[topic_id])
    }
    assert not still_templated, f"protected topics using template content: {still_templated}"
