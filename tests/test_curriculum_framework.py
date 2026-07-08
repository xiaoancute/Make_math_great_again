from fastapi.testclient import TestClient

from math_learning_graph.api import create_app
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
    assert "先用人话说" in data["answer"]
    assert "输入" in data["answer"]
