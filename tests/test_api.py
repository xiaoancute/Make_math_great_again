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
