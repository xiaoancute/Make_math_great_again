from __future__ import annotations

import logging
from collections.abc import Iterator

from math_learning_graph.diagnostic import public_diagnostic_session, score_diagnostic
from math_learning_graph.graph import KnowledgeGraph
from math_learning_graph.models import (
    ChatTurn,
    DiagnosticAnswer,
    DiagnosticResult,
    DiagnosticSession,
    DomainOverview,
    KnowledgePoint,
    LearningProfile,
    RoadmapItem,
    TeacherAnswerResponse,
    TeacherPromptResponse,
    TopicMemoryInput,
)
from math_learning_graph.openai_teacher import TeacherClient, openai_teacher_from_env
from math_learning_graph.seed import (
    load_domain_overviews,
    load_knowledge_points,
    load_roadmap_items,
)
from math_learning_graph.teacher import (
    SECTION_FORMAL,
    answer_respects_term_first,
    build_followup_fallback,
    build_teacher_answer,
    build_teacher_prompt,
)

_logger = logging.getLogger(__name__)


class _TermFirstViolation(Exception):
    """Internal signal: a streamed opening answer broke the terms-before-definition rule."""


class MathLearningService:
    def __init__(
        self,
        graph: KnowledgeGraph,
        domains: list[DomainOverview],
        roadmap: list[RoadmapItem],
        ai_teacher: TeacherClient | None = None,
    ) -> None:
        self._graph = graph
        self._domains = domains
        self._roadmap = roadmap
        self._ai_teacher = ai_teacher

    @classmethod
    def create_default(cls, ai_teacher: TeacherClient | None = None) -> MathLearningService:
        points = load_knowledge_points()
        return cls(
            graph=KnowledgeGraph.from_points(points),
            domains=load_domain_overviews(),
            roadmap=load_roadmap_items(),
            ai_teacher=ai_teacher if ai_teacher is not None else openai_teacher_from_env(),
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

    def diagnostic_session(self) -> DiagnosticSession:
        return public_diagnostic_session()

    def score_diagnostic(self, answers: list[DiagnosticAnswer]) -> DiagnosticResult:
        return score_diagnostic(answers, topic_names=self._topic_names())

    def teacher_prompt(
        self,
        topic_id: str,
        student_age: int,
        question: str,
        mastered_topic_ids: set[str] | None = None,
        placement_level: str | None = None,
        placement_summary: str | None = None,
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
                placement_level=placement_level,
                placement_summary=placement_summary,
            ),
        )

    def teacher_answer(
        self,
        topic_id: str,
        student_age: int,
        question: str,
        mastered_topic_ids: set[str] | None = None,
        memory_records: list[TopicMemoryInput] | None = None,
        model: str | None = None,
        placement_level: str | None = None,
        placement_summary: str | None = None,
        history: list[ChatTurn] | None = None,
    ) -> TeacherAnswerResponse:
        point = self.get_topic(topic_id)
        mastered_topic_ids = mastered_topic_ids or set()
        history = history or []
        profile = self.learning_profile(topic_id, mastered_topic_ids)
        prompt = build_teacher_prompt(
            point,
            student_age=student_age,
            question=question,
            learning_profile=profile,
            topic_names=self._topic_names(),
            memory_records=memory_records or [],
            placement_level=placement_level,
            placement_summary=placement_summary,
            history=history,
        )
        request_teacher = openai_teacher_from_env(model)
        ai_teacher = request_teacher or self._ai_teacher
        if ai_teacher is not None:
            try:
                answer = ai_teacher.generate_answer(prompt)
                # Opening turn must be terms-first; follow-ups are dialogue and exempt.
                if answer and (history or answer_respects_term_first(answer)):
                    return TeacherAnswerResponse(
                        topic_id=topic_id,
                        answer=answer,
                        learning_profile=profile,
                        source="ai",
                    )
                _logger.warning(
                    "AI teacher answer for %s rejected (term-first gate); using local teacher",
                    topic_id,
                )
            except Exception:
                _logger.exception("AI teacher failed for %s; using local teacher", topic_id)
        if history:
            # Mid-conversation: an honest handoff beats re-dumping the opening lesson.
            return TeacherAnswerResponse(
                topic_id=topic_id,
                answer=build_followup_fallback(question),
                learning_profile=profile,
                source="local",
            )
        return TeacherAnswerResponse(
            topic_id=topic_id,
            answer=build_teacher_answer(
                point,
                student_age=student_age,
                question=question,
                learning_profile=profile,
                topic_names=self._topic_names(),
                memory_records=memory_records or [],
                placement_level=placement_level,
                placement_summary=placement_summary,
            ),
            learning_profile=profile,
            source="local",
        )

    def _topic_names(self) -> dict[str, str]:
        return {point.id: point.name for point in self._graph.all_points()}

    def teacher_answer_stream(
        self,
        topic_id: str,
        student_age: int,
        question: str,
        mastered_topic_ids: set[str] | None = None,
        memory_records: list[TopicMemoryInput] | None = None,
        model: str | None = None,
        placement_level: str | None = None,
        placement_summary: str | None = None,
        history: list[ChatTurn] | None = None,
    ) -> Iterator[dict[str, str]]:
        """Yield SSE-ready events: {"type": "delta"|"replace"|"done", ...}.

        The term-first gate runs incrementally on opening turns: the moment the
        formal-definition header arrives before the terms block, the stream is
        cut and replaced by the local teacher. Topic lookup errors raise before
        any event is produced.
        """
        point = self.get_topic(topic_id)
        mastered_topic_ids = mastered_topic_ids or set()
        history = history or []
        profile = self.learning_profile(topic_id, mastered_topic_ids)
        prompt = build_teacher_prompt(
            point,
            student_age=student_age,
            question=question,
            learning_profile=profile,
            topic_names=self._topic_names(),
            memory_records=memory_records or [],
            placement_level=placement_level,
            placement_summary=placement_summary,
            history=history,
        )
        ai_teacher = openai_teacher_from_env(model) or self._ai_teacher

        def local_text() -> str:
            if history:
                return build_followup_fallback(question)
            return build_teacher_answer(
                point,
                student_age=student_age,
                question=question,
                learning_profile=profile,
                topic_names=self._topic_names(),
                memory_records=memory_records or [],
                placement_level=placement_level,
                placement_summary=placement_summary,
            )

        def events() -> Iterator[dict[str, str]]:
            if ai_teacher is None:
                yield {"type": "replace", "text": local_text()}
                yield {"type": "done", "source": "local"}
                return
            accumulated = ""
            try:
                stream_fn = getattr(ai_teacher, "generate_answer_stream", None)
                deltas = (
                    stream_fn(prompt) if stream_fn else iter([ai_teacher.generate_answer(prompt)])
                )
                for delta in deltas:
                    if not delta:
                        continue
                    accumulated += delta
                    if (
                        not history
                        and SECTION_FORMAL in accumulated
                        and not answer_respects_term_first(accumulated)
                    ):
                        raise _TermFirstViolation
                    yield {"type": "delta", "text": delta}
                if not accumulated or (
                    not history and not answer_respects_term_first(accumulated)
                ):
                    raise _TermFirstViolation
                yield {"type": "done", "source": "ai"}
            except _TermFirstViolation:
                _logger.warning(
                    "AI stream for %s rejected (term-first gate); using local teacher",
                    topic_id,
                )
                yield {"type": "replace", "text": local_text()}
                yield {"type": "done", "source": "local"}
            except Exception:
                _logger.exception("AI stream failed for %s; using local teacher", topic_id)
                yield {"type": "replace", "text": local_text()}
                yield {"type": "done", "source": "local"}

        return events()
