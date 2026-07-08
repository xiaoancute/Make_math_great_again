from __future__ import annotations

from math_learning_graph.curriculum_seed import load_curriculum_knowledge_points
from math_learning_graph.models import (
    DomainOverview,
    GradeBand,
    KnowledgePoint,
    MathDomain,
    RoadmapItem,
    TextbookPosition,
)


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
    ]


def load_knowledge_points() -> list[KnowledgePoint]:
    """Return textbook-aligned seed knowledge points used by the in-memory service."""

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
        ),
    ]

    return [*core_points, *load_curriculum_knowledge_points()]


def load_seed_knowledge_points() -> list[KnowledgePoint]:
    return load_knowledge_points()
