"""Extra primary/junior topics to densify the learning graph.

Content is original plain-language teaching text aligned with typical
Chinese compulsory-education math strands (number, algebra, geometry,
functions, statistics). It is NOT a copy of any commercial textbook page.
Structure references open knowledge-graph practice (prerequisite edges,
term glossary first) described in docs/content-sources.md.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping

from math_learning_graph.depth import (
    default_layers,
    default_practice_ladder,
    default_reflection_questions,
    default_worked_examples,
)
from math_learning_graph.models import (
    GradeBand,
    KnowledgePoint,
    PracticeTask,
    TextbookPosition,
    WorkedExample,
)

CURRICULUM = "人教版义务教育数学（理解扩充）"


def _position(grade: str, chapter: str, section: str) -> TextbookPosition:
    return TextbookPosition(
        curriculum=CURRICULUM,
        grade=grade,
        chapter=chapter,
        section=section,
    )


def _worked(title: str, problem: str, steps: list[str], check: str) -> WorkedExample:
    return WorkedExample(title=title, problem=problem, steps=steps, answer_check=check)


def _task(level: str, prompt: str, goal: str) -> PracticeTask:
    return PracticeTask(level=level, prompt=prompt, goal=goal)


def _point(
    *,
    topic_id: str,
    name: str,
    grade_band: GradeBand,
    grade: str,
    chapter: str,
    section: str,
    human: str,
    why: str,
    terms: Mapping[str, str],
    formal: str = "",
    prerequisites: Iterable[str] = (),
    next_topics: Iterable[str] = (),
    formulas: Iterable[str] = (),
    examples: Iterable[str] = (),
    route: Iterable[str] = (),
    misconceptions: Iterable[str] = (),
    visuals: Iterable[str] = (),
    exercise_types: Iterable[str] = (),
    conceptual_layers: Iterable[str] = (),
    worked_examples: Iterable[WorkedExample] = (),
    practice_ladder: Iterable[PracticeTask] = (),
    reflection_questions: Iterable[str] = (),
) -> KnowledgePoint:
    route_items = list(route)
    formal_text = formal or (
        f"在课本里，「{name}」用来描述：{human}"
    )
    point = KnowledgePoint(
        id=topic_id,
        name=name,
        grade_band=grade_band,
        textbook_positions=[_position(grade, chapter, section)],
        human_explanation=human,
        life_examples=list(examples),
        why_needed=why,
        formal_definition=formal_text,
        term_explanations=dict(terms),
        misconceptions=list(misconceptions)
        or [
            f"只背「{name}」这个词，却说不出它在处理什么关系。",
            "用一个没解释过的新词去解释另一个新词。",
        ],
        prerequisite_ids=list(prerequisites),
        next_ids=list(next_topics),
        formulas=list(formulas),
        visualization_methods=list(visuals) or ["画图", "列表", "举生活例子"],
        ai_teaching_hints=[
            "永远先拆词：学生可能不认识你随口说出的术语。",
            "先问：卡在哪个词，还是卡在哪一步？",
            "每用一个新符号，先说它代表什么。",
        ],
        exercise_types=list(exercise_types) or ["解释词", "举例子", "判断对错", "小步练习"],
        school_route=[grade, chapter, section],
        understanding_route=route_items
        or ["先弄懂词", "看在比什么/算什么", "举例子", "再看课本说法"],
    )
    return point.model_copy(
        update={
            "conceptual_layers": list(conceptual_layers) or default_layers(point),
            "worked_examples": list(worked_examples) or default_worked_examples(point),
            "practice_ladder": list(practice_ladder) or default_practice_ladder(name),
            "reflection_questions": list(reflection_questions)
            or default_reflection_questions(name),
        },
    )


def load_expanded_knowledge_points() -> list[KnowledgePoint]:
    p, j, b = GradeBand.PRIMARY, GradeBand.JUNIOR, GradeBand.BRIDGE
    return [
        # —— 小学：数与运算加厚 ——
        _point(
            topic_id="zero_and_placeholder",
            name="0 的意义与占位",
            grade_band=p,
            grade="一年级上册至二年级",
            chapter="1～20 的认识 / 100 以内的数",
            section="0 表示没有与占位",
            human="0 既可以表示「一个都没有」，也可以在多位数里占住某个位置，让别的数字站对地方。",
            why="没有 0 的占位，10、101、1001 这类数就写不清楚。",
            terms={
                "0": "可以表示没有；在多位数里也可以占位置。",
                "占位": "让数字站在正确的数位上，即使这一位是「空的」。",
            },
            formal="0 是自然数中表示「没有」的数；在十进制记数里也用于表示某数位上没有单位。",
            prerequisites=["number_recognition", "place_value_decimal_system"],
            next_topics=["integer_addition_subtraction", "decimal"],
            examples=["篮子里没有苹果写成 0", "305 的十位是 0，表示没有整十"],
            route=["没有", "写 0", "多位数空位", "占位", "读数"],
            misconceptions=["以为 0 没有用", "把 0 随便删掉导致数变了"],
            visuals=["空篮子", "数位表空格"],
            conceptual_layers=[
                "0 有两副面孔：一副说「一个都没有」（篮子里 0 个苹果），"
                "另一副在多位数里当「占位工」。",
                "占位是关键：305 里的 0 站在十位，宣告「没有整十，但位置得留住」，"
                "删掉它整个数就塌了。",
                "别把两副面孔搞混：单独一个 0 常表示没有，夹在数字中间的 0 多半在占位。",
            ],
            worked_examples=[
                _worked(
                    "为什么 305 不能写成 35",
                    "305 里的 0 在说什么？",
                    [
                        "先看百位：3 表示 3 个百。",
                        "十位是 0：表示「没有整十」，但位置还在。",
                        "个位 5：5 个一。",
                        "若删掉 0 变成 35，就只剩 3 个十和 5 个一，意思完全变了。",
                    ],
                    "能说出 0 在这里是占位，不是可有可无的装饰。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "用自己的话说：0 什么时候表示没有，什么时候表示占位？",
                    "分清两种用法。",
                ),
                _task("会做", "比较 204 和 240，指出 0 各在哪一位。", "结合数位。"),
                _task("迁移", "小数 2.05 里的 0 在占什么位置？", "把占位迁到小数。"),
            ],
            reflection_questions=[
                "如果没有 0，10 该怎么写？",
                "「没有」和「占位」有什么不同？",
            ],
        ),
        _point(
            topic_id="odd_even_numbers",
            name="奇数与偶数",
            grade_band=p,
            grade="一年级下册至二年级",
            chapter="分类与数的性质初步",
            section="单数双数",
            human="能两个两个正好分完的是偶数；会剩下 1 个的是奇数。",
            why="配对、整除、质数偶偶性等后面的性质都从这里起步。",
            terms={
                "偶数": "能平均分成两个一样多、且正好分完的整数（个位是 0、2、4、6、8）。",
                "奇数": "两个两个分会剩 1 个的整数（个位是 1、3、5、7、9）。",
            },
            formal="能被 2 整除的整数叫偶数；不能被 2 整除的整数叫奇数。",
            prerequisites=["number_recognition", "division_meaning"],
            next_topics=["factors_multiples", "integer_multiplication_division"],
            examples=["12 个同学两两握手刚好分完", "11 个苹果两个两个拿会剩 1 个"],
            route=["两个两个分", "分完或剩 1", "看个位", "奇偶名字"],
            visuals=["配对圈", "数轴上跳 2"],
            conceptual_layers=[
                "偶数是能两个两个刚好配对、分完不剩的数；奇数配到最后总剩 1 个落单。",
                "为什么看个位就行？整十、整百都能两两分完，能否配对只由个位那一位决定。",
                "别把奇偶和大小、正负混了：奇偶只问「能不能被 2 分完」，和数有多大无关。",
            ],
            worked_examples=[
                _worked(
                    "17 是奇数还是偶数",
                    "17 块糖两个两个地分，能分完吗？",
                    [
                        "两个两个地拿，拿 8 次拿走 16 块。",
                        "还剩 1 块，配不成对。",
                        "剩下 1 个，所以 17 是奇数；也可直接看个位 7 是奇数。",
                    ],
                    "能说出「看个位」和「两两配对」得到的是同一个结论。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "用配对的说法解释：为什么 6 是偶数、7 是奇数？",
                    "把奇偶还原成能不能两两分完。",
                ),
                _task("会做", "判断 20、25、38、41 各是奇数还是偶数。", "熟练用个位判断。"),
                _task(
                    "迁移",
                    "两个偶数相加，结果一定是奇数还是偶数？举例说说。",
                    "从定义推奇偶的运算规律。",
                ),
            ],
            reflection_questions=[
                "为什么判断奇偶只要看个位，不用管前面几位？",
                "0 是奇数还是偶数？说说你的理由。",
                "奇数加奇数，得到的是奇数还是偶数？",
            ],
        ),
        _point(
            topic_id="factors_multiples",
            name="因数与倍数",
            grade_band=p,
            grade="五年级上册",
            chapter="因数与倍数",
            section="因数、倍数、质数合数",
            human="如果 A 乘某整数正好得到 B，就说 A 是 B 的因数，B 是 A 的倍数。",
            why="约分、通分、最小公倍数、质因数分解都靠它。",
            terms={
                "因数": "能整除某个数的整数（在小学正整数范围内讨论）。",
                "倍数": "某个数乘整数得到的结果。",
                "质数": "大于 1，并且只有 1 和它本身两个因数的数。",
                "合数": "大于 1，并且因数超过两个的数。",
            },
            formal="若存在整数 k 使 a×k=b，则 a 是 b 的因数，b 是 a 的倍数。",
            prerequisites=["multiplication_meaning", "division_meaning", "odd_even_numbers"],
            next_topics=["gcd_lcm", "fraction_operations", "factorization"],
            formulas=["a | b 表示 a 整除 b（后续会见到）"],
            examples=["12 的因数有 1、2、3、4、6、12", "3 的倍数：3、6、9、12…"],
            route=["整除", "谁乘谁得谁", "列因数", "质数合数", "后面约分要用"],
            misconceptions=["把质数和奇数混为一谈", "以为 1 是质数"],
            visuals=["矩形拆分", "因数对"],
            conceptual_layers=[
                "因数和倍数是一对说法：3×4=12，就说 3、4 是 12 的因数，12 是它们的倍数。",
                "关键在「整除」：能除得干干净净、没有余数，才算得上因数和倍数的关系。",
                "别把质数和奇数混：质数是「只有 1 和自己两个因数」，9 是奇数却不是质数。",
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "用乘法说一说：为什么 6 是 24 的因数、24 是 6 的倍数？",
                    "把因数倍数还原成一句乘法。",
                ),
                _task("会做", "写出 24 的所有因数。", "成对地找，不漏不重。"),
                _task(
                    "迁移",
                    "一个数最小的倍数是它自己，那它最大的因数是谁？",
                    "从定义想清楚边界。",
                ),
            ],
            reflection_questions=[
                "为什么说因数和倍数总是成对出现，不能只说「3 是因数」？",
                "1 是所有数的因数吗？它自己有几个因数？",
                "质数和奇数，哪些地方像、哪些地方不一样？",
            ],
            worked_examples=[
                _worked(
                    "找 18 的因数",
                    "18 能被哪些正整数整除？",
                    [
                        "从 1 试到 18：1×18、2×9、3×6。",
                        "4 不行，5 不行…",
                        "写成从小到大：1、2、3、6、9、18。",
                        "成对出现，不容易漏。",
                    ],
                    "能成对列出，并说明「整除」是什么意思。",
                )
            ],
        ),
        _point(
            topic_id="gcd_lcm",
            name="最大公因数与最小公倍数",
            grade_band=p,
            grade="五年级上册",
            chapter="因数与倍数",
            section="最大公因数、最小公倍数",
            human="最大公因数是几个数「都能被整除」的数里最大的那个；最小公倍数是几个数「都能整除它」的数里最小的那个。",
            why="约分靠最大公因数，通分靠最小公倍数。",
            terms={
                "最大公因数": "几个数的公共因数里最大的。",
                "最小公倍数": "几个数的公共倍数里最小的。",
                "公约数": "几个数共同的因数。",
            },
            formal="正整数 a、b 的最大公因数记作 gcd(a,b)；最小公倍数记作 lcm(a,b)。",
            prerequisites=["factors_multiples", "fraction"],
            next_topics=["fraction_operations", "ratio"],
            examples=["12 和 18 的最大公因数是 6", "4 和 6 的最小公倍数是 12"],
            route=["先找因数/倍数", "找公共的", "取最大/最小", "用到约分通分"],
            visuals=["集合圈", "数轴标记倍数"],
            conceptual_layers=[
                "两个数各有一堆因数，挑出两边都有的、最大的那个，就是最大公因数。",
                "反过来，两个数各有一串倍数，挑出两边都有的、最小的那个，就是最小公倍数。",
                "一个往「小」处找（因数有限），一个往「大」处找（倍数无穷），别把方向搞反。",
            ],
            worked_examples=[
                _worked(
                    "12 和 18 的最大公因数",
                    "12 和 18 最大能同时被谁整除？",
                    [
                        "12 的因数：1、2、3、4、6、12。",
                        "18 的因数：1、2、3、6、9、18。",
                        "两边都有的是 1、2、3、6，最大的是 6。",
                    ],
                    "能说出为什么取「最大」的那个公因数，而不是随便一个。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "解释一下：为什么 1 一定是任何两个数的公因数？",
                    "理解公因数的含义。",
                ),
                _task("会做", "求 8 和 12 的最大公因数和最小公倍数。", "两个方向都会找。"),
                _task(
                    "迁移",
                    "把 6/8 约成最简分数，用的是最大公因数还是最小公倍数？",
                    "把它用到约分。",
                ),
            ],
            reflection_questions=[
                "最大公因数会不会比原来两个数还大？为什么？",
                "最小公倍数会不会比原来两个数都小？",
                "约分和通分，为什么一个用最大公因数、一个用最小公倍数？",
            ],
        ),
        _point(
            topic_id="time_and_elapsed",
            name="时间与经过时间",
            grade_band=p,
            grade="一年级下册至三年级",
            chapter="认识时间",
            section="时、分、秒与经过时间",
            human="时间是在说「什么时候」和「过了多久」；钟面把一圈分成 60 小格来量。",
            why="行程问题、作息和函数里的「自变量是时间」都要用。",
            terms={
                "时": "较大的时间单位，1 时 = 60 分。",
                "分": "1 分 = 60 秒。",
                "经过时间": "从开始到结束中间过了多久。",
            },
            formal="时间计量采用六十进制：1 时=60 分，1 分=60 秒。",
            prerequisites=["number_recognition", "measurement_units"],
            next_topics=["rate_speed_distance", "unit_conversion"],
            examples=["从 8:20 到 9:05 过了多久", "一节课 40 分钟"],
            route=["读钟面", "开始时刻", "结束时刻", "相减得经过", "注意借位 60"],
            misconceptions=["把时间当十进制直接减", "分针格数和分钟混淆"],
            visuals=["钟面", "时间线段"],
            conceptual_layers=[
                "时间有两问：一问「几点」（时刻），一问「过了多久」（经过时间），别混。",
                "钟面一圈 60 小格，满 60 分才进 1 时——是逢六十进一，不是逢十进一。",
                "算经过时间就是终点减起点；分位不够减时，向「时」借 1 当 60 分。",
            ],
            worked_examples=[
                _worked(
                    "从 8:20 到 9:05 过了多久",
                    "8:20 出门，9:05 到校，路上花了多久？",
                    [
                        "分位不够减：5 分减 20 分不够。",
                        "把 9:05 看成 8 时 65 分（借 1 时=60 分）。",
                        "8 时 65 分 − 8 时 20 分 = 45 分。",
                    ],
                    "能说清为什么借的是 60 分，而不是 10 分。",
                )
            ],
            practice_ladder=[
                _task("看懂", "为什么算时间不能像算钱那样直接十进制相减？", "认清六十进制。"),
                _task("会做", "8:00 上课，40 分钟后下课，几点几分？", "会算结束时刻。"),
                _task("迁移", "电影 19:50 开始，放映 2 时 20 分，几点结束？", "跨整时地算经过。"),
            ],
            reflection_questions=[
                "「8 时」说的是时刻，「8 小时」说的是时长，差在哪里？",
                "为什么钟面满 60 分就进 1 时，而不是满 100 分？",
                "跨过整时（比如从 8:50 到 9:10）算经过，容易错在哪一步？",
            ],
        ),
        _point(
            topic_id="money_calculation",
            name="人民币与简单计算",
            grade_band=p,
            grade="一年级下册至二年级",
            chapter="认识人民币",
            section="元角分与找零",
            human="钱是用「元、角、分」表示的数量；买东西是在做加减，找零是在算差。",
            why="小数、百分数折扣和实际应用都从货币量感长出来。",
            terms={
                "元": "人民币的基本单位。",
                "角": "1 元 = 10 角。",
                "找零": "付出的钱减去应付的钱。",
            },
            formal="人民币主单位是元，1 元=10 角=100 分。",
            prerequisites=["integer_addition_subtraction", "decimal"],
            next_topics=["decimal_operations", "percent"],
            examples=["3 元 5 角写成 3.5 元", "付 10 元买 6.5 元商品"],
            route=["认识面额", "换算", "合计", "找零"],
            visuals=["钱币图", "价签"],
            conceptual_layers=[
                "元、角、分是钱的三级单位：1 元=10 角，1 角=10 分，也是逢十进一。",
                "买东西是加法（把价钱合起来），找零是减法（付的钱减该付的钱）。",
                "用「元」做单位时，角落在小数点后第一位，所以 3 元 5 角=3.5 元。",
            ],
            worked_examples=[
                _worked(
                    "付 10 元买 6.5 元找多少",
                    "买一支笔 6.5 元，给 10 元，应找回多少？",
                    [
                        "找零 = 付的钱 − 该付的钱。",
                        "10 − 6.5 = 3.5（元）。",
                        "3.5 元就是 3 元 5 角。",
                    ],
                    "能把 3.5 元换成 3 元 5 角，说清小数点后第一位是角。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "为什么 2 元 3 角写成「元」是 2.3 元，不是 2.03 元？",
                    "对上小数位和单位。",
                ),
                _task("会做", "买 4.5 元和 2 元两样东西，一共多少钱？", "会把价钱相加。"),
                _task(
                    "迁移",
                    "带 20 元，买了 12.8 元的东西，还能再买 8 元的吗？",
                    "用找零判断够不够。",
                ),
            ],
            reflection_questions=[
                "为什么用「元」做单位时，角要写在小数点后面？",
                "找零算的是加法还是减法？为什么？",
                "1 角为什么等于 0.1 元，而不是 0.01 元？",
            ],
        ),
        _point(
            topic_id="bar_line_pie_charts",
            name="条形图、折线图与扇形图",
            grade_band=p,
            grade="四年级至六年级",
            chapter="统计",
            section="常见统计图",
            human="统计图是用图形高度、折线起伏或扇形大小，把「谁多谁少、怎么变化、占多少」一眼看出来。",
            why="不会读图，就读不懂新闻数据和函数图像的前身。",
            terms={
                "条形图": "用直条长短比数量。",
                "折线图": "用折线看随时间或顺序的变化。",
                "扇形图": "用圆的各块表示各部分占整体的多少。",
            },
            formal="条形统计图、折线统计图、扇形统计图是小学常见的数据直观表示方式。",
            prerequisites=["data_collection_chart", "average", "percent"],
            next_topics=["data_analysis", "probability"],
            examples=["各班人数条形图", "一周气温折线", "兴趣小组人数扇形"],
            route=["看标题", "看图例", "读数量", "比大小", "说结论"],
            misconceptions=["只看图形好看不看刻度", "扇形图当条形图比长短"],
            visuals=["三种图对照"],
            conceptual_layers=[
                "三种图各管一件事：条形图比多少，折线图看变化，扇形图看占比。",
                "选哪种图看你想说什么：比大小用条形，看趋势用折线，看部分占整体用扇形。",
                "扇形图整个圆代表全部（100%），各块加起来是一整圆，别拿它去比长短。",
            ],
            worked_examples=[
                _worked(
                    "该用哪种统计图",
                    "想展示一周每天的气温变化，选哪种图？",
                    [
                        "问题关键词是「变化」，气温随天数一天天变。",
                        "要看随时间的起伏，折线图最合适。",
                        "若只想比哪天最热，用条形图也行，但看趋势折线更清楚。",
                    ],
                    "能说出选折线是因为要看「变化趋势」，不是随手选的。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "读一张条形图前，为什么一定要先看纵轴的刻度？",
                    "刻度决定高低的含义。",
                ),
                _task("会做", "想看全班各种水果的喜欢人数各占几成，该用哪种图？", "按目的选图。"),
                _task(
                    "迁移",
                    "同一份数据，条形图和扇形图各更适合回答什么问题？",
                    "分清各图擅长什么。",
                ),
            ],
            reflection_questions=[
                "为什么扇形图适合看占比，却不适合读具体数量？",
                "折线图里线「陡」和「平」分别在说什么？",
                "看统计图时如果不看刻度，可能被误导成什么样？",
            ],
        ),
        _point(
            topic_id="median_mode_range",
            name="中位数、众数与极差",
            grade_band=b,
            grade="六年级至七年级",
            chapter="数据的分析",
            section="中位数、众数、极差",
            human="平均数会被极端值拉偏；中位数看「排在中间」的数；众数看「出现最多」的数；极差看最大最小差多少。",
            why="描述一组数据时，只记平均数往往不够。",
            terms={
                "中位数": "把数据按大小排好后，处在正中间的数。",
                "众数": "出现次数最多的数。",
                "极差": "最大值减最小值。",
            },
            formal="中位数、众数是描述数据集中趋势的统计量；极差描述离散程度的一种简单量。",
            prerequisites=["average", "data_collection_chart", "number_comparison"],
            next_topics=["data_analysis", "data_collection_description"],
            examples=["五次考试分数找中位数", "最受欢迎鞋码是众数"],
            route=["排序", "找中间", "数次数", "最大减最小", "和平均数对比"],
            misconceptions=["没排序就找中位数", "以为众数一定唯一"],
            conceptual_layers=[
                "平均数容易被一个特别大或特别小的数拉偏，于是有了别的看法。",
                "中位数看「排中间」，众数看「最常出现」，极差看「拉开多大」，各说一个侧面。",
                "中位数必须先排序再找中间；众数问哪个最多；极差只问差多少，别互相套用。",
            ],
            worked_examples=[
                _worked(
                    "找五次成绩的中位数",
                    "五次成绩 88、92、75、92、60，中位数是多少？",
                    [
                        "先从小到大排：60、75、88、92、92。",
                        "五个数，正中间是第 3 个：88。",
                        "顺便：众数是出现两次的 92，极差=92−60=32。",
                    ],
                    "能说出中位数为什么要先排序，不排序找的是假中间。",
                )
            ],
            practice_ladder=[
                _task("看懂", "为什么说平均数有时会「骗人」，中位数更稳？", "理解极端值的影响。"),
                _task("会做", "数据 3、3、5、8、100，分别求平均数和中位数。", "对比两者的差别。"),
                _task("迁移", "全班鞋码要进货，该看平均数、中位数还是众数？", "按用途选统计量。"),
            ],
            reflection_questions=[
                "一组数据里混进一个特别大的值，平均数和中位数谁受影响更大？",
                "众数一定只有一个吗？有没有可能一个都没有？",
                "极差大说明了什么？它又没告诉我们什么？",
            ],
        ),
        _point(
            topic_id="angle_measure",
            name="角的度量",
            grade_band=p,
            grade="四年级上册",
            chapter="角的度量",
            section="角度与量角器",
            human="角是从一点出发的两条射线张开的大小；用量角器可以量出张开多少度。",
            why="三角形内角、平行线、旋转都要用「角有多大」。",
            terms={
                "度": "量角大小的单位，记作 °。",
                "直角": "正好 90° 的角。",
                "平角": "180°，看起来像一条直线。",
                "周角": "360°，转一整圈。",
            },
            formal="角的度量单位是度，1 周角=360°，1 平角=180°，1 直角=90°。",
            prerequisites=["line_angle_basic"],
            next_topics=["triangle_basic", "parallel_lines", "rotation"],
            examples=["课桌角大约是直角", "打开的书本夹角"],
            route=["顶点", "两条边", "张开大小", "用量角器", "读度数"],
            visuals=["量角器", "活动角"],
            conceptual_layers=[
                "角量的是「两条边张开多大」，跟边画多长没关系，只看张口。",
                "把一整圈平均分成 360 份，每份是 1 度（1°），角就用它占几份来量。",
                "记住几个界标：直角 90°、平角 180°（成一条直线）、周角 360°（转一圈）。",
            ],
            worked_examples=[
                _worked(
                    "边长不同角却一样大",
                    "两个角张口一样，但一个的边画得长、一个短，谁大？",
                    [
                        "角量的是两条边张开的程度，不是边的长短。",
                        "边只是画出来指示方向，画多长都行。",
                        "所以这两个角一样大。",
                    ],
                    "能说出角的大小和边长无关，只看张开多少度。",
                )
            ],
            practice_ladder=[
                _task("看懂", "为什么把角的两条边延长，角的度数不变？", "抓住「张开」才是本质。"),
                _task(
                    "会做",
                    "一个角是 90°，另一个 45°，后者是前者的几分之几？",
                    "会比较角的大小。",
                ),
                _task(
                    "迁移",
                    "把一个周角平均分成 4 个相等的角，每个多少度？是什么角？",
                    "把度数用到分割。",
                ),
            ],
            reflection_questions=[
                "为什么角的大小和它两条边画多长没有关系？",
                "为什么一圈定成 360°，而直角正好是它的四分之一？",
                "平角看起来像一条直线，它和一条直线有什么不同？",
            ],
        ),
        _point(
            topic_id="parallel_perpendicular_primary",
            name="平行与垂直（小学）",
            grade_band=p,
            grade="四年级上册",
            chapter="平行四边形和梯形",
            section="平行线与垂线",
            human="同一平面内，永不相交的两条直线互相平行；相交成直角的两条直线互相垂直。",
            why="长方形、平行四边形、坐标系都建立在平行与垂直上。",
            terms={
                "平行": "同一平面内不相交，像铁轨。",
                "垂直": "相交成 90°。",
                "垂足": "两条线垂直时的交点。",
            },
            formal="在同一平面内不相交的两条直线互相平行；夹角为直角的两条直线互相垂直。",
            prerequisites=["line_angle_basic", "angle_measure"],
            next_topics=["parallelogram", "coordinate_plane", "parallel_lines"],
            examples=["本子的横线", "墙壁与地面"],
            route=["同一平面", "是否相交", "是否成直角", "画记号"],
            misconceptions=["看着「斜」就不是平行", "垂直必须横平竖直才算"],
            conceptual_layers=[
                "同一平面里，两条直线要么相交、要么永不相交；永不相交的叫平行。",
                "相交时如果夹角正好 90°，就叫垂直，是相交里最特殊的一种。",
                "别被「斜」骗了：两条斜线只要方向一致、永不相交，照样是平行。",
            ],
            worked_examples=[
                _worked(
                    "斜着的两条线也能平行",
                    "两条都朝右上斜、间距处处相等的线，平行吗？",
                    [
                        "平行的关键是「同一平面内永不相交」。",
                        "两条线方向一样、间距不变，延长下去永远碰不到头。",
                        "所以它们平行，跟摆得斜不斜没关系。",
                    ],
                    "能说出判断平行看「会不会相交」，不看摆得正不正。",
                )
            ],
            practice_ladder=[
                _task("看懂", "为什么说垂直是相交的一种特殊情况？", "理清垂直和相交的关系。"),
                _task("会做", "长方形相邻两条边是什么关系？相对两条边呢？", "在图形里认平行垂直。"),
                _task("迁移", "两条直线都垂直于同一条直线，它们之间是什么关系？", "推理出平行。"),
            ],
            reflection_questions=[
                "为什么说平行一定要强调「在同一平面内」？",
                "两条直线垂直时夹角是 90°，这时其余三个角各是多少？",
                "生活中哪些地方要用到垂直，哪些地方要用到平行？",
            ],
        ),
        _point(
            topic_id="translation_rotation_flip",
            name="平移、旋转与轴对称",
            grade_band=p,
            grade="二年级至五年级",
            chapter="图形的运动",
            section="平移旋转轴对称",
            human="平移是整体滑动不转身；旋转是绕一个点转；轴对称是像照镜子一样对折能重合。",
            why="全等、相似、函数图像变换都从「图形怎么动」开始。",
            terms={
                "平移": "方向和距离一定，形状方向不变地移动。",
                "旋转": "绕定点转动一定角度。",
                "轴对称": "沿一条直线对折后两边重合。",
            },
            formal="平移、旋转、轴对称是小学阶段基本的图形运动。",
            prerequisites=["geometric_figures_intro", "rectangle_square_features"],
            next_topics=["axis_symmetry", "rotation", "congruent_triangles"],
            examples=["电梯门平移", "钟面指针旋转", "蝴蝶翅膀对称"],
            route=["看怎么动", "有没有翻转", "对应点", "对应角"],
            visuals=["描点移动", "对折纸"],
            conceptual_layers=[
                "三种运动各有各的样子：平移是滑动，旋转是转圈，轴对称是对折照镜子。",
                "看运动就抓不变量：平移方向大小不变，旋转到中心距离不变，轴对称两边一样。",
                "关键区别：平移旋转不「翻面」，轴对称会左右翻过来，别把它们混成一类。",
            ],
            worked_examples=[
                _worked(
                    "电梯门是哪种运动",
                    "电梯门向右滑开，是平移、旋转还是轴对称？",
                    [
                        "门整体向右移，没有绕点转，也没翻面。",
                        "每个点都朝同一方向、移动同样远。",
                        "这正是平移的特征，所以是平移。",
                    ],
                    "能说出判断依据是「同方向、同距离、不转身」。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "用自己的话说清楚：平移和旋转最大的不同在哪？",
                    "抓住转不转身。",
                ),
                _task(
                    "会做",
                    "钟面上分针从 12 走到 3，是哪种运动？绕哪里转？",
                    "认出旋转和它的中心。",
                ),
                _task(
                    "迁移",
                    "正方形沿对角线对折两边能重合，说明它有什么？",
                    "把轴对称用到判断。",
                ),
            ],
            reflection_questions=[
                "平移、旋转、轴对称，哪些会让图形「翻面」，哪些不会？",
                "旋转一定要有一个中心点吗？没有中心还能转吗？",
                "一个图形可能同时有好几条对称轴吗？举个例子。",
            ],
        ),
        _point(
            topic_id="area_triangle_trapezoid",
            name="三角形与梯形的面积",
            grade_band=p,
            grade="五年级上册",
            chapter="多边形的面积",
            section="三角形、梯形面积",
            human="三角形面积可以想成「同样底高的平行四边形的一半」；梯形可以想成上下底平均后再乘高。",
            why="后面圆、组合图形、以及用面积理解乘法公式都会用到。",
            terms={
                "底": "当作底边的那条边。",
                "高": "从对角顶点到这条底边的垂直距离。",
                "梯形": "只有一组对边平行的四边形。",
            },
            formal="三角形面积 = 底×高÷2；梯形面积 = (上底+下底)×高÷2。",
            prerequisites=["area", "parallelogram", "parallel_perpendicular_primary"],
            next_topics=["primary_circle_features", "volume"],
            formulas=["S=ah/2", "S=(a+b)h/2"],
            examples=["三角形花坛占地", "梯形田埂"],
            route=["找底和高", "为什么除以 2", "拼补图形", "套公式"],
            misconceptions=["高不垂直也乱乘", "梯形只用一个底"],
            conceptual_layers=[
                "三角形面积不神秘：两个一样的三角形拼成平行四边形，它就是那一半。",
                "梯形面积=（上底+下底）×高÷2，其实是把上下底取平均，再当矩形算。",
                "无论哪个公式，高都必须垂直于所选的底，斜着的边不能当高。",
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "为什么三角形面积公式里要「÷2」？用拼图说一说。",
                    "把 ÷2 讲成两个三角形拼一个平行四边形。",
                ),
                _task(
                    "会做",
                    "上底 3、下底 5、高 4 的梯形，面积是多少？",
                    "会套梯形公式。",
                ),
                _task(
                    "迁移",
                    "把梯形的上底缩短到 0，它变成什么图形？公式还对吗？",
                    "看公式之间的联系。",
                ),
            ],
            reflection_questions=[
                "三角形和平行四边形，面积公式差在哪一步？为什么？",
                "梯形公式里为什么是上底加下底，再除以 2？",
                "如果高画歪了（不垂直于底），算出的面积会偏大还是偏小？",
            ],
            worked_examples=[
                _worked(
                    "三角形面积为什么除以 2",
                    "底 6、高 4 的三角形面积怎么想？",
                    [
                        "先想一个底 6、高 4 的平行四边形，面积 6×4=24。",
                        "对角线把它分成两个一样的三角形。",
                        "所以每个三角形是 24÷2=12。",
                        "公式 ah/2 就是这个意思。",
                    ],
                    "能说出「除以 2」来自两个全等三角形，不是硬背。",
                )
            ],
        ),
        _point(
            topic_id="circle_circumference_area",
            name="圆的周长与面积",
            grade_band=p,
            grade="六年级上册",
            chapter="圆",
            section="圆周长与圆面积",
            human="圆周长是绕圆一圈的长度；圆面积是圆面铺了多大。它们都和半径、圆周率有关。",
            why="扇形、圆柱、圆锥和很多实际测量都建立在圆上。",
            terms={
                "半径": "圆心到圆上任意一点的线段长。",
                "直径": "穿过圆心、两端在圆上的线段，是半径的 2 倍。",
                "圆周率": "任何圆的周长与直径的比，约是 3.14，记作 π。",
            },
            formal="C=2πr=πd；S=πr²。",
            prerequisites=["primary_circle_features", "area", "decimal_operations"],
            next_topics=["volume", "circle", "trigonometric_ratios"],
            formulas=["C=2πr", "S=πr²"],
            examples=["圆形花坛一圈多长", "圆桌面有多大"],
            route=["半径直径", "π 是比", "周长", "面积", "别混"],
            misconceptions=["周长面积公式套反", "半径直径混用"],
            conceptual_layers=[
                "圆周长量「绕一圈的边」，圆面积量「圆面盖住的地方」，一个是线一个是面。",
                "圆周率 π 是任何圆的周长除以直径，永远约 3.14，是圆的「身份密码」。",
                "别把公式套反：周长 C=2πr 只乘一次 r，面积 S=πr² 里 r 要平方。",
            ],
            worked_examples=[
                _worked(
                    "半径 5 的圆周长和面积",
                    "圆半径 5 厘米，周长和面积各是多少？（π 取 3.14）",
                    [
                        "周长 C=2πr=2×3.14×5=31.4（厘米）。",
                        "面积 S=πr²=3.14×5²=3.14×25=78.5（平方厘米）。",
                        "注意周长单位是厘米，面积单位是平方厘米。",
                    ],
                    "能说清周长为什么用一次 r、面积为什么 r 要平方。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "为什么说 π 是「圆的身份证」，任何圆都一样？",
                    "理解 π 是固定比值。",
                ),
                _task(
                    "会做",
                    "直径 10 的圆，周长是多少？（π 取 3.14）",
                    "会用直径算周长。",
                ),
                _task(
                    "迁移",
                    "两个圆半径一个 2、一个 4，面积差几倍？",
                    "看半径平方对面积的影响。",
                ),
            ],
            reflection_questions=[
                "周长和面积，为什么单位不一样（一个长度、一个面积）？",
                "半径变成 2 倍，周长变几倍？面积又变几倍？",
                "π 为什么不是 3.14 这么简单，而是除不尽的？",
            ],
        ),
        _point(
            topic_id="cuboid_cylinder_volume",
            name="长方体与圆柱的体积",
            grade_band=p,
            grade="五年级下册至六年级",
            chapter="长方体和圆柱",
            section="体积与容积",
            human="体积是物体占空间多大；长方体可想成「底面积×高」；圆柱也是「圆底面积×高」。",
            why="容积、密度和后面立体几何都要用体积直觉。",
            terms={
                "体积": "物体所占空间的大小。",
                "容积": "容器最多能装多少（从里面量）。",
                "底面积": "底面那一层的面积。",
            },
            formal="长方体体积 V=abh；圆柱体积 V=πr²h。",
            prerequisites=["volume", "circle_circumference_area", "area"],
            next_topics=["solid_geometry_spatial_relations"],
            formulas=["V=abh", "V=Sh", "V=πr²h"],
            examples=["纸箱能装多少", "水杯大约装多少毫升"],
            route=["占空间", "一层层累起来", "底面积", "乘高"],
            misconceptions=["体积容积单位混用", "圆柱当成长方体乱套"],
            conceptual_layers=[
                "体积是「占了多大空间」；把底面一层的面积，乘上叠了多高，就是体积。",
                "长方体体积=底面积×高=长×宽×高；圆柱换成圆底面积×高，思路一样。",
                "体积和容积像双胞胎：体积从外面量占多大，容积从里面量能装多少。",
            ],
            worked_examples=[
                _worked(
                    "圆柱体积怎么算",
                    "底面半径 2、高 5 的圆柱，体积是多少？（π 取 3.14）",
                    [
                        "先算圆底面积 S=πr²=3.14×2²=12.56。",
                        "再乘高：V=Sh=12.56×5=62.8。",
                        "本质就是「一层圆面积，叠 5 个高」。",
                    ],
                    "能说出圆柱体积和长方体一样，都是底面积乘高。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "为什么长方体和圆柱的体积都能写成「底面积×高」？",
                    "抓住一层层累起来的思路。",
                ),
                _task(
                    "会做",
                    "长 4、宽 3、高 2 的长方体，体积是多少？",
                    "会算长方体体积。",
                ),
                _task(
                    "迁移",
                    "同样底面积，一个高 2、一个高 6，体积差几倍？",
                    "看高对体积的影响。",
                ),
            ],
            reflection_questions=[
                "面积和体积，一个用平方单位、一个用立方单位，为什么？",
                "体积和容积说的是同一回事吗？一个盒子它俩会不会不同？",
                "把圆柱的高变成原来的 2 倍，体积变几倍？",
            ],
        ),
        _point(
            topic_id="word_problem_diagram",
            name="线段图与应用题",
            grade_band=p,
            grade="三年级至六年级",
            chapter="数学广角 / 实际问题",
            section="用线段图表征数量关系",
            human="线段图是把条件和问题画成线段长短，让「多多少、少多少、几倍」看得见。",
            why="方程应用、行程工程问题，先画清楚比硬套公式重要。",
            terms={
                "线段图": "用线段表示数量关系的图。",
                "单位量": "当作 1 份的那个量。",
                "问题": "题目要求的未知结果。",
            },
            formal="线段图是小学阶段表征应用题数量关系的常用工具。",
            prerequisites=["quantity_relationship", "integer_addition_subtraction", "fraction"],
            next_topics=[
                "equation_applications_primary",
                "rate_speed_distance",
                "primary_equation",
            ],
            examples=["甲比乙多 3 个", "乙是甲的 2 倍少 1"],
            route=["读题", "谁和谁比", "画线段", "标已知", "找所求"],
            misconceptions=["不标单位就画", "倍比和差比混在一根线上乱标"],
            visuals=["线段图模板"],
            conceptual_layers=[
                "线段图是把文字里的数量画成线段：谁长谁短、差多少、几倍，一眼看清。",
                "画图先定「单位量」——把当作 1 份的量画一段，别的量照它比着画。",
                "线段图不是答案，是脚手架：帮你把「多、少、倍」翻译成加减乘除。",
            ],
            worked_examples=[
                _worked(
                    "用线段图理清「甲比乙多 3」",
                    "甲有 8 个，甲比乙多 3 个，乙有几个？",
                    [
                        "先画乙一段，再画甲，甲比乙长出 3 那一截。",
                        "从图上看：乙 = 甲 − 多出来的 3。",
                        "8 − 3 = 5，乙有 5 个。",
                    ],
                    "能指着图说出「多 3」画在哪一段，为什么用减法。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "为什么应用题先画线段图，往往比直接列式更不容易错？",
                    "体会图把关系摆明。",
                ),
                _task(
                    "会做",
                    "乙是甲的 2 倍，甲有 4 个，用线段图求乙。",
                    "会画倍数关系。",
                ),
                _task(
                    "迁移",
                    "「甲比乙多 3」和「甲是乙的 2 倍」，线段图画法有何不同？",
                    "分清差比和倍比。",
                ),
            ],
            reflection_questions=[
                "线段图里的「一段」代表什么？为什么先要定好它？",
                "差关系（多几、少几）和倍数关系，在线段图上长得一样吗？",
                "画完线段图，怎么从图上看出该用加减还是乘除？",
            ],
        ),
        _point(
            topic_id="interest_simple",
            name="利息与百分数应用",
            grade_band=p,
            grade="六年级",
            chapter="百分数的应用",
            section="利息、折扣、税率初步",
            human="利息可以想成：本金按一定百分率，过一段时间「多出来」的钱。",
            why="把百分数从「会算」推进到「会解释生活里的涨跌」。",
            terms={
                "本金": "一开始存进去或借出的钱。",
                "利率": "利息占本金的百分率。",
                "利息": "额外得到或支付的钱。",
            },
            formal="单利利息 ≈ 本金 × 利率 × 时间（小学阶段的简化模型）。",
            prerequisites=["percent", "decimal_operations", "money_calculation"],
            next_topics=["linear_function", "rate_speed_distance"],
            formulas=["利息=本金×利率×时间"],
            examples=["存 1000 元，年利率 2%"],
            route=["本金", "百分之几", "时间", "多出来的钱", "本息和"],
            misconceptions=["利率和时间单位不匹配", "百分号当小数乱移"],
            conceptual_layers=[
                "利息是钱「过一段时间多出来的部分」：本金越大、利率越高、存得越久越多。",
                "利率是「利息占本金的百分之几」，年利率 2% 表示一年多出本金的 2%。",
                "算利息前先对齐单位：年利率就配「几年」，别拿年利率去乘月数。",
            ],
            worked_examples=[
                _worked(
                    "存 1000 元一年的利息",
                    "存入 1000 元，年利率 2%，存 1 年，利息是多少？",
                    [
                        "利息 = 本金 × 利率 × 时间。",
                        "1000 × 2% × 1 = 1000 × 0.02 = 20（元）。",
                        "一年后连本带息 = 1000 + 20 = 1020 元。",
                    ],
                    "能把 2% 换成 0.02，并说清为什么要乘时间。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "为什么本金一样时，存的时间越长利息越多？",
                    "理解时间的作用。",
                ),
                _task(
                    "会做",
                    "本金 500 元，年利率 3%，存 2 年，利息多少？",
                    "会代入公式。",
                ),
                _task(
                    "迁移",
                    "年利率 2%，如果只存半年，时间该写几？",
                    "对齐时间单位。",
                ),
            ],
            reflection_questions=[
                "利率写成 2%，直接当 2 来乘对不对？为什么？",
                "利息、本金、本息和，三个词分别指什么？",
                "为什么算利息一定要注意利率和时间的单位配套？",
            ],
        ),
        # —— 初中：代数与函数加厚 ——
        _point(
            topic_id="number_line",
            name="数轴",
            grade_band=j,
            grade="七年级上册",
            chapter="有理数",
            section="数轴",
            human="数轴是画成一条线的「数的家」：原点、正方向、单位长度定好后，每个有理数都有一个点。",
            why="绝对值、不等式、函数图像都建立在「数可以对应点」上。",
            terms={
                "原点": "表示 0 的那一点。",
                "正方向": "通常向右，表示越来越大的方向。",
                "单位长度": "从 0 到 1 的那段长度。",
            },
            formal="规定了原点、正方向和单位长度的直线叫做数轴。",
            prerequisites=["rational_numbers", "negative_number_intro"],
            next_topics=["absolute_value", "inequalities", "coordinate_plane"],
            examples=["温度计像竖着的数轴", "向东为正向西为负"],
            route=["画线", "定 0", "定方向", "定 1 的长度", "定点"],
            misconceptions=["负数方向画反", "单位长度忽大忽小"],
            conceptual_layers=[
                "数轴是把数排成一条线：定好原点、正方向、单位长度，每个数就有了家。",
                "有了数轴，抽象的数变成看得见的点：越往右越大，越往左越小。",
                "三要素缺一不可：没定单位长度，1 和 2 的距离忽大忽小，点就站不准。",
            ],
            worked_examples=[
                _worked(
                    "在数轴上找 −2",
                    "怎样在数轴上标出 −2 的位置？",
                    [
                        "先找原点 0，规定向右为正方向。",
                        "−2 是负的，要往原点左边数。",
                        "以单位长度为一步，向左走 2 步，那一点就是 −2。",
                    ],
                    "能说出为什么 −2 在 0 的左边，而不是右边。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "为什么说数轴的「原点、正方向、单位长度」缺一不可？",
                    "理解三要素的作用。",
                ),
                _task(
                    "会做",
                    "在数轴上标出 −3、0、2，看谁在最左边。",
                    "会定位正负数。",
                ),
                _task(
                    "迁移",
                    "温度计为什么可以看成竖着的数轴？0 在哪里？",
                    "把数轴迁到实际。",
                ),
            ],
            reflection_questions=[
                "为什么数轴上越往右的数越大？这是规定还是必然？",
                "如果单位长度画得忽大忽小，会带来什么问题？",
                "数轴上每个点都对应一个数吗？每个数都能找到点吗？",
            ],
        ),
        _point(
            topic_id="opposite_numbers",
            name="相反数",
            grade_band=j,
            grade="七年级上册",
            chapter="有理数",
            section="相反数",
            human="相反数是「离 0 一样远，但在数轴两边」的两个数；把符号对调就得到相反数。",
            why="减法要化成加法、解方程移项，都会用到相反数。",
            terms={
                "相反数": "只有符号不同的两个数，如 3 与 -3。",
                "互为相反数": "彼此是对方的相反数。",
            },
            formal="只有符号不同的两个数叫做互为相反数；0 的相反数是 0。",
            prerequisites=["number_line", "rational_numbers"],
            next_topics=["absolute_value", "rational_numbers"],
            examples=["前进 5 与后退 5", "盈利 8 与亏损 8"],
            route=["数轴对称", "符号", "0 的特殊", "运算里变号"],
            conceptual_layers=[
                "相反数是一对：离 0 一样远，却分站数轴两边，比如 3 和 −3。",
                "求相反数很简单——把符号对调：正变负、负变正，数字大小不动。",
                "0 是特例：它的相反数还是 0，因为它就站在原点上，两边都不偏。",
            ],
            worked_examples=[
                _worked(
                    "−5 的相反数是谁",
                    "−5 的相反数是什么？它们在数轴上什么位置？",
                    [
                        "把符号对调：−5 变成 +5。",
                        "所以 −5 的相反数是 5。",
                        "在数轴上，5 和 −5 离原点都是 5 个单位，分在两边。",
                    ],
                    "能说出相反数「离 0 一样远、方向相反」。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "为什么说 3 和 −3 是一对相反数，而不是随便两个数？",
                    "抓住离 0 等远、方向相反。",
                ),
                _task(
                    "会做",
                    "写出 7、−2、0 的相反数。",
                    "会对调符号。",
                ),
                _task(
                    "迁移",
                    "「盈利 8 元」记作 +8，那「亏损 8 元」怎么记？",
                    "用相反数表示相反意义。",
                ),
            ],
            reflection_questions=[
                "为什么 0 的相反数是它自己？",
                "一个数和它的相反数相加，结果是多少？为什么？",
                "「相反数」和「负数」是一回事吗？举个例子说说。",
            ],
        ),
        _point(
            topic_id="adding_subtracting_rational",
            name="有理数加减法",
            grade_band=j,
            grade="七年级上册",
            chapter="有理数",
            section="有理数的加减",
            human="有理数加减可以想成在数轴上向右（加正）或向左（加负）移动；减法等于加上相反数。",
            why="整式、方程、函数里的符号运算都从这里稳住。",
            terms={
                "同号": "两个数符号相同。",
                "异号": "两个数符号不同。",
                "绝对值大的数": "离 0 更远的那个，决定和的符号（异号时）。",
            },
            formal="a−b=a+(−b)；同号相加取相同符号并加绝对值，异号相加取绝对值较大者的符号并减绝对值。",
            prerequisites=["absolute_value", "opposite_numbers", "number_line"],
            next_topics=["algebraic_expression", "linear_equation_one_variable"],
            examples=["温度从 -3℃ 升高 5℃", "收支相抵"],
            route=["化成加法", "看同号异号", "算绝对值", "定符号"],
            misconceptions=["只减绝对值忘了符号", "减去负数时变号错"],
            conceptual_layers=[
                "加减可以在数轴上「走路」：加正数向右走，加负数向左走，走到哪是答案。",
                "同号相加，绝对值相加、符号不变；异号相加，绝对值相减、跟大的符号走。",
                "减法不用另学：减一个数等于加它的相反数，全部化成加法就统一了。",
            ],
            worked_examples=[
                _worked(
                    "−3 加 5 等于几",
                    "温度 −3℃ 升高 5℃，变成多少度？",
                    [
                        "−3 和 +5 异号，先比绝对值：5>3。",
                        "绝对值相减：5 − 3 = 2。",
                        "符号跟绝对值大的 +5 走，所以是 +2，即 2℃。",
                    ],
                    "能说出异号相加为什么是「相减」，符号又怎么定。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "为什么「减去一个数」可以变成「加上它的相反数」？",
                    "理解减法化加法。",
                ),
                _task(
                    "会做",
                    "计算 −7+3 和 −7−3。",
                    "区分同号异号。",
                ),
                _task(
                    "迁移",
                    "5−8 和 5+(−8) 结果一样吗？说说为什么。",
                    "把减法看成加相反数。",
                ),
            ],
            reflection_questions=[
                "同号相加和异号相加，符号的定法有什么不同？",
                "为什么把减法都改写成加法，运算反而更省心？",
                "−3−(−5) 里两个负号在做什么？结果是多少？",
            ],
        ),
        _point(
            topic_id="multiplying_dividing_rational",
            name="有理数乘除法",
            grade_band=j,
            grade="七年级上册",
            chapter="有理数",
            section="有理数的乘除",
            human="乘除先定符号：同号得正、异号得负；再把绝对值按整数乘除算。",
            why="整式乘法、科学记数法、负斜率函数都要用。",
            terms={
                "积的符号": "由因数符号决定：同正异负。",
                "倒数": "乘积为 1 的两个数互为倒数。",
            },
            formal="负负得正、异号得负；a÷b=a×(1/b)（b≠0）。",
            prerequisites=["adding_subtracting_rational", "fraction_operations"],
            next_topics=["power_scientific_notation", "algebraic_expression"],
            examples=["连续两次转向", "平均分配债务"],
            route=["先符号", "后绝对值", "除法变乘倒数", "0 不能做除数"],
            conceptual_layers=[
                "有理数乘除分两步：先定符号，再算绝对值，两步分开就不会乱。",
                "符号规则：同号得正、异号得负；负负得正，就是「相反的相反」回到正。",
                "除法不用单独学：除以一个数等于乘它的倒数，只是 0 永远不能当除数。",
            ],
            worked_examples=[
                _worked(
                    "(−4)×(−3) 为什么得正",
                    "计算 (−4)×(−3)，符号怎么定？",
                    [
                        "先看符号：两个都是负，同号得正。",
                        "再算绝对值：4 × 3 = 12。",
                        "合起来是 +12。负负得正就在这里。",
                    ],
                    "能分开说清「符号怎么来、数字怎么来」。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "为什么算有理数乘除要「先定符号，再算数字」？",
                    "理解两步分开。",
                ),
                _task(
                    "会做",
                    "计算 (−6)÷2 和 (−6)÷(−3)。",
                    "会定商的符号。",
                ),
                _task(
                    "迁移",
                    "6÷(−2) 和 6×(−1/2) 结果一样吗？为什么？",
                    "把除法看成乘倒数。",
                ),
            ],
            reflection_questions=[
                "「负负得正」用生活里的什么例子能说通？",
                "为什么 0 不能做除数？",
                "乘法和除法在「定符号」这件事上，规则一样吗？",
            ],
        ),
        _point(
            topic_id="scientific_notation",
            name="科学记数法",
            grade_band=j,
            grade="七年级上册",
            chapter="整式的加减",
            section="科学记数法",
            human=(
                "科学记数法是把很大或很小的数写成 a×10ⁿ 的样子，"
                "其中 a 在 1 到 10 之间，方便比大小和读写。"
            ),
            why="天文、微粒、计算器显示都会用这种写法。",
            terms={
                "科学记数法": "a×10ⁿ 的记法，1≤|a|<10，n 为整数。",
                "数量级": "大致由 10 的指数反映「有多大/多小」。",
            },
            formal="任一非零数可写成 a×10ⁿ（1≤|a|<10，n∈Z）的形式，称为科学记数法。",
            prerequisites=["power_scientific_notation", "decimal", "multiplying_dividing_rational"],
            next_topics=["real_numbers", "linear_function"],
            formulas=["3.0×10^8", "2.5×10^{-3}"],
            examples=["光速约 3×10⁸ m/s", "0.0025=2.5×10⁻³"],
            route=["移动小数点", "数位数得指数", "写 a", "检查范围"],
            conceptual_layers=[
                "科学记数法专治「太长的数」：写成 a×10ⁿ，一眼看出有多大或多小。",
                "规矩是 a 必须在 1 到 10 之间（含 1 不含 10），指数 n 记小数点搬了几位。",
                "大数用正指数（往左搬点），小数用负指数（往右搬点），别把方向弄反。",
            ],
            worked_examples=[
                _worked(
                    "把 30000 写成科学记数法",
                    "30000 用科学记数法怎么写？",
                    [
                        "把小数点从末尾往左搬到 3 后面：3.0000。",
                        "一共搬了 4 位，所以指数是 4。",
                        "写成 3×10⁴，检查 3 在 1 到 10 之间，符合。",
                    ],
                    "能说出指数 4 是「小数点搬了 4 位」，不是随便数的。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "为什么科学记数法规定 a 必须在 1 到 10 之间？",
                    "理解 a 的范围。",
                ),
                _task(
                    "会做",
                    "把 0.0025 写成科学记数法。",
                    "会处理小数。",
                ),
                _task(
                    "迁移",
                    "3×10⁵ 和 3×10³，哪个大？大多少倍？",
                    "用指数比大小。",
                ),
            ],
            reflection_questions=[
                "指数的正负，分别对应「大数」还是「小数」？",
                "写成 30×10³ 算不算标准的科学记数法？为什么？",
                "科学记数法为什么方便比较两个差很多倍的数？",
            ],
        ),
        _point(
            topic_id="formula_square_difference",
            name="平方差公式",
            grade_band=j,
            grade="八年级上册",
            chapter="整式的乘法",
            section="平方差公式",
            human="两数和乘两数差，结果等于它们的平方差：前面两项交叉的中间项会消掉。",
            why="因式分解、心算、后面的公式变形会反复用。",
            terms={
                "平方差": "两个数的平方相减。",
                "公式": "可以反复套用的标准写法。",
            },
            formal="(a+b)(a−b)=a²−b²。",
            prerequisites=["polynomial_multiplication", "distributive_property"],
            next_topics=["factorization", "formula_perfect_square"],
            formulas=["(a+b)(a-b)=a^2-b^2"],
            examples=["99×101", "(x+3)(x-3)"],
            route=["认出和与差", "交叉项抵消", "剩平方减平方", "验算展开"],
            misconceptions=["写成 a²+b²", "符号弄反"],
            conceptual_layers=[
                "平方差公式说的是：两数「和」乘两数「差」，正好等于两数的平方相减。",
                "为什么中间项没了？展开 (a+b)(a−b) 时 +ab 和 −ab 刚好抵消，剩 a²−b²。",
                "用它的信号是：看到「和 × 差」这种一正一负的结构，一步就能写出结果。",
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "用展开说明：为什么 (a+b)(a−b) 的中间项会消掉？",
                    "理解交叉项抵消。",
                ),
                _task(
                    "会做",
                    "用平方差公式算 (x+4)(x−4)。",
                    "会套公式。",
                ),
                _task(
                    "迁移",
                    "怎样用平方差公式快速心算 51×49？",
                    "把公式用到心算。",
                ),
            ],
            reflection_questions=[
                "为什么 (a+b)(a−b) 不等于 a²+b²？错在哪一步？",
                "平方差公式和普通的多项式乘法，是两回事还是一回事？",
                "什么样的两个式子相乘，才能用平方差公式？",
            ],
            worked_examples=[
                _worked(
                    "用平方差算 98×102",
                    "怎样心算 98×102？",
                    [
                        "看成 (100−2)(100+2)。",
                        "套公式得 100²−2²。",
                        "10000−4=9996。",
                        "说明公式在「少算中间交叉项」。",
                    ],
                    "能说明为什么中间项消失。",
                )
            ],
        ),
        _point(
            topic_id="formula_perfect_square",
            name="完全平方公式",
            grade_band=j,
            grade="八年级上册",
            chapter="整式的乘法",
            section="完全平方公式",
            human="两数和（或差）的平方，不只是两项平方相加，还要加上（或减去）它们乘积的 2 倍。",
            why="配方法、二次函数顶点式都靠完全平方。",
            terms={
                "完全平方式": "能写成某个式子平方的式子。",
                "中间项": "2ab 这一项，最容易漏。",
            },
            formal="(a±b)²=a²±2ab+b²。",
            prerequisites=["polynomial_multiplication", "formula_square_difference"],
            next_topics=["factorization", "quadratic_equation", "quadratic_function"],
            formulas=["(a+b)^2=a^2+2ab+b^2"],
            examples=["(x+1)²", "边长 a+b 的正方形面积"],
            route=["画正方形拆块", "两块矩形是 2ab", "不要漏中间", "展开验算"],
            misconceptions=["(a+b)²=a²+b²", "符号只改一项"],
            visuals=["正方形面积拆分"],
            conceptual_layers=[
                "完全平方公式的重点是那个「容易漏的中间项」：(a+b)²=a²+2ab+b²。",
                "为什么有 2ab？把边长 a+b 的正方形切成四块，两块是 a²、b²，两块是 ab。",
                "差的情形只改中间项符号：(a−b)²=a²−2ab+b²，两头的平方永远是正。",
            ],
            worked_examples=[
                _worked(
                    "(x+3)² 展开是什么",
                    "把 (x+3)² 展开。",
                    [
                        "首项平方：x²。",
                        "中间项是两数乘积的 2 倍：2×x×3=6x。",
                        "末项平方：3²=9。合起来 x²+6x+9。",
                    ],
                    "能说出 6x 这个中间项是怎么来的，别漏掉。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "为什么 (a+b)² 不等于 a²+b²？中间少了什么？",
                    "记住 2ab。",
                ),
                _task(
                    "会做",
                    "展开 (x−2)²。",
                    "会处理差的平方。",
                ),
                _task(
                    "迁移",
                    "用正方形切块图解释 (a+b)² 里的 2ab 从哪来。",
                    "把公式和面积对上。",
                ),
            ],
            reflection_questions=[
                "完全平方公式里的中间项 2ab，为什么最容易被漏掉？",
                "(a+b)² 和 (a−b)²，展开后差别只在哪一项？",
                "为什么无论 a、b 正负，(a+b)² 展开的首末两项都是正的？",
            ],
        ),
        _point(
            topic_id="linear_inequality_solving",
            name="一元一次不等式的解法",
            grade_band=j,
            grade="七年级下册",
            chapter="不等式与不等式组",
            section="解一元一次不等式",
            human="解不等式很像解方程，但有一条关键不同：两边同乘或同除一个负数时，不等号要反向。",
            why="取值范围、可行域、函数定义域都会用不等式语言。",
            terms={
                "解集": "所有使不等式成立的未知数取值的集合。",
                "不等号变向": "乘除负数时，大于变小于、小于变大于。",
            },
            formal="解一元一次不等式的步骤与方程类似，移项变号；乘除负数时不等号改变方向。",
            prerequisites=["inequalities", "linear_equation_one_variable", "number_line"],
            next_topics=["inequality_systems", "function_intro"],
            examples=["2x+1>5", "−3x≥6"],
            route=["化简", "移项", "系数化为 1", "注意负数", "数轴表示"],
            misconceptions=["乘负数忘变向", "解集不会在数轴上表示"],
            conceptual_layers=[
                "解不等式的步骤和解方程几乎一样：移项、合并、把未知数系数化成 1。",
                "唯一要盯紧的差别：两边同乘或同除一个负数，不等号必须掉头（大变小）。",
                "答案不是一个数而是一片范围（解集），常用数轴画出来看得更清楚。",
            ],
            worked_examples=[
                _worked(
                    "解 −3x≥6 为什么要变号",
                    "解不等式 −3x≥6。",
                    [
                        "两边同除以 −3，把 x 的系数化成 1。",
                        "除的是负数，不等号掉头：≥ 变成 ≤。",
                        "得到 x≤−2。",
                    ],
                    "能说清为什么除以负数时不等号要反向。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "解不等式和解方程，最关键的一步差别在哪？",
                    "锁定变号规则。",
                ),
                _task(
                    "会做",
                    "解 2x+1>5。",
                    "会做不变号的情形。",
                ),
                _task(
                    "迁移",
                    "解 −x<3，并在数轴上表示解集。",
                    "会变号并画数轴。",
                ),
            ],
            reflection_questions=[
                "为什么两边同乘正数不变号，同乘负数就要变号？",
                "不等式的解和方程的解，一个是范围一个是点，为什么不同？",
                "在数轴上表示解集时，空心点和实心点分别表示什么？",
            ],
        ),
        _point(
            topic_id="systems_substitution_addition",
            name="代入法与加减法解方程组",
            grade_band=j,
            grade="七年级下册",
            chapter="二元一次方程组",
            section="代入法、加减法",
            human="代入法是从一个方程解出一个未知数，塞进另一个方程；加减法是让某个未知数系数相反再相加消掉。",
            why="这是「消元」思想：把两个未知变成一个未知。",
            terms={
                "消元": "想办法去掉一个未知数。",
                "代入": "用等于的式子去替换。",
                "加减消元": "两式相加或相减消去一项。",
            },
            formal="解二元一次方程组常用代入消元法与加减消元法。",
            prerequisites=["linear_equation_systems", "linear_equation_one_variable"],
            next_topics=["linear_equation_two_variables", "linear_function"],
            examples=["鸡兔同笼列方程组", "两商品价格问题"],
            route=["选方法", "消元", "解一元", "回代", "检验"],
            conceptual_layers=[
                "解方程组的核心只有两个字：消元——把两个未知数想办法变成一个。",
                "代入法：从一个方程解出某个未知数的式子，整个塞进另一个方程。",
                "加减法：把两个方程相加或相减，让某个未知数正好抵消掉。",
            ],
            worked_examples=[
                _worked(
                    "用加减法解方程组",
                    "解 x+y=5，x−y=1。",
                    [
                        "两式相加：左边 x+y+x−y=2x，右边 5+1=6。",
                        "得 2x=6，x=3。",
                        "代回 x+y=5，得 y=2。",
                    ],
                    "能说出为什么相加能消掉 y（系数正好相反）。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "「消元」是什么意思？为什么解方程组要先消元？",
                    "抓住化二元为一元。",
                ),
                _task(
                    "会做",
                    "用代入法解 y=2x，x+y=6。",
                    "会用代入法。",
                ),
                _task(
                    "迁移",
                    "什么时候用加减法比代入法更省事？举个例子。",
                    "会挑方法。",
                ),
            ],
            reflection_questions=[
                "代入法和加减法，殊途同归的那个「同归」是什么？",
                "什么样的方程组，一眼就适合用加减法消元？",
                "解出一个未知数后，为什么还要「回代」求另一个？",
            ],
        ),
        _point(
            topic_id="function_concept_junior",
            name="变量与函数（再认）",
            grade_band=j,
            grade="八年级下册",
            chapter="一次函数",
            section="变量与函数",
            human="在一个变化过程里，有的量会变叫变量；如果一个量确定后另一个量跟着唯一确定，就说后者是前者的函数。",
            why="一次、反比例、二次函数都是这一句话的不同长相。",
            terms={
                "变量": "可以取不同值的量。",
                "常量": "在讨论过程中不变的量。",
                "自变量": "主动变化、当作输入的量。",
                "函数值": "对应出来的输出。",
            },
            formal=(
                "一般地，在一个变化过程中，如果有两个变量 x 与 y，"
                "对于 x 的每一个确定的值，y 都有唯一确定的值与它对应，"
                "那么就说 y 是 x 的函数。"
            ),
            prerequisites=["function_intro", "quantity_relationship", "coordinate_plane"],
            next_topics=[
                "linear_function",
                "function_graph_reading",
                "inverse_proportion_function",
            ],
            examples=["出租车费随里程变", "温度随时间变"],
            route=["找两个量", "谁随谁变", "是否唯一对应", "表格图像表达式"],
            misconceptions=["有两个字母就是函数", "一个 x 对应两个 y 仍叫函数"],
            conceptual_layers=[
                "函数讲的是「一个量变，另一个量跟着变」，而且跟得「唯一确定」。",
                "关键词是唯一：给一个自变量的值，函数值只能有一个，不能一对多。",
                "变量是会变的量，常量是过程里不变的量；自变量是输入，函数值是输出。",
            ],
            worked_examples=[
                _worked(
                    "这是不是函数关系",
                    "出租车费随里程变化：每个里程数，车费能不能确定？",
                    [
                        "里程是自变量（主动变），车费随它变。",
                        "给定一个里程，车费按规则算出来，只有一个值。",
                        "一对一确定，所以车费是里程的函数。",
                    ],
                    "能说出判断依据是「一个输入是否只对一个输出」。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "「y 是 x 的函数」这句话里，最要紧的词是哪个？",
                    "锁定唯一确定。",
                ),
                _task(
                    "会做",
                    "正方形边长 a，面积 S=a²，S 是 a 的函数吗？",
                    "会判断函数关系。",
                ),
                _task(
                    "迁移",
                    "「一个 x 对应两个 y」这种对应，还能叫函数吗？为什么？",
                    "抓住反例。",
                ),
            ],
            reflection_questions=[
                "变量和常量的区别是什么？同一个字母会不会既是变量又是常量？",
                "为什么函数强调「唯一确定」？一对多为什么不行？",
                "生活里再举一个「一个量随另一个量唯一确定」的例子。",
            ],
        ),
        _point(
            topic_id="slope_intercept_meaning",
            name="一次函数的斜率与截距",
            grade_band=j,
            grade="八年级下册",
            chapter="一次函数",
            section="k 与 b 的意义",
            human="在 y=kx+b 里，k 描述「斜得多厉害、向哪边斜」，b 描述直线与 y 轴交在哪里。",
            why="读图、写解析式、比较变化快慢都靠 k、b。",
            terms={
                "斜率": "这里先理解为 k，反映倾斜程度与正负方向。",
                "截距": "与坐标轴交点的坐标；常说的纵截距是 b。",
            },
            formal="一次函数 y=kx+b（k≠0）中，k 为斜率，b 为直线在 y 轴上的截距。",
            prerequisites=["linear_function", "function_graph_reading", "ratio"],
            next_topics=["quadratic_function", "inverse_proportion_function"],
            formulas=["y=kx+b"],
            examples=["y=2x+1 比 y=x+1 更陡", "b 改变则上下平移"],
            route=["k>0 上升", "k<0 下降", "|k| 大更陡", "b 是纵截距"],
            misconceptions=["k 只表示角度数字", "b 与 x 轴截距混淆"],
            conceptual_layers=[
                "一次函数 y=kx+b 里有两个旋钮：k 管「斜」，b 管「高低」。",
                "k 决定方向和陡缓：k>0 向上斜，k<0 向下斜，|k| 越大越陡。",
                "b 是直线穿过 y 轴的位置（纵截距）；改 b 只是把整条线上下平移。",
            ],
            worked_examples=[
                _worked(
                    "从 y=2x+1 读出 k 和 b",
                    "y=2x+1 的图像斜向哪、和 y 轴交在哪？",
                    [
                        "对照 y=kx+b：k=2，b=1。",
                        "k=2>0，直线向上斜，而且比 k=1 更陡。",
                        "b=1，直线与 y 轴交在 (0,1)。",
                    ],
                    "能分别说出 k 和 b 各控制图像的什么。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "在 y=kx+b 里，k 和 b 各自控制图像的哪一面？",
                    "分清两个作用。",
                ),
                _task(
                    "会做",
                    "比较 y=3x 和 y=x，哪条更陡？为什么？",
                    "用 |k| 判断陡缓。",
                ),
                _task(
                    "迁移",
                    "把 y=2x+1 改成 y=2x−3，图像会怎么变？",
                    "看 b 的平移作用。",
                ),
            ],
            reflection_questions=[
                "为什么说 |k| 越大直线越陡，而不是 k 越大越陡？",
                "b 变了但 k 不变，两条直线之间是什么关系？",
                "k 和 b，哪个决定直线往上还是往下，哪个决定高还是低？",
            ],
        ),
        _point(
            topic_id="quadratic_formula",
            name="求根公式与配方法",
            grade_band=j,
            grade="九年级上册",
            chapter="一元二次方程",
            section="配方法与公式法",
            human="配方法是把方程凑成完全平方式再开方；求根公式是把配方过程固化成可直接套的式子。",
            why="不是每道方程都能因式分解，公式法保证「能解就解出来」。",
            terms={
                "配方法": "通过加减项把左边变成完全平方。",
                "求根公式": "ax²+bx+c=0（a≠0）的解的公式。",
                "判别式": "b²−4ac，用来判断有没有实数根。",
            },
            formal="x=[−b±√(b²−4ac)]/(2a)，其中 Δ=b²−4ac。",
            prerequisites=["quadratic_equation", "formula_perfect_square", "quadratic_radicals"],
            next_topics=["quadratic_function", "quadratic_function_high_school"],
            formulas=["x=[-b±sqrt(b^2-4ac)]/(2a)"],
            examples=["x²−5x+6=0", "x²+2x−2=0"],
            route=["化一般式", "算 Δ", "判断根", "代入公式", "检验"],
            misconceptions=["Δ 算错仍硬套", "分母 2a 漏写"],
            conceptual_layers=[
                "配方法把方程凑成「完全平方=某数」，再开方求解，靠的是完全平方公式。",
                "求根公式是把配方过程一次算完、固化下来的万能式子，代入 a、b、c 就能解。",
                "判别式 Δ=b²−4ac 是「探路灯」：先看它正负，就知道有没有实数根。",
            ],
            worked_examples=[
                _worked(
                    "用求根公式解 x²−5x+6=0",
                    "解 x²−5x+6=0。",
                    [
                        "对照一般式：a=1，b=−5，c=6。",
                        "判别式 Δ=(−5)²−4×1×6=25−24=1>0，有两个根。",
                        "代公式 x=(5±√1)/2=(5±1)/2，得 x=3 或 x=2。",
                    ],
                    "能说出先算判别式的意义，再解释 ± 为什么给两个根。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "判别式 b²−4ac 是用来干什么的？为什么先算它？",
                    "理解判别式的作用。",
                ),
                _task(
                    "会做",
                    "用求根公式解 x²−2x−3=0。",
                    "会代公式。",
                ),
                _task(
                    "迁移",
                    "求根公式和配方法，本质上是不是一回事？说说看。",
                    "看到两者的联系。",
                ),
            ],
            reflection_questions=[
                "为什么求根公式里会出现「±」，它对应几个根？",
                "判别式等于 0 时，方程的根有什么特别？",
                "不是所有二次方程都能因式分解，为什么求根公式还能解？",
            ],
        ),
        _point(
            topic_id="quadratic_vertex",
            name="二次函数的顶点与增减",
            grade_band=j,
            grade="九年级上册",
            chapter="二次函数",
            section="顶点式与图像",
            human="抛物线有最高点或最低点叫顶点；顶点把图像分成上升和下降两段。",
            why="最值问题、配方法、图像平移都落在顶点上。",
            terms={
                "顶点": "抛物线的最高或最低点。",
                "对称轴": "把抛物线分成对称两半的竖直线。",
                "开口方向": "由二次项系数正负决定向上或向下。",
            },
            formal="y=a(x−h)²+k 的顶点为 (h,k)；a>0 开口向上，a<0 开口向下。",
            prerequisites=[
                "quadratic_function",
                "formula_perfect_square",
                "function_graph_reading",
            ],
            next_topics=["quadratic_function_high_school", "derivative_intro"],
            formulas=["y=a(x-h)^2+k"],
            examples=["喷泉高度", "利润最大问题直觉"],
            route=["看 a 正负", "找顶点", "对称轴", "左右增减"],
            conceptual_layers=[
                "抛物线不是一直升或一直降，它有个拐弯的极点——顶点，是最高或最低处。",
                "开口方向由 a 定：a>0 开口向上，顶点是最低点；a<0 向下，顶点是最高点。",
                "顶点式 y=a(x−h)²+k 直接把顶点 (h,k) 写在脸上，对称轴就是 x=h。",
            ],
            worked_examples=[
                _worked(
                    "从顶点式读顶点",
                    "y=2(x−1)²+3 的顶点、对称轴、开口方向各是什么？",
                    [
                        "对照 y=a(x−h)²+k：a=2，h=1，k=3。",
                        "顶点是 (h,k)=(1,3)，对称轴是直线 x=1。",
                        "a=2>0，开口向上，顶点 (1,3) 是最低点。",
                    ],
                    "能说出顶点坐标怎么从顶点式直接读出来。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "顶点为什么既是抛物线的极点，又在对称轴上？",
                    "理解顶点的双重身份。",
                ),
                _task(
                    "会做",
                    "写出 y=−(x+2)²+5 的顶点和开口方向。",
                    "会读顶点式。",
                ),
                _task(
                    "迁移",
                    "喷泉水柱的最高点，对应抛物线的什么？",
                    "把顶点用到实际。",
                ),
            ],
            reflection_questions=[
                "开口向上和向下，顶点分别是最高点还是最低点？",
                "对称轴左右两边，函数一个在增一个在减，为什么？",
                "把 y=x² 变成 y=(x−1)²，图像发生了什么变化？",
            ],
        ),
        # —— 初中几何加厚 ——
        _point(
            topic_id="triangle_angle_sum",
            name="三角形内角和",
            grade_band=j,
            grade="八年级上册",
            chapter="三角形",
            section="内角和定理",
            human="任意三角形三个内角加起来都是 180°，像把三个角撕下来能拼成一个平角。",
            why="求角、证明平行、相似判定都会反复用。",
            terms={
                "内角": "三角形内部的角。",
                "外角": "一边与邻边延长线的夹角。",
            },
            formal="三角形三个内角的和等于 180°。",
            prerequisites=["triangle_basic", "angle_measure", "parallel_lines"],
            next_topics=["congruent_triangles", "similar_triangles", "pythagorean_theorem"],
            formulas=["∠A+∠B+∠C=180°"],
            examples=["已知两角求第三角", "等边三角形每个角 60°"],
            route=["撕角拼平角", "平行线证明思路", "用定理求角"],
            visuals=["撕纸拼角"],
            conceptual_layers=[
                "三角形不管长什么样，三个内角加起来永远是 180°，这是铁律。",
                "直观感受：把三个角撕下来拼到一起，正好拼成一条直线（平角 180°）。",
                "有了它，知道两个角就能算第三个；等边三角形三角相等，各 60°。",
            ],
            worked_examples=[
                _worked(
                    "已知两角求第三角",
                    "三角形两个内角是 50° 和 60°，第三个角多少度？",
                    [
                        "三个内角和是 180°。",
                        "已知两个：50°+60°=110°。",
                        "第三个 = 180°−110°=70°。",
                    ],
                    "能说出为什么用 180 去减，而不是别的数。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "用「撕角拼平角」说明为什么三角形内角和是 180°。",
                    "理解定理的直观来源。",
                ),
                _task(
                    "会做",
                    "一个三角形两角是 90° 和 30°，第三个角是多少？",
                    "会用定理求角。",
                ),
                _task(
                    "迁移",
                    "等边三角形每个内角都相等，各是多少度？",
                    "把定理用到特殊三角形。",
                ),
            ],
            reflection_questions=[
                "为什么无论三角形大小形状，内角和都是 180°？",
                "一个三角形能不能有两个直角？用内角和说明。",
                "钝角三角形里，那个钝角最大能接近多少度？",
            ],
        ),
        _point(
            topic_id="congruent_criteria",
            name="全等三角形判定",
            grade_band=j,
            grade="八年级上册",
            chapter="全等三角形",
            section="SSS、SAS、ASA、AAS、HL",
            human="全等是形状大小完全一样，能完全重合；判定是「满足哪些条件就能断定全等」，不用比所有边角。",
            why="几何证明里最常用的「桥」。",
            terms={
                "全等": "形状和大小都相同，对应边角相等。",
                "对应": "重合时落在一起的边或角。",
                "判定": "用来下结论的条件组合。",
            },
            formal="常用判定：SSS、SAS、ASA、AAS；直角三角形还有 HL。",
            prerequisites=["congruent_triangles", "triangle_basic", "geometric_proof_intro"],
            next_topics=["similar_triangles", "pythagorean_theorem"],
            examples=["桥架对称结构", "复制定理证明"],
            route=["找已知边角", "选判定", "写对应", "推对应相等"],
            misconceptions=["AAA 能判定全等", "对应乱写导致边角不配"],
            conceptual_layers=[
                "全等就是两个三角形完全一样、能严丝合缝地重合，对应边和角都相等。",
                "判定的意义：不用量遍所有六个边角，满足几个关键条件就能断定全等。",
                "常用判定 SSS、SAS、ASA、AAS 是不同的条件组合，直角三角形另有 HL。",
            ],
            worked_examples=[
                _worked(
                    "两边夹一角能定全等吗",
                    "两三角形有两条边分别相等，且这两边的夹角也相等，全等吗？",
                    [
                        "两边相等、夹角相等，正好是 SAS 的条件。",
                        "SAS 是公认的判定，条件够了。",
                        "所以两个三角形全等。",
                    ],
                    "能说出用的是 SAS，并指出「夹角」必须是那两边夹着的角。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "为什么判定全等不用把六个边角都比一遍？",
                    "理解判定省在哪。",
                ),
                _task(
                    "会做",
                    "已知两三角形三条边分别相等，用哪个判定说明全等？",
                    "会选 SSS。",
                ),
                _task(
                    "迁移",
                    "为什么三个角对应相等（AAA）不能断定两三角形全等？",
                    "看到判定的边界。",
                ),
            ],
            reflection_questions=[
                "「全等」和「相似」，一个要求什么、另一个放宽了什么？",
                "写全等时为什么一定要把「对应」的顶点顺序摆对？",
                "SAS 里的角必须是「夹角」，如果换成另一个角，还成立吗？",
            ],
        ),
        _point(
            topic_id="similar_ratio",
            name="相似比与相似三角形",
            grade_band=j,
            grade="九年级下册",
            chapter="相似",
            section="相似三角形",
            human="相似是形状一样、大小可以不同；对应边成比例，对应角相等。",
            why="测量无法直接量的高度、地图比例、三角函数的几何基础。",
            terms={
                "相似": "形状相同，大小未必相同。",
                "相似比": "对应边的比值。",
                "对应角": "位置对应的角，相似时相等。",
            },
            formal="对应角相等、对应边成比例的三角形叫做相似三角形。",
            prerequisites=["similar_triangles", "ratio", "congruent_criteria"],
            next_topics=["trigonometric_ratios", "proportion"],
            formulas=["a/a'=b/b'=c/c'=k"],
            examples=["影子测高", "放大图纸"],
            route=["找相等角", "找比例边", "写相似比", "求未知边"],
            conceptual_layers=[
                "相似是「形状相同、大小可不同」：像同一张照片放大或缩小。",
                "两条判据：对应角都相等，对应边都成同一个比例，这个比例叫相似比。",
                "相似比 k 就是放大倍数：k=1 时其实就是全等，是相似的特例。",
            ],
            worked_examples=[
                _worked(
                    "用相似比求未知边",
                    "两个相似三角形，对应边 3 和 6。小三角形另一边是 4，它的对应边多长？",
                    [
                        "先求相似比：大边 6 比小边 3，相似比是 2。",
                        "对应边都按同一比例：大边 = 小边 × 2。",
                        "另一条大边 = 4 × 2 = 8。",
                    ],
                    "能说出所有对应边用的是同一个相似比。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "相似和全等，差别在「大小」这一点上，具体怎么理解？",
                    "抓住形状同、大小可不同。",
                ),
                _task(
                    "会做",
                    "相似比是 3 的两个三角形，小的一边 5，大的对应边多长？",
                    "会用相似比算边。",
                ),
                _task(
                    "迁移",
                    "为什么测量旗杆高度可以用影子和相似三角形？",
                    "把相似用到测高。",
                ),
            ],
            reflection_questions=[
                "相似比等于 1 时，两个图形是什么关系？",
                "为什么相似只要求对应角相等、对应边成比例，不要求边相等？",
                "放大一张地图，图上的角会变吗？长度的比例会变吗？",
            ],
        ),
        _point(
            topic_id="pythagorean_applications",
            name="勾股定理的应用",
            grade_band=j,
            grade="八年级下册",
            chapter="勾股定理",
            section="应用",
            human="直角三角形里，两条直角边的平方和等于斜边的平方；可用来求边长或判断是否直角。",
            why="距离、导航、空间对角线的平面基础。",
            terms={
                "直角边": "夹直角的两条边。",
                "斜边": "直角的对边，最长。",
                "勾股数": "能构成直角三角形边长的正整数组合，如 3、4、5。",
            },
            formal="直角三角形两直角边 a、b 与斜边 c 满足 a²+b²=c²。",
            prerequisites=["pythagorean_theorem", "quadratic_radicals", "triangle_basic"],
            next_topics=["coordinate_plane", "trigonometric_ratios", "space_vectors"],
            formulas=["a^2+b^2=c^2"],
            examples=["梯子靠墙", "电视屏幕尺寸"],
            route=["确认直角", "谁是斜边", "代入", "取算术平方根"],
            misconceptions=["斜边代错", "开方丢单位"],
            conceptual_layers=[
                "勾股定理只在直角三角形里成立：两条直角边平方相加，等于斜边平方。",
                "它有两个用处：知道两边求第三边；或反过来验证一个三角形是不是直角。",
                "斜边永远是直角对面那条、也是最长的一条，代公式前先把它认准。",
            ],
            worked_examples=[
                _worked(
                    "梯子靠墙够多高",
                    "梯子长 5 米，底端离墙 3 米，梯子顶端离地多高？",
                    [
                        "梯子是斜边 c=5，离墙 3 是一条直角边 a=3，高是另一直角边 b。",
                        "由 a²+b²=c²：9+b²=25，所以 b²=16。",
                        "b=√16=4，顶端离地 4 米。",
                    ],
                    "能说出为什么梯子长是斜边，而不是直角边。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "勾股定理为什么只能用在直角三角形上？",
                    "认清适用前提。",
                ),
                _task(
                    "会做",
                    "直角三角形两直角边是 6 和 8，斜边多长？",
                    "会求斜边。",
                ),
                _task(
                    "迁移",
                    "三边是 5、12、13 的三角形是直角三角形吗？怎么判断？",
                    "用定理反向验证。",
                ),
            ],
            reflection_questions=[
                "怎么一眼认出直角三角形里哪条是斜边？",
                "已知斜边和一条直角边，求另一条直角边，公式该怎么变形？",
                "勾股定理反过来（知道三边验直角）为什么也成立？",
            ],
        ),
        _point(
            topic_id="circle_central_inscribed",
            name="圆心角与圆周角",
            grade_band=j,
            grade="九年级上册",
            chapter="圆",
            section="圆心角、圆周角",
            human="圆心角的顶点在圆心；圆周角的顶点在圆上。同弧所对的圆周角是圆心角的一半。",
            why="圆的很多证明和计算都绕着「角与弧的对应」。",
            terms={
                "圆心角": "顶点在圆心的角。",
                "圆周角": "顶点在圆周、两边和圆相交的角。",
                "弧": "圆上两点之间的部分。",
            },
            formal="同弧或等弧所对的圆周角等于它所对圆心角的一半。",
            prerequisites=["circle", "angle_measure", "triangle_angle_sum"],
            next_topics=["trigonometric_ratios"],
            examples=["看表盘扇形", "拱桥圆弧"],
            route=["找弧", "找圆心角", "找圆周角", "用一半关系"],
            conceptual_layers=[
                "两种角都对着圆上一段弧，区别在顶点：圆心角顶点在圆心，圆周角在圆上。",
                "核心关系：对着同一段弧，圆周角总是圆心角的一半。",
                "认准「对着哪段弧」是关键——两角必须对着同一段弧，一半关系才成立。",
            ],
            worked_examples=[
                _worked(
                    "圆周角是圆心角的一半",
                    "一段弧所对的圆心角是 80°，它所对的圆周角是多少？",
                    [
                        "先确认两个角对着同一段弧。",
                        "圆周角 = 圆心角的一半。",
                        "80°÷2 = 40°，圆周角是 40°。",
                    ],
                    "能说出用「一半」的前提是两角对着同一段弧。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "圆心角和圆周角，怎么从图上一眼区分？",
                    "看顶点位置。",
                ),
                _task(
                    "会做",
                    "同一段弧所对的圆周角是 30°，圆心角是多少？",
                    "会用一半关系反算。",
                ),
                _task(
                    "迁移",
                    "直径所对的圆周角是多少度？用一半关系想一想。",
                    "推出直径所对圆周角。",
                ),
            ],
            reflection_questions=[
                "为什么强调「同弧」所对，才有一半的关系？",
                "同一段弧所对的圆周角，位置不同大小会变吗？",
                "半圆（直径所对）的圆周角为什么恰好是直角？",
            ],
        ),
        _point(
            topic_id="view_of_solids",
            name="三视图初步",
            grade_band=j,
            grade="七年级至九年级",
            chapter="丰富的图形世界 / 投影与视图",
            section="主视图、左视图、俯视图",
            human="三视图是从正面、左面、上面看立体得到的平面图形，用来把空间形状说清楚。",
            why="读图纸、理解立体几何对象的第一步。",
            terms={
                "主视图": "从正面看。",
                "左视图": "从左面看。",
                "俯视图": "从上面看。",
            },
            formal="物体的三视图是正投影下从三个方向得到的投影图。",
            prerequisites=["geometric_figures_intro", "volume"],
            next_topics=["solid_geometry_spatial_relations"],
            examples=["积木堆的三视图", "纸箱"],
            route=["选定方向", "看轮廓", "长对正", "高平齐", "宽相等"],
            misconceptions=["把斜线当看得见的棱乱画", "视图方向搞反"],
            conceptual_layers=[
                "三视图是把立体「拍平」：分别从正面、左面、上面看，各画一张平面图。",
                "主视图从正面看，左视图从左面看，俯视图从上面看，三张合起来描述形状。",
                "三张图有规矩对齐：主视图和俯视图长对正，主视图和左视图高平齐。",
            ],
            worked_examples=[
                _worked(
                    "正方体的三视图",
                    "一个正方体，它的主视图、左视图、俯视图各是什么形状？",
                    [
                        "从正面看，是一个正方形（主视图）。",
                        "从左面看，也是一个正方形（左视图）。",
                        "从上面看，还是一个正方形（俯视图）。",
                    ],
                    "能说出每张视图是「从哪个方向看」得到的。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "为什么一张视图说不清立体形状，要画三张？",
                    "理解三视图互补。",
                ),
                _task(
                    "会做",
                    "竖着放的圆柱，俯视图大概是什么形状？",
                    "会想象投影。",
                ),
                _task(
                    "迁移",
                    "为什么画三视图时，看不见的棱不能当实线乱画？",
                    "注意可见性。",
                ),
            ],
            reflection_questions=[
                "主视图、左视图、俯视图，分别站在哪个方向看？",
                "为什么三张视图之间要「长对正、高平齐、宽相等」？",
                "两个不同的立体，有没有可能三视图完全一样？",
            ],
        ),
        _point(
            topic_id="probability_classical",
            name="古典概型直觉",
            grade_band=j,
            grade="九年级上册",
            chapter="概率初步",
            section="等可能情形下的概率",
            human="如果每个基本结果机会一样，事件概率就是「符合条件的结果数 ÷ 全部结果数」。",
            why="列表树状图之后，用分数语言描述可能性。",
            terms={
                "基本结果": "一次试验最细的可能结果。",
                "等可能": "每个基本结果机会相同。",
                "概率": "可能性大小的数，常在 0 到 1 之间。",
            },
            formal="古典概型中，P(A)=m/n，其中 n 为等可能基本结果总数，m 为事件 A 包含的结果数。",
            prerequisites=["probability", "probability_tree_listing", "fraction"],
            next_topics=["probability_high_school", "random_variables"],
            formulas=["P=m/n"],
            examples=["掷均匀骰子得偶数", "袋中摸球"],
            route=["确认等可能", "列全结果", "数符合的", "写成分数", "约分"],
            misconceptions=["没列全就除", "把「感觉可能」当等可能"],
            conceptual_layers=[
                "古典概型的前提是「等可能」：每个基本结果发生的机会都一样，一个不偏。",
                "概率就是一个分数：符合条件的结果数，除以全部结果数。",
                "算前必须做两件事：确认真的是等可能，把所有结果不重不漏地列全。",
            ],
            worked_examples=[
                _worked(
                    "掷骰子得偶数的概率",
                    "掷一个均匀骰子，点数是偶数的概率是多少？",
                    [
                        "骰子 6 个面等可能，全部结果 n=6。",
                        "偶数点有 2、4、6，符合的结果 m=3。",
                        "P=m/n=3/6=1/2。",
                    ],
                    "能说出为什么先要确认「均匀」（等可能）。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "为什么用「符合数÷总数」算概率，前提必须是等可能？",
                    "抓住等可能前提。",
                ),
                _task(
                    "会做",
                    "袋里 2 红 3 白共 5 球，摸到红球的概率是多少？",
                    "会写成分数。",
                ),
                _task(
                    "迁移",
                    "掷一枚均匀硬币，正面朝上的概率是多少？为什么？",
                    "把公式用到硬币。",
                ),
            ],
            reflection_questions=[
                "「感觉某个结果更容易出现」和「等可能」有什么冲突？",
                "如果结果没列全就去算，概率会算错在哪？",
                "概率为什么总在 0 和 1 之间，不会是 2 或负数？",
            ],
        ),
        _point(
            topic_id="sampling_bias",
            name="抽样与偏差直觉",
            grade_band=j,
            grade="八年级下册至九年级",
            chapter="数据分析",
            section="抽样调查",
            human="抽样是只查一部分来了解全体；样本要有代表性，否则结论会偏。",
            why="媒体数据和统计题都要会问：这样本代表谁？",
            terms={
                "总体": "要了解的全体。",
                "样本": "实际调查的一部分。",
                "偏差": "样本系统性偏向某类对象。",
            },
            formal="用样本估计总体时，抽样方式影响估计的可靠性。",
            prerequisites=["data_analysis", "data_collection_description", "average"],
            next_topics=["normal_distribution", "random_variables"],
            examples=["只在篮球社问平均身高", "网上自愿填问卷"],
            route=["谁是总体", "怎么抽", "会不会偏", "结论能推广吗"],
            conceptual_layers=[
                "全部调查太费劲，就抽一部分来看，这一部分叫样本，全体叫总体。",
                "样本要有「代表性」：像总体的缩小版，各类人都按比例照顾到。",
                "抽得偏了（只抽某一类人），结论就会跟着偏，不能代表全体。",
            ],
            worked_examples=[
                _worked(
                    "这样调查身高偏在哪",
                    "想知道全校平均身高，只在篮球社里量，行不行？",
                    [
                        "总体是全校学生，样本却只有篮球社。",
                        "篮球社学生普遍偏高，不像全校的缩小版。",
                        "样本有偏差，算出的身高会偏大，不能代表全校。",
                    ],
                    "能指出问题出在样本不具代表性，而不是算错了。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "为什么调查全体太难时，可以只抽一部分来估计？",
                    "理解抽样的意义。",
                ),
                _task(
                    "会做",
                    "想了解全校学生近视率，怎样抽样比较不偏？",
                    "会设计有代表性的抽样。",
                ),
                _task(
                    "迁移",
                    "网上自愿填的问卷，结果为什么可能有偏差？",
                    "识别自愿样本偏差。",
                ),
            ],
            reflection_questions=[
                "样本和总体的关系，像什么和什么？",
                "什么样的抽样最容易产生偏差？",
                "样本大小和代表性，哪个更能决定结论可不可靠？",
            ],
        ),
        _point(
            topic_id="set_language_junior",
            name="集合语言入门",
            grade_band=b,
            grade="九年级至高一衔接",
            chapter="预备知识",
            section="集合的描述",
            human="集合是把一些对象打包看成一个整体；用「属于」说明某个对象在不在包里。",
            why="函数定义域、不等式解集、概率样本空间都会用集合说话。",
            terms={
                "集合": "确定的一些对象组成的整体。",
                "元素": "集合里的对象。",
                "属于": "元素在集合中，记作 ∈。",
            },
            formal="集合由元素构成；元素与集合的关系是属于或不属于。",
            prerequisites=["inequalities", "function_concept_junior"],
            next_topics=["set_concept", "function_properties_high_school"],
            examples=["班级里所有女生", "方程的解的集合"],
            route=["说清对象", "不重复", "确定准则", "用符号写"],
            misconceptions=["含糊对象也能成集合", "同一元素写两次"],
            conceptual_layers=[
                "集合就是把一些对象打包成一个整体，这些对象叫它的元素。",
                "「属于」（∈）说的是某对象在不在这个包里，在就属于，不在就不属于。",
                "集合有两条硬规矩：对象要「确定」（能判断在不在），而且不重复。",
            ],
            worked_examples=[
                _worked(
                    "这些能不能组成集合",
                    "「班上所有女生」和「班上个子高的同学」，哪个能确定地组成集合？",
                    [
                        "「所有女生」标准明确，每个人是不是女生都能判断。",
                        "「个子高」没定标准，多高算高说不清。",
                        "所以前者是集合，后者标准含糊，不能算。",
                    ],
                    "能说出集合要求元素「确定」，标准含糊就不行。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "为什么集合里的元素必须是「确定的」？",
                    "抓住确定性。",
                ),
                _task(
                    "会做",
                    "用集合表示「小于 5 的正整数」，有哪些元素？",
                    "会列举元素。",
                ),
                _task(
                    "迁移",
                    "「小于 10 的正偶数」和「小于 10 的质数」各是什么集合？有公共元素吗？",
                    "把集合用到分类比较。",
                ),
            ],
            reflection_questions=[
                "「属于」和「不属于」，在集合里各用什么符号？",
                "为什么同一个元素在集合里写两次没有意义？",
                "生活里还有什么例子，是把一堆对象打包成整体来看的？",
            ],
        ),
        _point(
            topic_id="absolute_value_equations",
            name="绝对值方程初步",
            grade_band=j,
            grade="七年级至八年级",
            chapter="有理数 / 绝对值",
            section="简单绝对值方程",
            human="绝对值表示到 0 的距离；含绝对值的方程常要按「里面是正是负」分成两边讨论。",
            why="为二次函数、距离公式和解更复杂的方程做准备。",
            terms={
                "绝对值方程": "未知数出现在绝对值号里的方程。",
                "零点分段": "让绝对值里面为 0 的点，用来分情况。",
            },
            formal="|x|=a（a>0）的解是 x=a 或 x=−a。",
            prerequisites=["absolute_value", "linear_equation_one_variable", "number_line"],
            next_topics=["inequalities", "quadratic_equation"],
            examples=["|x|=3", "|x−1|=2"],
            route=["绝对值意义", "距离", "两种可能", "检验"],
            conceptual_layers=[
                "绝对值是「到 0 的距离」，距离没有负的，所以绝对值永远大于等于 0。",
                "解 |x|=a 要想到两种可能：里面等于 +a，或等于 −a，两点离 0 一样远。",
                "所以一个绝对值方程往往有两个解，别只写一个就收工。",
            ],
            worked_examples=[
                _worked(
                    "解 |x−1|=2",
                    "解方程 |x−1|=2。",
                    [
                        "绝对值是距离：x−1 到 0 的距离是 2。",
                        "所以 x−1=2 或 x−1=−2。",
                        "分别解得 x=3 或 x=−1。",
                    ],
                    "能说出为什么有两个解，两种情况各对应什么。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "为什么 |x|=3 有两个解，而不是一个？",
                    "抓住距离的两个方向。",
                ),
                _task(
                    "会做",
                    "解 |x|=5。",
                    "会写出两个解。",
                ),
                _task(
                    "迁移",
                    "|x|=−2 有解吗？为什么？",
                    "用绝对值非负判断。",
                ),
            ],
            reflection_questions=[
                "绝对值为什么永远不会是负数？",
                "|x−1|=2 里的「−1」在几何上把什么点移了位置？",
                "什么时候一个绝对值方程会没有解？",
            ],
        ),
        _point(
            topic_id="polynomial_degree_terms",
            name="整式的次数与项",
            grade_band=j,
            grade="七年级上册",
            chapter="整式的加减",
            section="项、系数、次数",
            human="整式由一项一项加起来；每一项有系数和次数，整式的次数看次数最高的那一项。",
            why="合并同类项、多项式乘法都要先认清「项」。",
            terms={
                "项": "用加号连接的每一块（减号可看成加负数）。",
                "系数": "项里头的数字因数。",
                "次数": "一项里字母指数的和；多项式取最高的。",
            },
            formal="整式是数或含字母的积以及它们的和；多项式的次数是次数最高的项的次数。",
            prerequisites=["algebraic_expression", "like_terms"],
            next_topics=["polynomial_multiplication", "factorization"],
            examples=["3x²−2x+1 是二次三项式"],
            route=["拆项", "看系数", "看字母指数", "定次数"],
            conceptual_layers=[
                "多项式是一项一项用加号连起来的（减号看成加负数），每一块叫一项。",
                "每一项有两样：系数（数字部分）和次数（字母指数的和）。",
                "整个多项式的次数，看它最高那一项的次数，不是把各项次数加起来。",
            ],
            worked_examples=[
                _worked(
                    "认清 3x²−2x+1 的项和次数",
                    "3x²−2x+1 有几项？各项系数是几？整式的次数是几？",
                    [
                        "拆成三项：3x²、−2x、+1。",
                        "系数分别是 3、−2、1；次数分别是 2、1、0。",
                        "最高次是 2，所以是二次三项式。",
                    ],
                    "能说出整式次数看最高项，不是各项相加。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "整式的「次数」为什么取最高项的，而不是各项之和？",
                    "理解次数的定义。",
                ),
                _task(
                    "会做",
                    "说出 5x³+2x−7 的项数、各项系数和整式次数。",
                    "会拆项定次数。",
                ),
                _task(
                    "迁移",
                    "−x 的系数是多少？次数是几？",
                    "注意隐藏的系数。",
                ),
            ],
            reflection_questions=[
                "「项」和「系数」，一个说的是什么，一个说的是什么？",
                "常数项（比如 +1）的次数为什么是 0？",
                "−2x 前面的负号，属于系数还是另算？",
            ],
        ),
        _point(
            topic_id="factor_common_factor",
            name="提公因式法",
            grade_band=j,
            grade="八年级上册",
            chapter="因式分解",
            section="提公因式",
            human="提公因式是把每一项都有的公共部分提出来，写成乘法形式，方便约分或继续分解。",
            why="因式分解最基本的一招，后面公式法经常先提公因式。",
            terms={
                "公因式": "每一项都含有的公共因式。",
                "因式分解": "把和差形式写成积的形式。",
            },
            formal="ab+ac=a(b+c)。",
            prerequisites=["factorization", "distributive_property", "polynomial_degree_terms"],
            next_topics=["formula_square_difference", "rational_expression"],
            examples=["2x+4=2(x+2)", "x²+x=x(x+1)"],
            route=["找公共的", "提出来", "括号里剩什么", "展开检验"],
            conceptual_layers=[
                "提公因式是乘法分配律反着用：把每项都有的公共部分提到括号外面。",
                "因式分解就是把「和差形式」改写成「乘积形式」，提公因式是最基本一招。",
                "提完要检验：把括号乘开，应该正好还原成原来的式子。",
            ],
            worked_examples=[
                _worked(
                    "给 2x+4 提公因式",
                    "把 2x+4 分解因式。",
                    [
                        "看每一项：2x 和 4 都含有因数 2。",
                        "把 2 提到括号外：2x+4=2(x+2)。",
                        "检验：2×x+2×2=2x+4，还原正确。",
                    ],
                    "能说出提出的 2 是「每项都有的」，并会展开检验。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "提公因式和乘法分配律，是什么关系？",
                    "看到它是分配律反用。",
                ),
                _task(
                    "会做",
                    "把 x²+x 分解因式。",
                    "会提字母公因式。",
                ),
                _task(
                    "迁移",
                    "把 6a+9 提公因式，公因式取 3 好还是取 1 好？",
                    "取最大公因式。",
                ),
            ],
            reflection_questions=[
                "因式分解和整式乘法，方向正好相反，怎么理解？",
                "怎么判断公因式提得「彻底」了？",
                "如果每一项没有公共的因式，还能提公因式吗？",
            ],
        ),
        _point(
            topic_id="rational_equation_intro",
            name="分式方程入门",
            grade_band=j,
            grade="八年级上册",
            chapter="分式",
            section="分式方程",
            human=(
                "分式方程是分母里含未知数的方程；要先找公分母去分母，"
                "最后必须检验，因为可能使分母为 0。"
            ),
            why="工程问题、浓度问题常列出分式方程。",
            terms={
                "分式方程": "分母含未知数的方程。",
                "增根": "去分母后多出来、使原分母为 0 的根。",
            },
            formal="解分式方程需去分母转化为整式方程，并检验使分母不为 0。",
            prerequisites=[
                "rational_expression",
                "linear_equation_one_variable",
                "fraction_operations",
            ],
            next_topics=["linear_equation_applications"],
            examples=["1/x=2", "行程中速度关系"],
            route=["找公分母", "去分母", "解整式方程", "检验分母"],
            misconceptions=["不检验增根", "公分母漏因式"],
            conceptual_layers=[
                "分式方程的特点是分母里藏着未知数，比如 1/x=2 里 x 在分母上。",
                "解法是「去分母」：两边同乘公分母，把它变成普通的整式方程再解。",
                "最后检验绝不能省：如果某个解让原方程分母为 0，它是增根，要舍掉。",
            ],
            worked_examples=[
                _worked(
                    "解 1/x=2 并检验",
                    "解分式方程 1/x=2。",
                    [
                        "两边同乘 x（去分母）：1=2x。",
                        "解得 x=1/2。",
                        "检验：x=1/2 不为 0，分母有意义，是真解。",
                    ],
                    "能说出为什么解完一定要回头检验分母。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "分式方程为什么解完必须检验，普通方程却常常不用？",
                    "抓住增根的风险。",
                ),
                _task(
                    "会做",
                    "解 2/x=4。",
                    "会去分母求解。",
                ),
                _task(
                    "迁移",
                    "如果解出来的 x 正好让分母为 0，这个解算数吗？",
                    "识别增根。",
                ),
            ],
            reflection_questions=[
                "「去分母」这一步，是怎么把分式方程变简单的？",
                "什么是增根？它是从哪一步冒出来的？",
                "为什么去分母时公分母不能漏掉某个因式？",
            ],
        ),
        _point(
            topic_id="inverse_proportion_graph",
            name="反比例函数图像",
            grade_band=j,
            grade="九年级下册",
            chapter="反比例函数",
            section="图像与性质",
            human=(
                "反比例函数 y=k/x（k≠0）的图像是双曲线，两支分别在对角象限，"
                "越靠近坐标轴越贴近但不相交。"
            ),
            why="理解「积一定」时的变化，并和一次函数对比。",
            terms={
                "双曲线": "反比例函数图像的形状名称。",
                "象限": "坐标平面被轴分成的四个区域。",
            },
            formal="函数 y=k/x（k≠0）叫做反比例函数。",
            prerequisites=["inverse_proportion_function", "function_graph_reading", "proportion"],
            next_topics=["function_properties_high_school"],
            formulas=["y=k/x"],
            examples=["矩形面积一定时长与宽", "行程中速度与时间（路程一定）"],
            route=["k 正负定象限", "列表描点", "看增减", "不与轴相交"],
            conceptual_layers=[
                "反比例函数 y=k/x 描述「乘积一定」：x 大 y 就小，两者反着走。",
                "图像是两支弯曲的双曲线，靠近坐标轴时越贴越近，但永远不相交。",
                "k 的正负决定图像在哪两个对角象限：k>0 在一三象限，k<0 在二四象限。",
            ],
            worked_examples=[
                _worked(
                    "为什么反比例图像不碰坐标轴",
                    "y=6/x 里，x 能取 0 吗？图像会碰到 y 轴吗？",
                    [
                        "分母不能为 0，所以 x≠0。",
                        "x 越接近 0，y 越大（6 除以很小的数很大），点往上冲到不了轴。",
                        "所以图像无限贴近坐标轴，却永远不相交。",
                    ],
                    "能说出「不与轴相交」是因为 x、y 都不能为 0。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "反比例函数里，x 变大时 y 怎么变？为什么？",
                    "抓住反着走。",
                ),
                _task(
                    "会做",
                    "y=8/x，当 x=2 和 x=4 时，y 各是多少？",
                    "会代入求值。",
                ),
                _task(
                    "迁移",
                    "长方形面积固定是 12，长和宽的关系是不是反比例？",
                    "把反比例用到实际。",
                ),
            ],
            reflection_questions=[
                "反比例函数图像为什么分成两支，而不是连成一条？",
                "为什么 x 和 y 都不能等于 0？",
                "一次函数和反比例函数，图像最大的不同在哪里？",
            ],
        ),
        _point(
            topic_id="trig_ratio_right_triangle",
            name="锐角三角函数定义",
            grade_band=j,
            grade="九年级下册",
            chapter="锐角三角函数",
            section="正弦余弦正切",
            human="在直角三角形里，一个锐角的对边、邻边与斜边的比值是固定的，分别叫正弦、余弦、正切。",
            why="测高、测距、物理分解力的几何语言。",
            terms={
                "对边": "不挨着这个角的那条边。",
                "邻边": "夹这个角的直角边。",
                "正弦": "对边比斜边。",
                "余弦": "邻边比斜边。",
                "正切": "对边比邻边。",
            },
            formal="sinθ=对边/斜边，cosθ=邻边/斜边，tanθ=对边/邻边。",
            prerequisites=["trigonometric_ratios", "pythagorean_applications", "similar_ratio"],
            next_topics=["trigonometric_functions"],
            formulas=["sin, cos, tan"],
            examples=["仰角测楼高", "坡度"],
            route=["标直角", "定锐角", "找对边邻边斜边", "写比值", "用表或计算器"],
            misconceptions=["对边邻边搞反", "不是直角三角形硬套定义"],
            conceptual_layers=[
                "在直角三角形里盯住一个锐角，它三条边的比值是固定的，只跟角的大小有关。",
                "三个比值各有名字：正弦=对边/斜边，余弦=邻边/斜边，正切=对边/邻边。",
                "为什么固定？因为同一个锐角的直角三角形都相似，对应边的比都相等。",
            ],
            worked_examples=[
                _worked(
                    "在 3-4-5 直角三角形里求比值",
                    "直角三角形三边 3、4、5，斜边是 5，求较小锐角的三个比值。",
                    [
                        "较小锐角对着最短边：对边=3，邻边=4，斜边=5。",
                        "正弦=对边/斜边=3/5；余弦=邻边/斜边=4/5。",
                        "正切=对边/邻边=3/4。",
                    ],
                    "能说出哪条是对边、邻边、斜边，别搞反。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "对边、邻边、斜边，怎么相对于一个锐角认清楚？",
                    "认准三条边。",
                ),
                _task(
                    "会做",
                    "在 3-4-5 直角三角形里，对边是 4 的那个锐角，正弦是多少？",
                    "会写比值。",
                ),
                _task(
                    "迁移",
                    "为什么同一个角度，不管三角形画多大，正弦值都一样？",
                    "用相似解释固定性。",
                ),
            ],
            reflection_questions=[
                "正弦、余弦、正切，三个比值分别是哪两条边相除？",
                "为什么这些比值只跟角的大小有关，跟三角形大小无关？",
                "如果三角形不是直角三角形，还能直接用这些定义吗？",
            ],
        ),
    ]
