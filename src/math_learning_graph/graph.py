from __future__ import annotations

import networkx as nx

from math_learning_graph.models import KnowledgePoint, LearningProfile


class KnowledgeGraph:
    def __init__(self, points: list[KnowledgePoint]) -> None:
        self._points = {point.id: point for point in points}
        self._graph = nx.DiGraph()

        for point in points:
            self._graph.add_node(point.id)

        for point in points:
            for prerequisite_id in point.prerequisite_ids:
                if prerequisite_id not in self._points:
                    raise ValueError(
                        f"Knowledge point {point.id} references missing prerequisite "
                        f"{prerequisite_id}"
                    )
                self._graph.add_edge(prerequisite_id, point.id)

    @classmethod
    def from_points(cls, points: list[KnowledgePoint]) -> KnowledgeGraph:
        ids = [point.id for point in points]
        if len(ids) != len(set(ids)):
            raise ValueError("Knowledge point ids must be unique")
        return cls(points)

    def get(self, topic_id: str) -> KnowledgePoint:
        try:
            return self._points[topic_id]
        except KeyError as exc:
            raise KeyError(f"Unknown topic id: {topic_id}") from exc

    def all_points(self) -> list[KnowledgePoint]:
        return [self._points[topic_id] for topic_id in self.learning_order()]

    def is_acyclic(self) -> bool:
        return nx.is_directed_acyclic_graph(self._graph)

    def learning_order(self) -> list[str]:
        return list(nx.topological_sort(self._graph))

    def prerequisites_for(self, topic_id: str) -> list[str]:
        self.get(topic_id)
        ancestors = nx.ancestors(self._graph, topic_id)
        return [node for node in self.learning_order() if node in ancestors]

    def future_topics_for(self, topic_id: str) -> list[str]:
        self.get(topic_id)
        descendants = nx.descendants(self._graph, topic_id)
        return [node for node in self.learning_order() if node in descendants]

    def learning_profile(
        self,
        topic_id: str,
        mastered_topic_ids: set[str],
    ) -> LearningProfile:
        prerequisites = self.prerequisites_for(topic_id)
        mastered = sorted(topic_id for topic_id in mastered_topic_ids if topic_id in prerequisites)
        weak = [topic_id for topic_id in prerequisites if topic_id not in mastered_topic_ids]
        future = self.future_topics_for(topic_id)

        return LearningProfile(
            topic_id=topic_id,
            mastered=mastered,
            weak=weak,
            future=future,
        )
