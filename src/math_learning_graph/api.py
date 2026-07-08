from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query

from math_learning_graph.models import (
    DomainOverview,
    KnowledgePoint,
    LearningProfile,
    RoadmapItem,
    TeacherAnswerResponse,
    TeacherPromptResponse,
)
from math_learning_graph.service import MathLearningService


def _parse_mastered_ids(mastered: str) -> set[str]:
    return {item.strip() for item in mastered.split(",") if item.strip()}


def create_app() -> FastAPI:
    app = FastAPI(title="Make Math Great Again Core")
    service = MathLearningService.create_default()

    @app.get("/healthz")
    def healthz() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/domains", response_model=list[DomainOverview])
    def list_domains() -> list[DomainOverview]:
        return service.list_domains()

    @app.get("/roadmap", response_model=list[RoadmapItem])
    def list_roadmap() -> list[RoadmapItem]:
        return service.list_roadmap()

    @app.get("/topics", response_model=list[KnowledgePoint])
    def list_topics() -> list[KnowledgePoint]:
        return service.list_topics()

    @app.get("/topics/{topic_id}", response_model=KnowledgePoint)
    def get_topic(topic_id: str) -> KnowledgePoint:
        try:
            return service.get_topic(topic_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.get("/topics/{topic_id}/teacher-prompt", response_model=TeacherPromptResponse)
    def get_teacher_prompt(
        topic_id: str,
        age: int = Query(ge=6, le=16),
        question: str = Query(min_length=1),
        mastered: str = Query(default=""),
    ) -> TeacherPromptResponse:
        try:
            return service.teacher_prompt(
                topic_id,
                student_age=age,
                question=question,
                mastered_topic_ids=_parse_mastered_ids(mastered),
            )
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.get("/topics/{topic_id}/teacher-answer", response_model=TeacherAnswerResponse)
    def get_teacher_answer(
        topic_id: str,
        age: int = Query(ge=6, le=16),
        question: str = Query(min_length=1),
        mastered: str = Query(default=""),
    ) -> TeacherAnswerResponse:
        try:
            return service.teacher_answer(
                topic_id,
                student_age=age,
                question=question,
                mastered_topic_ids=_parse_mastered_ids(mastered),
            )
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.get("/profiles/{topic_id}", response_model=LearningProfile)
    def get_learning_profile(
        topic_id: str,
        mastered: str = Query(default=""),
    ) -> LearningProfile:
        try:
            return service.learning_profile(topic_id, _parse_mastered_ids(mastered))
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    return app


app = create_app()
