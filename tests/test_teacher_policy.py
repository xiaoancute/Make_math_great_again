from math_learning_graph.seed import load_seed_knowledge_points
from math_learning_graph.teacher import build_teacher_answer, build_teacher_prompt


def test_teacher_prompt_uses_age_and_blocks_answer_only_style():
    point = next(
        item for item in load_seed_knowledge_points() if item.id == "function_intro"
    )

    prompt = build_teacher_prompt(point, student_age=12, question="函数为什么要存在？")

    assert "12岁" in prompt
    assert "先讲直觉" in prompt
    assert "不要直接给最终答案" in prompt
    assert "不要假设学生理解术语" in prompt
    assert "先用人话解释" in prompt
    assert "不要用一个新术语解释另一个新术语" in prompt
    assert "术语解释" in prompt
    assert "输入" in prompt
    assert "输出" in prompt
    assert "生活变化" in prompt
    assert "函数为什么要存在？" in prompt


def test_teacher_answer_is_student_facing_and_explains_terms():
    point = next(
        item for item in load_seed_knowledge_points() if item.id == "function_intro"
    )

    answer = build_teacher_answer(point, student_age=12, question="函数为什么要存在？")

    assert "先用人话说" in answer
    assert "变量" in answer
    assert "输入" in answer
    assert "你现在卡住的是哪个词" in answer
