from __future__ import annotations

from math_learning_graph.models import (
    ChatTurn,
    KnowledgePoint,
    LearningProfile,
    TopicMemoryInput,
)

# Fixed section headers — tests and clients rely on this order.
SECTION_TERMS = "【先弄懂这些词】"
SECTION_WHAT = "【到底在讲什么】"
SECTION_WHY = "【为什么会出现】"
SECTION_EXAMPLE = "【举个例子】"
SECTION_FORMAL = "【课本会怎么说】"
SECTION_CHECK = "【自己检查】"


def _join_or_default(values: list[str], default: str) -> str:
    text = "；".join(value for value in values if value)
    return text or default


def _topic_names(topic_ids: list[str], topic_names: dict[str, str]) -> list[str]:
    return [topic_names.get(topic_id, topic_id) for topic_id in topic_ids]


def _numbered(values: list[str]) -> str:
    return "\n".join(f"{index}. {value}" for index, value in enumerate(values, start=1))


def term_lines(point: KnowledgePoint) -> list[str]:
    """Plain-language glossary lines; never empty for a teachable topic."""
    if point.term_explanations:
        return [f"{term}：{explanation}" for term, explanation in point.term_explanations.items()]
    # Fallback still refuses to dump the formal name alone.
    plain = point.human_explanation or "先问：这个词在题里指什么、在比什么、在算什么。"
    return [f"{point.name}：{plain}"]


def terms_block(point: KnowledgePoint, bullet: str = "- ") -> str:
    return "\n".join(f"{bullet}{line}" for line in term_lines(point))


def _worked_examples_text(point: KnowledgePoint) -> str:
    if not point.worked_examples:
        return "没有固定例题时：先让学生自己举一个例子，再说清已知和所求，再动笔。"
    lines: list[str] = []
    for example in point.worked_examples[:2]:
        steps = "；".join(example.steps)
        lines.append(
            f"{example.title}：{example.problem}。步骤：{steps}。检查：{example.answer_check}"
        )
    return "\n".join(lines)


def _practice_ladder_text(point: KnowledgePoint) -> str:
    if not point.practice_ladder:
        return "看懂：解释关键词；会做：完成课本例题；迁移：换情境判断。"
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


def _placement_text(
    placement_level: str | None,
    placement_summary: str | None,
) -> str:
    if not placement_level and not placement_summary:
        return (
            "学生水平：尚未摸底。"
            "默认按零基础术语处理：任何数学词第一次出现都要用人话解释。"
        )
    level = placement_level or "已摸底"
    summary = placement_summary or ""
    return f"学生摸底水平：{level}。{summary}"


def _age_register(age: int) -> str:
    if age <= 9:
        return "对方是年幼的孩子：句子要短，多用能摸到的实物和生活场景，避免抽象记号。"
    if age <= 15:
        return "对方是中小学生：可以用课堂例子，但每个术语第一次出现仍要先用人话解释。"
    if age <= 22:
        return "对方是高中生或大学生：可以更快进入符号和推理，但依然先拆词，不堆黑话。"
    return "对方是成年自学者：语气平等务实，不要孩子气；但同样先把术语拆成人话再给正式说法。"


def _history_block(history: list[ChatTurn]) -> str:
    turns = history[-8:]  # ponytail: cap resent context; sessions run short in practice
    lines: list[str] = []
    for turn in turns:
        lines.append(f"学生：{turn.question}")
        lines.append(f"老师：{turn.answer}")
    return "【之前的对话】\n" + "\n".join(lines) + "\n"


_OPENING_FORMAT = f"""输出硬顺序（必须按这个写，不能跳）：
{SECTION_TERMS}
{SECTION_WHAT}
{SECTION_WHY}
{SECTION_EXAMPLE}
{SECTION_FORMAL}
{SECTION_CHECK}"""

_FOLLOWUP_FORMAT = """这是一次继续对话，不是新开一课：
- 顺着学生最新的话直接往下走，不要重复完整讲稿，也不要再套六段格式。
- 学生答对了就确认，并往深一层带；答错了先判断是卡在词还是卡在步骤，再给一个更小的问题。
- 新术语第一次出现时，仍然必须先用人话拆词。"""


def build_teacher_prompt(
    point: KnowledgePoint,
    student_age: int,
    question: str,
    learning_profile: LearningProfile | None = None,
    topic_names: dict[str, str] | None = None,
    memory_records: list[TopicMemoryInput] | None = None,
    placement_level: str | None = None,
    placement_summary: str | None = None,
    history: list[ChatTurn] | None = None,
) -> str:
    route = " -> ".join(point.understanding_route)
    examples = "；".join(point.life_examples)
    misconceptions = "；".join(point.misconceptions)
    hints = "；".join(point.ai_teaching_hints)
    conceptual_layers = "；".join(point.conceptual_layers)
    worked_examples = _worked_examples_text(point)
    practice_ladder = _practice_ladder_text(point)
    reflection_questions = "；".join(point.reflection_questions)
    terms = "；".join(term_lines(point))
    learning_memory = _learning_memory_text(learning_profile, topic_names, memory_records)
    placement = _placement_text(placement_level, placement_summary)
    conversation = _history_block(history) if history else ""
    output_format = _FOLLOWUP_FORMAT if history else _OPENING_FORMAT

    return f"""你是一名中文数学老师，对方是{student_age}岁的学习者。{_age_register(student_age)}

产品目标：让学生不在术语上犯困，先听懂「到底在讲什么」，再碰课本说法。

讲解主题：{point.name}
{placement}
{learning_memory}
{conversation}
学生问题：{question}

{output_format}

讲解规则：
1. 永远不要假设学生已经知道你用的数学术语是什么意思。
2. 第一次使用任何数学术语前，必须先用人话解释它在说什么。
3. 不要用一个未解释的新术语解释另一个新术语。
4. 先拆词，再讲关系，最后才给正式定义和公式。
5. 不要直接给最终答案，也不要只列公式。
6. 如果学生答错，先判断是卡在词还是卡在步骤，再给一个更小的问题。
7. 每次解释都要说明这个概念为什么存在，以及以后会用在哪里。
8. 如果掌握记录显示前置薄弱，先补前置词与关系，再回到当前问题。
9. 学生困惑时，先问「你卡在哪个词，还是卡在哪一步？」

材料（讲解时按需使用，术语必须最先出现）：
{SECTION_TERMS}
{terms}
{SECTION_WHAT}
{point.human_explanation}
{SECTION_WHY}
{point.why_needed}
生活例子：{examples}
理解路线：{route}
分层理解：{conceptual_layers}
例题拆解：{worked_examples}
练习阶梯：{practice_ladder}
自查问题：{reflection_questions}
常见错误：{misconceptions}
{SECTION_FORMAL}
{point.formal_definition}
讲解提示：{hints}
"""


def build_teacher_answer(
    point: KnowledgePoint,
    student_age: int,
    question: str,
    learning_profile: LearningProfile | None = None,
    topic_names: dict[str, str] | None = None,
    memory_records: list[TopicMemoryInput] | None = None,
    placement_level: str | None = None,
    placement_summary: str | None = None,
) -> str:
    """Deterministic local teacher: terms first, formal definition last among core blocks."""
    # ponytail: static lesson ignores age on purpose — register comes from the topic's
    # grade band; per-age adaptation is the AI path's job (see _age_register).
    _ = student_age
    examples = _join_or_default(
        point.life_examples,
        "自己找一个能数、能分、能比的例子。",
    )
    misconceptions = _join_or_default(
        point.misconceptions,
        "只记住说法或公式，却说不出它在处理什么关系。",
    )
    visuals = _join_or_default(
        point.visualization_methods,
        "画图、列表或用实物摆一摆。",
    )
    worked_examples = _worked_examples_text(point)
    reflection_questions = point.reflection_questions or [
        "这些词我能用人话讲吗？",
        "我能说出这节到底在讲什么关系吗？",
        "我能举一个自己的例子吗？",
    ]
    learning_memory = _learning_memory_text(learning_profile, topic_names, memory_records)
    placement = _placement_text(placement_level, placement_summary)
    formal = point.formal_definition or point.human_explanation
    what = point.human_explanation or f"这节在讲和「{point.name}」有关的一种数量或图形关系。"
    why = point.why_needed or "它是为了处理一类具体麻烦才出现的，不是凭空背的标题。"

    memory_block = f"\n{learning_memory}\n" if learning_memory else "\n"

    return f"""你问的是：{question}
{placement}
{memory_block}{SECTION_TERMS}
{terms_block(point)}

{SECTION_WHAT}
{what}

{SECTION_WHY}
{why}

{SECTION_EXAMPLE}
{examples}
如果觉得抽象，可以：{visuals}

跟着做一做：
{worked_examples}

{SECTION_FORMAL}
{formal}

容易混的地方：{misconceptions}

{SECTION_CHECK}
{_numbered(reflection_questions[:3])}"""


def answer_section_order(answer: str) -> list[str]:
    """Return section headers in the order they appear (for tests)."""
    headers = [
        SECTION_TERMS,
        SECTION_WHAT,
        SECTION_WHY,
        SECTION_EXAMPLE,
        SECTION_FORMAL,
        SECTION_CHECK,
    ]
    found = [(answer.find(header), header) for header in headers if header in answer]
    found.sort(key=lambda item: item[0])
    return [header for _, header in found]


def answer_respects_term_first(answer: str) -> bool:
    """North-star gate for an OPENING teacher answer: the plain-language terms block
    must be present and must come before the textbook definition. Looser than a fixed
    six-header template so a genuinely good model answer isn't discarded for an
    intro line or a reordered example — it only enforces 先词后事. Follow-up turns
    in a conversation are exempt (they are dialogue, not lectures)."""
    if SECTION_TERMS not in answer:
        return False
    if SECTION_FORMAL in answer:
        return answer.index(SECTION_TERMS) < answer.index(SECTION_FORMAL)
    return True


def build_followup_fallback(question: str) -> str:
    """When the AI teacher drops mid-conversation, be honest — don't re-dump the lesson."""
    return (
        f"你刚才说：{question}\n"
        "现在联系不上在线 AI 老师，接不上刚才的对话。\n"
        "别停下：回到上面的讲解，把【先弄懂这些词】再读一遍，"
        "然后照【自己检查】的问题自己答一轮；"
        "连上网之后接着问，我们会从你停下的地方继续。"
    )
