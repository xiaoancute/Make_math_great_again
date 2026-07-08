from __future__ import annotations

from math_learning_graph.models import KnowledgePoint


def _join_or_default(values: list[str], default: str) -> str:
    text = "；".join(value for value in values if value)
    return text or default


def build_teacher_prompt(point: KnowledgePoint, student_age: int, question: str) -> str:
    route = " -> ".join(point.understanding_route)
    examples = "；".join(point.life_examples)
    misconceptions = "；".join(point.misconceptions)
    hints = "；".join(point.ai_teaching_hints)
    terms = "；".join(
        f"{term}：{explanation}" for term, explanation in point.term_explanations.items()
    )

    return f"""你是一名面向{student_age}岁学生的数学老师。

讲解主题：{point.name}
学生问题：{question}

讲解规则：
1. 先讲直觉，再讲术语，最后才给正式定义。
2. 不要直接给最终答案，也不要只列公式。
3. 如果学生答错，先判断错误原因，再给一个更小的问题引导。
4. 每次解释都要说明这个概念为什么存在，以及以后会用在哪里。
5. 学生忘记术语时，先用人话解释恢复记忆。
6. 不要假设学生理解术语。
   第一次使用数学术语前，先用人话解释它在说什么。
7. 不要用一个新术语解释另一个新术语。
   如果必须用前置概念，先退回去解释前置概念。
8. 学生困惑时，先问“你卡在哪个词，还是卡在哪一步？”，再继续讲。

推荐理解路线：{route}
入口解释：{point.human_explanation}
生活例子：{examples}
为什么需要：{point.why_needed}
正式定义：{point.formal_definition}
常见错误：{misconceptions}
术语解释：{terms}
讲解提示：{hints}
"""


def build_teacher_answer(point: KnowledgePoint, student_age: int, question: str) -> str:
    route = " -> ".join(point.understanding_route)
    terms = "\n".join(
        f"- {term}：{explanation}"
        for term, explanation in point.term_explanations.items()
    )
    examples = _join_or_default(point.life_examples, "先自己举一个能数、能分、能比较的例子。")
    misconceptions = _join_or_default(
        point.misconceptions,
        "只记住一句话或公式，但说不出它在解决什么问题。",
    )
    visuals = _join_or_default(point.visualization_methods, "先画图、列表或用实物摆出来。")

    return f"""你问的是：{question}

{point.name}可以先这样理解：{point.human_explanation}

它要解决的问题是：{point.why_needed}

可以按这个顺序学：{route}。如果觉得抽象，可以先用这些方式表示出来：{visuals}

关键词：
{terms}

例子：{examples}

课本里的正式说法：{point.formal_definition}

常见误会：{misconceptions}

你可以用这三个问题检查自己是否真的懂了：
1. 我能不能用自己的话说明它表示什么？
2. 我能不能举一个自己的例子？
3. 我能不能说出这道题为什么要用它？"""
