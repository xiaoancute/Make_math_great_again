"""First-run placement: probe what the student actually understands, not grade on paper."""

from __future__ import annotations

from collections.abc import Mapping

from math_learning_graph.models import (
    DiagnosticAnswer,
    DiagnosticItem,
    DiagnosticItemPublic,
    DiagnosticResult,
    DiagnosticSession,
)


def load_diagnostic_items() -> list[DiagnosticItem]:
    """Short ladder: each item checks a term/relationship, not exam tricks."""
    return [
        DiagnosticItem(
            id="d_equality",
            prompt="「等号 =」在说什么？",
            choices=[
                "左边算完了，右边是答案",
                "左右两边表示同样多，像天平平衡",
                "一定要把数加起来",
                "只是写在竖式中间的符号",
            ],
            correct_index=1,
            topic_id="equality",
            level_rank=1,
            probes="等号是不是被当成「得出答案」的提示",
        ),
        DiagnosticItem(
            id="d_fraction",
            prompt="把一个饼平均分成 4 块，拿走 1 块。这 1 块可以怎么说？",
            choices=[
                "就是 1，因为拿走了一块",
                "是 1/4：把整体当成 1，这一块是其中一份",
                "是 4/1，因为一共 4 块",
                "分数只在做题时用，生活里不用",
            ],
            correct_index=1,
            topic_id="fraction",
            level_rank=2,
            probes="单位1 和「几分之几」是不是清楚",
        ),
        DiagnosticItem(
            id="d_quantity",
            prompt="「小明比小红多 3 个苹果」这句话，核心在说什么？",
            choices=[
                "只要会加减就能算，不用想关系",
                "两个量在比多少，差是 3",
                "一定要用乘法",
                "这是几何问题",
            ],
            correct_index=1,
            topic_id="quantity_relationship",
            level_rank=2,
            probes="数量关系是不是听得懂",
        ),
        DiagnosticItem(
            id="d_equation",
            prompt="方程里的 x 是什么？",
            choices=[
                "一个必须背下来的神秘字母",
                "暂时还不知道的量，用符号占个位置",
                "永远等于 0",
                "只能表示长度",
            ],
            correct_index=1,
            topic_id="linear_equation_one_variable",
            level_rank=3,
            probes="未知数是不是被当成「背公式用的字母」",
        ),
        DiagnosticItem(
            id="d_transposition",
            prompt="解方程时「移项要变号」，本质在干什么？",
            choices=[
                "老师规定的口诀，背就行",
                "两边做同样的事，保持相等，只是写法变了",
                "把数字随便挪位置",
                "只有减法才能移项",
            ],
            correct_index=1,
            topic_id="transposition",
            level_rank=3,
            probes="移项是不是离开了「等式两边同样操作」",
        ),
        DiagnosticItem(
            id="d_function",
            prompt="「函数」这个词，最先该抓住哪一层意思？",
            choices=[
                "一个很难的高中公式名",
                "一个量变了，另一个量按规则跟着变，且一个输入只对一个输出",
                "只要有 x 和 y 就是函数",
                "必须先会画很复杂的图像",
            ],
            correct_index=1,
            topic_id="function_intro",
            level_rank=4,
            probes="函数是不是只剩定义句，没有输入输出画面",
        ),
        DiagnosticItem(
            id="d_set",
            prompt="「集合」这个词，最先该抓住哪一层意思？",
            choices=[
                "把一些确定的对象放在一起当成一个整体看，关键是说清「谁在里面、谁不在」",
                "就是一堆数字的另一种叫法",
                "必须写成花括号才算数学",
                "还没学过这个词，说不上来",
            ],
            correct_index=0,
            topic_id="set_concept",
            level_rank=5,
            probes="集合是不是只剩记号，没有「确定对象的整体」这层画面",
        ),
        DiagnosticItem(
            id="d_monotonic",
            prompt="「函数单调递增」在描述什么关系？",
            choices=[
                "图像必须是一条直线",
                "y 的值永远是正数",
                "在一段范围里，x 越大 y 跟着越大——两个量变化方向一致",
                "还没学过，说不上来",
            ],
            correct_index=2,
            topic_id="function_properties_high_school",
            level_rank=5,
            probes="单调性是不是被当成图形口诀，而不是两个量的变化关系",
        ),
        DiagnosticItem(
            id="d_sine",
            prompt="「sin（正弦）」最先该抓住什么？",
            choices=[
                "计算器上的一个按键，按了就有答案",
                "直角三角形里，锐角定了，对边与斜边的比也就定了——sin 说的就是这个比",
                "一串必须背下来的公式",
                "还没学过，说不上来",
            ],
            correct_index=1,
            topic_id="trigonometric_functions",
            level_rank=6,
            probes="三角函数是不是只剩按键和口诀，没有「角定则比定」的画面",
        ),
        DiagnosticItem(
            id="d_derivative",
            prompt="「导数」这个词，先抓哪一层意思？",
            choices=[
                "一个套公式算出来的结果，意义不重要",
                "某一瞬间变化有多快——像车速表指针读数，不是全程平均速度",
                "和斜率没有关系的全新概念",
                "还没学过，说不上来",
            ],
            correct_index=1,
            topic_id="derivative_intro",
            level_rank=6,
            probes="导数是不是只会求，说不出「瞬时变化率」的画面",
        ),
    ]


def public_diagnostic_session() -> DiagnosticSession:
    """Questions without correct answers — for the client UI."""
    return DiagnosticSession(
        title="先看看你卡在哪",
        intro=(
            "不是考试，也不是排名。"
            "就几道题，摸清哪些词你已经懂、哪些还容易懵。"
            "答完我们再决定从哪一课开始讲。"
        ),
        items=[
            DiagnosticItemPublic(
                id=item.id,
                prompt=item.prompt,
                choices=item.choices,
                topic_id=item.topic_id,
                level_rank=item.level_rank,
                probes=item.probes,
            )
            for item in load_diagnostic_items()
        ],
    )


def score_diagnostic(
    answers: list[DiagnosticAnswer],
    topic_names: Mapping[str, str] | None = None,
) -> DiagnosticResult:
    items = {item.id: item for item in load_diagnostic_items()}
    if not answers:
        return DiagnosticResult(
            level_label="还没摸底",
            level_rank=0,
            starter_topic_id="equality",
            known_topic_ids=[],
            weak_topic_ids=["equality"],
            summary="还没做摸底。默认从最基础的「等号在说什么」开始，绝不默认你会术语。",
            correct_count=0,
            total_count=len(items),
        )

    answered_ids = [answer.item_id for answer in answers]
    if len(answered_ids) != len(set(answered_ids)):
        raise ValueError("Diagnostic item ids must be unique")
    for answer in answers:
        item = items.get(answer.item_id)
        if item is None:
            raise ValueError(f"Unknown diagnostic item id: {answer.item_id}")
        if answer.choice_index >= len(item.choices):
            raise ValueError(f"Invalid choice index for diagnostic item: {answer.item_id}")

    known: list[str] = []
    wrong: list[str] = []
    correct_count = 0
    rank_results: dict[int, list[bool]] = {}

    for answer in answers:
        item = items[answer.item_id]
        is_correct = answer.choice_index == item.correct_index
        rank_results.setdefault(item.level_rank, []).append(is_correct)
        if is_correct:
            correct_count += 1
            if item.topic_id not in known:
                known.append(item.topic_id)
        elif item.topic_id not in wrong:
            wrong.append(item.topic_id)

    # Unanswered items are unprobed, not weak — an old client that only shows the
    # junior ladder must not get senior topics stamped into its weak list.
    level_rank, level_label = _level_from_ranks(rank_results)

    # Only frontier misses count as weak: a primary kid failing the derivative
    # probe hasn't "broken" anything — that rung just isn't theirs yet.
    topic_rank = {item.topic_id: item.level_rank for item in items.values()}
    weak = [t for t in wrong if topic_rank.get(t, 1) <= level_rank + 1]

    starter = _starter_topic(known, weak)
    summary = _summary(level_label, known, weak, starter, topic_names or {})

    return DiagnosticResult(
        level_label=level_label,
        level_rank=level_rank,
        starter_topic_id=starter,
        known_topic_ids=known,
        weak_topic_ids=weak,
        summary=summary,
        correct_count=correct_count,
        total_count=len(answers),
    )


_LEVEL_LABELS = {
    1: "小学起步",
    2: "小学中段",
    3: "小初衔接",
    4: "初中函数入门",
    5: "高中入门",
    6: "高中根基",
}


def _level_from_ranks(rank_results: dict[int, list[bool]]) -> tuple[int, str]:
    """Climb the ladder rung by rung: a rank counts once every rank below it is
    fully confirmed and it has at least one correct answer. Acing the function
    probe while misreading the equals sign does not make you 初中水平."""
    level = 1
    confirmed = 0
    for rank in sorted(rank_results):
        if rank > confirmed + 1:
            break
        results = rank_results[rank]
        if any(results):
            level = max(level, rank)
        if not all(results):
            break
        confirmed = rank
    return level, _LEVEL_LABELS[level]


def _starter_topic(known: list[str], weak: list[str]) -> str:
    ladder = [
        "equality",
        "fraction",
        "quantity_relationship",
        "linear_equation_one_variable",
        "transposition",
        "function_intro",
        "set_concept",
        "function_properties_high_school",
        "trigonometric_functions",
        "derivative_intro",
    ]
    for topic_id in ladder:
        if topic_id in weak:
            return topic_id
    for topic_id in ladder:
        if topic_id not in known:
            return topic_id
    return "derivative_intro"


def _summary(
    level_label: str,
    known: list[str],
    weak: list[str],
    starter: str,
    topic_names: Mapping[str, str],
) -> str:
    def show(topic_ids: list[str]) -> str:
        return "、".join(topic_names.get(t, t) for t in topic_ids)

    known_text = show(known) if known else "还没确认会的"
    weak_text = show(weak) if weak else "暂时没扫出大洞"
    starter_text = topic_names.get(starter, starter)
    return (
        f"摸底结果：大约在「{level_label}」。"
        f"看起来比较稳的有：{known_text}。"
        f"更该先补的是：{weak_text}。"
        f"建议下一课从「{starter_text}」相关内容开始；"
        "讲的时候仍会先拆词，不默认你会课本术语。"
    )


def placement_memory_text(result: DiagnosticResult | None) -> str:
    if result is None:
        return "学生还没做过水平摸底。第一次接触时，先用最白话，并主动问卡在哪个词。"
    return (
        f"摸底水平：{result.level_label}（{result.correct_count}/{result.total_count}）。"
        f"{result.summary}"
    )
