from __future__ import annotations

from math_learning_graph.models import KnowledgePoint, PracticeTask, WorkedExample


def with_deep_scaffold(point: KnowledgePoint) -> KnowledgePoint:
    return point.model_copy(
        update={
            "conceptual_layers": point.conceptual_layers or default_layers(point),
            "worked_examples": point.worked_examples or default_worked_examples(point),
            "practice_ladder": point.practice_ladder or default_practice_ladder(point.name),
            "reflection_questions": point.reflection_questions
            or default_reflection_questions(point.name),
        },
    )


def default_layers(point: KnowledgePoint) -> list[str]:
    route_text = (
        "，".join(point.understanding_route[:4])
        if point.understanding_route
        else point.name
    )
    return [
        f"先用一句人话抓住它：{point.human_explanation}",
        f"再按顺序拆开：{route_text}。",
        f"最后回到课本词：看到“{point.name}”时，要能说出它在处理什么关系。",
    ]


def default_worked_examples(point: KnowledgePoint) -> list[WorkedExample]:
    scene = point.life_examples[0] if point.life_examples else f"自己举一个和{point.name}有关的例子"
    return [
        WorkedExample(
            title="从例子到概念",
            problem=scene,
            steps=[
                f"先说清楚例子里的对象：{scene}。",
                f"再把它翻译成人话：{point.human_explanation}",
                f"最后才写数学说法：这一步是在理解{point.name}，不是背一句定义。",
            ],
            answer_check="能换一个自己的例子，并指出同一个关系，就说明不是死记。",
        )
    ]


def default_practice_ladder(name: str) -> list[PracticeTask]:
    return [
        PracticeTask(
            level="看懂",
            prompt=f"用自己的话解释{name}在说什么。",
            goal="先确认概念入口，不急着套公式。",
        ),
        PracticeTask(
            level="会做",
            prompt=f"找一道课本例题，标出哪里用到了{name}。",
            goal="把概念和具体步骤连起来。",
        ),
        PracticeTask(
            level="迁移",
            prompt=f"换一个生活或图形场景，判断还能不能用{name}。",
            goal="检查是否能离开原题型继续使用。",
        ),
    ]


def default_reflection_questions(name: str) -> list[str]:
    return [
        f"如果不用{name}，这类问题会卡在哪里？",
        "我能不能说出每一步为什么成立，而不是只说下一步怎么算？",
        "这个知识以后会连接到哪个更大的问题？",
    ]


def scaffolded_fields(point: KnowledgePoint) -> list[str]:
    """Which teachable fields still carry auto-generated template text.

    Detects the fixed fingerprints the default_* builders leave behind, so the
    content debt is visible instead of hiding inside 'looks filled' topics.
    """
    fields: list[str] = []
    if point.conceptual_layers and point.conceptual_layers[0].startswith("先用一句人话抓住它："):
        fields.append("conceptual_layers")
    if point.worked_examples and point.worked_examples[0].title == "从例子到概念":
        fields.append("worked_examples")
    default_practice_prompt = f"用自己的话解释{point.name}在说什么。"
    if point.practice_ladder and point.practice_ladder[0].prompt == default_practice_prompt:
        fields.append("practice_ladder")
    if point.reflection_questions and point.reflection_questions[0] == (
        f"如果不用{point.name}，这类问题会卡在哪里？"
    ):
        fields.append("reflection_questions")
    return fields
