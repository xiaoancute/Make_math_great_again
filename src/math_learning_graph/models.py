from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class GradeBand(StrEnum):
    PRIMARY = "primary"
    JUNIOR = "junior"
    BRIDGE = "primary_to_junior"


class MathDomain(StrEnum):
    NUMBER_OPERATIONS = "number_operations"
    ALGEBRA_EQUATIONS = "algebra_equations"
    GEOMETRY = "geometry"
    FUNCTIONS = "functions"
    STATISTICS_PROBABILITY = "statistics_probability"
    MATHEMATICAL_THINKING = "mathematical_thinking"
    MODELING_APPLICATIONS = "modeling_applications"


class TextbookPosition(BaseModel):
    model_config = ConfigDict(frozen=True)

    curriculum: str
    grade: str
    chapter: str
    section: str


class KnowledgePoint(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    grade_band: GradeBand
    textbook_positions: list[TextbookPosition] = Field(default_factory=list)
    human_explanation: str
    life_examples: list[str] = Field(default_factory=list)
    why_needed: str
    formal_definition: str
    term_explanations: dict[str, str] = Field(default_factory=dict)
    misconceptions: list[str] = Field(default_factory=list)
    prerequisite_ids: list[str] = Field(default_factory=list)
    next_ids: list[str] = Field(default_factory=list)
    formulas: list[str] = Field(default_factory=list)
    visualization_methods: list[str] = Field(default_factory=list)
    ai_teaching_hints: list[str] = Field(default_factory=list)
    exercise_types: list[str] = Field(default_factory=list)
    school_route: list[str] = Field(default_factory=list)
    understanding_route: list[str] = Field(default_factory=list)


class LearningProfile(BaseModel):
    model_config = ConfigDict(frozen=True)

    topic_id: str
    mastered: list[str]
    weak: list[str]
    future: list[str]


class DomainOverview(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: MathDomain
    name: str
    purpose: str
    primary_scope: list[str] = Field(default_factory=list)
    junior_scope: list[str] = Field(default_factory=list)
    related_domains: list[MathDomain] = Field(default_factory=list)
    common_breaks: list[str] = Field(default_factory=list)


class RoadmapItem(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    domain: MathDomain
    stage: GradeBand
    core_topic_ids: list[str] = Field(default_factory=list)
    prerequisite_topic_ids: list[str] = Field(default_factory=list)
    next_item_ids: list[str] = Field(default_factory=list)
    is_foundational: bool = False
    is_breakpoint: bool = False
    early_intuition: str = ""


class TeacherPromptResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    topic_id: str
    prompt: str


class TeacherAnswerResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    topic_id: str
    answer: str
    learning_profile: LearningProfile | None = None
