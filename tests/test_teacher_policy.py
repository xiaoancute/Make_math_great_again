from math_learning_graph.seed import load_seed_knowledge_points
from math_learning_graph.teacher import build_teacher_prompt


def test_teacher_prompt_uses_age_and_blocks_answer_only_style():
    point = next(
        item for item in load_seed_knowledge_points() if item.id == "function_intro"
    )

    prompt = build_teacher_prompt(point, student_age=12, question="函数为什么要存在？")

    assert "12岁" in prompt
    assert "先讲直觉" in prompt
    assert "不要直接给最终答案" in prompt
    assert "生活变化" in prompt
    assert "函数为什么要存在？" in prompt
