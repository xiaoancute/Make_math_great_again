from fastapi.testclient import TestClient

from math_learning_graph.api import create_app


def test_topic_endpoint_returns_routes_and_human_explanation():
    client = TestClient(create_app())

    response = client.get("/topics/function_intro")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "function_intro"
    assert data["human_explanation"]
    assert data["understanding_route"]


def test_topic_endpoint_returns_deep_learning_scaffold():
    client = TestClient(create_app())

    response = client.get("/topics/fraction")

    assert response.status_code == 200
    data = response.json()
    assert any("单位1" in layer for layer in data["conceptual_layers"])
    assert data["worked_examples"][0]["steps"]
    assert "单位1" in " ".join(data["worked_examples"][0]["steps"])
    assert [task["level"] for task in data["practice_ladder"]] == ["看懂", "会做", "迁移"]
    assert data["reflection_questions"]


def test_learning_profile_endpoint_shows_knowledge_gaps():
    client = TestClient(create_app())

    response = client.get(
        "/profiles/linear_equation_one_variable",
        params={"mastered": "equality,arithmetic_operations"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["mastered"] == ["arithmetic_operations", "equality"]
    assert "transposition" in data["weak"]
