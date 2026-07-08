from __future__ import annotations

from math_learning_graph.graph import KnowledgeGraph
from math_learning_graph.models import (
    DomainOverview,
    KnowledgePoint,
    LearningProfile,
    RoadmapItem,
    TeacherAnswerResponse,
    TeacherPromptResponse,
)
from math_learning_graph.seed import (
    load_domain_overviews,
    load_knowledge_points,
    load_roadmap_items,
)
from math_learning_graph.teacher import build_teacher_answer, build_teacher_prompt


class MathLearningService:
    def __init__(
        self,
        graph: KnowledgeGraph,
        domains: list[DomainOverview],
        roadmap: list[RoadmapItem],
    ) -> None:
        self._graph = graph
        self._domains = domains
        self._roadmap = roadmap

    @classmethod
    def create_default(cls) -> MathLearningService:
        points = load_knowledge_points()
        return cls(
            graph=KnowledgeGraph.from_points(points),
            domains=load_domain_overviews(),
            roadmap=load_roadmap_items(),
        )

    def list_domains(self) -> list[DomainOverview]:
        return self._domains

    def list_roadmap(self) -> list[RoadmapItem]:
        return self._roadmap

    def list_topics(self) -> list[KnowledgePoint]:
        return [self._graph.get(topic_id) for topic_id in self._graph.learning_order()]

    def get_topic(self, topic_id: str) -> KnowledgePoint:
        return self._graph.get(topic_id)

    def learning_profile(self, topic_id: str, mastered_topic_ids: set[str]) -> LearningProfile:
        return self._graph.learning_profile(topic_id, mastered_topic_ids)

    def teacher_prompt(
        self,
        topic_id: str,
        student_age: int,
        question: str,
        mastered_topic_ids: set[str] | None = None,
    ) -> TeacherPromptResponse:
        point = self.get_topic(topic_id)
        mastered_topic_ids = mastered_topic_ids or set()
        profile = self.learning_profile(topic_id, mastered_topic_ids)
        return TeacherPromptResponse(
            topic_id=topic_id,
            prompt=build_teacher_prompt(
                point,
                student_age=student_age,
                question=question,
                learning_profile=profile,
                topic_names=self._topic_names(),
            ),
        )

    def teacher_answer(
        self,
        topic_id: str,
        student_age: int,
        question: str,
        mastered_topic_ids: set[str] | None = None,
    ) -> TeacherAnswerResponse:
        point = self.get_topic(topic_id)
        mastered_topic_ids = mastered_topic_ids or set()
        profile = self.learning_profile(topic_id, mastered_topic_ids)
        return TeacherAnswerResponse(
            topic_id=topic_id,
            answer=build_teacher_answer(
                point,
                student_age=student_age,
                question=question,
                learning_profile=profile,
                topic_names=self._topic_names(),
            ),
            learning_profile=profile,
        )

    def _topic_names(self) -> dict[str, str]:
        return {point.id: point.name for point in self._graph.all_points()}
