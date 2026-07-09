import json
from pathlib import Path

from math_learning_graph.android_export import android_topics_payload
from math_learning_graph.service import MathLearningService


ROOT = Path(__file__).resolve().parents[1]
ANDROID_TOPICS = ROOT / "android-app" / "src" / "main" / "assets" / "topics.json"


def test_android_export_uses_backend_learning_order():
    exported = json.loads(android_topics_payload())
    service_topics = [
        topic.model_dump(mode="json")
        for topic in MathLearningService.create_default().list_topics()
    ]

    assert exported == service_topics
    assert [topic["id"] for topic in exported] == [topic["id"] for topic in service_topics]


def test_packaged_android_topics_match_backend_seed():
    packaged = json.loads(ANDROID_TOPICS.read_text(encoding="utf-8"))
    generated = json.loads(android_topics_payload())

    assert packaged == generated
    assert len(packaged) >= 30
