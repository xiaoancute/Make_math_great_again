from __future__ import annotations

from math_learning_graph.curriculum_expand import load_expanded_knowledge_points
from math_learning_graph.curriculum_seed import load_curriculum_knowledge_points
from math_learning_graph.depth import with_deep_scaffold
from math_learning_graph.high_school_seed import load_high_school_knowledge_points
from math_learning_graph.models import (
    DomainOverview,
    GradeBand,
    KnowledgePoint,
    MathDomain,
    PracticeTask,
    RoadmapItem,
    TextbookPosition,
    WorkedExample,
)


def _worked(title: str, problem: str, steps: list[str], answer_check: str) -> WorkedExample:
    return WorkedExample(title=title, problem=problem, steps=steps, answer_check=answer_check)


def _task(level: str, prompt: str, goal: str) -> PracticeTask:
    return PracticeTask(level=level, prompt=prompt, goal=goal)


def load_domain_overviews() -> list[DomainOverview]:
    return [
        DomainOverview(
            id=MathDomain.NUMBER_OPERATIONS,
            name="数与运算",
            purpose=("理解数量、数的表示和数量变化，是所有数学学习的底座。"),
            primary_scope=["整数", "小数", "分数", "四则运算", "运算律"],
            junior_scope=["有理数", "实数", "代数式运算"],
            related_domains=[MathDomain.ALGEBRA_EQUATIONS, MathDomain.STATISTICS_PROBABILITY],
            common_breaks=[
                "不理解单位1",
                "分数只会算不会解释",
                "运算律只会背公式",
            ],
        ),
        DomainOverview(
            id=MathDomain.ALGEBRA_EQUATIONS,
            name="代数与方程",
            purpose=("把现实数量关系翻译成符号，并通过等价变形解决未知量。"),
            primary_scope=["等量关系", "用字母表示数", "简易方程"],
            junior_scope=["整式", "一元一次方程", "二元一次方程组", "不等式"],
            related_domains=[MathDomain.NUMBER_OPERATIONS, MathDomain.FUNCTIONS],
            common_breaks=[
                "把等号当结果提示",
                "移项不理解等式性质",
                "不会从应用题找数量关系",
            ],
        ),
        DomainOverview(
            id=MathDomain.GEOMETRY,
            name="图形与几何",
            purpose="研究形状、位置、大小和空间关系。",
            primary_scope=["平面图形", "周长", "面积", "体积", "角"],
            junior_scope=["相交线和平行线", "三角形", "全等", "相似", "圆"],
            related_domains=[MathDomain.NUMBER_OPERATIONS, MathDomain.MATHEMATICAL_THINKING],
            common_breaks=["面积和周长混淆", "不会从图形直觉过渡到证明"],
        ),
        DomainOverview(
            id=MathDomain.FUNCTIONS,
            name="函数与变化关系",
            purpose="描述一个量变化时另一个量如何跟着变化。",
            primary_scope=["数量关系", "表格", "简单变化规律"],
            junior_scope=["函数概念", "一次函数", "反比例函数", "二次函数直觉"],
            related_domains=[MathDomain.ALGEBRA_EQUATIONS, MathDomain.MODELING_APPLICATIONS],
            common_breaks=[
                "直接背定义",
                "不理解输入输出",
                "不会把表格、图像和表达式互相转换",
            ],
        ),
        DomainOverview(
            id=MathDomain.STATISTICS_PROBABILITY,
            name="统计与概率",
            purpose="用数据和可能性描述不确定世界。",
            primary_scope=["收集数据", "平均数", "简单统计图"],
            junior_scope=["抽样", "频数分布", "概率初步"],
            related_domains=[MathDomain.NUMBER_OPERATIONS, MathDomain.MODELING_APPLICATIONS],
            common_breaks=["平均数含义薄弱", "概率只记公式不理解样本空间"],
        ),
        DomainOverview(
            id=MathDomain.MATHEMATICAL_THINKING,
            name="数学思想方法",
            purpose="沉淀分类、转化、数形结合、方程思想等跨章节方法。",
            primary_scope=["分类", "对应", "画图", "逆向思考"],
            junior_scope=["转化思想", "数形结合", "分类讨论", "归纳和证明"],
            related_domains=[
                MathDomain.NUMBER_OPERATIONS,
                MathDomain.ALGEBRA_EQUATIONS,
                MathDomain.GEOMETRY,
            ],
            common_breaks=["只学题型不抽象方法", "遇到新题不会迁移"],
        ),
        DomainOverview(
            id=MathDomain.MODELING_APPLICATIONS,
            name="建模与应用题",
            purpose="把现实问题拆成量、关系、条件和目标。",
            primary_scope=["文字题", "线段图", "比例应用", "行程和工程问题"],
            junior_scope=["方程建模", "函数建模", "统计建模"],
            related_domains=[MathDomain.ALGEBRA_EQUATIONS, MathDomain.FUNCTIONS],
            common_breaks=[
                "关键词套公式",
                "找不到未知量",
                "不会检验答案是否符合现实",
            ],
        ),
    ]


def load_roadmap_items() -> list[RoadmapItem]:
    return [
        RoadmapItem(
            id="quantity_sense",
            name="数量感与四则运算",
            domain=MathDomain.NUMBER_OPERATIONS,
            stage=GradeBand.PRIMARY,
            core_topic_ids=["arithmetic_operations"],
            next_item_ids=["fraction_decimal_ratio", "equation_readiness"],
            is_foundational=True,
            early_intuition="数表示多少，运算表示数量动作。",
        ),
        RoadmapItem(
            id="fraction_decimal_ratio",
            name="分数、小数、比和比例",
            domain=MathDomain.NUMBER_OPERATIONS,
            stage=GradeBand.PRIMARY,
            core_topic_ids=["fraction"],
            prerequisite_topic_ids=["arithmetic_operations"],
            next_item_ids=["equation_readiness", "probability_intro"],
            is_breakpoint=True,
            early_intuition="先抓住单位1和平均分，再进入符号运算。",
        ),
        RoadmapItem(
            id="equation_readiness",
            name="等量关系与方程准备",
            domain=MathDomain.ALGEBRA_EQUATIONS,
            stage=GradeBand.BRIDGE,
            core_topic_ids=["equality", "quantity_relationship"],
            prerequisite_topic_ids=["arithmetic_operations"],
            next_item_ids=["linear_equation_path"],
            is_foundational=True,
            early_intuition="方程来自两边同样多，不是凭空出现的符号游戏。",
        ),
        RoadmapItem(
            id="linear_equation_path",
            name="一元一次方程",
            domain=MathDomain.ALGEBRA_EQUATIONS,
            stage=GradeBand.JUNIOR,
            core_topic_ids=[
                "distributive_property",
                "transposition",
                "linear_equation_one_variable",
            ],
            prerequisite_topic_ids=["equality", "quantity_relationship"],
            next_item_ids=["function_intro_path"],
            is_breakpoint=True,
            early_intuition=("未知数是暂时不知道的量，解方程是在保持等式不变地把它找出来。"),
        ),
        RoadmapItem(
            id="function_intro_path",
            name="函数与变化关系入门",
            domain=MathDomain.FUNCTIONS,
            stage=GradeBand.JUNIOR,
            core_topic_ids=["linear_equation_two_variables", "function_intro"],
            prerequisite_topic_ids=["quantity_relationship", "linear_equation_one_variable"],
            is_breakpoint=True,
            early_intuition=("函数先是生活里的变化关系，再是表格、图像和表达式。"),
        ),
        RoadmapItem(
            id="geometry_measurement",
            name="图形测量到几何推理",
            domain=MathDomain.GEOMETRY,
            stage=GradeBand.BRIDGE,
            core_topic_ids=[],
            is_foundational=True,
            early_intuition="几何先看形状和空间，再把观察变成理由和证明。",
        ),
        RoadmapItem(
            id="probability_intro",
            name="统计与概率初步",
            domain=MathDomain.STATISTICS_PROBABILITY,
            stage=GradeBand.BRIDGE,
            core_topic_ids=[],
            prerequisite_topic_ids=["fraction"],
            early_intuition="概率是在描述可能性，分数是它最早的语言。",
        ),
        RoadmapItem(
            id="high_school_function_path",
            name="高中函数主线",
            domain=MathDomain.FUNCTIONS,
            stage=GradeBand.SENIOR,
            core_topic_ids=[
                "set_concept",
                "function_properties_high_school",
                "exponential_logarithmic_functions",
                "trigonometric_functions",
                "derivative_intro",
            ],
            prerequisite_topic_ids=["function_intro", "quadratic_function"],
            next_item_ids=["high_school_calculus_path"],
            is_breakpoint=True,
            early_intuition="高中函数先说清楚输入范围，再研究整体变化、周期变化和瞬时变化。",
        ),
        RoadmapItem(
            id="high_school_geometry_path",
            name="高中几何与向量",
            domain=MathDomain.GEOMETRY,
            stage=GradeBand.SENIOR,
            core_topic_ids=[
                "plane_vectors",
                "solid_geometry_spatial_relations",
                "space_vectors",
                "conic_sections",
            ],
            prerequisite_topic_ids=["coordinate_plane", "volume"],
            is_breakpoint=True,
            early_intuition="高中几何会把图形关系翻译成向量、坐标和方程。",
        ),
        RoadmapItem(
            id="high_school_probability_path",
            name="高中计数、概率与统计",
            domain=MathDomain.STATISTICS_PROBABILITY,
            stage=GradeBand.SENIOR,
            core_topic_ids=[
                "probability_high_school",
                "counting_principle",
                "random_variables",
                "normal_distribution",
            ],
            prerequisite_topic_ids=["probability", "data_analysis"],
            early_intuition="高中概率先把可能情况数清楚，再研究随机结果的分布。",
        ),
        RoadmapItem(
            id="high_school_calculus_path",
            name="导数与函数研究",
            domain=MathDomain.FUNCTIONS,
            stage=GradeBand.SENIOR,
            core_topic_ids=["derivative_intro", "derivative_applications"],
            prerequisite_topic_ids=["function_properties_high_school"],
            is_breakpoint=True,
            early_intuition="导数是在问变化有多快，用来判断函数增减、最值和图像形状。",
        ),
    ]


def load_knowledge_points() -> list[KnowledgePoint]:
    """Return textbook-aligned seed knowledge points used by the in-memory service."""

    points = _merge_knowledge_points()
    missing_terms = [point.id for point in points if not point.term_explanations]
    if missing_terms:
        raise ValueError(
            "every topic needs term_explanations (plain language first): "
            + ", ".join(missing_terms)
        )
    return points


def _merge_knowledge_points() -> list[KnowledgePoint]:
    core_points = [
        KnowledgePoint(
            id="equality",
            name="等式",
            grade_band=GradeBand.PRIMARY,
            textbook_positions=[
                TextbookPosition(
                    curriculum="中国义务教育数学",
                    grade="小学四年级",
                    chapter="简易方程准备",
                    section="等量关系",
                )
            ],
            human_explanation="等式就是两边表示同样多，像天平保持平衡。",
            life_examples=["两袋苹果一样重", "5元加3元和8元一样多"],
            why_needed="方程和代数推理都要依赖两边保持相等这个想法。",
            formal_definition=("用等号连接、表示左右两个式子值相等的式子叫等式。"),
            term_explanations={
                "等号": "表示左右两边一样多的符号。",
                "式子": "由数、符号或字母组成的一段数学表达。",
            },
            misconceptions=["把等号看成计算结果提示，而不是两边关系。"],
            visualization_methods=["天平模型", "左右两边数量条"],
            ai_teaching_hints=["先用天平解释相等，再引入等号。"],
            exercise_types=["判断等式", "补全等量关系"],
            school_route=["小学", "数与代数", "等量关系"],
            understanding_route=["同样多", "两边平衡", "等号", "等式"],
            conceptual_layers=[
                "等式的第一层意思不是计算，而是左右两边表示同一个数量。",
                "等号像天平中间的支点：左边变了，右边也要用同样方式变，平衡才不会破坏。",
                "等式性质就是“保持一样多”的规则，不是额外背出来的技巧。",
            ],
            worked_examples=[
                _worked(
                    "从天平到等式",
                    "左边是5元和3元，右边是8元，为什么可以写5 + 3 = 8？",
                    [
                        "先看左边：5元和3元合起来是8元。",
                        "再看右边：右边本来就是8元。",
                        "两边虽然写法不同，但表示的钱数一样多，所以用等号连接。",
                        "如果两边同时减去3元，左边剩5元，右边变5元，仍然一样多。",
                    ],
                    "能说出“两边表示同样多”，而不是只说“算出来是8”。",
                )
            ],
            practice_ladder=[
                _task("看懂", "判断 6 + 4 = 10 和 6 + 4 = 9 哪个是等式。", "先看两边是否同样多。"),
                _task("会做", "把“左边和右边一样重”改写成一个等式。", "把语言翻译成符号。"),
                _task("迁移", "说明为什么方程两边同时加2，解不会变。", "把等式性质迁移到方程。"),
            ],
            reflection_questions=[
                "等号两边一定要长得一样吗，还是只要表示的值一样？",
                "为什么等式两边只能做同样的操作？",
            ],
        ),
        KnowledgePoint(
            id="arithmetic_operations",
            name="四则运算",
            grade_band=GradeBand.PRIMARY,
            textbook_positions=[
                TextbookPosition(
                    curriculum="中国义务教育数学",
                    grade="小学三至四年级",
                    chapter="数的运算",
                    section="加减乘除",
                )
            ],
            human_explanation=("四则运算是把数量合起来、拿走、成组增加或平均分。"),
            life_examples=["买东西合计价格", "把糖果平均分给朋友"],
            why_needed="后续分数、方程、函数都要把数量关系写成运算。",
            formal_definition=("加法、减法、乘法、除法及其运算规则共同构成四则运算。"),
            term_explanations={
                "运算": "对数量做动作，比如合起来、拿走、成组或平均分。",
                "规则": "大家约定好的计算办法。",
            },
            misconceptions=["只记步骤，不理解每种运算对应的数量动作。"],
            visualization_methods=["数轴", "阵列图", "平均分模型"],
            ai_teaching_hints=["把运算还原成数量动作。"],
            exercise_types=["口算", "混合运算", "现实问题列式"],
            school_route=["小学", "数与代数", "四则运算"],
            understanding_route=["数量变化", "合并和分开", "成组", "平均分"],
            conceptual_layers=[
                "四种运算就是四种数量动作：加是合起来，减是拿走或比差，乘是相同的组反复加，除是平均分或数组数。",
                "减法是加法的反向，除法是乘法的反向——四种运算其实是两对。",
                "看到应用题先问「数量在做什么动作」，动作找对了，运算符号自然就对了。",
            ],
            worked_examples=[
                _worked(
                    "一道题四种动作",
                    "文具店：一支笔 3 元。买 4 支付 20 元，找回多少？",
                    [
                        "4 支一样的笔是「相同的组」：3×4=12 元，这是乘。",
                        "付 20 元、商品拿走 12 元，剩下的是差：20-12=8 元，这是减。",
                        "一道题里动作可以接着动作：先乘再减，顺序由事情本身决定。",
                    ],
                    "能把式子 20-3×4 里每一步说回「谁在做什么」。",
                ),
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "把加、减、乘、除各配一个生活动作，用一句话说出来。",
                    "四种运算都有画面。",
                ),
                _task(
                    "会做",
                    "看式子 18÷3+2×4，先说每步对应什么动作，再算。",
                    "运算和动作互相翻译。",
                ),
                _task(
                    "迁移",
                    "编一道要用到两种运算的买东西问题，考考别人。",
                    "能反向出题说明真懂了。",
                ),
            ],
            reflection_questions=[
                "加和减是什么关系？乘和除呢？",
                "拿到应用题，第一步该问自己什么？",
                "为什么说乘法是「长大了的加法」？",
            ],
        ),
        KnowledgePoint(
            id="distributive_property",
            name="分配律",
            grade_band=GradeBand.PRIMARY,
            textbook_positions=[
                TextbookPosition(
                    curriculum="中国义务教育数学",
                    grade="小学四年级",
                    chapter="运算律",
                    section="乘法分配律",
                )
            ],
            human_explanation=("分配律说明先拆开再分别乘，和先合起来再乘一样。"),
            life_examples=["3盒彩笔和2盒彩笔，每盒12支，一共还是5盒12支"],
            why_needed="化简式子、解方程和理解面积公式都常用它。",
            formal_definition="a x (b + c) = a x b + a x c。",
            term_explanations={
                "分配": "把一个整体拆成几份后分别处理。",
                "括号": "把里面的内容先看成一个整体的符号。",
            },
            misconceptions=["只会套公式，不知道它来自面积或分组。"],
            prerequisite_ids=["arithmetic_operations"],
            next_ids=["linear_equation_one_variable"],
            formulas=["a x (b + c) = a x b + a x c"],
            visualization_methods=["矩形面积拆分图", "盒装物品分组图"],
            ai_teaching_hints=["先画一个被切开的长方形，再写符号。"],
            exercise_types=["拆括号", "提公因数", "面积模型解释"],
            school_route=["小学", "数与代数", "运算律"],
            understanding_route=["成组数量", "拆开计算", "面积拆分", "符号表达"],
            conceptual_layers=[
                "分配律说的是件日常事：5 盒加 2 盒、每盒 12 支，可以先加盒数再乘，"
                "也可以分别乘了再加，结果一样。",
                "画成长方形最清楚：宽 a、长 (b+c) 的大长方形，等于切成两块分别算面积再拼起来。",
                "反着用叫提公因数：12×7+12×3=12×(7+3)。把共同的「每份」提出来，常常算得飞快。",
            ],
            worked_examples=[
                _worked(
                    "102×7 的聪明算法",
                    "口算 102×7。",
                    [
                        "102 不好直接乘，拆成 100+2。",
                        "用分配律：(100+2)×7 = 100×7 + 2×7 = 700+14。",
                        "所以 102×7=714。拆开算之所以合法，靠的就是分配律，不是投机取巧。",
                    ],
                    "用竖式验算 102×7=714；再试试 98×6=(100−2)×6。",
                ),
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "画一个宽 3、长 (10+4) 的长方形，把 3×(10+4)=3×10+3×4 讲给别人听。",
                    "分配律有图可讲。",
                ),
                _task(
                    "会做",
                    "用分配律口算 45×11 和 99×8。",
                    "拆数计算成为本能。",
                ),
                _task(
                    "迁移",
                    "25×13+25×7 怎么一步算完？提出来的 25 在题里是什么身份？",
                    "提公因数就是分配律反着用。",
                ),
            ],
            reflection_questions=[
                "分配律里被「分配」的是什么？",
                "为什么 3×(10+4) 不等于 3×10+4？",
                "拆数和提公因数，是同一条定律的哪两个方向？",
            ],
        ),
        KnowledgePoint(
            id="fraction",
            name="分数",
            grade_band=GradeBand.PRIMARY,
            textbook_positions=[
                TextbookPosition(
                    curriculum="中国义务教育数学",
                    grade="小学三至五年级",
                    chapter="分数的认识",
                    section="几分之一与几分之几",
                )
            ],
            human_explanation="分数表示把一个整体平均分后取其中几份。",
            life_examples=["半块蛋糕", "四分之三杯水"],
            why_needed=("比例、百分数、概率和代数式都需要表达不是整数的量。"),
            formal_definition=("形如 a/b 的数表示把单位1平均分成b份后取a份，b不为0。"),
            term_explanations={
                "单位1": "这次被当作一个完整整体的东西。",
                "平均分": "每一份大小一样。",
                "分母": "表示整体被平均分成几份的数。",
                "分子": "表示取了其中几份的数。",
            },
            misconceptions=["只看上下两个数，不理解单位1和平均分。"],
            prerequisite_ids=["arithmetic_operations"],
            next_ids=["ratio"],
            formulas=["a/b"],
            visualization_methods=["面积模型", "数轴", "集合模型"],
            ai_teaching_hints=["先确认单位1，再讨论分母和分子。"],
            exercise_types=["识别单位1", "分数大小比较", "分数运算"],
            school_route=["小学", "数与代数", "分数"],
            understanding_route=["整体", "平均分", "取几份", "分数符号"],
            conceptual_layers=[
                "分数先问“这一个整体是谁”，这个整体叫单位1。",
                "只有平均分才有分母；没有平均分，几分之几就没有稳定意义。",
                "分母说单位1被平均分成几份，分子说取了其中几份。",
                "同一个3/4会因为单位1不同而表示不同大小，比如一张纸的3/4和一盒彩笔的3/4。",
            ],
            worked_examples=[
                _worked(
                    "为什么先找单位1",
                    "一盒有12支铅笔，拿走其中的3/4，拿走了多少支？",
                    [
                        "先确认单位1：这里的一盒12支铅笔是一个整体。",
                        "看分母4：把12支平均分成4份，每份是3支。",
                        "看分子3：取其中3份，所以是3 + 3 + 3 = 9支。",
                        "最后检查：拿走的是整盒的一部分，9支小于12支，符合题意。",
                    ],
                    "如果能先说出单位1是12支，而不是直接算3 ÷ 4，就抓住了分数意义。",
                )
            ],
            practice_ladder=[
                _task("看懂", "说出“全班人数的2/5”里单位1是什么。", "先找整体。"),
                _task("会做", "用图表示12的3/4，并写出每一份是多少。", "把平均分和计算连起来。"),
                _task(
                    "迁移",
                    "比较一张大纸的1/2和一张小纸的3/4，能不能只看分数大小。",
                    "理解单位1会影响实际大小。",
                ),
            ],
            reflection_questions=[
                "这道题的单位1是谁？它有没有变过？",
                "分母为什么必须来自平均分？",
                "我的答案和整体大小比起来合理吗？",
            ],
        ),
        KnowledgePoint(
            id="quantity_relationship",
            name="数量关系",
            grade_band=GradeBand.BRIDGE,
            textbook_positions=[
                TextbookPosition(
                    curriculum="中国义务教育数学",
                    grade="小学高年级至初一",
                    chapter="式与方程",
                    section="用字母表示数",
                )
            ],
            human_explanation="数量关系是在说两个或多个数量怎样互相影响。",
            life_examples=["路程会随着时间增加", "总价会随着数量增加"],
            why_needed="函数、方程和应用题建模都从发现数量关系开始。",
            formal_definition=(
                "数量关系是变量或已知量之间可用语言、表格、图像或式子描述的对应规则。"
            ),
            term_explanations={
                "数量": "可以数出来或量出来的多少。",
                "关系": "几个数量之间互相影响的方式。",
                "变量": "会变化的数量。",
            },
            misconceptions=["把应用题当关键词匹配，而不是找量之间的关系。"],
            prerequisite_ids=["arithmetic_operations"],
            next_ids=["function_intro", "linear_equation_one_variable"],
            visualization_methods=["关系表", "箭头图", "线段图"],
            ai_teaching_hints=["先问哪些量会变，再问谁影响谁。"],
            exercise_types=["找已知量和未知量", "用表格整理关系"],
            school_route=["小学到初中", "数与代数", "数量关系"],
            understanding_route=["生活变化", "两个量", "影响关系", "表达关系"],
            conceptual_layers=[
                "应用题不是文字游戏：每道题背后都是几个量在互相影响，先找到量，再找到影响方式。",
                "常见的关系就几种：合起来（部分+部分=总量）、比多少（大数-小数=差）、几倍（每份×份数=总量）。",
                "「小明比小红多 3 个」说的不是小明有几个，是两个量之间差 3——关系本身就是信息。",
            ],
            worked_examples=[
                _worked(
                    "从一句话里找关系",
                    "「买 5 支笔比买 3 支笔多花 6 元」，一支笔多少钱？",
                    [
                        "先找量：5 支的总价、3 支的总价、一支的单价。",
                        "找关系：5 支比 3 支多 2 支，多花的 6 元正是这 2 支的价钱。",
                        "所以一支笔 6÷2=3 元。没列什么公式，只是把「谁比谁多什么」说清楚了。",
                    ],
                    "能画一条线段图，把「多 2 支」和「多 6 元」标在同一段上。",
                ),
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "读一道应用题，先不做，只说出题里有哪几个量、谁影响谁。",
                    "把读题变成找量找关系。",
                ),
                _task(
                    "会做",
                    "用线段图表示「甲比乙多 3 个，甲乙一共 11 个」，再求甲乙。",
                    "关系画出来就好解。",
                ),
                _task(
                    "迁移",
                    "打车费=起步价+每公里单价×公里数。哪些量在变？哪些不变？",
                    "为函数的「变量」做准备。",
                ),
            ],
            reflection_questions=[
                "「比多 3 个」这句话告诉你哪个量的具体数值了吗？",
                "总价、单价、数量三个量，知道其中两个能求第三个吗？",
                "为什么说找关系比记题型更可靠？",
            ],
        ),
        KnowledgePoint(
            id="transposition",
            name="移项",
            grade_band=GradeBand.JUNIOR,
            textbook_positions=[
                TextbookPosition(
                    curriculum="中国义务教育数学",
                    grade="七年级",
                    chapter="一元一次方程",
                    section="解一元一次方程",
                )
            ],
            human_explanation=("移项不是把数随便搬家，而是在等式两边做同样操作后的简写。"),
            life_examples=["天平两边同时拿走同样重的砝码"],
            why_needed=("解方程时要把含未知数的项和常数项整理到合适的位置。"),
            formal_definition=("等式中某一项从一边移到另一边并改变符号，是等式同解变形的简写。"),
            term_explanations={
                "项": "式子里用加号或减号分开的每一块。",
                "变号": "加变成减，或减变成加。",
                "同解": "变形前后能让方程成立的答案一样。",
            },
            misconceptions=[
                "移动时忘记变号",
                "以为移项是独立规则，不理解来自等式性质。",
            ],
            prerequisite_ids=["equality", "arithmetic_operations"],
            next_ids=["linear_equation_one_variable"],
            visualization_methods=["天平变形", "左右式子颜色标注"],
            ai_teaching_hints=["每次移项都还原成两边同时加减同一项。"],
            exercise_types=["移项变形", "判断等价变形"],
            school_route=["初中", "方程", "一元一次方程"],
            understanding_route=[
                "等式平衡",
                "两边同操作",
                "整理未知数",
                "移项简写",
            ],
            conceptual_layers=[
                "移项的底层不是“搬过去变号”，而是等式两边同时加或减同一项。",
                "所谓变号，是把完整操作压缩成一步写法；如果还原出来，就不会觉得神秘。",
                "移项只允许移动加减项，先要看清楚项的边界，不能把乘法或括号里的局部硬搬。",
            ],
            worked_examples=[
                _worked(
                    "把移项还原成等式性质",
                    "x + 3 = 8 为什么能变成 x = 8 - 3？",
                    [
                        "目标是单独留下x，所以要把左边的+3去掉。",
                        "等式两边同时减3：x + 3 - 3 = 8 - 3。",
                        "左边+3和-3抵消，得到x = 8 - 3。",
                        "写快一点，就像把+3移到右边变成-3，但背后仍然是两边同时减3。",
                    ],
                    "能把“移项变号”还原成“两边同时减3”，才算真的懂。",
                )
            ],
            practice_ladder=[
                _task("看懂", "把 x + 5 = 12 的移项步骤写成两边同时减5。", "先还原操作。"),
                _task("会做", "解 2x - 7 = 9，并写出哪一步用了移项。", "把规则用于解方程。"),
                _task("迁移", "判断 3(x + 2) = 15 能不能直接把+2移出去。", "识别项和括号边界。"),
            ],
            reflection_questions=[
                "我移动的是一个完整的项吗？",
                "如果不用“移项”这个词，我能写出两边同操作吗？",
            ],
        ),
        KnowledgePoint(
            id="linear_equation_one_variable",
            name="一元一次方程",
            grade_band=GradeBand.JUNIOR,
            textbook_positions=[
                TextbookPosition(
                    curriculum="中国义务教育数学",
                    grade="七年级",
                    chapter="一元一次方程",
                    section="方程与解法",
                )
            ],
            human_explanation=(
                "一元一次方程就是只有一个未知数，而且未知数只出现一次方的等量关系。"
            ),
            life_examples=["已知总价和单价，求买了多少件"],
            why_needed="它是从算术问题进入代数建模的第一道门。",
            formal_definition=(
                "只含一个未知数，未知数次数为1，且可化为 ax + b = 0 的整式方程叫一元一次方程。"
            ),
            term_explanations={
                "未知数": "现在不知道、需要求出来的数。",
                "一元": "只有一个未知数。",
                "一次": "未知数没有平方、立方，只是普通的一次。",
                "方程": "含有未知数的等式。",
            },
            misconceptions=[
                "把含一个字母的式子都当方程",
                "不知道方程的解是让等式成立的值。",
            ],
            prerequisite_ids=[
                "equality",
                "arithmetic_operations",
                "distributive_property",
                "quantity_relationship",
                "transposition",
            ],
            next_ids=["linear_equation_two_variables", "function_intro"],
            formulas=["ax + b = 0"],
            visualization_methods=["天平模型", "线段图", "步骤树"],
            ai_teaching_hints=["先让学生说出未知量，再把数量关系翻译成等式。"],
            exercise_types=["列方程", "解方程", "检验解"],
            school_route=["初中", "方程", "一元一次方程"],
            understanding_route=["未知数", "等量关系", "列式", "等式变形", "求解"],
            conceptual_layers=[
                "一元一次方程先来自一个现实或数学里的等量关系，不是从ax+b=0突然开始。",
                "一元表示只有一个需要求的未知量；一次表示这个未知量只按普通倍数出现，没有平方。",
                "解方程的目标是把未知数单独留下，同时每一步都保持原来等式的解不变。",
                "检验不是形式动作，而是把求出的数放回原问题，看等量关系是否真的成立。",
            ],
            worked_examples=[
                _worked(
                    "从应用题到方程",
                    "一本练习册8元，买了x本又买一支2元笔，一共26元，求x。",
                    [
                        "先找未知量：不知道买了几本练习册，所以设为x本。",
                        "翻译数量关系：练习册总价是8x元，再加笔2元，一共26元。",
                        "列出等式：8x + 2 = 26。",
                        "两边同时减2，得到8x = 24。",
                        "两边同时除以8，得到x = 3。",
                        "检验：3本练习册24元，加2元是26元，符合题意。",
                    ],
                    "能说清楚8x、+2、=26各自来自题目哪句话。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "指出 5x + 4 = 19 里未知数、常数和等号两边各表示什么。",
                    "读懂方程结构。",
                ),
                _task(
                    "会做",
                    "解 3x - 6 = 12，并每一步写出等式两边做了什么。",
                    "建立等价变形习惯。",
                ),
                _task(
                    "迁移",
                    "把“总价=单价x数量+固定费用”改写成一个一元一次方程。",
                    "从公式迁移到建模。",
                ),
            ],
            reflection_questions=[
                "我设的未知数到底代表什么，有没有单位？",
                "方程左右两边是不是在比较同一种量？",
                "解出来以后代回原题是否合理？",
            ],
        ),
        KnowledgePoint(
            id="linear_equation_two_variables",
            name="二元一次方程",
            grade_band=GradeBand.JUNIOR,
            textbook_positions=[
                TextbookPosition(
                    curriculum="中国义务教育数学",
                    grade="七年级至八年级",
                    chapter="二元一次方程组",
                    section="二元一次方程",
                )
            ],
            human_explanation=("二元一次方程表示两个未知量之间的一条一次关系。"),
            life_examples=["鸡兔同笼中鸡和兔的数量关系"],
            why_needed="它连接方程组、坐标图像和一次函数。",
            formal_definition=("含有两个未知数，且含未知数的项次数都是1的整式方程叫二元一次方程。"),
            term_explanations={
                "二元": "有两个未知数。",
                "解": "能让方程成立的未知数取值。",
                "方程组": "几个方程放在一起，同时要求成立。",
            },
            misconceptions=[
                "以为有两个未知数就一定不能解",
                "不理解一个方程通常对应很多组解。",
            ],
            prerequisite_ids=["linear_equation_one_variable"],
            next_ids=["function_intro"],
            formulas=["ax + by = c"],
            visualization_methods=["解的表格", "坐标系中的直线"],
            ai_teaching_hints=["先用表格列出多组可行解，再过渡到直线图像。"],
            exercise_types=["找整数解", "方程组建模", "图像理解"],
            school_route=["初中", "方程", "二元一次方程组"],
            understanding_route=["两个未知数", "多组解", "表格", "图像直线"],
        ),
        KnowledgePoint(
            id="function_intro",
            name="函数入门",
            grade_band=GradeBand.JUNIOR,
            textbook_positions=[
                TextbookPosition(
                    curriculum="中国义务教育数学",
                    grade="八年级",
                    chapter="函数",
                    section="函数的概念",
                )
            ],
            human_explanation="函数是在描述一个量变了，另一个量怎样跟着变。",
            life_examples=["打车费用随里程变化", "水位随放水时间变化"],
            why_needed=("函数把变化关系变成可以预测、画图和推理的数学对象。"),
            formal_definition=(
                "在某个变化过程中，如果对于变量x的每一个确定值，"
                "变量y都有唯一确定的值与它对应，那么y是x的函数。"
            ),
            term_explanations={
                "变量": "会变化的数量。",
                "输入": "先给进去的那个数或条件。",
                "输出": "根据输入得到的结果。",
                "对应": "一个东西配到另一个东西。",
                "唯一": "只有一个，不会同时出现两个不同结果。",
            },
            misconceptions=["一上来背定义，不知道输入输出和唯一对应是什么意思。"],
            prerequisite_ids=[
                "quantity_relationship",
                "linear_equation_one_variable",
                "linear_equation_two_variables",
            ],
            formulas=["y = f(x)", "y = kx + b"],
            visualization_methods=["输入输出机器", "表格", "坐标图像", "变化故事"],
            ai_teaching_hints=["按生活变化、两个量、输入输出、表格、图像、表达式讲。"],
            exercise_types=["判断函数关系", "表格补全", "读图像", "写表达式"],
            school_route=["初中", "函数", "函数的概念"],
            understanding_route=[
                "生活变化",
                "两个量之间关系",
                "输入输出",
                "表格",
                "图像",
                "函数表达式",
                "正式数学定义",
            ],
            conceptual_layers=[
                "函数先描述变化：一个量变了，另一个量按照某种规则跟着变。",
                "输入是先给的量，输出是跟着确定下来的量；同一个输入只能对应一个输出。",
                "表格、图像、表达式是在说同一个关系的三种语言，不是三块互不相关的内容。",
                "一次函数里的k表示稳定变化速度，b表示输入为0时的起点。",
            ],
            worked_examples=[
                _worked(
                    "从打车费看函数",
                    "起步价8元，每多1千米加2元，路程x千米时费用y元。",
                    [
                        "先找变化的两个量：路程x会变，费用y会跟着变。",
                        "找规则：不管走多远，先有8元起步价。",
                        "每多1千米加2元，所以变化部分是2x。",
                        "写成表达式：y = 2x + 8。",
                        "检查唯一对应：给定x=3千米，费用只能是14元，不会同时有两个费用。",
                    ],
                    "能把同一个关系画成表格、点到图像上，并说出每个点是什么意思。",
                )
            ],
            practice_ladder=[
                _task(
                    "看懂",
                    "判断“一个人对应一个身份证号”是不是函数关系。",
                    "先看输入是否只有一个输出。",
                ),
                _task("会做", "根据y = 2x + 8填出x为0、1、2、3时的表格。", "连接表达式和表格。"),
                _task(
                    "迁移",
                    "看一条直线图像，说出起点和每增加1个单位的变化量。",
                    "从图像读出关系。",
                ),
            ],
            reflection_questions=[
                "我能不能用自己的话说明函数表示哪两个量的关系？",
                "我能不能说出这道题为什么要用它，而不是只因为题目在讲函数？",
                "这里谁是输入，谁是输出？",
                "同一个输入会不会出现两个不同输出？",
                "我能不能把表格、图像、表达式互相翻译？",
            ],
        ),
    ]

    return [
        with_deep_scaffold(point)
        for point in [
            *core_points,
            *load_curriculum_knowledge_points(),
            *load_expanded_knowledge_points(),
            *load_high_school_knowledge_points(),
        ]
    ]


def load_seed_knowledge_points() -> list[KnowledgePoint]:
    return load_knowledge_points()


def content_debt_report() -> list[dict[str, object]]:
    """Topics still carrying template scaffold text, most load-bearing first.

    Load-bearing = number of descendants in the prerequisite graph: filling an
    early prerequisite improves every lesson built on top of it.
    """
    from math_learning_graph.depth import scaffolded_fields
    from math_learning_graph.graph import KnowledgeGraph

    points = load_knowledge_points()
    graph = KnowledgeGraph.from_points(points)
    rows = []
    for point in points:
        fields = scaffolded_fields(point)
        if not fields:
            continue
        rows.append(
            {
                "id": point.id,
                "name": point.name,
                "band": point.grade_band.value,
                "descendants": len(graph.future_topics_for(point.id)),
                "scaffolded": fields,
            }
        )
    rows.sort(key=lambda row: (-int(row["descendants"]), str(row["id"])))
    return rows


if __name__ == "__main__":
    report = content_debt_report()
    total = len(load_knowledge_points())
    print(f"内容欠账：{len(report)}/{total} 个知识点仍在使用模板脚手架（按承重排序）\n")
    print(f"{'知识点':<34}{'学段':<20}{'下游':<6}待补字段")
    for row in report:
        name = f"{row['name']}({row['id']})"
        print(f"{name:<34}{row['band']:<20}{row['descendants']:<6}{','.join(row['scaffolded'])}")
