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

CURRICULUM = "人教版义务教育数学"


def _position(grade: str, chapter: str, section: str) -> TextbookPosition:
    return TextbookPosition(
        curriculum=CURRICULUM,
        grade=grade,
        chapter=chapter,
        section=section,
    )


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
    point = KnowledgePoint(
        id=topic_id,
        name=name,
        grade_band=grade_band,
        textbook_positions=[_position(grade, chapter, section)],
        human_explanation=human,
        life_examples=list(examples),
        why_needed=why,
        formal_definition=human,
        term_explanations=dict(terms),
        misconceptions=list(misconceptions),
        prerequisite_ids=list(prerequisites),
        next_ids=list(next_topics),
        formulas=list(formulas),
        visualization_methods=list(visuals),
        ai_teaching_hints=[
            "不要默认学生懂关键词；先解释词，再解释关系。",
            "先问学生能不能用自己的话复述这个概念。",
        ],
        exercise_types=list(exercise_types),
        school_route=[grade, chapter, section],
        understanding_route=route_items or [name, "用人话解释", "图形或生活例子", "符号表达"],
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


def load_curriculum_knowledge_points() -> list[KnowledgePoint]:
    return [
        _point(
            topic_id="number_recognition",
            name="数的认识",
            grade_band=GradeBand.PRIMARY,
            grade="一年级上册",
            chapter="准备课与位置",
            section="数一数",
            human="数是用来回答“有多少”的工具。",
            why="后面所有计算、测量和比较都要先知道数在表示什么。",
            terms={"数": "表示多少的记号。", "计数": "一个一个对应着数出来。"},
            next_topics=["place_value_decimal_system", "integer_addition_subtraction"],
            examples=["数铅笔", "数台阶"],
            route=["一个物体对应一个数", "数的顺序", "多少", "数字记号"],
            visuals=["实物计数", "点子图"],
            conceptual_layers=[
                "数不是一个字，是「有多少」的回答："
                "3 支铅笔、3 级台阶、3 次拍手，说的是同一个「3」。",
                "数数的关键是一一对应：一个东西配一个数，不跳过也不重复，最后念到的数就是总数。",
                "数有顺序：往后数一个就多 1，往前数一个就少 1，所以数还可以用来比大小。",
            ],
            worked_examples=[
                WorkedExample(
                    title="数台阶：最后念到的数就是总数",
                    problem="上楼时边走边数：1、2、3、4、5、6、7。这段楼梯一共有几级台阶？",
                    steps=[
                        "一脚踩一级，嘴里念一个数：踩一级念 1，再踩一级念 2……",
                        "不跳级、不重复念，这叫一一对应。",
                        "最后一级念到 7。7 不只是最后一级的编号，它同时表示总共有 7 级。",
                    ],
                    answer_check="把 7 个东西打乱顺序重新数一遍，总数还是 7，说明你数对了。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="数一数家里任意一堆东西（碗、书、遥控器），说说为什么最后念到的数就是总数。",
                    goal="建立一一对应和「最后一个数=总数」的感觉。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="数 12 颗豆子，数到一半停下再接着数。总数会变吗？为什么？",
                    goal="体会总数不随数的过程改变。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="不一个一个数：先把 10 个圈成一堆，再看剩几个，快速说出总数。",
                    goal="为「十个一捆」的位值思想做铺垫。",
                ),
            ],
            reflection_questions=[
                "3 支铅笔和 3 级台阶，「3」说的是同一件事吗？",
                "数数时跳过一个或重复一个，会出什么错？",
                "为什么最后念到的那个数刚好就是总数？",
            ],
        ),
        _point(
            topic_id="place_value_decimal_system",
            name="十进制与位值",
            grade_band=GradeBand.PRIMARY,
            grade="一年级下册至四年级上册",
            chapter="100以内数的认识 / 大数的认识",
            section="数位与计数单位",
            human="同一个数字放在不同位置，表示的大小不一样。",
            why="多位数、小数、竖式计算都靠位值来保证不乱。",
            terms={"数位": "数字所在的位置。", "计数单位": "一、十、百、千这样的单位。"},
            prerequisites=["number_recognition"],
            next_topics=["decimal", "integer_addition_subtraction"],
            examples=["23里的2表示2个十", "305里的0表示十位没有"],
            route=["一捆十个", "十个十是一百", "位置不同", "值不同"],
            visuals=["数位表", "小棒捆扎"],
            conceptual_layers=[
                "位值的核心约定只有一句话：满十个，就捆成一个更大的单位，往左挪一位。",
                "同一个数字「2」，在 23 里是 2 个十，在 32 里是 2 个一——位置在替你记住单位。",
                "有了这个约定，只用 0～9 十个数字就能写出任何大的数，这是数学里最省事的发明之一。",
            ],
            worked_examples=[
                WorkedExample(
                    title="为什么十要写成「10」",
                    problem="只有 0 到 9 这十个数字，数到十的时候该怎么写？",
                    steps=[
                        "数到 9 再多 1 个，个位已经放不下第十个「一」。",
                        "约定：把十个一捆成一个「十」，放到左边一位；个位空了，写 0 占住位置。",
                        "所以「10」的意思是：1 个十、0 个一——不是数字 1 和 0 恰好排在一起。",
                    ],
                    answer_check="能说出 10 里的 1 和 0 各表示什么，而不是背「一零就是十」。",
                ),
                WorkedExample(
                    title="23 和 32 为什么不一样大",
                    problem="同样用数字 2 和 3，为什么 23 和 32 差这么多？",
                    steps=[
                        "23：2 在十位，表示 2 个十；3 在个位，表示 3 个一，合起来是 20+3。",
                        "32：3 在十位，表示 3 个十；2 在个位，合起来是 30+2。",
                        "数字相同、位置不同，单位就不同——这就是「位值」两个字的意思。",
                    ],
                    answer_check="用小棒摆出 23 和 32（几捆带几根），一眼看出谁大、大在哪。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="把 47 说成「几个十和几个一」，再用小棒或画图摆出来。",
                    goal="把每个数字和它的计数单位对上。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="在数位表里写出 208，说说每个数字各表示多少、0 在干什么。",
                    goal="读写多位数时不乱位。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="钟表上 60 秒进 1 分。它和「满十进一」像在哪里、不像在哪里？",
                    goal="体会进位制是一种约定，十进制只是最常用的一种。",
                ),
            ],
            reflection_questions=[
                "为什么是满十进一，而不是满八、满十二？（提示：看看你的手指）",
                "同一个数字换到另一个数位上，什么变了，什么没变？",
                "如果没有位值，要写「一千零一」得画多少个记号？",
            ],
        ),
        _point(
            topic_id="integer_addition_subtraction",
            name="整数加减法",
            grade_band=GradeBand.PRIMARY,
            grade="一年级上册至三年级上册",
            chapter="加法和减法",
            section="进位、退位与竖式",
            human="加法是在合起来，减法是在拿走或比较差多少。",
            why="这是理解数量变化和后续四则混合运算的入口。",
            terms={"进位": "某一位满十后换成高一位的一个。", "退位": "从高一位拆一个十来用。"},
            prerequisites=["place_value_decimal_system"],
            next_topics=["arithmetic_operations", "mixed_operations"],
            examples=["一共有多少本书", "还剩多少个苹果"],
            route=["合并或拿走", "按位对齐", "满十进一", "不够退一"],
            visuals=["数轴", "计数器"],
            conceptual_layers=[
                "加减法先是动作：合起来、拿走、比差距。算式只是把动作记下来。",
                "竖式的全部道理是一句话：相同单位才能直接相加减，所以数位要对齐。",
                "进位和退位不是新规则，就是位值反着用：满十捆走送上位，不够就从上位拆一个下来。",
            ],
            worked_examples=[
                WorkedExample(
                    title="37+25：满十为什么要进一",
                    problem="计算 37 + 25。",
                    steps=[
                        "个位：7+5=12。12 里藏着 1 个十和 2 个一。",
                        "2 留在个位；那个十不属于个位，捆起来送到十位——这就是「进 1」。",
                        "十位：3 个十加 2 个十，再加送来的 1 个十，共 6 个十。",
                        "所以 37+25=62。",
                    ],
                    answer_check="用 62-25 倒回去，能回到 37，说明进位的十没有丢。",
                ),
                WorkedExample(
                    title="52-38：退位「借」的到底是什么",
                    problem="计算 52 - 38。",
                    steps=[
                        "个位 2 减 8 不够减。",
                        "从十位拆 1 个十下来：52 变成 4 个十和 12 个一。数没变，只是换了摆法。",
                        "个位：12-8=4。十位：4-3=1。",
                        "所以 52-38=14。",
                    ],
                    answer_check="14+38 应该正好回到 52；加回去对不上，就是退位时把数弄丢了。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="用小棒或画图，把 37+25 里「进一」的那个动作演一遍。",
                    goal="亲眼看见进位捆走的是什么。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="算 63-27，边算边说出每一位正在做什么。",
                    goal="退位靠理解，不靠背口诀。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="带 50 元买 32 元的书，还剩多少？"
                    "列式，并说出这是「拿走」还是「比差距」。",
                    goal="把算式接回生活里的数量动作。",
                ),
            ],
            reflection_questions=[
                "为什么个位的数不能直接和十位的数相加？",
                "进位写的那个小「1」，和个位上的「1」一样大吗？",
                "减法算完之后，怎么自己检查对不对？",
            ],
        ),
        _point(
            topic_id="multiplication_meaning",
            name="乘法的意义",
            grade_band=GradeBand.PRIMARY,
            grade="二年级上册",
            chapter="表内乘法",
            section="乘法的初步认识",
            human="乘法是在说几个相同的组一共有多少。",
            why="面积、比例、函数里的倍数关系都从乘法意义长出来。",
            terms={"几个几": "有几组，每组有同样多个。", "因数": "参与相乘的数。"},
            prerequisites=["integer_addition_subtraction"],
            next_topics=["division_meaning", "arithmetic_operations"],
            formulas=["a x b"],
            examples=["3盒彩笔，每盒6支", "4排座位，每排8个"],
            route=["重复加法", "相同组", "几个几", "乘法式子"],
            visuals=["阵列图", "分组图"],
            conceptual_layers=[
                "乘法不是新运算，是「同一个数加很多遍」的省事写法：每盒 6 支、3 盒，就是 6+6+6。",
                "用乘法的前提是「相同的组」：每组一样多才能乘；组不一样多，就先别乘。",
                "把组摆成一行一行，就是阵列："
                "横着看是 3 个 6，竖着看是 6 个 3——所以交换因数，总数不变。",
            ],
            worked_examples=[
                WorkedExample(
                    title="3 盒彩笔一共几支",
                    problem="每盒彩笔 6 支，3 盒一共多少支？",
                    steps=[
                        "先确认是「相同的组」：每盒都是 6 支，共 3 组。",
                        "用加法写：6+6+6=18。",
                        "加的都是同一个 6，改写成乘法：6×3=18，读作 3 个 6。",
                        "摆成 3 行 6 列的点阵，横着数、竖着数都是 18——因数交换，总数不变。",
                    ],
                    answer_check="能指着式子说出 6、3、18 各对应生活里的什么。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="找一个生活里「几个几」的例子（如 4 排椅子每排 8 把），"
                    "用加法和乘法各写一遍。",
                    goal="体会乘法是相同加数的简写。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="画阵列图，说明 5×3 和 3×5 为什么一样多。",
                    goal="交换律有画面，不是背出来的。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="3 盒彩笔分别是 6 支、6 支、5 支，还能直接用 6×3 算总数吗？为什么？",
                    goal="识别「每组一样多」这个乘法前提。",
                ),
            ],
            reflection_questions=[
                "乘法帮我们省了什么事？",
                "什么时候不能直接用乘法算总数？",
                "看到 4×7，你脑子里出现的是什么画面？",
            ],
        ),
        _point(
            topic_id="division_meaning",
            name="除法的意义",
            grade_band=GradeBand.PRIMARY,
            grade="二年级下册",
            chapter="表内除法",
            section="平均分",
            human="除法是在平均分，或者看一个数量里有几个同样的组。",
            why="分数、比、比例和概率都需要理解平均分和每份多少。",
            terms={"平均分": "每份一样多。", "商": "除法算出的结果。"},
            prerequisites=["multiplication_meaning"],
            next_topics=["fraction", "arithmetic_operations"],
            formulas=["a ÷ b"],
            examples=["12颗糖平均分给4人", "18里面有几个3"],
            route=["平均分", "每份多少", "有几个组", "除法式子"],
            visuals=["分物图", "线段图"],
            conceptual_layers=[
                "除法有两张脸：平均分（12 颗糖分给 4 人，每人几颗）和包含（12 里面有几个 3）。",
                "除法和乘法是一对：12÷4=3，靠的是 4×3=12。会乘法口诀，就会算除法。",
                "分不完剩下的叫余数。余数一定比除数小——不然还够再分一轮。",
            ],
            worked_examples=[
                WorkedExample(
                    title="12 颗糖的两种分法",
                    problem="12 颗糖：(1) 平均分给 4 个人，每人几颗？(2) 每 3 颗装一袋，能装几袋？",
                    steps=[
                        "第 (1) 问是「平均分」：一人一颗轮着发，发完每人 3 颗，记作 12÷4=3。",
                        "第 (2) 问是「包含」：数 12 里面有几个 3，能装 4 袋，记作 12÷3=4。",
                        "两问都用除法，但一个在求「每份多少」，一个在求「有几份」。",
                        "都能用乘法验证：4×3=12，正好分完。",
                    ],
                    answer_check="拿到除法应用题，先说出它问的是「每份多少」还是「有几份」。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="用 18 个小物件，把 18÷6 的两种问法各演示一遍。",
                    goal="两种除法画面都亲手摆过。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="算 14÷4，说清商和余数各是什么，余数为什么不能是 4。",
                    goal="理解「余数小于除数」的道理。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="全班 27 人春游，每辆车坐 6 人，需要几辆车？答案能是 4.5 吗？",
                    goal="余数在真实问题里要「进一」处理。",
                ),
            ],
            reflection_questions=[
                "12÷4 和 12÷3 问的问题有什么不同？",
                "为什么算除法可以靠乘法口诀？",
                "如果余数等于除数了，说明什么？",
            ],
        ),
        _point(
            topic_id="mixed_operations",
            name="四则混合运算",
            grade_band=GradeBand.PRIMARY,
            grade="三年级下册至四年级下册",
            chapter="四则运算",
            section="运算顺序",
            human="混合运算是在一个式子里安排多个数量动作的先后顺序。",
            why="应用题列综合算式、解方程和代数式变形都要守住运算顺序。",
            terms={"括号": "提醒里面先看作一个整体。", "运算顺序": "先算什么、后算什么的规则。"},
            prerequisites=[
                "integer_addition_subtraction",
                "multiplication_meaning",
                "division_meaning",
            ],
            next_topics=["distributive_property", "algebraic_expression"],
            examples=["先买几盒再加散装", "总价减优惠再平均分"],
            route=["一个动作", "多个动作", "先乘除后加减", "括号优先"],
            visuals=["步骤树", "数量动作图"],
            conceptual_layers=[
                "运算顺序不是随便定的规矩：先乘除后加减，"
                "是因为乘除算的是「一组的总量」，得先把组算清，才能和散的合并。",
                "括号的意思是「里面先看成一个整体」：同样的数字，括号位置不同，讲的就是不同的事。",
                "列综合算式，就是把一件事的先后动作写进一个式子；运算顺序在替你记住动作的先后。",
            ],
            worked_examples=[
                WorkedExample(
                    title="为什么 20−3×4 不先算减法",
                    problem="买 3 支单价 4 元的笔，付 20 元，找回多少？算式是 20−3×4。",
                    steps=[
                        "3×4 算的是「笔的总价」，是一组量，必须先算：12 元。",
                        "再从 20 元里拿走 12 元：20−12=8 元。",
                        "若从左往右先算 20−3=17，17 对应题里的什么量？什么都不是。"
                        "运算顺序一错，式子就讲不通事了。",
                    ],
                    answer_check="把 (20−3)×4 也算出来，想想它对应的是另一个什么故事。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="给 18÷3+2 编一个买东西的故事，说出每一步在算什么。",
                    goal="式子背后有事情。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="算 5+3×6 和 (5+3)×6，说说差别在哪里。",
                    goal="括号改变故事。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="总价 100 元，先减 10 元优惠，再平均分给 3 人：列成一个综合算式。",
                    goal="把动作装进一个式子。",
                ),
            ],
            reflection_questions=[
                "先乘除后加减，是硬性规定还是有道理的？",
                "括号在替你说什么话？",
                "运算顺序算错时，得出的数还对应题里的量吗？",
            ],
        ),
        _point(
            topic_id="decimal",
            name="小数",
            grade_band=GradeBand.PRIMARY,
            grade="三年级下册至四年级下册",
            chapter="小数的初步认识 / 小数的意义和性质",
            section="小数表示与大小比较",
            human="小数是把1继续平均分成十分、百分、千分后写出来的数。",
            why="测量、钱数、百分数和函数图像都经常使用小数。",
            terms={"小数点": "整数部分和小数部分的分界。", "十分之一": "把1平均分成10份中的1份。"},
            prerequisites=["place_value_decimal_system", "division_meaning"],
            next_topics=["decimal_operations", "percent"],
            examples=["1.5米", "3.25元"],
            route=["单位1", "继续平均分", "十分位", "百分位", "小数点"],
            visuals=["数轴", "方格纸"],
            conceptual_layers=[
                "小数不是新的数，是位值往右边接着写：个位右边点个点，"
                "第一位是十分之几，第二位是百分之几。",
                "0.3 就是把 1 平均分成 10 份取 3 份——和分数 3/10 说的是同一件事，写法不同。",
                "有了小数，钱、身高、体重这些「不是整数」的量就都能精确写下来了。",
            ],
            worked_examples=[
                WorkedExample(
                    title="1 元 2 角为什么写成 1.2 元",
                    problem="1 元 2 角，用「元」做单位该怎么写？",
                    steps=[
                        "1 元 = 10 角，所以 1 角就是十分之一元。",
                        "2 角就是 2 个十分之一元，写在小数点后第一位：0.2 元。",
                        "合起来：1 元 2 角 = 1.2 元。小数点是「整数部分到此为止」的分界记号。",
                    ],
                    answer_check="能说出 1.2 里的 1 和 2 各表示什么（1 个一、2 个十分之一）。",
                ),
                WorkedExample(
                    title="0.3 和 0.30 一样大吗",
                    problem="0.3 和 0.30，哪个大？",
                    steps=[
                        "0.3 是 3 个十分之一。",
                        "0.30 是 30 个百分之一——把每个十分之一再切成 10 小份，"
                        "30 小份正好是原来的 3 份。",
                        "所以一样大：末尾添 0 只是切得更细，数量没有变多。",
                    ],
                    answer_check="在 10×10 方格图上分别涂出 0.3 和 0.30，比较涂色面积。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="用钱说一说 3.75 元里每个数字表示多少。",
                    goal="把每个小数位和它的单位对上。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="在数轴 0 和 1 之间标出 0.4 和 0.8 的位置。",
                    goal="小数在数轴上有确定位置。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="身高 1.62 米，6 在哪一位、表示多少米？",
                    goal="把小数位值用到测量里。",
                ),
            ],
            reflection_questions=[
                "小数点右边第一位为什么是「十分之几」，不是「九分之几」？",
                "0.5 和 1/2 是同一个数吗？",
                "什么时候整数不够用，必须用小数？",
            ],
        ),
        _point(
            topic_id="decimal_operations",
            name="小数运算",
            grade_band=GradeBand.PRIMARY,
            grade="五年级上册",
            chapter="小数乘法与小数除法",
            section="小数四则计算",
            human="小数运算还是数量动作，只是单位被分得更细。",
            why="实际测量和初中函数里的数值计算经常要用小数。",
            terms={"小数位": "小数点右边的位置。", "近似数": "接近准确值、方便使用的数。"},
            prerequisites=["decimal", "arithmetic_operations"],
            next_topics=["ratio", "linear_function"],
            examples=["每千克2.5元买3.2千克", "速度和时间相乘求路程"],
            route=["看单位", "按整数方法想", "处理小数点", "估算检验"],
            visuals=["面积模型", "数轴"],
            conceptual_layers=[
                "小数计算和整数计算是同一套动作，只是有的位表示十分之几、"
                "百分之几，得管好小数点。",
                "加减要「小数点对齐」（相同数位才能相加）；乘法先当整数算，"
                "再数两个因数一共几位小数，点回去。",
                "加减对齐小数点，乘法数小数位数——用错规则，小数点就点歪。",
            ],
            worked_examples=[
                WorkedExample(
                    title="2.5 元/千克买 3.2 千克",
                    problem="苹果每千克 2.5 元，买 3.2 千克要多少钱？",
                    steps=[
                        "先当整数算：25×32=800，小数点先放一边。",
                        "数小数位：2.5 有 1 位，3.2 有 1 位，一共 2 位小数。",
                        "从 800 末尾往左数 2 位点上小数点：8.00，也就是 8 元。"
                        "估一下 2.5×3≈7.5，8 元合理。",
                    ],
                    answer_check="说说乘法为什么数「位数」，加法却要「对齐小数点」。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="摆一摆 1.2 + 0.35，说说为什么要把小数点对齐再加。",
                    goal="加减先对齐数位。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="算 0.4 × 0.3，说说结果为什么是 0.12 不是 1.2。",
                    goal="会数小数位数点小数点。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="每分钟走 0.08 千米，走 15 分钟多远？先估再算。",
                    goal="小数乘法用到行程。",
                ),
            ],
            reflection_questions=[
                "小数加法为什么要对齐小数点，而不是对齐末位？",
                "两个小于 1 的小数相乘，积为什么反而更小？",
                "什么时候先估算能帮你发现小数点点错了？",
            ],
        ),
        _point(
            topic_id="fraction_operations",
            name="分数运算",
            grade_band=GradeBand.PRIMARY,
            grade="五年级下册至六年级上册",
            chapter="分数的意义和性质 / 分数乘法与除法",
            section="通分、约分与分数四则运算",
            human="分数运算是在同一个单位1下处理几份、几倍和平均分。",
            why="比例、概率、代数分式都需要学生真正懂分数运算。",
            terms={
                "通分": "把分母变成相同，方便比较或加减。",
                "约分": "把分子分母同时缩小但大小不变。",
            },
            prerequisites=["fraction", "division_meaning"],
            next_topics=["ratio", "probability"],
            formulas=["a/b + c/d", "a/b x c/d"],
            examples=["半杯水再加四分之一杯", "一段路的三分之二"],
            route=["单位1", "同分母", "通分", "约分", "乘除意义"],
            visuals=["面积模型", "数轴"],
            conceptual_layers=[
                "分数加减是「先把份切成一样大，再数份数」；"
                "分数乘除是「取几分之几、平均分成几份」。",
                "分母不同不能直接加，像「3 个苹果 + 2 个橘子」说不清一共几个——"
                "通分就是把两边都换成同样大小的份。",
                "加减要通分（比份数），乘法却不用（1/2 的 1/3 直接分子乘分子）——"
                "两件事，别混。",
            ],
            worked_examples=[
                WorkedExample(
                    title="半杯水加四分之一杯",
                    problem="1/2 杯水再加 1/4 杯水，一共几杯？",
                    steps=[
                        "两个分数分母不同：一个按「半份」数，一个按「四分之一份」数，"
                        "单位不一样不能直接加。",
                        "通分：把 1/2 换成 2/4（半杯就是 2 个四分之一杯），份的大小统一了。",
                        "现在都是四分之一杯：2/4 + 1/4 = 3/4 杯。",
                    ],
                    answer_check="说说为什么不能写成 (1+1)/(2+4)=2/6。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="用一块饼画图说明 1/3 + 1/3 = 2/3，并讲讲分母为什么不变。",
                    goal="同分母加减就是数份数。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="算 1/2 + 1/3，先说通分成了几分之几。",
                    goal="会把异分母通分再加。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="一段路走了它的 2/3，这 2/3 里的 1/2 是全程的几分之几？",
                    goal="分数乘法就是「取几分之几」。",
                ),
            ],
            reflection_questions=[
                "分数相加为什么必须先通分，相乘却不用？",
                "约分把数字变小了，为什么大小没变？",
                "「一半的一半」为什么是 1/4，不是 1/2？",
            ],
        ),
        _point(
            topic_id="percent",
            name="百分数",
            grade_band=GradeBand.PRIMARY,
            grade="六年级上册",
            chapter="百分数",
            section="百分数的意义和应用",
            human="百分数是把比较的标准统一成100份。",
            why="折扣、增长率、统计图和概率表达都会用百分数。",
            terms={"百分号": "表示以100为标准。", "增长率": "增加的部分占原来的百分之几。"},
            prerequisites=["fraction", "decimal"],
            next_topics=["probability", "data_analysis"],
            formulas=["a% = a/100"],
            examples=["打八折", "正确率95%"],
            route=["单位1", "100份", "占几份", "百分号", "实际问题"],
            visuals=["百格图", "条形图"],
            conceptual_layers=[
                "百分数是「统一分母的分数」：都换成一百份，25% 就是 100 份里的 25 份，"
                "比较起来一眼见分晓。",
                "百分数永远相对「单位 1」：同样是 50%，半块蛋糕和半桌蛋糕差远了——"
                "先问「是谁的百分之几」。",
                "打八折就是按原价的 80% 收钱；增长 20% 就是在原来基础上再加 20/100。",
            ],
            worked_examples=[
                WorkedExample(
                    title="八折到底便宜了多少",
                    problem="原价 120 元的鞋打八折，现价多少？便宜了多少？",
                    steps=[
                        "八折 = 原价的 80%，这里的「单位 1」是原价 120 元。",
                        "现价：120×80% = 120×0.8 = 96 元。",
                        "便宜的部分：120−96=24 元；也可以直接算 120×20%。"
                        "两条路结果相同，因为 80%+20%=100%。",
                    ],
                    answer_check="换成七五折再算一遍，验证「现价+便宜的=原价」。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="找三个生活里的百分数（电量、折扣、成分表），各说出它的「单位 1」是谁。",
                    goal="百分数有主语。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="把 3/4、0.6、45% 从小到大排。",
                    goal="分数、小数、百分数互相翻译。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="先涨价 10% 再降价 10%，回到原价了吗？动手算给自己看。",
                    goal="发现「单位 1」中途换了人。",
                ),
            ],
            reflection_questions=[
                "百分数和分数、小数，是三种数还是三种写法？",
                "「增长 50%」和「是原来的 50%」一样吗？",
                "为什么百分数方便比较？",
            ],
        ),
        _point(
            topic_id="ratio",
            name="比",
            grade_band=GradeBand.PRIMARY,
            grade="六年级上册",
            chapter="比",
            section="比的意义",
            human="比是在比较两个数量之间的倍数关系。",
            why="比例、相似、三角函数和函数斜率都离不开比。",
            terms={
                "前项": "比号前面的量。",
                "后项": "比号后面的量。",
                "比值": "两个量相除得到的数。",
            },
            prerequisites=["fraction", "division_meaning"],
            next_topics=["proportion", "similar_triangles"],
            formulas=["a:b = a ÷ b"],
            examples=["果汁和水的配比", "地图比例尺"],
            route=["两个量", "谁和谁比", "除法", "比值", "等价的比"],
            visuals=["线段图", "双数轴"],
            conceptual_layers=[
                "比在回答「几倍、几分之几」：糖 2 勺、水 6 勺，糖比水是 2:6——"
                "说的是倍数关系，不是「差 4 勺」。",
                "2:6 和 1:3 是同一个比：两边同乘同除一个数，浓淡不变。这就是化简比。",
                "比、分数、除法是一家：2:6 = 2/6 = 2÷6。三种写法，一个意思。",
            ],
            worked_examples=[
                WorkedExample(
                    title="冲糖水：比在管什么",
                    problem="糖和水按 1:3 冲糖水。用 2 勺糖该配几勺水？用 4 勺糖呢？",
                    steps=[
                        "1:3 的意思是「水是糖的 3 倍」，和勺子大小无关。",
                        "2 勺糖 → 水 2×3=6 勺。比变成 2:6，化简还是 1:3，一样甜。",
                        "4 勺糖 → 水 12 勺。只要按同一倍数放大，味道不变。",
                        "若 2 勺糖配了 5 勺水，比是 2:5，不等于 1:3——比一变，关系就变了。",
                    ],
                    answer_check="3 勺糖配 9 勺水、4 勺糖配 12 勺水，哪杯更甜？算比就知道。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="说说 4:6 化简成 2:3 之后，什么变了、什么没变。",
                    goal="化简比不变味。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="把 12:18 化成最简比，再分别写成分数和除法。",
                    goal="三种写法互相翻译。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="按 3:2 把 30 颗糖分给两个人，各得几颗？提示：先想一共分成几份。",
                    goal="按比分配=先数份数。",
                ),
            ],
            reflection_questions=[
                "「比」和「差」各在描述什么？",
                "球赛比分 3:2 是数学里的比吗？能化简成 1.5:1 吗？",
                "化简比的时候，什么变了，什么没变？",
            ],
        ),
        _point(
            topic_id="proportion",
            name="比例",
            grade_band=GradeBand.PRIMARY,
            grade="六年级下册",
            chapter="比例",
            section="正比例、反比例和比例尺",
            human="比例是在说两个比相等，或者两个量按稳定规则一起变。",
            why="一次函数、反比例函数、相似图形和建模都需要比例直觉。",
            terms={
                "正比例": "一个量变成几倍，另一个量也变成几倍。",
                "反比例": "一个量变大，另一个量按乘积不变的方式变小。",
            },
            prerequisites=["ratio", "quantity_relationship"],
            next_topics=["linear_function", "inverse_proportion_function"],
            formulas=["a:b = c:d", "y = kx", "xy = k"],
            examples=["速度一定时路程和时间", "总量一定时每份和份数"],
            route=["比", "两个比相等", "变化关系", "正比例", "反比例"],
            visuals=["表格", "双数轴", "关系图"],
            conceptual_layers=[
                "比例是在说「两个比一样大」，或者两个量手拉手一起变，"
                "变的规矩是固定的。",
                "正比例是一个变 2 倍另一个也跟着变 2 倍，y 与 x 的比值不变；"
                "反比例是一个变 2 倍另一个反而变一半，x 与 y 的乘积不变。",
                "别把「一起变大」都当正比例：年龄和身高都在长，"
                "但不成固定比，就不是正比例。",
            ],
            worked_examples=[
                WorkedExample(
                    title="3 支笔 6 元，7 支多少钱",
                    problem="铅笔单价一样，3 支 6 元，买 7 支要多少钱？",
                    steps=[
                        "单价固定，钱数和支数成正比例：钱数÷支数就是每支的价，是个不变的数。",
                        "先求这个不变的比值：6÷3=2，每支 2 元。",
                        "7 支就是 7×2=14 元。也可以列 3∶6 = 7∶x，同样得 x=14。",
                    ],
                    answer_check="换成「12 元能买几支」，说说你靠的还是不是「单价不变」这一条。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="举一个正比例、一个反比例的生活例子，各说清谁保持不变。",
                    goal="分清「比值不变」和「乘积不变」。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="每小时 60 千米，2 小时、3 小时各走多远？算算路程÷时间变不变。",
                    goal="从数据里认出正比例。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="12 块糖分给小朋友，人越多每人越少，这是正比例还是反比例？",
                    goal="用「乘积不变」认出反比例。",
                ),
            ],
            reflection_questions=[
                "「两个量一起变大」一定是正比例吗？为什么？",
                "正比例盯住「比值不变」，反比例盯住什么不变？",
                "如果 x 变大 y 也变大，但比值忽大忽小，还算正比例吗？",
            ],
        ),
        _point(
            topic_id="negative_number_intro",
            name="负数初步",
            grade_band=GradeBand.PRIMARY,
            grade="六年级下册",
            chapter="负数",
            section="正负数表示相反意义的量",
            human="负数用来表示和正方向相反的量。",
            why="初中有理数、坐标系、不等式都要用负数。",
            terms={"正方向": "事先规定为正的方向。", "相反意义": "比如高于和低于、收入和支出。"},
            prerequisites=["number_recognition"],
            next_topics=["rational_numbers", "coordinate_plane"],
            examples=["零上和零下", "收入和支出"],
            route=["相反意义", "0作分界", "正数", "负数", "数轴"],
            visuals=["温度计", "数轴"],
            conceptual_layers=[
                "负数是给「方向相反的量」记账用的：零上 3 度记作 +3，零下 3 度记作 −3。",
                "0 不只是「没有」，它是正负的分界点、比较的基准。",
                "数轴上往右是正、往左是负：−5 在 −2 左边，所以 −5 < −2——负数离 0 越远反而越小。",
            ],
            worked_examples=[
                WorkedExample(
                    title="零下 3 度和零下 8 度谁更冷",
                    problem="冬天，甲地 −3℃，乙地 −8℃，哪里更冷？",
                    steps=[
                        "两个温度都在 0 度以下，负号表示「比 0 度低」。",
                        "−8 是低 8 度，−3 是低 3 度：低得更多的更冷。",
                        "画数轴：−8 在 −3 的左边，更小。所以 −8℃ < −3℃，乙地更冷。",
                    ],
                    answer_check="能讲出「负数比大小，离 0 越远越小」的道理，而不是背口诀。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="找三个生活中的负数（温度、楼层、余额），说说各自的 0 表示什么。",
                    goal="体会负数总是相对某个基准。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="在数轴上标出 −4、−1、2，再按从小到大排。",
                    goal="负数在数轴上有位置、可比较。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="收入记 +、支出记 −：先 +50 再 −30，最后离 0 多远？",
                    goal="为有理数加减做准备。",
                ),
            ],
            reflection_questions=[
                "如果没有负数，「零下 3 度」该怎么记？",
                "−7 和 −2 谁大？为什么和正数的感觉相反？",
                "0 是正数还是负数？",
            ],
        ),
        _point(
            topic_id="primary_equation",
            name="简易方程",
            grade_band=GradeBand.PRIMARY,
            grade="五年级上册",
            chapter="简易方程",
            section="用字母表示数与解简易方程",
            human="简易方程是把不知道的数先用字母占位，再用等量关系找出来。",
            why="这是从算术走向代数的关键桥梁。",
            terms={"字母": "暂时代替一个数的符号。", "解方程": "找出让等式成立的未知数。"},
            prerequisites=["equality", "quantity_relationship", "mixed_operations"],
            next_topics=["linear_equation_one_variable"],
            examples=["已知总价求数量", "已知周长求边长"],
            route=["不知道的数", "用字母表示", "等量关系", "方程", "求解"],
            visuals=["天平模型", "线段图"],
            conceptual_layers=[
                "方程就是「有字母占位的等式」：x+3=8 说的是「某个数加 3 之后等于 8」。",
                "解方程不是猜谜，是让天平保持平衡地做手术：两边同时减 3，x 就自己露出来了。",
                "「解」是让等式成立的那个数：把 x=5 塞回去，5+3 真的等于 8，才算解对。",
            ],
            worked_examples=[
                WorkedExample(
                    title="x+3=8：天平两边同时拿",
                    problem="解方程 x+3=8。",
                    steps=[
                        "把等式看成天平：左盘放着 x 和 3，右盘放着 8，现在是平的。",
                        "两边同时拿走 3，天平还平：x = 8−3。",
                        "所以 x=5。检验：5+3=8，成立。",
                    ],
                    answer_check="解 x−2=6，每一步都说清「两边同时做了什么」。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="用天平的话讲一遍 x+4=10 在说什么。",
                    goal="方程先有画面。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="解 3x=12，说说两边同时做了什么。",
                    goal="乘除同样保持平衡。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="小明有一些糖，给了同学 5 颗还剩 7 颗：设 x 列方程并解出来。",
                    goal="从故事走到方程。",
                ),
            ],
            reflection_questions=[
                "x 是「不知道」还是「暂时不知道」？",
                "为什么两边必须同时做同样的事？",
                "解出来的数，怎么自己检查对不对？",
            ],
        ),
        _point(
            topic_id="measurement_units",
            name="常见量与单位",
            grade_band=GradeBand.PRIMARY,
            grade="二年级上册至三年级上册",
            chapter="长度单位 / 时、分、秒 / 质量单位",
            section="单位认识与换算",
            human="单位是在说明这个数到底数的是什么。",
            why="没有单位，测量、面积、速度和应用题都会失去意义。",
            terms={"单位": "约定好的测量标准。", "换算": "用不同单位表示同一个量。"},
            prerequisites=["number_recognition", "place_value_decimal_system"],
            next_topics=["perimeter", "area", "volume"],
            examples=["3米和3厘米不是一回事", "1小时等于60分钟"],
            route=["量什么", "选单位", "读数", "换算", "检验是否合理"],
            visuals=["尺子", "钟表", "天平"],
            conceptual_layers=[
                "量一个东西，就是数它里面有几个「标准的一份」——这一份就是单位。",
                "1 米 = 100 厘米不是两个数相等，是同一段长度换了大小不同的「一份」去数。",
                "写数量必须带单位：光一个「3」什么都不是，「3 米」「3 分钟」「3 元」才是话。",
            ],
            worked_examples=[
                WorkedExample(
                    title="1.5 米等于多少厘米",
                    problem="身高 1.5 米，是多少厘米？",
                    steps=[
                        "米和厘米量的是同一种东西（长度），只是「一份」大小不同：1 米 = 100 厘米。",
                        "1.5 米就是 1.5 个「100 厘米」：1.5×100=150 厘米。",
                        "换算就是换单位重新数：数字变大是因为「一份」变小了，长度本身没变。",
                    ],
                    answer_check="能说出为什么换成小单位后数字反而变大。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="找三样东西，分别说说用毫米、厘米、米、千米哪个量最合适。",
                    goal="单位和场景匹配。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="把 2 千克 50 克写成以克为单位，再写成以千克为单位。",
                    goal="两个方向的换算都通。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="3 小时和 200 分钟哪个长？先统一单位再比。",
                    goal="比较之前必须统一单位。",
                ),
            ],
            reflection_questions=[
                "为什么比较两个量之前要先统一单位？",
                "换算之后数字变了，量本身变了吗？",
                "「满十进一」和「1 米=100 厘米」像在哪里、不像在哪里？",
            ],
        ),
        _point(
            topic_id="line_angle_basic",
            name="线与角",
            grade_band=GradeBand.PRIMARY,
            grade="二年级下册至四年级上册",
            chapter="角的初步认识 / 角的度量",
            section="线段、直线、射线和角",
            human="线描述位置和方向，角描述两条线张开的大小。",
            why="平面图形、三角形、平行线和圆都需要线与角的语言。",
            terms={"线段": "有两个端点的一段直线。", "角": "从同一点出发的两条射线形成的图形。"},
            prerequisites=["measurement_units"],
            next_topics=["triangle_basic", "parallel_lines"],
            examples=["门打开的角度", "道路的交叉"],
            route=["点", "线段", "射线", "直线", "角", "度量"],
            visuals=["量角器", "折纸"],
            conceptual_layers=[
                "三种线的区别全在端点上：线段两个端点、能量长度；"
                "射线一个端点、往一头无限延伸；直线没有端点、两头无限。",
                "角不是两条边的长度，是两条射线从同一点张开的程度。边画多长，角都不变。",
                "量角的单位是度：把一整圈平均分成 360 份，一份就是 1°。直角 90°，平角 180°。",
            ],
            worked_examples=[
                WorkedExample(
                    title="边画长了，角会变大吗",
                    problem="用放大镜看一个 30° 的角，角变大了吗？",
                    steps=[
                        "放大镜把两条边显得更长、更粗。",
                        "但角量的是两条边张开的程度，不是边的长短。",
                        "拿量角器一量：还是 30°。角的大小只跟张开程度有关。",
                    ],
                    answer_check="画一个角，把两边各延长一倍，再量一次，确认度数没变。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="用两条手臂演示锐角、直角、钝角，说出各自和 90° 的关系。",
                    goal="角的大小有身体记忆。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="各画一条线段、射线、直线，标出端点，说说哪个能量长度。",
                    goal="三种线分得清。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="钟面 3 点整，时针和分针的夹角是多少度？怎么算出来的？",
                    goal="把「一圈 360°」用起来。",
                ),
            ],
            reflection_questions=[
                "为什么直线不能量长度，线段可以？",
                "角的两条边画得越长，角就越大吗？",
                "一圈为什么定成 360 度？想想 360 能被多少个数整除。",
            ],
        ),
        _point(
            topic_id="perimeter",
            name="周长",
            grade_band=GradeBand.PRIMARY,
            grade="三年级上册",
            chapter="长方形和正方形",
            section="周长",
            human="周长是一圈边线的总长度。",
            why="它帮助学生区分边界长度和内部面积。",
            terms={"边界": "图形最外面的一圈。", "总长度": "把每一段边长加起来。"},
            prerequisites=["measurement_units", "line_angle_basic"],
            next_topics=["area"],
            formulas=["长方形周长 = 2 x (长 + 宽)"],
            examples=["给操场围栏杆", "给画框包边"],
            route=["沿边走一圈", "每段边", "加起来", "公式只是简写"],
            visuals=["绕绳模型", "方格纸"],
            conceptual_layers=[
                "周长就是沿着图形边线走一圈的总长度——它是一个长度，单位用米、厘米。",
                "求周长的老实办法只有一个：把每条边加起来。"
                "长方形公式 (长+宽)×2 只是「四条边相加」的省写。",
                "弯曲的边线也有周长：用绳子沿边摆一圈，再拉直了量。",
            ],
            worked_examples=[
                WorkedExample(
                    title="篱笆要买多长",
                    problem="长方形菜地长 6 米、宽 4 米，围一圈篱笆需要多少米？",
                    steps=[
                        "围篱笆就是沿边走一圈：6+4+6+4。",
                        "两条长、两条宽，所以可以写成 (6+4)×2=20 米。",
                        "公式没有新东西，只是把「四条边相加」写得省事。",
                    ],
                    answer_check="把 6+4+6+4 逐边加一遍，结果和公式一致才算懂。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="用手指沿书本封面描一圈，说出周长指的是哪一段长度。",
                    goal="周长=边线一圈，有身体感觉。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="算边长 5 厘米的正方形周长，说说为什么可以用 5×4。",
                    goal="公式能退回到加法。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="画两个面积一样、形状不同的图形，量量周长一样吗？",
                    goal="周长和面积是两件事。",
                ),
            ],
            reflection_questions=[
                "周长的单位为什么是厘米，不是平方厘米？",
                "(长+宽)×2 里的「×2」是从哪来的？",
                "量弯曲边线的周长，用什么工具合适？",
            ],
        ),
        _point(
            topic_id="area",
            name="面积",
            grade_band=GradeBand.PRIMARY,
            grade="三年级下册至五年级上册",
            chapter="面积 / 多边形的面积",
            section="长方形、平行四边形、三角形和梯形面积",
            human="面积是在问一个平面图形里面铺了多少个单位小方格。",
            why="面积模型能解释乘法、分配律、几何公式和二次函数直觉。",
            terms={"面积单位": "用来铺满平面的单位小方格。", "底和高": "互相垂直的一组测量线。"},
            prerequisites=["perimeter", "multiplication_meaning"],
            next_topics=["volume", "distributive_property"],
            formulas=["长方形面积 = 长 x 宽", "三角形面积 = 底 x 高 ÷ 2"],
            examples=["铺地砖", "计算土地大小"],
            route=["铺方格", "数方格", "长乘宽", "割补转化", "公式"],
            visuals=["方格纸", "割补图"],
            conceptual_layers=[
                "面积是「铺满这块面需要多少个标准小方格」——数格子数出来的，"
                "单位是平方厘米、平方米。",
                "长方形面积=长×宽不是新规则：每行铺「长」个方格、铺「宽」行，乘法在数总格数。",
                "周长量边线一圈、面积量里面铺满，是两回事：周长相同的图形，面积可以差很远。",
            ],
            worked_examples=[
                WorkedExample(
                    title="长×宽到底在数什么",
                    problem="长 5 厘米、宽 3 厘米的长方形，面积是多少？",
                    steps=[
                        "用 1 平方厘米的小方格去铺：每行正好铺 5 个。",
                        "一共能铺 3 行。",
                        "总格数就是 5×3=15，所以面积是 15 平方厘米。"
                        "长×宽就是「每行个数×行数」。",
                    ],
                    answer_check="画出方格真数一遍，是 15 个，和公式一致。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="把手掌按在方格纸上描出轮廓，数格子估一估手掌面积。",
                    goal="面积=数格子，先于公式。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="算长 7 宽 4 的长方形面积，并说出单位为什么带「平方」。",
                    goal="单位有道理，不是装饰。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="周长都是 16 厘米的长方形，长和宽取多少时面积最大？列表试一试。",
                    goal="体会周长定了面积并没定。",
                ),
            ],
            reflection_questions=[
                "面积单位为什么叫「平方」厘米？",
                "长×宽和乘法的「几个几」有什么关系？",
                "两块地周长相等，面积一定相等吗？",
            ],
        ),
        _point(
            topic_id="volume",
            name="体积",
            grade_band=GradeBand.PRIMARY,
            grade="五年级下册",
            chapter="长方体和正方体",
            section="体积和容积",
            human="体积是在问一个立体里面能装多少个单位小正方体。",
            why="空间想象、单位换算和初中几何都需要体积直觉。",
            terms={"体积单位": "用来填满空间的小正方体。", "容积": "容器里面能装多少。"},
            prerequisites=["area", "measurement_units"],
            next_topics=["geometric_figures_intro"],
            formulas=["长方体体积 = 长 x 宽 x 高"],
            examples=["盒子能装多少", "水箱容量"],
            route=["一层方格", "很多层", "长宽高", "单位小正方体", "体积公式"],
            visuals=["积木模型", "展开图"],
            conceptual_layers=[
                "体积是「装满这个空间需要多少个标准小方块」，单位是立方厘米、立方米。",
                "长方体体积=长×宽×高：每层铺 长×宽 个小方块，一共叠「高」层。",
                "长度数线段、面积数方格、体积数方块——一维二维三维，"
                "贯穿的是同一个「数单位」的思想。",
            ],
            worked_examples=[
                WorkedExample(
                    title="长×宽×高在数什么",
                    problem="长 4 厘米、宽 3 厘米、高 2 厘米的长方体，体积是多少？",
                    steps=[
                        "底层用 1 立方厘米的小方块铺：每行 4 个、铺 3 行，一层 4×3=12 个。",
                        "一共叠 2 层：12×2=24 个。",
                        "所以体积是 24 立方厘米。公式就是「一层的个数×层数」。",
                    ],
                    answer_check="用积木或画图按层真数一遍，是 24 块。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="找家里一个盒子，说说它的体积到底在数什么。",
                    goal="体积=数方块，先有画面。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="算棱长 3 厘米的正方体体积，说说为什么是 3×3×3。",
                    goal="公式退回到分层数。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="把 24 个小方块摆成不同的长方体，长宽高有几种摆法？体积变了吗？",
                    goal="形状变了体积不变。",
                ),
            ],
            reflection_questions=[
                "长度、面积、体积的单位，分别在数什么？",
                "体积公式为什么比面积公式多乘一个数？",
                "两个盒子看上去差不多大，体积一定差不多吗？",
            ],
        ),
        _point(
            topic_id="data_collection_chart",
            name="数据收集与统计图",
            grade_band=GradeBand.PRIMARY,
            grade="一年级下册至六年级上册",
            chapter="统计",
            section="分类、记录、条形统计图和扇形统计图",
            human="统计图是把一堆数据整理成容易看出多少和变化的图。",
            why="初中统计、概率和现实判断都要先会看数据。",
            terms={"数据": "记录下来的数量或信息。", "统计图": "用图形显示数据。"},
            prerequisites=["number_recognition", "percent"],
            next_topics=["data_collection_description", "data_analysis"],
            examples=["统计喜欢的运动", "看各类支出占比"],
            route=["收集", "分类", "记录", "画图", "读结论"],
            visuals=["条形图", "折线图", "扇形图"],
            conceptual_layers=[
                "统计图不是把数字画好看，是让人「一眼看出」原始数据里藏着的多少和趋势。",
                "图各有专长：条形图比多少、折线图看变化趋势、扇形图看各部分占整体的比例。"
                "选错图，好数据也讲不清事。",
                "图会骗人：纵轴不从 0 开始，一点点差距会被放大成天壤之别。看图要先看坐标轴。",
            ],
            worked_examples=[
                WorkedExample(
                    title="比销量用哪种图，看趋势又用哪种",
                    problem="记录了一家店周一到周日的每日销量，想「比哪天最高」又想「看一周走势」，"
                    "各用什么图？",
                    steps=[
                        "「比哪天最高」是比多少：条形图，一根柱子一天，谁高谁多，一目了然。",
                        "「看一周走势」是看变化：折线图，点连成线，上坡下坡直接看出来。",
                        "如果想看「周末销量占全周几成」，那才轮到扇形图。图跟着问题走。",
                    ],
                    answer_check="给「班级各兴趣小组人数占比」选图，说出为什么不是折线图。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="收集全家一周每天的步数，先想清楚要回答什么问题再选图。",
                    goal="先有问题，再选图。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="把同一组数据分别画成条形图和折线图，说说各自更适合回答什么。",
                    goal="图和问题对得上。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="找一张纵轴不从 0 开始的图，说说它把差距夸大了多少。",
                    goal="学会怀疑地读图。",
                ),
            ],
            reflection_questions=[
                "同一堆数据，为什么要挑不同的图来画？",
                "扇形图适合表示什么，不适合表示什么？",
                "看统计图时，为什么要先看坐标轴？",
            ],
        ),
        _point(
            topic_id="average",
            name="平均数",
            grade_band=GradeBand.PRIMARY,
            grade="四年级下册",
            chapter="平均数与条形统计图",
            section="平均数",
            human="平均数是把总量重新分得一样多后每份是多少。",
            why="平均数是理解数据整体水平的第一种工具。",
            terms={"总量": "全部合起来的量。", "平均": "重新分成一样多。"},
            prerequisites=["division_meaning", "data_collection_chart"],
            next_topics=["data_analysis"],
            formulas=["平均数 = 总数 ÷ 份数"],
            examples=["平均身高", "平均每天读书页数"],
            route=["合起来", "重新平均分", "每份一样多", "代表整体水平"],
            visuals=["移多补少", "条形图"],
            conceptual_layers=[
                "平均数是「假如大家一样多，每份该是多少」——把总量重新匀开。",
                "算法是总数÷份数，背后是「移多补少」："
                "多的匀给少的，最后一样高的那个高度就是平均数。",
                "平均数是虚拟的代表值，可能谁都不等于它，"
                "还容易被一个特别大的数拉高。",
            ],
            worked_examples=[
                WorkedExample(
                    title="三次成绩的平均分",
                    problem="一个同学三次数学考 80、90、100 分，平均每次多少分？",
                    steps=[
                        "平均数是「假如三次一样高，每次几分」。",
                        "先合起来：80+90+100=270 分。",
                        "再平均分到 3 次：270÷3=90 分，相当于把 100 多出的 10 分匀给 80。",
                    ],
                    answer_check="如果第四次考了 70 分，平均分会升还是降？为什么。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="三摞书 4、5、6 本，用「移多补少」摆成一样高，看看每摞几本。",
                    goal="平均数就是匀平后的高度。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="求 2、4、9 三个数的平均数。",
                    goal="会用总数÷份数。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="一组数里混进一个特别大的数，平均数会怎样变？",
                    goal="体会平均数被极端值拉动。",
                ),
            ],
            reflection_questions=[
                "为什么平均数可能不等于其中任何一个数？",
                "加进一个很大的数，平均数为什么会被拉高？",
                "「移多补少」和「总数÷份数」为什么算出同一个数？",
            ],
        ),
        _point(
            topic_id="rational_numbers",
            name="有理数",
            grade_band=GradeBand.JUNIOR,
            grade="七年级上册",
            chapter="第一章 有理数",
            section="有理数及其运算",
            human="有理数把正数、0、负数、分数和小数放进同一个数的系统。",
            why="初中代数从有理数开始扩展数的范围。",
            terms={
                "正数": "比0大的数。",
                "负数": "比0小、表示相反意义的数。",
                "数轴": "用线上的点表示数。",
            },
            prerequisites=["negative_number_intro", "fraction", "decimal"],
            next_topics=["absolute_value", "real_numbers", "algebraic_expression"],
            examples=["海拔低于海平面", "收入和支出"],
            route=["相反意义", "0", "数轴", "正负数", "有理数运算"],
            visuals=["数轴", "温度计"],
            conceptual_layers=[
                "有理数是把学过的数收编成一家：正负整数、正负分数（含小数），"
                "都能写成两个整数的比。",
                "数轴是有理数的家：每个有理数在数轴上有唯一的位置，比大小就是比左右。",
                "绝对值是「离 0 的距离」：−3 和 3 离 0 一样远，所以 |−3|=|3|=3。距离不分方向。",
            ],
            worked_examples=[
                WorkedExample(
                    title="把一堆数放上数轴",
                    problem="把 −2、0.5、−1/2、3 放到数轴上，并从小到大排列。",
                    steps=[
                        "先认出同类：0.5 就是 1/2，−1/2 就是 −0.5。",
                        "负数在 0 左边：−2 比 −0.5 离 0 更远，所以更靠左、更小。",
                        "从左到右读出来：−2 < −1/2 < 0.5 < 3。左小右大，一条规则管所有有理数。",
                    ],
                    answer_check="换 −1.5、2/3、−3 再排一次，检验还是只用「左小右大」这一条规则。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="说说 0.75、−4、2/3 各属于有理数里的哪一类。",
                    goal="家族成员认得全。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="求 |−6| 和 |6|，并解释为什么相等。",
                    goal="绝对值就是距离。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="温度从 −3℃ 升高 5℃ 是多少度？在数轴上走一遍。",
                    goal="为有理数加减运算铺路。",
                ),
            ],
            reflection_questions=[
                "为什么要给整数和分数取一个统一的名字「有理数」？",
                "绝对值为什么永远不会是负数？",
                "数轴上任取两个数，怎么立刻判断谁大？",
            ],
        ),
        _point(
            topic_id="absolute_value",
            name="绝对值",
            grade_band=GradeBand.JUNIOR,
            grade="七年级上册",
            chapter="第一章 有理数",
            section="数轴、相反数和绝对值",
            human="绝对值是在问一个数离0有多远，不管方向。",
            why="比较大小、解不等式和距离问题都需要绝对值。",
            terms={"距离": "两个位置之间隔了多远。", "相反数": "离0一样远但方向相反的两个数。"},
            prerequisites=["rational_numbers"],
            next_topics=["inequalities"],
            formulas=["|a|"],
            examples=["-3和3离0都是3格"],
            route=["数轴", "方向", "距离", "离0多远", "绝对值符号"],
            visuals=["数轴"],
            conceptual_layers=[
                "绝对值就是「离 0 有多远」，只问距离、不问方向，"
                "所以永远不会是负的。",
                "|−3| 和 |3| 都等于 3，因为它们在数轴上离 0 都是 3 格；"
                "一对相反数的绝对值相等。",
                "别把「加负号」当「取绝对值」：−(−3)=3 是相反数，"
                "|−3|=3 是距离，路子不同却常撞出同一个答案。",
            ],
            worked_examples=[
                WorkedExample(
                    title="|−5| 和 |5| 谁大",
                    problem="求 |−5| 和 |5|，比比谁大。",
                    steps=[
                        "绝对值问「离 0 多远」：−5 在 0 左边 5 格，|−5|=5。",
                        "5 在 0 右边 5 格，|5|=5。",
                        "两个都是 5，一样大——方向相反，离 0 的距离却相同。",
                    ],
                    answer_check="|0| 是多少？说说为什么绝对值不可能是负数。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="在数轴上标出 −4 和 4，数一数各离 0 几格。",
                    goal="绝对值就是数轴上的距离。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="求 |−7|、|2|、|−1/2|。",
                    goal="会去掉符号只留距离。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="两个数的绝对值都是 6，它们可能是谁？",
                    goal="一个绝对值对应一对相反数。",
                ),
            ],
            reflection_questions=[
                "绝对值为什么永远不会是负数？",
                "|−3| 和 −(−3) 得数一样，意思一样吗？",
                "绝对值相等的两个数，一定相等吗？",
            ],
        ),
        _point(
            topic_id="power_scientific_notation",
            name="乘方与科学记数法",
            grade_band=GradeBand.JUNIOR,
            grade="七年级上册",
            chapter="第一章 有理数",
            section="有理数的乘方",
            human="乘方是同一个数连续相乘的简写。",
            why="大数、小数、面积体积增长和二次函数都用到乘方。",
            terms={"底数": "被重复相乘的数。", "指数": "重复相乘的次数。"},
            prerequisites=["multiplication_meaning", "rational_numbers"],
            next_topics=["quadratic_equation", "quadratic_function"],
            formulas=["a^n", "a x 10^n"],
            examples=["10的6次方表示一百万", "正方形面积用边长的平方"],
            route=["重复乘", "简写", "底数", "指数", "科学记数法"],
            visuals=["方格面积", "数量级尺"],
            conceptual_layers=[
                "乘方是「同一个数连乘」的简写：2×2×2 写成 2³，读作 2 的 3 次方。"
                "写法省事，增长惊人。",
                "10 的乘方专门管「数量级」：10³=1000，10⁶ 是一百万——指数正好是 0 的个数。",
                "科学记数法 a×10ⁿ（a 在 1 到 10 之间）是大数小数的标准格式，比大小先看指数。",
            ],
            worked_examples=[
                WorkedExample(
                    title="对折 10 次的纸有多少层",
                    problem="一张纸对折 1 次是 2 层，对折 10 次是多少层？",
                    steps=[
                        "每折一次层数乘 2：折 10 次就是 10 个 2 连乘。",
                        "写成乘方：2¹⁰。分步算：2⁵=32，2¹⁰=32×32=1024。",
                        "折 10 次就破千层——乘方长得比乘法快得多，所以它配得上一个专门记号。",
                    ],
                    answer_check="算一算 2⁵ 和 5²，确认底数和指数不能随便交换。",
                ),
                WorkedExample(
                    title="地球到太阳的距离怎么写",
                    problem="把 150000000 千米写成科学记数法。",
                    steps=[
                        "把小数点往左挪，挪到只剩一位整数：1.5，一共挪了 8 位。",
                        "挪 8 位相当于除以 10⁸，要补回来就乘 10⁸。",
                        "所以 150000000 = 1.5×10⁸ 千米。指数 8 记录的就是小数点挪的位数。",
                    ],
                    answer_check="把 1.5×10⁸ 反着展开，数一数 0 的个数，回到原数。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="把 3×3×3×3 写成乘方，说出底数和指数各管什么。",
                    goal="记号各就各位。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="比较 2³ 和 3² 的大小，再写出 10⁴ 等于多少。",
                    goal="小指数算得熟。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="光速约 3×10⁸ 米/秒，声速约 340 米/秒，大约差几个数量级？",
                    goal="学会用指数比数量级。",
                ),
            ],
            reflection_questions=[
                "2³ 和 3×2 差在哪里？",
                "科学记数法为什么规定 a 要在 1 到 10 之间？",
                "指数每加 1，数变成原来的几倍？",
            ],
        ),
        _point(
            topic_id="algebraic_expression",
            name="整式",
            grade_band=GradeBand.JUNIOR,
            grade="七年级上册",
            chapter="第二章 整式的加减",
            section="整式",
            human="整式是用数、字母和加减乘方拼出的数量表达。",
            why="方程、函数和公式都需要先会读懂式子。",
            terms={"单项式": "没有加减分开的一个整式块。", "多项式": "几个单项式加减组成的式子。"},
            prerequisites=["primary_equation", "mixed_operations"],
            next_topics=["like_terms", "polynomial_multiplication"],
            examples=["3x表示3个x", "2a+5表示某个量再加5"],
            route=["具体数", "字母代替数", "项", "整式", "式子含义"],
            visuals=["式子结构树", "面积模型"],
            conceptual_layers=[
                "字母是数的「代表」：a+a+a 写成 3a，不是新东西，"
                "就是「3 个 a」——乘法的意义原样搬过来。",
                "同类项才能合并：3a+2a=5a（5 个 a）；但 3a+2b 合不了——"
                "3 个苹果加 2 根香蕉，还是两样东西。",
                "式子会算数：把 a=4 代进 3a+2 得 14。整式就是「装着任意数的算式」。",
            ],
            worked_examples=[
                WorkedExample(
                    title="3a+2a 能合并，3a+2b 为什么不能",
                    problem="化简 3a+2a 和 3a+2b。",
                    steps=[
                        "3a 是 3 个 a，2a 是 2 个 a：合起来 5 个 a，写作 5a。",
                        "3a+2b 是 3 个 a 和 2 个 b：数的不是同一种东西，只能原样写着。",
                        "「同类项」的意思就是「数的是同一种东西」，这是合并的前提。",
                    ],
                    answer_check="代 a=2、b=5 检验：3a+2a=10=5a 成立；"
                    "3a+2b=16，而 5ab=50——乱并会算错。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="用「几个几」的话解释 4x 和 x⁴ 的区别。",
                    goal="记号不打架。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="化简 5m+3−2m+4，先说出哪些是同类项。",
                    goal="同类项挑得出来。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="用字母写出「买 x 支 3 元的笔和 1 个 5 元的本」的总价，"
                    "再算 x=6 时的值。",
                    goal="式子连接生活。",
                ),
            ],
            reflection_questions=[
                "字母表示数，和方程里的「未知数」是一回事吗？",
                "为什么只有同类项才能合并？",
                "把数代入式子，算出来的是什么？",
            ],
        ),
        _point(
            topic_id="like_terms",
            name="合并同类项",
            grade_band=GradeBand.JUNIOR,
            grade="七年级上册",
            chapter="第二章 整式的加减",
            section="整式的加减",
            human="同类项是同一种字母部分的数量，可以像同类物品一样合并。",
            why="解方程、化简函数表达式和因式分解前都要会合并。",
            terms={"项": "式子里被加减号分开的块。", "系数": "字母前面乘着的数。"},
            prerequisites=["algebraic_expression", "distributive_property"],
            next_topics=["linear_equation_one_variable"],
            examples=["3个苹果加2个苹果是5个苹果，3x+2x=5x"],
            route=["项", "字母部分相同", "系数相加", "字母部分不变"],
            visuals=["物品分类", "颜色标注式子"],
            conceptual_layers=[
                "「项」是式子里被加减号隔开的块：3x²+5x−2 有三项，负号跟着自己的项走。",
                "同类项 = 字母部分完全相同（字母和指数都一样）："
                "3x² 和 5x² 同类；3x² 和 3x 不同类——x² 和 x 是两种东西。",
                "合并的道理是分配律反着用：3x+5x=(3+5)x。"
                "系数相加、字母部分照抄，数的是「几个 x」。",
            ],
            worked_examples=[
                WorkedExample(
                    title="整理式子像整理书包",
                    problem="化简 4x+3y−x+2y。",
                    steps=[
                        "先认项：4x、3y、−x、2y（负号属于 −x 这一项）。",
                        "分类：x 家族有 4x 和 −x；y 家族有 3y 和 2y。",
                        "各自合并：4x−x=3x；3y+2y=5y。",
                        "结果是 3x+5y。x 和 y 不同类，到此为止——不能再并成 8xy。",
                    ],
                    answer_check="代 x=2、y=1 检验：原式=8+3−2+2=11，3x+5y=11 对上；"
                    "而 8xy=16——乱并立刻露馅。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="圈出 5a²+3a−2a²+a 里的同类项，说说凭什么算同类。",
                    goal="同类认得准。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="化简 7m−3n+2m+n。",
                    goal="系数相加，字母不动。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="x²+x 为什么不能合并成 x³？代 x=2 验证你的说法。",
                    goal="用代入法给自己纠错。",
                ),
            ],
            reflection_questions=[
                "判断同类项，看系数还是看字母部分？",
                "合并同类项和分配律是什么关系？",
                "怀疑自己并错了，最快的检查办法是什么？",
            ],
        ),
        _point(
            topic_id="geometric_figures_intro",
            name="几何图形初步",
            grade_band=GradeBand.JUNIOR,
            grade="七年级上册",
            chapter="第四章 几何图形初步",
            section="立体图形、平面图形、线段和角",
            human="几何图形是把现实物体抽象成点、线、面和体来研究。",
            why="后续平行线、三角形、圆和证明都建立在这些基本语言上。",
            terms={"点": "只表示位置。", "线": "表示延伸方向。", "面": "表示平铺的范围。"},
            prerequisites=["line_angle_basic", "volume"],
            next_topics=["parallel_lines", "triangle_basic", "circle"],
            examples=["把纸盒看成长方体", "把道路看成线段"],
            route=["现实物体", "抽象形状", "点线面体", "位置关系", "度量"],
            visuals=["实物模型", "展开图"],
            conceptual_layers=[
                "几何图形是从实物里「抽」出来的：只留形状、大小、位置，"
                "不管颜色材质——魔方抽成正方体，车轮抽成圆。",
                "点线面体是一家：点动成线，线动成面，面动成体。笔尖划过是线，雨刷扫过是面。",
                "几何有自己的说话规矩：点用大写字母，线段用两个端点表示。"
                "先约定好记号，后面的推理才不吵架。",
            ],
            worked_examples=[
                WorkedExample(
                    title="车轮为什么是圆的",
                    problem="从「车轮是圆的」这件事里，几何在关心什么？",
                    steps=[
                        "先抽象：不管橡胶花纹和颜色，把车轮看成一个圆。",
                        "圆的本事：圆上每一点到圆心的距离都相等（这段距离叫半径）。",
                        "所以轮轴装在圆心，车身高度始终等于半径，走起来不颠。"
                        "换成方轮子，高度忽高忽低，一路颠簸。",
                    ],
                    answer_check="再举一个「实物→图形→性质→用途」的例子，比如井盖为什么是圆的。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="找五件实物，说出各自可以抽象成什么立体图形。",
                    goal="会做「实物→图形」的抽象。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="给「点动成线、线动成面、面动成体」各举一个生活例子。",
                    goal="维度升高有画面。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="数一数长方体有几个面、几条棱、几个顶点，算算 面+顶点−棱 等于几。",
                    goal="学会数图形的组成要素。",
                ),
            ],
            reflection_questions=[
                "把实物抽象成图形时，丢掉了什么、留下了什么？",
                "「点动成线」，那线有粗细吗？",
                "为什么几何要规定统一的记号和说法？",
            ],
        ),
        _point(
            topic_id="parallel_lines",
            name="相交线与平行线",
            grade_band=GradeBand.JUNIOR,
            grade="七年级下册",
            chapter="第五章 相交线与平行线",
            section="平行线的判定与性质",
            human="平行线是在同一平面内一直不相交的两条直线。",
            why="几何证明从平行线的角关系开始训练理由链。",
            terms={
                "同位角": "两条线被第三条线截出时位置相同的角。",
                "判定": "用条件说明它为什么成立。",
            },
            prerequisites=["line_angle_basic", "geometric_figures_intro"],
            next_topics=["triangle_basic", "congruent_triangles"],
            examples=["铁轨的两条边", "格纸上的平行线"],
            route=["相交", "角关系", "平行", "判定", "性质", "简单证明"],
            visuals=["截线图", "折纸"],
            conceptual_layers=[
                "同一平面里两条直线只有两种命运：相交（有且只有一个交点）或平行（永不相交）。",
                "相交出四个角：对顶角相等不用量——因为它们都和同一个角拼成 180°。",
                "判断平行不用追到无穷远：画第三条线截它们，"
                "同位角相等（或内错角相等）就能断定平行。",
            ],
            worked_examples=[
                WorkedExample(
                    title="对顶角为什么一定相等",
                    problem="两条直线相交，∠1=50°，它对面的 ∠3 是多少度？",
                    steps=[
                        "∠1 和旁边的 ∠2 拼成一条直线：∠2=180°−50°=130°。",
                        "∠2 和 ∠3 也拼成一条直线：∠3=180°−130°=50°。",
                        "所以 ∠3=∠1。对顶角相等不是巧合，"
                        "是「都和同一个角互补」一步步推出来的。",
                    ],
                    answer_check="把 ∠1 换成 70° 再推一遍，看看结论是否照样成立。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="画两条相交直线，量出四个角，验证对顶角相等。",
                    goal="先动手量，再讲道理。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="画两条平行线和一条截线，标出一组同位角和一组内错角。",
                    goal="三线八角认得清。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="铁轨、斑马线、作业本的横线，哪些在用平行？平行给它们带来什么好处？",
                    goal="体会平行的实际功能。",
                ),
            ],
            reflection_questions=[
                "对顶角相等，为什么可以不用量角器就确定？",
                "「永不相交」没法验证到无穷远，数学用什么办法判定平行？",
                "垂直是相交的特例，还是平行的特例？",
            ],
        ),
        _point(
            topic_id="coordinate_plane",
            name="平面直角坐标系",
            grade_band=GradeBand.JUNIOR,
            grade="七年级下册",
            chapter="第七章 平面直角坐标系",
            section="有序数对与坐标",
            human="坐标系用两个数确定平面上一个点的位置。",
            why="函数图像、几何变换和数据图都需要坐标语言。",
            terms={
                "横坐标": "表示左右位置的数。",
                "纵坐标": "表示上下位置的数。",
                "有序数对": "顺序不能换的一对数。",
            },
            prerequisites=["negative_number_intro", "rational_numbers"],
            next_topics=["function_intro", "linear_function", "quadratic_function"],
            examples=["座位第3列第5排", "地图定位"],
            route=["一条数轴定位", "两条数轴", "横纵方向", "有序数对", "点的位置"],
            visuals=["坐标纸", "地图网格"],
            conceptual_layers=[
                "坐标系解决一个日常问题：「在哪」怎么说才准？"
                "电影院用「几排几座」，棋盘用「第几行第几列」——都是用两个数定一个位置。",
                "把两条数轴垂直摆放、交在 0 点，平面上每个点就有了专属的一对数 (x, y)："
                "先横后纵，顺序不能换。",
                "(2,3) 和 (3,2) 是两个不同的点——就像 2 排 3 座和 3 排 2 座不是同一个座位。"
                "「有序」是坐标的命根子。",
            ],
            worked_examples=[
                WorkedExample(
                    title="向东 3 步再向北 2 步的宝藏",
                    problem="从原点出发，向东走 3 步、再向北走 2 步，宝藏埋在哪个点？",
                    steps=[
                        "向东是 x 轴正方向：横坐标是 3。",
                        "向北是 y 轴正方向：纵坐标是 2。",
                        "宝藏在点 (3,2)。要是写反成 (2,3)，"
                        "挖到的就是别人家的坑——顺序本身就是信息。",
                    ],
                    answer_check="把 (3,2) 和 (2,3) 都描在方格纸上，看看它们差多远。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="用「几排几座」的经验解释：为什么定一个平面位置需要两个数？",
                    goal="坐标从生活经验里长出来。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="在方格纸上描出 (2,3)、(−1,2)、(0,−2)，说说负号让你往哪边走。",
                    goal="四个象限都走得开。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="约定你的课桌是原点，写出前后左右四位同学的坐标。",
                    goal="体会原点是自选的约定。",
                ),
            ],
            reflection_questions=[
                "为什么一个数不够确定平面上的位置？",
                "(2,3) 和 (3,2) 差在哪里？",
                "换一个原点，同一个座位的坐标会怎么变？",
            ],
        ),
        _point(
            topic_id="real_numbers",
            name="实数",
            grade_band=GradeBand.JUNIOR,
            grade="七年级下册",
            chapter="第六章 实数",
            section="平方根、立方根和实数",
            human="实数把有理数和像根号2这样不能写成分数的数放在一起。",
            why="几何长度、坐标、函数和二次根式都需要实数范围。",
            terms={"平方根": "平方后得到原数的数。", "无理数": "不能写成两个整数之比的数。"},
            prerequisites=["rational_numbers", "power_scientific_notation"],
            next_topics=["quadratic_radicals", "pythagorean_theorem"],
            formulas=["sqrt(a)"],
            examples=["边长为1的正方形对角线是根号2"],
            route=["有理数", "开方", "数轴上的新点", "无理数", "实数"],
            visuals=["数轴", "正方形对角线"],
            conceptual_layers=[
                "有理数以为自己填满了数轴，直到 √2 出现：面积为 2 的正方形，"
                "边长写不成任何分数。",
                "√2=1.41421356…，小数点后不循环也不到头——这类数叫无理数。"
                "「无理」是「不是两个整数的比」，不是不讲道理。",
                "有理数加上无理数，合称实数。这回数轴才真被填满：每个点配一个数，每个数占一个点。",
            ],
            worked_examples=[
                WorkedExample(
                    title="√2 为什么不是分数",
                    problem="两个边长 1 的正方形沿对角线剪开，能拼成一个面积为 2 的大正方形。"
                    "它的边长是多少？",
                    steps=[
                        "边长自乘等于面积 2，这个数记作 √2（平方等于 2 的非负数）。",
                        "试着夹它：1.4²=1.96 偏小，1.5²=2.25 偏大——√2 在 1.4 和 1.5 之间。",
                        "再试 1.41、1.414……永远夹不中一个平方恰好是 2 的分数。"
                        "数学家证明了：这样的分数根本不存在。",
                        "所以 √2 是新品种：无限不循环小数，起名叫无理数。",
                    ],
                    answer_check="用同样的夹法，说出 √3 在哪两个一位小数之间。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="√4、√9 是无理数吗？先算出来再回答。",
                    goal="不是带根号的都无理。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="不用计算器，说出 √10 在哪两个整数之间，并给出理由。",
                    goal="会用夹逼法估值。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="π 也是无理数：它和 √2 的「无理」说的是同一件事吗？",
                    goal="无理数不止根号一族。",
                ),
            ],
            reflection_questions=[
                "「无理数」的「无理」到底指什么？",
                "有理数没填满数轴，缺的是哪些点？",
                "√2 ≈ 1.414 里的「≈」丢掉了什么？",
            ],
        ),
        _point(
            topic_id="linear_equation_systems",
            name="二元一次方程组",
            grade_band=GradeBand.JUNIOR,
            grade="七年级下册",
            chapter="第八章 二元一次方程组",
            section="消元法与实际问题",
            human="方程组是几个条件同时成立，解是同时满足它们的未知数取值。",
            why="它是从单个条件走向多条件建模的关键。",
            terms={"消元": "想办法先去掉一个未知数。", "公共解": "同时让所有方程成立的解。"},
            prerequisites=["linear_equation_two_variables", "linear_equation_one_variable"],
            next_topics=["linear_function"],
            formulas=["ax + by = c"],
            examples=["鸡兔同笼", "两种票价求人数"],
            route=["两个未知数", "两个条件", "同时成立", "消元", "检验"],
            visuals=["两条直线交点", "表格"],
            conceptual_layers=[
                "二元一次方程组是「两个未知数、两个条件」，"
                "解是同时让两个方程都成立的那一对数。",
                "主意是「消元」——想办法先干掉一个未知数，"
                "把两元问题变成会解的一元方程。",
                "一个二元方程有无数组解，两个方程一起才把解框成一对；"
                "这一对数，几何上就是两条直线的交点。",
            ],
            worked_examples=[
                WorkedExample(
                    title="鸡兔同笼",
                    problem="鸡兔共 8 只，脚共 22 只，各几只？（设鸡 x、兔 y）",
                    steps=[
                        "两个条件列两个方程：头数 x+y=8，脚数 2x+4y=22。",
                        "消元：由 x+y=8 得 x=8−y，代入第二式 2(8−y)+4y=22。",
                        "16+2y=22，y=3；回代 x=5。检验：5+3=8、10+12=22，都对。",
                    ],
                    answer_check="若脚数改成 26，方程组哪里变、鸡兔各几只？",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="说说为什么只知道「鸡兔共 8 只」还定不下各几只。",
                    goal="一个条件不够，要两个。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="解方程组 x+y=5，x−y=1。",
                    goal="会用消元求一对解。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="两种票 10 元和 15 元，共 6 张花 70 元，各几张？列方程组。",
                    goal="把实际问题写成方程组。",
                ),
            ],
            reflection_questions=[
                "为什么两个未知数需要两个条件才能定下来？",
                "「消元」的核心思路是把难题变成什么？",
                "方程组的解，和两条直线的交点是什么关系？",
            ],
        ),
        _point(
            topic_id="inequalities",
            name="一元一次不等式",
            grade_band=GradeBand.JUNIOR,
            grade="七年级下册",
            chapter="第九章 不等式与不等式组",
            section="不等式的性质与解集",
            human="不等式不是找一个答案，而是找一片能满足条件的数。",
            why="现实限制条件、取值范围和函数定义域都需要不等式。",
            terms={"解集": "所有能让不等式成立的数。", "不等号": "表示大于、小于等关系的符号。"},
            prerequisites=["absolute_value", "transposition"],
            next_topics=["inequality_systems"],
            formulas=["ax + b > c"],
            examples=["预算不超过100元", "身高大于某个标准"],
            route=["不相等关系", "等式性质类比", "变形", "解集", "数轴表示"],
            visuals=["数轴射线", "范围条"],
            conceptual_layers=[
                "不等式不是求一个准确答案，是求「一片数」——"
                "所有能让条件成立的数，合起来叫解集。",
                "解不等式和解方程几乎一样，就一条要小心："
                "两边同乘或同除一个负数，不等号要翻向。",
                "方程的解是几个点，不等式的解是数轴上一段射线；"
                "「不超过」含等号（≤），「小于」不含（<）。",
            ],
            worked_examples=[
                WorkedExample(
                    title="乘负数为什么要变号",
                    problem="解 2x < 6，再解 −2x < 6，比比不等号方向。",
                    steps=[
                        "2x<6：两边同除以正数 2，不等号不变，得 x<3。",
                        "−2x<6：两边同除以 −2（负数），不等号翻向，得 x>−3。",
                        "验一下 x=−2：−2×(−2)=4<6 成立，而 −2>−3，正好落在解集里。",
                    ],
                    answer_check="举一个满足 x<3 的数，再举一个不满足的，看看是否真分两边。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="在数轴上把 x<3 涂出来，说说为什么是一段而不是一个点。",
                    goal="解集是一片数。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="解 x+2>5，并在数轴上表示解集。",
                    goal="会像解方程一样变形。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="预算不超过 100 元，每本 8 元最多买几本？列不等式解。",
                    goal="把「不超过」写成 ≤。",
                ),
            ],
            reflection_questions=[
                "解不等式和解方程，最大的不同在哪一步？",
                "为什么两边乘负数时不等号要翻向？",
                "「不超过」和「小于」在数轴上差了哪个点？",
            ],
        ),
        _point(
            topic_id="inequality_systems",
            name="一元一次不等式组",
            grade_band=GradeBand.JUNIOR,
            grade="七年级下册",
            chapter="第九章 不等式与不等式组",
            section="不等式组",
            human="不等式组是多个范围条件同时满足，最后取它们重叠的部分。",
            why="多条件限制的应用题和函数取值范围都要用这种想法。",
            terms={"公共部分": "几个范围共同拥有的那一段。", "无解": "没有任何数能同时满足条件。"},
            prerequisites=["inequalities"],
            next_topics=["linear_function"],
            examples=["年龄至少12岁且不超过15岁", "价格在两个限制之间"],
            route=["一个范围", "多个范围", "画在同一数轴", "找重叠", "写解集"],
            visuals=["数轴重叠图"],
            conceptual_layers=[
                "不等式组是「几个范围要同时满足」，"
                "答案是它们在数轴上重叠的那一段。",
                "先分别解出每个不等式的范围，画在同一条数轴上，"
                "重叠的公共部分就是解集。",
                "若两个范围根本不重叠（比如既要 x>5 又要 x<2），"
                "就没有数能同时满足，叫无解。",
            ],
            worked_examples=[
                WorkedExample(
                    title="同时满足两个条件",
                    problem="解不等式组：x>1 且 x≤4。",
                    steps=[
                        "第一个范围 x>1：数轴上 1 的右边（不含 1）。",
                        "第二个范围 x≤4：数轴上 4 的左边（含 4）。",
                        "画在同一数轴，重叠的一段是 1<x≤4，这就是公共部分。",
                    ],
                    answer_check="若改成 x>1 且 x<0，会怎样？在数轴上说说为什么无解。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="把 x≥2 和 x≤5 画在一条数轴上，指出重叠的一段。",
                    goal="公共部分就是重叠区。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="解不等式组 x+1>3 且 x<6。",
                    goal="先各自解再取重叠。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="年龄至少 12 岁且不超过 15 岁，用不等式组写出来。",
                    goal="把两个限制翻译成组。",
                ),
            ],
            reflection_questions=[
                "不等式组的解，为什么取「重叠」而不是「合起来」？",
                "什么情况下不等式组会无解？",
                "「至少」和「不超过」分别对应哪个不等号？",
            ],
        ),
        _point(
            topic_id="data_collection_description",
            name="数据的收集、整理与描述",
            grade_band=GradeBand.JUNIOR,
            grade="七年级下册",
            chapter="第十章 数据的收集、整理与描述",
            section="全面调查、抽样调查和统计图",
            human="数据整理是在把零散信息变成能回答问题的证据。",
            why="统计不是画图作业，而是用数据判断现实问题。",
            terms={"样本": "从总体中选出的一部分。", "频数": "某类数据出现的次数。"},
            prerequisites=["data_collection_chart", "percent"],
            next_topics=["data_analysis", "probability"],
            examples=["调查睡眠时间", "统计出行方式"],
            route=["提出问题", "收集数据", "整理分类", "画图", "解释结论"],
            visuals=["频数表", "条形图", "扇形图"],
            conceptual_layers=[
                "统计的第一步不是算，是问清楚：想知道什么？问全体（普查）还是问一部分（抽样）？",
                "抽样的命门是「代表性」：只在篮球队里量身高，推不出全校平均——"
                "样本偏了，后面算得再好也白算。",
                "频数表是数据的中转站：把原始记录按类计数，再选图表达。"
                "数字 → 表 → 图，一步步变成能回答问题的证据。",
            ],
            worked_examples=[
                WorkedExample(
                    title="查全校近视率，必须每人都查吗",
                    problem="想知道全校 2000 人的近视率，怎么做省力又靠谱？",
                    steps=[
                        "普查最准但最贵：2000 人逐个查视力。",
                        "抽样：抽 100 人来查，用样本的近视率去估计全体。",
                        "关键在怎么抽：只抽六年级会偏高，只抽一年级会偏低；"
                        "各年级按比例随机抽，样本才像全校的缩影。",
                        "若抽出的 100 人里 38 人近视，就估计全校约 38%。",
                    ],
                    answer_check="说说「在网吧门口调查中学生平均上网时长」错在哪里。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="「查全班身高」和「查全国中学生身高」，哪个适合普查、哪个必须抽样？",
                    goal="两种收集方式选得对。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="把全班同学的鞋码记成频数表，再选一种合适的图画出来。",
                    goal="走完数据到图的全流程。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="电视投票说「90% 观众支持」，可信吗？想想是谁在投票。",
                    goal="识别自选样本的偏差。",
                ),
            ],
            reflection_questions=[
                "什么时候必须抽样，没法普查？",
                "样本越大越准吗？偏掉的样本再大有用吗？",
                "频数表丢掉了什么信息，留下了什么？",
            ],
        ),
        _point(
            topic_id="triangle_basic",
            name="三角形",
            grade_band=GradeBand.JUNIOR,
            grade="八年级上册",
            chapter="第十一章 三角形",
            section="边、角、多边形内角和",
            human="三角形是由三条线段围成的最基本多边形。",
            why="几何证明、全等、相似和三角函数都从三角形开始。",
            terms={"内角": "三角形里面的角。", "高": "从顶点到对边的垂线段。"},
            prerequisites=["parallel_lines", "line_angle_basic"],
            next_topics=["congruent_triangles", "similar_triangles", "trigonometric_ratios"],
            formulas=["三角形内角和 = 180°"],
            examples=["屋架结构", "路标形状"],
            route=["三条边围成", "边角关系", "内角和", "多边形", "证明"],
            visuals=["拼角实验", "折纸"],
            conceptual_layers=[
                "三条线段首尾相接就是三角形——但不是随便三条都行："
                "两边加起来必须比第三边长，不然接不拢。",
                "三角形是唯一「装上就不变形」的多边形：三边一定，形状就定死。"
                "这叫稳定性，晾衣架和铁塔都在用它。",
                "任何三角形的三个内角加起来都是 180°：把三个角撕下来拼一拼，正好拼成一条直线。",
            ],
            worked_examples=[
                WorkedExample(
                    title="3、4、9 能围成三角形吗",
                    problem="三根小棒长 3、4、9 厘米，能首尾相接围成三角形吗？",
                    steps=[
                        "围三角形需要两条短边合力够到第三边：3+4=7。",
                        "7 < 9：两根短的接起来都够不着长的那根，合不拢。",
                        "所以围不成。判定标准：任意两边之和大于第三边。",
                    ],
                    answer_check="换 3、4、5 试一遍（3+4>5，3+5>4，4+5>3），这组就能围成。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="撕下纸三角形的三个角，拼到一条直线上，看看内角和。",
                    goal="180° 是拼出来的，不是背出来的。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="三角形两个角分别是 50° 和 60°，第三个角是多少度？",
                    goal="内角和会用。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="自行车架、屋顶桁架为什么做成三角形，不做成四边形？",
                    goal="稳定性接到真实结构。",
                ),
            ],
            reflection_questions=[
                "为什么两边之和必须大于第三边？",
                "四边形装上会晃、三角形不会，差别在哪里？",
                "内角和 180° 和「平角是 180°」有什么联系？",
            ],
        ),
        _point(
            topic_id="congruent_triangles",
            name="全等三角形",
            grade_band=GradeBand.JUNIOR,
            grade="八年级上册",
            chapter="第十二章 全等三角形",
            section="全等三角形的判定",
            human="全等表示两个图形形状和大小都一样，可以完全重合。",
            why="它是初中几何证明中最重要的理由工具之一。",
            terms={"对应": "重合时互相配对的边或角。", "判定条件": "足够说明全等的一组信息。"},
            prerequisites=["triangle_basic"],
            next_topics=["axis_symmetry", "similar_triangles"],
            formulas=["SSS", "SAS", "ASA", "AAS", "HL"],
            examples=["证明两段长度相等", "判断两个零件是否一样"],
            route=["重合", "对应边角", "需要哪些条件", "判定", "推出结论"],
            visuals=["透明纸重叠", "边角标记图"],
            conceptual_layers=[
                "全等就是「完全重合」：形状大小都一样，平移、旋转、翻个面之后能严丝合缝盖住对方。",
                "重合时互相盖住的边和角叫「对应」：△ABC≌△DEF 的字母顺序就是配对表，"
                "A 对 D、B 对 E、C 对 F。",
                "不用把六个量全查一遍：三条边一定，三角形就定死了（稳定性）——"
                "这就是判定条件 SSS 的底气。",
            ],
            worked_examples=[
                WorkedExample(
                    title="碎玻璃带哪块去配",
                    problem="三角形玻璃摔成三块：一块只带一个完整角，一块只带一条完整边，"
                    "一块带着两个角和它们的夹边。带哪块能配出原样？",
                    steps=[
                        "配玻璃就是配一个全等三角形：大小形状都不许差。",
                        "只有一个角：同角的三角形千千万，定不下来。",
                        "只有一条边：同边的三角形也无穷多。",
                        "两角加夹边：两个角定住方向，夹边定住大小，"
                        "只能画出唯一一个三角形——这就是 ASA 判定。",
                    ],
                    answer_check="自己试：给定两角和夹边，看能不能画出第二个不重合的三角形。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="剪两个全等三角形，翻转叠合，指出三对对应边、三对对应角。",
                    goal="对应关系动手认。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="已知 △ABC≌△DEF，AB=5，∠A=40°，直接说出 DE 和 ∠D。",
                    goal="按字母顺序读对应。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="裁缝量几个尺寸就能做出合身衣服，这和全等判定像在哪里？",
                    goal="判定=用最少信息锁定全形。",
                ),
            ],
            reflection_questions=[
                "全等和「形状一样但大小可以不同」（相似）差在哪？",
                "为什么三条边能定死三角形，四条边定不死四边形？",
                "△ABC≌△DEF 的字母顺序在传递什么信息？",
            ],
        ),
        _point(
            topic_id="axis_symmetry",
            name="轴对称",
            grade_band=GradeBand.JUNIOR,
            grade="八年级上册",
            chapter="第十三章 轴对称",
            section="轴对称与等腰三角形",
            human="轴对称是沿一条线折过去，两边能完全重合。",
            why="它把图形直觉、全等证明和等腰三角形性质连起来。",
            terms={
                "对称轴": "折叠后两边重合的那条线。",
                "垂直平分线": "既垂直又平分一条线段的直线。",
            },
            prerequisites=["congruent_triangles"],
            next_topics=["rotation", "circle"],
            examples=["剪纸", "镜面对称"],
            route=["折叠", "重合", "对应点", "对称轴", "性质证明"],
            visuals=["折纸", "镜像图"],
            conceptual_layers=[
                "轴对称就是「沿一条线对折，两边严丝合缝地盖住」，"
                "那条折线叫对称轴。",
                "折过去重合，说明每一对对应点到对称轴距离相等、连线被它垂直平分——"
                "所以对称轴是对应点连线的垂直平分线。",
                "轴对称是「翻折」，图形被镜像了（左右手关系）；"
                "旋转是「转动」，两者都不改变大小和形状。",
            ],
            worked_examples=[
                WorkedExample(
                    title="对称点到轴一样远",
                    problem="点 A 在对称轴左边 3 厘米，它的对称点 A′ 在哪？",
                    steps=[
                        "轴对称要求折叠后 A 和 A′ 重合，说明它们离对称轴一样远。",
                        "A 在轴左边 3 厘米，A′ 就在轴右边 3 厘米，正对着 A。",
                        "连线 AA′ 被对称轴垂直平分：轴既把它分成两半，又和它垂直。",
                    ],
                    answer_check="若 A 到轴 3 厘米、A′ 到轴 5 厘米，还是轴对称吗？为什么。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="把一张纸对折剪个图案，展开后说说对称轴在哪。",
                    goal="折叠重合就是轴对称。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="给出点 A 和对称轴，画出它的对称点 A′。",
                    goal="会用「等距、垂直」定对称点。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="等腰三角形的对称轴在哪？它为什么把底边垂直平分？",
                    goal="用轴对称解释等腰三角形。",
                ),
            ],
            reflection_questions=[
                "对称轴为什么是对应点连线的垂直平分线？",
                "轴对称（翻折）和旋转有什么不同？",
                "一个图形可能有不止一条对称轴吗？举个例子。",
            ],
        ),
        _point(
            topic_id="polynomial_multiplication",
            name="整式的乘法",
            grade_band=GradeBand.JUNIOR,
            grade="八年级上册",
            chapter="第十四章 整式的乘法与因式分解",
            section="整式的乘法",
            human="整式乘法是把每一部分按分配律逐个相乘再合并。",
            why="因式分解、分式、二次方程和函数表达式都要用它。",
            terms={"幂": "乘方得到的式子。", "展开": "把乘积变成加减形式。"},
            prerequisites=[
                "algebraic_expression",
                "distributive_property",
                "power_scientific_notation",
            ],
            next_topics=["factorization", "quadratic_equation"],
            formulas=["(a + b)(c + d) = ac + ad + bc + bd"],
            examples=["长方形面积展开", "平方差公式"],
            route=["单项式乘法", "分配律", "多项式乘法", "公式", "合并"],
            visuals=["面积模型"],
            conceptual_layers=[
                "整式乘法没有新定律，全是分配律连着用：(a+b)(c+d) 就是让每一项和每一项都握一次手。",
                "面积模型最直观：长 (a+b)、宽 (c+d) 的大长方形切成四小块——"
                "ac、ad、bc、bd，一块不多一块不少。",
                "乘法公式如 (a+b)²=a²+2ab+b² 不是新知识，"
                "是「握手」的结果太常用，才起个名字方便复用。",
            ],
            worked_examples=[
                WorkedExample(
                    title="(x+2)(x+3) 的四次握手",
                    problem="展开 (x+2)(x+3)。",
                    steps=[
                        "画长 (x+3)、宽 (x+2) 的长方形，切成四块：x·x、x·3、2·x、2·3。",
                        "四块面积分别是 x²、3x、2x、6。",
                        "合并同类项：3x+2x=5x。所以 (x+2)(x+3)=x²+5x+6。",
                        "检验：代 x=1，左边 3×4=12，右边 1+5+6=12，对上了。",
                    ],
                    answer_check="代 x=2 再验一次；漏掉任何一次握手，数字立刻对不上。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="画面积图解释 (a+b)(c+d) 为什么恰好展开成四项。",
                    goal="每次握手在图上有一块。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="展开 (x+1)(x+4)，每一步说清是谁乘了谁。",
                    goal="不漏项、不错号。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="用面积图说明 (a+b)² 为什么不等于 a²+b²，中间的 2ab 是哪两块？",
                    goal="公式退回到图。",
                ),
            ],
            reflection_questions=[
                "整式乘法里用到的定律，哪一条是新的？",
                "(a+b)² 的 2ab 在面积图上是哪两块？",
                "展开之后为什么总要合并同类项？",
            ],
        ),
        _point(
            topic_id="factorization",
            name="因式分解",
            grade_band=GradeBand.JUNIOR,
            grade="八年级上册",
            chapter="第十四章 整式的乘法与因式分解",
            section="因式分解",
            human="因式分解是把一个加减式改写成几个因式相乘。",
            why="解方程、约分、函数零点都常靠把式子拆成乘积。",
            terms={"因式": "相乘中的每一块。", "公因式": "每一项都共同含有的因式。"},
            prerequisites=["polynomial_multiplication", "like_terms"],
            next_topics=["rational_expression", "quadratic_equation"],
            formulas=["a^2 - b^2 = (a + b)(a - b)"],
            examples=["把面积和拆成长宽乘积", "提取共同因数"],
            route=["乘法反过来", "找公因式", "公式结构", "乘回去检查"],
            visuals=["面积拼图", "式子颜色标记"],
            conceptual_layers=[
                "因式分解是整式乘法「反着走」——"
                "把一串加减的式子，改写成几个东西相乘。",
                "两条常用路子：提公因式（每项都有的那块拎出来），"
                "套公式（如 a²−b²=(a+b)(a−b) 是平方差）。",
                "结果一定是「乘积」，乘回去要等于原式；"
                "分解到每个因式都拆不动了才算到底。",
            ],
            worked_examples=[
                WorkedExample(
                    title="x²−9 怎么拆",
                    problem="把 x²−9 分解因式。",
                    steps=[
                        "先认结构：x² 是 x 的平方，9 是 3 的平方，中间减号——正是平方差。",
                        "套 a²−b²=(a+b)(a−b)，这里 a=x、b=3。",
                        "得 x²−9=(x+3)(x−3)。乘回去：x²−3x+3x−9=x²−9，对上。",
                    ],
                    answer_check="用 x=5 代入原式和结果，看看是不是都等于 16。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="说说 2a+2b 里每项都含哪个公因式，提出来是什么。",
                    goal="认出公因式。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="分解 x²−4，指出 a 和 b 各是谁。",
                    goal="会套平方差公式。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="分解 3x+3，再乘回去检查。",
                    goal="用提公因式并自检。",
                ),
            ],
            reflection_questions=[
                "因式分解和整式乘法，为什么说是「反过来」的一对？",
                "分解完怎么知道对不对？",
                "x²−9 能拆，x²+9 为什么（在实数里）拆不成平方差？",
            ],
        ),
        _point(
            topic_id="rational_expression",
            name="分式",
            grade_band=GradeBand.JUNIOR,
            grade="八年级上册",
            chapter="第十五章 分式",
            section="分式、分式运算和分式方程",
            human="分式像分数，只是分子或分母里可以有字母。",
            why="它让学生用代数方式表达比例、速度和反比例关系。",
            terms={"分式": "分母中含有字母的式子。", "最简分式": "不能再约分的分式。"},
            prerequisites=["fraction_operations", "factorization"],
            next_topics=["inverse_proportion_function"],
            formulas=["A/B, B != 0"],
            examples=["路程除以速度表示时间", "工作效率问题"],
            route=["分数", "字母进入分母", "分母不能为0", "约分", "方程"],
            visuals=["分数类比表", "关系表"],
            conceptual_layers=[
                "分式就是「分母里含字母的分数」，比如 1/x、(x+1)/(x−2)，"
                "规矩和分数几乎一样。",
                "一条铁律：分母不能等于 0（除以 0 没意义），"
                "所以要排除让分母为 0 的那些 x。约分靠因式分解把上下公因式消掉。",
                "分式和分数最大的不同是「分母带字母会变」：同一个分式，"
                "x 取不同值可能没意义，这在整数分数里不会发生。",
            ],
            worked_examples=[
                WorkedExample(
                    title="分式什么时候没意义",
                    problem="分式 (x+1)/(x−2)，x 取什么值时它没有意义？",
                    steps=[
                        "分式的分母不能为 0，否则除法说不通。",
                        "让分母为 0：x−2=0，即 x=2。",
                        "所以 x=2 时没意义，其余都行。比如 x=3 时值为 (3+1)/(3−2)=4。",
                    ],
                    answer_check="分式 5/(x+3) 在 x 取什么值时没意义？你看的是哪部分？",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="说说 1/x 和 1/3 有什么相同、有什么不同。",
                    goal="分式是「带字母的分数」。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="求 x/(x−1) 在 x 取什么值时没意义。",
                    goal="会找分母为 0 的值。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="约分 (2x)/(x²)（x≠0），说说消掉了什么公因式。",
                    goal="用因式分解约分。",
                ),
            ],
            reflection_questions=[
                "分式为什么必须提防分母为 0？",
                "分式和普通分数，最大的不同是什么？",
                "约分为什么不改变分式的值？",
            ],
        ),
        _point(
            topic_id="quadratic_radicals",
            name="二次根式",
            grade_band=GradeBand.JUNIOR,
            grade="八年级下册",
            chapter="第十六章 二次根式",
            section="二次根式的性质与运算",
            human="二次根式是在表示某个非负数的平方根。",
            why="勾股定理、距离公式和二次方程都离不开根式。",
            terms={"被开方数": "根号里面的数。", "最简二次根式": "已经化到最简单的根式。"},
            prerequisites=["real_numbers"],
            next_topics=["pythagorean_theorem", "quadratic_equation"],
            formulas=["sqrt(a), a >= 0"],
            examples=["正方形面积为2时边长是根号2"],
            route=["平方", "反过来开方", "非负", "化简", "运算"],
            visuals=["正方形面积", "数轴"],
            conceptual_layers=[
                "开方是平方的逆操作：知道正方形面积求边长，就是开方。√9=3，因为 3²=9。",
                "根号里的数（被开方数）不能是负数：没有哪个实数自乘会得负数，"
                "所以 √(−4) 在实数里无解。",
                "根式能化简：√8 里藏着一个完全平方 4，√8=√(4×2)=2√2。"
                "把能开出来的先开出来，就是化到最简。",
            ],
            worked_examples=[
                WorkedExample(
                    title="√8 为什么等于 2√2",
                    problem="化简 √8。",
                    steps=[
                        "把 8 拆出一个完全平方因子：8=4×2。",
                        "4 能开方开尽：√4=2，把它请到根号外面。",
                        "剩下开不尽的 2 留在根号里：√8=2√2。这就是「最简二次根式」——"
                        "根号里再没有能开出来的平方因子。",
                    ],
                    answer_check="反过来验证：(2√2)²=4×2=8，回到了被开方数。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="用「面积求边长」解释 √16 为什么等于 4。",
                    goal="开方=平方反过来。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="化简 √12 和 √50，各说出提出来的完全平方是谁。",
                    goal="会找完全平方因子。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="面积为 8 的正方形，边长是多少？化到最简再说它大约是几点几。",
                    goal="根式接回面积与估值。",
                ),
            ],
            reflection_questions=[
                "为什么根号里不能是负数？",
                "「最简」二次根式，简在什么地方？",
                "√9 是有理数，√2 是无理数，差别从哪来？",
            ],
        ),
        _point(
            topic_id="pythagorean_theorem",
            name="勾股定理",
            grade_band=GradeBand.JUNIOR,
            grade="八年级下册",
            chapter="第十七章 勾股定理",
            section="直角三角形三边关系",
            human="勾股定理说明直角三角形两条直角边的平方和等于斜边的平方。",
            why="它把图形长度和代数计算连起来，是坐标距离和三角函数的基础。",
            terms={"直角边": "夹成直角的两条边。", "斜边": "直角对面的那条边。"},
            prerequisites=["triangle_basic", "quadratic_radicals", "area"],
            next_topics=["trigonometric_ratios", "coordinate_plane"],
            formulas=["a^2 + b^2 = c^2"],
            examples=["求梯子长度", "判断三角形是否为直角三角形"],
            route=["直角三角形", "边上的正方形", "面积关系", "平方和", "求长度"],
            visuals=["正方形拼图", "网格距离"],
            conceptual_layers=[
                "勾股定理说：直角三角形里，两条直角边各自平方加起来，"
                "正好等于斜边的平方。",
                "「平方」不是空话，是边上正方形的面积——"
                "两个小正方形面积之和=大正方形面积，这就是 a²+b²=c²。",
                "只对直角三角形成立，斜边（对着直角的最长边）放在 c；"
                "反过来若 a²+b²=c²，这三角形就是直角三角形。",
            ],
            worked_examples=[
                WorkedExample(
                    title="直角边 3 和 4，斜边多长",
                    problem="直角三角形两条直角边是 3 和 4，斜边多长？",
                    steps=[
                        "斜边对着直角、是最长边，记作 c；两直角边 a=3、b=4。",
                        "勾股定理 a²+b²=c²，即 3²+4²=c²。",
                        "9+16=25，所以 c²=25，c=√25=5，斜边长 5。",
                    ],
                    answer_check="直角边 6、8，斜边多少？说说你怎么知道用哪条边当 c。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="在方格纸上画 3、4、5 的直角三角形，数格子验证 9+16=25。",
                    goal="平方就是边上正方形的面积。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="直角边 5 和 12，求斜边。",
                    goal="会用 a²+b²=c² 求斜边。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="梯子靠墙，底离墙 6 米、顶高 8 米，梯子多长？",
                    goal="把勾股定理用到实际长度。",
                ),
            ],
            reflection_questions=[
                "为什么 a²+b²=c² 里，c 一定是斜边？",
                "「平方和」和「边上正方形的面积」是怎么对上的？",
                "如果三边满足 a²+b²=c²，能反推它是直角三角形吗？",
            ],
        ),
        _point(
            topic_id="parallelogram",
            name="平行四边形",
            grade_band=GradeBand.JUNIOR,
            grade="八年级下册",
            chapter="第十八章 平行四边形",
            section="平行四边形、矩形、菱形和正方形",
            human="平行四边形是两组对边分别平行的四边形。",
            why="它承接平行线和全等证明，也为面积与向量直觉打底。",
            terms={"对边": "不相邻、相对的两条边。", "对角线": "连接不相邻两个顶点的线段。"},
            prerequisites=["parallel_lines", "congruent_triangles"],
            next_topics=["similar_triangles"],
            formulas=["平行四边形面积 = 底 x 高"],
            examples=["伸缩门", "瓷砖图案"],
            route=["四边形", "两组平行", "性质", "判定", "特殊平行四边形"],
            visuals=["格纸", "活动四边形模型"],
            conceptual_layers=[
                "平行四边形是「两组对边都平行」的四边形——像被推斜了的长方形。",
                "由「两组对边平行」能推出一串性质：对边相等、对角相等、"
                "对角线互相平分（用全等三角形证）。面积=底×高，不是底×斜边。",
                "长方形、菱形、正方形都是特殊的平行四边形；"
                "平行四边形不稳定（伸缩门能拉动），三角形才稳定。",
            ],
            worked_examples=[
                WorkedExample(
                    title="面积为什么用高不用斜边",
                    problem="平行四边形底 6、斜边 5、高 4，面积多少？为什么不是 6×5？",
                    steps=[
                        "沿高切一刀，右边三角形挪到左边，正好拼成一个长方形。",
                        "拼成的长方形长是底 6、宽是高 4，面积=底×高=6×4=24。",
                        "斜边 5 是倾斜的边，不是长方形的宽，用它会把面积算大。",
                    ],
                    answer_check="若高变成 3，面积变多少？说说为什么盯住高而不是斜边。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="推一推活动四边形模型，说说什么变了、对边平行变没变。",
                    goal="抓住「两组对边平行」这条根。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="平行四边形底 8、高 5，求面积。",
                    goal="会用底×高。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="为什么长方形是特殊的平行四边形？它特殊在哪？",
                    goal="认出特殊平行四边形。",
                ),
            ],
            reflection_questions=[
                "平行四边形面积为什么是底×高，不是底×斜边？",
                "从「两组对边平行」能推出哪些性质？",
                "平行四边形和三角形，谁稳定？伸缩门用的是哪个特点？",
            ],
        ),
        _point(
            topic_id="linear_function",
            name="一次函数",
            grade_band=GradeBand.JUNIOR,
            grade="八年级下册",
            chapter="第十九章 一次函数",
            section="函数、正比例函数和一次函数",
            human="一次函数描述一种稳定的线性变化：每多一点输入，输出按固定速度变。",
            why="它是学生第一次系统把表格、图像和表达式统一起来。",
            terms={"斜率": "图像倾斜程度，也表示变化速度。", "截距": "图像和坐标轴相交的位置。"},
            prerequisites=[
                "function_intro",
                "coordinate_plane",
                "proportion",
                "linear_equation_systems",
            ],
            next_topics=["quadratic_function", "inverse_proportion_function"],
            formulas=["y = kx + b"],
            examples=["打车费用", "水位匀速上升"],
            route=["两个变量", "表格", "坐标点", "直线", "表达式", "变化速度"],
            visuals=["表格", "坐标图像"],
            conceptual_layers=[
                "一次函数描述「匀速变化」：x 每增加 1，y 就固定地增加 k，"
                "画出来是一条直线。",
                "y=kx+b 里，k 是变化速度（斜率），b 是起点（x=0 时的 y，截距）。"
                "正比例 y=kx 是 b=0 的特例。",
                "「一次」指 x 最高一次方；斜率不变才是直线，"
                "若变化速度会变就不是一次函数了。",
            ],
            worked_examples=[
                WorkedExample(
                    title="打车费用",
                    problem="起步价 8 元，之后每千米 2 元。费用 y 和里程 x 的关系式？",
                    steps=[
                        "起步价是「还没走就要的」，对应 x=0 时的 y，就是截距 b=8。",
                        "每千米 2 元是变化速度，对应斜率 k=2。",
                        "关系式 y=2x+8。走 5 千米：y=2×5+8=18 元。",
                    ],
                    answer_check="若起步价涨到 10 元，式子哪个数变？走 5 千米变多少钱？",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="在 y=2x+8 里，说说 2 和 8 各代表打车的什么。",
                    goal="认出斜率和截距的实际意义。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="写出 y=3x−1 在 x=0、1、2 时的 y，说说 x 每加 1、y 加几。",
                    goal="体会「匀速变化」。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="水池已有 5 升，每分钟进 3 升，写出水量随时间的关系式。",
                    goal="把实际匀速变化写成一次函数。",
                ),
            ],
            reflection_questions=[
                "y=kx+b 里，k 和 b 分别控制直线的什么？",
                "正比例函数和一次函数是什么关系？",
                "为什么「变化速度固定」画出来就是直线？",
            ],
        ),
        _point(
            topic_id="data_analysis",
            name="数据的分析",
            grade_band=GradeBand.JUNIOR,
            grade="八年级下册",
            chapter="第二十章 数据的分析",
            section="平均数、中位数、众数和方差",
            human="数据分析是在用几个代表性指标看一组数据的水平和波动。",
            why="真实世界的数据不能只看一个数字，要知道代表性和稳定性。",
            terms={"中位数": "按大小排好后中间的数。", "方差": "描述数据离平均数有多分散。"},
            prerequisites=["average", "data_collection_description"],
            next_topics=["probability"],
            formulas=["平均数", "方差"],
            examples=["比较两组成绩是否稳定", "分析气温变化"],
            route=["一组数据", "整体水平", "中间位置", "最常出现", "波动大小"],
            visuals=["点图", "箱线直觉图"],
            conceptual_layers=[
                "数据分析是「用几个数概括一堆数」——"
                "既看整体在什么水平，也看它们波动大不大。",
                "看水平有三把尺子：平均数（匀开后每份）、中位数（排序后正中间）、"
                "众数（出现最多的）；看波动看方差，方差大说明数据分散、不稳定。",
                "平均数怕极端值（一个首富拉高「人均」），这时中位数更能代表大多数——"
                "选哪个指标要看数据长什么样。",
            ],
            worked_examples=[
                WorkedExample(
                    title="平均数被拉偏时",
                    problem="5 人月薪（千元）3、3、4、5、35，平均数和中位数各是多少，谁更代表？",
                    steps=[
                        "平均数=(3+3+4+5+35)÷5=50÷5=10 千元。",
                        "中位数：排序后正中间第 3 个，是 4 千元。",
                        "多数人只有三四千，平均数被 35 拉到 10，中位数 4 更贴近大多数人。",
                    ],
                    answer_check="去掉月薪 35 的那人，平均数变成多少？说说极端值的影响。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="给一组数 2、2、3、9，分别找出众数和中位数。",
                    goal="认得三种代表值。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="求 4、6、6、8、6 的平均数和众数。",
                    goal="会算水平指标。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="两组成绩平均分一样，但一组忽高忽低，用哪个指标看出差别？",
                    goal="用方差看稳定性。",
                ),
            ],
            reflection_questions=[
                "平均数、中位数、众数，为什么有时差很多？",
                "什么情况下中位数比平均数更能代表一组数据？",
                "两组数据平均数相同，还能靠什么区分它们？",
            ],
        ),
        _point(
            topic_id="quadratic_equation",
            name="一元二次方程",
            grade_band=GradeBand.JUNIOR,
            grade="九年级上册",
            chapter="第二十一章 一元二次方程",
            section="一元二次方程及其解法",
            human="一元二次方程是未知数最高次数为2的方程。",
            why="面积问题、抛物线、增长模型都会自然产生二次方程。",
            terms={"二次项": "含未知数平方的项。", "根": "让方程成立的未知数取值。"},
            prerequisites=["factorization", "quadratic_radicals", "power_scientific_notation"],
            next_topics=["quadratic_function"],
            formulas=["ax^2 + bx + c = 0"],
            examples=["已知矩形面积求边长", "抛物线与地面的交点"],
            route=["平方项", "标准形式", "因式分解", "配方", "公式", "检验"],
            visuals=["面积模型", "抛物线交点"],
            conceptual_layers=[
                "一元二次方程就是「未知数最高带平方」的方程，"
                "比如 x²+…=0，比一次方程升了一级。",
                "因为有平方，它常常有两个根。最直观的解法是因式分解："
                "写成两个东西相乘等于 0，则其中一个必为 0。",
                "二次项系数不能为 0（否则退回一次方程）；"
                "「两数相乘为 0，必有一个是 0」是分解法的命根子。",
            ],
            worked_examples=[
                WorkedExample(
                    title="面积求边长",
                    problem="一块矩形地长比宽多 2 米，面积 15 平方米，宽多少？",
                    steps=[
                        "设宽 x 米，长 (x+2) 米，面积 x(x+2)=15，整理成 x²+2x−15=0。",
                        "分解：找两数积 −15、和 +2，是 5 和 −3，得 (x+5)(x−3)=0。",
                        "必有一个因式为 0：x=−5 或 x=3。宽是长度不能为负，取 x=3 米。",
                    ],
                    answer_check="把 x=3 代回「宽×长=面积」验算，并说说 x=−5 为什么舍去。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="说说 (x−1)(x−4)=0 为什么能直接看出 x=1 或 x=4。",
                    goal="乘积为 0 必有因式为 0。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="解 x²−5x+6=0（提示：分解成两个一次因式）。",
                    goal="会用因式分解求根。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="一个数与它加 3 的积是 10，求这个数，列方程解。",
                    goal="把实际关系写成二次方程。",
                ),
            ],
            reflection_questions=[
                "一元二次方程为什么常有两个根，一次方程只有一个？",
                "「两数相乘等于 0」为什么能推出其中一个是 0？",
                "实际问题里，为什么有的根算出来要舍去？",
            ],
        ),
        _point(
            topic_id="quadratic_function",
            name="二次函数",
            grade_band=GradeBand.JUNIOR,
            grade="九年级上册",
            chapter="第二十二章 二次函数",
            section="二次函数的图象和性质",
            human="二次函数描述输出里含有输入平方的变化，图像通常是一条抛物线。",
            why="它把方程、图像、最值和现实建模合在一起。",
            terms={"抛物线": "二次函数常见的U形图像。", "顶点": "抛物线最高或最低的位置。"},
            prerequisites=["linear_function", "quadratic_equation", "coordinate_plane"],
            next_topics=[],
            formulas=["y = ax^2 + bx + c"],
            examples=["抛球高度变化", "围栏面积最大问题"],
            route=["平方变化", "列表", "画点", "抛物线", "顶点", "最值"],
            visuals=["坐标图像", "动态表格"],
            conceptual_layers=[
                "二次函数是「输出里带输入平方」的关系，比如 y=x²，"
                "画出来是一条对称的抛物线。",
                "因为有平方，变化速度不再固定：离顶点越远变得越快。"
                "抛物线有个顶点，a>0 开口朝上有最小值，a<0 开口朝下有最大值。",
                "和一次函数比，一次是直线（匀速），二次是曲线（变速）；"
                "顶点是研究最值的关键位置。",
            ],
            worked_examples=[
                WorkedExample(
                    title="y=x² 为什么是曲线",
                    problem="列表画 y=x² 在 x=−2、−1、0、1、2 的点，说说图像形状。",
                    steps=[
                        "算 y：x=−2→4，−1→1，0→0，1→1，2→4。",
                        "描点连线：两边高、中间 0，关于 y 轴左右对称，是 U 形抛物线。",
                        "顶点在 (0,0) 是最低点；x 每远离 0，y 增得越来越快，所以是曲线。",
                    ],
                    answer_check="把 y=x² 换成 y=−x²，开口朝哪、顶点是最高还是最低？",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="说说 y=x² 的图像为什么关于 y 轴对称。",
                    goal="平方让正负 x 得同一个 y。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="列表画出 y=x²−1 的几个点，指出顶点。",
                    goal="会描点看抛物线。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="一次函数和二次函数的图像，一个直一个弯，根子上差在哪个字？",
                    goal="抓住「平方」带来变速。",
                ),
            ],
            reflection_questions=[
                "二次函数的图像为什么是曲线，而一次函数是直线？",
                "开口朝上和朝下，由哪个数决定？",
                "顶点为什么是找最大或最小值的关键？",
            ],
        ),
        _point(
            topic_id="rotation",
            name="旋转",
            grade_band=GradeBand.JUNIOR,
            grade="九年级上册",
            chapter="第二十三章 旋转",
            section="图形旋转和中心对称",
            human="旋转是图形绕着一个点按固定角度转动。",
            why="它补齐初中图形变换，也帮助理解圆和对称。",
            terms={"旋转中心": "图形围绕转动的点。", "旋转角": "转过的角度。"},
            prerequisites=["axis_symmetry", "coordinate_plane"],
            next_topics=["circle"],
            examples=["风车转动", "钟表指针"],
            route=["固定点", "转动方向", "角度", "对应点", "中心对称"],
            visuals=["旋转纸片", "坐标变换图"],
            conceptual_layers=[
                "旋转是「绕着一个定点转一个角度」——像钟表指针绕轴心转，"
                "形状大小都不变，只是朝向变了。",
                "三要素定一次旋转：旋转中心（绕谁转）、旋转角（转多少度）、"
                "方向（顺时针还是逆时针）。每个点到中心的距离转前转后不变。",
                "转 180° 就是「中心对称」，是旋转的特例；"
                "轴对称是翻折（会镜像），旋转不镜像。",
            ],
            worked_examples=[
                WorkedExample(
                    title="钟表指针转过的角",
                    problem="分针从 12 走到 3，绕中心转了多少度，往哪个方向？",
                    steps=[
                        "旋转中心是钟表轴心，分针每一点都绕它转。",
                        "表面一圈 360°，均分 12 大格，每格 30°；从 12 到 3 是 3 格。",
                        "3×30°=90°，方向和指针走向一致，是顺时针。",
                    ],
                    answer_check="从 12 走到 6 转了多少度？这时和原来构成什么对称？",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="转一张三角形纸片，说说旋转前后哪里变了、哪里没变。",
                    goal="旋转不改变形状大小。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="一个点绕中心顺时针转 90°，说说它到中心的距离变不变。",
                    goal="抓住「到中心等距」。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="图形绕中心转 180° 后和原图的关系，叫什么对称？",
                    goal="认出中心对称是旋转特例。",
                ),
            ],
            reflection_questions=[
                "描述一次旋转，为什么必须说清中心、角度和方向三样？",
                "旋转和轴对称，哪个会把图形「镜像」？",
                "中心对称为什么是旋转的一种特殊情况？",
            ],
        ),
        _point(
            topic_id="circle",
            name="圆",
            grade_band=GradeBand.JUNIOR,
            grade="九年级上册",
            chapter="第二十四章 圆",
            section="圆的性质、位置关系和正多边形",
            human="圆是到同一个中心点距离都相等的点组成的图形。",
            why="圆把距离、角、对称和实际测量集中在一起。",
            terms={
                "圆心": "圆中间的固定点。",
                "半径": "圆心到圆上任意一点的线段。",
                "弦": "连接圆上两点的线段。",
            },
            prerequisites=["geometric_figures_intro", "rotation", "pythagorean_theorem"],
            next_topics=["trigonometric_ratios"],
            formulas=["C = 2πr", "S = πr^2"],
            examples=["车轮", "钟面"],
            route=["定点", "定长", "圆周", "圆心角", "位置关系", "计算"],
            visuals=["圆规作图", "旋转半径"],
            conceptual_layers=[
                "圆是「到圆心距离都相等的点」聚成的一圈线——"
                "那个相等的距离就是半径。",
                "圆可看成半径绕圆心旋转一周扫出来的；半径处处相等是一切性质的根。"
                "弦是圆上两点的连线，直径是过圆心的最长弦。",
                "半径 r、周长 C=2πr、面积 S=πr² 各管一件事："
                "r 是长度，C 是绕一圈的长，S 是圈里的面，别混用。",
            ],
            worked_examples=[
                WorkedExample(
                    title="半径 5 的圆，周长和面积",
                    problem="一个圆半径 5 厘米，周长和面积各是多少？（π 取 3.14）",
                    steps=[
                        "周长绕圆一圈：C=2πr=2×3.14×5=31.4 厘米。",
                        "面积是圈里的面：S=πr²=3.14×5²=3.14×25=78.5 平方厘米。",
                        "单位不同：周长是厘米，面积是平方厘米，因为面积用了 r²。",
                    ],
                    answer_check="半径变成 10，面积会变成原来的几倍？为什么不是 2 倍。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="用圆规画圆，说说圆规两脚的距离对应圆的什么。",
                    goal="定长就是半径。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="半径 3 的圆，求周长（π 取 3.14）。",
                    goal="会用 C=2πr。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="半径扩大到 2 倍，周长和面积各变几倍？",
                    goal="分清 C 随 r、S 随 r²。",
                ),
            ],
            reflection_questions=[
                "圆的一切性质，为什么都从「半径处处相等」来？",
                "半径加倍，为什么面积变 4 倍而周长只变 2 倍？",
                "弦最长能有多长？那时它叫什么？",
            ],
        ),
        _point(
            topic_id="probability",
            name="概率初步",
            grade_band=GradeBand.JUNIOR,
            grade="九年级上册",
            chapter="第二十五章 概率初步",
            section="随机事件、列举法和频率估计概率",
            human="概率是在描述一件事发生的可能性有多大。",
            why="它让学生用数量而不是感觉判断不确定事件。",
            terms={"随机事件": "可能发生也可能不发生的事件。", "样本空间": "所有可能结果的集合。"},
            prerequisites=["fraction", "percent", "data_collection_description"],
            next_topics=[],
            formulas=["概率 = 有利结果数 ÷ 所有等可能结果数"],
            examples=["掷骰子", "抽签"],
            route=["可能或不可能", "所有结果", "有利结果", "比例", "频率估计"],
            visuals=["树状图", "列表"],
            conceptual_layers=[
                "概率是用一个 0 到 1 之间的数，量「这件事有多可能发生」——"
                "0 是不可能，1 是一定。",
                "当每个结果都等可能时，概率=有利结果数÷所有结果数。"
                "掷骰子出 6，就是 1÷6。",
                "概率说的是「长期趋势」，不是「这一次一定」："
                "抛硬币正面概率 1/2，不代表两次里必有一次正面。",
            ],
            worked_examples=[
                WorkedExample(
                    title="掷骰子出偶数的概率",
                    problem="掷一个均匀骰子，出现偶数的概率是多少？",
                    steps=[
                        "所有等可能结果：1、2、3、4、5、6 共 6 种。",
                        "有利结果是偶数：2、4、6 共 3 种。",
                        "概率=有利÷全部=3÷6=1/2，也就是长期看约一半次数出偶数。",
                    ],
                    answer_check="出「大于 4」的概率是多少？说说有利结果是哪几个。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="说说「太阳从东边升起」和「掷骰子出 7」的概率分别接近几。",
                    goal="概率在 0 到 1 之间。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="掷一个骰子，求出现 3 的概率。",
                    goal="会用有利÷全部。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="袋里 2 红 3 白共 5 球，摸到红球的概率是多少？",
                    goal="把公式用到摸球。",
                ),
            ],
            reflection_questions=[
                "概率为什么总在 0 和 1 之间？",
                "「正面概率 1/2」是说两次必有一次正面吗？",
                "用公式算概率，前提是每个结果都「等可能」，这条为什么重要？",
            ],
        ),
        _point(
            topic_id="similar_triangles",
            name="相似三角形",
            grade_band=GradeBand.JUNIOR,
            grade="九年级下册",
            chapter="第二十七章 相似",
            section="相似三角形的判定和性质",
            human="相似表示形状一样、大小可以不同。",
            why="比例、缩放、测量和三角函数都建立在相似思想上。",
            terms={"相似比": "对应边长度的比。", "对应角": "形状匹配时相互对应的角。"},
            prerequisites=["ratio", "triangle_basic", "congruent_triangles"],
            next_topics=["trigonometric_ratios"],
            formulas=["对应边成比例，对应角相等"],
            examples=["地图和真实地形", "影子测高"],
            route=["放大缩小", "形状不变", "对应角", "对应边比", "判定"],
            visuals=["缩放图", "网格图"],
            conceptual_layers=[
                "相似就是「形状一样、大小可以不同」——"
                "像照片放大，长相没变，只是整体缩放了。",
                "相似三角形对应角相等、对应边成同一个比（相似比）。"
                "全等是相似比为 1 的特例（大小也一样）。",
                "光「看着像」不算，得对应角相等且对应边成比例；"
                "相似保「形状」，全等还保「大小」。",
            ],
            worked_examples=[
                WorkedExample(
                    title="影子测树高",
                    problem="1 米竹竿影长 2 米，同一时刻大树影长 10 米，树多高？",
                    steps=[
                        "同一时刻阳光方向一样，竹竿、大树和各自影子组成两个相似三角形。",
                        "相似比来自影子：2∶10，大三角形是小的 5 倍。",
                        "竿高∶树高 = 影长比：1∶树高 = 2∶10，所以树高=1×5=5 米。",
                    ],
                    answer_check="若影子变成 3 米、大树影长 12 米，树高怎么算？用的是哪对边？",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="把一个三角形每条边放大 2 倍，说说角变了没、形状变了没。",
                    goal="相似=形状不变的缩放。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="两个相似三角形相似比 1∶3，小的一边 4，对应大边多长？",
                    goal="会用对应边成比例。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="地图比例尺 1∶100000，图上三角地块和实地是什么关系？",
                    goal="把相似用到缩放测量。",
                ),
            ],
            reflection_questions=[
                "相似和全等，差别在「大小」还是「形状」？",
                "为什么「看着像」不能作为相似的判据？",
                "影子测高，靠的是相似的哪条性质？",
            ],
        ),
        _point(
            topic_id="trigonometric_ratios",
            name="锐角三角函数",
            grade_band=GradeBand.JUNIOR,
            grade="九年级下册",
            chapter="第二十八章 锐角三角函数",
            section="正弦、余弦、正切",
            human="锐角三角函数是在直角三角形里，用边长的比描述一个角。",
            why="它把角度和长度联系起来，可用于测高、测距和后续数学学习。",
            terms={
                "正弦": "对边和斜边的比。",
                "余弦": "邻边和斜边的比。",
                "正切": "对边和邻边的比。",
            },
            prerequisites=["similar_triangles", "pythagorean_theorem", "ratio"],
            next_topics=[],
            formulas=["sin A", "cos A", "tan A"],
            examples=["测楼高", "坡度"],
            route=["直角三角形", "固定锐角", "相似保证比不变", "三种边长比", "测量"],
            visuals=["直角三角形标边", "测高示意图"],
            conceptual_layers=[
                "锐角三角函数是「用边的比来代表一个角」——"
                "在直角三角形里，角定了，几条边的比也就定了。",
                "三种比对应三个名字：正弦=对边/斜边，余弦=邻边/斜边，"
                "正切=对边/邻边。同一个角无论三角形画多大，这些比都不变（靠相似）。",
                "只在直角三角形里、对锐角说；比值只跟角度有关、跟大小无关——"
                "这正是它能测高测距的原因。",
            ],
            worked_examples=[
                WorkedExample(
                    title="3-4-5 三角形里角 A 的三个比",
                    problem="直角三角形三边 3、4、5，求对着边 3 的锐角 A 的正弦、余弦、正切。",
                    steps=[
                        "5 是斜边（对着直角）。角 A 对着 3，所以对边=3、邻边=4。",
                        "sinA=对边/斜边=3/5=0.6；cosA=邻边/斜边=4/5=0.8。",
                        "tanA=对边/邻边=3/4=0.75。角越小对边越短，正弦越小。",
                    ],
                    answer_check="三边同时放大 2 倍成 6、8、10，sinA 会变吗？为什么。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="在直角三角形里，对着角 A 指出哪条是对边、邻边、斜边。",
                    goal="先认清三条边的身份。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="直角三角形对边 6、斜边 10，求 sinA。",
                    goal="会算对边/斜边。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="同一个角画大画小两个直角三角形，量边算 tanA，看看变不变。",
                    goal="用相似解释比值不变。",
                ),
            ],
            reflection_questions=[
                "同一个角，三角形画大画小，为什么三角函数的比不变？",
                "sin、cos、tan 三个比，各是哪两条边相除？",
                "三角函数为什么能用来「测量够不着的高度」？",
            ],
        ),
        _point(
            topic_id="inverse_proportion_function",
            name="反比例函数",
            grade_band=GradeBand.JUNIOR,
            grade="九年级下册",
            chapter="第二十六章 反比例函数",
            section="反比例函数的图象和性质",
            human="反比例函数描述两个量相乘保持不变时的变化关系。",
            why="它让比例从小学算术进入坐标图像和函数语言。",
            terms={"常数k": "乘积保持不变的那个数。", "双曲线": "反比例函数常见的两支曲线图像。"},
            prerequisites=[
                "proportion",
                "rational_expression",
                "coordinate_plane",
                "function_intro",
            ],
            next_topics=[],
            formulas=["y = k/x"],
            examples=["总路程一定时速度和时间", "面积一定时长和宽"],
            route=["乘积不变", "表格", "坐标点", "曲线", "实际限制"],
            visuals=["表格", "坐标图像"],
            conceptual_layers=[
                "反比例函数描述「乘积不变」的关系：一个量变大，另一个就按比例变小，"
                "乘起来始终等于同一个数 k。",
                "写成 y=k/x（即 xy=k）。x 越大 y 越小，但 x·y 恒等于 k；"
                "画出来是两支不碰坐标轴的曲线，叫双曲线。",
                "和正比例（y=kx，比值不变、直线）正相反："
                "这里是乘积不变、曲线。x 不能为 0（分母不为 0）。",
            ],
            worked_examples=[
                WorkedExample(
                    title="面积一定的长和宽",
                    problem="长方形面积固定 12，长 x 和宽 y 的关系式是什么？x=3 时 y 多少？",
                    steps=[
                        "面积=长×宽固定：x·y=12，这就是乘积不变，k=12。",
                        "写成函数：y=12/x。",
                        "x=3 时 y=12/3=4；x=6 时 y=2。长变大宽就变小，乘积始终 12。",
                    ],
                    answer_check="x=4 时 y 是多少？验证 x·y 是不是还等于 12。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="说说 y=6/x 里，x 变大时 y 怎么变，xy 等于几。",
                    goal="抓住乘积不变。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="列出 y=12/x 在 x=1、2、3、4 时的 y。",
                    goal="会用 y=k/x 求值。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="总路程 120 千米，速度 v 和时间 t 什么关系？写成函数。",
                    goal="把实际「乘积不变」写成反比例。",
                ),
            ],
            reflection_questions=[
                "反比例「乘积不变」、正比例「比值不变」，图像为什么一弯一直？",
                "反比例函数里 x 为什么不能等于 0？",
                "「速度越快时间越短」为什么是反比例而不是正比例？",
            ],
        ),
        _point(
            topic_id="number_comparison",
            name="数的大小比较",
            grade_band=GradeBand.PRIMARY,
            grade="一年级上册至二年级下册",
            chapter="数的认识",
            section="比较多少与大小",
            human="比较大小是在判断两个数量谁多、谁少，或者在数轴上谁更靠后。",
            why="后面估算、排序、分数小数比较和不等式都要先会比较。",
            terms={"大于": "比另一个数多。", "小于": "比另一个数少。"},
            prerequisites=["number_recognition"],
            next_topics=["place_value_decimal_system", "inequalities"],
            examples=["比较两盒彩笔谁多", "按身高排队"],
            route=["一一对应", "多少", "数轴位置", "大于小于符号"],
            visuals=["点子图", "数轴"],
            conceptual_layers=[
                "比大小就是看两堆东西谁多谁少；数轴上越往右的数越大。",
                "一一对应最可靠：两队一个对一个，谁还剩人谁就多。"
                "数字大不一定东西多，得数位对齐着比。",
                "「>」开口朝大数，「<」尖头指小数，符号只是把「谁多」写下来，"
                "不是新东西。",
            ],
            worked_examples=[
                WorkedExample(
                    title="32 和 28 谁大",
                    problem="32 和 28，哪个大？",
                    steps=[
                        "先比十位：3 个十比 2 个十多，32 已经赢了，个位不用再看。",
                        "想成数轴：32 在 28 的右边，右边的数大。",
                        "写成符号：32 > 28，开口对着大的那个 32。",
                    ],
                    answer_check="比 45 和 54，说说为什么位数一样时要先看十位。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="两盒彩笔，一盒 7 支一盒 9 支，一个对一个比比谁多。",
                    goal="用对应关系比多少。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="给 15、9、21 从小到大排队，再填上大于小于号。",
                    goal="会给多个数排序。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="先别算出得数，判断 20+5 和 30 谁大。",
                    goal="比大小不一定要先算准。",
                ),
            ],
            reflection_questions=[
                "数字看着大，东西就一定多吗？（比如 9 和 10）",
                "位数一样时，为什么要先比最高位？",
                "「>」和「<」怎么记住哪头对着大数？",
            ],
        ),
        _point(
            topic_id="rounding_estimation",
            name="估算与近似数",
            grade_band=GradeBand.PRIMARY,
            grade="二年级下册至四年级上册",
            chapter="万以内数的认识 / 大数的认识",
            section="近似数和估算",
            human="估算是先得到一个接近真实结果、方便判断的数。",
            why="学生做应用题和复杂计算时，需要先判断答案是否合理。",
            terms={
                "近似数": "接近准确值、方便使用的数。",
                "四舍五入": "按后一位决定保留位是否进一。",
            },
            prerequisites=["place_value_decimal_system", "number_comparison"],
            next_topics=["decimal_operations", "data_analysis"],
            examples=["估一下一箱书大约多重", "判断计算结果是不是离谱"],
            route=["准确数", "接近", "保留到某一位", "估算检验"],
            visuals=["数轴", "区间条"],
            conceptual_layers=[
                "近似数是「差不多的数」：不追求分毫不差，只要够用、好算、好判断。",
                "四舍五入看要舍掉的第一位：≥5 就往前进 1，<5 就直接舍去。"
                "它其实是在问「离哪个整十、整百更近」。",
                "估算是为了快判断合不合理，不是求精确答案；"
                "该精确时（付钱、吃药）不能用近似。",
            ],
            worked_examples=[
                WorkedExample(
                    title="387 约等于几百",
                    problem="把 387 保留到百位，是多少？",
                    steps=[
                        "保留到百位，就看它离 300 近还是离 400 近。",
                        "看十位上的 8：过了半路 350，更靠近 400。",
                        "四舍五入进 1：387≈400。",
                    ],
                    answer_check="把 342 保留到百位，说说这次为什么是 300 而不是 400。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="在数轴上标出 387，看看它离 300 近还是离 400 近。",
                    goal="近似就是离哪个整数更近。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="把 63、48 分别保留到十位。",
                    goal="会用四舍五入。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="一本书 19 元，买 21 本，估一下大约带多少钱够。",
                    goal="用估算判断够不够。",
                ),
            ],
            reflection_questions=[
                "为什么正好一半的时候（5）要往上进？",
                "估算和精确计算，各在什么时候用？",
                "近似数比准确数「少了」什么，又「方便」在哪？",
            ],
        ),
        _point(
            topic_id="multiplication_table",
            name="乘法口诀",
            grade_band=GradeBand.PRIMARY,
            grade="二年级上册至二年级下册",
            chapter="表内乘法",
            section="乘法口诀",
            human="乘法口诀是把常见的相同组数量结果记熟，方便快速计算。",
            why="多位数乘除、面积、比例和函数数值计算都会频繁用到。",
            terms={"口诀": "把常用结果压缩成容易记住的句子。"},
            prerequisites=["multiplication_meaning"],
            next_topics=["integer_multiplication_division", "area"],
            examples=["三四十二表示3组4一共12", "算4排每排6人"],
            route=["相同组", "重复加法", "阵列", "口诀", "快速计算"],
            visuals=["九九表", "阵列图"],
            conceptual_layers=[
                "乘法口诀是把「几个几相加」的结果提前背熟，"
                "用的时候一句话就报出得数。",
                "口诀不是新算法，是加法的速记："
                "「三四十二」= 3 个 4 或 4 个 3，都是 4+4+4=12。",
                "口诀只帮你记结果，为什么是这个结果还得靠「相同组相加」撑着——"
                "忘了能自己推回来。",
            ],
            worked_examples=[
                WorkedExample(
                    title="「四六二十四」从哪来",
                    problem="4 排小朋友，每排 6 人，一共几人？用口诀怎么算？",
                    steps=[
                        "「每排 6 人、4 排」就是 4 个 6 相加：6+6+6+6。",
                        "一个一个加：6、12、18、24，得 24。",
                        "这正是口诀「四六二十四」——背熟了就不必每次都加。",
                    ],
                    answer_check="说说「四六二十四」和「六四二十四」为什么是同一句。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="画 3 排每排 4 个的点子图，数出总数，对上「三四十二」。",
                    goal="口诀背后是阵列。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="不看口诀表，用连加推出「五六三十」。",
                    goal="忘了口诀能自己推。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="一盒鸡蛋 2 行每行 5 个，用口诀说一共几个。",
                    goal="把口诀用到真实分组。",
                ),
            ],
            reflection_questions=[
                "「三四十二」和「四三十二」为什么得数一样？",
                "如果忘了某句口诀，你能靠什么把它推回来？",
                "背口诀省下的是什么，省不掉的又是什么？",
            ],
        ),
        _point(
            topic_id="integer_multiplication_division",
            name="整数乘除法",
            grade_band=GradeBand.PRIMARY,
            grade="三年级上册至四年级上册",
            chapter="多位数乘一位数 / 除数是一位数的除法",
            section="笔算乘除法",
            human="整数乘除法是在更大的数里处理相同组和平均分。",
            why="面积、体积、比例、速度和代数计算都离不开整数乘除。",
            terms={
                "笔算": "按数位一步一步写下来的计算。",
                "余数": "平均分后剩下不够再分的一部分。",
            },
            prerequisites=[
                "place_value_decimal_system",
                "multiplication_table",
                "division_meaning",
            ],
            next_topics=["mixed_operations", "fraction_operations"],
            examples=["24盒彩笔每盒12支", "96本书平均分到8个班"],
            route=["相同组", "按位乘除", "进位退位", "验算"],
            visuals=["数位表", "分组图"],
            conceptual_layers=[
                "多位数乘除还是「几个几」和「平均分」，"
                "只是数大了，得按数位一位一位地算。",
                "笔算把大数拆成各个数位分别算再合起来："
                "12×24 是「12×20 加 12×4」，靠的是数位和口诀。",
                "乘法满十向前进位，除法不够分向后退位借数——"
                "方向相反，但都是数位在搬家。",
            ],
            worked_examples=[
                WorkedExample(
                    title="每盒 12 支，24 盒共几支",
                    problem="24 盒彩笔，每盒 12 支，一共多少支？",
                    steps=[
                        "把 24 拆成 20 和 4，先算 12×4=48。",
                        "再算 12×20=240（12×2=24，末尾添个 0）。",
                        "两部分合起来：240+48=288 支，这就是笔算「分位相乘再相加」。",
                    ],
                    answer_check="用「288÷24 是不是 12」验算，说说验算为什么能查错。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="用口诀说清 12×4 里每一步在算什么。",
                    goal="多位数乘法靠口诀拼出来。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="笔算 96÷8，说说每一位是怎么分的。",
                    goal="会按数位做除法。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="一箱 24 瓶，5 箱够不够给 100 人每人 1 瓶？",
                    goal="用乘法判断够不够。",
                ),
            ],
            reflection_questions=[
                "12×24 为什么可以拆成 12×20 加 12×4？",
                "乘法「进位」和除法「退位」，方向为什么相反？",
                "验算为什么能帮你发现算错了？",
            ],
        ),
        _point(
            topic_id="division_with_remainder",
            name="有余数的除法",
            grade_band=GradeBand.PRIMARY,
            grade="二年级下册至三年级上册",
            chapter="有余数的除法",
            section="余数的意义",
            human="有余数的除法是在平均分后，还剩下一些不够再分成一整组。",
            why="它帮助学生理解除法不是永远整除，也为分数和取整问题打底。",
            terms={"余数": "平均分后剩下的数量。", "整除": "没有剩下的除法情况。"},
            prerequisites=["division_meaning"],
            next_topics=["fraction", "integer_multiplication_division"],
            examples=["17颗糖每人分5颗，还剩2颗", "装箱后剩几件"],
            route=["平均分", "每组一样多", "剩下", "余数小于除数"],
            visuals=["实物分组", "线段图"],
            conceptual_layers=[
                "有余数的除法就是「平均分完还剩一点」，"
                "那剩下的、不够再凑一组的，叫余数。",
                "余数必须比除数小：只要剩下的还够分一组，就该继续分，"
                "说明还没分完。",
                "整除是「正好分光、余数为 0」，有余数是「剩一点」，"
                "都是同一个平均分动作。",
            ],
            worked_examples=[
                WorkedExample(
                    title="17 颗糖每人 5 颗",
                    problem="17 颗糖，每人分 5 颗，能分给几人，还剩几颗？",
                    steps=[
                        "每人 5 颗，一份一份地拿：分掉 5、10、15，正好给了 3 人。",
                        "还剩 17−15=2 颗，2 颗不够再凑成 5 颗一份，只能剩着。",
                        "写成 17÷5=3……2。余数 2 比除数 5 小，说明分到头了。",
                    ],
                    answer_check="如果算成「余 5」对不对？说说余数为什么不能等于除数。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="摆 13 根小棒，每 4 根一捆，能捆几捆、剩几根？",
                    goal="看见「剩下」就是余数。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="算 23÷6，写成「商……余数」，再检查余数够不够再分。",
                    goal="会判断余数合不合法。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="25 人坐船每船 6 人，至少几条船？想想剩下的人怎么办。",
                    goal="余数决定要不要多一组。",
                ),
            ],
            reflection_questions=[
                "余数为什么一定要比除数小？",
                "「余 0」和「有余数」有什么不一样？",
                "坐船问题里，剩下的 1 个人为什么还得多一条船？",
            ],
        ),
        _point(
            topic_id="unit_conversion",
            name="单位换算",
            grade_band=GradeBand.PRIMARY,
            grade="二年级上册至五年级下册",
            chapter="常见量 / 面积单位 / 体积单位",
            section="长度、质量、时间、面积和体积单位换算",
            human="单位换算是在用不同单位说同一个量。",
            why="不懂单位，应用题、面积体积和速度问题都会看错数量。",
            terms={
                "单位进率": "两个单位之间相差多少倍。",
                "同一个量": "东西没有变，只是说法变了。",
            },
            prerequisites=["measurement_units", "place_value_decimal_system"],
            next_topics=["area", "volume", "rate_speed_distance"],
            examples=["1米等于100厘米", "1平方米等于10000平方厘米"],
            route=["量什么", "单位", "进率", "乘或除", "检验大小"],
            visuals=["单位阶梯", "尺子"],
            conceptual_layers=[
                "单位换算是「东西没变，只是换个尺子说」："
                "1 米和 100 厘米量的是同一段长。",
                "换算靠进率：大单位换小单位数变多，要乘；"
                "小单位换大单位数变少，要除。",
                "长度进率是 100（米↔厘米），面积却是 10000——"
                "因为面积是长×宽，进率被乘了两次。",
            ],
            worked_examples=[
                WorkedExample(
                    title="1 平方米等于多少平方厘米",
                    problem="1 平方米是多少平方厘米？为什么不是 100？",
                    steps=[
                        "面积是长×宽：1 米×1 米就是 1 平方米。",
                        "换成厘米量：100 厘米×100 厘米。",
                        "100×100=10000，所以 1 平方米=10000 平方厘米，进率 100 用了两次。",
                    ],
                    answer_check="说说面积换算比长度换算多出来的那个 100 是从哪来的。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="拿尺子比一比，说说 1 米为什么等于 100 厘米。",
                    goal="换算是同一个量换说法。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="把 3 米换成厘米，把 500 厘米换成米。",
                    goal="会判断该乘还是该除。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="一块地 2 平方米，是多少平方厘米？",
                    goal="面积换算用平方进率。",
                ),
            ],
            reflection_questions=[
                "大单位换小单位，数字是变多还是变少？为什么？",
                "面积单位换算为什么进率是 10000，不是 100？",
                "换算前后，那个「量」本身变了吗？",
            ],
        ),
        _point(
            topic_id="rectangle_square_features",
            name="长方形和正方形",
            grade_band=GradeBand.PRIMARY,
            grade="三年级上册",
            chapter="长方形和正方形",
            section="边和角的特征",
            human="长方形和正方形用边长和直角描述规则的四边形。",
            why="它们是周长、面积、体积和坐标图像的基本形状。",
            terms={"对边": "相对的两条边。", "直角": "像课本角一样正正的角。"},
            prerequisites=["line_angle_basic"],
            next_topics=["perimeter", "area", "parallelogram"],
            examples=["课桌面", "方格纸中的小格"],
            route=["四条边", "四个角", "对边相等", "正方形是特殊长方形"],
            visuals=["方格纸", "折纸"],
            conceptual_layers=[
                "长方形是「四个角都是直角、对边一样长」的四边形；"
                "正方形再多一条：四条边都一样长。",
                "正方形是特殊的长方形——长方形该有的（四直角、对边相等）它都有，"
                "只是长和宽碰巧相等。",
                "判断靠「角」和「边」两条线索：光有直角不够，还得看对边等不等；"
                "四边全等才升级成正方形。",
            ],
            worked_examples=[
                WorkedExample(
                    title="正方形算不算长方形",
                    problem="有人说「正方形也是长方形」，对吗？",
                    steps=[
                        "长方形的要求：四个角都是直角、对边分别相等。",
                        "正方形四个角都是直角，四条边相等所以对边也相等，两条都满足。",
                        "该满足的都满足了，正方形就是「长宽相等的长方形」，是特殊的长方形。",
                    ],
                    answer_check="反过来「长方形都是正方形」对吗？举个例子说明。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="在方格纸上画一个长方形，量一量对边是不是相等。",
                    goal="亲手确认对边相等。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="给三个四边形，判断哪些是长方形、哪些是正方形。",
                    goal="用边和角两个线索判断。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="只知道「四个角都是直角」，能断定它是正方形吗？",
                    goal="分清长方形和正方形的界线。",
                ),
            ],
            reflection_questions=[
                "为什么正方形是特殊的长方形，反过来却不行？",
                "只看「四个直角」，能分出长方形和正方形吗？",
                "长方形的「对边相等」，在生活里哪儿见得到？",
            ],
        ),
        _point(
            topic_id="primary_circle_features",
            name="圆的初步认识",
            grade_band=GradeBand.PRIMARY,
            grade="六年级上册",
            chapter="圆",
            section="圆的认识、周长和面积",
            human="圆是到同一个中心点距离都一样远的一圈点。",
            why="初中圆、旋转、角度和几何证明都需要先有圆的直觉。",
            terms={"半径": "圆心到圆上一点的线段。", "直径": "经过圆心、两端在圆上的线段。"},
            prerequisites=["line_angle_basic", "measurement_units"],
            next_topics=["circle"],
            formulas=["C = 2πr", "S = πr^2"],
            examples=["车轮", "钟面"],
            route=["定点", "定长", "一圈点", "半径", "周长和面积"],
            visuals=["圆规作图", "绳子绕圆"],
            conceptual_layers=[
                "圆是「离中心一样远的一圈点」——用绳子拴住一头转一圈，"
                "笔尖画出的就是圆。",
                "半径是中心到圆上的距离，处处相等；直径穿过圆心、"
                "等于两条半径，所以直径=2×半径。",
                "圆没有边角，靠「定点+定长」定义；"
                "正因为半径处处相等，车轮才滚得稳。",
            ],
            worked_examples=[
                WorkedExample(
                    title="直径为什么是半径的 2 倍",
                    problem="一个圆半径 3 厘米，直径多少？",
                    steps=[
                        "半径是圆心到圆上一点的距离：3 厘米。",
                        "直径经过圆心、两端都在圆上，正好是「一条半径 + 对面一条半径」。",
                        "3+3=6 厘米，所以直径=2×半径=6 厘米。",
                    ],
                    answer_check="已知直径 10 厘米，半径多少？说说你用的是哪条关系。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="用绳子拴一支笔转一圈，说说画出来的为什么是圆。",
                    goal="体会「定点+定长」。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="量出一个圆的直径，除以 2 得到半径。",
                    goal="会用直径=2×半径。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="车轴装在圆心而不是边上，为什么车才不颠？",
                    goal="半径处处相等的用处。",
                ),
            ],
            reflection_questions=[
                "圆为什么没有「最长的边」或「角」？",
                "直径为什么一定是半径的 2 倍？",
                "如果半径不处处相等，滚起来会怎样？",
            ],
        ),
        _point(
            topic_id="equation_applications_primary",
            name="简易方程应用",
            grade_band=GradeBand.PRIMARY,
            grade="五年级上册",
            chapter="简易方程",
            section="列方程解决问题",
            human="列方程是把题目里的相等关系写成含未知数的等式。",
            why="初中的方程和函数建模都从这里开始。",
            terms={"未知量": "题目里还不知道、需要求的量。", "等量关系": "两边一样多的关系。"},
            prerequisites=["primary_equation", "quantity_relationship"],
            next_topics=["linear_equation_one_variable", "linear_equation_applications"],
            examples=["已知总价和单价求数量", "已知周长求边长"],
            route=["找未知量", "找相等关系", "列方程", "解方程", "检验"],
            visuals=["线段图", "天平模型"],
            conceptual_layers=[
                "列方程解应用题，就是把题里「谁和谁一样多」用带字母的等式写下来，"
                "再解出来。",
                "关键一步是找「等量关系」：题里哪两笔量其实相等；"
                "把未知的那个设成 x，等式就列出来了。",
                "算术是「倒着想」，列方程是「顺着题意写」："
                "未知数也能大大方方参加式子，不用先绕开它。",
            ],
            worked_examples=[
                WorkedExample(
                    title="买笔花了多少钱",
                    problem="每支笔 3 元，小明买笔花了 15 元，买了几支？",
                    steps=[
                        "找未知量：买的支数，设成 x 支。",
                        "找等量关系：单价×数量=总价，也就是 3×x=15。",
                        "解方程：两边同除以 3，x=5。检验：3×5=15，对上题目。",
                    ],
                    answer_check="把「花了 15 元」改成「18 元」，方程哪里变、答案怎么变？",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="说出「每支 3 元买 x 支花 15 元」里，相等的是哪两笔钱。",
                    goal="先抓等量关系。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="一个数加上 7 等于 20，设 x 列方程并解。",
                    goal="会把文字翻译成方程。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="正方形周长 20 厘米，设边长 x 列方程求边长。",
                    goal="把等量关系用到几何。",
                ),
            ],
            reflection_questions=[
                "列方程时，最难的一步是不是「找相等关系」？",
                "为什么设了未知数 x 之后，题目反而好写了？",
                "检验这一步能查出什么错？",
            ],
        ),
        _point(
            topic_id="rate_speed_distance",
            name="速度、时间和路程",
            grade_band=GradeBand.PRIMARY,
            grade="五年级上册至六年级下册",
            chapter="小数乘除法 / 比和比例",
            section="行程问题",
            human="速度是在说单位时间里走了多少路。",
            why="它是比例、一次函数和应用题建模的常见入口。",
            terms={"速度": "每一份时间走过的路程。", "单位时间": "被当作一份的时间。"},
            prerequisites=["decimal_operations", "quantity_relationship", "unit_conversion"],
            next_topics=["proportion", "linear_function"],
            formulas=["路程 = 速度 x 时间"],
            examples=["每小时60千米开3小时", "每分钟走80米"],
            route=["路程", "时间", "每份时间", "速度", "三量关系"],
            visuals=["线段图", "表格"],
            conceptual_layers=[
                "速度就是「每一份时间走多少路」——每小时 60 千米，"
                "就是每 1 小时走 60 千米。",
                "三个量拴在一条式子上：路程=速度×时间。"
                "知道两个就能求第三个，除法是乘法反过来。",
                "比速度要「单位一致」：60 千米/时和 80 米/分不能直接比，"
                "得先换成同一种单位。",
            ],
            worked_examples=[
                WorkedExample(
                    title="每小时 60 千米开 3 小时",
                    problem="汽车每小时行 60 千米，开 3 小时走多远？",
                    steps=[
                        "速度 60 千米/时，意思是每 1 小时走 60 千米。",
                        "3 小时就是 3 个 60 千米：路程=速度×时间=60×3。",
                        "60×3=180 千米。反过来 180÷60=3 求时间，180÷3=60 求速度。",
                    ],
                    answer_check="把「3 小时」换成「2.5 小时」，路程怎么算、是多少？",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="用一句话说清「每分钟走 80 米」里，80 是每多少时间走的路。",
                    goal="抓住「单位时间」的意思。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="每分钟 80 米，走 5 分钟多远？",
                    goal="会用路程=速度×时间。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="甲每小时 60 千米，乙每分钟 800 米，谁快？先统一单位。",
                    goal="比速度要先统一单位。",
                ),
            ],
            reflection_questions=[
                "知道路程和时间，怎么求速度？为什么用除法？",
                "两个速度单位不同，为什么不能直接比大小？",
                "「每小时 60 千米」这句话里，藏着哪三个量的关系？",
            ],
        ),
        _point(
            topic_id="scale_ratio_application",
            name="比例尺",
            grade_band=GradeBand.PRIMARY,
            grade="六年级下册",
            chapter="比例",
            section="比例尺",
            human="比例尺是在说图上距离和实际距离按同一个比缩小或放大。",
            why="它连接比、比例、相似图形和现实测量。",
            terms={"图上距离": "图里量到的距离。", "实际距离": "现实里的真实距离。"},
            prerequisites=["ratio", "proportion", "unit_conversion"],
            next_topics=["similar_triangles"],
            formulas=["比例尺 = 图上距离 : 实际距离"],
            examples=["地图上1厘米表示实际1千米", "按比例画教室平面图"],
            route=["两个距离", "同单位", "比", "放大缩小", "实际计算"],
            visuals=["地图", "双数轴"],
            conceptual_layers=[
                "比例尺是「图上量的和实际的，按同一个比缩小」——"
                "图上 1 厘米代表实际多远，先说清楚。",
                "比例尺=图上距离∶实际距离，是个固定的比；"
                "实际距离=图上距离÷比例尺，图上距离=实际距离×比例尺。",
                "算之前两个距离要换成同一单位；"
                "1∶100000 里 100000 越大，图缩得越狠、画得越小。",
            ],
            worked_examples=[
                WorkedExample(
                    title="地图上 3 厘米是实际多远",
                    problem="比例尺 1∶1000000 的地图上量得两地相距 3 厘米，实际多少千米？",
                    steps=[
                        "比例尺 1∶1000000：图上 1 厘米代表实际 1000000 厘米。",
                        "图上 3 厘米：实际=3×1000000=3000000 厘米。",
                        "换成千米：3000000 厘米=30 千米（1 千米=100000 厘米）。",
                    ],
                    answer_check="若实际 50 千米，图上该画几厘米？说说你把哪一步反过来用了。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="说说比例尺 1∶100 是把实际放大还是缩小，缩到几分之一。",
                    goal="读懂比例尺的含义。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="比例尺 1∶10000 的图上 2 厘米，是实际多少米？",
                    goal="图上距离×比例尺求实际。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="教室长 8 米，用 1∶100 画平面图，图上画几厘米？",
                    goal="实际距离反推图上距离。",
                ),
            ],
            reflection_questions=[
                "比例尺里的两个距离，为什么要先换成同一单位？",
                "1∶1000000 和 1∶100，哪个把地方缩得更小？",
                "比例尺和「比」是同一回事吗？",
            ],
        ),
        _point(
            topic_id="remove_parentheses",
            name="去括号",
            grade_band=GradeBand.JUNIOR,
            grade="七年级上册",
            chapter="第二章 整式的加减",
            section="去括号与添括号",
            human="去括号是在不改变式子意思的前提下，把括号里的项放出来。",
            why="合并同类项、解方程和整式乘法前经常要先处理括号。",
            terms={"符号": "项前面的加号或减号。", "添括号": "把几项重新合成一组。"},
            prerequisites=["algebraic_expression", "distributive_property"],
            next_topics=["like_terms", "linear_equation_one_variable"],
            examples=["3-(x+2)不能直接写成3-x+2", "把总价拆成几部分"],
            route=["括号是一组", "前面是加号", "前面是减号", "符号变化", "合并"],
            visuals=["颜色标注式子", "面积模型"],
            conceptual_layers=[
                "去括号是「把打包的一组数拆开」，但不能改变式子的值，"
                "所以要看括号前是加号还是减号。",
                "括号前是「−」，等于给整组乘 −1：里面每一项都要变号；"
                "括号前是「+」，直接照抄。",
                "最常错在减号：3−(x+2)≠3−x+2。"
                "减号管着括号里所有项，不是只管第一项。",
            ],
            worked_examples=[
                WorkedExample(
                    title="3−(x+2) 到底等于几",
                    problem="化简 3−(x+2)。",
                    steps=[
                        "括号前是减号，相当于减掉「x 和 2」一整组。",
                        "括号里每一项都变号：−(x+2)=−x−2。",
                        "合起来：3−x−2=1−x。（错写成 3−x+2 就把 +2 漏改了。）",
                    ],
                    answer_check="用 x=1 代入原式和你的结果，看看是不是都等于 0。",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="说说 5−(2+1) 为什么等于 2，而不是 5−2+1=4。",
                    goal="减号管着括号里全部。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="去括号化简 a−(b−c)。",
                    goal="会给每一项正确变号。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="化简 8−(x−3)，再代 x=5 验一下。",
                    goal="把去括号用到含字母的式子。",
                ),
            ],
            reflection_questions=[
                "括号前是减号时，为什么里面每一项都要变号？",
                "去括号前后，式子的值为什么必须不变？",
                "3−(x+2) 最容易错在哪一项？",
            ],
        ),
        _point(
            topic_id="linear_equation_applications",
            name="一元一次方程应用",
            grade_band=GradeBand.JUNIOR,
            grade="七年级上册",
            chapter="第三章 一元一次方程",
            section="实际问题与一元一次方程",
            human="方程应用是在把现实条件翻译成一个能求未知数的等式。",
            why="学生不会应用题时，常卡在找量和关系，而不是卡在计算。",
            terms={"设未知数": "先给不知道的量起一个字母名字。", "检验": "把答案放回原题检查。"},
            prerequisites=["linear_equation_one_variable", "quantity_relationship"],
            next_topics=["linear_equation_systems", "linear_function"],
            examples=["打折销售", "工程合作", "行程追及"],
            route=["读题", "找量", "设未知数", "列等式", "解和检验"],
            visuals=["表格", "线段图"],
            conceptual_layers=[
                "方程应用题的功夫全在「翻译」——把中文里的相等关系，"
                "改写成一个含未知数的等式。",
                "套路固定：设未知数 → 用它把各个量表示出来 → "
                "找到相等的两笔量 → 列等式 → 解并检验。",
                "卡住的多半不是计算，是没找对「设谁为 x」和「哪两笔量相等」，"
                "把关系理顺方程就出来了。",
            ],
            worked_examples=[
                WorkedExample(
                    title="打八折后的原价",
                    problem="一件衣服打八折后卖 120 元，原价多少？",
                    steps=[
                        "设原价为 x 元。八折就是原价的 80%，即 0.8x。",
                        "相等关系：打折价=120，也就是 0.8x=120。",
                        "解方程：x=120÷0.8=150 元。检验：150×0.8=120，对上。",
                    ],
                    answer_check="把「八折」改成「九折」，方程哪里变、原价变大还是变小？",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="说说「打八折卖 120 元」里，相等的是哪两笔钱。",
                    goal="先找等量关系。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="一个数的 3 倍再加 4 等于 25，设 x 列方程并解。",
                    goal="会把文字译成方程。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="相距 300 米同向走，甲每分 60 米追乙每分 40 米，几分钟追上？",
                    goal="把相等关系用到行程。",
                ),
            ],
            reflection_questions=[
                "应用题真正难的，是计算还是「找相等关系」？",
                "设未知数时，设谁为 x 会让式子更好列？",
                "解完为什么一定要代回原题检验？",
            ],
        ),
        _point(
            topic_id="geometric_proof_intro",
            name="几何证明入门",
            grade_band=GradeBand.JUNIOR,
            grade="七年级下册至八年级上册",
            chapter="相交线与平行线 / 三角形",
            section="证明理由链",
            human="证明是在把每一步为什么成立说清楚。",
            why="初中几何不是只看图猜结论，而是要用已知条件推出结论。",
            terms={"已知": "题目已经告诉你的条件。", "结论": "需要说明成立的结果。"},
            prerequisites=["parallel_lines", "triangle_basic"],
            next_topics=["congruent_triangles", "similar_triangles"],
            examples=["证明两个角相等", "证明两条线平行"],
            route=["看图", "找已知", "找要证", "每步有理由", "写成证明"],
            visuals=["理由链", "图形标注"],
            conceptual_layers=[
                "几何证明是「讲道理」——不是看图猜结论，"
                "而是从已知一步步、每步都有依据地推到结论。",
                "每一步都要配一个「理由」（定义、已知或学过的定理），"
                "像链条一样：由 A 推 B、由 B 推 C，环环扣紧。",
                "「看起来相等」不能当证据；图只是帮助思考，"
                "真正算数的是每步背后的理由。",
            ],
            worked_examples=[
                WorkedExample(
                    title="平行线下的内错角",
                    problem="已知 a∥b 被直线 c 所截，求证一对内错角 ∠1=∠2。",
                    steps=[
                        "找已知：a∥b（两条直线平行），c 是截线。",
                        "找依据：学过「两直线平行，内错角相等」这条性质。",
                        "由 a∥b，依据这条性质，直接得 ∠1=∠2，这就是一步带理由的证明。",
                    ],
                    answer_check="如果题目没说 a∥b，还能得到 ∠1=∠2 吗？理由为什么不能省？",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="给一句「因为…所以…」，指出哪部分是已知、哪部分是结论。",
                    goal="分清已知和结论。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="已知 a∥b，写出「内错角相等」这一步的理由。",
                    goal="每步都配一个依据。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="用「三角形内角和 180°」说明「知道两个角能求第三个角」，理由是什么？",
                    goal="把定理当理由用。",
                ),
            ],
            reflection_questions=[
                "为什么「图上看着相等」不能当证明的理由？",
                "证明里的每一步，都必须有什么？",
                "已知条件少一个，结论还成立吗？怎么判断？",
            ],
        ),
        _point(
            topic_id="function_graph_reading",
            name="函数图像读法",
            grade_band=GradeBand.JUNIOR,
            grade="八年级下册",
            chapter="第十九章 一次函数",
            section="函数图象",
            human="读函数图像是在从点、线和变化趋势里看两个量的关系。",
            why="不会读图，就很难理解一次函数、反比例函数和二次函数。",
            terms={"横轴": "通常表示输入量的方向。", "纵轴": "通常表示输出量的方向。"},
            prerequisites=["function_intro", "coordinate_plane"],
            next_topics=["linear_function", "quadratic_function"],
            examples=["看水位随时间变化", "看费用随里程变化"],
            route=["横轴纵轴", "点表示一组值", "线表示变化", "上升下降", "读实际意义"],
            visuals=["坐标图像", "变化故事"],
            conceptual_layers=[
                "读函数图像就是「把线翻译成故事」——横轴是输入、纵轴是输出，"
                "线的走势告诉你两个量怎么一起变。",
                "图上一个点=一组对应值（横坐标配纵坐标）；线往上走表示输出随输入增大，"
                "往下走表示减小，平的表示不变。",
                "别把图形的「陡」直接当数值大：陡表示变化快（斜率大），"
                "高才表示数值大——位置和坡度是两回事。",
            ],
            worked_examples=[
                WorkedExample(
                    title="读水位变化图",
                    problem="横轴时间、纵轴水位，图像先上升后水平，说明发生了什么？",
                    steps=[
                        "先看轴：横轴时间、纵轴水位，一个点表示「某时刻水位多少」。",
                        "上升段：时间往后水位变高，说明在进水。",
                        "水平段：时间在走水位却不变，说明停止进水、水位保持。",
                    ],
                    answer_check="若后面又出现下降段，代表水池发生了什么？",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="在图上找一个点，读出它的横坐标和纵坐标各代表什么。",
                    goal="一个点就是一组对应值。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="给一段上升的图像，说说输出随输入是变大还是变小。",
                    goal="从走势读增减。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="费用随里程的图，越走越陡说明什么？（提示：看变化快慢）",
                    goal="区分「高」和「陡」。",
                ),
            ],
            reflection_questions=[
                "图上一个点，包含了几个信息？",
                "线「往上走」和「很高」是一回事吗？",
                "为什么同一段变化，图越陡代表变得越快？",
            ],
        ),
        _point(
            topic_id="probability_tree_listing",
            name="列表法与树状图",
            grade_band=GradeBand.JUNIOR,
            grade="九年级上册",
            chapter="第二十五章 概率初步",
            section="列举所有可能结果",
            human="列表法和树状图是在把所有可能结果有顺序地列全。",
            why="概率题常错在漏数或重复数，不是只错在公式。",
            terms={"列举": "一个一个列出来。", "重复": "同一个结果被数了多次。"},
            prerequisites=["probability"],
            next_topics=[],
            examples=["抛两枚硬币", "从两个袋子各取一个球"],
            route=["一次选择", "第二次选择", "所有分支", "不漏不重", "算比例"],
            visuals=["树状图", "表格"],
            conceptual_layers=[
                "列表法和树状图是「把所有可能结果有顺序地列全」的工具——"
                "专治概率题里的漏数和重数。",
                "一步一步分支：第一次选什么、在此基础上第二次选什么，画成树或排成表，"
                "数清一共几种、有利几种，再算比例。",
                "关键是「有顺序、不漏不重」；两步的总数是两步选择数相乘"
                "（比如 2×2=4），不是相加。",
            ],
            worked_examples=[
                WorkedExample(
                    title="抛两枚硬币",
                    problem="抛两枚硬币，两枚都是正面的概率是多少？",
                    steps=[
                        "用树状图：第一枚正/反，每种下面第二枚再分正/反，共 2×2=4 种。",
                        "全部结果：正正、正反、反正、反反，一个不漏一个不重。",
                        "「两个都正」只有「正正」1 种，概率=1÷4=1/4。",
                    ],
                    answer_check="「一正一反」的概率是多少？为什么是 2/4 而不是 1/4？",
                ),
            ],
            practice_ladder=[
                PracticeTask(
                    level="看懂",
                    prompt="抛两枚硬币，把 4 种结果全列出来，检查有没有漏或重。",
                    goal="学会不漏不重地列举。",
                ),
                PracticeTask(
                    level="会做",
                    prompt="从 {红、蓝} 和 {甲、乙} 各取一个，用表列出所有搭配。",
                    goal="会用列表法列组合。",
                ),
                PracticeTask(
                    level="迁移",
                    prompt="掷两个骰子，一共多少种结果？（想想 6×6）",
                    goal="把「相乘」用到更多分支。",
                ),
            ],
            reflection_questions=[
                "为什么两步选择的总数是相乘，而不是相加？",
                "树状图和列表法，各在什么时候更顺手？",
                "概率题最容易错在「漏数」还是「算比例」？",
            ],
        ),
    ]
