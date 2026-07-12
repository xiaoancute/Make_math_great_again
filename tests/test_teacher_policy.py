from math_learning_graph.models import LearningProfile
from math_learning_graph.seed import load_knowledge_points, load_seed_knowledge_points
from math_learning_graph.teacher import (
    SECTION_CHECK,
    SECTION_EXAMPLE,
    SECTION_FORMAL,
    SECTION_TERMS,
    SECTION_WHAT,
    SECTION_WHY,
    answer_section_order,
    build_teacher_answer,
    build_teacher_prompt,
    term_lines,
)


def test_teacher_prompt_requires_term_first_hard_order():
    point = next(
        item for item in load_seed_knowledge_points() if item.id == "function_intro"
    )

    prompt = build_teacher_prompt(point, student_age=12, question="函数为什么要存在？")

    assert "12岁" in prompt
    assert "不要假设学生已经知道" in prompt or "不要假设学生理解术语" in prompt
    assert "先用人话" in prompt or "先用人话解释" in prompt
    assert "不要用一个未解释的新术语解释另一个新术语" in prompt
    assert "不要直接给最终答案" in prompt
    assert SECTION_TERMS in prompt
    assert prompt.index(SECTION_TERMS) < prompt.index(SECTION_WHAT)
    assert prompt.index(SECTION_WHAT) < prompt.index(SECTION_FORMAL)
    assert "输入" in prompt
    assert "输出" in prompt
    assert "函数为什么要存在？" in prompt


def test_teacher_answer_puts_terms_before_concept_and_formal_definition():
    point = next(
        item for item in load_seed_knowledge_points() if item.id == "function_intro"
    )

    answer = build_teacher_answer(point, student_age=12, question="函数为什么要存在？")

    order = answer_section_order(answer)
    assert order[:5] == [
        SECTION_TERMS,
        SECTION_WHAT,
        SECTION_WHY,
        SECTION_EXAMPLE,
        SECTION_FORMAL,
    ]
    assert SECTION_CHECK in order

    terms_at = answer.index(SECTION_TERMS)
    what_at = answer.index(SECTION_WHAT)
    formal_at = answer.index(SECTION_FORMAL)
    assert terms_at < what_at < formal_at

    for term in point.term_explanations:
        assert term in answer
        # Each glossary term must appear in the terms section, not only later.
        assert term in answer[terms_at:what_at]

    assert "变量" in answer
    assert "输入" in answer


def test_teacher_answer_uses_learning_memory_names():
    point = next(
        item
        for item in load_seed_knowledge_points()
        if item.id == "linear_equation_one_variable"
    )
    profile = LearningProfile(
        topic_id="linear_equation_one_variable",
        mastered=["equality", "arithmetic_operations"],
        weak=["transposition"],
        future=["function_intro"],
    )

    answer = build_teacher_answer(
        point,
        student_age=12,
        question="一元一次方程为什么要这样解？",
        learning_profile=profile,
        topic_names={
            "equality": "等式",
            "arithmetic_operations": "四则运算",
            "transposition": "移项",
            "function_intro": "函数入门",
        },
    )

    assert "你的掌握记录" in answer
    assert "等式" in answer
    assert "四则运算" in answer
    assert "移项" in answer
    assert "函数入门" in answer
    assert answer.index(SECTION_TERMS) < answer.index(SECTION_FORMAL)


def test_every_seed_topic_has_teachable_terms():
    points = load_knowledge_points()
    missing = [point.id for point in points if not term_lines(point)]
    assert not missing
    # Prefer explicit glossary entries so teaching does not invent empty shells.
    empty_glossary = [point.id for point in points if not point.term_explanations]
    assert not empty_glossary, f"topics missing term_explanations: {empty_glossary}"
