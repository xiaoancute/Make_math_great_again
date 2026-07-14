# 开源参考项目

本文记录 MMGA 后续设计和实现时应优先参考的开源项目。参考目标不是照搬产品，而是吸收成熟结构，避免重复造轮子。

## MMGA 的定位

MMGA 不是搜题工具，也不是题海训练 App。核心方向是：

- 中文小学、初中、高中数学教材对齐。
- 校内路线和理解路线并行。
- 用知识图谱找前置漏洞。
- AI 老师先解释术语和直觉，再进入定义、公式和题目。
- 学习记忆长期记录学生已经懂什么、可能缺什么、下一步补什么。

## 重点参考项目

| 项目 | 可参考内容 | 不应照搬的地方 |
|---|---|---|
| [MathClaw](https://github.com/MathClaw-ruc/MathClaw) | 学习记忆、知识点图谱、错题图谱、学习计划、每日/每周总结、多模型配置。 | 不要把 MMGA 做成多通道解题 Agent；MMGA 的主线仍是教材知识体系和前置概念诊断。 |
| [math-knowledge-graph](https://github.com/Jia-Yee/math-knowledge-graph) | 大规模数学知识节点、前置/后续边、节点类型、图谱可视化和数据组织方式。 | 不要直接把庞大图谱塞进 App；必须先筛成适合中小学学习的教材节点和理解节点。 |
| [MathVoice](https://github.com/llSourcell/mathvoice) | 苏格拉底式 AI 老师、结构化输出、掌握度追踪、错误分析、前置解锁、白板思路。 | 不要改成英文 Web 白板产品；MMGA 应保留中文 Android 壳子和本地教材路线。 |
| [zicojiao/ai-math-tutor](https://github.com/zicojiao/ai-math-tutor) | 白板讲解、多模态输入、实时数学辅导体验。 | 暂不把拍照搜题和复杂白板作为主线，除非它服务于概念解释。 |
| [Fractionfrenzy-App-AI-Mathematical-tutor](https://github.com/Denuwanweerakkody/Fractionfrenzy-App-AI-Mathematical-tutor-) | 单一知识域的本体建模、分数概念依赖关系。 | 不要只做单点知识；MMGA 必须保持完整体系骨架。 |

## 后续实现优先级

1. 参考 `math-knowledge-graph`，把 MMGA 的知识点边类型继续规范化：前置、后续、同类、易混、教材包含。
2. 参考 `MathClaw`，把学习记忆拆成更稳定的数据结构：掌握记录、错因记录、复习记录、薄弱前置建议。
3. 参考 `MathVoice`，把 AI 老师响应改成结构化结果：先问卡点、解释词、补直觉、给例子、判断是否理解。
4. 只在概念解释需要时参考白板类项目，不优先做拍题答案流。

## 判断功能是否偏航

新增功能前先问三件事：

- 它是否帮助学生知道“这个概念为什么出现”？
- 它是否帮助系统发现前置知识漏洞？
- 它是否避免默认学生已经理解术语？

如果答案是否定的，即使竞品有这个功能，也不要优先做。
