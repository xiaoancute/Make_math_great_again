DO NOT send optional commentary

# Repository Guidelines

## 项目结构与模块组织

这是一个后端优先项目，用于小学到初中数学学习 App 的核心能力，并带一个很薄的 Android 壳子。Python 源码位于 `src/math_learning_graph/`：

- `api.py`：FastAPI 应用和 HTTP 接口。
- `models.py`：Pydantic 数据模型。
- `graph.py`：知识图谱逻辑。
- `review.py`：间隔复习调度。
- `teacher.py`：AI 老师提示词策略。
- `seed.py`：内置种子知识点。

Android 壳子位于 `android-app/`，只负责启动入口和调用后端 API，不承载数学领域逻辑。测试位于 `tests/`，覆盖主要行为，例如 `tests/test_knowledge_graph.py` 和 `tests/test_teacher_policy.py`。项目元数据和工具配置在 `pyproject.toml`、`build.gradle.kts` 和 `settings.gradle.kts`。`prompt.md` 是产品方案提示词，不属于运行时代码。

## 构建、测试与本地开发命令

以下命令是项目可用命令清单。Agent 不要在用户电脑上运行编译、构建或长时间验证命令；需要验证时优先查看或触发 GitHub Actions。

- `python -m pip install -e ".[dev]"`：以可编辑模式安装项目和开发依赖。
- `python -m pytest`：运行 `tests/` 下的全部测试。
- `python -m ruff check src tests`：检查导入、升级建议、常见错误和代码风格。
- `PYTHONPATH=src uvicorn math_learning_graph.api:app --reload`：本地启动 FastAPI 服务。
- `gradle :android-app:assembleDebug`：构建 Android 调试包，应交给 GitHub Actions 执行。

## 代码风格与命名规范

使用 Python 3.11+，尽量保留清晰类型标注。Ruff 行宽为 100，启用 `E`、`F`、`I`、`UP`、`B` 规则。模块应小而直接，名称对应领域职责。函数、变量、模块使用 `snake_case`；Pydantic 模型和类使用 `PascalCase`。

## 测试指南

测试框架使用 `pytest`。新增测试放在 `tests/`，文件命名为 `test_<behavior>.py`。优先测试公开行为，不测试内部实现细节：知识图谱遍历、学习画像输出、复习时间、API 响应和 AI 老师策略。验证优先交给 GitHub Actions；不要默认在本机跑测试或编译。

## 提交与 Pull Request 规范

当前提交历史使用类似 Conventional Commits 的前缀，例如 `test: define math learning core expectations`。提交信息保持简短祈使句，例如 `feat: add topic dependency endpoint` 或 `fix: handle missing review state`。

PR 应包含简洁说明、测试结果、相关 issue；只有当用户可见行为变化时才附 API 示例或截图。

## Agent 专用说明

保持改动范围小。优先扩展现有模块，避免为未来需求添加抽象、样板代码或新目录。

- 不要做 Web 前端；Android 只保留薄壳，领域逻辑放在后端和核心模块。
- 不要重复造轮子；优先参考成熟项目经验、标准库和已安装依赖。
- 不要在用户电脑上跑编译或构建；需要验证时使用 GitHub Actions。
