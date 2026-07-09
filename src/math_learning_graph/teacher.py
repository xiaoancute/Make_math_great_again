from __future__ import annotations

from math_learning_graph.models import KnowledgePoint, LearningProfile, TopicMemoryInput


def _join_or_default(values: list[str], default: str) -> str:
    text = "；".join(value for value in values if value)
    return text or default


def _topic_names(topic_ids: list[str], topic_names: dict[str, str]) -> list[str]:
    return [topic_names.get(topic_id, topic_id) for topic_id in topic_ids]


def _numbered(values: list[str]) -> str:
    return "\n".join(f"{index}. {value}" for index, value in enumerate(values, start=1))


def _worked_examples_text(point: KnowledgePoint) -> str:
    if not point.worked_examples:
        return "暂无固定例题；先让学生自己举例，再拆步骤。"
    lines: list[str] = []
    for example in point.worked_examples[:2]:
        steps = "；".join(example.steps)
        lines.append(
            f"{example.title}：{example.problem}。步骤：{steps}。检查：{example.answer_check}"
        )
    return "\n".join(lines)


def _practice_ladder_text(point: KnowledgePoint) -> str:
    if not point.practice_ladder:
        return "看懂：解释概念；会做：完成课本例题；迁移：换情境判断。"
    return "\n".join(
        f"- {task.level}：{task.prompt}（目标：{task.goal}）"
        for task in point.practice_ladder
    )


def _learning_memory_text(
    learning_profile: LearningProfile | None,
    topic_names: dict[str, str] | None,
    memory_records: list[TopicMemoryInput] | None = None,
) -> str:
    if learning_profile is None:
        return ""

    names = topic_names or {}
    mastered = _join_or_default(
        _topic_names(learning_profile.mastered, names),
        "暂时没有记录为已经懂的前置知识",
    )
    weak = _join_or_default(
        _topic_names(learning_profile.weak, names),
        "当前前置知识都已经标记为会",
    )
    future = _join_or_default(
        _topic_names(learning_profile.future[:5], names),
        "暂无后续关联知识",
    )
    memory_lines = _memory_record_lines(memory_records or [], names)
    return f"""你的掌握记录：
- 已经懂：{mastered}
- 可能要先补：{weak}
- 后面会用到：{future}
- 本机复习记录：{memory_lines}"""


def _memory_record_lines(
    memory_records: list[TopicMemoryInput],
    topic_names: dict[str, str],
) -> str:
    if not memory_records:
        return "暂无更细的复习记录"
    lines = []
    for record in sorted(memory_records, key=lambda item: item.topic_id)[:12]:
        name = topic_names.get(record.topic_id, record.topic_id)
        lines.append(
            f"{name}：掌握等级 {record.mastery_level}，"
            f"复习 {record.review_count} 次，遗忘 {record.lapse_count} 次"
        )
    return "；".join(lines)


def build_teacher_prompt(
    point: KnowledgePoint,
    student_age: int,
    question: str,
    learning_profile: LearningProfile | None = None,
    topic_names: dict[str, str] | None = None,
    memory_records: list[TopicMemoryInput] | None = None,
) -> str:
    route = " -> ".join(point.understanding_route)
    examples = "；".join(point.life_examples)
    misconceptions = "；".join(point.misconceptions)
    hints = "；".join(point.ai_teaching_hints)
    conceptual_layers = "；".join(point.conceptual_layers)
    worked_examples = _worked_examples_text(point)
    practice_ladder = _practice_ladder_text(point)
    reflection_questions = "；".join(point.reflection_questions)
    terms = "；".join(
        f"{term}：{explanation}" for term, explanation in point.term_explanations.items()
    )
    learning_memory = _learning_memory_text(learning_profile, topic_names, memory_records)

    return f"""你是一名面向{student_age}岁学生的数学老师。

讲解主题：{point.name}
学生问题：{question}
{learning_memory}

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
9. 如果掌握记录显示前置知识薄弱，先补前置知识，再回到当前问题。

推荐理解路线：{route}
入口解释：{point.human_explanation}
生活例子：{examples}
为什么需要：{point.why_needed}
正式定义：{point.formal_definition}
分层理解：{conceptual_layers}
例题拆解：{worked_examples}
练习阶梯：{practice_ladder}
自查问题：{reflection_questions}
常见错误：{misconceptions}
术语解释：{terms}
讲解提示：{hints}
"""


def build_teacher_answer(
    point: KnowledgePoint,
    student_age: int,
    question: str,
    learning_profile: LearningProfile | None = None,
    topic_names: dict[str, str] | None = None,
    memory_records: list[TopicMemoryInput] | None = None,
) -> str:
    route = " -> ".join(point.understanding_route)
    terms = "\n".join(
        f"- {term}：{explanation}"
        for term, explanation in point.term_explanations.items()
    )
    examples = _join_or_default(
        point.life_examples,
        "先自己举一个能数、能分、能比较的例子。",
    )
    misconceptions = _join_or_default(
        point.misconceptions,
        "只记住一句话或公式，但说不出它在解决什么问题。",
    )
    visuals = _join_or_default(
        point.visualization_methods,
        "先画图、列表或用实物摆出来。",
    )
    conceptual_layers = _numbered(point.conceptual_layers) or point.human_explanation
    worked_examples = _worked_examples_text(point)
    practice_ladder = _practice_ladder_text(point)
    reflection_questions = point.reflection_questions or [
        "我能不能用自己的话说明它表示什么？",
        "我能不能举一个自己的例子？",
        "我能不能说出这道题为什么要用它？",
    ]
    learning_memory = _learning_memory_text(learning_profile, topic_names, memory_records)

    return f"""你问的是：{question}
{learning_memory}

{point.name}可以先这样理解：{point.human_explanation}

它要解决的问题是：{point.why_needed}

可以按这个顺序学：{route}。
如果觉得抽象，可以先用这些方式表示出来：{visuals}

分层理解：
{conceptual_layers}

关键词：
{terms}

例子：{examples}

例题拆解：
{worked_examples}

练习阶梯：
{practice_ladder}

课本里的正式说法：{point.formal_definition}

常见误会：{misconceptions}

你可以用这三个问题检查自己是否真的懂了：
{_numbered(reflection_questions[:3])}"""
