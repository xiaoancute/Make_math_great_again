from __future__ import annotations

import argparse
import json
from pathlib import Path

from math_learning_graph.service import MathLearningService


def android_topics_payload() -> str:
    topics = MathLearningService.create_default().list_topics()
    data = [topic.model_dump(mode="json") for topic in topics]
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def export_android_topics(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(android_topics_payload(), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export backend seed topics for Android offline use."
    )
    parser.add_argument(
        "path",
        type=Path,
        help="Output path, e.g. android-app/src/main/assets/topics.json",
    )
    args = parser.parse_args()
    export_android_topics(args.path)


if __name__ == "__main__":
    main()
