import pytest

from math_learning_graph.graph import KnowledgeGraph
from math_learning_graph.seed import load_seed_knowledge_points


def test_seed_graph_is_acyclic_and_orders_prerequisites_first():
    graph = KnowledgeGraph.from_points(load_seed_knowledge_points())

    order = graph.learning_order()

    assert graph.is_acyclic()
    assert order.index("equality") < order.index("linear_equation_one_variable")
    assert order.index("arithmetic_operations") < order.index("fraction")
    assert order.index("quantity_relationship") < order.index("function_intro")


def test_learning_profile_marks_mastered_weak_and_future_topics():
    graph = KnowledgeGraph.from_points(load_seed_knowledge_points())

    profile = graph.learning_profile(
        topic_id="linear_equation_one_variable",
        mastered_topic_ids={"equality", "arithmetic_operations"},
    )

    assert profile.topic_id == "linear_equation_one_variable"
    assert profile.mastered == ["arithmetic_operations", "equality"]
    assert "distributive_property" in profile.weak
    assert "transposition" in profile.weak
    assert "linear_equation_two_variables" in profile.future
    assert "function_intro" in profile.future


def test_missing_prerequisite_reference_is_rejected():
    points = load_seed_knowledge_points()
    broken = points[0].model_copy(update={"prerequisite_ids": ["missing_topic"]})

    with pytest.raises(ValueError, match="missing_topic"):
        KnowledgeGraph.from_points([broken, *points[1:]])


def test_seed_includes_textbook_aligned_primary_and_junior_topics():
    points = load_seed_knowledge_points()
    by_id = {point.id: point for point in points}

    assert len(points) >= 60
    assert by_id["number_recognition"].textbook_positions[0].grade == "一年级上册"
    assert by_id["rational_numbers"].textbook_positions[0].chapter == "第一章 有理数"
    assert by_id["quadratic_function"].textbook_positions[0].grade == "九年级上册"
    assert by_id["trigonometric_ratios"].textbook_positions[0].chapter == "第二十八章 锐角三角函数"
